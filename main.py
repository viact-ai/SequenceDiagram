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
import os

server = PlantUML(url='http://www.plantuml.com/plantuml/img/',
                        basic_auth={},
                        form_auth={}, http_opts={}, request_opts={})
    

openai.api_key = os.getenv("API_KEY")

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
    try:
        img_base64 = session["image"]
        session["image"] = ""
        return render_template("home.html", imageUrl = img_base64)
    except:
        return render_template("home.html", imageUrl = "")

@app.route("/process", methods = ["GET", "POST"])
def process():
    
    if openai.api_key == None:
        flash("No API key, please ask admin")
        return redirect("/home")

    if request.method == "POST":

        usecase = ""
        requirements = ""
        usecase = request.form["inputUsecase"]
        requirements = request.form["inputRequirements"]

        
        # check = write_to_txt("test1.txt", uml_string['choices'][0]['text'])
        try:
            uml_string =  get_uml_string(usecase, requirements)
            svg_bytes = server.processes(uml_string['choices'][0]['text'].replace('\\n', '\n'))
            base64_bytes = base64.b64encode(svg_bytes)
            base64_string = base64_bytes.decode('utf-8')
            session["image"] = base64_string
            # print(session["image"])
            return redirect("/home")
        except:
            flash("Can not generate graph base on your requirements")
            return redirect("/home")
@app.route("/changeApiKey", methods = ["GET", "POST"])
# @token_required
def changeApiKey():
    if request.method == "POST":
        
        openai.api_key = request.form["openai_key"]

        return jsonify({
            "status": "1",
            "content": "change success"
        })
    
    else:
        return jsonify({
            "status": "1",
            "content": "ping success"
        })

@app.route("/sequenceReturnUrl", methods = ["GET", "POST"])
# @token_required
def get_url_sequence():

    if request.method == "POST":

        usecase = ""
        requirements = ""
        usecase = request.form["inputUsecase"]
        requirements = request.form["inputRequirements"]
        
        try:
            uml_string =  get_uml_string(usecase, requirements)
            img_url = server.get_url(uml_string['choices'][0]['text'].replace('\\n', '\n'))
            return jsonify({
                "status": "1",
                "content": img_url
            })
        except:
            return jsonify({
                "status": "0",
                "content": "No sequence was gen"
        })
    
    else:
        return jsonify({
            "status": "1",
            "content": "ping success"
        })

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=5000)

