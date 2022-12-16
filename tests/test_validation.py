"""Test functions in validation.py.

This script tests the function error_statistics() from the module
validation.py.
"""
from okplm import error_statistics


# Test error_statistics
t_sim = list(range(20))
v_sim = list(range(20))
t_obs = [3, 5, 6, 15]
v_obs = [3, 5, 7, 15]

res = error_statistics(t_sim, v_sim, t_obs, v_obs)

t_obs = [33, 5, 6, 15]
v_obs = [3, 5, 7, 15]

res = error_statistics(t_sim, v_sim, t_obs, v_obs)
