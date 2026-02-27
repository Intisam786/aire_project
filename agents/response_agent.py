from autogen import AssistantAgent
from utility.llm_config import llm_config

def get_response_agent():
    return AssistantAgent(
        name="ResponseAgent",
        llm_config=llm_config,
        system_message=(
            "You are a response agent. "
            "For every detected event, suggest the most secure and appropriate response. "
            "In your reply, provide a clear summary of the recommended actions and rationale, but do NOT include any email block or notification instructions. "
        )
    )
