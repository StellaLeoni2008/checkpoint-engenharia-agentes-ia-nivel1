#importações
import os
import uuid
from dotenv import load_dotenv
from typing import TypedDict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_API_KEY')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')

# Criação do AgentState como um TypedDict
class AgentState(TypedDict):
    comentario_original: str
    politicas_relevantes: List[str]
    analise_do_agente: str
    status_da_moderacao: str
    justificativa_final: str
    humano_confirmou: bool

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

# Criação dos nós do grafo
#Agente Analisador
def analyzer_agent(state: AgentState):
    prompt = f"""
    Analise o comentário abaixo e classifique em UMA das categorias:

    - spam
    - linguagem inadequada
    - assédio
    - seguro

    Comentário:
    {state['comentario_original']}

    Responda apenas com o nome da categoria.
    """

    response = model.invoke(prompt)

    return {
        "analise_do_agente": response.content.strip().lower()
    }

# Agente Pesquisador de Políticas
def policy_researcher_agent(state: AgentState):
    if state["analise_do_agente"] in ["spam", "linguagem inadequada", "assédio"]:
        resultado = tavily.search("diretrizes da comunidade para moderação de comentários")
        politicas = [item["content"] for item in resultado.get("results", [])]
        return {"politicas_relevantes": politicas}

    return {"politicas_relevantes": []}

#Agente Revisor
def review_agent(state: AgentState):
    categoria = state["analise_do_agente"]

    if categoria == "spam":
        return {"status_da_moderacao": "Remover por Spam"}

    elif categoria == "linguagem inadequada":
        return {"status_da_moderacao": "Editar por linguagem inadequada"}

    elif categoria == "assédio":
        return {"status_da_moderacao": "Remover por assédio"}

    return {"status_da_moderacao": "Aprovar"}

#Ação Final
def executar_acao_final(state: AgentState):
    if state.get("justificativa_final"):
        return {
            "justificativa_final": state["justificativa_final"]
        }

    if state.get("humano_confirmou"):
        return {
            "justificativa_final": f"Ação final executada: {state['status_da_moderacao']}"
        }

    return {
        "justificativa_final": "Ação cancelada pelo moderador humano."
    }

#Função para verificar o resultado da análise do agente e decidir o próximo passo
def verify_problem(state: AgentState):
    categoria = state["analise_do_agente"]

    if categoria in ["spam", "linguagem inadequada", "assédio"]:
        return "problema"
    return "sem_problema"


# Construa o Grafo
graph = StateGraph(AgentState)

graph.add_node("analyzer_agent", analyzer_agent)
graph.add_node("policy_researcher_agent", policy_researcher_agent)
graph.add_node("review_agent", review_agent)
graph.add_node("executar_acao_final", executar_acao_final)

graph.set_entry_point("analyzer_agent")

graph.add_conditional_edges(
    "analyzer_agent",
    verify_problem,
    {
        "problema": "policy_researcher_agent",
        "sem_problema": END
    }
)

graph.add_edge("policy_researcher_agent", "review_agent")
graph.add_edge("review_agent", "executar_acao_final")
graph.add_edge("executar_acao_final", END)

memory = InMemorySaver()

app = graph.compile(
    checkpointer=memory,
    interrupt_before=["executar_acao_final"]
) 

imagem = app.get_graph().draw_mermaid_png()

with open("grafo_moderacao.png", "wb") as f:
    f.write(imagem)

#Capture a Interrupção
if __name__ == "__main__":
    initial_state = {
        "comentario_original": "Compre agora esse produto grátis clicando no link suspeito!",
        "politicas_relevantes": [],
        "analise_do_agente": "",
        "status_da_moderacao": "",
        "justificativa_final": "",
        "humano_confirmou": False
    }

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    for event in app.stream(initial_state, config=config):
        print(event)

    # 1. Captura o snapshot completo do estado pausado
    snapshot = app.get_state(config)
    estado_atual = snapshot.values

    print("\n--- SNAPSHOT DO ESTADO ATUAL ---")
    print(estado_atual)

    print("\n--- PAUSA PARA INTERVENÇÃO HUMANA ---")
    print("Comentário:", estado_atual["comentario_original"])
    print("Análise:", estado_atual["analise_do_agente"])
    print("Recomendação:", estado_atual["status_da_moderacao"])

    # 2. Permite modificar a justificativa
    nova_justificativa = input(
        "Digite uma nova justificativa final ou pressione ENTER para manter a automática: "
    ).strip()

    escolha = input('Digite "sim" para confirmar ou "não" para cancelar: ').strip().lower()

    # 3. Injeta a nova informação no estado
    if escolha == "sim":
        new_values = {
            "humano_confirmou": True,
            "justificativa_final": nova_justificativa
            if nova_justificativa
            else f"Ação confirmada: {estado_atual['status_da_moderacao']}"
        }
    else:
        new_values = {
            "humano_confirmou": False,
            "status_da_moderacao": "Ação cancelada pelo humano",
            "justificativa_final": nova_justificativa
            if nova_justificativa
            else "Ação cancelada pelo moderador humano."
        }

    # 4. Atualiza o estado do grafo
    app.update_state(config, new_values)

    # 5. Continua a execução
    for event in app.stream(None, config=config):
        print(event)

    estado_final = app.get_state(config).values

    print("\n--- RESULTADO FINAL ---")
    print(estado_final)







