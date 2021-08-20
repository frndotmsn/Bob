# Setup

1. you need to add an token.txt File containing the AuthTok of your Application / Bot.
2. change the bob.json file so that it contains all the neccessary infomation that the Bot needs.

Idk what else for now

# How to setup the bob.json file

The bob.json file must contain various properties on the root object.
Here is a standart layout for the file, which contains the properties.

```

{
	"relListe": /*e.g. ["feeding", "consuming"]*/,
	"klassenliste": /*e.g. ["Adam", "Lisa", "Jennifer", "Ben"]*/,
	"relSubst": {
		"ohneNamen": /*e.g. ["Jesus", "Food", "America"]*/,
		"mitADJ3": /*e.g ["Humans", "Pizza", "Mouses"]*/
	},
	"words": {
		"exaggerations": /*e.g. ["very", "very, very", "incredible"]*/,
		"adjectives": /*e.g. ["royal", "disgusting", "addicted", "dumg", "stupid", "entitled"]*/,
		"substantives":  {
			/* only use this when dealing with languages that contain these three kinds of substantives. Else put everything into neutral */
			"neutral": 
			"feminine": 
			"masculine": 
		}
	}
}

```