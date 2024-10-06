import discord
from discord.ext import commands
from dbActions.SettingsActions import SettingsActions
from utils.config import load_user_json_settings

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings_actions = SettingsActions(bot.guilds_client["guilds"])
        self.user_defaults = load_user_json_settings()


    @commands.command()
    async def bio(self, ctx, member: discord.Member):
        user_id = member.id
        user = await self.settings_actions.get_user(user_id)
        if not user:
            self.bot.user_settings_cache[user_id] = self.user_defaults
            await self.settings_actions.add_user(user_id, self.user_defaults)
            user_settings = self.user_defaults
        else:
            self.bot.user_settings_cache[user_id] = user['settings']
            user_settings = user['settings']

        bio = user_settings.get('bio', {})

        embed = discord.Embed(
            title=f"{member.display_name}'s Bio",
            color=self.bot.settings_cache[ctx.guild.id]['color']
        )
        embed.set_thumbnail(url=member.avatar.url)
        bio = self.bot.user_settings_cache[user_id]['bio']
        embed.add_field(name="Name", value=bio['name'])
        embed.add_field(name="Interests", value=bio['interests'])
        embed.add_field(name="Education level", value=bio['education'])
        embed.add_field(name="Goals", value=bio['goals'])

 
        await ctx.reply(embed=embed)
    
    @commands.command()
    async def editbio(self, ctx, field, *, value: str):
        user_id = ctx.author.id
        user = await self.settings_actions.get_user(user_id)
        

        if not user:
            await self.settings_actions.add_user(user_id, self.user_defaults)
        else:
            self.bot.user_settings_cache[user_id] = user['settings']
            user_settings = user['settings']

        user_settings['bio'][field] = value
        await self.settings_actions.update_user_settings(user_id, 'bio', user_settings['bio'])

        embed = discord.Embed(
            title=f"Updated `{field}` field",
            colour=self.bot.settings_cache[ctx.guild.id]['color']
        )
        embed.add_field(name=field, value=f"`{value}`")

        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Social(bot))