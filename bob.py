import os
import json
import time
import datetime
import random

import discord

import basic

#HOPEFULLY THE COMMIT WORKS NOW!

class Bot(discord.Client):

    configfilename = "bob.json"

    data = {
        "metexts": {},
        "birthdays": {},
        "cdate": None,
        "laststarwarsmeme": 0,
        "eventchannel": None
    }

    async def on_ready(self):
        print('Logged on!')
        try:
            self.load()
            print("The " + self.configfilename + " file was loaded")
        except FileNotFoundError:
            print("The " + self.configfilename + " file couldn't be loaded")

    async def on_message(self, msg):
        # Check if a bot wrote the Message
        if not msg.author.bot:
            # Check if Message is meant for Bob
            if str(msg.content)[0] == '!':
                try:
                    # Get Message without '!'
                    chars = str(msg.content)[1:]
                    concatenated = False
                    cconcatenated = []
                    args = [""]
                    for ccharnum in range(0, len(chars)):
                        if chars[ccharnum] == '"':
                            concatenated = not concatenated
                            cconcatenated.append(ccharnum)
                        elif concatenated:
                            cconcatenated.append(ccharnum)
                    
                    carg = 0
                    for ccharnum in range(0, len(chars)):
                        if chars[ccharnum] == ' ' and not ccharnum in cconcatenated:
                            carg += 1
                            args.append("")
                        else:
                            args[carg] += chars[ccharnum]
                    
                    for cargnum in range(0, len(args)):
                        if args[cargnum][0] == '"' and args[cargnum][len(args[cargnum])-1] == '"':
                            args[cargnum] = args[cargnum][1:len(args[cargnum])-1]
                        elif args[cargnum][0] == '"':
                            args[cargnum] = args[cargnum][1:]
                        elif args[cargnum][len(args[cargnum])-1] == '"':
                            args[cargnum] = args[cargnum][0:len(args[cargnum])-1]
                    
                    argobj = None
                    
                    # If the Message contains Arguments, add them to the Object that is handed over to the Function
                    if len(args[1:]) > 0:
                        obj = '{'
                        i = 0
                        while i < len(args[1:]):
                            obj += '"'
                            obj += args[1:][i][1:]
                            obj += '": "'
                            obj += args[1:][i+1]
                            obj += '"'
                            if i + 2 < len(args[1:]):
                                obj += ', '
                            i += 2
                        argobj = json.loads(obj + '}')

                        print(argobj)

                    method = getattr(self, '_' + args[0], self.invalid)
                    await method(msg, argobj)
                except Exception as e:
                    print(f'error because of {msg}: {e}')

    def getMember(self, fullname, channel):
        print("name: " + fullname.split('#')[0])
        print("disc: " + fullname.split('#')[1])
        for m in channel.members:
            print(str(m))
        return discord.utils.get(self.get_all_members(), name=fullname.split('#')[0], discriminator=fullname.split('#')[1])

    async def invalid(self, msg, args):
        await msg.channel.send("Diese Aktion kann ich nicht durchführen!")

    def save(self):
        fstream = open(self.configfilename, 'w')
        fstream.write(json.dumps(self.data))
        fstream.close()

    def load(self):
        fstream = open(self.configfilename, 'r', encoding="utf-8")
        self.data = json.loads(fstream.read())
        fstream.close()

    async def _randomsatz(self, msg, arg):
        klassenliste = self.data["klassenliste"]
        if (arg is None):
            await msg.channel.send("Du musst mit -name [NAME] das Subjekt des Satzes auswählen!")
            return
        if (not arg["name"] in klassenliste):
            await msg.channel.send("Der den du mit -name angegeben hast, befindet sich nicht in der Klassenliste!")
            return

        AdjListe = self.data["words"]["adjectives"]
        ÜbertreibungListe = self.data["words"]["exaggerations"]
        FListe = self.data["words"]["substantives"]["feminine"]
        MListe = self.data["words"]["substantives"]["masculine"]
        NListe = self.data["words"]["substantives"]["feminine"]

        SubstListe = FListe + MListe + NListe

        Subst = SubstListe[random.randint(0, len(SubstListe)-1)]
        adj1 = AdjListe[random.randint(0, len(AdjListe)-12)]
        adj2 = AdjListe[random.randint(0, len(AdjListe)-12)]
        adj3 = "" if random.randint(0, 1) < 1 else AdjListe[random.randint(0, len(AdjListe)-1)]
        Übertreibung1 = "" if random.randint(0, 1) < 1 else ÜbertreibungListe[random.randint(0, len(ÜbertreibungListe)-1)] + " "
        Übertreibung2 = "" if random.randint(0, 1) < 1 else ÜbertreibungListe[random.randint(0, len(ÜbertreibungListe)-1)] + " "
        Übertreibung3 = "" if random.randint(0, 1) < 1 else ÜbertreibungListe[random.randint(0, len(ÜbertreibungListe)-1)] + " "
        RelSubstListeOhneNamen = [ "die Welt", "Deutschland", "Gott", "Jesus", "Sushi" ]
        RelSubstListeMitADJ3 = [ " Menschen", " Pizza", " Pizzen", " Tiere", " Jungs", " Mädchen", " Programmierer", " Psychopathinnen" ]

        RelSubst = ""
        if ((random.randint(0, len(klassenliste) * 3 + len(RelSubstListeOhneNamen) + len(RelSubstListeMitADJ3) - 1) < (len(klassenliste) * 3))):
            RelSubst = klassenliste[random.randint(0, len(klassenliste)-1)]
        else:
            if (random.randint(0, len(RelSubstListeOhneNamen) + len(RelSubstListeMitADJ3) - 1) < len(RelSubstListeOhneNamen)):
                RelSubst = RelSubstListeOhneNamen[random.randint(0, len(RelSubstListeOhneNamen)-1)]
            else:
                RelSubst = (adj3 + RelSubstListeMitADJ3[random.randint(0, len(RelSubstListeMitADJ3-1))]).strip()

        RelListe = self.data["relListe"]
        REL = RelListe[random.randint(0, len(RelListe)-1)]

        rel = ""
        if random.randint(0, 2) > 1:
            rel += Übertreibung3 + "gerne "
        rel += (REL.replace(",", " " + RelSubst + " ") if "," in REL else RelSubst + " " + REL) + "!"

        artikel = ""
        relpronomen = ""
        AdjEndung = ""

        if (Subst in MListe):
            artikel = "ein"
            relpronomen = "der "
            AdjEndung = "r"

        if (Subst in FListe):
            artikel = "eine"
            relpronomen = "die "
            AdjEndung = ""
        if (Subst in NListe):
            artikel = "ein"
            relpronomen = "das "
            AdjEndung = "s"
        
        relativsatz = ", " + relpronomen + rel
        await msg.channel.send(f'{arg["name"]} ist {artikel} {Übertreibung1}{adj1}{AdjEndung}, {Übertreibung2}{adj2}{AdjEndung} {Subst}{relativsatz}')
    async def _HA(self, msg, arg):
        FÄCHER = ["mathe", "deutsch", "latein", "englisch", "musik", "physik", "chemie", "religion"]
        
        if not arg:
            await msg.channel.send("Du hast kein Argument angegeben. Bitte Poste Hausaufgaben per DMs an @BobDerBaumeisert mit !HA -fach mathe -typ post, damit andere sie mit !HA -fach mathe -typ get bekommen können!")
            return
        if not arg["typ"] or arg["fach"]:
            await msg.channel.send(f'Du hast keinen {"typ" if arg["fach"] else "fach"} angegeben. Um die beschreibung der !HA methode zu bekommen, gebe !HA ein.')
            return
        if arg["typ"].lower() == "post":
            if len(msg.attachments) == 0:
                await msg.channel.send("Du musst, wenn du eine Hausaufgabe posten willst, diese per drag & drop mitsenden!")
                return
            if len(msg.attachments) > 1:
                await msg.channel.send("Du kannst pro post anfrage immer nur eine Hausaufgabe senden")
                return
            attachment = msg.atttachments[0]
            dat = open(arg["fach"].lower() + "HA." + attachment.to_file().filename, "wb")
            attachment.save(dat)
            await msg.channel.send("Ihre Datei wurde als Hausaufgabe abgespeichert!")
            return
        #if arg["typ"].lower() == "get":


