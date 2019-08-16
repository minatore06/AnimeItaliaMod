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
            with open("warn.txt") as f:
                lines = f.readlines()

            last_line = lines[len(lines)-1]
            id = int(last_line[19:23])+1
            print(id)
        except IndexError:
            id = 1111;

        if discord.utils.find(lambda r: r.name == 'Staff', message.guild.roles) not in message.author.roles:
            await message.channel.send("Solo lo staff può eseguire questo comando")
            return;

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
            f.write(str(target)+" "+str(id)+": "+motivo+"\n")

        await message.channel.send("Warn loggato")


    elif cmd == prefix + "warnings":
        if discord.utils.find(lambda r: r.name == 'Staff', message.guild.roles) not in message.author.roles:
            await message.channel.send("Solo lo staff può eseguire questo comando")
            return;

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

        warnings = []
        f = open("warn.txt", "r")
        for line in f:
            if str(target) in line:
                warnings.append(line[18:len(line)])
        f.close();

        embed = discord.Embed(
            description=''.join(warnings),
            color=0x00ff00)
        embed.set_author(name = "Warnings di " + str(message.mentions[0]), icon_url=message.mentions[0].avatar_url)
        await message.channel.send(content=None, embed=embed)

    elif cmd == prefix + "delwarn":
        id = argresult
        if len(id) < 4 or len(id) > 4:
            await message.channel.send("ID non valido")
            return;

        with open("warn.txt", "r") as f:
            lines = f.readlines()
        with open("warn.txt", "w") as f:
            for line in lines:
                if line.strip("\n")[19:23] != str(id):
                    f.write(line);

        await message.channel.send("Warn cancellato")


client.run(token);