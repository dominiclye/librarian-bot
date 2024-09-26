from discord.ext import commands
import discord
from dbActions.SettingsActions import SettingsActions
from utils.config import load_user_json_settings


class Productivity(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.settings_actions = SettingsActions(bot.guilds_client["users"])
        self.user_defaults = load_user_json_settings()
    
    @commands.command()
    async def goals(self, ctx):
        user_id = ctx.author.id
        user = await self.settings_actions.get_user(user_id)
        if not user:
            self.bot.user_settings_cache[user_id] = self.user_defaults
            await self.settings_actions.add_user(user_id, self.user_defaults)
            user_settings = self.user_defaults
        else:
            self.bot.user_settings_cache[user_id] = user['settings']
            user_settings = user['settings']
        
        goals = user_settings.get('goals', []) 

        embed = discord.Embed(title=f"{ctx.author.display_name}'s Goals",  color=self.bot.settings_cache[ctx.guild.id]['color'])
        if goals:
            for goal in goals:
                embed.add_field(name=goal["title"], 
                                value=f"Status: `{goal['status']}`",
                                inline=False)
            
        else:
            embed.description = "You haven't added any goals"
        
        await ctx.reply(embed=embed)

    @commands.command()
    async def add_goal(self, ctx, *, goal):
        user_id = ctx.author.id
        if 'goals' not in self.bot.user_settings_cache[user_id]:
            self.bot.user_settings_cache[user_id]['goals'] = []
        
        self.bot.user_settings_cache[user_id]['goals'].append(
            {"title": goal, 
             "status": "incomplete"
            })
        await self.settings_actions.update_user_settings(user_id, 'goals', self.bot.user_settings_cache[user_id]['goals'])

        embed = discord.Embed(title="Goal Created", description=f"Added goal \"{goal}\" to goals", color=self.bot.settings_cache[ctx.guild.id]['color'])
        embed.add_field(name="Status", value="`incomplete`")

        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Productivity(bot))