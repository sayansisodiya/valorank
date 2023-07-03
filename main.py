import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import json

load_dotenv()
TOKEN = os.getenv('TOKEN')
BASE_URL = "https://api.henrikdev.xyz"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.command(name="rank")
async def rank(ctx):

	message = ctx.message
	user, tag = None, None
	command = message.content[1:]
	keywords = command.split(' ')

	if keywords[0] == "rank":

		user, tag = keywords[1].split('#')

		try:
			response = requests.get(f"{BASE_URL}/valorant/v1/mmr/na/{user}/{tag}")

			if response.status_code == 200:
				data = json.loads(response.text)
				rank_img_url = data["data"]["images"]["large"]
				rank = data["data"]["currenttierpatched"]
				ranking_in_tier = data["data"]["ranking_in_tier"]
				last_game_rr_delta = data["data"]["mmr_change_to_last_game"]

				embed = discord.Embed(
					title=rank,
					description=f"{user}#{tag}",
					color=discord.Color.red() if last_game_rr_delta < 0 else discord.Color.green()
				)

				embed.add_field(name="Progress to next rank", value=f"{ranking_in_tier}/100", inline=False)
				embed.add_field(name="Last game RR change", value=last_game_rr_delta, inline=False)
				embed.set_thumbnail(url=rank_img_url)

				await ctx.send(embed=embed)
		except:
			print("something went wrong")

bot.run(TOKEN)