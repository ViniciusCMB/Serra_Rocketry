from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div(
    [
        daq.LEDDisplay(id="y", label="Stopwatch", value=10),
        html.Center(
            [
                html.Header("Enter seconds"),
                dcc.Input(
                    id="myinput",
                    type="number",
                    placeholder="10",
                    value=10,
                ),
            ]
        ),
        dcc.Interval(
            id="trigger-while-button-on", interval=1000, n_intervals=0
        ),
        daq.PowerButton(
            id="start", on=False
        ),
    ]
)


@app.callback(
    Output("y", "value"),
    Input("trigger-while-button-on", "n_intervals"),
    Input("myinput", "value"),
    Input("start", "on"),
    Input("y", "value"),
)
def update_output(n, input_value, start_watch, led_value):
    if input_value != None and start_watch == False:
        return int(input_value)
    if n >= 0 and start_watch == True:
        if led_value > 0:
            led_value -= 1
            return led_value
        if led_value == 0:
            print("Time's up!")
            return led_value
    return led_value


if __name__ == "__main__":
    app.run_server(debug=True)