# Python program to implement server side of chat room. 
from socket import *
import sys 
from _thread import *

# Making a server socket using the socket function.
# SOCK_STREAM specifies a TCP connection.
server = socket(AF_INET, SOCK_STREAM) 

if len(sys.argv) != 2: 
	print ("Use: python server.py <port-no>")
	exit() 

# Extracting the port number on which the server socket will listen
server_port = int(sys.argv[1])
# Binding the socket to the host '' and port provided in the command line. 
server.bind(('127.0.0.1', server_port))

listOfActiveClients, listOfActiveClientNames = [], []

def establish_connection():
	print('The server is now active and listening on port ' + str(server_port))
	server.listen(10) 

	while True: 
		try:
			# The server socket accepts a connection from a client, and the client is appended to the list of active clients.
			connectionSocket, addr = server.accept()
			connectionSocket.send("NAME".encode())
			name = connectionSocket.recv(1024).decode()
			connectionSocket.send("CONN_SUCCESS".encode())

			listOfActiveClients.append(connectionSocket)
			listOfActiveClientNames.append(name)

			# broadcast(f"###### '{name}' has joined the chatroom ######", connectionSocket, 1)
			broadcast(f"###### '{name}' has joined the chatroom ###### $PJOIN", connectionSocket, 1)

			print(f"{name} is in the chatroom! - {addr}")
			# Prints the total clients in the chatroom everytime a new client enters the chatroom.
			print('[Total clients in the chatroom = ' + str(len(listOfActiveClients)) + ']')
			
			# A new thread is started for every client getting connected to the server.
			start_new_thread(clientConnectionThread,(connectionSocket,addr))
			
		except:
			print("Error ocurred - ", sys.exc_info())
			break

# Thread function
def clientConnectionThread(client, addr): 

	sendMsg = ""
	for i in range(0, len(listOfActiveClientNames)-1):
		sendMsg += listOfActiveClientNames[i] + ","
	sendMsg += listOfActiveClientNames[len(listOfActiveClientNames)-1]
	
	client.send(f"{sendMsg}$PTLUPDT".encode())

	while True:
		# Receives messages from the client
		msg = client.recv(2048).decode()

		if 'exit()' in msg:
			deleteFromList(client, addr, msg.split(':')[0])
			client.send('CONN_CLOSED'.encode())
			# leave_msg = "###### '" + msg.split(':')[0] + "' has left the chatroom ######"
			leave_msg = "###### '" + msg.split(':')[0] + "' has left the chatroom ###### $PLEAVE"
			broadcast(leave_msg, client, 1)

		else:
			# If message is not a empty string then if is executed.	
			if msg:
				# print(msg)
				broadcast(msg, client, 0)

	client.close()

# Function used to send message of one client to all the other clients connected to the server socket.
def broadcast(message, client, exclude): 
	for c in listOfActiveClients:
		if ((exclude == 1) and (c != client)): 
			c.send(message.encode())
		elif (exclude == 0):
			c.send(message.encode())

# Function removes those client connections from the list those who have been disconnected.
def deleteFromList(connection, addr, name): 
	if connection in listOfActiveClients: 
		listOfActiveClients.remove(connection)
		listOfActiveClientNames.remove(name)
		print(f"{name} just left the chatroom! - {addr}")
		print('[Total clients in the chatroom = ' + str(len(listOfActiveClients)) + ']')

establish_connection()