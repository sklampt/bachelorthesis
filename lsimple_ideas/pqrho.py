import numpy as np
import matplotlib.pyplot as plt

rho_inv  = np.arange(1., 8.5, 0.05)
plt.plot(rho_inv, label='pqrho from diagnostics')

rho_air  = np.arange(0.15,1.47,0.0075)
rho_inv_air = 1.3 / rho_air
plt.plot(rho_inv_air, label='pqrho, calculated as: 1.3/rho_air')

plt.legend()

plt.show()