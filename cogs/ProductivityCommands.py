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
                embed.add_field(name=f"{goal['index']}. {goal['title']}", 
                                value=f"Status: `{goal['status']}`",
                                inline=False)
            
        else:
            embed.description = "You haven't added any goals"
        
        await ctx.reply(embed=embed)

    @commands.command()
    async def add_goal(self, ctx, *, goal: str):
        user_id = ctx.author.id

        if 'goals' not in self.bot.user_settings_cache[user_id]:
            self.bot.user_settings_cache[user_id]['goals'] = []

        goals = self.bot.user_settings_cache[user_id]['goals']
        next_index = len(goals) + 1

        self.bot.user_settings_cache[user_id]['goals'].append({
            "title": goal,
            "status": "incomplete",
            "index": next_index
        })

        await self.settings_actions.update_user_settings(user_id, 'goals', self.bot.user_settings_cache[user_id]['goals'])

        embed = discord.Embed(
            title="Goal Created", 
            description=f"Added goal \"{goal}\" to your goals",
            color=self.bot.settings_cache[ctx.guild.id]['color']
        )
        embed.add_field(name="Status", value="`incomplete`")
        embed.add_field(name="Index", value=f"`{next_index}`")

        await ctx.reply(embed=embed)

    @commands.command()
    async def remove_goal(self, ctx, goal_index: int):
        user_id = ctx.author.id

        goals = self.bot.user_settings_cache.get(user_id, {}).get('goals', [])
        embed = discord.Embed(title="Removed Goal", color=self.bot.settings_cache[ctx.guild.id]['color'])

        if not goals:
            embed.description = "There are no goals to remove."
            return await ctx.reply(embed=embed)

        if goal_index > len(goals) or goal_index < 1:
            embed.description = "Invalid goal index."
            return await ctx.reply(embed=embed)

        removed_goal = None
        for goal in goals:
            if goal["index"] == goal_index:
                removed_goal = goal
                goals.remove(goal)
                break

        if removed_goal:
            self.bot.user_settings_cache[user_id]['goals'] = goals
            await self.settings_actions.update_user_settings(user_id, 'goals', goals)

            embed.description = f"Successfully removed goal: {removed_goal['title']}"
            embed.add_field(name=f"Index {removed_goal['index']}", value=f"`{removed_goal['title']}`")
        else:
            embed.description = "No goal found with the given index."

        await ctx.reply(embed=embed)

    @commands.command()
    async def goal_status(self, ctx, goal_index: int, status):
        user_id = ctx.author.id
        goals = self.bot.user_settings_cache.get(user_id, {}).get('goals', [])
        embed = discord.Embed(title="Updated Goal Status", color=self.bot.settings_cache[ctx.guild.id]['color'])

        if not goals:
            embed.description = "There are no goals to update."
            return await ctx.reply(embed=embed)

        if goal_index > len(goals) or goal_index < 1:
            embed.description = "Invalid goal index."
            return await ctx.reply(embed=embed)

        updated_goal = None
        for goal in goals:
            if goal["index"] == goal_index:
                updated_goal = goal
                goal["status"] = status
                break

        if updated_goal:
            self.bot.user_settings_cache[user_id]['goals'] = goals
            await self.settings_actions.update_user_settings(user_id, 'goals', goals)

            embed.description = f"Successfully updated goal: \"{updated_goal['title']}\""
            embed.add_field(name=f"Status", value=f"`{updated_goal['status']}`")
        else:
            embed.description = "No goal found with the given index."
    
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Productivity(bot))