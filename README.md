#PokemonGo-RedStreak

<b>Disclaimer: Using this software is against the ToS and can get you banned. Use at your own risk.<b>

Currently includes the following PokemonGo hacks
<br> 1) Seeking and capturing specific pokemon within a given radius from a given location
<br> 2) Farming Pokestops within a given radius from a given location

<br> usage: python main.py [-h] [-a AUTH_SERVICE] -u USERNAME [-p PASSWORD] -l LOCATION -st STEP_LIMIT [-i IGNORE | -o ONLY] 

##Usage

###Step1

Download the project zip and unzip in it a desired location on your local system.

###Step2

Create a file config.json with your authentication details as shown below and place it inside the project folder along with main.py
#### Contents of config.json

{
    "auth_service": "google",
    "username": "test@gmail.com",
    "password": "password",
    "location": "0.0,0.0"
}

location can be an address or (lat,lng)

###Step 3
Move into the project folder in the terminal and then run <b>python main.py -st 10</b>

st indicates the number of steps away from your location it should look, higher numbers being farther.

##Credits
Building off Mila432's [PokemonGo Map](https://github.com/Mila432/Pokemon_Go_API) and tjado's [pgoapi](https://github.com/tejado/pgoapi)

<br>
If you have an idea for a new feature that could be added, please go ahead!


