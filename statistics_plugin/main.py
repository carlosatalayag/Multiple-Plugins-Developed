import json
import csv_utils 

import flask, requests, json
from flask import Flask, request, make_response, jsonify, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)

csv_name = ''

@app.get("/get_csvs")
def get_memes():
    csvs=[]
    csvs = csv_utils.list_csvs()

    output = jsonify(csvs)
    return output, 200

@app.route('/select_csv', methods=['POST'])
def select_csv():
    global csv_name
    data = request.json
    name = data['csv']
    csv_name = name
    #return csv information
    json_information = csv_utils.csv_information(name)
    return json_information

@app.route('/select_column', methods=['POST'])
def select_column():
    data = request.json
    column = data['column']
    # return general statistcis of column selected
    column_description = csv_utils.column_description(csv_name, column)
    return column_description

@app.get("/get_image")
def get_image():
    file = 'images.png'
    #return render_template('img_render.html', image=file)
    return send_from_directory('static', 'images.png')

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
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()