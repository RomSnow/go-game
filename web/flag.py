from dataclasses import dataclass


@dataclass
class Flag:
    is_up: bool = False

    def __bool__(self):
        return self.is_up
