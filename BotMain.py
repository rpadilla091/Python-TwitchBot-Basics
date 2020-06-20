'''
BotMain.py
Roberto Padilla

Twitch Bot example using our twitch_socket test library.
You can use this as a starter to build our own bot,
Please make sure to add your bot credentials and the chat your bot will join inside config.ini.

Note: to obtain an OAuth key from your bot please go to https://twitchapps.com/tmi/ and login with your bot account.
'''
import twitch_socket
import sys #<<< This is just for the pyversion command example, feel free to remove if together with the pyversion command if you desire

#Initialize TwitchBot IRC and Websocket Connection
twitch_obj = twitch_socket.twitch_socket()
socket_obj = twitch_obj.openSocket()
twitch_obj.joinRoom(socket_obj)
twitch_obj.sendMessage(socket_obj, "My new and cool bot has joined the chat!")

#Initialize Websocket messages buffer
readbuffer = ""

while True:
    #Read Websocket and agregate the message to variable temp
    readbuffer = readbuffer.encode('utf-8') + socket_obj.recv(1024)
    temp = str.split(readbuffer.decode('utf-8'), "\n")
    readbuffer = temp.pop()

    #sart reading the actual message received by the socket
    for line in temp:
        print(line) #<< Here you can add a break point and debug the code to see how line actually looks
        if "Bot Go Away" in line:
            #Here we can remove the bot from the chat, you can add any message, text or command to trigger this portion
            socket_obj.send("PART #" + twitch_obj.CHANNEL)
            print("attempted to leave")
        if "PING :tmi.twitch.tv" in line:
            #Here we pretty much let TwitchIRC that we are still alive
            socket_obj.send("PONG :tmi.twitch.tv\r\n")
            print("I just sent a PONG")

        user = twitch_obj.getUser(line) #Chat user who sent the current chat message
        message = twitch_obj.getMessage(line) #Current Chat message
        print(user + " typed :" + message)

        #special command zone, here we can verify if the message contains a predefined command
        #remember that you can pretty much do and run anything when we detect a command
        if "hello!" in message:
            twitch_obj.sendMessage(socket_obj, "Hello Bot!")

        if "pyversion!" in message:
            python_version = sys.version
            twitch_obj.sendMessage(socket_obj, python_version)