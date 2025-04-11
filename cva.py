# -*- coding: utf-8 -*-
"""
@author: cyrus
"""

# A derivative contract with 3 future time points (t1 = 1 year, t2, t3)

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