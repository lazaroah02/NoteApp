import base64

def convert_graphqlid_to_int(id):
    print(f"ID:{id}")
    byte_id = bytes(id, "UTF-8")
    decoded_id = base64.b64decode(byte_id)
    str_id = str(decoded_id).split(":")[1]
    number_id = str_id[0:len(str_id) - 1]
    return number_id