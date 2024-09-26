from discord.ext import commands
import discord

class ErrorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error",
                description=f"» Error, you are missing the required argument `{err.param}`!",
                color=self.bot.color
            )

            await ctx.reply(embed=embed, mention_author=False)
        
        elif isinstance(err, commands.MissingPermissions):
            err = ', '.join(err.missing_perms)

            embed = discord.Embed(
                title="Error",
                description=f"Error, you are missing the required permission(s): `{err}`!",
                color=self.bot.color
            )
            await ctx.reply(embed=embed, mention_author=False)
        
        elif isinstance(err, commands.MissingAnyRole):
            err = ', '.join(err.missing_roles)

            embed = discord.Embed(
                title="Error",
                description=f"Error, you are missing the required role(s): `{err}!",
                color=self.bot.color
            )

            await ctx.reply(embed=embed, mention_author=False)
        elif not isinstance(err, commands.CommandNotFound):
            embed = discord.Embed(
                title="Error",
                description=f"Error with command `{ctx.invoked_with}`: {err}!",
                color=self.bot.color
            )

            await ctx.reply(embed=embed, mention_author=False)
        else:
            print(f"Error: `{err}`")

async def setup(bot):
    await bot.add_cog(ErrorHandling(bot))