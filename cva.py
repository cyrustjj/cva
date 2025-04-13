# -*- coding: utf-8 -*-
"""
@author: cyrus
"""

# Example 1: A derivative contract with 3 future time points (t1 = 1 year, t2, t3)

# Parameters
expected_exposure = [10,8,5]  # $10mil, $8mil, $5mil 
prob_default = [0.02, 0.03, 0.04]
discount_factors = [0.952, 0.907, 0.864]   # 1/(1+0.05), 1/(1+0.05)^2, 1/(1+0.05)^3
LGD = 0.6

# CVA = sum_of( EE(t) x PD(t) x LGD x DF(t))

CVA = 0
for EE, PD, DF in zip(expected_exposure, prob_default, discount_factors):
    CVA += EE * PD * LGD * DF

print(f"CVA: ${CVA:0.4f}")

# Example 2: BCVA based on simualted expected exposure paths using Monte Carlo
'''
1. Simulate EE paths using Monte Carlo
2. Calculate CVA and DVA across time steps
3. Combine into BCVA

Assumptions:
    a) Simulated exposures follow a Brownian Motion (N-dist increments)
    b) Default probability & LGD are constant
    c) No wrong-way or right-way risk is considered
'''

import numpy as np
import matplotlib.pyplot as plt

# Parameters
n_paths = 10000     # Monte Carlo paths
n_steps = 10        # Time steps within period T
T = 2
dt = T/n_steps
time_grid = np.linspace(0, T, n_steps)

discount_factors = np.exp(-0.05 * time_grid)  # Assume 5% flat discount curve

# Credit Parameters
LGD_counterparty = 0.6
PD_counterparty_annual = 0.05
LGD_own = 0.5
PD_own_annual = 0.03

# Convert annual PD to default probabilities per time step
PD_counterparty_dt = 1 - np.exp(-PD_counterparty_annual * dt)
PD_own_dt = 1 - np.exp(-PD_own_annual * dt)

# Simulate exposures (simple Brownian motion, positive exposure only)
np.random.seed(35)
exposure_paths = np.maximum(np.cumsum(np.random.normal(0, 10, (n_paths, n_steps)), axis=1), 0)

# Expected Exposure (EE) at each time step
EE = np.mean(exposure_paths, axis=0)

# CVA and DVA per time step
CVA_t = EE * PD_counterparty_dt * LGD_counterparty * discount_factors
DVA_t = EE * PD_own_dt * LGD_own * discount_factors

# Total CVA, DVA and BCVA
CVA = np.sum(CVA_t)
DVA = np.sum(DVA_t)
BCVA = DVA - CVA

# Print results
print(f"Total CVA:  ${CVA:,.2f}")
print(f"Total DVA:  ${DVA:,.2f}")
print(f"Bilateral CVA (BCVA): ${BCVA:,.2f}")

# Plot
plt.figure(figsize=(10, 5))
plt.plot(time_grid, EE, label='Expected Exposure')
plt.title("Expected Exposure Over Time")
plt.xlabel("Time (Years)")
plt.ylabel("Exposure")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
