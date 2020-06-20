'''
twitch_socket.py
Roberto Padilla
This Class contains a set of Functions to connect to Twitch IRC Chat
You could do this on separate python files in order to have a better organized set of Functions,
but on this way is easier to manage your import on your main bot python script.
'''
import socket
import configparser
import datetime

class twitch_socket:

    def __init__(self):
        '''
        Variables to initialize:
        -config = this object handles the configuration values stored on our .ini file
        -HOST,PORT,PASS,IDENT,CHANNEL = this variables are pretty much an instance from the
                                        .ini configuration file, but this will be easier to
                                        read and call, but you can call the values directly
                                        from the configuration file with:
                                            config[section][value name] << returns a string
        '''
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.HOST = config['TWITCH']['Host']
        self.PORT = int(config['TWITCH']['Port'])
        self.PASS = config['TWITCH']['Pass']
        self.IDENT = config['TWITCH']['Ident']
        self.CHANNEL = config['TWITCH']['Channel']

    def openSocket(self):
        '''
        openSocket :: Return tw_skt = twitch IRC login commands
        Here we prepare our commands to login to Twitch IRC by sending our Bot Username & Bot Password as well as our channel to join.
        > PASS = Here we send our OAuth key from our Bot
        > NICK = Here we send our Bot Username
        > JOIN = Here we define the channel that we want our Bot to join
        '''
        tw_skt = socket.socket()
        tw_skt.connect((self.HOST, self.PORT))
        tw_skt.sendall(b"PASS " + self.PASS.encode('utf-8') + b"\r\n") #b'PASS oauth:*************************\r\n'
        tw_skt.sendall(b"NICK " + self.IDENT.encode('utf-8') + b"\r\n") #b'NICK bot_twitchusername\r\n'
        tw_skt.sendall(b"JOIN #" + self.CHANNEL.encode('utf-8') + b"\r\n") #b'PASSiuhihg kjnfkjn userchat_twitchusername\r\n'
        tw_skt.sendall(b":" + self.IDENT.encode('utf-8') + b"!" + self.IDENT.encode('utf-8') + b"@" + self.IDENT.encode('utf-8') + b".tmi.twitch.tv JOIN #" + self.CHANNEL.encode('utf-8'))
        print("Parameters sent to TwitchIRC >> BotName: " + self.PASS + " // Joining Channel: " + self.CHANNELs)
        return tw_skt

    def sendMessage(self, skt, message):
        '''
        sendMessage
            -> skt = Websocket object
            -> message = string message to push to chat
        We use this function to push any message to our current TwitchIRC connection with our Bot
        > PRIVMSG = Push message to connected chat

        Printed message example
            -> [2020-06-20 02:52:04] Bot Message Sent: TwitchBot Test...
        '''
        messageTemp = "PRIVMSG #" + self.CHANNEL + " :" + message
        skt.sendall(messageTemp.encode('utf-8') + b"\r\n")
        print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] Bot Message Sent: " + messageTemp)

    '''
    Initialization functions
    '''

    def joinRoom(self, s):
        '''
        joinRoom
            -> s = Websocket object
        This function uses our Websocket object with Login Commands to join to TwitchIRC.
        We try to Login into TwitchIRC inside a loop until we success with our logon.
        '''
        readbuffer = ""
        Loading = True
        while Loading:
            readbuffer = bytes(readbuffer, 'utf-8') + s.recv(1024)
            temp = str.split(readbuffer.decode('utf-8'), "\n")
            readbuffer = temp.pop()

            for line in temp:
                print(line + "___--___")
                Loading = self.loadingComplete(line)

        self.sendMessage(s, "Successfully joined chat")

    def loadingComplete(self, line):
        '''
        loadingComplete :: Return True/False
            -> line = line of string
        Here we verify that we receive a Connection Sucessfull message from TwitchIRC.
        '''
        if ("End of /NAMES list" + line):
            return False
        else:
            return True

    '''
    Chat Reading Functions
    '''

    def getUser(self, line):
        '''
        getUser :: Return user = Chat Message Username
            -> line = line of string comming from Websocket
        This function will return the current chat user that sent a message
        example of line is :username!username@username.tmi.twitch.tv PRIVMSG #username :Message
        '''
        separate = line.split(":", 2)  # the 2 will split this into 3 parts; 2 slices separate the parts
        user = separate[1].split("!", 1)[0]  # 0 preceeds the first colon or exclamation mark
        return user

    def getMessage(self, line):
        '''
        getMessage :: Return message = Chat Message
            -> line = line of string comming from Websocket
        example of line is :username!username@username.tmi.twitch.tv PRIVMSG #username :Message
        '''
        separate = line.split(":", 2)
        try:
            message = separate[2]
        except IndexError:
            message = 'null'
        return message