from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage
from config import llm
from core.state import AgentState

members = ["Researcher", "Analyst", "Editor"]
options = ["FINISH"] + members

class RouteResponse(BaseModel):
    next: Literal["FINISH", "Researcher", "Analyst", "Editor"] = Field(
        description="Кто должен действовать следующим? Выбери FINISH, если работа полностью завершена."
    )

supervisor_llm = llm.with_structured_output(RouteResponse)

SUPERVISOR_PROMPT = """
Ты Supervisor (Управляющий).
Твоя команда: {members}.
Твоя задача — решить, кто должен действовать следующим, чтобы выполнить запрос пользователя.
- Если нужны данные из сети -> направляй к Researcher.
- Если нужны вычисления или анализ кода -> направляй к Analyst.
- Если данные собраны и нужен финальный отчет -> направляй к Editor.
- Если Editor уже написал финальный отчет и задача решена -> выдай FINISH.

Изучи историю сообщений и выбери следующего исполнителя.
"""

def supervisor_node(state: AgentState):
    prompt = SystemMessage(content=SUPERVISOR_PROMPT.format(members=", ".join(members)))
    messages = [prompt] + state["messages"]
    
    print("\n[Supervisor] -> Думает, кому передать задачу...")
    res = supervisor_llm.invoke(messages)
    print(f"[Supervisor] -> Выбрал: {res.next}")
    
    return {"next": res.next}