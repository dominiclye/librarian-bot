from utils.config import load_json_settings

class SettingsActions:
    def __init__(self, db):
        self.db = db
        self.defaults = load_json_settings()

    async def get_guild(self, guild_id):
        return await self.db.find_one({"guild_id": guild_id})
    
    async def add_guild(self, guild_id, settings):
        """Adds a new guild to the guilds collection

        Args:
            guild_id (_type_): The discord guild id of the server to be added
            settings (_type_): The settings defaults

        Returns:
            _type_: _description_
        """
        return await self.db.insert_one({
            "guild_id": guild_id,
            "settings": settings,
            })
    
    async def update_settings(self, guild_id, setting_key, setting_value):
        return await self.db.update_one(
            {"guild_id": guild_id},
            {"$set": {f"settings.{setting_key}": setting_value}},
            upsert=True  
        )
