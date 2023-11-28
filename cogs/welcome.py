import discord
from discord import ui, app_commands
from discord.ext import commands
import modules.aws.aws_grabber as aws_grabber

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="verify", description="Sends the verification / welcome message")
    async def verify(self, ctx: commands.Context):
        """ Welcome users to the discord
            Present users with Roles
            If student confirm registration
            Modal Popup for AWS comparison
            Either grant or retry access
        """

        # embed part for welcome message
        embed = discord.Embed(
            title="Welcome to CCI's Space Grand Challenge 2022!", color=0xbd8b13, description='Please make sure you have read all the rules before you start! ')
        embed.add_field(name='MISSION KOLLUXIUM Z-85-0', value='Participate in a gamified satellite cybercrime challenge scenario crafted by Cal Poly\'s California Cybersecurity Institute. This year, students will be competing in Mission Kolluxium Z-85-0 to solve challenges that involve intricate, multi-layered cybercrime plots featuring complex characters, physical and digital evidence chains, and puzzles.')
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/964783915002900521/965162229446115408/SGC_Banner-01-comp.jpg")
        embed.set_footer(text="Press start to continue")

        # what button does if clicked

        view = Start()
        await ctx.response.send_message(embed=embed, view=view)

class Start(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='Start', style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = False

        embed = discord.Embed(
            title="By clicking Accept, you indicate that you have fully read and understand the rules in the #rules channel.", color=0xbd8b13)
        view= agree()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class RolePicker(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='Parent', style=discord.ButtonStyle.primary)
    async def parent(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 'parent'
        for child in self.children:
            child.disabled = True
        await clear_roles(interaction)
        # await interaction.response.edit_message(view=self)
        await add_role(interaction, "Parent/Guardian")
        self.stop()

    @discord.ui.button(label='Coach', style=discord.ButtonStyle.primary)
    async def coach(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 'coach'
        for child in self.children:
            child.disabled = True
        await clear_roles(interaction)
        # await interaction.response.edit_message(view=self)
        await add_role(interaction, "Coach")
        self.stop()

    @discord.ui.button(label='Participant', style=discord.ButtonStyle.secondary)
    async def student(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 'Participant'
        for child in self.children:
            child.disabled = True

        view = Confirm()

        embed = discord.Embed(
            title="Have you registered for the space grand challenge?", color=0xbd8b13)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        self.stop()


# Define a simple View that gives us a confirmation menu
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(
            label='No', url="https://www.cognitoforms.com/CCI17/SPACEGRANDCHALLENGEOctober2022"))

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.primary)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        await interaction.response.send_modal(welcome_modal())
        self.stop()


class agree(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='Accept', style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = False
        view = RolePicker()
        embed = discord.Embed(
            title="Are you a parent, coach, or Participant?", color=0xbd8b13)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label='Decline', style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = discord.ui.View()
        view.clear_items()
        embed = discord.Embed(
            title="Sorry, you need to agree to the rules to participate in this competition.", color=0xbd8b13)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class emailhelp(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='Help', style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        email_channel = discord.utils.get(
                interaction.guild.text_channels, name='registration')

        embed = discord.Embed(
            title="You will recieve a dm shortly from staff.", color=0xbd8b13)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

        emailhelp_embed = discord.Embed(
            title=" Email Registration Help", description="Please DM " + interaction.user.mention + " to assist them", color=0xff0000)
        view = claim_emailhelp()
        email_message = await email_channel.send(content="<@&961352126360064114>", embed=emailhelp_embed, view=view)

class claim_emailhelp(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='Claim', style=discord.ButtonStyle.blurple)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("here")
        print(interaction.message.embeds)
        for embed in interaction.message.embeds:
            message = embed.description

        claimed_embed = discord.Embed(
            title= "Claimed!", description=message, color=0xFFFF00)
        await interaction.message.delete()
        await interaction.response.send_message(content="Claimed by " + interaction.user.mention, embed=claimed_embed, view=resolve_emailhelp())
        self.stop()

class resolve_emailhelp(discord.ui.View):
    @discord.ui.button(label='Resolve', style=discord.ButtonStyle.green)
    async def resolve(self, interaction: discord.Interaction, button: discord.ui.Button):
        for embed in interaction.message.embeds:
            message = embed.description

        resolved_embed = discord.Embed(
            title= "Resolved!", description=message, color=0x00FF00)
        await interaction.message.edit(content="Resolved by " + interaction.user.mention, embed=resolved_embed, view=None)
        self.stop()

class welcome_modal(ui.Modal, title="Enter your email to be assigned a role!"):
    """If the participant said they have signed up, creates a modal so the participant
       can be verified with said registration
    """

    email = ui.TextInput(label="Email", style=discord.TextStyle.short,
                         placeholder='Enter your SGC registered email!', required=True, max_length=100)

    async def on_submit(self, interaction: discord.Interaction):

        # TODO: ADD TEAM EMAIL COMPARISON WITH REGISTRATION (presumably in AWS). COMPARE TEAM # AND EMAIL.
        # ADD CHECK OR NOTI, IF EMAIL HAS ALREADY BEEN WELCOMED TO SERVER (prevents malicous/ cheating logins)

        user_info = await aws_grabber.check_email(email=self.email.value)
        await clear_roles(interaction)

        if not user_info:
            embed = discord.Embed(title="The email you entered is not working. Please dismiss all messages and try again or click the help button below to get assistance.", color=0xbd8b13)
            view = emailhelp()
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            role = discord.utils.get(
                interaction.guild.roles, name='Participant')
            await interaction.user.add_roles(role, atomic=True)
            
        
        elif user_info[0]:
            # Giving user the student role
            role = discord.utils.get(
                interaction.guild.roles, name='Participant')
            await interaction.user.add_roles(role, atomic=True)
            team_name = user_info[3].strip().replace(" ", "-").lower()
            all_roles = interaction.guild.roles
            await self.check_all_channel(interaction, interaction.user, team_name, all_roles)
            print(user_info)
            await interaction.response.send_message(f"Welcome {user_info[1]}! You now have the role: {user_info[2]}. Feel free to look around!", ephemeral=True)


    async def check_all_channel(self, interaction, user, team_name, all_roles):
        team_name = self.get_team_name(team_name, all_roles)

        if (team_name):
            if team_name not in user.roles:
                team_role = discord.utils.get(all_roles, name=team_name)
                await user.add_roles(team_role, atomic=True)
            else:
                message = "You already have this teams role"
                await interaction.response.send_message(message, ephemeral=True)
        else:
            message = "COULD NOT FIND YOUR TEAM PLEASE USE /help_message for assistance"
            await interaction.response.send_message(message, ephemeral=True)

    def get_team_name(self, team_name, team_roles):
        for role in team_roles:
            teams = role.name
            info = teams.split("-")
            i = 2
            team_names = ""
            while i < len(info):
                if (i < len(info) - 1):
                    team_names += info[i]
                    team_names += "-"

                elif i == len(info) - 1:
                    team_names += info[i]

                i += 1
            if team_names == team_name:
                print(teams)
                return teams
        print("Not found")
        return False

async def add_role(interaction, role):
    target_role = discord.utils.get(interaction.guild.roles, name=role)
    await interaction.user.add_roles(target_role, atomic=True)
    await interaction.response.edit_message(content=f"You now have the role: {role}! Feel free to look around! (Repeat the `/verify` command if this is wrong)", view=None, embed=None)

async def clear_roles(interaction):
    removePre = ['Parent/Guardian', 'Coach', 'Participant']
    for pre in removePre:
        role = discord.utils.get(interaction.guild.roles, name=pre)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role, atomic=True)
            print(f"Found previous role: {role}, RESETTING")


async def setup(bot):  # set async function
    await bot.add_cog(WelcomeCog(bot))  # Use await
