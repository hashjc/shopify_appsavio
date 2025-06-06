# Utility for Order Related methods
# 1. Create Order
# 2. Edit Order
# 3. Delete Order
# 4. Get Order: By Order Id
from monday.boards import get_board_all_columns
from monday.boards import find_column_id_from_board_data
from monday.boards import get_column_title_to_column_id_mapping
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
    print('Create Order method - Order columsn values input ', order_column_values, flush=True)
    #order_column_values = {}
    column_title_to_column_id_mapping = get_column_title_to_column_id_mapping(order_board_id)
    print("Order.py Order board col title to id mappings ", column_title_to_column_id_mapping, flush=True)
    for key in order_column_values.keys():
        col_title = key
        col_value = order_column_values.get(key)
        col_result = find_column_id_from_board_data(order_metadata, col_title)
        print('Create Order method - Col title, value, id ', col_title, ' value = ', col_value, ' col id res = ', col_result, flush=True)
        if(col_result.get("success") == True):
            col_id = col_result.get("column_id")
            order_column_values[col_id] = col_value

    print("Order.py Create order method: Column Values ", order_column_values, flush=True)

    # Create Order Record
    order_creation_result = create_item_record(order_board_id, order_name, order_column_values)

    return order_creation_result

