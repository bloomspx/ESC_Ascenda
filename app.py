from codecs import ignore_errors
from flask import Flask, render_template, request, redirect, jsonify
from transformers import pipeline
from bs4 import BeautifulSoup, UnicodeDammit
from nlp import run_chatterbox, generate_sentiments, generate_summary, generate_word_cloud
from utils import extract_text
from flask_cors import CORS
import pandas as pd
import requests, os, time, sys, base64

app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['GET'])
def home():
    return "Flask server is currently running on localhost:5000."

@app.route('/upload', methods=['POST'])
def upload():
    request_file = request.get_json()
    text = request_file['text']
    print(text)
    text_file = open("data/dataurlPDF.txt", "w", encoding='utf-8')
    text_file.write(text)
    text_file.close()
    return 200

@app.route('/save-file', methods=['POST'])
def saveFile():
    request_file = request.get_json()
    # print(request_file)
    filename = request_file['name']
    text = request_file['text']
    text = text.strip()

    if filename != "":
        text_file = open("data/temp.txt", "w", encoding='utf-8')
        text_file.write(text)
        text_file.close()
        try:
            # text_file = open("data/temp.txt", "w", encoding='utf-8')
            # filedata = "".join(text)
            # text_file.write(dataURL)
            # text_file.close()
            # text = extract_text(filename)
            print("text", text)
            num_words = len(text.split(' '))
            num_sent = len(text.split('.'))

            print("Total wordcount:", num_words)
            print("Total sentences:", num_sent)
            return jsonify({'wordcount': num_words, 'sentcount':num_sent}), 200
        except Exception as err:
            return jsonify({'error': err}), 500

@app.route('/sentiment-analysis', methods=['GET'])
def sentimentanalysis():
    try:
        with open("data/temp.txt", "r", encoding='utf-8') as f:
            lines = f.readlines()
            text = "".join(lines)
            result = generate_sentiments(text)
            return jsonify({'sentiments': result}), 200
    except Exception as err:
        return jsonify({'error': err}), 500

@app.route('/summary', methods=['GET'])
def summarize():
    try:
        with open("data/temp.txt", "r", encoding='utf-8') as f:
            lines = f.readlines()
            text = "".join(lines)
            result = generate_summary(text)
            return jsonify({'summary': result}), 200
    except Exception as err:
        return jsonify({'error': err}), 500

@app.route('/wordcloud', methods=['GET'])
def wordcloud():
    try:
        with open("data/temp.txt", "r", encoding='utf-8') as f:
            lines = f.readlines()
            text = "".join(lines)
            result = generate_word_cloud(text)
            return jsonify({'wordcloud': result}), 200
    except Exception as err:
        return jsonify({'error': err}), 500




@app.route('/text-analysis', methods=['POST'])
def performTA():
    
    request_file = request.get_json()
    print(request_file)
    filename = request_file['name']
    filedata = request_file['text']


    if filename != "":
        text_file = open("data/temp.txt", "w", encoding='utf-8')
        n = text_file.write(filedata)
        text_file.close()
    try:
        result = run_chatterbox("temp.txt")
        return jsonify({'result': result}), 200
    except Exception as err:
        return jsonify({'error': err}), 500

@app.route('/text-to-speech', methods=['GET', 'POST'])
def performTTS():
    ### TODO
    return
    

if __name__ == '__main__':
    app.run(debug=True)