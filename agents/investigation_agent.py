from autogen import AssistantAgent
from utility.llm_config import llm_config

def get_investigation_agent():
    return AssistantAgent(
        name="InvestigationAgent",
        llm_config=llm_config,
        system_message=(
            "You are an investigation agent."
            " You will be provided with the event, baseline profiles, and all relevant policy documents."
            " Your job is to investigate the event for anomalies, policy violations, or suspicious activity."
            " Reference the baseline profiles and policies in your reasoning."
            " Clearly explain any findings, referencing specific baselines or policies as needed."
            " If the event appears normal and compliant, state this explicitly."
            " Always return a string with your reasoning and references."
        )
    )
