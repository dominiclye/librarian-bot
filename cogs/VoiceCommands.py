from discord.ext import commands
from discord.ext.commands import has_permissions
from dbActions.SettingsActions import SettingsActions
import discord

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.settings_actions = SettingsActions(bot.guilds_client["guilds"])
        self.temp_channels = {}

    @commands.command()
    @has_permissions(manage_channels=True)
    async def jtc(self, ctx, cid):
        embed = discord.Embed(
            title="Voice Chat Interface",
            description=f"Join to Create channel changed.",
            color=self.bot.color
        )
        embed.add_field(name="Channel ID", value=f"`{cid}`")

        self.bot.settings_cache[ctx.guild.id]['jtc_id'] = cid
        await self.settings_actions.update_settings(ctx.guild.id, 'jtc_id', cid)
        await ctx.reply(embed=embed)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild_id = member.guild.id
        jtc = self.bot.settings_cache.get(guild_id, {}).get('jtc_id')
        
        if before.channel is None and after.channel and str(after.channel.id) == str(jtc):
            guild = member.guild
            channel = await guild.create_voice_channel(name=f"{member.display_name}'s Channel")
            await member.move_to(channel)
            
            if guild.id not in self.temp_channels:
                self.temp_channels[guild.id] = []
            
            self.temp_channels[guild.id].append(channel.id)

        if before.channel and before.channel.id in self.temp_channels.get(member.guild.id, []):
            if len(before.channel.members) == 0:
                await before.channel.delete()
                self.temp_channels[member.guild.id].remove(before.channel.id)

async def setup(bot):
    await bot.add_cog(Voice(bot))