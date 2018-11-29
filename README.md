# Python-TwitchBot-Basics
A base structure to start a TwitchBot project on Python 3.5+, including support for chat commands, text-to-speech recognition, timeout, and banned words.

# How to build
run.py has the main logic for user commands, this is the one you need to run. Please be aware that you will need to keep the code running in order to make the bot work on Twitch Chat.

con.py has the connection settings such as Twitch key, user name and Twitch IRC parameters. You need to provide your bot Twitch key, as well as the Twitch username that the bot will be connecting.

tts.py has the text-to-speech logic, this code depends on gTTS library.

commands.py has the stored commands and functions, here you will build your commands logic.

chat_message.py has the chat functions to obtain the message text and the user, as well as whisper message sender.

mod.py has the chat moderation functions, including ban and timeout.

#libraries required
-gTTS (for text-to-speech functionality)
