from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from config import llm

PROMPT = """
Ты Editor (Редактор/Критик).
Твоя задача — собрать финальный отчет на основе данных от Искателя и Аналитика.
Проверь информацию на логичность. Напиши красивый, структурированный Markdown-отчет.
Не используй инструменты, просто синтезируй текст.
"""

agent = create_agent(
    llm, 
    tools=[], 
    system_prompt=PROMPT
)

def editor_node(state):
    res = agent.invoke(state)
    return {"messages": [HumanMessage(content=res["messages"][-1].content, name="Editor")]}