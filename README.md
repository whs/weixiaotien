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

(Read notes before using the result!)

| #  | Model name                                                     | Score  | Rel       | Party | Invalid          | Cost      | In Tok / Out Tok |
|----|----------------------------------------------------------------|--------|-----------|-------|------------------|-----------|------------------|
| 1  | anthropic/claude-sonnet-4                                      | 76.00% | 7/8 + 1/3 | 2/2   | Rel 2            | $0.008028 | 1805 / 1171      |
| 2  | anthropic/claude-3.5-sonnet                                    | 71.43% | 6/8 + 0/3 | 2/2   | Rel 1            | $0.007218 | 1758 / 6003      |
| 3  | qwen/qwen-max                                                  | 69.00% | 7/8 + 0/3 | 2/2   | Rel 3            | $0.002805 | 1492 / 1310      |
| 4  | openai/gpt-4.5-preview                                         | 66.67% | 7/8 + 1/3 | 2/2   | Rel 4            | N/A       | 1408 / 1510      |
| 5  | openai/chatgpt-4o-latest                                       | 65.00% | 8/8 + 1/3 | 2/2   | Rel 7            | N/A       | 1517 / 1607      |
| 6  | openai/o3:flex                                                 | 64.44% | 8/8 + 2/3 | 2/2   | Rel 8            | N/A       | 1480 / 9632      |
| 7  | phi4-reasoning                                                 | 63.33% | 5/8 + 1/3 | 2/2   | Party 1          | N/A       | 10640 / 13200    |
| 8  | anthropic/claude-opus-4-20250514                               | 60.83% | 7/8 + 0/3 | 2/2   | Rel 5            | N/A       | 1832 / 1375      |
| 9  | x-ai/grok-3-beta                                               | 57.50% | 5/8 + 1/3 | 2/2   | Rel 2            | $0.009623 | 1671 / 1215      |
| 10 | deepseek/deepseek-r1-0528                                      | 55.00% | 6/8 + 1/3 | 2/2   | Rel 5            | $0.003902 | 1832 / 3414      |
| 11 | meta-llama/llama-3.3-70b-instruct                              | 48.57% | 4/8 + 1/3 | 2/2   | Rel 2            | $0.000202 | 1827 / 1756      |
| 12 | meta-llama/llama-4-maverick                                    | 45.00% | 4/8 + 1/3 | 2/2   | Rel 3            | $0.000676 | 1903 / 1934      |
| 13 | google/gemini-2.5-flash                                        | 42.50% | 6/8 + 0/3 | 2/2   | Rel 10           | $0.000971 | 1448 / 1596      |
| 14 | gemma3:27b                                                     | 40.00% | 4/8 + 0/3 | 2/2   | Rel 4            | N/A       | 1290 / 1057      |
| 15 | google/gemini-2.5-pro                                          | 40.00% | 2/8 + 0/3 | 2/2   |                  | $0.054706 | 1280 / 11270     |
| 16 | openai/gpt-4.1                                                 | 38.79% | 7/8 + 1/3 | 2/2   | Rel 14 / Party 1 | N/A       | 1751 / 2185      |
| 17 | llama3.1:8b                                                    | 35.00% | 6/8 + 0/3 | 1/2   | Rel 6 / Party 1  | N/A       | 1505 / 1396      |
| 18 | hf.co/mradermacher/openthaigpt1.5-72b-instruct-i1-GGUF:IQ2_S   | 35.00% | 3/8 + 0/3 | 2/2   | Rel 3            | N/A       | 1470 / 1618      |
| 19 | openai/gpt-4o                                                  | 31.25% | 3/8 + 0/3 | 2/2   | Rel 5            | N/A       | 1370 / 1285      |
| 20 | hf.co/JulienElkaim/Tsunami-1.0-14B-Instruct-Q4_K_M-GGUF:Q4_K_M | 30.00% | 2/8 + 0/3 | 2/2   | Rel 2            | N/A       | 1367 / 765       |
| 21 | hf.co/mradermacher/openthaigpt1.5-14b-instruct-GGUF:Q8_0       | 27.50% | 2/8 + 1/3 | 2/2   | Rel 5            | N/A       | 1439 / 1220      |
| 22 | deepseek/deepseek-chat-v3-0324                                 | 26.00% | 3/8 + 0/3 | 2/2   | Rel 12           | $0.000964 | 1583 / 1708      |
| 23 | google/gemini-2.5-flash-lite-preview-06-17                     | 25.00% | 2/8 + 0/3 | 2/2   | Rel 6            | $0.000152 | 1352 / 1131      |
| 24 | gemma3:12b                                                     | 23.33% | 2/8 + 0/3 | 2/2   | Rel 10           | N/A       | 1419 / 1515      |
| 25 | openai/gpt-4.1-mini                                            | 20.00% | 0/8 + 0/3 | 2/2   | Rel 12           | N/A       | 1517 / 2003      |
| 26 | anthropic/claude-3.5-haiku                                     | 20.00% | 0/8 + 0/3 | 2/2   | Rel 5            | $0.001845 | 1759 / 1204      |
| 27 | amazon/nova-pro-v1                                             | 20.00% | 0/8 + 0/3 | 2/2   | Rel 11           | $0.001833 | 2798 / 3320      |
| 28 | hf.co/mradermacher/Sailor2-20B-Chat-GGUF:Q8_0                  | 20.00% | 0/8 + 0/3 | 2/2   | Rel 11           | N/A       | 1641 / 1551      |
| 29 | hf.co/Qwen/Qwen3-32B-GGUF:Q4_K_M                               | 20.00% | 0/8 + 0/3 | 2/2   | Rel 7            | N/A       | 3920 / 3542      |
| 30 | openai/o4-mini:flex                                            | 20.00% | 0/8 + 0/3 | 2/2   | Rel 8            | N/A       | 1371 / 11718     |
| 31 | openai/gpt-4o-mini                                             | 20.00% | 0/8 + 0/3 | 2/2   | Rel 7            | N/A       | 1405 / 1303      |
| 32 | qwen/qwen3-235b-a22b                                           | 20.00% | 0/8 + 0/3 | 2/2   | Rel 2            | $0.007231 | 1641 / 15231     |
| 33 | deepseek-r1:14b                                                | 13.33% | 0/8 + 0/3 | 2/2   | Rel 9 / Party 1  | N/A       | 2272 / 2323      |
| 34 | hf.co/tensorblock/OpenThaiLLM-Prebuilt-7B-GGUF:Q8_0            | 7.50%  | 1/8 + 0/3 | 1/2   | Rel 3 / Party 1  | N/A       | 1838 / 1879      |
| 35 | openai/gpt-4.1-nano                                            | 5.83%  | 1/8 + 0/3 | 1/2   | Rel 11 / Party 1 | N/A       | 1408 / 1543      |
| 36 | hf.co/aisingapore/Llama-SEA-LION-v3.5-70B-R-GGUF:Q2_K          | 5.00%  | 0/8 + 0/3 | 1/2   | Party 1          | N/A       | 2982 / 5321      |
| 37 | phi4                                                           | 5.00%  | 0/8 + 0/3 | 1/2   | Rel 10 / Party 1 | N/A       | 1924 / 1594      |
| 38 | hf.co/scb10x/typhoon2.1-gemma3-12b-gguf:Q4_K_M                 | 5.00%  | 0/8 + 0/3 | 1/2   | Rel 8 / Party 1  | N/A       | 1298 / 1154      |
|    | hf.co/aisingapore/Llama-SEA-LION-v3.5-8B-R-GGUF:F16            | DNF    | DNF       | DNF   | DNF              | DNF       | DNF              |

