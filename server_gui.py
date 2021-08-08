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
	server.listen(1) 

	while True: 
		try:
			# The server socket accepts a connection from a client, and the client is appended to the list of active clients.
			connectionSocket, addr = server.accept()
			connectionSocket.send("NAME".encode())
			name = connectionSocket.recv(1024).decode()

			connectionSocket.send("Connection Successful!".encode())

			listOfActiveClients.append(connectionSocket)
			listOfActiveClientNames.append(name)

			print(f"{name} is in the chatroom! - {addr}")
			broadcast(f"###### {name} has joined the chatroom ######")

			# Prints the total clients in the chatroom everytime a new client enters the chatroom.
			print('[Total clients in the chatroom = ' + str(len(listOfActiveClients)) + ']')
			
			# A new thread is started for every client getting connected to the server.
			start_new_thread(clientConnectionThread,(connectionSocket,addr))
			
		except:
			print("Error ocurred")
			break

# Thread function
def clientConnectionThread(client, addr): 

	while True:
		# Receives messages from the client
		msg = client.recv(2048).decode()

		if 'exit()' in msg:
			deleteFromList(client, addr)
			client.send('CONN_CLOSED'.encode())
			leave_msg = "###### " + msg.split(':')[0] + " has left the chatroom ######"
			broadcast(leave_msg)

		else:
			# If message is not a empty string then if is executed.	
			if msg:
				broadcast(msg)
			# If an empty string is received means the client has disconnected.
			else:
				deleteFromList(client, addr)
		
	client.close()

# Function used to send message of one client to all the other clients connected to the server socket.
def broadcast(message): 
	for client in listOfActiveClients: 
			client.send(message.encode())

# Function removes those client connections from the list those who have been disconnected.
def deleteFromList(connection, addr): 
	if connection in listOfActiveClients: 
		listOfActiveClients.remove(connection)
		print(addr,end='')
		print(" just left the chatroom!")
		print('[Total clients in the chatroom = ' + str(len(listOfActiveClients)) + ']')

establish_connection()