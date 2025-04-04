from litellm import acompletion, ChatCompletionAssistantToolCall, ChatCompletionToolCallFunctionChunk
import asyncio
import json
import signal
from r2ai.pipe import get_r2_inst
from r2ai.tools import run_python, r2cmd, execute_binary
from r2ai.repl import r2ai_singleton
from r2ai.auto import ChatAuto, SYSTEM_PROMPT_AUTO
from r2ai.interpreter import is_litellm_model
from r2ai.models import new_get_hf_llm

def signal_handler(signum, frame):
    raise KeyboardInterrupt

async def chat(ai, message, cb):
    model = ai.model.replace(":", "/")
    tools = [r2cmd, run_python, execute_binary]
    ai.messages.append({"role": "user", "content": message})
    tool_choice = 'auto'
    if not is_litellm_model(model) and ai and not ai.llama_instance:
        ai.llama_instance = new_get_hf_llm(ai, model, int(ai.env["llm.window"]))
    
    chat_auto = ChatAuto(model, interpreter=ai, system=SYSTEM_PROMPT_AUTO, tools=tools, messages=ai.messages, tool_choice=tool_choice, cb=cb)

    return await chat_auto.achat()