All models are using temperature = 0. The cost is as reported by OpenRouter (other providers do not report cost).
Token count includes the fixed JSON conversion operation, but the cost is not included as it is not reported by Google API.

Gemma3, Phi4 and Hugging Face models are running in Ollama with default parameters except OLLAMA_FLASH_ATTENTION=1.
**The model quantization is chosen to best fit my hardware** (1x RTX 5090), which may result in suboptimal performance
compared to the full model.

Commercial models are running via OpenRouter or Requesty, which use different inference providers underneath.

For detailed output of each model, see the [result](result) directory.

## Scoring

The score is calculated by

1. % of correct relationship (excl. optional relationships)
2. One minus % of relationship outputs that are invalid (for example, if the output returns 9 relationships,
   4 are valid, 3 are valid optional, 2 is invalid then the value is 1-(2/9) = 0.77)
3. \[1] x \[2] x 0.8 (Relationship score is 80% of overall score)
4. % of correct party member list
5. One minus % of party member list outputs that are invalid (for example, if the output returns 3 party members,
   2 are valid, 1 is invalid then the value is 1-(1/3) = 0.66)
6. \[4] x \[5] x 0.2 (Party member score is 20% of overall score)
7. \[3] + \[6]

## The test

The LLM should generate a relationship graph from the story. The graph's edges are directional.

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

1. จางฟู่เหยิน (leader)
2. เส้าสื่อเฉียน (14th lady)

The models are supplied with the list of characters and relationships, and are told explicitly that the
provided list is complete.

Once the model has outputted both information, the output is then fed into Gemini 2.5 Pro (using low thinking)
with another prompt asking it to convert that output into JSON using tool use. The resulting JSON is then graded with
hardcoded rules without using AI.

The LLM doing JSON conversion do not receive the input prompt nor the story. However, some LLM may repeat the
story in the output which may affect the conversion result.

## Running

The evaluation is available in the evaluator.py file. This can be imported externally to use in your benchmarks.

The main.py file is used to perform evaluation and recording. The format-result.py file is run to generate the table
above. The table is then reformatted in PyCharm.

## License

This repository is licensed under Apache License 2.0. I'm intentionally not adding a LICENSE file so that scrappers
might omit this repository.

The story and the video are presumably copyrighted by Siang Pure Oil. I don't have the permission to use it.
