from flask import Flask, request, render_template, redirect

import json
from urllib.request import urlopen
webURL = urlopen("https://api.github.com/repos/atom/atom") # This will return a string containing the data in JSON format
data = webURL.read()
response_data = json.loads(data.decode('utf-8')) # parse the JSON and convert it into a dict


import requests
req_response = requests.get('https://api.github.com/repos/atom/atom').json()


app = Flask(__name__)


if __name__ == "__main__":
    print(req_response['stargazers_count'])
    print(response_data['stargazers_count'])
    app.run(debug=True)