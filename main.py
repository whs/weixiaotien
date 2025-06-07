import os
from pathlib import Path
from typing import Union, Optional
import re

from openai import OpenAI
from openai.types.chat import ChatCompletion
from pydantic import BaseModel

from evaluator import Result, Output, grade
import evaluator

CURRENT_TEST_VERSION = 3

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
    openai_response: Optional[ChatCompletion] = None

def evaluate_model_openai(model: str, provider: str, openai_params=None, completion_params=None):
    if openai_params is None:
        openai_params = {}
    if completion_params is None:
        completion_params = {}

    client = OpenAI(**openai_params)
    response = client.beta.chat.completions.parse(
        model = model,
        messages=[
            {"role": "user", "content": evaluator.prompt},
        ],
        temperature=0,
        response_format=Output,
        **completion_params,
    )

    out_file = Path("result") / (slugify(model) + ".json")

    with out_file.open("w") as fp:
        result_data = ResultData(
            version=CURRENT_TEST_VERSION,
            model=model,
            result=None,
            error=None,
            score=0,
            provider=provider,
            openai_response=response,
        )

        try:
            output = response.choices[0].message.parsed
            result = grade(output)
            result_data.result = result
            result_data.score = result.score
        except Exception as e:
            result_data.error = repr(e)
            raise e
        finally:
            fp.write(result_data.model_dump_json(indent=4))

def main_openai():
    openrouter_args = {
        "provider": "openrouter_structured",
        "openai_params": {
            "api_key": os.environ.get("OPENROUTER_KEY", ""),
            "base_url": "https://openrouter.ai/api/v1/",
        },
        "completion_params": {
            "extra_body": {
                "usage": {"include": True},
                "require_parameters": True,
            }
        },
    }
    ollama_args = {
        "provider": "ollama_structured",
        "openai_params": {
            "api_key": "unused",
            "base_url": "http://localhost:11434/v1/",
        }
    }

    # Check that the model support structured_outputs!
    for model in [
        # {"model": "openai/gpt-4o-mini", **openrouter_args},
        # {"model": "openai/o4-mini", **openrouter_args}, # DNF
        # {"model": "openai/gpt-4.1", **openrouter_args},
        # {"model": "openai/gpt-4.5-preview", **openrouter_args},
        # {"model": "openai/gpt-4o-2024-11-20", **openrouter_args},
        # {"model": "google/gemini-2.5-flash-preview", **openrouter_args}, # DNF
        # {"model": "google/gemini-2.5-flash-preview:thinking", **openrouter_args}, # DNF
        # {"model": "meta-llama/llama-4-maverick", **openrouter_args},
        # {"model": "meta-llama/llama-3.3-70b-instruct", **openrouter_args},
        # {"model": "amazon/nova-pro-v1", **openrouter_args}, # DNF
        # {"model": "anthropic/claude-3.5-haiku", **openrouter_args}, # DNF
        # {"model": "anthropic/claude-3.5-sonnet", **openrouter_args},
        # {"model": "anthropic/claude-3.7-sonnet", **openrouter_args},
        # {"model": "anthropic/claude-3.7-sonnet:thinking", **openrouter_args},
        # {"model": "deepseek/deepseek-chat-v3-0324", **openrouter_args}, # DNF
        # {"model": "deepseek/deepseek-r1", **openrouter_args},
        # {"model": "qwen/qwen-max", **openrouter_args}, # DNF
        # {"model": "qwen/qwen3-235b-a22b", **openrouter_args},
        # {"model": "x-ai/grok-3-beta", **openrouter_args}, # No support

        # Ollama
        # {"model": "PetrosStav/gemma3-tools:27b", **ollama_args},
        # {"model": "hf.co/mradermacher/openthaigpt1.5-72b-instruct-i1-GGUF:IQ2_S", **ollama_args},
        # {"model": "hf.co/tensorblock/OpenThaiLLM-Prebuilt-7B-GGUF:Q8_0", **ollama_args},
        # {"model": "hf.co/aisingapore/Llama-SEA-LION-v3.5-70B-R-GGUF:Q2_K", **ollama_args},
        # {"model": "hf.co/aisingapore/Llama-SEA-LION-v3.5-8B-R-GGUF:F16", **ollama_args},
        # {"model": "hf.co/mradermacher/Sailor2-20B-Chat-GGUF:Q8_0", **ollama_args},
        # {"model": "hf.co/scb10x/typhoon2.1-gemma3-12b-gguf:Q4_K_M", **ollama_args},
        # {"model": "hf.co/JulienElkaim/Tsunami-1.0-14B-Instruct-Q4_K_M-GGUF:Q4_K_M", **ollama_args},
        # {"model": "hf.co/mradermacher/openthaigpt1.5-14b-instruct-GGUF:Q8_0", **ollama_args},
        {"model": "hf.co/Qwen/Qwen3-32B-GGUF:Q4_K_M", **ollama_args},
        # {"model": "phi4", **ollama_args},
    ]:
        print(model["model"])
        evaluate_model_openai(**model)
        print("\n")


if __name__ == "__main__":
    main_openai()
