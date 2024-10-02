
import traceback

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.app_commands import Group

import data
import sql
from dotenv import load_dotenv
import os

load_dotenv()

class Survey(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    channelGroup = Group(
        name='channel', description='Configure Channel Forwarder')
    close = Group(name='close', description='Closes a position or an order')
    add = Group(name='add', description='Add')

    @commands.Cog.listener()
    async def on_ready(self):
        print('Survey cog loaded.')

    @commands.command()
    @has_permissions(admi   nistrator=True)
    async def sync(self, ctx: discord.ext.commands.Context) -> None:
        try:
            fmt = await ctx.bot.tree.sync(guild=ctx.guild)

            await ctx.send(
                f"Synced {len(fmt)} commands to the current guild."
            )
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        return

    @channelGroup.command(name="add", description="Adds a channel to forwarder list.")
    @app_commands.describe(tgchannelid='The telegram channel you want messages to be forwarded to.')
    @app_commands.describe(channel='The channel you want messages to be forwarded from.')
    @app_commands.describe(header='The message header')
    @app_commands.describe(access='The only member who gets his message forwarded')
    async def addch(self, interaction: discord.Interaction, tgchannelid: int, header: str, channel: discord.TextChannel, access: discord.Member = None):
        try:
            if interaction.user.guild_permissions.administrator:
                if access is None:
                    result = sql.addChannel(
                        channel.id, tgchannelid, header)
                else:
                    result = sql.addChannel(
                        channel.id, tgchannelid, header, access.id)
                if result:
                    embed = discord.Embed(title=f"Success", description="Added channel to message forwarder list.",
                                          color=0x1eeb0f)
                    await interaction.response.send_message(embed=embed)
                else:
                    raise Exception
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            embed = discord.Embed(
                title=f"Error", description="Unknown Error", color=0xfb3737)
            await interaction.response.send_message(embed=embed)

    @channelGroup.command(name="remove", description="Removes a channel from forwarder list.")
    @app_commands.describe(id='The unique id to be removed.')
    async def remch(self, interaction: discord.Interaction, id: int):
        try:
            if interaction.user.guild_permissions.administrator:
                result = sql.removeChannel(id)
                if result:
                    embed = discord.Embed(title=f"Success", description="Removed a channel from message forwarder list.",
                                          color=0x1eeb0f)
                    await interaction.response.send_message(embed=embed)
                else:
                    raise Exception
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            embed = discord.Embed(
                title=f"Error", description="Unknown Error", color=0xfb3737)
            await interaction.response.send_message(embed=embed)

    @channelGroup.command(name="list", description="Lists all channels")
    async def list(self, interaction: discord.Interaction):
        try:
            if interaction.user.guild_permissions.administrator:
                result = sql.getAllForwards()
                if result:
                    embed = discord.Embed(title=f"Forwarder:", description=f"**ID** **Dis Channel** **TG Chat** **Header**\n{data.format()}",
                                          color=0x1eeb0f)
                    await interaction.response.send_message(embed=embed)
                elif result is None or len(result) == 0:
                    embed = discord.Embed(title=f"Forwarder:", description=f"**ID** **Dis Channel** **TG Chat** **Header**\n{data.format()}",
                                          color=0x1eeb0f)
                    await interaction.response.send_message(embed=embed)
                else:
                    raise Exception
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            embed = discord.Embed(
                title=f"Error", description="Unknown Error", color=0xfb3737)
            await interaction.response.send_message(embed=embed)




async def setup(bot):
    await bot.add_cog(Survey(bot), guilds=[discord.Object(id=os.getenv("DISCORD_GUILD_ID")),])


def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False
