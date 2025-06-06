import dataclasses
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

class Character(str, Enum):
    hero = "พระเอก"
    weixiaotien = "เว่ยเส้าเทียน"
    lixiashui = "หลี่เซียซุย"
    zhangfuyuan = "จางฟู่เหยิน"
    zhangmanzhi = "จางม่านจือ"
    shaoxiquan = "เส้าสื่อเฉียน"
    xiatongyi = "เซียะถงอี้"

class Relation(str, Enum):
    friend = "friend"
    father = "father"
    mother = "mother"
    son = "son"
    found = "found"
    adopted = "adopted"
    aunt = "aunt"
    aunt_of_mother_sister_mother = "aunt of mother's sister's mother"

class PartyTitle(str, Enum):
    leader = "หัวหน้าพรรค"
    fourteenth_lady = "แม่นาง 14"

class PartyMember(BaseModel):
    name: Character
    title: PartyTitle

    def __eq__(self, other):
        if not isinstance(other, PartyMember):
            return False

        return self.name == other.name and self.title == other.title

class Relationship(BaseModel):
    """Relationship from Character A to B. Relationship is directional - if not repeated then it may not holds true
    in the reverse direction."""
    a: Character
    relation: Relation
    b: Character

    def __eq__(self, other):
        if not isinstance(other, Relationship):
            return False

        return self.a == other.a and self.b == other.b and self.relation == other.relation

class Output(BaseModel):
    think_relationship: Optional[str] = Field(max_length=5000)
    relationships: list[Relationship]
    think_party: Optional[str] = Field(max_length=5000)
    party_members: list[PartyMember] = Field(description = "รายชื่อสมาชิกพรรคกิเลนขาว")

prompt = f"""
From this dialogue, extract two pieces of information:
1. Create a relationship graph of all named individuals
2. List all members of "พรรคกิเลนขาว" (White Kirin Party) and their positions

## Relationship Graph Instructions:
- First, use the `think_relationship` field to identify all relationships between named individuals
- When identifying relationships:
  - Consider both direct and indirect relationships
  - Remember that relationships are directional from `a` to `b`
  - Include mutual relationships twice (once in each direction). The reverse relationship might have different name, such as "father" and "son".
- Then map only the relationships you've identified into the JSON structure
- Skip any relationships that don't fit the provided JSON schema

## Party Member Instructions:
- First, use the `think_party` field to identify all "พรรคกิเลนขาว" members
- Only include individuals explicitly mentioned as party members in the dialogue
- List each member with their position in the party
- Only use positions that are specifically mentioned in the dialogue
- Do not assume someone is a party member without clear evidence

## Output JSON Schema

The output must strictly follow this JSON schema.

```jsonschema
{Output.model_json_schema(mode="serialization")}
```

## Input

พระเอก: เว่ยเส้าเทียน วันนี้เป็นวันตายของเจ้า
เว่ยเส้าเทียน: โอหัง แน่จริงก็เข้ามา
พระเอก: ตายซะ!
หลี่เซียซุย : ช้าก่อน! เว่ยเส้าเทียนคือพ่อของเจ้า!
หลี่เซียซุย: ซึ่งเป็นสหายรัก ของจางฟู่เหยินหัวหน้าพรรคกิเลนขาว ที่เก็บเจ้ามาเลี้ยงเมื่อ 22 ปีก่อน
ซึ่งจริงๆแล้วก่อนที่จะเจอเจ้า แม่นางเส้าสื่อเฉียน แม่นาง 14
เว่ยเส้าเทียน: แห่งพรรคกิเลนขาว ซึ่งได้พบเจ้าข้างหนองน้ำ ใกล้เมืองเหลียงคุน ซึ่งเป็นที่ๆ เซียะถงอี้ น้าสาวพี่แม่ได้แนะนำให้พบ
หลี่เซียซุย: ข้าหลี่เซียซุย ก่อนที่จะเจอเจ้า
เว่ยเส้าเทียน: ซึ่งอันที่จริงแล้ว ข้าเองก็ไม่เคยรู้มาก่อนว่าเจ้า เป็นลูกของ
หลี่เซียซุย: จางฟู่เหยิน
เว่ยเส้าเทียน: จนข้านึกขึ้นได้ จึงว่า
หลี่เซียซุย: จางม่านจือ แม่เจ้า
เว่ยเส้าเทียน: ได้พาข้าไปพบ
หลี่เซียซุย: พี่สาวแม่ของเจ้า
เว่ยเส้าเทียน: ซึ่งน้าสาวพี่แม่ของเจ้า ได้พาข้าไปรู้จักกับหลี่เซียซุย
หลี่เซียซุย: น้าสาวพี่ของแม่เจ้า
เว่ยเส้าเทียน: ก่อนที่จะเจอเจ้า
หลี่เซียซุย: เมื่อ 22 ปีก่อน
"""

