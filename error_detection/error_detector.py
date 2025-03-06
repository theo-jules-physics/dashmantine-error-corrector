import dash_mantine_components as dmc
from component_info import ComponentInfo
import os
import subprocess
import json


class NewVersionErrorDetector:

    def __init__(self, env_name: str):
        self.env_name = env_name
        self.project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.env_path = os.path.join(self.project_path, "envs", self.env_name)
        bin_dir = "Scripts" if os.name == "nt" else "bin"
        self.python_path = os.path.join(self.env_path, bin_dir, "python")

    def generate_component_exists_script(self, component_name: str):
        return f"""
import dash_mantine_components as dmc
import json
try:
    component = getattr(dmc, "{component_name}")
    print(json.dumps({{"exists": True}}))
except AttributeError:
    print(json.dumps({{"exists": False, "error": "Component does not exist"}}))
except Exception as e:
    print(json.dumps({{"exists": False, "error": str(e)}}))
"""
    
    def generate_check_parameter_script(self, component_name: str, parameter: str):
        return f"""
import dash_mantine_components as dmc
from inspect import signature
import json
try:
    component = getattr(dmc, "{component_name}")
    sig = signature(component)
    exists = "{parameter}" in sig.parameters
    print(json.dumps({{"exists": exists}}))
except AttributeError:
    print(json.dumps({{"exists": False, "error": "Component does not exist"}}))
except Exception as e:
    print(json.dumps({{"exists": False, "error": str(e)}}))
"""


    def check_parameter_exists(self, component_name: str, parameter: str):
        script = self.generate_check_parameter_script(component_name, parameter)
        result = subprocess.run([self.python_path, "-c", script], capture_output=True, text=True)
        try:
            response = json.loads(result.stdout)
            return response.get("exists", False)
        except json.JSONDecodeError:
            return False

    def check_component_exists(self, component_name: str):
        script = self.generate_component_exists_script(component_name)
        result = subprocess.run([self.python_path, "-c", script], capture_output=True, text=True)
        try:
            response = json.loads(result.stdout)
            return response.get("exists", False)
        except json.JSONDecodeError:
            return False

    def detect_error_component(self, component: ComponentInfo) -> str:
        component.errors = {
            'count': 0,
            'type': None,
            'message': f"No errors detected for {component.name} component",
            'invalid_items': []
        }
        
        if not self.check_component_exists(component.name):
            component.errors["type"] = "component"
            component.errors["count"] = 1
            component.errors["message"] = f"Component {component.name} does not exist"
            component.errors["invalid_items"].append(component.name)
            return component.errors["message"]
        
        for parameter in component.parameters:
            if not self.check_parameter_exists(component.name, parameter):
                component.errors["type"] = "parameter"
                component.errors["count"] += 1
                component.errors["invalid_items"].append(parameter)
        
        if component.errors["count"] > 0:
            component.errors["message"] = f"Errors detected for parameters in {component.name} component: {component.errors['invalid_items']} do not exist"
        
        return component.errors["message"]

