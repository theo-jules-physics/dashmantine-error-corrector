from dataclasses import dataclass, field


@dataclass
class ComponentInfo:
    name: str
    file_name: str
    line_limits: list[int]
    parameters: list[str] = field(default_factory=list)

    errors: dict[str, any] | None = None
