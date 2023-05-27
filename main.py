import asyncio

import discord
#   Import commands
from discord import app_commands

# Import the stats file
import stats as discord_stats
import ai_commands

TOKEN = "MTExMTYwNzE1NDk0MDU5NjI3NQ.GtII-p.387yPwJrSn7bvUPAUMhy9gHrbwCDVgGrSBnPMk"
GUILD_ID = 918826505876959242


class MyClient(discord.Client):
    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"Logged in as {self.user}!")


intents = discord.Intents.default()
intents.message_content = True

# Create the client
client = MyClient(intents=intents)

# Create the commands tree
tree = app_commands.CommandTree(client)


# Create a command
@tree.command(
    name = "stats",
    description = "Get the latest $NOOT stats!",
    guild = discord.Object(id=GUILD_ID),
)
@app_commands.describe(timeframe = "The duration of which you want to get the stats for")
@app_commands.choices(timeframe = [
    app_commands.Choice(name="5m", value="5m"),
    app_commands.Choice(name="15m", value="15m"),
    app_commands.Choice(name="30m", value="30m"),
    app_commands.Choice(name="1h", value="1h"),
    app_commands.Choice(name="6h", value="6h"),
    app_commands.Choice(name="24h", value="24h"),
])
async def stats(interaction, timeframe: str = "24h"):
    try:
        await interaction.response.defer()

        # Get the coin stats
        coin_stats = discord_stats.get_coin_stats()

        color = 0x000000

        # Get the embed color based on the 24h percentage change
        if coin_stats.change_24h > 0:
            color = 0x16a34a
        elif coin_stats.change_24h < 0:
            color = 0xdc2626

        # Get the gecko terminal stats
        screenshot = discord_stats.geckoterminal_stats(timeframe=timeframe)

        # Create the embed
        embed = discord.Embed(title=f"# Latest $NOOT stats - {timeframe}", description="Here are the latest $NOOT stats from Gecko Terminal and CoinGecko", color=color)

        # Add the image
        embed.set_image(url="attachment://stats.png")


        def __set_text_color_ansi(text: str, color: int, format: int = 0):
            return f"```ansi\n\u001b[{format};{color}m{text}\n```"


        # Add the fields
        embed.add_field(name="Price", value=__set_text_color_ansi(f"${float(coin_stats.price):.12f}", 37, 1), inline=False)
        embed.add_field(name="ATH", value=__set_text_color_ansi(f"${float(coin_stats.ath):.12f}", 36, 1), inline=True)
        embed.add_field(name="ATL", value=__set_text_color_ansi(f"${float(coin_stats.atl):.12f}", 31, 1), inline=True)
        embed.add_field(name="Market Cap", value=__set_text_color_ansi(f"${int(coin_stats.market_cap)}", 37, 1), inline=False)
        embed.add_field(name="24h Change", value=
        __set_text_color_ansi(
            (f"▲ {float(coin_stats.change_24h):.2f}%") if coin_stats.change_24h > 0 else (f"▼ {float(coin_stats.change_24h):.2f}%"),
            (36 if coin_stats.change_24h > 0 else 31),
            1
        ), inline=False)

        # Create a view
        view = discord.ui.View()

        poocoin_button = discord.ui.Button(
            label="📊 PooCoin Charts", url="https://poocoin.app/tokens/0x98a2500a2c3b8877b0ed5ac3acc300c50bf7064b",
            style=discord.ButtonStyle.link
        )

        # Telegram button
        telegram_button = discord.ui.Button(
            label="📎 Telegram", url="https://t.me/nootnew",
            style=discord.ButtonStyle.link
        )

        # Twitter button
        twitter_button = discord.ui.Button(
            label="🐦 Twitter", url="https://twitter.com/nootcoinbnb",
            style=discord.ButtonStyle.blurple
        )

        # Website button
        website_button = discord.ui.Button(
            label="🐧 Website", url="https://noot.fun",
            style=discord.ButtonStyle.link
        )

        # Add the buttons
        view.add_item(poocoin_button)
        view.add_item(telegram_button)
        view.add_item(twitter_button)
        view.add_item(website_button)


        await interaction.followup.send(embed=embed, file=screenshot, view=view)

    except Exception as e:
        await interaction.followup.send(f"Error: {e}")


@tree.command(
    name="ai_analysis",
    description="Get the latest $NOOT AI analysis based on the current price trends!",
    guild=discord.Object(id=GUILD_ID),
)
@app_commands.describe(timeframe="The duration of which you want to get the analysis for")
@app_commands.choices(timeframe = [
    app_commands.Choice(name="1 day", value=1),
    app_commands.Choice(name="7 days", value=7),
    app_commands.Choice(name="14 days", value=14),
    app_commands.Choice(name="30 days", value=30),
])
async def ai_analysis(interaction, timeframe: int = 1):
    await interaction.response.defer()

    try:
        # Here we get the AI analysis
        response = await ai_commands.get_ai_analysis(timeframe=timeframe)

        print(str(response))
        await interaction.followup.send(str(response))

    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

client.run(TOKEN)