import numpy as np
import matplotlib.pyplot as plt
def function(x):
    return 4 * (x[0] - 5) ** 2 + (x[1] - 6) ** 2


x=np.linspace(-50, 50, 100)
y=np.linspace(-50, 50, 100)
X, Y = np.meshgrid(x, y)
Z = function([X, Y])

fig = plt.figure()

ax = plt.axes(projection='3d')

ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='green')
ax.set_title('Surface plot geeks for geeks')
plt.show()