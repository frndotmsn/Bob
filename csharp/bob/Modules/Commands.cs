using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using Discord;
using Discord.WebSocket;
using Newtonsoft.Json;

namespace bob
{
    public class Commands
    {
        public async Task Randomsatz(Bob bob, SocketUserMessage msg)
        {
            try
            {
                string name = Bob.StringToDict(msg.ToString())["name"];
                if (name == null)
                {
                    await msg.ReplyAsync("Du musst mit -name [NAME] das Subjekt des Satzes auswählen!");
                    return;
                }

                List<string> klassenliste = bob._data.klassenliste;
                if (!klassenliste.Contains(name))
                {
                    await msg.ReplyAsync("Der den du mit -name angegeben hast, befindet sich nicht in der Klassenliste!");
                    return;
                }

                List<string> AdjListe = bob._data.words.adjectives;
                List<string> ÜbertreibungsListe = bob._data.words.exaggerations;
                List<string> FListe = bob._data.words.substantives.feminine;
                List<string> MListe = bob._data.words.substantives.masculine;
                List<string> NListe = bob._data.words.substantives.neutral;
                List<string> RelListe = bob._data.relListe;
                List<string> RelSubstListeOhneNamen = bob._data.relSubst.ohneNamen;
                List<string> RelSubstListeMitADJ3 = bob._data.relSubst.mitADJ3;

                List<string> SubstListe = new List<string>(FListe.Count + MListe.Count + NListe.Count);

                SubstListe.AddRange(FListe);
                SubstListe.AddRange(MListe);
                SubstListe.AddRange(NListe);

                string Subst = SubstListe[new Random().Next(0, SubstListe.Count)];
                string adj1 = AdjListe[new Random().Next(0, AdjListe.Count)];
                string adj2 = AdjListe[new Random().Next(0, AdjListe.Count)];
                string adj3 = new Random().Next(0, 2) < 1 ? "" : AdjListe[new Random().Next(0, AdjListe.Count)];
                string Übertreibung1 = new Random().Next(0, 2) < 1 ? "" : ÜbertreibungsListe[new Random().Next(0, ÜbertreibungsListe.Count)];
                string Übertreibung2 = new Random().Next(0, 2) < 1 ? "" : ÜbertreibungsListe[new Random().Next(0, ÜbertreibungsListe.Count)];
                string Übertreibung3 = new Random().Next(0, 2) < 1 ? "" : ÜbertreibungsListe[new Random().Next(0, ÜbertreibungsListe.Count)];

                string relSubst = "";
                if ((new Random().Next(0, klassenliste.Count + RelSubstListeOhneNamen.Count + RelSubstListeMitADJ3.Count) < klassenliste.Count * 3))
                    relSubst += klassenliste[new Random().Next(0, klassenliste.Count)];
                else
                    relSubst = new Random().Next(0, RelSubstListeOhneNamen.Count + RelSubstListeMitADJ3.Count) < RelSubstListeOhneNamen.Count ? RelSubstListeOhneNamen[new Random().Next(0, RelSubstListeOhneNamen.Count)] : (adj3 + RelSubstListeMitADJ3[new Random().Next(0, RelSubstListeMitADJ3.Count)]).Trim();
                
                string REL = RelListe[new Random().Next(0, RelListe.Count)];

                string rel = "";
                if (new Random().Next(0, 3) > 1)
                    rel += Übertreibung3 + " gerne ";
                rel += (REL.Contains(',') ? REL.Replace(",", " " + relSubst + " ") : relSubst + " " + REL) + "!";

                string artikel = "ein";
                string relpronomen = "";
                string AdjEndung = "";

                if (MListe.Contains(Subst))
                {
                    relpronomen = "der";
                    AdjEndung = "r";
                }
                if (FListe.Contains(Subst))
                {
                    artikel += "e";
                    relpronomen = "die";
                }
                if (NListe.Contains(Subst))
                {
                    relpronomen = "das";
                    AdjEndung = "s";
                }

                await msg.ReplyAsync(string.Format("{0} ist {1} {2} {3}{4}, {5} {6}{7} {8}, {9} {10}", name, artikel, Übertreibung1, adj1, AdjEndung, Übertreibung2, adj2, AdjEndung, Subst, relpronomen, rel));
            }
            catch (Exception e)
            {
                await msg.ReplyAsync("Ein falsches Format wurde bei der eingabe benutzt!");
            }
        }
    }
}
