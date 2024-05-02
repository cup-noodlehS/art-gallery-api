from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_websocket_message(user_id, message, payload ):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "websocket.send",
            "text": f"{message}: {payload}",
        },
    )

def string_to_list(string):
    # Remove the brackets and spaces from the string
    string = string.replace("[", "").replace("]", "").replace(" ", "")
    
    # Split the string by commas and convert each element to an integer
    integer_list = [int(x) for x in string.split(",")]
    
    return integer_list
    return converted_list