import os

TEST_CASES = {
    "test_case_1.py": (
        """import dash
import dash_mantine_components as dmc

app = dash.Dash(__name__)

app.layout = dmc.Container([
    dmc.Switch(label="Enable feature"),
])

if __name__ == "__main__":
    app.run_server(debug=True)
""",
        """import dash
import dash_mantine_components as dmc

app = dash.Dash(__name__)

app.layout = dmc.Container([
    dmc.ToggleSwitch(label="Enable feature"),
])

if __name__ == "__main__":
    app.run_server(debug=True)
""",
    ),
    "test_case_2.py": (
        """import dash
import dash_mantine_components as dmc

app.layout = dmc.Button("Click me", leftIcon="icon1", rightIcon="icon2")

if __name__ == "__main__":
    app.run_server(debug=True)
""",
        """import dash
import dash_mantine_components as dmc

app.layout = dmc.Button("Click me", leftSection="icon1", rightSection="icon2")

if __name__ == "__main__":
    app.run_server(debug=True)
""",
    ),
    "test_case_3.py": (
        """import dash
import dash_mantine_components as dmc

app.layout = dmc.Grid([
    dmc.Col(span=4, children=dmc.Text("Column 1")),
    dmc.Col(span=8, children=dmc.Text("Column 2"))
])

if __name__ == "__main__":
    app.run_server(debug=True)
""",
        """import dash
import dash_mantine_components as dmc

app.layout = dmc.Grid([
    dmc.GridCol(span=4, children=dmc.Text("Column 1")),
    dmc.GridCol(span=8, children=dmc.Text("Column 2"))
])

if __name__ == "__main__":
    app.run_server(debug=True)
""",
    ),
    "test_case_4.py": (
        """import dash
import dash_mantine_components as dmc

app.layout = dmc.Stack(
    position="center",
    spacing="md",
    children=[dmc.Text("Stack Item 1"), dmc.Text("Stack Item 2")]
)

if __name__ == "__main__":
    app.run_server(debug=True)
""",
        """import dash
import dash_mantine_components as dmc

app.layout = dmc.Stack(
    justify="center",
    gap="md",
    children=[dmc.Text("Stack Item 1"), dmc.Text("Stack Item 2")]
)

if __name__ == "__main__":
    app.run_server(debug=True)
""",
    ),
    "test_case_5.py": (
        """import dash
import dash_mantine_components as dmc

app.layout = dmc.Stack(
    position="center",
    spacing="md",
    children=[dmc.Text("Stack Item 1"), dmc.Text("Stack Item 2")]
)

if __name__ == "__main__":
    app.run_server(debug=True)
""",
        """import dash
import dash_mantine_components as dmc

app.layout = dmc.Stack(
    justify="center",
    gap="md",
    children=[dmc.Text("Stack Item 1"), dmc.Text("Stack Item 2")]
)

if __name__ == "__main__":
    app.run_server(debug=True)
""",
    ),
}


def create_test_case_folders(base_dir):
    current_dir = os.path.join(base_dir, "current")
    target_dir = os.path.join(base_dir, "target")

    os.makedirs(current_dir, exist_ok=True)
    os.makedirs(target_dir, exist_ok=True)

    for filename, (old_code, expected_code) in TEST_CASES.items():
        case_name = filename.replace(".py", "")
        current_case_dir = os.path.join(current_dir, case_name)
        target_case_dir = os.path.join(target_dir, case_name)

        os.makedirs(current_case_dir, exist_ok=True)
        os.makedirs(target_case_dir, exist_ok=True)

        old_code_path = os.path.join(current_case_dir, filename)
        expected_code_path = os.path.join(target_case_dir, filename)

        with open(old_code_path, "w") as f:
            f.write(old_code)

        with open(expected_code_path, "w") as f:
            f.write(expected_code)


if __name__ == "__main__":
    test_dir = "test_cases"
    create_test_case_folders(test_dir)
