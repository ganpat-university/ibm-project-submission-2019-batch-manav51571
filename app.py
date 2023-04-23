# import required libraries
from flask import Flask, render_template, request, jsonify
from flask import *
import joblib
import numpy as np
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
import os
import requests
import json
import ssl

# create Flask app instance
app = Flask(__name__)

# creating secret key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Cross-Site Request Forgery or CSRF Protection
csrf = CSRFProtect(app)


# Cookies Protection
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)


# Wrap Flask app with Talisman
Talisman(app, content_security_policy=None)


# load the trained machine learning model
model_SF = joblib.load('Model/random_forest_SF.pkl')


# Proper HTTP headers
@app.after_request
def apply_caching(response):
	response.headers.add('X-Frame-Options', 'deny')
	response.headers["HTTP-HEADER"] = "VALUE"
	response.headers.add('X-Content-Type-Options', 'nosniff')
	response.headers.add('X-XSS-Protection', '1; mode=block')
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response



# define the home page
@app.route('/')
def home():
	return render_template('index.html')


# define the maps page
@app.route('/maps')
def maps():
	return render_template('map.html')


# define the maps page
@app.route('/sf_home')
def sf_home():
	return render_template('SF_index.html')


# define the sf EDA page
@app.route('/sf_eda')
def sf_eda():
	return render_template('SF_EDA.html')


# define the SF prediction page
@app.route('/predict_sf', methods=['POST'])
def predict_sf():

	if request.method == 'POST':

		# get the input values from the user
		area_sf = request.form['area']
		month_sf = int(request.form['month'])
		days_sf = request.form['days']
		hour_sf = int(request.form['hour_sf'])
		min_sf = int(request.form['min_sf'])
		

		days_sf_dict = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3, 'Friday':4, 'Saturday':5, 'Sunday':6}
		
		area_sf_dict = {'Bayview Hunters Point': 0, 'Bernal Heights': 1, 'Castro/Upper Market': 2, 'Chinatown': 3, 'Excelsior': 4, 
		'Financial District/South Beach': 5, 'Glen Park': 6, 'Golden Gate Park': 7, 'Haight Ashbury': 8, 'Hayes Valley': 9, 
		'Inner Richmond': 10, 'Inner Sunset': 11, 'Japantown': 12, 'Lakeshore': 13, 'Lincoln Park': 14, 'Lone Mountain/USF': 15,
		'Marina': 16, 'McLaren Park': 17, 'Mission': 18, 'Mission Bay': 19, 'Nob Hill': 20, 'Noe Valley': 21,'North Beach': 22,
		'Oceanview/Merced/Ingleside': 23, 'Outer Mission': 24, 'Outer Richmond': 25, 'Pacific Heights': 26, 'Portola': 27, 
		'Potrero Hill': 28, 'Presidio': 29, 'Presidio Heights': 30, 'Russian Hill': 31, 'Seacliff': 32, 'South of Market': 33,
		'Sunset/Parkside': 34, 'Tenderloin': 35, 'Treasure Island': 36, 'Twin Peaks': 37, 'Visitacion Valley': 38,
		'West of Twin Peaks': 39, 'Western Addition': 40}
		
		crime_sf_dict={'Arson': 0, 'Assault': 1, 'Burglary': 2, 'Case Closure': 3, 'Civil Sidewalks': 4, 'Courtesy Report': 5,
		'Disorderly Conduct': 6, 'Drug Offense': 7, 'Drug Violation': 8, 'Embezzlement': 9, 'Fire Report': 10, 
		'Forgery And Counterfeiting': 11, 'Fraud': 12, 'Gambling': 13, 'Homicide': 14, 
		'Human Trafficking (A), Commercial Sex Acts': 15, 'Human Trafficking (B), Involuntary Servitude': 16,
		'Human Trafficking, Commercial Sex Acts': 17, 'Larceny Theft': 18, 'Liquor Laws': 19, 
		'Lost Property': 20, 'Malicious Mischief': 21, 'Miscellaneous Investigation': 22, 'Missing Person': 23, 
		'Motor Vehicle Theft': 24, 'Motor Vehicle Theft?': 25, 'Non-Criminal': 26,
		'Offences Against The Family And Children': 27, 'Prostitution': 28, 'Rape': 29, 'Recovered Vehicle': 30, 
		'Robbery': 31, 'Sex Offense': 32, 'Stolen Property': 33, 'Suicide': 34, 'Suspicious': 35, 'Suspicious Occ': 36,
		'Traffic Collision': 37, 'Traffic Violation Arrest': 38, 'Vandalism': 39, 'Vehicle Impounded': 40, 
		'Vehicle Misplaced': 41, 'Warrant': 42, 'Weapons Carrying Etc': 43, 'Weapons Offence': 44, 'Weapons Offense': 45}


		if str(area_sf) not in area_sf_dict.keys():
			return render_template('404.html')

		if days_sf not in days_sf_dict.keys():
			return render_template('404.html')
		
		if not str(month_sf).isdigit() or not 0 <= month_sf < 13:
			return render_template('404.html')
		
		if not str(hour_sf).isdigit() or not 0 <= hour_sf < 24:
			return render_template('404.html')
		
		if not str(min_sf).isdigit() or not 0 <= min_sf < 60:
			return render_template('404.html')

		index_inp_day = days_sf_dict.get(days_sf)

		index_inp_neigh = area_sf_dict.get(area_sf)

		prediction = model_SF.predict([[index_inp_day, index_inp_neigh, min_sf, hour_sf, month_sf]])

		index_out_crimecat = list(crime_sf_dict.keys())[list(crime_sf_dict.values()).index(prediction)]

		# Render the Prediction Page
		return render_template('predicted_crime.html', prediction_text=index_out_crimecat, place="San Francisco")



@app.route('/search', methods=['GET','POST'])
def search():

	if request.method == 'POST':

		search_term = request.form['search_term']
		with open('static/own-assets/json/data.json') as f:
			data = json.load(f)
			for item in data:
				if item['name'] == search_term:
					return redirect(item['url'])

		return redirect(url_for('maps'))

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('cert.pem', 'key.pem')
app.run(ssl_context=context)
#app.run(debug=True)