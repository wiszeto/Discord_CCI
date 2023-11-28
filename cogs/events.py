import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from discord.ext import tasks


class EventCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.updates_events.start()
        self.announcing_events.start()

    events = []

    @app_commands.command(name="create_events", description="Create the events scheduled in the CCI website")
    @app_commands.default_permissions(administrator=True)
    async def create_events(self, itx: discord.Interaction):
        #test event
        # test = await itx.guild.create_scheduled_event(
        #     name="Test",
        #     description="Test",
        #     start_time = datetime.now().astimezone() + timedelta(minutes=5),
        #     end_time = datetime.now().astimezone() + timedelta(minutes=7),
        #     location="https://calpoly.zoom.us/webinar/register/WN_j9_IJmc2Qiafm4uNPeBvjQ"
        # )
        # self.events.append(test)
        opening_zoom = "https://calpoly.zoom.us/webinar/register/WN_sgte1c2KQrKFkknF8l-gpw"
        closing_zoom ="https://calpoly.zoom.us/webinar/register/WN_0RekaUCFTrG3ZfhWzcmugw"
        twitch="https://www.twitch.tv/calpolycci"

        #October 7
        """Welcome/ Introductions"""
        start = datetime(2023, 5, 12, 17, 0, 0, 0)
        end = datetime(2023, 5, 12, 17, 45, 0, 0)
        introduction = await itx.guild.create_scheduled_event(
            name="Weclome - Bill Britton",
            description="Welcome to SGC by Bill Britton",
            start_time = start.astimezone(),
            end_time = end.astimezone(),
            location=opening_zoom
        )
        self.events.append(introduction)

        """Welcome Bill """
        start = datetime(2023, 5, 12, 17, 5, 0, 0)
        end = datetime(2023, 5, 12, 17, 5, 5, 0)
        welc_bill = await itx.guild.create_scheduled_event(
            name="Guest Speakers/Presentations",
            description="Come to see CCI's guest speakers and presentation",
            start_time=start.astimezone(),
            end_time=end.astimezone(),
            location=opening_zoom
        )
        self.events.append(welc_bill)

        """Henery_challenge """
        start = datetime(2023, 5, 12, 17, 5, 5, 0)
        end = datetime(2023, 5, 12, 17, 5, 15, 0)
        h_challenge = await itx.guild.create_scheduled_event(
            name="Henery Challenge",
            description="Come see SCG Challenge presented by SGC Challenge - Henry Danielson ",
            start_time=start.astimezone(),
            end_time=end.astimezone(),
            location=opening_zoom
        )
        self.events.append(h_challenge)

        """Opening speaker - Lauren Williams, White House ONCD"""
        start = datetime(2023, 5, 12, 17, 5, 15, 0)
        end = datetime(2023, 5, 12, 17, 5, 25, 0)
        speakers_event = await itx.guild.create_scheduled_event(
            name="Opening speaker - Lauren Williams, White House ONCD",
            description="Come see Lauren Williams",
            start_time=start.astimezone(),
            end_time=end.astimezone(),
            location=opening_zoom
        )
        self.events.append(speakers_event)

        """Competition Logistics and Closing"""
        start = datetime(2023, 5, 12, 17, 25, 0, 0)
        end = datetime(2023, 5, 12, 17, 35, 0, 0)
        logistics = await itx.guild.create_scheduled_event(
            name="Competition Logistics and Closing",
            description="Come to Competition Logistics and Closing",
            start_time=start.astimezone(),
            end_time=end.astimezone(),
            location=opening_zoom
        )
        self.events.append(logistics)

        # await itx.response.send_message(content="Schedule Events Created", ephemeral=True)

        """Q&A"""
        start = datetime(2023, 5, 12, 17, 35, 0, 0)
        end = datetime(2023, 5, 12, 17, 40, 0, 0)
        QA = await itx.guild.create_scheduled_event(
            name="Questions - Breathing Room ",
            description="Come to Q&A",
            start_time=start.astimezone(),
            end_time=end.astimezone(),
            location=opening_zoom
        )
        self.events.append(QA)

        #October 8
        """Twitch Broadcast"""
        start = datetime(2023, 5, 13, 9, 0, 0, 0)
        # end = datetime(2023, 5, 13, 16, 16, 0, 0)
        twitch = await itx.guild.create_scheduled_event(
            name="Streaming on Twitch",
            description="Come to see our competition on Twitch",
            start_time=start.astimezone(),
            # end_time=end.astimezone(),
            location=twitch
        )
        self.events.append(twitch)

        """Opening Remarks"""
        start = datetime(2023, 5, 13, 9, 10, 0, 0)
        end = datetime(2023, 5, 13, 9, 15, 0, 0)
        opening_remarks = await itx.guild.create_scheduled_event(
            name="Opening Remarks/Competition Kick-Off",
            description="Come to competition kick-off",
            start_time=start.astimezone(),
            end_time=end.astimezone(),
            location=opening_zoom
        )
        self.events.append(opening_remarks)

        """Competition Begins"""
        start = datetime(2023, 5, 13, 9, 15, 0, 0)
        end = datetime(2023, 5, 13, 16, 15, 0, 0)
        competition_begin = await itx.guild.create_scheduled_event(
            name="Competition Begins",
            description="Competitors start hacking away",
            start_time=start.astimezone(),
            end_time=end.astimezone(),
            location="Here on Discord"
        )
        self.events.append(competition_begin)

        """Scoring"""
        start = datetime(2023, 5, 13, 16, 15, 0, 0)
        end = datetime(2023, 5, 13, 17, 0, 0, 0)
        score = await itx.guild.create_scheduled_event(
            name="Scoring",
            description="Tallying up the socres",
            start_time=start.astimezone(),
            end_time=end.astimezone(),
        )
        self.events.append(competition_begin)


        """Closing Ceremony"""
        start = datetime(2023, 5, 13, 17, 0, 0, 0)
        end = datetime(2023, 5, 13, 17, 30, 0, 0)
        closing = await itx.guild.create_scheduled_event(
            name="Closing Ceremony",
            description="Come see the Closing Ceremony",
            start_time=start.astimezone(),
            end_time=end.astimezone(),
            location=closing_zoom
        )
        self.events.append(closing)


        """Guest Presentation"""
        start = datetime(2023, 5, 13, 17, 5, 0, 0)
        end = datetime(2023, 5, 13, 17, 10, 0, 0)
        closing_guest = await itx.guild.create_scheduled_event(
            name="Guest Presentation",
            description="Come see the Guest Presentations",
            start_time=start.astimezone(),
            end_time=end.astimezone(),
            location=closing_zoom
        )
        self.events.append(closing_guest)


        """Winner Announced"""
        start = datetime(2023, 5, 13, 17, 10, 0, 0)
        end = datetime(2023, 5, 13, 17, 25, 0, 0)
        winners = await itx.guild.create_scheduled_event(
            name="Announcing Winners",
            description="Come and see the announcement of the winners",
            start_time=start.astimezone(),
            end_time=end.astimezone(),
            location=closing_zoom
        )
        self.events.append(winners)

    @app_commands.command(name="add_events", description="Adds the current events into the list")
    @app_commands.default_permissions(administrator=True)
    async def add_events(self, itx: discord.Interaction):
        print("Adding all events")
        guild_events = await itx.guild.fetch_scheduled_events(with_counts=False)
        for event in guild_events:
            self.events.append(event)
        await itx.response.send_message(content="Events added", ephemeral=True)


    @tasks.loop(minutes=5, count=None)
    async def updates_events(self):
        print("Checking update")
        if len(self.events) == 12:
            guild = self.bot.get_guild(961352126116798524)
            print("here in update")
            events = await guild.fetch_scheduled_events(with_counts=False)
            for idx, event in enumerate(events):
                print("Executing")

                if (event.end_time < datetime.now().astimezone()):
                    print(event.name + " OUTDATED DELETEING")
                    await event.delete()
    
    @tasks.loop(minutes=1, count=None)
    async def announcing_events(self):
        if len(self.events) > 0:
            guild = self.bot.get_guild(961352126116798524)
            events = await guild.fetch_scheduled_events(with_counts=False)
            for idx, event in enumerate(events):
                if (event.start_time - timedelta(minutes=5) < datetime.now().astimezone()):
                    print(event.name + " Starting in 5 minutes")
                    sponsor_channel = discord.utils.get(
                        guild.text_channels, name='announcements')
                    self.events.pop(idx)
                    await sponsor_channel.send(content="@everyone " + event.name + " event is starting soon")


    @app_commands.command(name="delete_events", description="Deletes all the schedule events")
    @app_commands.default_permissions(administrator=True)
    async def delete_events(self, itx: discord.Interaction):
        events = await itx.guild.fetch_scheduled_events(with_counts=False)
        for event in events:
            print(event.name)
            await event.delete()
        self.events = []
        await itx.response.send_message(content="Events deleted", ephemeral=True)

    @app_commands.command(name="clear_event_list", description="clears all the schedule events")
    @app_commands.default_permissions(administrator=True)
    async def clear_events(self, itx: discord.Interaction):
        self.events = []
        await itx.response.send_message(content="Event list cleared", ephemeral=True)

        

    @app_commands.command(name="start_events", description="starts all the schedule events")
    @app_commands.default_permissions(administrator=True)
    async def start_events(self, itx: discord.Interaction):
        events = await itx.guild.fetch_scheduled_events(with_counts=False)
        for event in events:
            if (event.status == discord.EventStatus.scheduled):
                await event.start()
        await itx.response.send_message(content="Events starts", ephemeral=True)
    

async def setup(bot):  # set async function
    await bot.add_cog(EventCog(bot))  # Use await
