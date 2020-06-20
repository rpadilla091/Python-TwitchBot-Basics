# Python-TwitchBot-Basics
A base structure to start a TwitchBot project on Python 3.5+ with basic text commands, you can use this example as a starter for your own TwitchBot.

# How to build
twitch_socket.py contains our TwitchIRC Chat logic Class with all the needed functions to connect our bot to Twitch, this module uses config.ini for our Bot credentials and name of channel to join. You don't need to modify anything inside this module in order for the bot to work, but feel free to explore it and improve the functionality as this is just a quick example without performance improvements.

BotMain.py is an example of how we can use our twitch_socket module to create our own bot and react to multiple commands.

config.ini is where we add our bot credentials and the name of the channel to join. 

