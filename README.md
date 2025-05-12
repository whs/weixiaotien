# WeiXiaoTien - a LLM evaluation

![Video](https://www.youtube.com/watch?v=c8LR1_0yc64)

Siang Pure Oil had an advertisement in early 2000 in Wuxia style. It involves an old man and a young hero fighting
then an old lady appears to interrupt the fight by telling the old man is the hero's father. Then the two old people
start telling him his family tree which can get confusing. The narrator interrupts the dizzying hero by advertising
the oil saying that it could help with dizzyness.

I think the story is a good LLM test case! For example, "แม่นาง 14" is a job position, but some LLM do understand it as
real mother (adopted or biological) in family trees.

However, the advertising and its analysis are public for several years so that it is possible that it may end up in
one of the training data, including this repository.

## Results

| Model name                               | Score  | Relationships | Party members | Invalid (rel/party) | Req / In Tok / Out Tok |
|------------------------------------------|--------|---------------|---------------|---------------------|------------------------|
| openai/gpt-4.5-preview                   | 85.45% | 8/8 + 1/3     | 2/2           | 2 / 0               | 1 / 818 / 386          |
| qwen/qwen3-235b-a22b                     | 70.00% | 5/8 + 0/3     | 2/2           | 0 / 0               | 1 / 1070 / 8304        |
| anthropic/claude-3.7-sonnet              | 62.86% | 5/8 + 1/3     | 2/2           | 1 / 0               | 2 / 5777 / 1495        |
| openai/gpt-4.1                           | 45.00% | 5/8 + 1/3     | 2/2           | 6 / 0               | 2 / 2087 / 630         |
| deepseek/deepseek-r1                     | 35.00% | 2/8 + 1/3     | 2/2           | 1 / 0               | 4 / 7725 / 15805       |
| openai/gpt-4o-2024-11-20                 | 26.00% | 2/8 + 1/3     | 2/2           | 7 / 0               | 1 / 818 / 384          |
| google/gemini-2.5-flash-preview:thinking | 0.00%  | 0/8 + 0/3     | 0/2           | 0 / 0               | 2 / 1619 / 15548       |
| google/gemini-2.5-flash-preview          | DNF    | DNF           | DNF           | DNF                 | DNF                    |
| qwen/qwen-max                            | DNF    | DNF           | DNF           | DNF                 | DNF                    |
| anthropic/claude-3.7-sonnet:thinking     | DNF    | DNF           | DNF           | DNF                 | DNF                    |
| qwen/qwen2.5-vl-72b-instruct             | DNF    | DNF           | DNF           | DNF                 | DNF                    |
| x-ai/grok-3-beta                         | DNF    | DNF           | DNF           | DNF                 | DNF                    |
| deepseek/deepseek-chat-v3-0324           | DNF    | DNF           | DNF           | DNF                 | DNF                    |
| openai/o4-mini                           | DNF    | DNF           | DNF           | DNF                 | DNF                    |

Gemma3 and Hugging Face models are running in Ollama with default parameters except OLLAMA_FLASH_ATTENTION=1.

Commercial models are running via OpenRouter. Errors (DNF = Did Not Finish) could be potentially from either the LLM
providers, or OpenRouter including incompatibility with Pydantic's OpenAI-compatible endpoints expectations (which is
the most common reason).

For detailed output of each model, see the [result](result) directory.

## The test

The LLM should generate relationship graph from the story. The graph's edges are directional.

The LLM harness in use is Pydantic, which use Tool Use to enforce that the LLM calls the output function with the
correct JSON schema. The model can correct mistakes up to 5 times. Models that do not support tool use are not
evaluated.

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
