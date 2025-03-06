import dash
import dash_mantine_components as dmc

app.layout = dmc.Stack(
    position="center",
    spacing="md",
    children=[dmc.Text("Stack Item 1"), dmc.Text("Stack Item 2")]
)

if __name__ == "__main__":
    app.run_server(debug=True)
