from flask import Flask, request, jsonify
from orders import create_order
import requests
import os
import json
app = Flask(__name__)

MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
BOARD_ID = os.getenv("MONDAY_BOARD_ID")
ORDER_BOARD_ID = os.getenv("MONDAY_ORDERS_BOARD_ID")
headers = {
    "Authorization": "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjUyMjU5NjU2OSwiYWFpIjoxMSwidWlkIjo3Njc0NjQ1OSwiaWFkIjoiMjAyNS0wNi0wNVQxNTowNzowNC40MDFaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjk2NTAyMjEsInJnbiI6ImFwc2UyIn0.TY4oQYraqw6fuq6I10A5Ga5JMn3LGoZv8qIQawbQlDY",
    "Content-Type": "application/json"
}
print('Start of main.py BOARD ID = ', ORDER_BOARD_ID, ', token =  ', MONDAY_API_KEY, flush=True)

@app.route('/')
def home():
    print('Home page')
    return "Hello from Render home page!"

@app.route('/order_create', methods=['POST'])
def order_created_in_shopify():
    """
    Order Creation webhook handler
    """
    print("Order Creation method ", flush=True)
    data = request.get_json()
    order_board_id = 2023614902
    print("Order Creation method 2 = ", data, flush=True)
    order_number = data.get("order_number", "")
    order_id = data.get("id", "")
    order_confirmed = data.get("confirmed", None) # True or False
    order_confirmation_number = data.get("confirmation_number", None)
    order_name = data.get("name", None)
    order_notes = data.get("note", None)
    order_total_price = data.get("total_price", None)
    order_subtotal_price = data.get("subtotal_price", None)
    order_discount = data.get("total_discounts", None)
    # Create Order: Step 1 Create All columns
    ITEM_NAME = order_number
    COLUMN_VALUES = {
        "Order Id": order_id,
        "Order Confirmed": order_confirmed,
        "Order Confirmation Number": order_confirmation_number,
        "Name": order_name,
        "Notes": order_notes,
        "Total Price": order_total_price,
        "Subtotal Price": order_subtotal_price,
        "Discount": order_discount
    }
    order_creation_result = create_order(order_board_id, ITEM_NAME, COLUMN_VALUES)
    print('order creation result ', order_creation_result, flush=True)
    # Create Order Line Items as Subitems
    return order_creation_result

@app.route('/order_create_draft', methods=['POST'])
def draft_order_created_in_shopify():
    """
    Order Creation webhook handler
    """
    order_board_id = 2023614902
    print("Order Creation Draft post request ", flush=True)
    data = request.get_json()
    print("Order Creation method 2 = ", data, flush=True)
    order_id = data.get("id", "")
    order_status = data.get("status", "")
    order_name = data.get("name", "")
    email = data.get("email", "")
    total = data.get("total_price", "")


    # Column Values
    ITEM_NAME = "New Shopify Order 4"
    COLUMN_VALUES = {
        "text_mkrm4aj8": "Test Item Description",
        "numeric_mkrm4z9t": 100.5,
        "status": {"index": 1},         # 'index' is the position in the status label list
        "date4": {"date": "2025-06-05"},  # format: YYYY-MM-DD
    }
    # Format values into a JSON string and escape it for GraphQL
    column_values_str = json.dumps(COLUMN_VALUES).replace('"', '\\"')

    # Create Graph QL
    query = f'''
        mutation {{
            create_item (
                board_id: "{order_board_id}",
                item_name: "{ITEM_NAME}",
                column_values: "{column_values_str}"
            ) {{
              id
            }}
        }}
    '''
    # Make an HTTP Request
    response = requests.post("https://api.monday.com/v2", json={"query": query}, headers=headers)
    print('Draft Order method -> Resposen status code ', response.status_code, flush=True)
    print('Draft Order method -> Resposen body ', response.json(), flush=True)
    return jsonify({"monday_response": response.json()})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    # Single threaded and not secure using app.run() but any ways
    # It runs Flask's development server, which is fine for local testing but not recommended on Render or any production environment.
    app.run(host='0.0.0.0', port=port)

