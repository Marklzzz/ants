Program has 3 methods:
game, visualize, simulate.
game (previously known as main) is a realtime hivemind simulation. parameters are passed from config.py
simulate creates a .txt file with all the states (at each frame) of hivemind system (bakes the simulation)
visualize draws from that txt file to save time

new main is main file of the program. at first lauch draw an ui with ability to modify defaul config.py parameters. using not recommended parameters may lead to unsustainable system and boring simulation

controller.py controls almost all interactions in the simuation. contains all the classes

requirements:
