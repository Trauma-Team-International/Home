import numpy as np
import matplotlib.pyplot as plt

def didt(sigma, gamma, mu, infected, exposed):
    return (sigma*exposed-(mu+gamma)*infected)


def drdt(gamma, mu, nu, susceptible, infected, recovered):
    return (gamma*infected)-(mu*recovered)+(nu*susceptible)


def euler_seir_model(init_values, beta, gamma, sigma, mu, nu, t, n):
    S_0, E_0, I_0, R_0 = init_values
    S, E, I, R = [S_0], [E_0], [I_0], [R_0]
    dt = t[1] - t[0]
    for _ in t[1:]:

        next_S = S[-1] + dt * dsdt(beta, mu, nu, n, S[-1], I[-1])
        next_E = E[-1] + dt * dedt(beta, sigma, mu, n, S[-1], I[-1], E[-1])
        next_I = I[-1] + dt * didt(sigma, gamma, mu, I[-1], E[-1])
        next_R = R[-1] + dt * drdt(gamma, mu, nu, S[-1], I[-1], R[-1])

        S.append(next_S)
        E.append(next_E)
        I.append(next_I)
        R.append(next_R)
    return np.stack([S, E, I, R]).T
    
t_max = 100
dt = .001
t = np.linspace(0, t_max, int(t_max/dt) + 1)
N = 1000  # population size
init_values = N, 1, 0, 0
# The parameter controlling how often a susceptible-infected contact results in a new exposure.
beta = 1.75
# The rate an infected recovers and moves into the resistant phase.
gamma = 0.2
sigma = 0.5  # The rate at which an exposed person becomes infective.
# The natural mortality rate (this is unrelated to disease). This models a population of a constant size,
mu = 0
nu = 0

# Run simulation
euler_results = euler_seir_model(init_values, beta, gamma, sigma, mu, nu, t, N)

# Plot results
plt.figure(figsize=(12, 8))
plt.plot(euler_results)
plt.legend(['Susceptible', 'Exposed', 'Infected', 'Recovered'])
plt.xlabel('Time Steps')

plt.show()
