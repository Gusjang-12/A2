import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pickle
import numpy as np

filename_new= 'polynomial_regression.pkl'
filename_old = 'car2.model'

model_old = pickle.load(open(filename_old, 'rb'))
model_new = pickle.load(open(filename_new, 'rb'))

app = dash.Dash(__name__, suppress_callback_exceptions=True)

navbar = html.Div([
    dcc.Link('Home', href='/'),
    dcc.Link(' | Old Model ', href='/old_model'),
    dcc.Link(' | New Model', href='/new_model'),
])

home_layout = html.Div([
    html.H1("Welcome to Car Price Prediction App"),
    html.P("Select a model from the navigation bar."),
])

model_layout = lambda model_name, model: html.Div([
    html.H1(f"Car Price Prediction - {model_name}"),
    html.P("Enter the car features to get a price prediction."),
    
    html.Label("Max Power (bhp):"),
    dcc.Input(id="power", type="number", value=82.4),
    
    html.Label("Mileage (kmpl):"),
    dcc.Input(id="mileage", type="number", value=19.392),
    
    html.Label("Year:"),
    dcc.Input(id="year", type="number", value=2010),

    html.Label("Engine:"),
    dcc.Input(id="engine", type="number", value=1250),

    html.Label("Seats:"),
    dcc.Input(id="seats", type="number", value=5, step=1),
    
    html.Button("Predict", id=f"predict-btn-{model_name}", n_clicks=0),
    html.H2(id=f"output-price-{model_name}", children="Predicted price will be shown here")
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/old_model':
        return model_layout("Old Model", model_old)
    elif pathname == '/new_model':
        return model_layout("New Model", model_new)
    else:
        return home_layout

def create_prediction_callback(model_name, model,use_exp=False):
    @app.callback(
        Output(f"output-price-{model_name}", "children"),
        Input(f"predict-btn-{model_name}", "n_clicks"),
        [Input("power", "value"), Input("mileage", "value"), Input("year", "value"),
         Input("engine", "value"), Input("seats", "value")]
    )
    def predict(n_clicks, power, mileage, year, engine, seats):
        if n_clicks > 0:
            input_data = np.array([[year, power, mileage, engine, seats]])
            price = model.predict(input_data)[0]
            real_price = np.exp(price) if use_exp else price
            return f"The predicted car price is: ฿{real_price:,.2f}"
        return "Enter values and press predict."
        
create_prediction_callback("Old Model", model_old ,use_exp=True)
create_prediction_callback("New Model", model_new,use_exp=False)

if __name__ == "__main__":
    #app.run_server(debug=True)
    app.run(host='0.0.0.0', port=224)
