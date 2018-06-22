from flask import Flask, request, jsonify
import pickle as pkl
from sklearn import tree

app = Flask(__name__)

#load saved model Logistic Regression Model
model = pkl.load(open('titanic-lr.sav','rb'))

@app.route("/")
def hello():
	return "Welcome to my landing page!!"

@app.route("/api", methods = ['POST'])
def predict():
	req_data = request.get_json()
	age = req_data['Age']
	fare = req_data['Fare']
	parch = req_data['Parch']
	pclass = req_data['Pclass']
	sibsp = req_data['SibSp']
	famsize = sibsp + parch + 1

	if req_data['Embarked'] == 'C':
		embark_c = 1
	else:
		embark_c = 0

	if req_data['Embarked'] == 'S':
		embark_s = 1
	else:
		embark_s = 0

	if req_data['Embarked'] == 'Q':
		embark_q = 1
	else:
		embark_q = 0

	if req_data['Sex'] == 'male':
		sex_bin = 1
	else:
		sex_bin = 0

	price_per = fare / famsize

	user_var = [[age
		, fare
		, parch
		, pclass
		, sibsp
		, famsize
		, price_per
		, embark_c
		, embark_s
		, embark_q
		, sex_bin]]

	output = model.predict(user_var)
	output_prod = model.predict_proba(user_var)

	return jsonify({'Prediction': output[0],
					'Confidence_Score': max(list(output_prod[0]))})

@app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
	if request.method == 'POST':  #this block is only entered when the form is submitted
		age = float(request.form['age'])
		fare = float(request.form['fare'])
		sex = request.form['sex']
		embark = request.form['embark']
		pclass = int(request.form['pclass'])
		sibsp = int(request.form['sib'])
		par = int(request.form['parents'])
		child = int(request.form['children'])

		parch = int(par) + int(child)
		famsize = int(parch) + int(sibsp) + 1
		price_per = fare / famsize


		if embark == 'C':
			embark_c = 1
		else:
			embark_c = 0

		if embark == 'S':
			embark_s = 1
		else:
			embark_s = 0

		if embark == 'Q':
			embark_q = 1
		else:
			embark_q = 0

		if sex == 'male':
			sex_bin = 1
		else:
			sex_bin = 0


		user_var = [[age
			, fare
			, parch
			, pclass
			, sibsp
			, famsize
			, price_per
			, embark_c
			, embark_s
			, embark_q
			, sex_bin]]

		output = model.predict(user_var)
		output_prod = model.predict_proba(user_var)

		if output[0] == 1:
			out_str = 'This passenger survived'
		else: 
			out_str = 'This passenger died'

		outcon = round(max(list(output_prod[0]))*100,2)

		return '''<h1>{}</h1>
				  <h1>Confidence: {}%</h1>'''.format(out_str, outcon)

	return '''<form method="POST">
				  Age: <input type="text" name="age"><br>
				  Fare (for entire family): <input type="text" name="fare"><br>
				  Passenger Class: <input type="text" name="pclass"><br>
				  Siblings: <input type="text" name="sib"><br>
				  Parents: <input type="text" name="parents"><br>
				  Children: <input type="text" name="children"><br>
				  Gender: <input type="text" name="sex"><br>
				  Port of Embarkation (C, S, Q) : <input type="text" name="embark"><br>
				  <input type="submit" value="Submit"><br>
			  </form>'''

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')
