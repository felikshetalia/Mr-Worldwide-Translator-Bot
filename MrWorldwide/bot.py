import discord
from responses import get_response, join_voice

async def send_message(message, user_message, is_private):
    try:
        response = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_bot():
    TOKEN = 'MTA3OTQwNzMyMjgwNTMyNTkyNA.GVzkuQ.z40fPI0i4f9d2MizKCj06xArSSL8U-29FO29LU'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(msg):
        if msg.author == client.user:
            return
        
        username = str(msg.author)
        user_message = str(msg.content)
        channel = str(msg.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if user_message[0] == '?':
            user_message = user_message[1:]  # [1:] Removes the '?'
            await send_message(msg, user_message, is_private=True)
        elif msg.content.startswith("!join"):
            await join_voice(msg)
        else:
            await send_message(msg, user_message, is_private=False)


    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)

