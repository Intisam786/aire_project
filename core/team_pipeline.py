
from autogen.agentchat.groupchat import GroupChat
from agents.detection_agent import get_detection_agent
from agents.investigation_agent import get_investigation_agent
from agents.response_agent import get_response_agent
from agents.critic_agent import get_critic_agent
import uuid
from utility.logger import get_logger
from datetime import datetime

logger = get_logger()

def run_team_investigation(event, trace_id=None, baseline=None):
    if trace_id is None:
        trace_id = str(uuid.uuid4())
    import json
    from rag.azure_search_utils import search_knowledge_base
    rag_results = search_knowledge_base(str(event.dict()), top_k=3)
    rag_context = "\n--- Retrieved Knowledge Base Context ---\n" + "\n\n".join([
        f"{doc['@search.score']:.2f}: {doc.get('content', str(doc))}" for doc in rag_results
    ])

    investigation_agent = get_investigation_agent()
    response_agent = get_response_agent()
    critic_agent = get_critic_agent()
    agents = [investigation_agent, response_agent, critic_agent]
    from autogen.agentchat.groupchat import GroupChatManager
    groupchat = GroupChat(
        agents=agents,
        messages=[],
        speaker_selection_method="manual",
        max_round=3
    )
    chat_manager = GroupChatManager(groupchat)
    logger.info(
        "Team investigation started",
        extra={
            "trace_id": trace_id,
            "event_id": event.event_id,
            "stage": "team_investigation",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": "InvestigationAgent, ResponseAgent, CriticAgent",
            "rag_context": rag_context,
            "baseline": baseline
        }
    )
    # Prepare the initial message for the group chat, injecting RAG context
    initial_message = {
        "role": "user",
        "content": (
            f"Investigate event: {event.dict()}\n"
            f"{rag_context}"
        )
    }
    messages = [initial_message]
    agent_names = ["InvestigationAgent", "ResponseAgent", "CriticAgent"]
    investigation_output = None
    response_output = None
    import re
    from tools.send_email import send_email_gmail
    for idx, agent in enumerate(agents):
        if agent_names[idx] == "InvestigationAgent":
            agent_input = (
                f"Event: {event.dict()}\n"
                f"{rag_context}"
            )
        elif agent_names[idx] == "ResponseAgent":
            agent_input = (
                f"Event: {event.dict()}\n"
                f"{rag_context}"
                f"\nInvestigation Output: {investigation_output if investigation_output else 'N/A'}"
            )
        elif agent_names[idx] == "CriticAgent":
            agent_input = (
                f"Event: {event.dict()}\n"
                f"Baseline Reference: {json.dumps(baseline, indent=2)}\n"
                f"Policy/Knowledge Reference: {rag_context}\n"
                f"Investigation Output: {investigation_output if investigation_output else 'N/A'}\n"
                f"Response Output: {response_output if response_output else 'N/A'}\n"
                f"Please critique the event considering the baseline, policy context, and previous agent outputs."
            )
        else:
            agent_input = (
                f"Event: {event.dict()}\n"
                f"{rag_context}"
            )
        output = agent.generate_reply(messages + [{"role": "user", "content": agent_input}])
        if not output:
            output = "No output returned."
        msg = {
            "role": "assistant",
            "name": agent_names[idx],
            "content": output
        }
        messages.append(msg)
        if agent_names[idx] == "InvestigationAgent":
            investigation_output = output
        if agent_names[idx] == "ResponseAgent":
            response_output = output
        # No email sending here; moved to after CriticAgent
        logger.info(
            "Team agent turn",
            extra={
                "trace_id": trace_id,
                "event_id": event.event_id,
                "stage": "team_investigation",
                "agent_order": idx + 1,
                "agent": agent_names[idx],
                "output": output,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
    # After all agents, check CriticAgent output for APPROVE and email block
    critic_output = messages[-1]["content"]
    mail_sent_flag = False
    if "APPROVE" in critic_output:
        email_match = re.search(r"Email To:\s*(.+)\nSubject:\s*(.+)\nBody:\s*([\s\S]+)", critic_output)
        if email_match:
            to = email_match.group(1).strip()
            subject = email_match.group(2).strip()
            body = email_match.group(3).strip()
            try:
                send_email_gmail(to, subject, body)
                logger.info("Email sent via CriticAgent", extra={"to": to, "subject": subject, "trace_id": trace_id})
                mail_sent_flag = True
            except Exception as e:
                logger.error(f"Failed to send email: {e}", extra={"trace_id": trace_id})
    logger.info(
        "Team investigation finished",
        extra={
            "trace_id": trace_id,
            "event_id": event.event_id,
            "stage": "team_investigation",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "result": critic_output,
            "agent": "InvestigationAgent, ResponseAgent, CriticAgent",
            "mail_sent": mail_sent_flag
        }
    )
    return critic_output
