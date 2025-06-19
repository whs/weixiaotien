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
| 1  | openai/gpt-4o                                                  | 76.00% | 7/8 + 1/3 | 2/2   | Rel 2            | $0.004000 | 1395 / 1188      |
| 2  | google/gemini-2.5-pro                                          | 66.67% | 6/8 + 1/3 | 2/2   | Rel 2            | $0.026759 | 1409 / 5722      |
| 3  | openai/o4-mini:flex                                            | 65.00% | 8/8 + 1/3 | 2/2   | Rel 7            | $0.011300 | 1486 / 11225     |
| 4  | anthropic/claude-opus-4-20250514                               | 64.55% | 7/8 + 0/3 | 2/2   | Rel 4            | $0.043800 | 1856 / 1461      |
| 5  | anthropic/claude-sonnet-4                                      | 60.00% | 7/8 + 1/3 | 2/2   | Rel 6            | $0.012624 | 2010 / 1836      |
| 6  | openai/chatgpt-4o-latest                                       | 55.00% | 7/8 + 1/3 | 2/2   | Rel 8            | $0.008600 | 1522 / 1456      |
| 7  | anthropic/claude-3.5-sonnet                                    | 52.00% | 4/8 + 0/3 | 2/2   | Rel 1            | $0.006684 | 1749 / 996       |
| 8  | hf.co/tensorblock/OpenThaiLLM-Prebuilt-7B-GGUF:Q8_0            | 47.71% | 6/8 + 1/3 | 2/2   | Rel 3 / Party 5  | N/A       | 7118 / 8615      |
| 9  | qwen/qwen-max                                                  | 45.00% | 5/8 + 1/3 | 2/2   | Rel 6            | $0.003032 | 1531 / 1339      |
| 10 | hf.co/Qwen/Qwen3-32B-GGUF:Q4_K_M                               | 42.50% | 3/8 + 0/3 | 2/2   | Rel 1            | N/A       | 1419 / 3453      |
| 11 | openai/gpt-4.1                                                 | 39.58% | 6/8 + 1/3 | 2/2   | Rel 9 / Party 1  | $0.004800 | 3001 / 3289      |
| 12 | phi4-reasoning                                                 | 38.00% | 3/8 + 0/3 | 2/2   | Rel 2            | N/A       | 2121 / 11967     |
| 13 | google/gemini-2.5-flash                                        | 34.29% | 4/8 + 1/3 | 2/2   | Rel 9            | $0.001453 | 1661 / 1809      |
| 14 | hf.co/scb10x/typhoon2.1-gemma3-12b-gguf:Q4_K_M                 | 32.50% | 5/8 + 0/3 | 2/2   | Rel 15           | N/A       | 1514 / 1803      |
| 15 | openai/gpt-4.5-preview                                         | 32.00% | 3/8 + 1/3 | 2/2   | Rel 6            | $0.085300 | 1391 / 1321      |
| 16 | hf.co/aisingapore/Llama-SEA-LION-v3.5-70B-R-GGUF:Q2_K          | 30.00% | 2/8 + 0/3 | 2/2   | Rel 2            | N/A       | 2465 / 2185      |
| 17 | openai/gpt-4o-mini                                             | 30.00% | 3/8 + 1/3 | 2/2   | Rel 8            | $0.000300 | 1476 / 1254      |
| 18 | openai/gpt-4.1-mini                                            | 28.82% | 3/8 + 2/3 | 2/2   | Rel 12           | $0.001100 | 1664 / 1666      |
| 19 | hf.co/mradermacher/Sailor2-20B-Chat-GGUF:Q8_0                  | 24.00% | 1/8 + 1/3 | 2/2   | Rel 3            | N/A       | 1486 / 1027      |
| 20 | phi4                                                           | 23.08% | 2/8 + 0/3 | 2/2   | Rel 11           | N/A       | 1943 / 1433      |
| 21 | gemma3:12b                                                     | 22.50% | 2/8 + 0/3 | 2/2   | Rel 14           | N/A       | 3308 / 3299      |
| 22 | gemma3:27b                                                     | 20.00% | 0/8 + 0/3 | 2/2   | Rel 14           | N/A       | 1425 / 1348      |
| 23 | anthropic/claude-3.5-haiku                                     | 20.00% | 0/8 + 0/3 | 2/2   | Rel 5            | $0.001818 | 1773 / 1189      |
| 24 | hf.co/mradermacher/openthaigpt1.5-72b-instruct-i1-GGUF:IQ2_S   | 20.00% | 0/8 + 0/3 | 2/2   | Rel 4            | N/A       | 1455 / 1080      |
| 25 | google/gemini-2.5-flash-lite-preview-06-17                     | 20.00% | 0/8 + 0/3 | 2/2   | Rel 14           | $0.000217 | 1530 / 1438      |
| 26 | hf.co/JulienElkaim/Tsunami-1.0-14B-Instruct-Q4_K_M-GGUF:Q4_K_M | 17.00% | 2/8 + 1/3 | 1/2   | Rel 2 / Party 1  | N/A       | 1415 / 1312      |
| 27 | hf.co/mradermacher/openthaigpt1.5-14b-instruct-GGUF:Q8_0       | 15.00% | 2/8 + 0/3 | 1/2   | Rel 2 / Party 1  | N/A       | 1401 / 663       |
| 28 | llama3.1:8b                                                    | 14.33% | 1/8 + 0/3 | 2/2   | Rel 9 / Party 1  | N/A       | 1549 / 1468      |
| 29 | deepseek-r1:14b                                                | 10.00% | 0/8 + 0/3 | 2/2   | Rel 10 / Party 2 | N/A       | 1720 / 2074      |
| 30 | openai/gpt-4.1-nano                                            | 8.33%  | 2/8 + 0/3 | 1/2   | Rel 10 / Party 1 | $0.000200 | 4513 / 4064      |
| 31 | hf.co/aisingapore/Llama-SEA-LION-v3.5-8B-R-GGUF:F16            | 4.76%  | 1/8 + 0/3 | 1/2   | Rel 6 / Party 2  | N/A       | 2744 / 3056      |

All models are using temperature = 0. The cost is as reported by OpenRouter or Requesty.
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
