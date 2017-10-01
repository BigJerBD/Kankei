from flask import Flask
from flask import render_template
import json
import requests

app = Flask(__name__)
MASHAPE_KEY = "waM1hvB1DVmshH9ViklToYsuQS7ep1fAu0GjsnWTIG7IYQouh7"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test/test1.json")
def get_data():
    with open('data/test1.json') as data_file:
        return json.dumps(json.load(data_file))


@app.route("/query/search_kanji/<string:search_str>")
def search_kanji(search_str):
    """
    use kanji alive to search for the possible kanji
    :param search_str:
    :return list of resulting possibles kanji
    """
    response = requests.get(
        "https://kanjialive-api.p.mashape.com/api/public/search/" + search_str,
        headers={
            "X-Mashape-Key": MASHAPE_KEY,
            "Accept": "application/json"
        }
    )
    return response.json()


@app.route("/query/get_relation/<string:kanji><string:radical>")
def get_relation(kanji,radical):
    """
    get the neighbour kanji related to the radical of the kanji
    :return: a dictionary/json-object representing the graph to add
    """
    pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)