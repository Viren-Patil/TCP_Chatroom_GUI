
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

chatParticipants = []

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
        # typing the message
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
        self.emojiBtnImg = PhotoImage(file="emojis/smiling.png")
        # to show chat window
        self.Window.deiconify()
        self.Window.protocol("WM_DELETE_WINDOW", self.handle_closure)
        self.Window.title("Chatroom")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 600,
                              height = 650,
                              bg = "#042F2A")

        self.header = Frame(self.Window, bg="#042F2A")
        self.header.place(relwidth=1)
        self.labelHead = Label(self.header,
                            bg = "#042F2A",
                            fg = "white",
                            text = self.name ,
                            font = "Helvetica 14 bold",
                            width = 20,
                            pady = 5)
        self.labelHead.pack(side=LEFT)
        
        self.participants = Button(self.header,
                                image = self.participantsImg,
                                width = 45,
                                bg = "#042F2A",
                                activebackground = "#042F2A",
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
                             font = "Helvetica 16",
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
                               
        self.entryFrame = Frame(self.labelBottom, bg="#042F2A")
        self.entryFrame.place(relwidth = 0.74,
                            relheight = 0.07,
                            rely = 0.008,
                            relx = 0.011)

        self.entryMsg = Entry(self.entryFrame,
                              bg = "#042F2A",
                              fg = "white",
                              font = "Helvetica 14",
                              borderwidth=0,
                              insertbackground="white")
         
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.957,
                            relheight = 1,
                            rely = 0.008,
                            relx = 0.021)
         
        self.entryMsg.focus()
         
        self.entryMsg.bind('<Return>', self.keyPress)

        self.emojiBtn = Button(self.labelBottom,
                                image = self.emojiBtnImg,
                                bg = "#042F2A",
                                activebackground = "#042F2A",
                                borderwidth=0,
                                command = lambda : self.emojiSelector())
         
        self.emojiBtn.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.07,
                             relwidth = 0.1)

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                image = self.sendImg,
                                bg = "#042F2A",
                                activebackground = "#042F2A",
                                borderwidth=0,
                                command = lambda : self.sendButton(self.entryMsg.get()))
         
        self.buttonMsg.place(relx = 0.89,
                             rely = 0.008,
                             relheight = 0.07,
                             relwidth = 0.1)
         
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

        for k in chatParticipants:
            if k == self.name:
                k = "You"
            btn = Label(mainframe2, text=k, font="Helvetica 13 bold", bg="#042F2A", fg="white", width=20, pady=10)
            btn.pack()

    def emojiSelector(self):
        es = Toplevel()
        es.title("Emojis")
        es.geometry("239x175")
        es.resizable(width = False,height = False)

        mainframe = Frame(es)
        mainframe.pack(fill=BOTH, expand=1)

        self.ej1Img = PhotoImage(file="emojis/smiling.png")
        ej1 = Button(mainframe, image = self.ej1Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F604"))
        ej1.grid(row=0, column=0)
        
        self.ej2Img = PhotoImage(file="emojis/sad.png")
        ej2 = Button(mainframe, image = self.ej2Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F614"))
        ej2.grid(row=0, column=1)

        self.ej3Img = PhotoImage(file="emojis/angry.png")
        ej3 = Button(mainframe, image = self.ej3Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F620"))
        ej3.grid(row=0, column=2)

        self.ej4Img = PhotoImage(file="emojis/cake.png")
        ej4 = Button(mainframe, image = self.ej4Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F382"))
        ej4.grid(row=0, column=3)

        self.ej5Img = PhotoImage(file="emojis/cat.png")
        ej5 = Button(mainframe, image = self.ej5Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F63A"))
        ej5.grid(row=0, column=4)

        self.ej6Img = PhotoImage(file="emojis/clap.png")
        ej6 = Button(mainframe, image = self.ej6Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F44F"))
        ej6.grid(row=0, column=5)

        self.ej7Img = PhotoImage(file="emojis/confused.png")
        ej7 = Button(mainframe, image = self.ej7Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F610"))
        ej7.grid(row=0, column=6)

        self.ej8Img = PhotoImage(file="emojis/cool.png")
        ej8 = Button(mainframe, image = self.ej8Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F60E"))
        ej8.grid(row=1, column=0)

        self.ej9Img = PhotoImage(file="emojis/crying.png")
        ej9 = Button(mainframe, image = self.ej9Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F622"))
        ej9.grid(row=1, column=1)

        self.ej10Img = PhotoImage(file="emojis/dead.png")
        ej10 = Button(mainframe, image = self.ej10Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F635"))
        ej10.grid(row=1, column=2)

        self.ej11Img = PhotoImage(file="emojis/dislike.png")
        ej11 = Button(mainframe, image = self.ej11Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F44E"))
        ej11.grid(row=1, column=3)

        self.ej12Img = PhotoImage(file="emojis/dog.png")
        ej12 = Button(mainframe, image = self.ej12Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F436"))
        ej12.grid(row=1, column=4)

        self.ej13Img = PhotoImage(file="emojis/fire.png")
        ej13 = Button(mainframe, image = self.ej13Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F525"))
        ej13.grid(row=1, column=5)

        self.ej14Img = PhotoImage(file="emojis/ghost.png")
        ej14 = Button(mainframe, image = self.ej14Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F47B"))
        ej14.grid(row=1, column=6)

        self.ej15Img = PhotoImage(file="emojis/greed.png")
        ej15 = Button(mainframe, image = self.ej15Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F911"))
        ej15.grid(row=2, column=0)

        self.ej16Img = PhotoImage(file="emojis/hands.png")
        ej16 = Button(mainframe, image = self.ej16Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F64F"))
        ej16.grid(row=2, column=1)

        self.ej17Img = PhotoImage(file="emojis/happy_teeth.png")
        ej17 = Button(mainframe, image = self.ej17Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F601"))
        ej17.grid(row=2, column=2)

        self.ej18Img = PhotoImage(file="emojis/happy.png")
        ej18 = Button(mainframe, image = self.ej18Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F642"))
        ej18.grid(row=2, column=3)

        self.ej19Img = PhotoImage(file="emojis/heart.png")
        ej19 = Button(mainframe, image = self.ej19Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F499"))
        ej19.grid(row=2, column=4)

        self.ej20Img = PhotoImage(file="emojis/in-love.png")
        ej20 = Button(mainframe, image = self.ej20Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F60D"))
        ej20.grid(row=2, column=5)

        self.ej21Img = PhotoImage(file="emojis/kiss.png")
        ej21 = Button(mainframe, image = self.ej21Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F618"))
        ej21.grid(row=2, column=6)

        self.ej22Img = PhotoImage(file="emojis/laughing.png")
        ej22 = Button(mainframe, image = self.ej22Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F602"))
        ej22.grid(row=3, column=0)

        self.ej23Img = PhotoImage(file="emojis/laughing2.png")
        ej23 = Button(mainframe, image = self.ej23Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F606"))
        ej23.grid(row=3, column=1)

        self.ej24Img = PhotoImage(file="emojis/like.png")
        ej24 = Button(mainframe, image = self.ej24Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F44D"))
        ej24.grid(row=3, column=2)

        self.ej25Img = PhotoImage(file="emojis/nerd.png")
        ej25 = Button(mainframe, image = self.ej25Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F913"))
        ej25.grid(row=3, column=3)

        self.ej26Img = PhotoImage(file="emojis/one-hundred.png")
        ej26 = Button(mainframe, image = self.ej26Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F4AF"))
        ej26.grid(row=3, column=4)

        self.ej27Img = PhotoImage(file="emojis/otter.png")
        ej27 = Button(mainframe, image = self.ej27Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F9A6"))
        ej27.grid(row=3, column=5)

        self.ej28Img = PhotoImage(file="emojis/shocked.png")
        ej28 = Button(mainframe, image = self.ej28Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F632"))
        ej28.grid(row=3, column=6)

        self.ej29Img = PhotoImage(file="emojis/sick.png")
        ej29 = Button(mainframe, image = self.ej29Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F912"))
        ej29.grid(row=4, column=0)

        self.ej30Img = PhotoImage(file="emojis/skull-and-bones.png")
        ej30 = Button(mainframe, image = self.ej30Img, borderwidth=0, command=lambda: self.addEmoji(u"\U00002620"))
        ej30.grid(row=4, column=1)

        self.ej31Img = PhotoImage(file="emojis/surprised.png")
        ej31 = Button(mainframe, image = self.ej31Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F62F"))
        ej31.grid(row=4, column=2)

        self.ej32Img = PhotoImage(file="emojis/teeth.png")
        ej32 = Button(mainframe, image = self.ej32Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F62C"))
        ej32.grid(row=4, column=3)

        self.ej33Img = PhotoImage(file="emojis/tongue.png")
        ej33 = Button(mainframe, image = self.ej33Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F61B"))
        ej33.grid(row=4, column=4)

        self.ej34Img = PhotoImage(file="emojis/very_happy.png")
        ej34 = Button(mainframe, image = self.ej34Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F603"))
        ej34.grid(row=4, column=5)

        self.ej35Img = PhotoImage(file="emojis/wink.png")
        ej35 = Button(mainframe, image = self.ej35Img, borderwidth=0, command=lambda: self.addEmoji(u"\U0001F609"))
        ej35.grid(row=4, column=6)

    def addEmoji(self, unicode):
        self.entryMsg.insert(END, unicode)

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
            # message = self.name + ': ' + self.msg + "$NORM"
            message = self.name + ': ' + self.msg
            clientSocket.send(message.encode())
            break
    
    # Function to receive messages from the server
    def receiveMsgs(self, clientSocket):
        while True: 
            try:
                # This code is executed when the server sends a message to the client
                message = clientSocket.recv(2048).decode()

                if message == "CONN_CLOSED":
                    break

                elif message == "NAME":
                    clientSocket.send(self.name.encode())
                    continue

                elif message == "CONN_SUCCESS":
                    message = "Connection Successful!"

                elif "$PTLUPDT" in message:
                    l = message.split('$')[0].split(',')
                    for i in l:
                        chatParticipants.append(i)
                    continue

                elif "$PJOIN" in message:
                    name = message.split("'")[1]
                    if name not in chatParticipants:
                        chatParticipants.append(name)
                    message = message.split('$')[0]

                elif "$PLEAVE" in message:
                    name = message.split("'")[1]
                    if name in chatParticipants:
                        chatParticipants.remove(name)
                    message = message.split('$')[0]

                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, message+"\n\n")
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)


            except:
                print("An error occured! - ", sys.exc_info())
                break

        clientSocket.close()
        self.Window.destroy()

    def disable_event(self):
        pass

    def handle_closure(self):
        cl = self.name + ": exit()"
        clientSocket.send(cl.encode())

g = GUI()