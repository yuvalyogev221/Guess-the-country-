from flask import Flask, request, jsonify
from logic import Comparison
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Server is alive!"

@app.route("/guess", methods=["POST"])
def guess():
    # Get from JS :
    data = request.get_json()

    country1 = data["country"]   # guessed
    country2 = data["target"]    # correct

    results_country1, results_country2, colors = Comparison(country1, country2)
    print(results_country1, results_country2, colors)

    # return to JS
    return jsonify({
        "colors": colors,
        "country1": results_country1, 
        "country2": results_country2
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
