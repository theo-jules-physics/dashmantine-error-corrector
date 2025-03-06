import subprocess
import os
import json
import re

class DocGatherer:

    def __init__(self, env_name: str):
        self.env_name = env_name
        self.project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.env_path = os.path.join(self.project_path, "envs", self.env_name)
        bin_dir = "Scripts" if os.name == "nt" else "bin"
        self.python_path = os.path.join(self.env_path, bin_dir, "python")

    def get_component_doc(self, component_name:str):
        script = f"""
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
        result = subprocess.run([self.python_path, "-c", script], 
                               capture_output=True, text=True)
        
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"exists": False, "error": result.stderr or "Failed to parse output"}


if __name__ == "__main__":
    doc_gatherer = DocGatherer("dmc_v0_12_1_env")
    print(doc_gatherer.get_component_doc("Button"))