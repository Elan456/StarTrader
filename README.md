# StarTrader
***
## Table of contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Tutorial](#tutorial)
   1. [Getting Started](#getting-started)
   2. [Shop](#shop)
   3. [Ship Building](#ship-building)
   4. [Route Management](#route-management)
   5. [Battle](#battle)
4. [Upcoming Features](#upcoming-features)
***

## Introduction

Welcome to the sprawling expanse of the cosmos, intrepid traveler! After a less-than-stellar turn of events in your previous
occupation, you've decided to blast your own trail among the stars. As a determined captain, you traverse the galaxy,
driven to craft your destiny anew by trading resources and confronting ruthless pirates. Expanding your ship is the
key to survival and success, as it is both your canvas and weapon in this gripping saga of ambition, growth,
and cosmic exploration.
***

## Installation

Currently, the game is not yet packaged into an executable. Instead, you will need to clone this repository and run
`main.py` with a python interpreter.

***The game has only been tested on 1920x1080 displays***

1. Clone the repository to your local machine.  
    `git clone https://github.com/Elan456/StarTrader.git`
2. Navigate inside the repository  
   `cd StarTrader`
3. Download required Python libraries  
   `pip install -r requirements.txt`
4. Run main.py  
   `python main.py`
***

## Tutorial

It is not essential to read this entire tutorial before playing the game, although I do
recommend following along with the [Getting Started](#getting-started) section.

Be sure to come back here if anything is confusing, as the game is currently way less
intuitive than it ought to be. 

### Getting Started
1. When you first launch the game, you should be in the shop screen with 5k credits shown
in the top left corner.  
Purchase:
   * 2 hamster wheels 
   * 1 poor container
   * 1 rock thrower
2. Let's assemble our ship. Click on the *Build* button in the bottom left corner
3. Click and drag on each module and place it on the grid as you like

Example:  
![First ship example](https://github.com/Elan456/StarTrader/blob/7504c7963885438fc0ce00cdc24727312a569613/assets/first_ship.png)  
5. Let's go do a route. Click on the *Route* button in the bottom left corner.
6. Here, you can move between systems for free by clicking on connected systems or
use the route selection menu on the right to carry cargo. See the [Route Management](#route-management)
section for more info. 
7. Select a route that earns around $100 and click *go*.
8. Once the battle starts, move up and down to avoid enemy projectiles and aim your
weapons.
9. Destroy the enemy core and attach any modules that come unattached to your ship.
10. Continuing taking routes and buying more modules for your ship.
11. There is full *save and quit* functionality, so don't be afraid to quit
and comeback. 

### Shop
- To purchase modules, click on the green *plus* sign button.
- To sell modules, click on the red *minus* sign button.
- When you sell a module, you get 100% of the value back.
- You can scroll using your scroll wheel, the *w* and *s* keys or the buttons in the
bottom right corner.
- The modules get more expensive from left to right.

### Ship Building
- Click and drag modules onto the hanger (gray grid) in the center.
- All modules must fit entirely within the hanger.
- The hanger can be upgraded to a larger size with the *Upgrade Hanger* button
- Dragging a module past the red line on the right side will sell it.
- Pressing *Save* will check if your ship is valid and if it is, will save it
locally. 
- Pressing reset will move all your modules off the grid and to the right side of the screen.
- Modules cannot overlap. 
- Speed is equal to your ship's power divided by its mass. Modules
on the second row of the shop generate power. The speed determines how
quickly your ship moves in battle, allowing you to dodge projectiles.

### Route Management
- You are located in the system with the white ring around it.
- The green lines with red centers connect to the systems 
that you can travel to. 
- Each one of those lines is also shown as a route in the route selection menu
on the right side. 

#### There are two ways to move around the galaxy
1. Free travel:  
Simply click on a system that has a green line attached to it, and your ship
will travel there instantly. You will not be attacked by pirates because you
have no cargo. 
2. Taking routes:  
    - Click *Go* on the route you want to take from the route selection menu.
    - These routes are sorted from highest to lowest award.  
    - The higher the reward, the more dangerous the pirates will be to intercept you.  
**If all the routes say no reward**, then you either have no cargo modules or
none of the neighboring systems desire something the system you are in has. 


### Battle
- Use the *w* and *s* keys to move your ship up and down.
- The speed of your ship is determined by the ratio of power to mass.
- If power modules are destroyed, you'll get slower. 
- If cargo modules are destroyed in battle, you'll make less money from
completing the route.
- All of your weapons shoot completely automatically.

#### Building during battle
- When a module gets disconnected from the rest of the ship, it will start floating around.
- These floating modules can be attached to your ship using your mouse.
- Often, collected modules can be worth more than the cargo you
were carrying. 
- After the battle, keep them as a member of your ship or sell them for extra profit!

***

## Upcoming Features
- Fuel implementation
- Original Score
- Sound effects
- Unique projectiles
- Interactive tutorial
