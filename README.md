# Fluid Cellular Automaton Visualization

> "A graphics program of this nature is specifically called a cellular automaton when it is 1) parallel, 2) local, and 3) homogeneous.
>
> (1) Parallelism means that the individual cell updates are performed independently. That is, we think of all of the updates being done at once. (Strictly speaking, your computer only updates one cell at a time, but we use a buffer to store the new cell values until a whole screen's worth has been computed to refresh the display.)
>
> (2) Locality means that when a cell is updated, its new color value is based solely on the old color values of the cell and of its nearest neighbors.
>
> (3) Homogeneity means that all cells are updated according to the same rules. Typically the color values of the cell and of its nearest eight neighbors are combined according to some logico-algebraic formula, or are used to locate an entry in a preset lookup table.
>
> Cellular automata can act as good models for physical, biological, and sociological phenomena because each person, or cell, or small region of space 'updates' itself independently (parallelism), basing its new state on the appearance of its immediate surroundings (locality) and on some generally shared laws of change (homogeneity)."
> - Excerpt from [The Cellular Automata Laboratory](https://www.fourmilab.ch/cellab/)

## What is This?

This is a fluid simulation that creates beautiful flowing patterns based on simple rules of interaction between neighboring points in space. Unlike traditional cellular automata that use rigid cells, this simulation uses fluid vectors - imagine tiny arrows that show which way the "fluid" is flowing at each point.

## How it Works

The simulation follows three key principles:

1. **Everything Updates Together**: Just like how a real fluid moves all at once, every point in our simulation updates simultaneously. While the computer can only calculate one point at a time, we store all the new values in a separate buffer until everything is ready to update at once.

2. **Neighbors Matter**: Each point looks at its eight surrounding neighbors to decide how it should change. It considers their:
   - Flow direction and speed
   - Temperature
   - Pressure
   - Color
   
3. **Same Rules Everywhere**: Every point follows exactly the same rules. There are no special cases or different behaviors in different regions.

## Cool Features

- **Temperature Effects**: Warmer areas tend to rise and create swirling patterns
- **Pressure Waves**: Creates rippling effects through the fluid
- **Color Mixing**: Colors blend and flow naturally with the motion
- **Vortices**: Spinning patterns emerge from the interaction of neighboring flows

## How to Play

1. Click and drag to add fluid motion
2. Adjust temperature to create rising or falling flows
3. Change colors to create beautiful mixing patterns
4. Play with different visualization modes to see:
   - Flow vectors
   - Pressure patterns
   - Temperature distribution
   - Spinning motions (vorticity)
   - Color mixing

The simulation creates patterns that totally mirrors real fluid behaviors like weather patterns and ocean currents.
