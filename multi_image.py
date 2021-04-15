from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(19680801)
Nr = 2
Nc = 1

fig, axs = plt.subplots(Nr,Nc)
fig.suptitle('Multiple images')
data = ((1 + 1 + 2) / 10) * np.random.rand(10, 20)
axs[0].imshow(data)
data = ((1 + 1 + 5) / 10) * np.random.rand(1, 20)
axs[1].imshow(data)



plt.show()
