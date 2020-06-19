import asyncio

import discord
import json
import datetime
import re


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


def check(author):
    def inner_check(message):
        return message.author == author


async def banDash(target, motivo):
    try:
        await client.get_guild(681624606976901211).ban(target, reason=motivo, delete_message_days=1)
    except:
        return False
    return True


async def kickDash(target, motivo):
    try:
        await client.get_guild(681624606976901211).kick(target, reason=motivo)
    except:
        return False
    return True


async def warnDash(target, motivo):
    return

token = read_token()


client = discord.Client()


@client.event
async def on_ready():
    await (await client.fetch_channel(722767918936489995)).fetch_message(722776120897831072)
    print("Ready")


@client.event
async def on_message(message):
    message_ar = message.content.split(" ")
    cmd = message_ar[0]
    args = message_ar[1:len(message_ar)]
    argresult = ' '.join(args)
    prefix = '/'

    permissionlevel = 0
    if message.author.id == 143318398548443136:
        permissionlevel = 15
    else:
        role = discord.utils.find(lambda r: r.name == 'Admin', message.guild.roles)
        if role in message.guild.get_member(message.author.id).roles:
            permissionlevel = 5
        else:
            role = discord.utils.find(lambda r: r.name == 'Supervisore', message.guild.roles)
            if role in message.guild.get_member(message.author.id).roles:
                permissionlevel = 4
            else:
                role = discord.utils.find(lambda r: r.name == 'Moderatore', message.guild.roles)
                if role in message.guild.get_member(message.author.id).roles:
                    permissionlevel = 3
                else:
                    role = discord.utils.find(lambda r: r.name == 'Helper', message.guild.roles)
                    if role in message.guild.get_member(message.author.id).roles:
                        permissionlevel = 2

    if cmd == prefix + "help":
        embed = discord.Embed(title="Elenco comandi", description=prefix+"ping: pong\n"+prefix+"warn(@utente o id) (motivo): warna un utente (accessibile solo allo staff)\n"+prefix+"warnings (@utente o id): visualizza i warn di un utente(se non si specifica un utente mostra tutti i warn)\n"+prefix+"delwarn (id warn): elimina un warn tramite id (accessibile solo ai mod)", color=0xff00ff)
        await message.channel.send(content=None, embed=embed)

    elif cmd == prefix + "ping":
        await message.channel.send("pong")

    elif re.search(("discord.gg/" or "discord.com/invite/" or "discordapp.com/invite/")+"\w{7}", message.content):
        if permissionlevel > 3:
            if permissionlevel == 4:
                await message.channel.send("Puraido sei contento?", delete_after=10.0)
            return
        await message.delete()
        await message.channel.send("Yeah "+message.author.mention+", non mandare inviti", delete_after=15.0)

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

                warnings = []
                for w in list(warns['warning'].keys()):
                    warnings.append(warns['warning'][w])
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

                id = list(warns['warning'].keys())

                for line in warnings:
                    embed.add_field(
                        name="`#" + id[list(warns['warning'].values()).index(line)] + "` Mod: " + line['moderatore'] + " | data: " + line["data"], value=line['motivo'], inline=False)

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


@client.event
async def on_raw_reaction_add(payload):
    user = client.get_user(payload.user_id)
    canale = client.get_channel(payload.channel_id)
    if payload.message_id == 722776120897831072:#  and (reaction.emoji.name == "meg" or reaction.emoji.name == "nicoehh" or reaction.emoji.name == "shinobu"): # == 722777019175403543 or reaction.emoji.id == 687240294890209302 or reaction.emoji.id == 687235747484270624):
        await canale.send("Yey, peace peace, oni no onii-chan\nInviare l'id dell'utente su cui deve cadere il martello della giustizia", delete_after=30)
        try:
            msg = await client.wait_for('message', check=check(user), timeout=30.0)
        except asyncio.TimeoutError:
            await canale.send("'Tempo scaduto'\nI said with a posed look", delete_after=20)
            return
        target = client.get_user(int(msg.content))
        if target is None:
            await canale.send("'Utente non trovato'\nI said with a posed look", delete_after=20)
            return

        await canale.send("Yey\nInviare la motivazione dell'intervento", delete_after=30)
        try:
            msg = await client.wait_for('message', check=check(user), timeout=30.0)
        except asyncio.TimeoutError:
            await canale.send("'Tempo scaduto'\nI said with a posed look", delete_after=20)
            return
        motivo = msg.content

        permissionlevel = 0
        if user.id == 143318398548443136:
            permissionlevel = 15
        else:
            role = discord.utils.find(lambda r: r.name == 'Admin', canale.guild.roles)
            if role in client.get_guild(681624606976901211).get_member(user.id).roles:
                permissionlevel = 5
            else:
                role = discord.utils.find(lambda r: r.name == 'Supervisore', canale.guild.roles)
                if role in client.get_guild(681624606976901211).get_member(user.id).roles:
                    permissionlevel = 4
                else:
                    role = discord.utils.find(lambda r: r.name == 'Moderatore', canale.guild.roles)
                    if role in client.get_guild(681624606976901211).get_member(user.id).roles:
                        permissionlevel = 3
                    else:
                        role = discord.utils.find(lambda r: r.name == 'Helper', canale.guild.roles)
                        if role in client.get_guild(681624606976901211).get_member(user.id).roles:
                            permissionlevel = 2

        if payload.emoji.id == 722777019175403543:  #ban
            if permissionlevel < 3:
                await canale.send("'Non hai il permesso per eseguire questa funzione'\nI said with a posed look", delete_after=10)
                return
            if await banDash(target, motivo):
                await canale.send("'Unlimited Rulebook: versione ban\nL'utente è stato colpito con tutta la forza e ridotto in pezzettini", delete_after=20)
            else:
                await canale.send("Operazione fallita, oni no onii-chan c'è stato un errore", delete_after=10)
        elif payload.emoji.id == 687240294890209302:  #kick
            if permissionlevel < 2:
                await canale.send("'Non hai il permesso per eseguire questa funzione'\nI said with a posed look", delete_after=10)
                return
            if await kickDash(target, motivo):
                await canale.send("'Unlimited Rulebook: versione kick\nL'utente è stato colpito e stordito", delete_after=20)
            else:
                await canale.send("Operazione fallita, oni no onii-chan c'è stato un errore", delete_after=10)
        elif payload.emoji.id == 687235747484270624:  #warn
            if permissionlevel < 2:
                await canale.send("'Non hai il permesso per eseguire questa funzione'\nI said with a posed look", delete_after=10)
                return
            await warnDash(target, motivo)
            await canale.send("`Messaggio di servizio dal programmatore` Non ho voglia di creare questa funzione ora, arrangiatevi", delete_after=20)

client.run(token)
