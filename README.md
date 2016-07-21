#PokemonGo-RedStreak

Currently includes the following PokemonGo hacks
<br> 1) Seeking and capturing specific pokemon within a given radius from a given location
<br> 2) Farming Pokestops within a given radius from a given location

<br> usage: python main.py [-h] [-a AUTH_SERVICE] -u USERNAME [-p PASSWORD] -l LOCATION -st STEP_LIMIT [-i IGNORE | -o ONLY] 

<br> One may also create a file config.json containing your authentication details as shown below

{
    "auth_service": "google",
    "username": "test@gmail.com",
    "password": "password",
    "location": "0.0,0.0"
}

location can be an address or lat,lng

And then run python main.py -st 10

st indicates the number of steps away from your location it should look, higher numbers being farther.

<br>
<br> Using this software is against the ToS and can get you banned. Use at your own risk.

##Credits
Building off Mila432's [PokemonGo Map](https://github.com/Mila432/Pokemon_Go_API) and tjado's [pgoapi](https://github.com/tejado/pgoapi)

<br>
If you have an idea for a new feature that could be added, please go ahead!


