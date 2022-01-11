import json

class Balance():
    def __init__(self):
        self.file = 'assets/userdata/economy/eco.json'

    # ============()============
    #   All users
    # ============()============
    
    async def get_all_users(self):
        with open(self.file, 'r', encoding="utf8") as f:
            users = json.load(f)
        
        return users
    
    # ============()============
    #   Get guild users
    # ============()============

    async def get_guild_users(self,id):
        await self.create_guild(id)
        with open(self.file, 'r', encoding="utf8") as f:
            content = json.load(f)
            guild_users = content[str(id)]
        
        return guild_users
    
    # ============()============
    #   Create guild
    # ============()============

    async def create_guild(self, id):
        users = await self.get_all_users()

        if str(id) in users:
            return False
        else:
            users[str(id)] = {}

        with open(self.file, "w") as f:
            json.dump(users, f)

        return True

    # ============()============
    #   Create account
    # ============()============
    
    async def create_account(self, user, id):
        await self.create_guild(id)
        users = await self.get_all_users()

        if str(user.id) in users[str(id)]:
            return False
        else:
            users[str(id)][str(user.id)] = {}
            users[str(id)][str(user.id)]['balance'] = 200

        with open(self.file, "w") as f:
            json.dump(users, f)

        return True

    # ============()============
    #   Update balance
    # ============()============

    async def update_balance(self, user, balance, id):
        await self.create_account(user, id)

        users = await self.get_all_users()

        users[str(id)][str(user.id)]['balance'] += balance

        with open(self.file, "w") as f:
            json.dump(users, f)

        return users[str(id)][str(user.id)]['balance']