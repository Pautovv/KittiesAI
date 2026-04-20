from core.graph import app
from langchain_core.messages import HumanMessage

if __name__ == "__main__":
    print("Ready!")

    while True:
        user_input = input("Запрос: ").strip()
        if user_input.lower() in ["exit", "quit"]: break
        if not user_input: continue

        initial_state = {"messages": [HumanMessage(content=user_input, name="User")]}

        print("\n" + "="*50)
        for event in app.stream(initial_state, {"recursion_limit": 20}):
            for node_name, state_update in event.items():
                if node_name != "Supervisor":
                    last_msg = state_update["messages"][-1]
                    print(f"\n[{node_name}] пишет:\n{last_msg.content}\n" + "-"*50)
        print("="*50 + "\n")