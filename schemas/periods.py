from datetime import datetime
from pydantic import model_validator
from pydantic import ConfigDict
from pydantic import BaseModel

class Monster(BaseModel):
    id:str
    name: str
    hp: int
    floor:str
    room:str
    note:str|None=None
    weakness:list[str]
    model_config = ConfigDict(from_attributes=True)
    @model_validator(mode="before")
    @classmethod
    def validate_weakness(cls, data):
        if not isinstance(data, dict):
            return {
                "id": str(data.id),
                "name": data.name,
                "hp": data.hp,
                "floor": data.floor,
                "room": data.room,
                "note": data.note,
                "weakness": [w.element for w in data.weaknesses]
            }
        return data

class Period(BaseModel):
    mode:str
    id:str
    major_version: int
    version: str
    half: str
    start_time: datetime
    end_time: datetime
    total_hp: int
    monsters: list[Monster]
    model_config = ConfigDict(from_attributes=True)
    @model_validator(mode="before")
    @classmethod
    def validate_monsters(cls, data):
        if not isinstance(data, dict):
            return {
                "mode": data.mode,
                "id": data.id,
                "major_version": data.major_version,
                "version": f"{data.major_version}.{data.minor_version}",
                "half": data.half,
                "start_time": data.start_time,
                "end_time": data.end_time,
                "total_hp": data.total_hp,
                "monsters": data.monsters,
            }
        return data


class Periods(BaseModel):
    mode: str
    periods: list[Period]
    model_config = ConfigDict(from_attributes=True)



















