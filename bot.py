import discord
import json
import datetime


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()


client = discord.Client()


@client.event
async def on_ready():
    print("Ready")


@client.event
async def on_message(message):
    message_ar = message.content.split(" ")
    cmd = message_ar[0]
    args = message_ar[1:len(message_ar)]
    argresult = ' '.join(args)
    prefix = '/'

    if cmd == prefix + "help":
        embed = discord.Embed(title="Elenco comandi", description=prefix+"ping: pong\n"+prefix+"warn(@utente o id) (motivo): warna un utente (accessibile solo allo staff)\n"+prefix+"warnings (@utente o id): visualizza i warn di un utente\n"+prefix+"delwarn (id warn): elimina un warn tramite id (accessibile solo ai mod)", color=0xff00ff)
        await message.channel.send(content=None, embed=embed)

    elif cmd == prefix + "ping":
        await message.channel.send("pong")

#   comando per assegnare warn
    elif cmd == prefix + "warn":  # /warn (@utente/id) (motivo)
        with open("warn.json") as f:
            warns = json.load(f)

        if discord.utils.find(lambda r: r.name == 'Staff', message.guild.roles) not in message.author.roles:
            await message.channel.send("`Solo lo staff può eseguire questo comando`")
            return

        try:  # presa id utente da warnare
            target = message.mentions[0].id
            if args[0] != message.mentions[0].mention:
                raise IndexError
        except IndexError:
            try:
                target = args[0]
                if len(target) != 18:
                    await message.channel.send("ID non valido")
                    return
            except IndexError:
                await message.channel.send("Uso del comando: `/warn (@utente/ID) (regola violata)`")
                return

        if message.guild.get_member(int(target)) is None:
            await message.channel.send("`L'utente non esiste o non si trova nel server`")
            return
        if (message.guild.get_member(int(target))).bot:
            await message.channel.send("`Non è possibile warnare un bot`")
            return

#   presa del motivo del warn
        motivo = ' '.join(message_ar[2:len(message_ar)])
        if motivo == '':
            await message.channel.send("`Devi specificare un motivo`")
            return

        try:
            id = str(warns['nextId']).zfill(4)
            warns['nextId'] = int(warns['nextId'])+1
        except KeyError:
            warns['nextId'] = 2
            id = '1'.zfill(4)

        try:
            warns['utente'][str(target)].append(id.zfill(4))
        except KeyError:
            warns['utente'][str(target)] = [id]

        warns['warning'][id] = {'utente': target, 'motivo': motivo, 'moderatore': str(message.author), 'data': (datetime.datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")}

        try:  # invio messaggio in dm al target
            await client.get_user(int(target)).send("Sei stato warnato su Anicord per: `" + motivo + "`")
        except discord.errors.Forbidden:
            await message.channel.send("`L'utente ha bloccato il bot o non permette di inviare dm, per cui non è stato possibile avvertirlo`")
        except:
            await message.channel.send("`Non è stato possibile avvertire l'utente`")

#   salvataggio su file del warn
        with open("warn.json", "w") as f:
            json.dump(warns, f)

        await message.channel.send("`Warn loggato ed utente segnalato`")

#   mostra i warn di un utente
    elif cmd == prefix + "warnings":
        if discord.utils.find(lambda r: r.name == 'Staff', message.guild.roles) not in message.author.roles:
            await message.channel.send("`Solo lo staff può eseguire questo comando`")
            return

#   prende l'id dell'utente
        try:
            target = message.mentions[0].id
        except IndexError:
            try:
                target = args[0]
                if len(target) != 18:
                    await message.channel.send("`ID non valido`")
                    return
            except IndexError:
                with open("warn.json", "r") as f:
                    warns = json.load(f)

            #   embed di output
                embed = discord.Embed(
                    color=0xcf672d,
                    timestamp=datetime.datetime.now()
                )
                embed.set_author(
                    name="Warnings nel server",
                    icon_url="https://vignette.wikia.nocookie.net/bakemonogatari1645/images/b/b9/Shinobu.png/revision/latest/top-crop/width/360/height/450?cb=20161221045011"
                )
                embed.set_footer(
                    text="Steins;Gate",
                    icon_url=message.guild.icon_url
                )

                for line in warns['warning']:
                    embed.add_field(
                        name="`#" + id[list(warns['warning'].values()).index(line)] + "` Mod: " + line[
                            'moderatore'] + " | data: " + line["data"], value=line['motivo'], inline=False)

                await message.channel.send(content=None, embed=embed)
                return

        warnings = []
        with open("warn.json", "r") as f:
            warns = json.load(f)

            try:
                for w in warns['utente'][str(target)]:
                    warnings.append(warns['warning'][w])
                id = list(warns['warning'].keys())

            #   embed di output
                embed = discord.Embed(
                    color=0xcf672d,
                    timestamp=datetime.datetime.now()
                )
                embed.set_author(
                    name="Warnings di " + str(client.get_user(int(target))),
                    icon_url=client.get_user(int(target)).avatar_url)
                embed.set_footer(
                    text=target,
                    icon_url=message.guild.icon_url
                )

                for line in warnings:
                    embed.add_field(name="`#" + id[list(warns['warning'].values()).index(line)] + "` Mod: " + line['moderatore'] + " | data: " + line["data"], value=line['motivo'], inline=False)

                await message.channel.send(content=None, embed=embed)
            except KeyError:
                await message.channel.send("`L'utente non ha nessun warn nel server`")
                return

#   comando per cancellare un warn tramite id
    elif cmd == prefix + "delwarn":
        if discord.utils.find(lambda r: r.name == 'Staff', message.guild.roles) not in message.author.roles:
            await message.channel.send("`Solo lo staff può eseguire questo comando`")
            return

        if discord.utils.find(lambda r: r.name == 'Helper', message.guild.roles) in message.author.roles:
            await message.channel.send("`Gli helper non possono usare questo comando`")
            return

        id = argresult
        if len(id) < 4 or len(id) > 4:
            await message.channel.send("`ID non valido`")
            return

#   cancellazione warn
        trovato = False
        with open("warn.json", "r") as f:
            warns = json.load(f)

            if id in warns['warning']:
                del warns['utente'][str(message.guild.get_member(warns['warning'][id]['utente']).id)][warns['utente'][str(message.guild.get_member(warns['warning'][id]['utente']).id)].index(id)]
                del warns['warning'][id]
                trovato = True

        with open("warn.json", "w") as f:
            json.dump(warns, f)

        if trovato:
            await message.channel.send("`Warn cancellato`")
        else:
            await message.channel.send("`Warn non trovato`")

client.run(token)
