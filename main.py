import os
from pathlib import Path
from typing import Union, Optional
import re

from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from evaluator import evaluate, Result

CURRENT_TEST_VERSION = 2

def slugify(i: str) -> str:
    return "--".join(re.findall("[A-Za-z0-9._:-]+", i))

# This is for loading of result file - it is NOT automatically put in
class Cost(BaseModel):
    request_cost_1k: float
    input_token_1m: float
    output_token_1m: float

class ResultData(BaseModel):
    version: int = 1
    model: str
    result: Union[Result, None]
    score: float
    error: Optional[str] = None
    cost: Optional[Cost] = None

def evaluate_model(model):
    agent = Agent(model, retries=5)

    out_file = Path("result") / (slugify(model.model_name) + ".json")

    with out_file.open("w") as fp:
        result_data = ResultData(version=CURRENT_TEST_VERSION, model=model.model_name, result=None, error=None, score=0)
        try:
            out = evaluate(agent)
            result_data.result = out
            result_data.score = out.score
            fp.write(result_data.model_dump_json(indent=4))

            print(f"Found relationship: {len(out.valid_relationships)} + {len(out.valid_optional_relationships)}")
            print(f"Found party members: {len(out.valid_party_member_list)}")
            print(f"Score: {out.score}")
        except Exception as e:
            result_data.error = repr(e)
            fp.write(result_data.model_dump_json(indent=4))
            raise e

def main():
    ollama = OpenAIProvider(base_url='http://localhost:11434/v1')
    openrouter = OpenAIProvider(base_url='https://openrouter.ai/api/v1', api_key=os.environ.get("OPENROUTER_KEY", ""))
    models = [
        # Thai LLMs on Ollama
        # OpenAIModel(model_name="PetrosStav/gemma3-tools:27b", provider=ollama),
        # OpenAIModel(model_name="hf.co/mradermacher/openthaigpt1.5-72b-instruct-i1-GGUF:IQ2_S", provider=ollama),
        # OpenAIModel(model_name="hf.co/mradermacher/openthaigpt1.5-14b-instruct-GGUF:Q8_0", provider=ollama),
        OpenAIModel(model_name="hf.co/JulienElkaim/Tsunami-1.0-14B-Instruct-Q4_K_M-GGUF:Q4_K_M", provider=ollama),
        # OpenAIModel(model_name="hf.co/tensorblock/OpenThaiLLM-Prebuilt-7B-GGUF:Q8_0", provider=ollama),

        # Public models
        # GeminiModel('gemini-2.0-flash', provider='google-vertex'),
        # GeminiModel('gemini-2.5-flash-preview-04-17', provider='google-vertex'),
        # GeminiModel('gemini-2.5-pro-preview-05-06', provider='google-vertex'),
        # OpenAIModel(model_name="amazon/nova-pro-v1", provider=openrouter), # Fail
        # OpenAIModel(model_name="anthropic/claude-3.5-haiku", provider=openrouter),
        # OpenAIModel(model_name="anthropic/claude-3.5-haiku-20241022", provider=openrouter),
        # OpenAIModel(model_name="anthropic/claude-3.5-sonnet", provider=openrouter),
        # OpenAIModel(model_name="anthropic/claude-3.5-sonnet-20240620", provider=openrouter),
        # OpenAIModel(model_name="anthropic/claude-3.7-sonnet", provider=openrouter),
        # OpenAIModel(model_name="anthropic/claude-3.7-sonnet:thinking", provider=openrouter), # Fail
        # OpenAIModel(model_name="deepseek/deepseek-chat-v3-0324", provider=openrouter),
        # OpenAIModel(model_name="deepseek/deepseek-r1", provider=openrouter),
        # OpenAIModel(model_name="google/gemini-2.5-flash-preview:thinking", provider=openrouter),
        # OpenAIModel(model_name="meta-llama/llama-3.3-70b-instruct", provider=openrouter),
        # OpenAIModel(model_name="meta-llama/llama-4-maverick", provider=openrouter), # Fail
        # OpenAIModel(model_name="openai/gpt-4.1", provider=openrouter),
        # OpenAIModel(model_name="openai/gpt-4.5-preview", provider=openrouter),
        # OpenAIModel(model_name="openai/gpt-4o-2024-11-20", provider=openrouter),
        # OpenAIModel(model_name="openai/o4-mini", provider=openrouter), # API error
        # OpenAIModel(model_name="qwen/qwen-max", provider=openrouter), # Fail
        # OpenAIModel(model_name="qwen/qwen3-235b-a22b", provider=openrouter),
        # OpenAIModel(model_name="x-ai/grok-3-beta", provider=openrouter), # API error
    ]

    for model in models:
        print(model.model_name)
        evaluate_model(model)
        print("\n")

if __name__ == "__main__":
    main()
