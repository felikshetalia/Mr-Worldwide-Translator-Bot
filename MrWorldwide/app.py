import openai
import discord
from discord.ext import commands
import os

print(discord.__version__)

# openai.api_key = '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'

# language = input("Please type translation language: ")

# audio = open("Dora.m4a", "rb")
# transcribe = openai.Audio.transcribe("whisper-1", audio)

# print("#-----------------------TRANSCRIBED-----------------------#")
# print(transcribe['text'])

# response = openai.Completion.create(
#   model="text-davinci-003",
#   prompt=f"Translate this into {language}:\n" + transcribe['text'],
#   temperature=0.6,
#   max_tokens=1000,
#   top_p=1.0,
#   frequency_penalty=0.0,
#   presence_penalty=0.0
# )

# print("#-----------------------TRANSLATED-----------------------#")
# print(response['choices'][0]['text'])



intents = discord.Intents.default()
intents.message_content = True

# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)
connections = {}

@bot.command()
async def record(ctx):  # If you're using commands.Bot, this will also work.
    voice = ctx.author.voice

    if not voice:
        await ctx.respond("You aren't in a voice channel!")

    vc = await voice.channel.connect()  # Connect to the voice channel the author is in.
    connections.update({ctx.guild.id: vc})  # Updating the cache with the guild and channel.

    vc.start_recording(
        discord.sinks.WaveSink(),  # The sink type to use.
        once_done,  # What to do once done.
        ctx.channel  # The channel to disconnect from.
    )
    await ctx.respond("Started recording!")

async def once_done(sink: discord.sinks, channel: discord.TextChannel, *args):  # Our voice client already passes these in.
    recorded_users = [  # A list of recorded users
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    await sink.vc.disconnect()  # Disconnect from the voice channel.
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]  # List down the files.
    await channel.send(f"finished recording audio for: {', '.join(recorded_users)}.", files=files)  # Send a message with the accumulated files.

@bot.command()
async def stop_recording(ctx):
    if ctx.guild.id in connections:  # Check if the guild is in the cache.
        vc = connections[ctx.guild.id]
        vc.stop_recording()  # Stop recording, and call the callback (once_done).
        del connections[ctx.guild.id]  # Remove the guild from the cache.
        await ctx.delete()  # And delete.
    else:
        await ctx.respond("I am currently not recording here.")  # Respond with this if we aren't recording.

bot.run("MTAwODc0NjQ2Njg0NTY3MTUzOA.GcVlme.dIJnB3Bir03q_CqXKKoX0cNY4jK3s9Jfdy2yws")