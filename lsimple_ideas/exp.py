import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-9.788129e-17, -0.3, 1e-5)
#x = np.arange(-4.7, 0, 0.01)
plt.plot(x, np.exp(x), label= 'exp')

def alpha1(r):
    r = 1 + r
    return r

result = np.zeros(len(x))
for i in range(len(x)):
    result[i] = alpha1(x[i])

plt.plot(x, result, label= 'taylor')

plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.show()