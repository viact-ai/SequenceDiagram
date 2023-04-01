import streamlit as st
import openai
from plantuml import PlantUML
from os.path import abspath
from PIL import Image
import json 
from gptUtils import get_uml_string, write_to_txt
from flask import Flask,request,redirect, url_for, send_from_directory,Response,jsonify,make_response, render_template, flash, session
from flask_session import Session
import base64
import plantuml
from io import BytesIO
server = PlantUML(url='http://www.plantuml.com/plantuml/img/',
                        basic_auth={},
                        form_auth={}, http_opts={}, request_opts={})
    

openai.api_key = ""

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def start():
    session["image"] = ""
    return redirect("/home")

@app.route("/home", methods = ["GET", "POST"])
def home():
    img_base64 = session["image"]
    session["image"] = ""
    return render_template("home.html", imageUrl = img_base64)

@app.route("/process", methods = ["GET", "POST"])
def process():
    
    if openai.api_key == "":
        flash("No API key, please ask admin")
        return redirect("/home")

    if request.method == "POST":

        usecase = ""
        requirements = ""
        usecase = request.form["inputUsecase"]
        requirements = request.form["inputRequirements"]

        uml_string =  get_uml_string(usecase, requirements)
        check = write_to_txt("test1.txt", uml_string['choices'][0]['text'])
        try:

            svg_bytes = server.processes(uml_string['choices'][0]['text'].replace('\\n', '\n'))
            base64_bytes = base64.b64encode(svg_bytes)
            base64_string = base64_bytes.decode('utf-8')
            session["image"] = base64_string
            # print(session["image"])
            return redirect("/home")
        except:
            flash("Can not generate graph base on your requirements")
            return redirect("/home")


if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=5000)

