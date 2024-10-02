from dotenv import load_dotenv
import os
import asyncio
import traceback
from discord.ext import tasks, commands
import data
import sql
import telegram
import discord
from discord.ext import commands
import re

load_dotenv(".env")
token = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
telToken = os.getenv("TELEGRAM_TOKEN")

disBot = commands.Bot(command_prefix='.', intents=intents)
bot: telegram.Bot

star_pattern = re.compile(r'(\*{1,2})')


@tasks.loop(minutes=5)
async def reconnect():
    try:
        if not sql.sqlData.connection.is_connected():
            sql.connect()
    except Exception as e:
        print(e)
        print(traceback.format_exc())


def format_str(string):
    import re

    special_chars = r'_`'

    pattern = r'([{}])'.format(re.escape(special_chars))

    string = re.sub(pattern, r'\\\1', string)

    tokens = star_pattern.split(string)

    star_pos = {'*': [None, '_'], '**': [None, '*']}

    for idx, token in enumerate(tokens):
        if token in star_pos:
            if star_pos[token][0] is None:
                star_pos[token][0] = idx
            else:
                tokens[star_pos[token][0]] = tokens[idx] = star_pos[token][1]
                star_pos[token][0] = None

    if star_pos['*'][0] is not None:
        tokens[star_pos['*'][0]] = r'\*'

    return ''.join(tokens).replace('[', '').replace(']', '')


async def load():
    await disBot.load_extension("cogstuff")


@disBot.event
async def on_ready():
    print(f'We have logged in as {disBot.user}')
    job.start()


@tasks.loop(hours=1)
async def job():
    try:
        sql.refresh()
    except Exception as e:
        print(e)
        print(traceback.format_exc())


@disBot.event
async def on_message(message: discord.Message):
    try:
        dot = list(zip(*data.forwards))
        # if message.channel.id in disChannelID and message.author.id != bot.id or message.author.get_role(995795374486859826).name == "TA" and message.content.startswith("*") and message.channel.category.id == 993221007965945917 and message.author.id != bot.id:
        if len(dot) == 5 and any(i == int(message.channel.id) for i in [int(j) for j in dot[1]]):
            indexo = dot[1].index(str(message.channel.id))
            ctx = await disBot.get_context(message)
            if dot[4][indexo] is None or dot[4][indexo] == str(message.author.id):
                if message.content != "":
                    try:
                        await bot.sendMessage(text=f"*{data.header(dot[3][indexo], message.id, dot[2][indexo])}*\n{format_str(message.clean_content)}",
                                              chat_id=dot[2][indexo],
                                              parse_mode=telegram.constants.ParseMode.MARKDOWN)
                    except telegram.error.BadRequest:
                        print(
                            f"Chat id not found! Please check again with chat id: {dot[2][indexo]}")
                elif len(message.embeds) == 0:
                    await bot.sendMessage(text=f"*{data.header(dot[3][indexo], message.id, dot[2][indexo])}*", chat_id=dot[2][indexo],
                                          parse_mode=telegram.constants.ParseMode.MARKDOWN, )

                if len(message.embeds) != 0:
                    embed = message.embeds[0]
                    if embed.title is None:
                        embed.title = ""
                    if embed.description != "" or embed.title != "":
                        await bot.sendMessage(
                            text=f"*{data.header(dot[3][indexo], message.id, dot[2][indexo])}*\n*{embed.title}*\n{format_str(await discord.ext.commands.clean_content().convert(ctx, embed.description))}",
                            chat_id=dot[2][indexo],
                            parse_mode=telegram.constants.ParseMode.MARKDOWN)
                        if embed.image.url is not None:
                            await bot.send_photo(chat_id=dot[2][indexo], photo=embed.image.url)

                    else:
                        await bot.sendMessage(text=f"*{data.header(dot[3][indexo], message.id, dot[2][indexo])}*\n*{embed.title}*", chat_id=dot[2][indexo],
                                              parse_mode=telegram.constants.ParseMode.MARKDOWN, )
                for file in message.attachments:
                    print(file.url)
                    await bot.send_photo(chat_id=dot[2][indexo], photo=file.url)
                data.last_message[dot[2][indexo]] = dot[3][indexo]
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print(data.forwards)
    await disBot.process_commands(message)


async def main():
    sql.connect()
    await load()
    await disBot.start(token)

if __name__ == '__main__':

    bot = telegram.Bot(telToken)
    loop = asyncio.run(main())
