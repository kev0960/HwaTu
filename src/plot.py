import matplotlib.pyplot as plt
import numpy as np

with open("log2") as log:
  content = log.readlines()

p0 = []
p1 = []
for line in content:
  l = line.split(' ')
  player_0 = float(l[4])
  player_1 = float(l[5])

  p0.append(player_0)
  p1.append(player_1)

fig, ax = plt.subplots()
ax.plot(np.arange(0, len(p0)), p0, np.arange(0, len(p0)), p1)
ax.set_xlabel("Num iterations (per 3000)")
ax.set_ylabel("Average score (7 point is winning)")
fig.suptitle("Average score between Model player and Random Agent.")
plt.show()