#    async def _HA(self, msg, arg):
#        FÄCHER = ["mathe", "deutsch"]
#
#        if arg:
#            if arg["typ"]:
#                if arg["typ"].lower() == "post":
#                    if arg["fach"]:
#                        if arg["fach"].lower() in FÄCHER:
#                            if len(msg.attachments) == 1:
#                                attachment = msg.attachments[0]
#                                dat = open(arg["fach"].lower() + "HA." + attachment.to_file().filename, "wb")
#                                attachment.save(dat)
#                                await msg.channel.send("Ihre Datei wurde als Hausaufgabe abgespeichert!")
#                            else:
#                                await msg.channel.send("Die anzahl der Anhänge muss 1 betragen!")
#                        else:
#                            await msg.channel.send("Kein gegebenes Fach vorhanden")
#                    else:
#                        await msg.channel.send("Kein Fach angegeben! Versuche z.B. !HA -typ get -fach Mathe für Mathehausaufgaben")
#
#                elif arg["typ"].lower() == "get":
#                    if arg["fach"]:
#                        if arg["fach"].lower() in FÄCHER:
#                            await msg.channel.send(file=discord.File(arg["fach"].lower() + 'HA.pdf', arg["fach"][0].upper() + arg["fach"][1:].lower() + "_HA.pdf"))
#                        else:
#                            await msg.channel.send("Kein gegebenes Fach vorhanden")
#                    else:
#                        await msg.channel.send("Kein Fach angegeben! Versuche z.B. !HA -typ get -fach Mathe für Mathehausaufgaben")
#                    await msg.channel.send("Falschen Typ angegeben (Versuchen sie get oder post)")
#            else:
#                await msg.channel.send("Kein Typ angegeben!")
#        else:
#            await msg.channel.send("Keine Argumenten angegeben!")
#        
#    async def _rechne(self, msg, arg):
#        print(arg)
#        result, error = basic.run("<stdin>", arg["aufgabe"])
#
#        if error: await msg.channel.send(str(error))
#        else: await msg.channel.send(result)
#
#    async def _moin(self, msg, args):
#        await msg.channel.send("Moin! Servus! Moin!")
#
#    async def _könnenwirdasschaffen(self, msg, args):
#        await msg.channel.send("Jo wir schaffen das! " + str(msg.author))
#
#    async def _lasssaufen(self, msg, args):
#        await msg.channel.send("SAUFEN aber Wasser. Natürich aus der Vodka-Quelle.")
#
#    async def _akzeptieren(self, msg, args):
#        await msg.channel.send("Ich akzeptiere gerne mit.")
#    
#    async def _me(self, msg, arg=None):
#        if not arg == None and not arg["new"] == None:
#            self.data["metexts"].update({self.getMember(str(msg.author), msg.channel).id: arg["new"]})
#            await msg.channel.send("Ihr me Text wurde erfolgreich geändert!")
#        elif self.getMember(str(msg.author), msg.channel).id in self.data["metexts"].keys():
#            await msg.channel.send(self.data["metexts"][self.getMember(str(msg.author), msg.channel).id])
#        else:
#            await msg.channel.send(str(self.getMember(str(msg.author), msg.channel)) + "Du hast noch keinen !me Eintrag")
#
#    async def _stop(self, msg, args):
#        self.removefromactions(str(msg.author))
#        await msg.channel.send("Ok ich höre auf!")
#
#    async def _save(self, msg, args):
#        self.save()
#        await msg.channel.send("Gespeichert!")
#
#    async def _load(self, msg, args):
#        self.load()
#        await msg.channel.send("Geladen!")
#
#    async def _birthday(self, msg, arg=None):
#        if arg and arg["set"]:
#            if arg["p"]:
#                self.data["birthdays"].update({self.getMember(str(msg.author).id): arg["set"]})
#            else:
#                self.data["birthdays"].update({discord.Member(arg["p"]): arg["set"]})
#            await msg.channel.send("Der !birthday Eintrag wurde erfolgreich geändert")
#        elif self.getMember(str(msg.author)).id in self.birthdays.keys():
#            await msg.channel.send(self.birthdays[self.getMember(str(msg.author)).id])
#        else:
#            await msg.channel.send(str(self.getMember(str(msg.author))) + "Du hast noch keinen !birthday Eintrag")
#
#    async def _seteventchannel(self, msg, arg):
#        self.data["eventchannel"] = msg.channel
#        await msg.channel.send("Der Eventchannel wurde geupdated!")
#
#    async def _listen_voice(self, msg, arg):
#        await msg.author.voice.channel.connect()
#
#    async def _leave_voice(self, msg, arg):
#        await msg.voice_client.disconnect()

client = Bot()
cfgf = open("token.txt", 'r')
token = cfgf.read()
client.run(token)