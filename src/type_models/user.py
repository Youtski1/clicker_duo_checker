from dataclasses import dataclass


@dataclass
class User: 
    id: int
    telegram_id: int
    full_name: str
    username: str
    feathers: int
    damage: int
