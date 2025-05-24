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

| #  | Model name                                                     | Score  | Rel       | Party | Invalid         | Cost      | In Tok / Out Tok |
|----|----------------------------------------------------------------|--------|-----------|-------|-----------------|-----------|------------------|
| 1  | meta-llama/llama-4-maverick                                    | 76.00% | 7/8 + 1/3 | 2/2   | Rel 2           | N/A       | 1153 / 1113      |
| 2  | deepseek/deepseek-r1                                           | 62.86% | 5/8 + 1/3 | 2/2   | Rel 1           | $0.046424 | 1224 / 11624     |
| 3  | openai/gpt-4.5-preview                                         | 60.00% | 4/8 + 1/3 | 2/2   |                 | $0.177450 | 1998 / 184       |
| 4  | meta-llama/llama-3.3-70b-instruct                              | 55.00% | 6/8 + 1/3 | 2/2   | Rel 5           | $0.001643 | 1255 / 571       |
| 5  | openai/gpt-4o-2024-11-20                                       | 44.00% | 3/8 + 1/3 | 2/2   | Rel 1           | $0.006875 | 1998 / 188       |
| 6  | openai/gpt-4.1                                                 | 42.22% | 4/8 + 1/3 | 2/2   | Rel 4           | $0.008812 | 1998 / 602       |
| 7  | PetrosStav/gemma3-tools:27b                                    | 42.22% | 4/8 + 1/3 | 2/2   | Rel 4           | N/A       | 1819 / 632       |
| 8  | hf.co/scb10x/typhoon2.1-gemma3-12b-gguf:Q4_K_M                 | 42.22% | 4/8 + 1/3 | 2/2   | Rel 4           | N/A       | 1137 / 631       |
| 9  | qwen/qwen3-235b-a22b                                           | 40.00% | 3/8 + 1/3 | 2/2   | Rel 2           | $0.011488 | 1295 / 28747     |
| 10 | hf.co/mradermacher/openthaigpt1.5-72b-instruct-i1-GGUF:IQ2_S   | 37.33% | 3/8 + 1/3 | 2/2   | Rel 1 / Party 1 | N/A       | 1296 / 414       |
| 11 | openai/gpt-4o-mini                                             | 36.67% | 4/8 + 1/3 | 2/2   | Rel 7           | $0.000598 | 1998 / 497       |
| 12 | hf.co/JulienElkaim/Tsunami-1.0-14B-Instruct-Q4_K_M-GGUF:Q4_K_M | 26.67% | 1/8 + 1/3 | 2/2   | Rel 1           | N/A       | 1296 / 361       |
| 13 | hf.co/tensorblock/OpenThaiLLM-Prebuilt-7B-GGUF:Q8_0            | 21.67% | 1/8 + 0/3 | 2/2   | Rel 5           | N/A       | 1296 / 313       |
| 14 | hf.co/mradermacher/openthaigpt1.5-14b-instruct-GGUF:Q8_0       | 20.00% | 0/8 + 0/3 | 2/2   | Rel 7           | N/A       | 1296 / 569       |
| 15 | hf.co/aisingapore/Llama-SEA-LION-v3.5-8B-R-GGUF:F16            | 13.33% | 1/8 + 0/3 | 1/2   | Party 2         | N/A       | 1223 / 169       |
| 16 | phi4                                                           | 10.00% | 0/8 + 0/3 | 1/2   | Rel 7           | N/A       | 1634 / 497       |
| 17 | hf.co/mradermacher/Sailor2-20B-Chat-GGUF:Q8_0                  | 6.67%  | 1/8 + 0/3 | 1/2   | Rel 5 / Party 1 | N/A       | 1296 / 282       |
| 18 | hf.co/aisingapore/Llama-SEA-LION-v3.5-70B-R-GGUF:Q2_K          | 5.00%  | 0/8 + 0/3 | 1/2   | Rel 6 / Party 1 | N/A       | 1225 / 354       |

All models are using temperature = 0. The cost is as reported by OpenRouter.

Gemma3, Phi4 and Hugging Face models are running in Ollama with default parameters except OLLAMA_FLASH_ATTENTION=1.
**The model quantization is chosen to best fit my hardware** (1x RTX 5090), which may result in suboptimal performance
compared to the full model.

Commercial models are running via OpenRouter. Since the test use Structured Output, OpenRouter only support models
that are running on OpenAI and Fireworks' infrastructure.

Scoring is performed by

1. % of correct relationship (excl. optional relationships)
2. One minus % of relationship outputs that are invalid (for example, if the output returns 9 relationships,
   4 are valid, 3 are valid optional, 2 is invalid then the value is 1-(2/9) = 0.77)
3. \[1] x \[2] x 0.8 (Relationship score is 80% of overall score)
4. % of correct party member list
5. One minus % of party member list outputs that are invalid (for example, if the output returns 3 party members,
   2 are valid, 1 is invalid then the value is 1-(1/3) = 0.66)
6. \[4] x \[5] x 0.2 (Party member score is 20% of overall score)
7. \[3] + \[6]

For detailed output of each model, see the [result](result) directory.

## The test

The LLM should generate relationship graph from the story. The graph's edges are directional.

As of v3 version of the test, we use structured output to ensure that the model output as instructed. The `temperature`
is set at 0, while other parameters at default. Models are provided with a `think_*` field which it may use to think
before responding, if the model itself do not use the `<think>` tag.

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

## FAQ

### Why use JSON output?

Most LLM tests use two LLM - one under test, and one judging the result of the first one. This test, however, use
hardcoded result to grade, which requires that the LLM output in machine-readable format.

Some LLM might not be tuned to output JSON, and will not perform well in this test. The reason I structured the test
this way are:

1. Since there are no LLM that perform perfectly according to instructions, I don't trust that the grading LLM will
   always grade correctly. Since the expected result is already known, it is better for a normal computer program to
   be the judge as it should always judge according to instructions (except for bugs).
2. I'm more interested in LLM-as-a-Library which applications can be built upon. If there are better ways to parse
   LLM outputs, then the tests may switch to that method. This also means the tests here test two things - how the
   LLM is able to understand the story, and how well is its JSON output capabilities.
3. It is possible to run the tests for both JSON output and traditional text output judged by LLM, but it complicates
   the reporting. The traditional test is left as an exercise for the reader.

## License

This repository is licensed under Apache License 2.0. I'm intentionally not adding a LICENSE file so that scrappers
might omit this repository.

The story and the video are presumably copyrighted by Siang Pure Oil. I don't have the permission to use it.
