from pathlib import Path

from py_markdown_table.markdown_table import markdown_table

from main import ResultData, CURRENT_TEST_VERSION


def main():
    out: list[ResultData] = []

    for file in Path("result").iterdir():
        try:
            result = ResultData.model_validate_json(file.open().read())
        except Exception as exc:
            print(f"Failed to load {file.name}: {repr(exc)}")
            continue
        out.append(result)

    out.sort(key=lambda i: i.result.score if not i.error else -999, reverse=True)

    formatted = []

    for rank, item in enumerate(out):
        model_name = item.model

        if item.version != CURRENT_TEST_VERSION:
            model_name += f" **(test v{item.version})**"

        if item.error:
            # TODO: Even in errors sometimes we can have more info
            formatted.append({
                "#": rank+1,
                "Model name": model_name,
                "Score": "DNF",
                "Rel": "DNF",
                "Party": "DNF",
                "Invalid": "DNF",
                "Cost": "DNF",
                "In Tok / Out Tok": "DNF",
            })
        else:
            cost = None
            request_tokens = 0
            response_tokens = 0

            if item.openai_response:
                request_tokens = item.openai_response.usage.prompt_tokens
                response_tokens = item.openai_response.usage.completion_tokens

                if item.openai_response.usage.completion_tokens_details and item.openai_response.usage.completion_tokens_details.reasoning_tokens:
                    response_tokens += item.openai_response.usage.completion_tokens_details.reasoning_tokens

                if "cost" in item.openai_response.usage.model_extra:
                    # OpenRouter report the cost here
                    cost = item.openai_response.usage.model_extra["cost"]

            invalid = []
            if len(item.result.invalid_relationships) > 0:
                invalid.append(f"Rel {len(item.result.invalid_relationships)}")
            if len(item.result.invalid_party_member_list) > 0:
                invalid.append(f"Party {len(item.result.invalid_party_member_list)}")

            formatted.append({
                "#": rank+1,
                "Model name": model_name,
                "Score": "{:.2f}%".format(item.score * 100),
                "Rel": f"{len(item.result.valid_relationships)}/8 + {len(item.result.valid_optional_relationships)}/3",
                "Party": f"{len(item.result.valid_party_member_list)}/2",
                "Invalid": " / ".join(invalid),
                "Cost": "${:.6f}".format(cost) if cost is not None else "N/A",
                "In Tok / Out Tok": f"{request_tokens} / {response_tokens}",
            })

    print(markdown_table(formatted).set_params(row_sep="markdown", padding_weight="right", padding_width=1, quote=False).get_markdown())


if __name__ == "__main__":
    main()
