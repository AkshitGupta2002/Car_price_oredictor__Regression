from flask import Flask, render_template, request, redirect
import pandas as pd 
import pickle
import numpy as np 
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors=CORS(app)
model=pickle.load(open('LinearRegressionModel.pkl','rb'))
car = pd.read_csv("Cleaned_data.csv")

@app.route('/')
def index():
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    year = sorted(car['year'].unique(), reverse =True)
    fuel_type = car['fuel_type'].unique()

    return render_template('index.html', companies = companies, car_models = car_models, years = year, fuel_types = fuel_type)


@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    company = request.form.get('company')
    car_models = request.form.get('car_models')
    fuel_type=request.form.get('fuel_type')
    year = request.form.get('year')
    driven = request.form.get('kilo_driven')

    prediction=model.predict(pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'], data=np.array([car_models,company,year,driven,fuel_type]).reshape(1, 5)))

    print(prediction)
    return str(np.round(prediction[0],2))


if __name__=="main":
    app.run(debug=True)