from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from evaluator import evaluate

def main():
    model = OpenAIModel(
        model_name="PetrosStav/gemma3-tools:27b",
        provider=OpenAIProvider(base_url='http://localhost:11434/v1')
    )
    agent = Agent(model, retries=5)

    out = evaluate(agent)
    print(out)

    print(f"Found relationship: {len(out.valid_relationships)} + {len(out.valid_optional_relationships)}")
    print(f"Found party members: {len(out.valid_party_member_list)}")
    print(f"Score: {out.score}")

if __name__ == "__main__":
    main()
