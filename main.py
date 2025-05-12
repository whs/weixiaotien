import os
from pathlib import Path
from typing import Union, Optional
import re

import pydantic_ai.models
import requests
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from evaluator import Result, prompt, Output, grade
import evaluator

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
    provider: Optional[str] = None
    pydantic_output: Optional[AgentRunResult[Output]] = None
    openai_response: Optional[dict] = None
    ollama_response: Optional[dict] = None

    def get_raw_output(self) -> Optional[Union[AgentRunResult[Output], dict]]:
        if self.pydantic_output:
            return self.pydantic_output
        if self.openai_response:
            return self.openai_response
        if self.ollama_response:
            return self.ollama_response

        return self.result.output

def evaluate_model_pydantic(model: pydantic_ai.models.Model):
    agent = Agent(model, retries=5)

    provider = "unknown"
    if "openrouter" in model.base_url:
        provider = "openrouter"
    elif "localhost" in model.base_url:
        provider = "ollama"

    out_file = Path("result") / (slugify(model.model_name) + ".json")

    with out_file.open("w") as fp:
        result_data = ResultData(
            version=CURRENT_TEST_VERSION,
            model=model.model_name,
            result=None,
            error=None,
            score=0,
            pydantic_output=None,
            provider=f"{provider}_pydantic",
        )
        try:
            output = agent.run_sync(prompt, output_type=Output)
            result = grade(output.output)
            result_data.result = result
            result_data.score = result.score
            result_data.pydantic_output = output

            print(f"Found relationship: {len(result.valid_relationships)} + {len(result.valid_optional_relationships)}")
            print(f"Found party members: {len(result.valid_party_member_list)}")
            print(f"Score: {result.score}")
        except Exception as e:
            result_data.error = repr(e)
            raise e
        finally:
            fp.write(result_data.model_dump_json(indent=4))

def evaluate_model_openai(model: str, provider: str, completion_url: str, headers: Optional[dict]=None, api_params: Optional[dict]=None):
    if not api_params:
        api_params = {}

    resp = requests.post(completion_url, json={
        "model": model,
        "messages": [
            {"role": "user", "content": evaluator.prompt},
        ],
        "temperature": 0,
        "response_format": {
            "type": "json_schema",
            "json_schema": Output.model_json_schema(mode="serialization"),
        },
        **api_params,
    }, headers=headers)

    out_file = Path("result") / (slugify(model) + ".json")

    with out_file.open("w") as fp:
        result_data = ResultData(
            version=CURRENT_TEST_VERSION,
            model=model,
            result=None,
            error=None,
            score=0,
            provider=provider,
            openai_response=resp.json()
        )

        try:
            body = resp.json()
            result_data.openai_response = body

            resp.raise_for_status()

            response_text: str = body['choices'][-1]['message']['content']
            response_text = response_text.removeprefix("```json").removeprefix("```").removesuffix("```")
            output = Output.model_validate_json(response_text)
            result = grade(output)
            result_data.result = result
            result_data.score = result.score
        except Exception as e:
            result_data.error = repr(e)
            raise e
        finally:
            fp.write(result_data.model_dump_json(indent=4))

def evaluate_model_ollama(model: str, provider: str, completion_url: str, api_params: Optional[dict]=None):
    # Seems that OpenAI-compatible endpoint on Ollama doesn't actually work with Structured output...
    if not api_params:
        api_params = {}

    resp = requests.post(completion_url, json={
        "model": model,
        "messages": [
            {"role": "user", "content": evaluator.prompt},
        ],
        "temperature": 0,
        "stream": False,
        "format": Output.model_json_schema(mode="serialization"),
        **api_params,
    })

    out_file = Path("result") / (slugify(model) + ".json")

    with out_file.open("w") as fp:
        result_data = ResultData(
            version=CURRENT_TEST_VERSION,
            model=model,
            result=None,
            error=None,
            score=0,
            provider=provider,
        )

        try:
            body = resp.json()
            result_data.ollama_response = body

            resp.raise_for_status()

            response_text: str = body['message']['content']
            output = Output.model_validate_json(response_text)
            result = grade(output)
            result_data.result = result
            result_data.score = result.score
        except Exception as e:
            result_data.error = repr(e)
            raise e
        finally:
            fp.write(result_data.model_dump_json(indent=4))

def main_pydantic():
    ollama = OpenAIProvider(base_url='http://localhost:11434/v1')
    openrouter = OpenAIProvider(base_url='https://openrouter.ai/api/v1', api_key=os.environ.get("OPENROUTER_KEY", ""))
    models = [
        # Thai LLMs on Ollama
        # OpenAIModel(model_name="PetrosStav/gemma3-tools:27b", provider=ollama),
        # OpenAIModel(model_name="hf.co/mradermacher/openthaigpt1.5-72b-instruct-i1-GGUF:IQ2_S", provider=ollama),
        # OpenAIModel(model_name="hf.co/mradermacher/openthaigpt1.5-14b-instruct-GGUF:Q8_0", provider=ollama),
        # OpenAIModel(model_name="hf.co/JulienElkaim/Tsunami-1.0-14B-Instruct-Q4_K_M-GGUF:Q4_K_M", provider=ollama),
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
        evaluate_model_pydantic(model)
        print("\n")

def main_openai():
    openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
    headers_openrouter = {
        "Authorization": f"Bearer {os.environ.get("OPENROUTER_KEY", "")}",
    }
    params_openrouter = {
        "usage": {"include": True},
        "provider": {"require_parameters": True},
    }
    # Check that the model support structured_outputs!
    for model in [
        # {"model": "meta-llama/llama-4-maverick", "provider": "openrouter_structured", "completion_url": openrouter_url, "headers": headers_openrouter, "api_params": params_openrouter},
        # {"model": "google/gemini-2.5-flash-preview:thinking", "provider": "openrouter_structured", "completion_url": openrouter_url, "headers": headers_openrouter, "api_params": params_openrouter},
        # {"model": "openai/o4-mini", "provider": "openrouter_structured", "completion_url": openrouter_url, "headers": headers_openrouter, "api_params": params_openrouter},
    ]:
        print(model["model"])
        evaluate_model_openai(**model)
        print("\n")

def main_ollama():
    ollama_chat_url = "http://localhost:11434/api/chat"
    for model in [
        # {"model": "hf.co/mradermacher/openthaigpt1.5-72b-instruct-i1-GGUF:IQ2_S", "provider": "ollama_structured", "completion_url": ollama_chat_url},
        # {"model": "hf.co/tensorblock/OpenThaiLLM-Prebuilt-7B-GGUF:Q8_0", "provider": "ollama_structured", "completion_url": ollama_chat_url},
        # {"model": "PetrosStav/gemma3-tools:27b", "provider": "ollama_structured", "completion_url": ollama_chat_url},
        # {"model": "hf.co/aisingapore/Llama-SEA-LION-v3.5-70B-R-GGUF:Q2_K", "provider": "ollama_structured", "completion_url": ollama_chat_url},
        # {"model": "hf.co/mradermacher/Sailor2-20B-Chat-GGUF:Q8_0", "provider": "ollama_structured", "completion_url": ollama_chat_url},
        {"model": "hf.co/scb10x/typhoon2.1-gemma3-12b-gguf:Q4_K_M", "provider": "ollama_structured", "completion_url": ollama_chat_url},
    ]:
        print(model["model"])
        evaluate_model_ollama(**model)
        print("\n")


if __name__ == "__main__":
    main_pydantic()
    main_openai()
    main_ollama()
