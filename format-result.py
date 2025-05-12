from pathlib import Path

from py_markdown_table.markdown_table import markdown_table

from main import ResultData



def main():
    out: list[ResultData] = []

    for file in Path("result").iterdir():
        try:
            result = ResultData.model_validate_json(file.open().read())
        except:
            continue
        out.append(result)

    out.sort(key=lambda i: i.result.score if not i.error else -999, reverse=True)

    formatted = []

    for rank, item in enumerate(out):
        if item.error:
            formatted.append({
                "#": rank+1,
                "Model name": item.model,
                "Score": "DNF",
                "Relationships": "DNF",
                "Party members": "DNF",
                "Invalid (rel/party)": "DNF",
                "Cost": "DNF",
                "Req / In Tok / Out Tok": "DNF",
            })
        else:
            usage = item.result.output.usage()
            cost = None
            if item.cost is not None:
                cost = ((usage.requests * item.cost.request_cost_1k/1000)
                        + (usage.request_tokens * item.cost.input_token_1m/float(1e6))
                        + (usage.response_tokens * item.cost.output_token_1m/float(1e6)))
            formatted.append({
                "#": rank+1,
                "Model name": item.model,
                "Score": "{:.2f}%".format(item.score * 100),
                "Relationships": f"{len(item.result.valid_relationships)}/8 + {len(item.result.valid_optional_relationships)}/3",
                "Party members": f"{len(item.result.valid_party_member_list)}/2",
                "Invalid (rel/party)": f"{len(item.result.invalid_relationships)} / {len(item.result.invalid_party_member_list)}",
                "Cost": "${:.6f}".format(cost) if cost is not None else "N/A",
                "Req / In Tok / Out Tok": f"{usage.requests} / {usage.request_tokens} / {usage.response_tokens}",
            })

    print(markdown_table(formatted).set_params(row_sep="markdown", padding_weight="right", padding_width=1, quote=False).get_markdown())


if __name__ == "__main__":
    main()
