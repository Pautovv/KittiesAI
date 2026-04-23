from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from config import llm
from tools.agent_tools import search_internet, search_local_database 

PROMPT = """Ты Researcher (Искатель). 
Твоя задача — ТОЛЬКО найти нужные данные.
У тебя есть два инструмента:
1. search_internet — для поиска новостей, цен и публичной информации в интернете.
2. search_local_database — для поиска приватного кода, документации или локальных файлов пользователя.
ВАЖНО: При вызове инструментов передавай аргументы в строгом формате JSON!
ПРАВИЛО: Выпиши найденные данные сухим текстом и ВСЁ. Не извиняйся, не пиши код и не делай расчеты."""

agent = create_agent(
    llm, 
    tools=[search_internet, search_local_database],
    system_prompt=PROMPT
)

def researcher_node(state):
    res = agent.invoke(state)
    return {"messages": [HumanMessage(content=res["messages"][-1].content, name="Researcher")]}