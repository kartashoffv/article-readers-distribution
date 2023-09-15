from flask import Flask, request, jsonify
from main import *
import codecs
import json

app = Flask(__name__)

texts_init = []

@app.route('/add_text', methods=['POST'])
def add_text():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Check if 'texts' field is present in JSON data
        if 'texts' in data:
            # Ensure that 'texts' is a list of strings
            if isinstance(data['texts'], list):
                # Append the texts to the list
                texts_init.extend(data['texts'])
                return jsonify({"message": "Texts added successfully"}), 200
            else:
                return jsonify({"error": "Field 'texts' must be a list of strings"}), 400
        else:
            return jsonify({"error": "Field 'texts' is required in JSON data"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_distr', methods=['GET'])
def get_texts():
    dist_output = [text for text in texts_init]
    cats = get_cats_from_texts(dist_output)
    return jsonify({"texts": get_output_distributions(cats)}), 200

if __name__ == '__main__':
    app.run(debug=True)
