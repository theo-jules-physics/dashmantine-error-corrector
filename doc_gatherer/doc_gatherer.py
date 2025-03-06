import subprocess
import os
import json
import inspect

class DocGatherer:

    def __init__(self, env_name: str):
        self.env_name = env_name
        self.project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.env_path = os.path.join(self.project_path, "envs", self.env_name)
        bin_dir = "Scripts" if os.name == "nt" else "bin"
        self.python_path = os.path.join(self.env_path, bin_dir, "python")

    def generate_component_doc_script(self, component_name:str):
        return f"""
import dash_mantine_components as dmc
import inspect
import json
import re

try:
    component = getattr(dmc, "{component_name}")
    docstring = inspect.getdoc(component)

    print(json.dumps({{"exists": True, "docstring": docstring}}))
except AttributeError:
    print(json.dumps({{"exists": False, "error": "Component does not exist"}}))
except Exception as e:
    print(json.dumps({{"exists": False, "error": str(e)}}))
        """


    def generate_component_signature_script(self, component_name:str):
        return f"""
import dash_mantine_components as dmc
import inspect
import json

try:
    component = getattr(dmc, "{component_name}")
    sig = inspect.signature(component)
    
    # Extract parameter information
    params = {{}}
    for param_name, param in sig.parameters.items():
        params[param_name] = {{
            "name": param_name,
            "default": str(param.default) if param.default is not param.empty else None,
            "required": param.default is param.empty,
            "kind": str(param.kind)
        }}
    
    print(json.dumps({{"exists": True, "signature": params}}))
except AttributeError:
    print(json.dumps({{"exists": False, "error": "Component does not exist"}}))
except Exception as e:
    print(json.dumps({{"exists": False, "error": str(e)}}))
"""

    def get_component_signature(self, component_name:str):
        script = self.generate_component_signature_script(component_name)
        result = subprocess.run([self.python_path, "-c", script], capture_output=True)
        response = json.loads(result.stdout)
        if not response.get("exists", False):
            return response
        
        # Convert the dictionary representation back to a Signature object
        params = {}
        for param_name, param_info in response["signature"].items():
            # Convert string representation of kind back to enum
            kind_str = param_info["kind"]
            kind = getattr(inspect.Parameter, kind_str.split(".")[-1])
            
            # Handle default values
            default = param_info["default"]
            if default == "None" or default is None:
                default = None
            elif default == "<class 'inspect._empty'>":
                default = inspect.Parameter.empty
            
            # Create Parameter object
            params[param_name] = inspect.Parameter(
                name=param_name,
                kind=kind,
                default=default if not param_info["required"] else inspect.Parameter.empty
            )
        return inspect.Signature(parameters=list(params.values()))
        
    def get_component_doc(self, component_name:str):
        script = self.generate_component_doc_script(component_name)
        result = subprocess.run([self.python_path, "-c", script], capture_output=True)
        return json.loads(result.stdout)
