# Boards related API Calls
import requests
import json

# Load your API key and board ID
MONDAY_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjUyMjU5NjU2OSwiYWFpIjoxMSwidWlkIjo3Njc0NjQ1OSwiaWFkIjoiMjAyNS0wNi0wNVQxNTowNzowNC40MDFaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjk2NTAyMjEsInJnbiI6ImFwc2UyIn0.TY4oQYraqw6fuq6I10A5Ga5JMn3LGoZv8qIQawbQlDY"

def get_board_all_columns(board_id):
    """Input: Single Board Id"""
    # GraphQL query to fetch board columns
    query = f'''
        query {{
            boards(ids: [{board_id}]) {{
                columns {{
                id
                title
                type
                settings_str
                }}
            }}
        }}
    '''

    # Set headers
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }
    # Result Variables
    data = None
    status_code = None
    error = None
    success = False
    # Send POST request to Monday.com API
    try:
        response = requests.post("https://api.monday.com/v2", headers=headers, json={"query": query})
        response.raise_for_status()
        data = response.json()
        status_code = response.status_code
        success = True
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
        'metadata': data,
        'error': error
    }


def get_column_title_to_column_id_mapping(board_id):
    """
    Input
        1) Board Id:
    Output:
        1) Column Title to Column Id mappings:
        If a column title is repeated the first occurrence's id is returned
    """
    error = ''
    column_title_to_id_mapping = {}
    if(board_id is None or len(str(board_id)) == 0):
        error = 'Board Id is blank'
        return {"success": False, "error": error}
    # Get Board Information
    board_info_result = get_board_all_columns(board_id)
    if(board_info_result.get("success") == True):
        result = board_info_result.get("metadata", {})
        boards = result.get("data", {}).get("boards", [])
        if (len(boards) == 0):
            error = "Board not found"
            return {"success": False, "error": error}
        # Get Board Columns
        columns = boards[0].get("columns", [])
        for column in columns:
            col_title = column.get("title")
            col_id = column.get("id")
            if col_title not in column_title_to_id_mapping:
                column_title_to_id_mapping[col_title] = col_id
        return {"success": True, "error": "", "mapping": column_title_to_id_mapping}
    else:
        return {"success": False, "error": board_info_result.get("error", "An error finding board")}

def find_column_id_from_board_data(board_data, column_title):
    """
    Input:
        1) Board Data: As it is
        2) Column Title: To match
    """
    success = False
    error = ''
    column_id = None
    column_info = {}
    boards = board_data.get("data", {}).get("boards", [])
    if (len(boards) == 0):
        error = "Board not found"
        return {"error": error, "success": success, "column_id": column_id, "column_info": column_info}
    # Get Board Columns
    columns = boards[0].get("columns", [])
    for column in columns:
        if column.get("title") == column_title:
            success = True
            column_info = column
            column_id = column.get("id", None)
            return {"error": "", "success": success, "column_id": column_id, "column_data": column}
    else:
        return {"error": f"Column {column_title} did Not match ", "success": False, "column_id": column_id, "column_data": column}

def find_column_id_from_column_title(board_id, column_title):
    """
    Input:
        1) Board Id: To return boards's metadata. Ensure You give Single Board Id as integer
        2) Column Title: To match
    """
    success = False
    error = ''
    column_id = None
    column_info = {}
    if((board_id is None or len(str(board_id)) == 0) or
       (column_title is None or len(column_title) == 0)):
        return {"success": success, "column_id": column_id, "column_info": column_info}
    # Get Board Information
    board_info_result = get_board_all_columns(board_id)
    if(board_info_result.get("success") == True):
        result = board_info_result.get("metadata", {})
        boards = result.get("data", {}).get("boards", [])
        if (len(boards) == 0):
            error = "Board not found"
            return {"error": error, "success": False, "column_id": column_id, "column_info": column_info}
        # Get Board Columns
        columns = boards[0].get("columns", [])
        for column in columns:
            if column.get("title") == column_title:
                column_info = column
                column_id = column.get("id", None)
                return {"error": "", "success": True,  "column_id": column_id, "column_data": column}


