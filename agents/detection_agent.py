from autogen import AssistantAgent
from utility.llm_config import llm_config

def get_detection_agent():
    return AssistantAgent(
        name="DetectionAgent",
        llm_config=llm_config,
        system_message=(
            "You are a security detection agent."
            " You will be provided with the event and relevant baseline profile."
            " Your job is to analyze the event, compare it to the baseline, and determine if further investigation is needed."
            " If the event matches the baseline (location, role, time), reduce the risk score and explain why."
            " If the event deviates from the baseline, increase the risk score and explain which attribute(s) are anomalous."
            " Always return a string with your reasoning and reference the baseline context."
        )
    )
