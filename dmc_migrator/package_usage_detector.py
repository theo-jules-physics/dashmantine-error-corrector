import ast
import os
import logging

from component_info import ComponentInfo

logger = logging.getLogger(__name__)


class DMCUsageDetector:

    def __init__(self, root_dir, target_package="dash_mantine_components"):
        self.root_dir = root_dir
        self.target_package = target_package
        self.results = {}

    def scan_files(self):
        for subdir, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py"):
                    self._analyze_file(os.path.join(subdir, file))

    def _analyze_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read(), filename=file_path)
            except SyntaxError:
                print(f"Syntax error in file: {file_path}")
                return

        alias = self._extract_alias(tree)

        if not alias:
            print(f"No alias found for {self.target_package} in {file_path}")
            return

        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(
                node.func, ast.Attribute
            ):
                if (
                    isinstance(node.func.value, ast.Name)
                    and node.func.value.id == alias
                ):
                    component_name = node.func.attr
                    start_line = node.lineno
                    end_line = (
                        node.end_lineno
                        if hasattr(node, "end_lineno")
                        else start_line
                    )

                    arguments = [
                        arg.id if isinstance(arg, ast.Name) else ast.dump(arg)
                        for arg in node.args
                    ]
                    keyword_arguments = [kw.arg for kw in node.keywords]

                    parameters = arguments + keyword_arguments

                    if file_path not in self.results:
                        self.results[file_path] = {}

                    if component_name not in self.results[file_path]:
                        self.results[file_path][component_name] = []
                    self.results[file_path][component_name].append(
                        ComponentInfo(
                            name=component_name,
                            file_name=file_path,
                            line_limits=[start_line, end_line],
                            parameters=parameters,
                        )
                    )

    def _extract_alias(self, tree):

        alias = None
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias_node in node.names:
                    if alias_node.name == self.target_package:
                        alias = (
                            alias_node.asname
                            if alias_node.asname
                            else alias_node.name.split(".")[0]
                        )
                        break

            elif (
                isinstance(node, ast.ImportFrom)
                and node.module == self.target_package
            ):
                alias = node.module.split(".")[0]
                break

        return alias

    def run(self):
        logger.info(
            f"Scanning files in {self.root_dir} for {self.target_package} usage."
        )
        self.scan_files()
        logger.info(
            f"Scan complete. Found {len(self.results)} files with {self.target_package} usage."
        )
