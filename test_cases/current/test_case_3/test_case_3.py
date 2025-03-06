import dash
import dash_mantine_components as dmc

app.layout = dmc.Grid([
    dmc.Col(span=4, children=dmc.Text("Column 1")),
    dmc.Col(span=8, children=dmc.Text("Column 2"))
])

if __name__ == "__main__":
    app.run_server(debug=True)
