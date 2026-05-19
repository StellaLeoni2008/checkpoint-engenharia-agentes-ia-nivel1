# 🖥️  Sistema Inteligente de Moderação com Multiagentes

<img width="1600" height="800" alt="ChatGPT Image 18 de mai  de 2026, 18_22_46" src="https://github.com/user-attachments/assets/378ab335-0f58-4f02-95fe-8cf644f65048" />

Projeto desenvolvido como prova prática do **Checkpoint Nível 1** da carreira **Engenharia de Agentes de IA**.

O sistema utiliza **LangGraph** para orquestrar múltiplos agentes responsáveis por analisar comentários, identificar possíveis violações das diretrizes da comunidade e permitir intervenção humana antes da decisão final.

---

## 📌 Objetivo
Construir um fluxo inteligente de moderação capaz de:
- Analisar comentários automaticamente
- Detectar possíveis violações
- Pesquisar políticas relevantes
- Sugerir ações de moderação
- Permitir intervenção humana (Human in the Loop)
- Atualizar o estado do fluxo dinamicamente

---

## 🧠 Arquitetura do Sistema
O fluxo foi desenvolvido utilizando um grafo de agentes com **LangGraph**.
### Fluxo:
1. O comentário é analisado
2. Caso exista problema:
   - O sistema pesquisa políticas relacionadas
   - Um agente revisa a situação
3. O fluxo pausa para intervenção humana
4. O moderador pode:
   - Confirmar
   - Cancelar
   - Editar justificativas
5. O fluxo continua até a execução final

---

## 🔄 Diagrama do Grafo

<img width="200" height="340" alt="grafo_moderacao - cópia" src="https://github.com/user-attachments/assets/2812fdae-fde8-470b-bfe2-bd7b74816d39" />

---

## 🤖 Agentes

### 🔎 Analyzer Agent
Responsável por analisar o comentário e classificá-lo como:
- spam
- linguagem inadequada
- assédio
- seguro

### 📚 Policy Researcher Agent
Pesquisa diretrizes da comunidade utilizando Tavily Search quando uma possível violação é identificada.

### 🛡️ Review Agent
Define a ação recomendada com base na análise realizada pelos agentes anteriores.

---

## 👤 Human in the Loop
Permite intervenção humana antes da execução final do fluxo.
O moderador pode:
- Aprovar a ação
- Cancelar
- Inserir uma nova justificativa
- Alterar a decisão final do sistema

---

## 🧠 Conceitos Aplicados e Aprendizados
Durante o desenvolvimento deste projeto, foi possível aplicar na prática conceitos fundamentais de arquiteturas multiagentes e workflows inteligentes utilizando LangGraph.

Principais conceitos trabalhados:
- Construção de sistemas multiagentes
- Human in the Loop (HITL)
- Persistência e atualização dinâmica de estado
- Checkpoints para interrupção e retomada do fluxo
- Fluxos condicionais com LangGraph
- Streaming de eventos
- Modularização de agentes
- Separação de responsabilidades entre componentes
- Orquestração de agentes com LangGraph
Além disso, o projeto permitiu compreender melhor como sistemas de IA podem combinar automação com supervisão humana, tornando o fluxo mais seguro, interpretável e próximo de aplicações reais.

---

## ▶️ Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/StellaLeoni2008/checkpoint-engenharia-agentes-ia-nivel1.git
cd checkpoint-engenharia-agentes-ia-nivel1
```

### 2. Crie e ative um ambiente virtual

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_gemini
TAVILY_API_KEY=sua_chave_tavily
```

### 5. Execute o projeto

```bash
python agentes.py
```

---



## Autores 
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/237313711?v=4" width=115><br><sub>Stella Leoni</sub>](https://github.com/StellaLeoni2008) | 
| :---: |


<p align="right">
18/05/2026
