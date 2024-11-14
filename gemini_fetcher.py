import google.generativeai as genai
from openvpnclient import OpenVPNClient  # thanks https://github.com/KTH-SSAS/python-openvpn-client
import asyncio
import consts

genai.configure(api_key=consts.GEMINI_TOKEN)
vpn = OpenVPNClient(consts.vpn_file_path)


async def get_answer_from_gemini(prompt):
    vpn.connect()

    model = genai.GenerativeModel("gemini-1.5-flash")
    await asyncio.sleep(0)
    response = model.generate_content(prompt)
    
    vpn.disconnect()
    return response.text


async def get_478_story():
    base_story = consts.base_478_story
    return await get_answer_from_gemini(
        "Перефразируй, добавь немного деталей\n" + base_story
    )
