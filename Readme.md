## Farmer Against Potatoes Idle, Whack A Potato bot

This is just a simple implementation of opencv to auto start the mini game and hit the green and yellow potatoes.

The current code should perform a scan/sclick every ~0.15 seconds atm

### Installation
Windows only

Install python 3.10

Then simply run `python -m pip install -r requirements.txt`

### Usage
Open up the game and open up the minigame screen then run `python main.py`

Settings are set to work with the game in the top left of your screen on the first monitor, with the resolution of 1280/720

If you want to have the screen in a different location/resultion you should be able to tweek the following variables found in main.py
`baseX` This is how many pixels from the left to where your game screen starts
`baseY` This is how many pixels from the top to where your game screen starts
`extraWidth` This is an awkward value based on what resultion you choose
`extraHeight` This is an awkward value based on what resultion you choose

`debug` You can set this to true and you can view the `tests/screenshot.png` that gets created in tests for reviewing if your values above line up with the screen capture

