from flask import Flask, jsonify, request
from crossdomain import crossdomain
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

import os
import json
import requests

application = Flask(__name__)

@application.route("/typeform", methods=["GET"])
@crossdomain(origin='*')
def typeform_get():
  """ Gets the most recent submission for a specific typeform
  """

  uid = request.args.get("uid")
  api_key = request.args.get("key")
  url = "https://api.typeform.com/v1/form/" + uid + "?key=" + api_key + "&order_by[]=date_submit,desc&limit=1"

  r = requests.get(url)
  context = r.json()["responses"][0]["answers"]
  return jsonify(**context)

@application.route("/yelp", methods=["GET"])
@crossdomain(origin='*')
def yelp_search():
  # read API keys
  if "consumer_key" in os.environ:
    auth = Oauth1Authenticator(
      consumer_key=os.environ['consumer_key'],
      consumer_secret=os.environ['consumer_secret'],
      token=os.environ['token'],
      token_secret=os.environ['token_secret']
    )
  else:
    with open('config_secret.json') as cred:
      creds = json.load(cred)
      auth = Oauth1Authenticator(**creds)
      client = Client(auth)

  client = Client(auth)

  params = {
    'term': request.args.get('category', 'food'),
    'lang': 'en'
  }
  response = client.search('South Bend, IN', **params)
  businesses = response.businesses
  results = {b.name: {"business_url": b.url, "image_url": b.image_url, "snippet": b.snippet_text} for b in businesses}
  return jsonify(**results)

if __name__ == "__main__":
  application.debug = True
  application.run()
