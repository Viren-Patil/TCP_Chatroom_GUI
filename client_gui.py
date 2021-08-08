
# import all the required  modules
import sys
from socket import *
from _thread import *
from tkinter import *
from tkinter import font
from tkinter import ttk

# Creating a TCP client side socket
clientSocket = socket(AF_INET, SOCK_STREAM) 
if len(sys.argv) != 2: 
	print ("Usage: python client.py <port-no>")
	exit() 
	
server_host = '127.0.0.1'
server_port = int(sys.argv[1])
# Connecting the client socket to the server socket.
clientSocket.connect((server_host, server_port))

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self):
       
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
         
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.login.resizable(width = False,
                             height = False)
        self.login.configure(width = 400,
                             height = 300,
                             bg="#075E54")
        # create a Label
        self.pls = Label(self.login,
                       text = "Please enter your name",
                       justify = CENTER,
                       font = "Helvetica 14 bold",
                       bg="#075E54",
                       fg="white")
         
        self.pls.place(relwidth=1, rely=0.2)
         
        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                             font = "Helvetica 14",
                             bg="#042F2A",
                             fg="white",
                             justify=CENTER,
                             borderwidth=0,
                             insertbackground="white")
         
        self.entryName.place(relwidth = 0.5, rely = 0.35, relx = 0.25)
         
        # set the focus of the curser
        self.entryName.focus()
         
        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text = "Join the Room",
                         font = "Helvetica 14 bold",
                         bg="#042F2A",
                         borderwidth=0,
                         fg="white",
                         command = lambda: self.goAhead(self.entryName.get()))
         
        self.go.place(relwidth=0.5 ,relx = 0.25, rely = 0.55)
        self.Window.mainloop()
 
    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)

        start_new_thread(self.receiveMsgs,(clientSocket,))
 
    # The main layout of the chat
    def layout(self,name):
       
        self.name = name
        self.sendImg = PhotoImage(file="send2.png")
        self.participantsImg = PhotoImage(file="group.png")
        # to show chat window
        self.Window.deiconify()
        self.Window.protocol("WM_DELETE_WINDOW", self.handle_closure)
        self.Window.title("Chatroom")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 500,
                              height = 550,
                              bg = "#042F2A")

        self.header = Frame(self.Window, bg="#042F2A")
        self.header.place(relwidth=1)
        self.labelHead = Label(self.header,
                             bg = "#042F2A",
                              fg = "white",
                              text = self.name ,
                               font = "Helvetica 14 bold",
                               width = 5,
                               pady = 5)
        self.labelHead.pack(side=LEFT)
        
        self.participants = Button(self.header,
                                image = self.participantsImg,
                                width = 45,
                                bg = "#042F2A",
                                borderwidth=0,
                                command= lambda : self.popup())
        self.participants.pack(side=RIGHT)

        self.line = Label(self.Window,
                          width = 450,
                          bg = "#075E54")
         
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
        
        self.textCons = Text(self.Window,
                             width = 20,
                             height = 2,
                             bg = "#042F2A",
                             fg = "white",
                             wrap = WORD,
                             font = "Helvetica 13",
                             padx = 15,
                             pady = 5)
         
        self.textCons.place(relheight = 0.795,
                            relwidth = 1,
                            rely = 0.08)
         
        self.labelBottom = Label(self.Window,
                                 bg = "#075E54",
                                 height = 60)
         
        self.labelBottom.place(relwidth = 1,
                               rely = 0.875)
         
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#042F2A",
                              fg = "white",
                              font = "Helvetica 13",
                              borderwidth=0,
                              insertbackground="white")
         
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
         
        self.entryMsg.focus()
         
        self.entryMsg.bind('<Return>', self.keyPress)

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                image = self.sendImg,
                                width = 20,
                                bg = "#042F2A",
                                borderwidth=0,
                                command = lambda : self.sendButton(self.entryMsg.get()))
         
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06,
                             relwidth = 0.22)
         
        self.textCons.config(cursor = "arrow")
         
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons, width=13)
         
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 1)
         
        scrollbar.config(command = self.textCons.yview)
         
        self.textCons.config(state = DISABLED)

    def keyPress(self, event):
        self.sendButton(self.entryMsg.get())

    def popup(self):
        pt = Toplevel()
        pt.title("Participants")
        pt.geometry("400x250")
        pt.resizable(width = False,height = False)
        # root.configure(bg="#042F2A")
        mainframe = Frame(pt)
        mainframe.pack(fill=BOTH, expand=1)

        canvas = Canvas(mainframe, bg="#075E54")
        canvas.pack(side=LEFT, fill=BOTH, expand = 1)

        scrollbar2 = Scrollbar(mainframe, orient = VERTICAL, command=canvas.yview)
        scrollbar2.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar2.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all"))) 

        mainframe2 = Frame(canvas)
        canvas.create_window((100,0), window=mainframe2, anchor="nw")

        for k in range(1, 100):
            btn = Label(mainframe2, text=f"Person {k}", font="Helvetica 13 bold", bg="#042F2A", fg="white", width=20, pady=10)
            btn.pack()

    # A function to start the thread for sending messages
    def sendButton(self, msg):
        if(msg):
            self.textCons.config(state = DISABLED)
            self.msg=msg
            self.entryMsg.delete(0, END)

            start_new_thread(self.sendMsgs,(clientSocket,))

    # Function to actually send messages to the server
    def sendMsgs(self, clientSocket):
        self.textCons.config(state=DISABLED)
        while True:
            message = self.name + ': ' + self.msg
            clientSocket.send(message.encode())
            break
    
    # Function to receive messages from the server
    def receiveMsgs(self, clientSocket):
        while True: 
            try:
                # This code is executed when the server sends a message to the client
                # which is then printed on the client side terminal.
                message = clientSocket.recv(2048).decode()

                if message == "CONN_CLOSED":
                    break
                elif message == "NAME":
                    clientSocket.send(self.name.encode())
                else:
                    # insert messages to text box
                    self.textCons.config(state = NORMAL)
                    self.textCons.insert(END, message+"\n\n")
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
            except:
                print("An error occured!")
                break

        clientSocket.close()
        self.Window.destroy()

    def disable_event(self):
        pass

    def handle_closure(self):
        cl = self.name + ": exit()"
        clientSocket.send(cl.encode())

g = GUI()