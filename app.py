from flask import Flask, request, jsonify
from ticker import fetch_ticker
from main import launch_ui 
import os

app = Flask(__name__)

@app.route('/api/getTicker', methods=['GET'])
def get_ticker():
    company = request.args.get('company')
    symbol = fetch_ticker(company)
    return jsonify({"company": company, "symbol": symbol})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    launch_ui().launch(server_name="0.0.0.0", server_port=port)
