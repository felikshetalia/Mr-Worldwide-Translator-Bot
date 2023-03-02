import discord
from responses import get_response, join_voice
from discord.ext import commands
import os
import sys

async def send_message(message, user_message, is_private):
    try:
        response = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


async def finished_callback(sink, ctx):
    # Here you can access the recorded files:
    recorded_users = [
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in
             sink.audio_data.items()]
    await ctx.channel.send(f"Finished! Recorded audio for {', '.join(recorded_users)}.", files=files)

def run_bot():
    tok = os.getenv('TOKEN')
    TOKEN = 'uwu'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    bot = commands.Bot(command_prefix='!', intents=intents)
    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        print(f'Token: {tok}')
        for path in sys.path:
            print(path)


    @bot.command()
    async def join(ctx):
        await join_voice(ctx)

    @bot.command()
    async def start_record(ctx):
        await ctx.author.voice.channel.connect()  # Connect to the voice channel of the author
        print(ctx.voice_client)
        ctx.voice_client.start_recording(discord.sinks.MP3Sink(), finished_callback, ctx)  # Start the recording
        await ctx.respond("Recording...")


    @bot.command()
    async def stop_recording(ctx):
        ctx.voice_client.stop_recording()  # Stop the recording, finished_callback will shortly after be called
        await ctx.respond("Stopped!")

    # @bot.command()
    # async def rec(ctx):
    #     ctx.voice_client.record(lambda e: print(f"Exception: {e}"))
    #
    # @bot.command()
    # async def stop(ctx: commands.Context):
    #     if not ctx.voice_client.is_recording():
    #         return
    #     await ctx.send(f'Stopping the Recording')
    #
    #     wav_bytes = await ctx.voice_client.stop_record()
    #
    #     name = str(random.randint(000000, 999999))
    #     with open(f'{name}.wav', 'wb') as f:
    #         f.write(wav_bytes)
    #     await ctx.voice_client.disconnect()

    # @bot.command()
    # async def on_message(ctx, args):
    #     if ctx.author == bot.user:
    #         return
    #
    #     username = str(ctx.author)
    #     user_message = str(ctx.content)
    #     channel = str(ctx.channel)
    #
    #     print(f"{username} said: '{user_message}' ({channel})")
    #
    #     if user_message[0] == '?':
    #         user_message = user_message[1:]  # [1:] Removes the '?'
    #         await send_message(ctx, user_message, is_private=True)
    #
    #     elif ctx.content.startswith("!join"):
    #         await join_voice(ctx)

        # elif ctx.content.startswith("!start_recording"):
        #     # print("elif start recording")
        #     print('in start_recording')
        #     # await ctx.author.voice.channel.connect()
        #     ctx.voice_client.start_recording(discord.sinks.MP3Sink(), finished_callback, ctx)  # Start the recording
        #     await ctx.respond("Recording...")
        #
        # elif ctx.content.startswith("!stop_recording"):
        #     # await ctx.author.voice.channel.disconnect()
        #     ctx.voice_client.stop_recording()  # Stop the recording, finished_callback will shortly after be called
        #     # channel = client.get_channel(1007991681121005600)
        #     # await channel.send('recorded!')
        #     await ctx.respond("Stopped!")

        # else:
        #     await send_message(ctx, user_message, is_private=False)

    # @client.event
    # async def start_recording(ctx):
    #     print('in start_recording')
    #     await ctx.author.voice.channel.connect()
    #     ctx.voice_client.start_recording(discord.sinks.MP3Sink(), finished_callback, ctx)  # Start the recording
    #     await ctx.respond("Recording...")
    #
    #
    #
    # @client.event
    # async def stop_recording(ctx):
    #     # await ctx.author.voice.channel.disconnect()
    #     ctx.voice_client.stop_recording()  # Stop the recording, finished_callback will shortly after be called
    #     # channel = client.get_channel(1007991681121005600)
    #     # await channel.send('recorded!')
    #     await ctx.respond("Stopped!")






        # @client.event
    # async def on_voice_state_update(member, before, after):
    #     if before.channel is None and after.channel is not None:  # User joined voice channel
    #         voice_channel = after.channel
    #         await voice_channel.connect()
    #
    #     elif after.channel is None and before.channel is not None:  # User left voice channel
    #         voice_client = client.voice_clients[0]
    #         await voice_client.disconnect()
    #
    # @client.event
    # async def on_voice_state_update(member, before, after):
    #     if before.channel is None and after.channel is not None:  # User joined voice channel
    #         voice_channel = after.channel
    #         await voice_channel.connect()
    #
    #     elif after.channel is None and before.channel is not None:  # User left voice channel
    #         voice_client = client.voice_clients[0]
    #         await voice_client.disconnect()
    #
    #     elif before.self_mute != after.self_mute or before.self_deaf != after.self_deaf:  # User muted or deafened themselves
    #         voice_client = client.voice_clients[0]
    #         if voice_client.is_connected():
    #             await voice_client.move_to(None)  # Disconnect and reconnect to update user's mute/deaf status
    #
    # @client.event
    # async def on_voice_state_update(member, before, after):
    #     if before.channel is None and after.channel is not None:  # User joined voice channel
    #         voice_channel = after.channel
    #         await voice_channel.connect()
    #
    #     elif after.channel is None and before.channel is not None:  # User left voice channel
    #         voice_client = client.voice_clients[0]
    #         await voice_client.disconnect()
    #
    #     elif before.self_mute != after.self_mute or before.self_deaf != after.self_deaf:  # User muted or deafened themselves
    #         voice_client = client.voice_clients[0]
    #         if voice_client.is_connected():
    #             await voice_client.move_to(None)  # Disconnect and reconnect to update user's mute/deaf status
    #
    #     elif before.channel != after.channel:  # User switched voice channels
    #         voice_client = client.voice_clients[0]
    #         if voice_client.is_connected():
    #             await voice_client.move_to(after.channel)  # Move to the new voice channel
    # # Remember to run your bot with your personal TOKEN
    bot.run(TOKEN)

