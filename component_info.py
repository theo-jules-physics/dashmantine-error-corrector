from dataclasses import dataclass, field

@dataclass
class ComponentInfo:
    name: str
    parameters: list[str] = field(default_factory=list)
    file_name: str
    line_limits : list[int]
    errors: dict[str, any] | None = None