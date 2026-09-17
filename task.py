from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    description: str
    is_completed: bool = False
