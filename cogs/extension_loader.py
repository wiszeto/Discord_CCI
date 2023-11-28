import discord
from discord.ext import commands

class ExtLoaderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # nice to have, not really needed since ctrl-c ctrl-v is handy
    # will possibly be useful for the event
    @commands.command(name="reload_ext", description="Reloads specified extension")
    @commands.has_guild_permissions(administrator=True)
    async def reload_ext(self, ctx, ext):
        try:
            await self.bot.reload_extension(ext)
            await ctx.channel.send(f"Reload Finished on EXT: {ext} {ctx.author.mention}")

        except:
            cogs = '```'
            for cog in self.bot.extensions.keys():
                cogs += cog + "\n"
            cogs += '```'
            if ext != "help":
                await ctx.channel.send(f"No EXT: {ext} {ctx.author.mention} \n\nHere is a list of avaliable extensions:\n")
            await ctx.channel.send(cogs)

    @commands.command(name="load_ext", description="Loads new specified extension")
    @commands.has_guild_permissions(administrator=True)
    async def load_ext(self, ctx, ext):
        try:
            await self.bot.load_extension(ext)
            await ctx.channel.send(f"Load Finished on EXT: {ext} {ctx.author.mention}")

        except discord.ext.commands.ExtensionNotFound:
            await ctx.channel.send(f"NO SUCH EXTENSION FOUND: {ext}")
        except discord.ext.commands.ExtensionAlreadyLoaded:
            await ctx.channel.send(f"EXTENSION ALREADY LOADED: {ext}")
        except discord.ext.commands.ExtensionFailed:
            await ctx.channel.send(f"EXTENSION HAS AN ERROR: {ext}")

    @commands.command(name="unload_ext", description="Unoads specified extension")
    @commands.has_guild_permissions(administrator=True)
    async def unload_ext(self, ctx, ext):
        try:
            await self.bot.unload_extension(ext)
            await ctx.channel.send(f"Unload Finished on EXT: {ext} {ctx.author.mention}")

        except:
            cogs = '```'
            for cog in self.bot.extensions.keys():
                cogs += cog + "\n"
            cogs += '```'
            if ext != "help":
                await ctx.channel.send(f"EXTENSION WAS NEVER LOADED: {ext} {ctx.author.mention} \n\nHere is a list of loaded extensions:\n")
            await ctx.channel.send(cogs)


async def setup(bot):  # set async function
    await bot.add_cog(ExtLoaderCog(bot))  # Use await
