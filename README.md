#PokemonGo-RedStreak

<b>Disclaimer: Using this software is against the ToS and can get you banned. Use at your own risk.</b>

Currently includes the following PokemonGo hacks
- Seeking and capturing specific pokemon within a given radius from a given location
- Farming Pokestops within a given radius from a given location

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

##Credits
Building off Mila432's [PokemonGo Map](https://github.com/Mila432/Pokemon_Go_API) and tjado's [pgoapi](https://github.com/tejado/pgoapi)

<br>
If you have an idea for a new feature that could be added, please go ahead!


