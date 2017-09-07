# Theory of Mind Application in Multiagent Systems

This is my on-going project from my two summer internships at the USC Institute for Creative Technologies (ICT). The initial goal of this project was to model teamwork scenarios in multi-agent systems. The project uses a tool from the ICT called PsychSim, a social simulation modeling framework for partially-observable Markov decision processes (POMDP) using theory of mind. Theory of mind is the ability for humans to model the beliefs of other humans in communication, and is a key factor in human social interaction. Later, this project *evolved* into using evolutionary algorithms for optimizing agent behavior, and showing that agents with theory of mind models outperform agents that do not.

## Quickstart

This project was written in Python, and I used Anaconda to manage my Python environments. The included environment file allows you to quickly run my code:

`conda env create -f psychsim.yml`

## Teamwork Project

The teamwork project is based off of a concept military skirmish scenario. The scenario is set a two-dimensional grid world, with an allied military base, allied soldiers, allied helicopters, and enemy soldiers. The goal is for the allied soldiers to reach a destination on the map, while avoiding engaging or getting captured by the enemy soldiers. The catch is that the allied soldiers and helicopters can only partially observe the world (fog of war), while the enemy soldiers have full observability. The idea is for the helicopters to serve as decoys and distract the enemy soldiers, allowing allied soldiers to get to their destination safely. In this work, we experimented with modifying the agents' reward weights and finding the best weights for a fully-cooperative team.

To run this scenario: `python ./core/teamwork/loader.py`

A configurator will open, allowing you to modify the scenario and customize the agents' reward weights. Then the scenario will begin, and you will be able to watch the agents take turns until the either the soldiers get captured or the soldiers reach their destination.

## Evolutionary Optimization Project (in-progress)

The evolutionary optimization project is a competitive game between two agents trying to gather food. This scenario is set in a two-dimensional grid world, with the probability of food spawning on a random tile. The agents are able to move freely, and also equipped with a laser beam that disables the other agent for a turn. Each of the two agents have three possible models for their actions: greedy, altruistic, or sadistic. Greedy is the model of selecting actions for the best self interest, i.e. maximizing individual food. Altruistic is the model of selecting actions for both personal and the other agent's best self interest, i.e. going after food that will still allow the other agent to maximize their food. Sadistic is the model of maximizing food and harming the other agent in the process, e.g. firing the disabling laser beam. We clamp the weights and settings of one agent (beta) and run an evolutionary algorithm to optimize the other agent's (alpha) weights and settings. Our goal is to answer this question: does theory of mind affect the outcomes of competitive scenarios? We begin by randomizing the model that alpha has on beta, which could be incorrect. If theory of mind has an impact, then many generations of evolution should converge to the agent having the correct theory of mind model about the other agent.

This is still a work in progress, but to run the current scenario: `python ./core/evol/gathering_ea.py`

This will not show a graphical display of the scenario in action, since it is not feasible to display each individual for the entire population of the evolutionary algorithm. The result is a graph of the average score per generation. To view a graphical display of the game, run: `python ./core/gathering/gathering.py`


## Authors

* **Richard Yang** - *Project lead* - rry@stanford.edu
* **David Pynadath** -*Advisor* - pynadath@usc.edu


## License

This project is licensed under the MIT License