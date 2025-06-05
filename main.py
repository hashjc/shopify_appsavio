from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
BOARD_ID = os.getenv("MONDAY_BOARD_ID")

print('Start of main.py')

@app.route('/')
def home():
    return "Hello from Render home page!"

@app.route('/order_create', methods=['POST'])
def order_created_in_shopify():
    """
    Order Creation webhook handler
    """
    print("Order Creation method")
    data = request.get_json()
    print("Order Creation method 2 = ", data)

@app.route('/order_create_draft', methods=['POST'])
def draft_order_created_in_shopify():
    """
    Order Creation webhook handler
    """
    print("Order Creation Draft")
    data = request.get_json()
    print("Order Creation method 2 = ", data)

    order_name = data.get("name")
    email = data.get("email")
    total = data.get("total_price")

    query = '''
    mutation {
      create_item (
        board_id: %s,
        item_name: "Order %s",
        column_values: "{\"email\" : \"%s\", \"price\" : \"%s\"}"
      ) {
        id
      }
    }
    ''' % (BOARD_ID, order_name, email, total)

    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.monday.com/v2", json={"query": query}, headers=headers)

    return jsonify({"monday_response": response.json()})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    # Single threaded and not secure using app.run() but any ways
    # It runs Flask's development server, which is fine for local testing but not recommended on Render or any production environment.
    app.run(host='0.0.0.0', port=port)

