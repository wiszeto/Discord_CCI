import discord
from discord.ext import commands
from discord import app_commands

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            code = ord(char) + shift_amount
            if char.islower():
                code = 97 + (code - 97) % 26
            elif char.isupper():
                code = 65 + (code - 65) % 26
            result += chr(code)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def binary_add(a, b):
    return bin(int(a, 2) + int(b, 2))[2:]

def binary_subtract(a, b):
    return bin(int(a, 2) - int(b, 2))[2:]

def binary_multiply(a, b):
    return bin(int(a, 2) * int(b, 2))[2:]

def binary_divide(a, b):
    return bin(int(a, 2) // int(b, 2))[2:]

class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hex_to_decimal", description="Convert a hex value to decimal")
    async def hex_to_decimal(self, interaction: discord.Interaction, hex_value: str):
        try:
            decimal_value = int(hex_value, 16)
            await interaction.response.send_message(f"Decimal value: {decimal_value}")
        except ValueError:
            await interaction.response.send_message("Invalid hex value.")

    @app_commands.command(name="decimal_to_hex", description="Convert a decimal value to hex")
    async def decimal_to_hex(self, interaction: discord.Interaction, decimal_value: int):
        hex_value = hex(decimal_value)
        await interaction.response.send_message(f"Hex value: {hex_value}")
    
    @app_commands.command(name="encrypt", description="Encrypt a message using Caesar Cipher")
    async def encrypt(self, interaction: discord.Interaction, text: str, shift: int):
        encrypted_text = caesar_encrypt(text, shift)
        await interaction.response.send_message(f"Encrypted: {encrypted_text}")

    @app_commands.command(name="decrypt", description="Decrypt a message using Caesar Cipher")
    async def decrypt(self, interaction: discord.Interaction, text: str, shift: int):
        decrypted_text = caesar_decrypt(text, shift)
        await interaction.response.send_message(f"Decrypted: {decrypted_text}")
    
    @app_commands.command(name="binary_add", description="Add two binary numbers")
    async def binary_add_command(self, interaction: discord.Interaction, a: str, b: str):
        try:
            result = binary_add(a, b)
            await interaction.response.send_message(f"Result: {result}")
        except ValueError:
            await interaction.response.send_message("Invalid binary numbers.")

    @app_commands.command(name="binary_subtract", description="Subtract two binary numbers")
    async def binary_subtract_command(self, interaction: discord.Interaction, a: str, b: str):
        try:
            result = binary_subtract(a, b)
            await interaction.response.send_message(f"Result: {result}")
        except ValueError:
            await interaction.response.send_message("Invalid binary numbers.")

    @app_commands.command(name="binary_multiply", description="Multiply two binary numbers")
    async def binary_multiply_command(self, interaction: discord.Interaction, a: str, b: str):
        try:
            result = binary_multiply(a, b)
            await interaction.response.send_message(f"Result: {result}")
        except ValueError:
            await interaction.response.send_message("Invalid binary numbers.")

    @app_commands.command(name="binary_divide", description="Divide two binary numbers")
    async def binary_divide_command(self, interaction: discord.Interaction, a: str, b: str):
        try:
            result = binary_divide(a, b)
            await interaction.response.send_message(f"Result: {result}")
        except ValueError:
            await interaction.response.send_message("Invalid binary numbers.")

async def setup(bot):
    await bot.add_cog(Calculator(bot))