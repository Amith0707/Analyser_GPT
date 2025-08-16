from autogen_ext.models.openai import OpenAIChatCompletionClient

import os
from dotenv import load_dotenv
# load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OPENAI_API_KEY in environment variables.")

def get_model_client():
    openai_model_client=OpenAIChatCompletionClient(
        model='gpt-4o-mini',
        api_key=api_key,
        max_output_tokens=500 #-->For safety
    )
    return openai_model_client