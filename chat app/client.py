import socket,time
import chatlib  

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5680


def build_and_send_message(conn, code, data): # code = command

	message = chatlib.build_message(code,data) # create the message( will look like this: LOGIN           |0009|aaaa#bbbb)
	conn.send(message.encode()) # send to the server the message in the right format
	

def recv_message_and_parse(conn):
	full_msg = conn.recv(1024).decode() # gets the message from the server   need to be something like this for example "LOGIN           |0009|aaaa#bbbb"
	cmd, data = chatlib.parse_message(full_msg) # split it to a tuple with the command and the data
	return cmd, data
	

def connect():
    """create a socket and connect to it(to receive and send messages)"""
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket,   socket.AF_INET = IP protocol,   socket.SOCK_STREAM = protocol TCP
    my_socket.connect((SERVER_IP,SERVER_PORT)) # connect to the socket(make it able to send messages in the socket)
    return my_socket


def error_and_exit(error_msg):
    print(error_msg)
    time.sleep(10)
    exit()


def build_send_recv_parse(conn,cmd,data):
	"""send the data it received(send the data,cmd(you need to put them when you call the function) with build_and_send_message
	receive data with recv_message_and_parse and returns the data,msg_code that it received"""
	build_and_send_message(conn,cmd,data) # build+send the message to the server
	msg_code,data2 = recv_message_and_parse(conn) # get the message from the server and parse it and put it in 2 variables
	return data2,msg_code


def main():
    using_socket = connect()
    username = input("Enter your chat room username: ")
    build_and_send_message(using_socket, chatlib.PROTOCOL_CLIENT["username"],username)
    room = None
    t = time.time()
    wait_time = time.time() + 20
    while room == None:
        t = time.time()
        try:
            cmd,data = recv_message_and_parse(using_socket)
            if cmd == chatlib.PROTOCOL_SERVER["send_room"]: # if the server sent to the client his room
                room = int(data)
                print("Room" + str(room))
                break
        except:
            pass
        if t > wait_time: # waits 20 seconds for the server to get the client in a room, if didnt get it into a room it starts main() again
            main()
    room_ready = False
    print("Waiting for another guy to enter the room\n...")
    while room_ready == False:
        try:
            cmd,data = recv_message_and_parse(using_socket)
            if cmd == chatlib.PROTOCOL_SERVER["room_ready"]: # if the server sent to the client that the room is ready to talk
                print(f"Room is ready\nYou are talking with {data}\n")
                break
        except:
            pass
    build_and_send_message(using_socket, chatlib.PROTOCOL_CLIENT["ask_for_who_is_turn"], "inroom "+ str(room))
    command,turn_username = recv_message_and_parse(using_socket) # gets the username that it his turn
    
    while True:
            build_and_send_message(using_socket, chatlib.PROTOCOL_CLIENT["ask_for_who_is_turn"], "inroom "+ str(room))
            try:
                command,turn_username = recv_message_and_parse(using_socket) # gets the username that it his turn
            except ConnectionAbortedError:
                print("other user logged out of the room, you are alone in the room\n")
                main()

            if turn_username == username: # if its his/my turn
                message = str(room) + " " + input(username + ": ")
                build_and_send_message(using_socket,"MESSAGE",message) # send to the server his message
                cmd,data = recv_message_and_parse(using_socket)
                print(data)
            else: # not his turn
                try: # try to get message
                    cmd,data = recv_message_and_parse(using_socket)
                    if cmd == "MESSAGE": # only if the command is MESSAGE(it can be the turn command) it will print it
                        print(data)
                except: # gets an error if it didnt receive anything
                    pass


if __name__ == '__main__':
    try:
        main()
    except ConnectionResetError: # error that raise when it cant speak/send_messages to the server because the server closed(closed = end the program)
        error_and_exit("An Error raised\nthe server closed before closing the client") # printing the error and exit() the program