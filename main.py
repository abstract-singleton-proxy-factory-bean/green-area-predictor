import json, pandas as pd
from sklearn import linear_model
from flask import Flask, request, render_template, jsonify

dataframe = pd.read_csv('data/data.csv')
regression = linear_model.LinearRegression()
regression.fit(dataframe[['year']], dataframe.percentage)

def predict_percentage(year: int) -> int:
    prediction = regression.predict([[year]])

    return prediction[0]


app = Flask(__name__, template_folder="templates")

def get_default_data():
    with open('data/data.json', 'r') as file:
        content = ''.join(file.readlines())
        return json.loads(content)

@app.get("/")
def root():
    return render_template("index.html"), 200


@app.get("/predict")
def predict():
    year = int(request.args.get("year", 2021))

    if year < 2021 or year > 2040:
        return "<h1>Erro</h1>", 400

    return render_template("predict.html", context={
        "year": year,
        "green_area": predict_percentage(year)
    }), 200

@app.get("/api/predict")
def api_predict():
    years_range = int(request.args.get("year", 2021))

    if years_range < 2021 or years_range > 2040:
        return {}, 200

    file_data = get_default_data()
    predicted_data = [{ "year": year, "percentage": predict_percentage(year) } for year in range(2020, years_range + 1)]

    file_data += predicted_data
    return jsonify(file_data), 200


if __name__ == '__main__':
    app.run(debug=True, port=8081)
