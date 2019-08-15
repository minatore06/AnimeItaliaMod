import discord

def readToken():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = readToken()

client = discord.Client()

@client.event
def on_message(message):
    messageAr = message.content.split(" ");
    cmd = messageAr[0];
    args = messageAr.slice(1);
    argresult = args.join(' ');



client.run(token)