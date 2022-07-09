#*********FLASK IS A WEB FRAMEWORK USED TO BUILD A WEB APP FOR THE CHATBOT***********


#Import the Flask object 

from flask import Flask, render_template, request, jsonify, make_response

#Importing the chat module from docbot.py file
from docbot import chat

#Creating a Flask application instance that holds name of current Python module
app = Flask(__name__)

#@app.route is a decorator to handle incoming web requests and send responses to the user
@app.route('/', methods = ['GET', 'POST'])

#Creating function to handle request and display web page
def indexpage():
	if request.method == "POST":

		print(request.form.get('name'))
		return render_template("index.html")
	return render_template("index.html")

@app.route("/entry", methods=['POST'])
def entry():
	req = request.get_json()
	print(req)
	res = make_response(jsonify({"name":"{}.".format(chat(req)),"message":"OK"}), 200)
	return res

#Used for automatically start this file
if __name__ == "__main__":
	app.run(debug=True)
