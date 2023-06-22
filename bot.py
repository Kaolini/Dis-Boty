import asyncio
import pathlib
from datetime import datetime
import funks
import requests
import discord
import responses
from discord.ext import tasks, commands
import os, random
from twitchAPI.twitch import Twitch
from discord.utils import get
import json



async def send_message(message, user_message, is_private):
    try:
        response = responses.response_handler(user_message)
        if is_private:
            await message.author.send
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)


async def get_file(ctx, filepath):
    file = random.choice(os.listdir(filepath))
    with open(f"{filepath}/{file}", 'rb') as fp:
        fp = pathlib.Path(f"{filepath}/{file}")
        picture = discord.File(fp=fp)
        await ctx.send(file=picture)


client_id = "tiwmuc5jeqlpi9jole26ykc1ewmpkm"
client_secret = "lobwaq9n1olcw5425fqiu88rtbyr0r"
twitch = Twitch(client_id, client_secret)
twitch.authenticate_app([])
TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/helix/streams"
API_HEADERS = {
    'Client-ID': client_id,
    'Accept': 'application/vnd.twitchtv.v5+json',
}
reqSession = requests.Session()
# def checkuser(user):
#     try:
#         userid = twitch.get_users(logins=[user])['data'][0]['id']
#         url = TWITCH_STREAM_API_ENDPOINT_V5.format(userid)
#         try:
#             req = requests.Session().get(url, headers=API_HEADERS)
#             jsondata = req.json()
#             if 'stream' in jsondata:
#                 if jsondata['stream'] is not None:
#                     return True
#                 else:
#                     return False
#         except Exception as e:
#             print("Error checking user: ", e)
#             return False
#     except IndexError:
#         return False
def checkUser(userID):
    try:
        body = {
            'client_id': client_id,
            'client_secret': client_secret,
            "grant_type": 'client_credentials'
        }
        r = requests.post('https://id.twitch.tv/oauth2/token', body)

        # data output
        keys = r.json()
        headers = {
            'Client-ID': client_id,
            'Authorization': 'Bearer ' + keys['access_token']
        }

        stream = requests.get(f'https://api.twitch.tv/helix/streams?user_login={userID}', headers=headers)
        jsondata = stream.json()

        if len(jsondata['data']) == 1:
            return True
        else:
            return False

    except Exception as e:
        print("Error checking user: ", e)
        return False





