from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from config import llm
from tools.agent_tools import search_internet

PROMPT = """Ты Researcher (Искатель). 
Твоя задача — ТОЛЬКО найти нужные данные в интернете (например, цены, факты, статистику).
Используй инструмент search_internet. 
ВАЖНО: При вызове инструмента передавай аргументы в строгом формате JSON!
ПРАВИЛО: Выпиши найденные данные сухим текстом и ВСЁ. Не извиняйся за то, что не можешь выполнить другие части задачи пользователя (написать код и т.д.). Просто дай цифры."""

agent = create_agent(
    llm, 
    tools=[search_internet], 
    system_prompt=PROMPT
)

def researcher_node(state):
    res = agent.invoke(state)
    return {"messages": [HumanMessage(content=res["messages"][-1].content, name="Researcher")]}