from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from .config import get_model, SYSTEM_PROMPT
from .tools import tools

def build_agent():
    model = get_model()
    return create_agent(
        model,
        tools,
        system_prompt=SYSTEM_PROMPT,
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={"sql_db_query": True},
                description_prefix="⚠️  Query pending your approval",
            ),
        ],
        checkpointer=InMemorySaver(),
    )