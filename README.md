# Reinforcment-Learning-MC

Reinforment learnig project with Q-learning and eligibility trace algorithm

agent.py is the ﬁle in which there is learning algorithm. For this exercise, at the beginning of a new game, the reset function called returns to the agent information about the range of possible x coordinates. 

main.py is the program that actually run the agent. You can run it with the command python main.py. It also accepts a few command-line arguments: 
- --ngames N will run your agent for N games against in the same environment and report the total cumulative reward 
- --niter N maximum number of iterations allowed for each game 
- --batch B will run B instances of your agent in parallel, each against its own bandit, and report the average total cumulative reward 
- --verbose will print details at each step of what your agent did. This can be helpful to understand if something is going wrong. 
- --interactive will train your agent ngames times, then run an interactive game displaying informational plots. You need to have matplotlib installed to use it.


The running of your agent follows a general procedure that will be shared for all later practicals: 
- The environment generates an observation 
- This observation is provided to your agent via the act method which chooses an action 
- The environment processes your action to generate a reward
