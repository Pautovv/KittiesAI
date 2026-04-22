import chainlit as cl
from langchain_core.messages import HumanMessage
from core.graph import app

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="**KittiesAI готов!**\nНапиши мне сложную задачу для ресерча!"
    ).send()
    cl.user_session.set("state", {"messages": []})

@cl.on_message
async def on_message(message: cl.Message):
    state = cl.user_session.get("state")
    state["messages"].append(HumanMessage(content=message.content, name="User"))
    
    last_agent_response = "Не удалось получить ответ."

    async for event in app.astream(state, {"recursion_limit": 20}):
        for node_name, state_update in event.items():
            if node_name == "Supervisor":
                if "messages" in state_update:
                    new_messages = state_update["messages"]
                    last_agent_response = new_messages[-1].content
                    async with cl.Step(name="Supervisor (Smalltalk)") as step:
                        step.output = last_agent_response
                    state["messages"].extend(new_messages)
                continue 
            
            new_messages = state_update["messages"]
            last_agent_response = new_messages[-1].content
            
            async with cl.Step(name=node_name) as step:
                step.output = last_agent_response
            
            state["messages"].extend(new_messages)

    await cl.Message(content=last_agent_response).send()
    
    cl.user_session.set("state", state)