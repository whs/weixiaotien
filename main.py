import os
import re
import typing
from pathlib import Path
from typing import Union, Optional, Literal

import openai
import pydantic
from openai import OpenAI
from openai.types.chat import ChatCompletion
from pydantic import BaseModel

import evaluator
from evaluator import Result, Output, grade

CURRENT_TEST_VERSION = 3


def slugify(i: str) -> str:
    return "--".join(re.findall("[A-Za-z0-9._:-]+", i))


class ResultData(BaseModel):
    version: int = 1
    model: str
    result: Union[Result, None]
    score: float
    error: Optional[str] = None
    provider: Optional[str] = None
    responses: Optional[list[Union[ChatCompletion, typing.Any]]] = None
    convertor: Optional[Union[Literal["self"], str]] = None
    cost: Optional[float] = None


# Set JudgeClient to OpenAI instance that supports tool use
CONVERTOR_CLIENT: OpenAI
CONVERTOR_MODEL: str
CONVERTOR_PARAMS = {}

think_tag_re = re.compile('^<think>.*?</think>', re.DOTALL)

def jsonize_conversion(model_output: str, client: OpenAI, completion_params, retry=3) -> (Optional[Output], list[
    Union[ChatCompletion, typing.Any]]):
    out_response = []

    # Remove thinking tags - ollama doesn't separate thinking output in API
    model_output = think_tag_re.sub('', model_output)

    convertor_params = {
        "messages": [
            {"role": "system", "content": evaluator.json_prompt},
            {"role": "user", "content": model_output},
        ],
        "temperature": 0,
        "tool_choice": {"type": "function", "function": {"name": "output"}},
        "reasoning_effort": "low",
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "output",
                    "strict": True,
                    "parameters": Output.model_json_schema()
                },
            },
        ],
    }
    for i in range(retry):
        try:
            response = client.chat.completions.create(**convertor_params, **completion_params)
            out_response.append(response)
            convertor_params["messages"].append(response.choices[0].message)

            if response.choices[0].message.tool_calls is not None:
                output = Output.model_validate_json(
                    response.choices[0].message.tool_calls[0].function.arguments)
                return output, out_response

            print("Tools not called, asking again")
            convertor_params["messages"].append({
                "role": "system",
                "content": "You must call the tool `output`",
            })
        except openai.BadRequestError as bad_req:
            print("Tool call not supported")
            out_response.append(bad_req.body)
            return None, out_response
        except pydantic.ValidationError as validation_err:
            convertor_params["messages"].append({
                "role": "tool",
                "name": "output",
                "tool_call_id": response.choices[0].message.tool_calls[0].id,
                "content": "Failed to parse tool call. Fix the errors and try again. Error:\n" + str(validation_err),
            })
            print(f"Validation error in try attempt {i}")

    return None, out_response


def evaluate_model(model: str, provider: str, openai_params=None, completion_params=None):
    if openai_params is None:
        openai_params = {}
    if completion_params is None:
        completion_params = {}

    client = OpenAI(**openai_params)
    out_file = Path("result") / (slugify(model) + ".json")
    with out_file.open("w") as fp:
        result_data = ResultData(
            version=CURRENT_TEST_VERSION,
            model=model,
            result=None,
            error=None,
            score=0,
            provider=provider,
            responses=[]
        )

        try:
            # 1) Get the plaintext result from the model
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": evaluator.prompt},
                ],
                temperature=0,
                **completion_params,
            )
            result_data.responses.append(response)

            # # 2) Use tool use to convert into JSON
            output, tool_use_response = jsonize_conversion(response.choices[0].message.content, CONVERTOR_CLIENT, completion_params={
                "model": CONVERTOR_MODEL,
                **CONVERTOR_PARAMS,
            })
            result_data.convertor = CONVERTOR_MODEL
            result_data.responses = result_data.responses + tool_use_response
            result = grade(output)
            result_data.result = result
            result_data.score = result.score
        except Exception as e:
            result_data.error = repr(e)
            raise e
        finally:
            fp.write(result_data.model_dump_json(indent=4))


