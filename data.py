import traceback

last_message: dict[int, str] = {}
last_message_id: int = 0
forwards: list


def format() -> str:
    try:
        result = ''

        # Use a for loop to iterate over the outer list
        for i, inner_list in enumerate(forwards):
            # Use another for loop to iterate over the inner list
            for j, item in enumerate(inner_list):
                # If this is the second inner list, surround the item with < and > characters
                if j == 1:
                    result += f'<#{item}> '
                else:
                    result += f'{item} '
            # Add a newline character at the end of each inner list
            result += '\n'

        # Print the result
        return (result)
    except Exception as e:
        print(e)
        print(traceback.format_exc())


def header(message: str, message_id: int, tg_chat_id: int) -> str:
    if last_message.get(tg_chat_id) is None:
        return message
    if last_message.get(tg_chat_id) == message or message_id == last_message_id:
        return ""
    else:
        return message
