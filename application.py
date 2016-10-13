from flask import Flask, jsonify, request
from crossdomain import crossdomain
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

if __name__ == "__main__":
  application.debug = True
  application.run()
