import json

class Pet():
    def __init__(self):
        self.file = "assets/userdata/fun/" + "pets.json"

    # ============()============
    #   Getting all owners
    # ============()============
    
    async def get_users(self):
        """``Returns an object with all the owners``

        ``Input``: Nothing
        ``Output example``: { "1234554321": {"pet": "dog", "pet_level": 3, "pet_xp": 50}, "5432112345": {"pet": "cat", "pet_level": 1, "pet_xp": 14} }
        ``Usage example``: await self.get_users()
        """
        with open(self.file, 'r', encoding="utf8") as f:
            users = json.load(f)
        
        return users

    # ============()============
    #   Create owner
    # ============()============
    
    async def create_account(self, user):
        """``Creates a JSON object, returns True if object is created and False if object already exists``

        ``Input``: discord user
        ``Output example``: True
        ``Usage example``: await self.create_account(ctx.author)
        """
        users = await self.get_users()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]['pet'] = ""
            users[str(user.id)]['pet_level'] = 1
            users[str(user.id)]['pet_xp'] = 0

        with open(self.file, "w") as f:
            json.dump(users, f)

        return True

    # ============()============
    #   Update owner
    # ============()============

    async def update_account(self, user, pet):
        """``Updates the balance of a user then returns the balance after updating``

        ``Input``: discord user, dict
        ``Output example``: {"pet": "cat", "pet_level": 5, "pet_xp": 13}
        ``Usage example``: await bal.update_account(ctx.author, {"pet": "cat", "pet_level": 0, "pet_xp": 5}) <= How many you want to add
        """

        await self.create_account(user)
        users = await self.get_users()

        users[str(user.id)]['pet'] = pet['pet']
        users[str(user.id)]['pet_level'] += pet['pet_level']
        users[str(user.id)]['pet_xp'] += pet['pet_xp']

        with open(self.file, "w") as f:
            json.dump(users, f)

        if users[str(user.id)]['pet_xp'] >= (users[str(user.id)]['pet_level'] * 15):
            await self.add_user_level(user, users[str(user.id)]['pet_level'] + 1)

        return users[str(user.id)]

    # < ----------------------------------------
    #         Pet level updating
    # ---------------------------------------- > 

    async def add_pet_level(self, user, level = 0):
        users = await self.get_users(id)

        users[str(user.id)]["xp"] = 0
        users[str(user.id)]["level"] = level

        with open(self.file, "w") as f:
            json.dump(users, f)

        lvl = users[str(user.id)]["level"]
        return lvl