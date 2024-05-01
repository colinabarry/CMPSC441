# Report: AI Techniques in Adventure Game

## Abstract

This report details the application of various AI techniques within a text-based adventure game. The game involves navigating a player through a generated landscape, engaging in combat, and managing resources. The AI components contribute to world generation, player decision-making, and storytelling.

## Problems Solved

### 1. Integrating Game Components

**a. Realistic City Distribution with Genetic Algorithms (GA):**

- **Problem:** Randomly placed cities lacked realism and could be positioned in illogical locations like mountains or underwater.
- **Solution:** A GA was implemented to optimize city placement.
- **Algorithm:**
  1. **Initial Population:** Generate random city locations within the map bounds.
  2. **Fitness Function:** Evaluate each solution based on criteria such as:
     - Distance from water bodies.
     - Distance from mountains.
     - Minimum distance between cities.
  3. **Selection:** Choose the fittest solutions to reproduce.
  4. **Crossover:** Combine genetic information from parent solutions to create offspring.
  5. **Mutation:** Introduce random changes to offspring to increase diversity.
  6. **Iteration:** Repeat steps 2-5 for a set number of generations.
- **Inputs:** Map size, elevation data, number of cities.
- **Outputs:** Optimized city locations.

**b. Terrain-Based Travel Costs:**

- **Problem:** Travel between cities had uniform costs, ignoring terrain difficulty.
- **Solution:** Travel cost now reflects the cumulative elevation change along the chosen route.
- **Algorithm:**
  1. **Path Generation:** Create a sequence of grid cells connecting the starting and ending cities.
  2. **Elevation Summation:** Sum the elevation values of each cell in the path.
  3. **Cost Calculation:** Multiply the elevation sum by a scaling factor to determine the travel cost.
- **Inputs:** Route coordinates, elevation map.
- **Outputs:** Travel cost.

**c. Route-Restricted Movement:**

- **Problem:** Players could move between any two cities, regardless of the presence of a connecting route.
- **Solution:** Movement is now restricted to established routes between cities.
- **Algorithm:**
  1. **Route Representation:** Store routes as pairs of city indices.
  2. **Movement Validation:** Check if the desired movement corresponds to an existing route before allowing travel.
- **Inputs:** Current city, destination city, list of routes.
- **Outputs:** Boolean indicating whether the movement is valid.

**d. Win/Loss Conditions:**

- **Problem:** Gameplay lacked clear win/loss conditions.
- **Solution:** The game ends if the player runs out of money or loses a combat encounter.
- **Implementation:**
  - Track player's remaining money.
  - End the game if money falls below zero.
  - End the game if the player loses a combat encounter.

### 2. Additional AI Technique: Storytelling with Text Generation

- **Problem:** The game lacked narrative depth and player engagement.
- **Solution:** A text generation model is used to create a dynamic story based on player actions and game events.
- **Tool:** Google AI's Gemini large language model.
- **Implementation:**
  - Log key game events, including travel details and combat encounters.
  - Feed the log to the text generation model.
  - Generate narrative text that describes the player's journey, incorporating combat descriptions, travel challenges, and strategic choices.
- **Benefits:**
  - Enhances immersion and player engagement.
  - Provides context and meaning to player actions.
  - Creates a unique story for each playthrough.

### 3. AI Components Summary

The game utilizes a combination of AI techniques to create a more engaging and dynamic experience:

- **Genetic Algorithms:** Generate realistic city placements.
- **Terrain Analysis:** Calculate travel costs based on elevation data.
- **Rule-Based System:** Restrict movement to valid routes.
- **Text Generation:** Create a compelling narrative based on player actions and game events.

These AI components work together to provide a richer gameplay experience, offering both strategic challenges and narrative depth.

## Appendix A: Gemini Transcripts

- [Route finder](https://g.co/gemini/share/275c3888ea07)
- [Run combat episode](https://g.co/gemini/share/6ef0e5cbb630)
