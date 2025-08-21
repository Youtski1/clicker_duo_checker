from dataclasses import dataclass


@dataclass
class Duo:
    id: int
    owner_id: int
    level: int
    stage: int
    health: int 
    recovery_time: str