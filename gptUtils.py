import streamlit as st
import openai
from plantuml import PlantUML
from os.path import abspath
from PIL import Image
import json 


def get_uml_string(usecase, requirements):

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt='''
                Can you generate UML diagram for {} with requirements: 
                {}
                Return staruml format in 1000 tokens, notice to syntax, ignore syntax error (Just return UML code)'''
                .format(usecase, requirements),
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )

    return response

def write_to_txt(txt_file, uml_string):
    f = open(txt_file,"w")
    f.write(uml_string)
    f.close()
    return 1
