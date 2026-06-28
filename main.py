from langgraph.types import Command
from src.sql_agent.agent import build_agent

agent = build_agent()

def ask(question: str, thread_id: str = "1"):
    config = {"configurable": {"thread_id": thread_id}}

    for step in agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        config,
        stream_mode="values",
    ):
        if "__interrupt__" in step:
            interrupt = step["__interrupt__"][0]
            for req in interrupt.value["action_requests"]:
                print("\n" + req["description"])

            decision = input("\nApprove this query? (y/n): ").strip().lower()
            action = "approve" if decision == "y" else "reject"

            for step2 in agent.stream(
                Command(resume={"decisions": [{"type": action}]}),
                config,
                stream_mode="values",
            ):
                if "messages" in step2:
                    step2["messages"][-1].pretty_print()
            return

        elif "messages" in step:
            step["messages"][-1].pretty_print()

if __name__ == "__main__":
    print("SQL Agent ready. Type 'quit' to exit.\n")
    thread = 1
    while True:
        question = input("Ask a question: ").strip()
        if question.lower() in ("quit", "exit"):
            break
        if question:
            ask(question, thread_id=str(thread))
            thread += 1