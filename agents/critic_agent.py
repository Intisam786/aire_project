from autogen.agentchat import AssistantAgent
from utility.llm_config import llm_config

def get_critic_agent():
    return AssistantAgent(
        name="CriticAgent",
        llm_config=llm_config,
        system_message=(
            "You are a critic agent."
            " You will be provided with the event, baseline profiles, and all relevant policy documents, as well as the investigation and response outputs."
            " Your job is to review the investigation and response for completeness, accuracy, and policy/baseline alignment."
            " Reference the baseline profiles and policies in your critique."
            " If the outputs are satisfactory and compliant, respond with 'APPROVE' and a brief justification."
            " If not, provide constructive feedback referencing specific baselines or policies."
            " If you respond with 'APPROVE', you MUST ALWAYS include at the end of your reply a short, structured email block for the security team, summarizing the incident and your final recommendations."
            " The email block MUST be formatted EXACTLY as follows (replace ... with real content, and use the recipient from the event if available):\n"
            "Email To: <recipient email from event>\n"
            "Subject: [Incident] <short summary>\n"
            "Body: <one or two sentences summarizing the incident and your final recommendations>."
            "\nDo not add any extra text after the email block. If you do not follow this format, your response will be rejected."
        )
    )
