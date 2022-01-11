from asyncio.windows_events import NULL
import json
import discord

file = "assets/userdata/levels/" + "data.json"
guild_file = "assets/userdata/levels/" + "ranks.json"

class Data:
    def __init__(self):
        self.file = file

    # < ----------------------------------------
    #         Opening a user's account
    # ---------------------------------------- >

    async def open_account(self, user, id):
        users = await self.get_users(id)

        if str(id) not in users:
            users[str(id)] = {}
        
        with open(file, "w") as f:
            json.dump(users, f)

        if str(user.id) in users[str(id)]:
            return False
        else:
            users[str(id)][str(user.id)] = {}
            users[str(id)][str(user.id)]["level"] = 1
            users[str(id)][str(user.id)]["xp"] = 0

        with open(file, "w") as f:
            json.dump(users, f)

        return True

    # < ----------------------------------------
    #         User Data
    # ---------------------------------------- > 

    async def get_user_data(self, user, id):
        with open(file, "r") as f:
            content = json.load(f)
            user = content[str(id)][str(user.id)]

        return user

    # < ----------------------------------------
    #         All Data
    # ---------------------------------------- > 

    async def get_users(self, id):
        with open(file, "r") as f:
            content = json.load(f)

        return content

    # < ----------------------------------------
    #         User updating
    # ---------------------------------------- > 

    async def update_user(self, id, user, xp = 0):
        await self.open_account(user, id)
        users = await self.get_users(id)

        users[str(id)][str(user.id)]["xp"] += xp

        with open(file, "w") as f:
            json.dump(users, f)

        amt = users[str(id)][str(user.id)]["xp"]
        level = users[str(id)][str(user.id)]["level"]
        if amt >= (level * 15):
            await self.add_user_level(id, user, level + 1)

        return amt
    
    # < ----------------------------------------
    #         User updating
    # ---------------------------------------- > 

    async def add_user_level(self, id, user, level = 0):
        users = await self.get_users(id)

        users[str(id)][str(user.id)]["xp"] = 0
        users[str(id)][str(user.id)]["level"] = level

        with open(file, "w") as f:
            json.dump(users, f)

        lvl = users[str(id)][str(user.id)]["level"]
        return lvl

    # < ----------------------------------------
    #         Getting all ranks
    # ---------------------------------------- > 

    async def get_ranks(self):
        with open(guild_file, "r") as f:
            ranks = json.load(f)

        return ranks

    # < ----------------------------------------
    #         Getting guild ranks
    # ---------------------------------------- > 

    async def get_guild_ranks(self, id):
        with open(guild_file, "r") as f:
            content = json.load(f)
            ranks = content[str(id)]

        return ranks

    # < ----------------------------------------
    #         Setting guild ranks
    # ---------------------------------------- >

    async def open_guild(self, id):
        ranks = await self.get_ranks()

        if str(id) in ranks:
            return False
        else:
            ranks[str(id)] = {}

        with open(guild_file, "w") as f:
            json.dump(ranks, f)

        return True

    # < ----------------------------------------
    #         Add guild rank
    # ---------------------------------------- >

    async def add_guild_rank(self, rank, role_id, id):
        await self.open_guild(id)
        ranks = await self.get_ranks()

        if rank in ranks:
            return "There is already a role applied to this rank!"

        ranks[str(id)][str(rank)] = str(role_id)
        with open(guild_file, "w") as f:
            json.dump(ranks, f)

        return False

    # < ----------------------------------------
    #         Rank updating
    # ---------------------------------------- > 

    async def update_user_rank(self, member, id = int):
        await self.open_guild( id)

        user = await self.get_user_data(member, id)
        level = user["level"]

        ranks = await self.get_guild_ranks(id)

        if str(level) in ranks:
            return ranks[str(level)]
        
        return False

    # < ----------------------------------------
    #         Remove rank
    # ---------------------------------------- > 

    async def remove_guild_rank(self, level, id):
        await self.open_guild(id)

        ranks = await self.get_ranks()

        if str(level) in ranks[str(id)]:
            del ranks[str(id)][str(level)]
            with open(guild_file, "w") as f:
                json.dump(ranks, f)

            return False

        else:
            return "No rank reward found for level " + str(level)