import discord


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()


client = discord.Client()


@client.event
def on_message(message):
    message_ar = message.content.split(" ");
    cmd = message_ar[0];
    args = message_ar.slice(1);
    argresult = args.join(' ');


client.run(token)