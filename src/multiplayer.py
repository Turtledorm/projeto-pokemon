#!/usr/bin/env python3

from flask import Flask, Response, request
from main import *
from pokemon import *

app = Flask(__name__)

poke = Pokemon(le_pokemon())

@app.route("/battle/")
def inicia_batalha(poke):
    battle_state = cria_bs(poke)
    return battle_state
    


### <TESTES> ###

@app.route('/')
def hello_world():
    x = input("Digite o nº do ataque: ")
    return "Hello World!"


@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')

### </TESTES> ###


def cria_bs(poke):
    return ('<?xml version="1.0" encoding="utf-8"?>'
          + "<battle_state>"
          + poke.to_xml()
          + "</battle_state>")



    app.debug = True
    app.run()  # Usar host='0.0.0.0' para server público
