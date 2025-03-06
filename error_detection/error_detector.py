import dash_mantine_components as dmc
from inspect import signature
from dataclasses import dataclass, field

@dataclass
class ComponentCharacteristics:
    name: str
    parameters: list[str] = field(default_factory=list)
    file_name: str
    line_limits : list[int]
    errors: dict[str, any] | None = None

def check_parameter_exists(component_name: str, parameter: str):
    component = getattr(dmc, component_name)
    sig = signature(component)
    return parameter in sig.parameters

def detect_error_component(component: ComponentCharacteristics) -> str:

    component.errors = {
        'count': 0,
        'message': f"No errors detected for {component.name} component",
        'invalid_items': []
    }

    if not hasattr(dmc, component.name):
        component.errors["count"] = 1
        component.errors["message"] = f"Component {component.name} does not exist"
        component.errors["invalid_items"].append(component.name)
        return component.errors["message"]
    
    for parameter in component.parameters:
        if not check_parameter_exists(component.name, parameter):
            component.errors["count"] += 1
            component.errors["invalid_items"].append(parameter)

    if component.errors["count"] > 0:
        component.errors["message"] = f"Errors detected for parameters in {component.name} component: {component.errors['invalid_items']} do not exist"
    return component.errors["message"]

