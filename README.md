# WeiXiaoTien - a LLM evaluation

[Video of the advertisement](https://www.youtube.com/watch?v=c8LR1_0yc64)

Siang Pure Oil had an advertisement in early 2000 in Wuxia style. It involves an old man and a young hero fighting
then an old lady appears to interrupt the fight by telling the old man is the hero's father. Then the two old people
start telling him his family tree which can get confusing. The narrator interrupts the dizzying hero by advertising
the oil saying that it could help with dizzyness.

I think the story is a good LLM test case! For example, "แม่นาง 14" is a job position, but some LLM do understand it as
real mother (adopted or biological) in family trees.

However, the advertising and its analysis are public for several years so that it is possible that it may end up in
one of the training data, including this repository.

## Result

| #  | Model name                                                     | Score  | Rel       | Party | Invalid          | Cost      | Req / In Tok / Out Tok |
|----|----------------------------------------------------------------|--------|-----------|-------|------------------|-----------|------------------------|
| 1  | gemini-2.5-pro-preview-05-06                                   | 85.45% | 8/8 + 1/3 | 2/2   | Rel 2            | $0.004367 | 3 / 1966 / 191         |
| 2  | gemini-2.5-flash-preview-04-17                                 | 80.00% | 6/8 + 1/3 | 2/2   |                  | $0.000376 | 3 / 1966 / 135         |
| 3  | deepseek/deepseek-r1                                           | 70.00% | 5/8 + 1/3 | 2/2   |                  | $0.017394 | 2 / 3369 / 7206        |
| 4  | anthropic/claude-3.5-sonnet-20240620                           | 62.86% | 5/8 + 1/3 | 2/2   | Rel 1            | $0.012273 | 1 / 2131 / 392         |
| 5  | deepseek/deepseek-chat-v3-0324                                 | 55.00% | 5/8 + 2/3 | 2/2   | Rel 3            | $0.000543 | 1 / 969 / 287          |
| 6  | anthropic/claude-3.5-sonnet                                    | 53.33% | 4/8 + 1/3 | 2/2   | Rel 1            | $0.011817 | 1 / 2169 / 354         |
| 7  | qwen/qwen3-235b-a22b                                           | 52.00% | 4/8 + 0/3 | 2/2   | Rel 1            | $0.014000 | 1 / 1070 / 6925        |
| 8  | openai/gpt-4.1                                                 | 42.22% | 4/8 + 1/3 | 2/2   | Rel 4            | $0.008618 | 2 / 2121 / 547         |
| 9  | anthropic/claude-3.7-sonnet                                    | 40.00% | 3/8 + 1/3 | 2/2   | Rel 2            | $0.012957 | 1 / 2169 / 430         |
| 10 | openai/gpt-4o-2024-11-20                                       | 35.00% | 3/8 + 0/3 | 2/2   | Rel 3            | $0.004635 | 1 / 818 / 259          |
| 11 | meta-llama/llama-3.3-70b-instruct                              | 34.00% | 4/8 + 0/3 | 1/2   | Rel 1 / Party 4  | $0.000847 | 2 / 4623 / 1232        |
| 12 | openai/gpt-4.5-preview                                         | 33.64% | 3/8 + 2/3 | 2/2   | Rel 6            | $0.126900 | 1 / 818 / 437          |
| 13 | gemini-2.0-flash                                               | 22.50% | 1/8 + 0/3 | 2/2   | Rel 3            | $0.000364 | 3 / 1966 / 115         |
| 14 | hf.co/JulienElkaim/Tsunami-1.0-14B-Instruct-Q4_K_M-GGUF:Q4_K_M | 20.00% | 0/8 + 0/3 | 2/2   | Rel 6            | N/A       | 1 / 996 / 258          |
| 15 | PetrosStav/gemma3-tools:27b                                    | 17.50% | 3/8 + 1/3 | 1/2   | Rel 12           | N/A       | 1 / 1099 / 641         |
| 16 | hf.co/mradermacher/openthaigpt1.5-72b-instruct-i1-GGUF:IQ2_S   | 14.00% | 3/8 + 0/3 | 1/2   | Rel 7 / Party 1  | N/A       | 1 / 584 / 421          |
| 17 | hf.co/mradermacher/openthaigpt1.5-14b-instruct-GGUF:Q8_0       | 8.00%  | 0/8 + 0/3 | 2/2   | Rel 4 / Party 3  | N/A       | 2 / 2209 / 500         |
| 18 | anthropic/claude-3.5-haiku                                     | 6.67%  | 0/8 + 0/3 | 2/2   | Rel 6 / Party 4  | $0.020788 | 3 / 13150 / 2567       |
| 19 | anthropic/claude-3.5-haiku-20241022                            | 5.71%  | 0/8 + 0/3 | 2/2   | Rel 6 / Party 5  | $0.025130 | 3 / 12782 / 3726       |
| 20 | hf.co/scb10x/typhoon2.1-gemma3-12b-gguf:Q4_K_M                 | 5.43%  | 2/8 + 1/3 | 1/2   | Rel 12 / Party 6 | N/A       | 1 / 417 / 726          |
| 21 | hf.co/mradermacher/Sailor2-20B-Chat-GGUF:Q8_0                  | 3.33%  | 0/8 + 0/3 | 1/2   | Rel 8 / Party 2  | N/A       | 1 / 584 / 384          |
| 22 | hf.co/tensorblock/OpenThaiLLM-Prebuilt-7B-GGUF:Q8_0            | 0.00%  | 0/8 + 0/3 | 0/2   | Rel 9            | N/A       | 1 / 584 / 276          |
| 23 | hf.co/aisingapore/Llama-SEA-LION-v3.5-70B-R-GGUF:Q2_K          | 0.00%  | 0/8 + 0/3 | 0/2   | Rel 2 / Party 2  | N/A       | 1 / 515 / 119          |
| 24 | meta-llama/llama-4-maverick                                    | DNF    | DNF       | DNF   | DNF              | DNF       | DNF                    |
| 25 | amazon/nova-pro-v1                                             | DNF    | DNF       | DNF   | DNF              | DNF       | DNF                    |
| 26 | qwen/qwen-max                                                  | DNF    | DNF       | DNF   | DNF              | DNF       | DNF                    |
| 27 | google/gemini-2.5-flash-preview:thinking                       | DNF    | DNF       | DNF   | DNF              | DNF       | DNF                    |
| 28 | anthropic/claude-3.7-sonnet:thinking **(test v1)**             | DNF    | DNF       | DNF   | DNF              | DNF       | DNF                    |
| 29 | x-ai/grok-3-beta **(test v1)**                                 | DNF    | DNF       | DNF   | DNF              | DNF       | DNF                    |
| 30 | openai/o4-mini                                                 | DNF    | DNF       | DNF   | DNF              | DNF       | DNF                    |

Gemma3 and Hugging Face models are running in Ollama with default parameters except OLLAMA_FLASH_ATTENTION=1.
The model quantization is chosen to best fit my hardware (1x RTX 5090), which may result in suboptimal performance
compared to the full model.

Commercial models are running via OpenRouter. DNF (Did Not Finish) could be potentially from either the LLM
providers, or OpenRouter. The most common errors are: output schema mismatch, [rate limited](https://github.com/pydantic/pydantic-ai/issues/527).

Gemini models are running via Google Vertex AI, except when prefixed with `google/` which use OpenRouter.

Cost is based on the listed price of that model - the actual inference may have different cost that is not recorded.
I believe that Pydantic underreport the number of tokens, as `total_tokens` is higher than sum of input + output tokens.

Scoring is performed by

1. % of correct relationship (excl. optional relationships)
2. One minus % of relationship outputs that are invalid (for example, if the output returns 9 relationships,
   4 are valid, 3 are valid optional, 2 is invalid then the value is 1-(2/9) = 0.77)
3. $[1] \times [2] \times 0.8$ (Relationship score is 80% of overall score)
4. % of correct party member list
5. One minus % of party member list outputs that are invalid (for example, if the output returns 3 party members,
   2 are valid, 1 is invalid then the value is 1-(1/3) = 0.66)
6. $[4] \times [5] \times 0.2$ (Party member score is 20% of overall score)
7. $[3] + [6]$

For detailed output of each model, see the [result](result) directory.

## The test

The LLM should generate relationship graph from the story. The graph's edges are directional.

There are two LLM harnesses in use. Check which one from the "provider" field in the result JSON. If the field is
missing, then it is Pydantic.

1. Pydantic, which create a response tool to be used with Tool Use. The model receive the JSON Schema and is expected
   to follow it. It get 5 attempts to correct mistakes.
2. Direct API calls with structured output. [This is not supported by Pydantic](https://github.com/pydantic/pydantic-ai/issues/582).
   Models using this method has temperature set to 0. The LLM runtime will choose to output only tokens that are
   semantically correct according to the JSON schema. When this technique is tested with Ollama models, it seems that
   they produced better results than Tool Use. However, it seems that OpenRouter's support of this feature is unstable.
   I believe it also stunted the thinking process of LLMs that are trained to think but doesn't use the proper thinking
   feature.

The correct relationship graph edges are

| Character 1   | Relationship  | Character 2 |
|---------------|---------------|-------------|
| เว้ยเส้าเทียน | สหายรัก       | จางฟู่เหยิน |
| จางฟู่เหยิน | สหายรัก       | เว้ยเส้าเทียน |
| เว้ยเส้าเทียน | พ่อ           | พระเอก      |
| จางม่านจือ    | แม่           | พระเอก      |
| พระเอก | ลูก           | เว้ยเส้าเทียน      |
| พระเอก    | ลูก           | จางม่านจือ      |
| เส้าสี่เฉียน  | พบใกล้หนองน้ำ | พระเอก      |
| จางฟู่เหยิน   | เก็บมาเลี้ยง  | พระเอก      |

As for เซี๊ยะถงอี้, my interpretation differs from [Aquapatindra's interpretation](https://www.facebook.com/photo/?fbid=482218268541373&set=a.276875085742360).
I think "น้าสาวพี่แม่" is doubled as aunt is already means mother's older sister, but Aquapatindra believe that it should be
interpreted as aunt of mother of จางม่านจือ's older sister (the older sister may be born from a different mother).
Hence, her relationship is in optional state which the model can output either types. This is not scored.

Some people and LLM also believe จางม่านจือ and จางฟู่เหยิน is also related by family name. Since the relationship is unclear
it is not evaluated.

Additionally, the model should list the กิเลนขาว party members. The members are

- จางฟู่เหยิน (leader)
- เส้าสื่อเฉียน (14th lady)

## Running

The evaluation is available in the evaluator.py file. This can be imported externally to use in your benchmarks.

The main.py file is used to perform evaluation and recording. The format-result.py file is run to generate the table
above. The table is then reformatted in PyCharm.

## License

This repository is licensed under Apache License 2.0. I intentionally not adding a LICENSE file so that scrappers might
omit this repository.

The story and the video are presumably copyrighted by Siang Pure Oil. I don't have the permission to use it.
