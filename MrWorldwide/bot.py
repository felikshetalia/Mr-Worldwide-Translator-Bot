import discord
from responses import get_response, join_voice
import os

async def send_message(message, user_message, is_private):
    try:
        response = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_bot():
    TOKEN =
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

    @client.event
    async def on_voice_state_update(member, before, after):
        if before.channel is None and after.channel is not None:  # User joined voice channel
            voice_channel = after.channel
            await voice_channel.connect()

        elif after.channel is None and before.channel is not None:  # User left voice channel
            voice_client = client.voice_clients[0]
            await voice_client.disconnect()

    @client.event
    async def on_voice_state_update(member, before, after):
        if before.channel is None and after.channel is not None:  # User joined voice channel
            voice_channel = after.channel
            await voice_channel.connect()

        elif after.channel is None and before.channel is not None:  # User left voice channel
            voice_client = client.voice_clients[0]
            await voice_client.disconnect()

        elif before.self_mute != after.self_mute or before.self_deaf != after.self_deaf:  # User muted or deafened themselves
            voice_client = client.voice_clients[0]
            if voice_client.is_connected():
                await voice_client.move_to(None)  # Disconnect and reconnect to update user's mute/deaf status

    @client.event
    async def on_voice_state_update(member, before, after):
        if before.channel is None and after.channel is not None:  # User joined voice channel
            voice_channel = after.channel
            await voice_channel.connect()

        elif after.channel is None and before.channel is not None:  # User left voice channel
            voice_client = client.voice_clients[0]
            await voice_client.disconnect()

        elif before.self_mute != after.self_mute or before.self_deaf != after.self_deaf:  # User muted or deafened themselves
            voice_client = client.voice_clients[0]
            if voice_client.is_connected():
                await voice_client.move_to(None)  # Disconnect and reconnect to update user's mute/deaf status

        elif before.channel != after.channel:  # User switched voice channels
            voice_client = client.voice_clients[0]
            if voice_client.is_connected():
                await voice_client.move_to(after.channel)  # Move to the new voice channel
    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)

