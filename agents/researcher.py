from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from config import llm
from tools.agent_tools import search_internet

PROMPT = """
Ты Researcher (Искатель). 
Твоя задача — искать в интернете максимально точные, актуальные и подробные данные по запросу.
Используй инструмент search_internet. Добывай факты, цифры и ссылки. Никогда не выдумывай информацию.
"""

agent = create_agent(
    llm, 
    tools=[search_internet], 
    state_modifier=PROMPT
)

def researcher_node(state):
    res = agent.invoke(state)
    return {"messages": [HumanMessage(content=res["messages"][-1].content, name="Researcher")]}