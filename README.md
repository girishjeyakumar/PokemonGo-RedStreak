#PokemonGo-RedStreak

<b>Disclaimer: Using this software is against the ToS and can get you banned. Use at your own risk.</b>

Currently includes the following:
- Automatic seeking and capturing of specific pokemon within a given radius from a given location
- Automatic farming of some Pokestops within a given radius from a given location

##Some info

One of the main goals of the project was to understand the API, to have some fun with the game and to give other developers a starting point.This is definitely not the recommended way of playing the game and Niantic might soon come up more strict retaliations for these hacks.But having to capture nearly 100 Magikarps to get a Gyrados? That's a little too far and here is your solution!

There might not be much more development on this.But I learnt a lot and it was a lot of fun spinning pokestops,catching more than 20 pokemons and gaining more than 3000xp in around an hour just sitting at home.

Other develpers are welcome to build on this, fix some bugs and come up with more cool stuff.I am looking forward to seeing your additions.

**Note**: 
- Found to work better when the user is offline and the app is closed on the phone while running this.It prevents contradicting location data from the phone and your local system being sent to the backend simultaneously.
- Refrain from using large search radius as they have a higher chance of getting you banned.Limit to a step-limit of 1 or 2 to be on safer side.

##Prerequisites

Installation will require Python 2.7 and Pip.Python 3 is currently not supported.

###Ubuntu or Debian

You can install Python and Pip on Ubuntu by running the following command:
```
sudo apt-get install python python-pip
```

###Windows

Download Python [here](https://www.python.org/ftp/python/2.7.12/python-2.7.12.amd64.msi) and install. Then download [pip](https://bootstrap.pypa.io/get-pip.py) (right click that link and choose "Save Link As"), and double click the file you downloaded, assuming you installed Python correctly.

##Setup
- Download the project zip and unzip it in a desired location on your local system.
- Create a file config.json with your authentication details,as it's content, as shown below and place it inside the project folder along with main.py
```
**Content of config.json**

{
    "auth_service": "google [or ptc]",
    "username": "unsername",
    "password": "password",
    "location": "0.0,0.0 [or Valid Address]"
}
```
##Install Dependencies

Now, open a Terminal/Command Line (```Win```+```R``` and ```cmd``` on Windows) and ```cd``` to the folder you extracted the zip file to.
```
cd some/directory/
```
In Windows you can also right click within the folder and select "Open Command Window Here."
Then enter the following:
```
pip install -r requirements.txt
```

##Running

Move into the project folder in the terminal and then run:
```
python main.py -st 10
```
The number following -st indicates the maximum number of steps away from your location it should look, higher numbers being farther.5 steps is approximately a 1.2km radius.

###Using IGNORE and ONLY

Run the following command to ignore some pokemon even if it appears in your scope.These wild pokemon would not be captured.

```
python main.py -st 10 -i Pidgey,Rattata
```

Run the following command to only focus on some pokemon that appears in your scope.These wild pokemon are the only ones that would be captured.

```
python main.py -st 10 -o Pidgey,Rattata
```

##Credits
Building off Mila432's [PokemonGo Map](https://github.com/Mila432/Pokemon_Go_API) and tjado's [pgoapi](https://github.com/tejado/pgoapi)




