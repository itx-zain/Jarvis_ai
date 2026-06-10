from speak import speak
from ai_fallback import execute_llm_action

def execute_command(command: str) -> None:
    command = command.lower().strip()
    if not command:
        return
    execute_llm_action(command)
