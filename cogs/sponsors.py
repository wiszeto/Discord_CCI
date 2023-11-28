import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from discord.ext import tasks


class SponsorCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    sponsors = []

    @app_commands.command(name="sponsors", description="Shoutout all the sponsors in sponsor-universe channel")
    @app_commands.default_permissions(administrator=True)
    async def sponsor_message(self, itx: discord.Interaction):
        #Constellation Partners
        #JPL
        # jpl_embed = discord.Embed(
        #     title="Jet Propulsion Laboratory", 
        #     color=0xFF0000, 
        #     description="NASA JPL supports the CCI’s Cyber to Schools initiative by providing technical oversight, mentorship, SME, and allowing access to their deep resources and network." + "\n\n" +"Learn more about JPL at: https://www.jpl.nasa.gov/",
        #     url = "https://www.jpl.nasa.gov/")
        # jpl_embed.set_image(url="https://media.discordapp.net/attachments/882263327428997120/892579632526807090/final-jpl.png")
        # jpl_embed.set_footer(text="Click the title to learn more")
        # self.sponsors.append(jpl_embed)


        #AWS
        # aws_embed = discord.Embed(
        #     title="Amazon Web Services", 
        #     color=0xFF9900, 
        #     description="AWS provides a highly reliable, scalable, low-cost infrastructure platform in the cloud." + "\n\n" + "Learn more about AWS at: https://aws.amazon.com/",
        #     url = "https://aws.amazon.com/")
        # aws_embed.set_image(url="https://cdn.discordapp.com/attachments/981024250091687946/1019381539617918996/unknown.png")
        # aws_embed.set_footer(text="Click the title to learn more")
        # self.sponsors.append(aws_embed)

        #Foundation For The Future
        # future_embed = discord.Embed(
        #     title="Foundation For The Future", 
        #     color=0xFF5349, 
        #     description="The Foundation for the Future is an education and advocacy non-profit dedicated to advancing the space economy by developing critical infrastructure to enable it, investment tools to finance it, and a workforce to power it." + "\n\n" + "Learn more about Foundation For Future at: https://www.f4f.space/",
        #     url = "https://www.f4f.space/")
        # future_embed.set_image(url="https://media.discordapp.net/attachments/882263327428997120/892584296290856980/final-future-logo.png")
        # future_embed.set_footer(text="Click the title to learn more")
        # self.sponsors.append(future_embed)

        #Splunk
        security_embed = discord.Embed(
            title="Splunk", 
            color=0x0000FF, 
            description="Splunk was founded in 2003 to solve problems in complex digital infrastructures. From the beginning, we've helped organizations explore the vast depths of their data like spelunkers in a cave (hence, 'Splunk')" + "\n\n" + "Learn more about Splunk at: https://www.splunk.com/",
            url = "https://www.splunk.com/")
        security_embed.set_image(url="https://cdn.discordapp.com/attachments/981024250091687946/1105282505994678302/image.png")
        security_embed.set_footer(text="Click the title to learn more")
        self.sponsors.append(security_embed)
        
        ##National Security Space Association
        security_embed = discord.Embed(
            title="National Security Space Association", 
            color=0x0000FF, 
            description="The National Security Space Association is a non-profit support association solely dedicated to the National Security Space enterprise. They foster a holistic, mission-oriented workforce that will shape the face of National Security Space for generations to come." + "\n\n" + "Learn more about National Security Space Association at: https://www.nssaspace.org/",
            url = "https://www.nssaspace.org/")
        security_embed.set_image(url="https://cdn.discordapp.com/attachments/882263327428997120/892584999893741598/final-nssa-logo.png")
        security_embed.set_footer(text="Click the title to learn more")
        self.sponsors.append(security_embed)

        #Space System Command
        # space_embed = discord.Embed(
        #     title="Space System Command", 
        #     color=0xFFD700, 
        #     description="Space Systems Command, headquartered is responsible for developing, acquiring, equipping, fielding, and sustaining lethal and resilient space capabilities for warfighters." + "\n\n" + "Learn more about Space System Command at: https://www.ssc.spaceforce.mil/",
        #     url = "https://www.ssc.spaceforce.mil/")
        # space_embed.set_image(url="https://cdn.discordapp.com/attachments/981024250091687946/1019384314410053662/unknown.png")
        # space_embed.set_footer(text="Click the title to learn more")
        # self.sponsors.append(space_embed)


        #Comet Sponsors
        #Lmntrix
        # lmntrix_embed = discord.Embed(
        #     title="Lmntrix",
        #     color=0x87ceeb, 
        #     description="LMNTRIX is a robust multi-faceted cybersecurity company focused on active defense." + "\n\n" +"Learn more about LMNTRIX at: https://lmntrix.com/",
        #     url = "https://lmntrix.com/")
        # lmntrix_embed.set_image(url="https://cdn.discordapp.com/attachments/882263327428997120/892587806294163466/final-lmntrix.png")
        # lmntrix_embed.set_footer(text="Click the title to learn more")
        # self.sponsors.append(lmntrix_embed)

        #Lockhead Martin
        # lockhead_embed = discord.Embed(
        #     title="Lockhead Martin",
        #     color=0x00008B, 
        #     description="Lockheed Martin is a global security and aerospace company and is principally engaged in the research, design, development, manufacture, integration and sustainment of advanced technology systems, products and services." + "\n\n" + "Learn more about Lockhead Martin at: https://www.lockheedmartin.com/en-us/index.html",
        #     url = "https://www.lockheedmartin.com/en-us/index.html")
        # lockhead_embed.set_image(url="https://cdn.discordapp.com/attachments/981024250091687946/1019400699601227836/unknown.png")
        # lockhead_embed.set_footer(text="Click the title to learn more")
        # self.sponsors.append(lockhead_embed)

        #Planet Sponsors
        #Fortinet
        fortinet_embed = discord.Embed(
            title="Fortinet",
            color=0xFF0000, 
            description="Fortinet empowers its customers with intelligent, seamless protection across the expanding attack surface and the power to take on ever-increasing performance requirements of the borderless network—today and into the future." + "\n\n" + "Learn more about Fortinet at: https://www.fortinet.com/",
            url = "https://www.fortinet.com/")
        fortinet_embed.set_image(url="https://cdn.discordapp.com/attachments/981024250091687946/1019388434822995968/unknown.png")
        fortinet_embed.set_footer(text="Click the title to learn more")
        self.sponsors.append(fortinet_embed)

        await itx.response.send_message(content="Shouted out all the sponsors!", ephemeral=True)
        
        sponsor_channel = discord.utils.get(
            itx.guild.text_channels, name='sponsor-universe')
        for sponsor_embed in self.sponsors:
            await sponsor_channel.send(embed=sponsor_embed)
        

async def setup(bot):  # set async function
    await bot.add_cog(SponsorCog(bot))  # Use await`
