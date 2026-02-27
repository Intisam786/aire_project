from firewall.validator import validate_and_clean
from detection.rule_engine import detect_suspicious
from agents.detection_agent import get_detection_agent
from agents.investigation_agent import get_investigation_agent
from agents.response_agent import get_response_agent
from autogen import GroupChat, GroupChatManager, UserProxyAgent
from utility.llm_config import llm_config

def process_event(raw_event):
    log, error = validate_and_clean(raw_event)
    if error:
        return f"Rejected: {error}"
    if not detect_suspicious(log):
        return "No threat detected"

    detection_agent = get_detection_agent()
    investigation_agent = get_investigation_agent()
    response_agent = get_response_agent()
    user = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        code_execution_config=False
    )
    groupchat = GroupChat(
        agents=[user, detection_agent, investigation_agent, response_agent],
        messages=[],
        speaker_selection_method="Auto",
        allow_repeat_speaker=False,
        max_round=6
    )
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config
    )
    responses = []
    original_receive = user.receive
    def receive_and_capture(*args, **kwargs):
        if len(args) >= 2:
            message = args[0]
            if isinstance(message, dict):
                content = message.get("content", "")
                if content:
                    responses.append(content)
        return original_receive(*args, **kwargs)
    user.receive = receive_and_capture
    user.initiate_chat(
        recipient=manager,
        message=f"Analyze this event: {log.dict()}"
    )
    user.receive = original_receive
    return responses[-1] if responses else "No response from agents."