def run_discord_bot():
    TOCKEN = "MTExNTk0MjE2ODY3OTQyODE2Ng.GnxGF8.b76rUW363m6-fL9jlf3w_nbsb2Sa9TLJ10vg4c"
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    # client = discord.Client(intents=intents)
    client = commands.Bot(command_prefix="!", intents=intents)


    @client.command()
    async def get_list_users(ctx):
        # with open('jsons/boints.json', 'r') as file:
        #     users = json.loads(file.read())

        user_ids = []
        for i in ctx.guild.members:
            user_ids.append(i.id)
        boints = {}
        for k in user_ids:
            print(k)
            boints[k] = 1000

        # Adds the changes we made to the json file.
        with open('jsons/boints.json', 'w') as file:
            file.write(json.dumps(boints))
        # Tells the user it worked.

    @client.command()
    async def choose(ctx, mess, mess_2):
        choses = [mess, mess_2]
        chose = random.choice(choses)
        await ctx.send(f"{chose}")



    @client.command()
    async def add_twitch(ctx, twitch_name):
        # Opens and reads the json file.
        with open('jsons/streemers.json', 'r') as file:
            streamers = json.loads(file.read())

        # Gets the users id that called the command.
        user_id = ctx.author.id
        # Assigns their given twitch_name to their discord id and adds it to the streamers.json.
        streamers[user_id] = twitch_name

        # Adds the changes we made to the json file.
        with open('jsons/streemers.json', 'w') as file:
            file.write(json.dumps(streamers))
        # Tells the user it worked.
        await ctx.send(f"Added {twitch_name} for {ctx.author} to the notifications list.")



    @client.command()
    async def invite(ctx):
        author = ctx.message.author.mention
        channels_names = {}
        for channel in client.get_guild(1097398661908017252).channels:
            if str(channel.type) == "text":
                channels_names[channel.name] = channel.id
        print(channels_names)



        await ctx.channel.send(content=f"What game do you want to play?")
        res = await client.wait_for(
            "message",
            check=lambda x: x.channel.id == ctx.channel.id
                            and ctx.author.id == x.author.id
                            and x.content,
            timeout=None,
        )
        memb_list = []
        if not ctx.message.guild:
            await ctx.channel.send("In what channel do you wan to send an invite?")
            chan = await client.wait_for(
                "message",
                check=lambda x: x.channel.id == ctx.channel.id
                                and ctx.author.id == x.author.id
                                and x.content in channels_names,
                timeout=None,
            )
            dest_channel = client.get_guild(1097398661908017252).get_channel(channels_names[chan.content])
            await ctx.channel.send(f"Invite will be sent into '{chan.content}' channel")
            await dest_channel.send(
                f"@here ALLO! {author} invites you to play {res.content}! Write !accept if you wanna join!")
            red = False
            while not red:
                tasks = [asyncio.create_task(client.wait_for(
                    "message",
                    check=lambda x: x.channel.id == ctx.channel.id
                                    and ctx.author.id == x.author.id
                                    and x.content in "!ready",
                    timeout=None,
                ),name = "ready"),
                    asyncio.create_task(client.wait_for(
                        "message",
                        check=lambda x: x.channel.id == dest_channel.id
                                        and ctx.author.id != x.author.id
                                        and x.content in "!accept",
                        timeout=None,
                    ),name = "accept")
                ]
                done, pending = await asyncio.wait(tasks,return_when=asyncio.FIRST_COMPLETED)
                finished: asyncio.Task = list(done)[0]
                action = finished.get_name()
                result = finished.result()
                if action == "accept":
                    member = result.author.mention
                    memb_list.append(result.author)
                    await ctx.channel.send(
                        content=f"{member} accepted the invite!")
                elif action == "ready":
                    for i in memb_list:
                        await i.send(f"{author} is ready to play {res.content}! Hop on to VC!")
                    red = True

        else:
            await ctx.channel.send(content=f"@here ALLO! {author} invites you to play {res.content}! Write !accept if you wanna join!")
            red = False
            while not red:
                tasks = [asyncio.create_task(client.wait_for(
                    "message",
                    check=lambda x: x.channel.id == ctx.channel.id
                                    and ctx.author.id == x.author.id
                                    and x.content in "!ready",
                    timeout=None,
                ), name="ready"),
                    asyncio.create_task(client.wait_for(
                        "message",
                        check=lambda x: x.channel.id == ctx.channel.id
                                        and ctx.author.id != x.author.id
                                        and x.content in "!accept",
                        timeout=None,
                    ), name="accept")
                ]
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                finished: asyncio.Task = list(done)[0]
                action = finished.get_name()
                result = finished.result()
                if action == "accept":
                    member = result.author.mention
                    memb_list.append(result.author)
                    await ctx.message.author.send(f"{member} accepted the invite!")
                elif action == "ready":
                    for i in memb_list:
                        await i.send(f"{author} is ready to play {res.content}! Hop on to VC!")
                    red = True


    @client.command()
    async def gn(ctx):
        author = ctx.message.author.mention
        gn_time = datetime.now()
        await ctx.channel.send(content=f"{author} went to sleep! <:Sleepge:1118159574374035548>")
        res = await client.wait_for(
            "message",
            check=lambda x: x.channel.id == ctx.channel.id
                            and ctx.author.id == x.author.id
                            and x.content,
            timeout=None,
        )
        if res:
            wake_time = datetime.now()
            dur = funks.getDuration(gn_time, wake_time)
            await ctx.channel.send(content= funks.print_time(dur, author))

    @client.command()
    async def wish(ctx):
        author = ctx.message.author.mention
        if not " " in ctx.message.content:
            await ctx.channel.send(f"Please specify to who you want to make a wish!")
        else:
            await ctx.channel.send(content=f"What do you want to wish for {str(ctx.message.content).replace('!wish ', '')}?")
            res = await client.wait_for(
                "message",
                check=lambda x: x.channel.id == ctx.channel.id
                                and ctx.author.id == x.author.id
                                and x.content,
                timeout=None,
            )
            await ctx.channel.send(f"Hey {str(ctx.message.content).replace('!wish ', '')}!{author} wishes you {res.content}")

    @client.command()
    async def love(ctx):
        author = ctx.message.author.mention
        comp = funks.read_compl()
        await ctx.channel.send(f"{author} {comp}")

    @client.command()
    async def widehardio(ctx):
        await get_file(ctx, "pictures/widehardio")

    @client.command()
    async def nino(ctx):
        await get_file(ctx, "pictures/nino")

    @client.command()
    async def zain(ctx):
        await get_file(ctx, "pictures/zain")

    @client.command()
    async def petar(ctx):
        await get_file(ctx, "pictures/petar")

    @client.command()
    async def nameless(ctx):
        await get_file(ctx, "pictures/nameless")


    @client.command()
    async def avatar(ctx, *, avamember: discord.Member = None):  # set the member object to None
        if not avamember:  # if member is no mentioned
            member = ctx.message.author  # set member as the author
        userAvatar = avamember.avatar
        await ctx.send(userAvatar)

    @client.command()
    async def about(ctx):
        author = ctx.message.author
        with open("bot_doc.txt") as d:
            read = d.read()
        await author.send(read)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")

        @tasks.loop(seconds=60)
        async def live_notifs_loop():
            # Opens and reads the json file
            with open('jsons/streemers.json', 'r') as file:
                streamers = json.loads(file.read())
            # Makes sure the json isn't empty before continuing.
            if streamers is not None:
                # Gets the guild, 'twitch streams' channel, and streaming role.
                guild = client.get_guild(1097398661908017252)
                channel = client.get_channel(1119243519131926558)
                # Loops through the json and gets the key,value which in this case is the user_id and twitch_name of
                # every item in the json.
                for user_id, twitch_name in streamers.items():
                    # Takes the given twitch_name and checks it using the checkuser function to see if they're live.
                    # Returns either true or false.
                    status = checkUser(twitch_name)
                    # Gets the user using the collected user_id in the json
                    user = client.get_user(int(user_id))
                    # Makes sure they're live
                    if status is True:
                        res = 0
                        mess_ch = []
                        # Checks to see if the live message has already been sent.
                        async for message in channel.history(limit=10):
                            # If it has, break the loop (do nothing).
                            mess_ch.append(message.content)
                        for mess in mess_ch:
                            if str(user.mention) in mess and "is now life on Twitch" in mess:
                                res +=1
                            else:
                                continue

                        async for message in channel.history(limit=10):
                            if res > 0:
                                break
                            # If it hasn't, assign them the streaming role and send the message.
                            else:
                                print(user.mention)
                                print(message.content)
                                # Gets all the members in your guild.
                                # Sends the live notification to the 'twitch streams' channel then breaks the loop.
                                await channel.send(
                                    "@here"
                                    f"<:LETSGO:1114624389384785960>"
                                    f"\n{user.mention} is now life on Twitch!"
                                    f"\nhttps://www.twitch.tv/{twitch_name}")
                                print(f"{user} started streaming. Sending a notification.")
                                break
                    # If they aren't live do this:
                    else:
                        # Gets all the members in your guild.
                        # Checks to see if the live notification was sent.
                        async for message in channel.history(limit=200):
                            # If it was, delete it.
                            if str(user.mention) in message.content and "is now life on Twitch" in message.content:
                                print(f"deleting the message {message.content}")
                                await message.delete()

        # Start your loop.
        live_notifs_loop.start()

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if 'dota' in message.content.lower():
            emoji = client.get_emoji(1116017614376947853)
            await message.add_reaction(emoji)

        if 'black' in message.content.lower():
            emoji = client.get_emoji(1103575074994405386)
            await message.add_reaction(emoji)

        if user_message[0] == "$":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
        await client.process_commands(message)





    client.run(TOCKEN)
