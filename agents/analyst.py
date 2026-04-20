from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from config import llm
from tools.agent_tools import execute_python_code

PROMPT = """
Ты Analyst (Аналитик).
Твоя задача — анализировать данные, делать математические расчеты или писать скрипты.
Используй инструмент execute_python_code (Docker Sandbox).
Всегда пиши рабочий Python-код, используй print() для вывода результатов.
"""

agent = create_agent(
    llm, 
    tools=[execute_python_code], 
    state_modifier=PROMPT
)

def analyst_node(state):
    res = agent.invoke(state)
    return {"messages": [HumanMessage(content=res["messages"][-1].content, name="Analyst")]}