import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from dbActions.SettingsActions import SettingsActions

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.settings_actions = SettingsActions(bot.guilds_client["guilds"])

    @commands.command(aliases=['setcolour'])
    @commands.has_permissions(administrator=True)
    async def setcolor(self, ctx, color):
        try:
            if color.startswith("0x"):
                color = int(color, 16)
            elif color.startswith("#"):
                color = int(color[1:], 16)
            else:
                raise ValueError("Invalid color format, use '#RRGGBB' or '0xRRGGBB'")
            
            old_color = self.bot.settings_cache[ctx.guild.id]['color']
            self.bot.settings_cache[ctx.guild.id]['color'] = color
            await self.settings_actions.update_settings(ctx.guild.id, 'color', color)
            embed = discord.Embed(
                title="Bot Colors",
                description=f"Changing color theme",
                color=self.bot.settings_cache[ctx.guild.id]['color']
            )
            embed.add_field(name="Old Color", value=f"`#{hex(old_color)[2:]}`", inline=True)
            embed.add_field(name="New Color", value=f"`#{hex(color)[2:]}`", inline=True)
            await ctx.reply(embed=embed)
        except ValueError as e:
            await ctx.reply(str(e))
        except Exception as e:
            await ctx.reply(str(e))

async def setup(bot):
    await bot.add_cog(Settings(bot))