expected_result = [
    Relationship(a=Character.weixiaotien, relation=Relation.friend, b=Character.zhangfuyuan),
    Relationship(a=Character.zhangfuyuan, relation=Relation.friend, b=Character.weixiaotien),
    Relationship(a=Character.weixiaotien, relation=Relation.father, b=Character.hero),
    Relationship(a=Character.zhangmanzhi, relation=Relation.mother, b=Character.hero),
    Relationship(a=Character.hero, relation=Relation.son, b=Character.weixiaotien),
    Relationship(a=Character.hero, relation=Relation.son, b=Character.zhangmanzhi),
    Relationship(a=Character.shaoxiquan, relation=Relation.found, b=Character.hero),
    Relationship(a=Character.zhangfuyuan, relation=Relation.adopted, b=Character.hero),
]

# Like expected_result but is optional
allowed_result = [
    Relationship(a=Character.xiatongyi, relation=Relation.aunt, b=Character.hero),
    Relationship(a=Character.xiatongyi, relation=Relation.aunt_of_mother_sister_mother, b=Character.hero),
    Relationship(a=Character.xiatongyi, relation=Relation.aunt, b=Character.zhangmanzhi),
]

party_member_list = [
    PartyMember(name=Character.zhangfuyuan, title=PartyTitle.leader),
    PartyMember(name=Character.shaoxiquan, title=PartyTitle.fourteenth_lady),
]

@dataclasses.dataclass
class Result:
    valid_relationships: list[Relationship]
    valid_optional_relationships: list[Relationship]
    invalid_relationships: list[Relationship]
    missing_relationships: list[Relationship]
    valid_party_member_list: list[PartyMember]
    invalid_party_member_list: list[PartyMember]
    missing_party_members: list[PartyMember]

    @property
    def score(self) -> float:
        # Valid relationship score: % of the expected results found
        valid_relationship_score = float(len(self.valid_relationships)) / float(len(expected_result))
        # Invalid relationship score: % of the result that is valid
        output_relationship_count = len(self.valid_relationships) + len(self.valid_optional_relationships) + len(self.invalid_relationships)
        if output_relationship_count > 0:
            invalid_relationship_score = 1 - (float(len(self.invalid_relationships)) / float(output_relationship_count))
        else:
            invalid_relationship_score = 0

        party_member_list_score = float(len(self.valid_party_member_list)) / float(len(party_member_list))
        output_party_members_count = len(self.valid_party_member_list) + len(self.invalid_party_member_list)
        if output_party_members_count > 0:
            invalid_party_member_list_score = 1 - (float(len(self.invalid_party_member_list)) / float(output_party_members_count))
        else:
            invalid_party_member_list_score = 0

        # Relationship = 80% score
        # Party member = 20% score
        return (valid_relationship_score * invalid_relationship_score * 0.8) + (party_member_list_score * invalid_party_member_list_score * 0.2)


def grade(output: Output) -> Result:
    out = Result(
        valid_relationships=[],
        valid_optional_relationships=[],
        invalid_relationships=[],
        missing_relationships=[],
        valid_party_member_list=[],
        invalid_party_member_list=[],
        missing_party_members=[],
    )
    expected_result_remaining = expected_result.copy()
    allowed_result_remaining = allowed_result.copy()
    party_member_remaining = party_member_list.copy()

    # Grade relationship graph
    for rel in output.relationships:
        found = False
        for i, expected in enumerate(expected_result_remaining):
            if rel == expected:
                found = True
                out.valid_relationships.append(rel)
                del expected_result_remaining[i]
                break

        if found:
            continue

        for i, expected in enumerate(allowed_result_remaining):
            if rel == expected:
                found = True
                out.valid_optional_relationships.append(rel)
                del allowed_result_remaining[i]
                break

        if not found:
            out.invalid_relationships.append(rel)

    # Grade party member lists
    for member in output.party_members:
        found = False
        for i, expected in enumerate(party_member_remaining):
            if member == expected:
                found = True
                out.valid_party_member_list.append(member)
                del party_member_remaining[i]
                break

        if not found:
            out.invalid_party_member_list.append(member)

    out.missing_relationships = expected_result_remaining
    out.missing_party_members = party_member_remaining
    return out
