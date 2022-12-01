# Protocol Constants


CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)(the long of the 0009 numbers in there)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message(of the protocol_message in build_message() )
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"username" : "MY_NAME",
"ask_for_who_is_turn" : "WHO_TURN"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"send_room" : "IN_ROOM",
"room_ready" : "ROOM_READY",
"turn" : "USER_TURN",
"user_logged_out" : "USER_LOGGED_OUT"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	example of the function:
	build_message("LOGIN", "aaaa#bbbb") will return "LOGIN           |0009|aaaa#bbbb"
	"""
    """get the command plus data and return the protocol message(what parse_message gets)"""
    if len(cmd) > CMD_FIELD_LENGTH: # if the long of the command is longer then the most it can be
        return ERROR_RETURN
    if len(data) > MAX_DATA_LENGTH: # if the data is longer then what it should be
        return ERROR_RETURN

    protocol_message = ""
    num = len(data)
    spaces = ""
    if len(str(num)) < LENGTH_FIELD_LENGTH: # create the message spaces and the message long(009,0100)
        num1 = LENGTH_FIELD_LENGTH - len(str(num))
        num = "0"*num1 + str(num)
        spaces = " " * (CMD_FIELD_LENGTH - len(cmd)) # the spaces that there are, are the max long of the command minus(-) the long of the command
    protocol_message += str(cmd) + spaces + DELIMITER + num + DELIMITER + str(data) # implement everything you did in the function to the protocol that send   DELIMITER = |
    if len(protocol_message) > MAX_MSG_LENGTH:
        return None
    return protocol_message
#print(build_message("LOGIN", "aaaa#bbbb"))
#   return full_msg


def parse_message(data):
    """
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
    "get the message(what build_message returns) and need to return the command and the data"
    split_data = data.split("|")
    if len(split_data[0]) > CMD_FIELD_LENGTH: # if the long of the command is longer then the possible command length it will return (None,None)
        return ERROR_RETURN,ERROR_RETURN
    else:
        if len(split_data) != 3: # if the length of the list isn't 3 it doesnt fit to the protocol
            return ERROR_RETURN,ERROR_RETURN
        else:
            try: # it will get an error if it will try to int letter, if it will try to int letter it means that the data that it got wasn't correct
                for letter in split_data[1]: # if in the part that need to be int there are strings(if it doesnt space)
                    if letter != " ":
                        int(letter)
            except:
                return ERROR_RETURN, ERROR_RETURN
        cmd = ""
        for letter in split_data[0]: # remove from the command all of th e spaces
            if letter != " ":
                cmd += letter
        #print(split_data)
        data = ""  # data
        if len(split_data[2]) == int(split_data[1]): # if the long of the data is the long that it got in the message data
            data = split_data[2]
        if len(split_data[2]) != int(split_data[1]): # if the long isnt what it got in the data
            return ERROR_RETURN,ERROR_RETURN
        return cmd,data
#print(parse_message("LOGIN           |0009|aaaa#bbbb"))
#    return cmd, msg

	
def split_data(msg, expected_fields):
    """
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
    splited_list = []
    if msg.count(DATA_DELIMITER) == expected_fields:
        splited_list = msg.split(DATA_DELIMITER)
    if msg.count(DATA_DELIMITER) != expected_fields:
        splited_list = [ERROR_RETURN]
    return splited_list


def join_data(msg_fields):
    """
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns: string that looks like cell1#cell2#cell3
	"""
    msg_fields = [str(word) for word in msg_fields]
    string = DATA_DELIMITER.join(msg_fields)
    return string