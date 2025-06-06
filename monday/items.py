"""
Creating Monday APIs related to item record creation, edit and deletion.
1. Item Create
"""
# Boards related API Calls
import requests
import json

# Load your API key and board ID
MONDAY_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjUyMjU5NjU2OSwiYWFpIjoxMSwidWlkIjo3Njc0NjQ1OSwiaWFkIjoiMjAyNS0wNi0wNVQxNTowNzowNC40MDFaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjk2NTAyMjEsInJnbiI6ImFwc2UyIn0.TY4oQYraqw6fuq6I10A5Ga5JMn3LGoZv8qIQawbQlDY"


def create_item_record(board_id, item_name, column_values):
    """
    Input:
    1) Board Id - As Integer
    2) Item Name
    3) Column Values: Dictionary.
    Pass column_id: column_value type of key value pairs.
    Ensure you check date, person and picklist fields's appropriate format.

    """
    # Format values into a JSON string and escape it for GraphQL
    column_values_str = json.dumps(column_values).replace('"', '\\"')
    # Create GraphQL query
    query = f'''
        mutation {{
            create_item (
                board_id: "{board_id}",
                item_name: "{item_name}",
                column_values: "{column_values_str}"
            ) {{
                id
            }}
        }}
    '''
    # Set headers
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }
    # Result Variables
    result = None
    status_code = None
    error = None
    success = False
    item_id = None
    # Send POST request to Monday.com API
    try:
        response = requests.post("https://api.monday.com/v2", headers=headers, json={"query": query})
        response.raise_for_status()
        result = response.json()
        status_code = response.status_code
        success = True
        item_id = result.get("data", {}).get("create_item", {}).get("id")
    except requests.exceptions.Timeout as te:
        # Retry, or continue in a retry loop
        error = f'Timeout exception {te}'
    except requests.exceptions.TooManyRedirects as re:
        # Tell the user their URL was bad and try a different one
        error = f'Too many redirects {re} '
    except requests.exceptions.RequestException as e:
        error = f'HTTP Exception {e}'
        status_code = response.status_code
    except Exception as e:
        error = f'Exception occurred {e}'


    return {
        'success': success,
        'status_code': status_code,
        'metadata': result,
        'error': error,
        'item_id': item_id
    }
