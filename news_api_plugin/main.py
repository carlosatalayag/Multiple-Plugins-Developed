import json
import newsapi_conection

import flask, requests, json
from flask import Flask, request, make_response, jsonify, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route('/select_topic', methods=['POST'])
def get_topic_news():
    data = request.json
    topic = data['topic']
    news=[]
    news = newsapi_conection.get_json_tittles(topic)

    output = jsonify(news)
    return output, 200

@app.route('/select_title', methods=['POST'])
def get_new_information():
    data = request.json
    title = data['title']

    new_information = newsapi_conection.add_url_content_to_json(title)

    output = jsonify(new_information)
    return output, 200

@app.route('/get_url_information', methods=['POST'])
def get_url_information():
    data = request.json
    url = data['title']

    url_information = newsapi_conection.obtain_information_of_url(url)

    output = jsonify(url_information)
    return output, 200    

@app.route('/get_pdf_information', methods=['POST'])
def get_pdf_url_information():
    data = request.json
    url = data['title']

    url_information = newsapi_conection.get_url_doc_info(url)

    output = jsonify(url_information)
    return output, 200    

@app.get("/logo.png")
def plugin_logo():
    filename = 'logo.png'
    return flask.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        response = make_response(text, 200)
        response.mimetype = "text/json"
        return response

@app.get("/openapi.yaml")
def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        response = make_response(text, 200)
        response.mimetype = "text/plain"
        return response

def main():
    app.run(debug=True, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()