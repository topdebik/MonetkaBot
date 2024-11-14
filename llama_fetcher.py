import asyncio
from llama_cpp import Llama
import consts

LLM = Llama(model_path=consts.llama_model_path, n_ctx=512)

async def get_answer_from_llama(prompt):
    output = LLM(prompt, max_tokens=0)
    return output


async def get_478_story():
    base_story = consts.base_478_story
    return await get_answer_from_llama(
        "Перефразируй, добавь немного деталей\n" + base_story
    )
