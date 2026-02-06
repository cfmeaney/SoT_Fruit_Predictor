# Sea of Thieves – Food Haul Monte Carlo Simulator

In *Sea of Thieves*, collecting resources as you sail is a key part of the game. As players visit islands, they grab a pocket of food and bring it back to store in the barrels on their ship. But since players can only carry 5 pieces of food at a time, most islands have more than 5 food that can be collected, and there is a clear priority of which food to keep if forced to prioritize, the distribution of food in your ship barrels will not be representative of the distribution of food spawn rates. For example, if a player visits an island with 10 pieces of food uniformly distributed (2 of each), then the player will collect 2 pineapples, 2 mangoes, and 1 pomegranate - a different distribution than the uniform spawn rates.

Thus, an interesting question is what the average resulting distribution of food in a player's ship's barrels is.

This repo contains a small Monte Carlo simulation that estimates the distribution of accumulated food after visiting many islands in *Sea of Thieves*, given a set of simplified assumptions about fruit spawning and player behavior.

The script repeatedly:

1. Generates random fruit spawns on an island  
2. Keeps only the best fruit you can carry  
3. Repeats for many islands  
4. Plots the distribution of what ends up in your ship's barrels on average  

This gives an estimate of what the distribution of food should be given the assumptions.

## Usage

Run the script:

```bash
python SoT_Fruit_Predictor.py
```

A bar chart will appear showing the percentage of your final haul that is:
- bananas
- coconuts
- pomegranates
- mangos
- pineapples

### Adjustable parameters

At the top of the script (with example parameters):

```python
fruit_probs = [0.5, 0.3, 0.15, 0.04, 0.01] # must sum to 1
n = 10 # amount of fruit per island
p = 5 # number of fruit in pocket
I = 5000 # number of islands visited
```

## Assumptions and Details

The simulation makes several simplifying assumptions:

### Fruit Prioritization

From lowest to highest:

- banana  
- coconut  
- pomegranate  
- mango  
- pineapple  

Higher tiers are considered strictly better and are always kept over lower tiers. This is largely true in game as well where higher quality fruits simply give more restored health when eaten, and an extra bite in the case of pineapples.

### Fixed spawn count
Each island always has exactly `n` fruit items available.

### Independent probabilities
Each fruit is sampled independently from the same probability distribution.

### Pocket capacity
You can only carry `p` fruit items per island. 5 is the natural choice here as that is the amount of food that a player can carry in game. But the script allows you to but a different pocket size. Use cases for higher pocket sizes include cases where multiple players are collecting resources from the island or if the player brings a storage crate and can collect more than 5.

### Optimal selection
You always keep the **best** fruit found.
The script sorts fruit by quality and takes the top `p`.

### No other food types nor food loss

Other food types like meat which are present in game are ignored. Similarly, it is assumed that all food collected ends up in the ship
s barrels and doesn't get eaten along the way.

## Requirements

Use the `requirements.txt` file to install the packages needed to run the script.
