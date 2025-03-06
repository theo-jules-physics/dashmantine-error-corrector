import dash
import dash_mantine_components as dmc

app.layout = dmc.Button("Click me", leftSection="icon1", rightSection="icon2")

if __name__ == "__main__":
    app.run_server(debug=True)
