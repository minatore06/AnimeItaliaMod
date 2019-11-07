import discord


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()


client = discord.Client()


def assegna_warnpoint(regola):
    """
    funzione che calcoli il punteggio
    rispetto alla regola violata
    :param regola:
    :return:
    """
    try:
        num_reg = regola[7]
    except:
        num_reg = "null";

    if num_reg == '1':  # spam, flood, scam, flame
        return 5;
    elif num_reg == '2':  # insulti
        return 4;
    elif num_reg == '3':  # fastidi vari
        return 3;
    elif num_reg == '4':  # nick e immagini inappropriati
        return 2;
    elif num_reg == '5':  # volgarità, bestemmie, comportamento
        return 4;
    elif num_reg == '6':  # chat secondo la funzione
        return 1;
    elif num_reg == '7':  # tag staff e false segnalazioni
        return 2;
    elif num_reg == '8':  # discutere su decisioni staff
        return 2;
    elif num_reg == '9':  # doppio account
        return 8;
    else:  # custom
        return 1;


def old_warnpoint(target):
    """
    funzione che prenda il punteggio
    dell'ultimo warn di un utente
    :param target:
    :return:
    """
    old_point = '';

    f = open("warn.txt", "r")
    for line in f:
        if str(target) in line[0:18]:
            old_point = (line[39:40])
    f.close();

    if old_point == '':
        old_point = 10;
    return old_point;


@client.event
async def on_message(message):
    message_ar = message.content.split(" ");
    cmd = message_ar[0];
    args = message_ar[1:len(message_ar)];
    argresult = ' '.join(args);
    prefix = '/'

    if cmd == prefix + "help":
        embed = discord.Embed(title = "Elenco comandi", description = prefix+"ping: pong\n"+prefix+"warn(@utente o id) (motivo): warna un utente (accessibile solo allo staff)\n"+prefix+"warnings (@utente o id): visualizza i warn di un utente\n"+prefix+"delwarn (id warn): elimina un warn tramite id (accessibile solo ai mod)", color = 0xff00ff)
        await message.channel.send(content=None, embed=embed)

    elif cmd == prefix + "ping":
        await message.channel.send("pong");

#   comando per assegnare warn
    elif cmd == prefix + "warn":  # /warn (@utente/id) (regola o custom)
        try:  # presa id warn
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

        try:  # presa id utente da warnare
            target = message.mentions[0].id;
            if args[0] != message.mentions[0].mention:
                raise IndexError
        except IndexError:
            try:
                target = args[0];
                if len(target) != 18:
                    await message.channel.send("ID non valido")
                    return;
            except IndexError:
                await message.channel.send("Uso del comando: `/warn (@utente/ID) (regola violata)`")
                return;
        if message.guild.get_member(target).bot
            await message.channel.send("Non è possibile warnare un bot")

#   presa del motivo del warn
        motivo = ' '.join(message_ar[2:len(message_ar)])
        if motivo == '':
            await message.channel.send("Devi specificare un motivo")
            return;

#   calcolo punteggio rispetto alla regola
        punti_pun = assegna_warnpoint(motivo)
        punti_pun = int(old_warnpoint(target)) - int(punti_pun)

        try:  # invio messaggio in dm al target
            await client.get_user(int(target)).send("Sei stato warnato su AnimeItalia per: " + motivo)
        except discord.errors.Forbidden:
            await message.channel.send("L'utente ha bloccato il bot o non permette di inviare dm, per cui non è stato possibile avvertirlo")
        except:
            await message.channel.send("Non è stato possibile avvertire l'utente")

#   salvataggio su file del warn
        with open("warn.txt", "a") as f:
            f.write(str(target)+" "+str(id)+": punti rimasti "+str(punti_pun)+" "+motivo+"\n")

        await message.channel.send("Warn loggato ed utente segnalato")

#   mostra i warn di un utente
    elif cmd == prefix + "warnings":
        if discord.utils.find(lambda r: r.name == 'Staff', message.guild.roles) not in message.author.roles:
            await message.channel.send("Solo lo staff può eseguire questo comando")
            return;

#   prende l'id dell'utente
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
            if str(target) in line[0:18]:
                warnings.append(line[18:len(line)])
        f.close();

#   embed di output
        embed = discord.Embed(
            description=''.join(warnings),
            color=0xcf672d)
        embed.set_author(
            name="Warnings di " + client.get_user(int(target)).name+"#"+str(client.get_user(int(target)).discriminator),
            icon_url=client.get_user(int(target)).avatar_url)
        embed.set_footer(text=target)
        await message.channel.send(content=None, embed=embed)

#   comando per cancellare un warn tramite id
    elif cmd == prefix + "delwarn":
        if discord.utils.find(lambda r: r.name == 'Staff', message.guild.roles) not in message.author.roles:
            await message.channel.send("Solo lo staff può eseguire questo comando")
            return;

        if discord.utils.find(lambda r: r.name == '✔️Helper✔️', message.guild.roles) in message.author.roles:
            await message.channel.send("Gli helper non possono usare questo comando")
            return;

        id = argresult
        if len(id) < 4 or len(id) > 4:
            await message.channel.send("ID non valido")
            return;

        count = new_point2 = new_point = 0

#   cancellazione warn
        with open("warn.txt", "r") as f:
            lines = f.readlines()
        with open("warn.txt", "w") as f:
            for line in lines:
                if line[19:23] == str(id):
                    new_point = assegna_warnpoint(line[41:len(line)])
                    target = line[0:18]
#   prende i punti tolti e riaggiungerli all'ultimo warn fatto
                if line.strip("\n")[19:23] != str(id):
                    f.write(line);
#   sovrascrizione warn vecchi
        try:
            with open("warn.txt") as f:
                lines = f.readlines()
            for line in lines:
                count += 1
                if str(target) in line[0:18]:
                    new_point2 = int(line[39:40])
                    linea = list(line);
                    pos = count
            print(str(new_point)+" "+str(new_point2))
            new_point += new_point2
            linea[39] = str(new_point);
            linea = ''.join(linea)
            lines[pos-1] = linea;
            print(lines)

            with open("warn.txt", "w") as f:
                for line in lines:
                    f.write(line)

            await message.channel.send("Warn cancellato")
        except:
            await message.channel.send("Warn azzerati")


client.run(token);
