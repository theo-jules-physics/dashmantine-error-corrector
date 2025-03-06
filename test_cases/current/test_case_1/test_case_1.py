import dash
import dash_mantine_components as dmc

app = dash.Dash(__name__)

app.layout = dmc.Container([
    dmc.Switch(label="Enable feature"),
])

if __name__ == "__main__":
    app.run_server(debug=True)
