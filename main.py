from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
BOARD_ID = os.getenv("MONDAY_BOARD_ID")
print('Start of main.py')
@app.post("/shopify-webhook")
async def shopify_webhook(request: Request):
    data = await request.json()

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

    return {"monday_response": response.json()}