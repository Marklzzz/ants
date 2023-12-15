Program has 3 methods:
game, visualize, simulate.
game (previously known as main) is a realtime hivemind simulation. parameters are passed from config.py
simulate creates a .txt file with all the states (at each frame) of hivemind system (bakes the simulation)
visualize draws from that txt file to save time

new main is main file of the program. at first lauch draw an ui with ability to modify defaul config.py parameters. using not recommended parameters may lead to unsustainable system and boring simulation

controller.py controls almost all interactions in the simuation. contains all the classes necessary for the simulation

requirements:
colorama==0.4.6
llvmlite==0.41.1
numba==0.58.1
numpy==1.26.1
pygame==2.5.2
tqdm==4.66.1

To create new simulation using UI:
1) run main.py
2) input valid values into each box:
   ants_n - number of ants in the simulation
   n_target_types (from 2 to 5) amount of food target types + queen
   n_targets - amount of targets of each type
   target_health - how many uses by ants can target have
   margin_to_queen (from 1 to 9), converts to decimal from 0.1 to 0.9 - percentage of screen width (or height) separation required for ant to declare itself queen
   queen_start_health - defaul queen health (as well as maximum)
   simulate,main,visualize (1,2 or 3) with 1 runs simulate.py - pre-render into file.txt (warning: new simulate overwrites previous file). 2 runs game.py (previously known as main.py) - realtime simulation and visualization. 3 runs visualize.py, which uses data from file.txt to render pre-rendered simulation.
3) press enter. If all the values are valid, simulation or the visualization will start in a few seconds (shouldn't be longer than 15)

If you wish so, you can modify any parameter using config.txt and running any file separately, OR you can modify borders.txt (WARNING: highly unrecommended, as it might lead to crashes) and extend valid value interval.
   
