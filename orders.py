# Utility for Order Related methods
# 1. Create Order
# 2. Edit Order
# 3. Delete Order
# 4. Get Order: By Order Id
from monday.boards import get_board_all_columns
from monday.boards import find_column_id_from_board_data
from monday.items import create_item_record
#from monday.items import create_item
def create_order(order_board_id, order_name, order_column_values):
    """Create Order"""
    # Result Variables
    success = False
    error = ''
    status_code = None
    order_record_id = None
    # Get Board Metadata
    board_info_result = get_board_all_columns(order_board_id)
    order_metadata = board_info_result.get("metadata", {})
    # Check if there is any error in finding board
    if(board_info_result.get("success") != True):
        error = board_info_result.get("error")
        return {"success": success, "error": error}
    # Ensure Board exists
    boards = order_metadata.get("data", {}).get("boards", [])
    if (len(boards) == 0):
        error = "Board not found"
        return {"success": success, "error": error}

    # Iterate Over Each Column and Create Columns JSON
    order_column_values = {}
    for key in order_column_values.keys():
        col_title = key
        col_value = order_column_values.get(key)
        col_result = find_column_id_from_board_data(order_metadata, col_title)
        if(col_result.get("success") == True):
            col_id = col_result.get("column_id")
            order_column_values[col_id] = col_value

    print("Column Values ", order_column_values, flush=True)

    # Create Order Record
    order_creation_result = create_item_record(order_board_id, order_name, order_column_values)

    return order_creation_result

