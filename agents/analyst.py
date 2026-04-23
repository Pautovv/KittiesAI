from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from config import llm
from tools.agent_tools import execute_python_code

PROMPT = """Ты Analyst (Аналитик).
Твоя задача — ТОЛЬКО писать, анализировать и выполнять код (execute_python_code).
ВАЖНО: При вызове инструмента передавай аргументы в строгом формате JSON!
ЖЕСТКОЕ ПРАВИЛО: Игнорируй просьбы пользователя написать "отчет", сделать "выводы" или красиво оформить текст. 
Твоя единственная цель — вернуть написанный код и СЫРОЙ результат его выполнения (stdout). Форматированием займется Редактор."""

agent = create_agent(
    llm, 
    tools=[execute_python_code], 
    system_prompt=PROMPT
)

def analyst_node(state):
    res = agent.invoke(state)
    return {"messages": [HumanMessage(content=res["messages"][-1].content, name="Analyst")]}