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

| #  | Model name                                                        | Score  | Rel       | Party | Invalid         | Cost      | Req / In Tok / Out Tok |
|----|-------------------------------------------------------------------|--------|-----------|-------|-----------------|-----------|------------------------|
| 1  | openai/gpt-4.5-preview **(test v1)**                              | 85.45% | 8/8 + 1/3 | 2/2   | Rel 2           | $0.119250 | 1 / 818 / 386          |
| 2  | gemini-2.5-pro-preview-05-06 **(test v1)**                        | 85.45% | 8/8 + 1/3 | 2/2   | Rel 2           | $0.004367 | 3 / 1966 / 191         |
| 3  | gemini-2.5-flash-preview-04-17                                    | 80.00% | 6/8 + 1/3 | 2/2   |                 | $0.000376 | 3 / 1966 / 135         |
| 4  | anthropic/claude-3.5-sonnet-20240620 **(test v1)**                | 70.00% | 5/8 + 1/3 | 2/2   |                 | $0.036702 | 2 / 5584 / 1330        |
| 5  | qwen/qwen3-235b-a22b **(test v1)**                                | 70.00% | 5/8 + 0/3 | 2/2   |                 | $0.016758 | 1 / 1070 / 8304        |
| 6  | anthropic/claude-3.7-sonnet **(test v1)**                         | 62.86% | 5/8 + 1/3 | 2/2   | Rel 1           | $0.039756 | 2 / 5777 / 1495        |
| 7  | anthropic/claude-3.5-sonnet **(test v1)**                         | 53.33% | 4/8 + 1/3 | 2/2   | Rel 1           | $0.007182 | 1 / 2169 / 45          |
| 8  | openai/gpt-4.1 **(test v1)**                                      | 45.00% | 5/8 + 1/3 | 2/2   | Rel 6           | $0.009214 | 2 / 2087 / 630         |
| 9  | deepseek/deepseek-r1 **(test v1)**                                | 35.00% | 2/8 + 1/3 | 2/2   | Rel 1           | $0.038317 | 4 / 7725 / 15805       |
| 10 | openai/gpt-4o-2024-11-20 **(test v1)**                            | 26.00% | 2/8 + 1/3 | 2/2   | Rel 7           | $0.005885 | 1 / 818 / 384          |
| 11 | gemini-2.0-flash                                                  | 22.50% | 1/8 + 0/3 | 2/2   | Rel 3           | $0.000364 | 3 / 1966 / 115         |
| 12 | hf.co/JulienElkaim/Tsunami-1.0-14B-Instruct-Q4_K_M-GGUF:Q4_K_M    | 20.00% | 0/8 + 0/3 | 2/2   | Rel 6           | N/A       | 1 / 996 / 258          |
| 13 | anthropic/claude-3.5-haiku-20241022 **(test v1)**                 | 9.17%  | 1/8 + 0/3 | 2/2   | Rel 3 / Party 4 | $0.032990 | 4 / 21083 / 4031       |
| 14 | hf.co/mradermacher/openthaigpt1.5-14b-instruct-GGUF:Q8_0          | 8.00%  | 0/8 + 0/3 | 2/2   | Rel 4 / Party 3 | N/A       | 2 / 2209 / 500         |
| 15 | anthropic/claude-3.5-haiku **(test v1)**                          | 6.67%  | 0/8 + 1/3 | 2/2   | Rel 4 / Party 4 | $0.009316 | 2 / 7135 / 902         |
| 16 | PetrosStav/gemma3-tools:27b                                       | 5.71%  | 0/8 + 0/3 | 2/2   | Rel 7 / Party 5 | N/A       | 2 / 4100 / 1057        |
| 17 | meta-llama/llama-3.3-70b-instruct **(test v1)**                   | 3.33%  | 1/8 + 1/3 | 0/2   | Rel 4 / Party 4 | $0.001534 | 3 / 8420 / 2219        |
| 18 | google/gemini-2.5-flash-preview:thinking **(test v1)**            | 0.00%  | 0/8 + 0/3 | 0/2   |                 | $0.054661 | 2 / 1619 / 15548       |
| 19 | meta-llama/llama-4-maverick **(test v1)**                         | DNF    | DNF       | DNF   | DNF             | DNF       | DNF                    |
| 20 | amazon/nova-pro-v1 **(test v1)**                                  | DNF    | DNF       | DNF   | DNF             | DNF       | DNF                    |
| 21 | hf.co/tensorblock/OpenThaiLLM-Prebuilt-7B-GGUF:Q8_0 **(test v1)** | DNF    | DNF       | DNF   | DNF             | DNF       | DNF                    |
| 22 | qwen/qwen-max **(test v1)**                                       | DNF    | DNF       | DNF   | DNF             | DNF       | DNF                    |
| 23 | anthropic/claude-3.7-sonnet:thinking **(test v1)**                | DNF    | DNF       | DNF   | DNF             | DNF       | DNF                    |
| 24 | qwen/qwen2.5-vl-72b-instruct **(test v1)**                        | DNF    | DNF       | DNF   | DNF             | DNF       | DNF                    |
| 25 | x-ai/grok-3-beta **(test v1)**                                    | DNF    | DNF       | DNF   | DNF             | DNF       | DNF                    |
| 26 | hf.co/mradermacher/openthaigpt1.5-72b-instruct-i1-GGUF:IQ2_S      | DNF    | DNF       | DNF   | DNF             | DNF       | DNF                    |
| 27 | deepseek/deepseek-chat-v3-0324 **(test v1)**                      | DNF    | DNF       | DNF   | DNF             | DNF       | DNF                    |
| 28 | openai/o4-mini **(test v1)**                                      | DNF    | DNF       | DNF   | DNF             | DNF       | DNF                    |

Gemma3 and Hugging Face models are running in Ollama with default parameters except OLLAMA_FLASH_ATTENTION=1.
The model quantization is chosen to best fit my hardware (1x RTX 5090), which may result in suboptimal performance
compared to the full model.

Commercial models are running via OpenRouter. DNF (Did Not Finish) could be potentially from either the LLM
providers, or OpenRouter. The most common errors are: output schema mismatch, OpenAI API emulation incompatibility.

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

The LLM harness in use is Pydantic, which use Tool Use to enforce that the LLM calls the output function with the
correct JSON schema. The model can correct mistakes up to 5 times. Models that do not support tool use are not
evaluated.

[Structured output is not supported in Pydantic](https://github.com/pydantic/pydantic-ai/issues/582) but may soon change.

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
