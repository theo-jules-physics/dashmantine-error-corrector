import ast
import os
import logging

from component_info import ComponentInfo

logger = logging.getLogger(__name__)


class PackageUsageDetector:

    def __init__(self, root_dir, target_package):
        self.root_dir = root_dir
        self.target_package = target_package
        self.results = []

    def _extract_parameters(self, node):
        if isinstance(node, ast.Call):
            arguments = [
                arg.id if isinstance(arg, ast.Name) else type(arg).__name__
                for arg in node.args
            ]
            keyword_arguments = []
            for kw in node.keywords:
                if kw.arg == "children" and isinstance(
                    kw.value, (ast.Call, ast.List)
                ):
                    keyword_arguments.append((kw.arg, None))
                else:
                    keyword_arguments.append(kw.arg)

            if (
                len(arguments) == 0
                and len(keyword_arguments) == 1
                and keyword_arguments[0][1] is None
            ):
                return []

            parameters = arguments + [
                kw[0] if isinstance(kw, tuple) else kw
                for kw in keyword_arguments
            ]
            if parameters == ["List"]:
                parameters = []

            return parameters
        else:
            return []

    def scan_files(self):
        for subdir, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py"):
                    self._analyze_file(os.path.join(subdir, file))

    def _analyze_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
            file_lines = file_content.splitlines()
            try:
                tree = ast.parse(file_content, filename=file_path)
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

                    content = ('\n').join(file_lines[start_line-1:end_line])

                    parameters = self._extract_parameters(node)

                    self.results.append(
                        ComponentInfo(
                            name=component_name,
                            file_name=file_path,
                            line_limits=[start_line, end_line],
                            content=content,
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
