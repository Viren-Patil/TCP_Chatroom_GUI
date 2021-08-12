# TCP Chatroom

A decent looking UI generated on top of a TCP Client-Server Chatroom. Developed initially as a part of coursework in college, enhanced as a result of tedious and problematic usage of the chatroom on terminal. It is also possible to generate an executable file for it as you will be reading further.

## Getting Started

Clone/Download the project from the repository. Navigate to the folder containing *client_gui.py* and *server_gui.py* files. Open two terminal windows in the same path. Make sure you run the commands in the order shown below.

Terminal Window 1:
```
> python server_gui.py <port-number>
```
Terminal Window 2:
```
> python client_gui.py <port-number>
```

Make sure that the port numbers used in both the above commands are same. A different port number won't allow the client to get connected to the server. The port number should be entered without the angular brackets. For example:

Terminal Window 1:
```
> python server_gui.py 12000
```
Terminal Window 2:
```
> python client_gui.py 12000
```

Make sure you choose a port number that is free (i.e. not listening) on your system. Use *netstat* command to know which ports are open and can be used.

If you followed all steps properly you should be able to see the chat window as shown at the end of this README.

### Prerequisites

* Python 3.8 or above
* Tkinter v8.6
* **socket** library and **_thread** library (most likely already installed on your system, both Linux and Windows)


### Installing

Steps to install Python 3.8 can be found at [python.org](https://www.python.org/)
Tkinter comes along with Python 3.8 installation.

To check if python has installed properly follow this:
```
>>> python --version
```

To check the version of Tkinter follow:
Open terminal and open python interpreter. Execute the following.
```
>>> import tkinter
>>> tkinter.TkVersion
8.6
```

## Making sure everything is running properly

After you started the server and also ran the client to connect to it, make sure to check the terminal on which server is running. It should show no errors and should show some printed statements telling about the number of people in the chatroom. 
If you can see that you are all set, Cheers! 


## Deployment

* You can deploy the server on a public IP (which is what I would recommend as it is safer than the alternative I'll be listing next)

* Alternatively you can use [ngrok](https://ngrok.com) to do port forwarding.
Create and account and login. Download ngrok. Follow the steps 1 and 2 displayed on the dashboard.
For step 3 execute the following:

Navigate to the installed folder and make sure it has the executable file ngrok in it.
On powershell run:
```
./ngrok tcp 12000
```
On command prompt run:
```
ngrok.exe tcp 12000
```
The port number to be used above should be the one on which you will be running the server on your localhost.
You should see the following after executing the above command:

<img src="snapshots/ngrok.png">


## Built With

* Python
* Tkinter

## Editor used for development

* VSCode

## Acknowledgments

* Icons made by **Vectors Market** from [www.flaticon.com](www.flaticon.com)

## Snapshots of the application in use

