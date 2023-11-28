# Archived due to discord integration of its own content moderation.

import os
import re
import discord
from discord.ext import commands
from datetime import datetime

PATH = os.getcwd() + "/archive/filter/"

roleExempt = ["test_bot", "admin"]


class FilterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # try, some messages like epherial ones don't have roles, ignore it if so
        try:
            # see if author is exempt from filtering
            for exempt in roleExempt:
                role = discord.utils.get(message.guild.roles, name=exempt)
                if role in message.author.roles:
                    return
        except:
            return

            # Badwords.txt credit: https://code.google.com/archive/p/badwordslist/downloads
        lines = ""
        with open(PATH + 'badwords.txt') as file1:
            lines = file1.readlines()
        for line in lines:
            line = line.strip()
            if line in message.content.lower():

                markdownMsg = message.content
                markdownMsg = FilterCog.replace_keep_case(
                    line, f"**__{line}__**", markdownMsg)

                print(markdownMsg)

                mod_channel = discord.utils.get(
                    message.guild.text_channels, name="moderator-only")
                embed = discord.Embed(
                    title=f"Filtered Crude Language", color=0xFF0000, timestamp=datetime.now())
                embed.add_field(
                    name="User", value=message.author, inline=False)
                embed.add_field(
                    name="Message", value=markdownMsg, inline=False)
                await message.delete()
                await message.channel.send(f"{message.author.mention} Pwease no bad words :(")
                await mod_channel.send(embed=embed)
                return

    # thank you openstax: https://stackoverflow.com/questions/24893977/whats-the-best-way-to-regex-replace-a-string-in-python-but-keep-its-case
    def replace_keep_case(word, replacement, text):
        def func(match):
            g = match.group()
            if g.islower():
                return replacement.lower()
            if g.istitle():
                return replacement.title()
            if g.isupper():
                return replacement.upper()
            return replacement
        return re.sub(word, func, text, flags=re.I)


async def setup(bot):  # set async function
    await bot.add_cog(FilterCog(bot))  # Use await
