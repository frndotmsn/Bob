using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Reflection;
using Discord;
using Discord.Commands;
using Discord.WebSocket;
using Microsoft.Extensions.DependencyInjection;

namespace bob
{
    delegate Task Command(Bob bob, SocketUserMessage args);
    public struct Substantives
    {
        public List<string> neutral;
        public List<string> feminine;
        public List<string> masculine;
        public Substantives(List<string> neutral, List<string> feminine, List<string> masculine)
        {
            this.neutral = neutral;
            this.feminine = feminine;
            this.masculine = masculine;
        }
    }
    public struct Words
    {
        public List<string> exaggerations;
        public List<string> adjectives;
        public Substantives substantives;
        public Words(List<string> exaggerations, List<string> adjectives, Substantives substantives)
        {
            this.exaggerations = exaggerations;
            this.adjectives = adjectives;
            this.substantives = substantives;
        }
    }
    public struct RelSubst
    {
        public List<string> ohneNamen;
        public List<string> mitADJ3;
        public RelSubst(List<string> listeOhneNamen, List<string> mitADJ3)
        {
            this.ohneNamen = listeOhneNamen;
            this.mitADJ3 = mitADJ3;
        }
    }
    public struct Data
    {
        public List<string> relListe;
        public List<string> klassenliste;
        public RelSubst relSubst;
        public Words words;
        public Data(List<string> relListe, List<string> klassenliste, RelSubst relSubst, Words words)
        {
            this.relListe = relListe;
            this.klassenliste = klassenliste;
            this.relSubst = relSubst;
            this.words = words;
        }
    }
    static class MethodInfoExtension
    {
        public static bool MatchesDelegate(this MethodInfo methodInfo, Type delegateType)
        {
            MethodInfo delegateSignature = delegateType.GetMethod("Invoke");

            bool parametersEqual = delegateSignature
                .GetParameters()
                .Select(x => x.ParameterType)
                .SequenceEqual(methodInfo.GetParameters()
                    .Select(x => x.ParameterType));

            return delegateSignature.ReturnType == methodInfo.ReturnType && parametersEqual;
        }
    }
    public class Bob
    {
        public DiscordSocketClient _client;
        public static Dictionary<char, char> _escaped = new Dictionary<char, char> { { 'n', '\n' }, { 'r', '\r' }, { 't', '\t' } };
        private Dictionary<string, MethodInfo> _commands;
        public Data _data;
        private Commands _commandsObj;
        public async Task RunBotAsync()
        {
            this._client = new DiscordSocketClient();

            this._commands = new Dictionary<string, MethodInfo>();

            this._commandsObj = new Commands();

            this._data = Newtonsoft.Json.JsonConvert.DeserializeObject<Data>(System.IO.File.ReadAllText("bob.json"));

            foreach (MethodInfo info in typeof(Commands).GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly))
            {
                if (info.MatchesDelegate(typeof(Command)))
                    this._commands.Add(info.Name.ToLower(), info);
            }

            string token = "Nzg4OTAzOTkwNTMxMTk0OTcw.X9qSGA.kKQ7uyjpemk62nhd78Uxp01axZo" /*await System.IO.File.ReadAllTextAsync("token.txt")*/;

            this._client.Log += this._client_Log;

            await RegisterCommandsAsync();

            await this._client.LoginAsync(TokenType.Bot, token);

            await this._client.StartAsync();

            await Task.Delay(-1);
        }
        
        private Task _client_Log(LogMessage arg)
        {
            Console.WriteLine(arg);
            return Task.CompletedTask;
        }

        public async Task RegisterCommandsAsync()
        {
            this._client.MessageReceived += HandleCommandAsync;
        }
        public static List<string> GenerateArgs(string msg)
        {
            List<string> args = new List<string>();
            int cchar = 0;
            while (cchar < msg.Length)
            {
                if (msg[cchar] == ' ')
                {
                    cchar++;
                    continue;
                }
                string cstr = "";
                if (cchar == '"')
                {
                    cchar++;
                    bool escaped = false;
                    while (msg[cchar] != '"' || escaped && cchar < msg.Length)
                    {
                        if (escaped)
                        {
                            cstr += Bob._escaped.ContainsKey(msg[cchar]) ? Bob._escaped[msg[cchar]] : msg[cchar];
                            escaped = false;
                            cchar++;
                            continue;
                        }
                        if (msg[cchar] == '\\')
                        {
                            escaped = true;
                            cchar++;
                            continue;
                        }

                        cstr += msg[cchar];
                        cchar++;
                    }
                    args.Add(cstr);
                    continue;
                }

                for (; cchar < msg.Length && msg[cchar] != ' '; cchar++)
                    cstr += msg[cchar];
                args.Add(cstr);
            }
            return args;
        }
        public static Dictionary<string, string> ArgsToDict(List<string> args)
        {
            Dictionary<string, string> res = new Dictionary<string, string>();
            for (int i = 0; i < args.Count; i += 2)
                res.Add(args[i].Substring(1), args[i + 1]);
            return res;
        }
        public static Dictionary<string, string> StringToDict(string msg) => ArgsToDict(Bob.GenerateArgs(string.Join(' ', msg.ToString().Split(' ')[1..])));

        private async Task HandleCommandAsync(SocketMessage arg)
        {
            SocketUserMessage msg = arg as SocketUserMessage;
            if (msg.Author.IsBot) return;

            int argPos = 0;
            if (msg.HasCharPrefix('!', ref argPos))
            {
                MethodInfo command;
                string strCommand = msg.ToString().Split(' ')[0].Substring(1);
                if (!this._commands.TryGetValue(strCommand, out command))
                {
                    await msg.ReplyAsync("Command " + strCommand + " was Not defined");
                    return;
                }
                await (Task) command.Invoke(this._commandsObj, new object[] { this, msg });
            }
        }
    }
    class Program
    {
        static void Main(string[] args)
        {
            Bob bob = new Bob();
            bob.RunBotAsync().GetAwaiter().GetResult();
        }
    }
}
