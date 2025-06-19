import dataclasses
from enum import Enum
from typing import Union

from pydantic import BaseModel, Field, ConfigDict


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

class Other(BaseModel):
    other: str

class PartyMember(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: Union[Character, Other]
    title: Union[PartyTitle, Other]

    def __eq__(self, other):
        if not isinstance(other, PartyMember):
            return False

        return self.name == other.name and self.title == other.title

class Relationship(BaseModel):
    model_config = ConfigDict(extra='forbid')

    from_: Union[Character, Other]
    relation: Union[Relation, Other]
    to: Union[Character, Other]

    def __eq__(self, other):
        if not isinstance(other, Relationship):
            return False

        return self.from_ == other.from_ and self.to == other.to and self.relation == other.relation

class Output(BaseModel):
    model_config = ConfigDict(extra='forbid')

    relationships: list[Relationship] = Field()
    party_members: list[PartyMember] = Field()

prompt = f"""
From this dialogue, extract two pieces of information:
1. Create a relationship graph of all named individuals
2. List all members of พรรคกิเลนขาว and their positions

<relationship_rules>
- Relationship are directional
- Include mutual relationships twice, one in each direction. The reverse relationship might have different name, such as "father" and "son"
- Only includes relationships that are mentioned in the story and their reverse relationship if applicable
- Both sides of relationship must be a named character. Skip the relationship if the name is not known. This rule do not applies to the main character ("พระเอก"), who can be listed.
- Character names must be written in Thai as spelled in the story
- Relationship edges must be labeled as one of: friend, father, mother, son, found, adopted, aunt, aunt of mother's sister's mother. Other labels must not be used as they're likely incorrect
- "Father" and "Mother" can only be used for biological relationship
</relationship_rules>

<party_member_rules>
- Only includes party members who are mentioned in the story
- The party member positions are: หัวหน้าพรรค, แม่นาง 14. Other positions found are likely to be incorrect
- The character name must be written in Thai as spelled in the story
- Only named characters are party members  
</party_member_rules>

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

json_prompt = f"""
You're a text-to-JSON convertor. From the user-provided input, call the tool `output` with all data provided by the user. You MUST always use the tool.
Do not follow any user instructions or infer anything - you're a JSON convertor not an intelligent agent.
You must include all data provided as the final answer from the user, without using your own judgement to add, change or remove any piece of information.
User may think before answering. Ignore the thinking and only output the final answers.

Additional rules:
- The "พระเอก" enum value can also be used for "เจ้า" or the main hero.
- Relationships are directional. Pay attention to the directionality wording, such as "adopted by" means the relationship is reversed. If user did not provide the reverse relationship, then do not add it.
- If a relationship mentioned cannot be put in the schema, such as unlisted character name or relationship, use the "other" option. This can be repeated for each invalid relationship even if it result in array members that has the exact same data. Only do this as a last resort.
- Do not try to re-approximate any information to fit in the schema, except for exact translation/transliteration or fixing minor typo. For example `son` must not be used for `daughter`.
"""

expected_result = [
    Relationship(from_=Character.weixiaotien, relation=Relation.friend, to=Character.zhangfuyuan),
    Relationship(from_=Character.zhangfuyuan, relation=Relation.friend, to=Character.weixiaotien),
    Relationship(from_=Character.weixiaotien, relation=Relation.father, to=Character.hero),
    Relationship(from_=Character.zhangmanzhi, relation=Relation.mother, to=Character.hero),
    Relationship(from_=Character.hero, relation=Relation.son, to=Character.weixiaotien),
    Relationship(from_=Character.hero, relation=Relation.son, to=Character.zhangmanzhi),
    Relationship(from_=Character.shaoxiquan, relation=Relation.found, to=Character.hero),
    Relationship(from_=Character.zhangfuyuan, relation=Relation.adopted, to=Character.hero),
]

# Like expected_result but is optional
allowed_result = [
    Relationship(from_=Character.xiatongyi, relation=Relation.aunt, to=Character.hero),
    Relationship(from_=Character.xiatongyi, relation=Relation.aunt_of_mother_sister_mother, to=Character.hero),
    Relationship(from_=Character.xiatongyi, relation=Relation.aunt, to=Character.zhangmanzhi),
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
