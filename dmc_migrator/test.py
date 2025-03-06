import os
import shutil
import pytest

from dmc_migrator.dmc_migrator import DmcMigrator


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


@pytest.fixture
def setup_test_env():
    test_dir = "test_project"
    os.makedirs(test_dir, exist_ok=True)

    # Create test files
    for filename, (old_code, _) in TEST_CASES.items():
        file_path = os.path.join(test_dir, filename)
        with open(file_path, "w") as f:
            f.write(old_code)

    yield test_dir

    shutil.rmtree(test_dir)


def test_migration(setup_test_env):
    test_dir = setup_test_env

    DmcMigrator(test_dir).run()

    failed_cases = []

    for filename, (_, expected_code) in TEST_CASES.items():
        migrated_path = os.path.join(test_dir, filename)

        with open(migrated_path, "r") as f:
            migrated_code = f.read()

        if migrated_code.strip() != expected_code.strip():
            failed_cases.append((filename, migrated_code, expected_code))

    if failed_cases:
        for filename, migrated, expected in failed_cases:
            print(f"\n⚠️ Test Failed: {filename}")
            print(f"\n--- Migrated Code ---\n{migrated}")
            print(f"\n--- Expected Code ---\n{expected}")

        pytest.fail(f"{len(failed_cases)} migration test(s) failed.")

    print("✅ All migration tests passed successfully!")


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
