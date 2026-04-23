from typing import Literal, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, AIMessage
from config import llm
from core.state import AgentState

members = ["Researcher", "Analyst", "Editor"]

class RouteResponse(BaseModel):
    next: Literal["FINISH", "Researcher", "Analyst", "Editor"] = Field(
        description="К кому перейти дальше? Выбери FINISH, если работа полностью завершена."
    )
    smalltalk_response: Optional[str] = Field(
        default=None,
        description="Если юзер просто поздоровался, поблагодарил или пишет не по делу (smalltalk) — напиши дружелюбный ответ сюда, а в 'next' укажи FINISH. Иначе оставь пустым."
    )

supervisor_llm = llm.with_structured_output(RouteResponse)

SUPERVISOR_PROMPT = """Ты Supervisor (Управляющий).
Твоя команда: {members}.
Твоя задача — руководить процессом, строго соблюдая пайплайн.

ЖЕСТКИЕ ПРАВИЛА МАРШРУТИЗАЦИИ:
1. Поиск данных -> Researcher.
2. Математика, алгоритмы и написание кода -> Analyst.
3. Финальный текст -> Editor. ВАЖНО: Если Analyst отработал и написал код, ты ОБЯЗАН передать этот код Editor'у для красивого оформления. Запрещено нажимать FINISH сразу после Аналитика!
4. ЗАПРЕЩЕНО вызывать одного и того же агента 2 раза подряд.
5. SMALLTALK: Заполняй 'smalltalk_response' и выбирай 'FINISH' ТОЛЬКО если в сообщении НЕТ конкретной задачи. Если юзер просит "напиши код пожалуйста" — это ЗАДАЧА, а не smalltalk! Не путай вежливость с пустой болтовней.
"""

from langchain_core.messages import AIMessage, SystemMessage 

def supervisor_node(state: AgentState):
    messages_list = state.get("messages", [])

    if messages_list:
        last_sender = getattr(messages_list[-1], "name", "")
        if last_sender == "Editor":
            print("\n[Supervisor] -> Вижу отчет от Редактора. Принудительно завершаю!")
            return {"next": "FINISH"}

    prompt = SystemMessage(content=SUPERVISOR_PROMPT.format(members=", ".join(members)))
    messages = [prompt] + messages_list
    
    print("\n[Supervisor] -> Анализирует задачу...")
    res = supervisor_llm.invoke(messages)
    
    if messages_list:
        last_sender = getattr(messages_list[-1], "name", "")
        
        if last_sender == "Analyst" and res.next == "FINISH":
            print("[Supervisor] -> ВНИМАНИЕ: Аналитик закончил, но Босс хочет FINISH. Принудительно зову Редактора!")
            res.next = "Editor"

        elif res.next == last_sender and res.next != "FINISH":
            print(f"[Supervisor] -> ВНИМАНИЕ: Попытка вызвать {res.next} по кругу! Проталкиваю пайплайн дальше.")
            pipeline = ["Researcher", "Analyst", "Editor", "FINISH"]
            if last_sender in pipeline:
                next_index = pipeline.index(last_sender) + 1
                res.next = pipeline[next_index]
    
    print(f"[Supervisor] -> Выбрал: {res.next}")
    
    update = {"next": res.next}
    
    if res.smalltalk_response:
        print(f"[Supervisor] -> Отвечает сам: {res.smalltalk_response}")
        update["messages"] = [AIMessage(content=res.smalltalk_response, name="Supervisor")]
        
    return update