def main():
    openrouter_args = {
        "provider": "openrouter",
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
    requesty_args = {
        "provider": "requesty",
        "openai_params": {
            "api_key": os.environ.get("REQUESTY_KEY", ""),
            "base_url": "https://router.requesty.ai/v1",
        },
        "completion_params": {
        },
    }
    ollama_args = {
        "provider": "ollama",
        "openai_params": {
            "api_key": "unused",
            "base_url": "http://localhost:11434/v1/",
        },
    }
    import google.auth, google.auth.transport.requests
    credentials, project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    credentials.refresh(google.auth.transport.requests.Request())

    google_args = {
        "provider": "google",
        "openai_params": {
            "api_key": credentials.token,
            "base_url": f"https://aiplatform.googleapis.com/v1/projects/{project_id}/locations/global/endpoints/openapi",
        },
        "completion_params": {
        },
    }

    global CONVERTOR_CLIENT, CONVERTOR_MODEL, CONVERTOR_PARAMS
    convertor_provider = google_args
    CONVERTOR_CLIENT = OpenAI(**convertor_provider["openai_params"])
    CONVERTOR_PARAMS = convertor_provider["completion_params"]
    CONVERTOR_MODEL = "google/gemini-2.5-pro"

    # Check that the model support structured_outputs!
    for model in [
        # {"model": "openai/chatgpt-4o-latest", **requesty_args},
        # {"model": "openai/gpt-4.1", **requesty_args},
        # {"model": "openai/gpt-4.1-mini", **requesty_args},
        # {"model": "openai/gpt-4.1-nano", **requesty_args},
        # {"model": "openai/gpt-4.5-preview", **requesty_args},
        # {"model": "openai/gpt-4o", **requesty_args},
        # {"model": "openai/gpt-4o-mini", **requesty_args},
        # {"model": "openai/o3:flex", **requesty_args},
        # {"model": "openai/o4-mini:flex", **requesty_args},
        # {"model": "google/gemini-2.5-flash-lite-preview-06-17", **openrouter_args},
        # {"model": "google/gemini-2.5-flash", **openrouter_args},
        # {"model": "google/gemini-2.5-pro", **openrouter_args},
        # {"model": "meta-llama/llama-4-maverick", **openrouter_args},
        # {"model": "meta-llama/llama-3.3-70b-instruct", **openrouter_args},
        # {"model": "amazon/nova-pro-v1", **openrouter_args},
        # {"model": "anthropic/claude-3.5-haiku", **openrouter_args},
        # {"model": "anthropic/claude-3.5-sonnet", **openrouter_args},
        # {"model": "anthropic/claude-sonnet-4", **openrouter_args},
        # {"model": "anthropic/claude-opus-4", **openrouter_args},
        # {"model": "deepseek/deepseek-chat-v3-0324", **openrouter_args},
        # {"model": "deepseek/deepseek-r1-0528", **openrouter_args},
        # {"model": "qwen/qwen-max", **openrouter_args},
        # {"model": "qwen/qwen3-235b-a22b", **openrouter_args},
        # {"model": "x-ai/grok-3-beta", **openrouter_args},

        # Ollama
        # {"model": "gemma3:27b", **ollama_args},
        # {"model": "gemma3:12b", **ollama_args},
        # {"model": "hf.co/mradermacher/openthaigpt1.5-72b-instruct-i1-GGUF:IQ2_S", **ollama_args},
        # {"model": "hf.co/tensorblock/OpenThaiLLM-Prebuilt-7B-GGUF:Q8_0", **ollama_args},
        # {"model": "hf.co/aisingapore/Llama-SEA-LION-v3.5-70B-R-GGUF:Q2_K", **ollama_args},
        # {"model": "hf.co/aisingapore/Llama-SEA-LION-v3.5-8B-R-GGUF:F16", **ollama_args},
        # {"model": "hf.co/mradermacher/Sailor2-20B-Chat-GGUF:Q8_0", **ollama_args},
        # {"model": "hf.co/scb10x/typhoon2.1-gemma3-12b-gguf:Q4_K_M", **ollama_args},
        # {"model": "hf.co/JulienElkaim/Tsunami-1.0-14B-Instruct-Q4_K_M-GGUF:Q4_K_M", **ollama_args},
        # {"model": "hf.co/mradermacher/openthaigpt1.5-14b-instruct-GGUF:Q8_0", **ollama_args},
        # {"model": "hf.co/Qwen/Qwen3-32B-GGUF:Q4_K_M", **ollama_args},
        # {"model": "phi4", **ollama_args},
        # {"model": "phi4-reasoning", **ollama_args},
        # {"model": "deepseek-r1:14b", **ollama_args},
        # {"model": "llama3.1:8b", **ollama_args},
    ]:
        print(model["model"])
        evaluate_model(**model)
        print("\n")


if __name__ == "__main__":
    main()
