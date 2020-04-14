import matplotlib.pyplot as plt
import numpy as np
from scml.scml2020 import *

agent_types = [DecentralizingAgent, BuyCheapSellExpensiveAgent,
               IndDecentralizingAgent, MovingRangeAgent]

world = SCML2020World(
    **SCML2020World.generate(
        agent_types=agent_types,
        n_steps=50
    ),
    construct_graphs=True,
)

_, _ = world.draw()

world.run_with_progress()

fig, ax = plt.subplots(facecolor="w")
ax.plot(world.stats['n_negotiations'])
plt.xlabel('Simulation Step')
plt.ylabel('N. Negotiations')

ax.set_xticks(np.linspace(0, 50, 6))
ax.set_yticks(np.linspace(0, 400, 5))

plt.show()