import numpy as np
import matplotlib.pyplot as plt

r_iv = np.arange(8e-6, 1e-4, 1e-6)
plt.plot(r_iv, np.log10(r_iv*1e4))

def alpha1(r):
    r_so = 1e-4 #m
    x = (r - 1)/(r + 1)
    logarithm = 2 * (x + x**3/3 + x**5/5)
    alpha = logarithm/np.log(10)
    return alpha

result = np.zeros(len(r_iv))
for i in range(len(r_iv)):
    result[i] = alpha1(r_iv[i]*1e4)

plt.plot(r_iv, result)
plt.show()