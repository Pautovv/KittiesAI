from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from config import llm

PROMPT = """Ты Editor (Редактор/Критик).
Твоя задача — собрать финальный, красивый Markdown-отчет на основе данных от Искателя и Аналитика.
Обязательно включи в отчет все Python-скрипты, которые написал Аналитик (используй блоки ```python).
Не придумывай ничего от себя, только структурируй и красиво оформляй то, что сделали твои коллеги."""

agent = create_agent(
    llm, 
    tools=[], 
    system_prompt=PROMPT
)

def editor_node(state):
    res = agent.invoke(state)
    return {"messages": [HumanMessage(content=res["messages"][-1].content, name="Editor")]}