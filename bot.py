import discord


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()


client = discord.Client()


@client.event
async def on_message(message):
    message_ar = message.content.split(" ");
    cmd = message_ar[0];
    args = message_ar[1:len(message_ar)];
    argresult = ' '.join(args);
    prefix = '\\'

    if cmd == prefix + "ping":
        await message.channel.send("pong");

    if cmd == prefix + "warn":
        try:
            target = message.mentions[0].id;
        except IndexError:
            try:
                target = args[0];
                if len(target) != 18:
                    await message.channel.send("ID non valido")
                    return;
            except IndexError:
                await message.channel.send("Devi taggare qualcuno")
                return;

        motivo = ' '.join(message_ar[2:len(message_ar)])
        if motivo == '':
            await message.channel.send("Devi specificare un motivo")
            return;

        with open("warn.txt", "a") as f:
            f.write(str(target)+" "+motivo+"\n")

        await message.channel.send("Warn loggato")


client.run(token);