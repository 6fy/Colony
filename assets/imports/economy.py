import json

class Balance():
    def __init__(self):
        self.file = 'assets/userdata/economy/eco.json'

    # ============()============
    #   All users
    # ============()============
    
    async def get_all_users(self):
        """``Returns an object with all the users``

        ``Input``: Nothing
        ``Output example``: { "9147112941": {"1234554321": {"balance": 200}, "5432112345": {"balance": 200} }, "9147112941": {"1234554321": {"balance": 200} }
        ``Usage example``: await self.get_guild_users()
        """
        with open(self.file, 'r', encoding="utf8") as f:
            users = json.load(f)
        
        return users
    
    # ============()============
    #   Get guild users
    # ============()============

    async def get_guild_users(self,id):
        """``Returns an object with all the users in that particular guild``

        ``Input``: int
        ``Output example``: {"1234554321": {"balance": 200}, "5432112345": {"balance": 200}
        ``Usage example``: await self.get_guild_users(ctx.guild.id)
        """
        await self.create_guild(id)
        with open(self.file, 'r', encoding="utf8") as f:
            content = json.load(f)
            guild_users = content[str(id)]
        
        return guild_users
    
    # ============()============
    #   Create guild
    # ============()============

    async def create_guild(self, id):
        """``Creates a guild object, returns True if object is created and False if object already exists``

        ``Input``: int
        ``Output example``: True
        ``Usage example``: await self.create_account(ctx.guild.id)
        """
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
        """``Creates a JSON object, returns True if object is created and False if object already exists``

        ``Input``: discord user, int
        ``Output example``: True
        ``Usage example``: await self.create_account(ctx.author, ctx.guild.id)
        """
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
        """``Updates the balance of a user then returns the balance after updating``

        ``Input``: discord user, int, int
        ``Output example``: 200
        ``Usage example``: await bal.update_balance(ctx.author, bet, ctx.guild.id)
        """
        await self.create_account(user, id)

        users = await self.get_all_users()

        users[str(id)][str(user.id)]['balance'] += balance

        with open(self.file, "w") as f:
            json.dump(users, f)

        return users[str(id)][str(user.id)]['balance']