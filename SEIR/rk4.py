import numpy as np
import matplotlib.pyplot as plt


def dsdt(beta, mu, nu, n, susceptible, infected):
    return mu*(n-susceptible)-((beta*susceptible*infected)/n)-(nu*susceptible)


def dedt(beta, sigma, mu, n, susceptible, infected, exposed):
    return ((beta*susceptible*infected)/n)-((mu+sigma)*exposed)


def didt(sigma, gamma, mu, infected, exposed):
    return (sigma*exposed-(mu+gamma)*infected)


def drdt(gamma, mu, nu, susceptible, infected, recovered):
    return (gamma*infected)-(mu*recovered)+(nu*susceptible)


def k2_k3(arg, dt):
    return arg + 0.5 * dt


def calculate_next_step(k1, k2, k3, k4):
    return (1.0 / 6.0)*(k1 + 2 * k2 + 2 * k3 + k4)


def runge_seir_model(init_values, beta, gamma, sigma, mu, nu, t, n):
    S_0, E_0, I_0, R_0 = init_values
    S, E, I, R = [S_0], [E_0], [I_0], [R_0]
    dt = t[1] - t[0]
    for _ in t[1:]:

        beta_dt = k2_k3(beta, dt)
        gamma_dt = k2_k3(gamma, dt)
        sigma_dt = k2_k3(sigma, dt)
        mu_dt = k2_k3(mu, dt)
        nu_dt = k2_k3(nu, dt)
        n_dt = k2_k3(n, dt)

        k1_s = dt * dsdt(beta, mu, nu, n, S[-1], I[-1])
        k1_e = dt * dedt(beta, sigma, mu, n, S[-1], I[-1], E[-1])
        k1_i = dt * didt(sigma, gamma, mu, I[-1], E[-1])
        k1_r = dt * drdt(gamma, mu, nu, S[-1], I[-1], R[-1])

        k2_s = dt * dsdt(beta_dt, mu_dt, nu_dt, n_dt,
                         k2_k3(S[-1], k1_s), k2_k3(I[-1], k1_i))
        k2_e = dt * dedt(beta_dt, sigma_dt, mu_dt, n_dt,
                         k2_k3(S[-1], k1_s), k2_k3(I[-1], k1_i), k2_k3(E[-1], k1_e))
        k2_i = dt * didt(sigma_dt, gamma_dt, mu_dt,
                         k2_k3(I[-1], k1_i), k2_k3(E[-1], k1_e))
        k2_r = dt * drdt(gamma_dt, mu_dt, nu_dt,
                         k2_k3(S[-1], k1_s), k2_k3(I[-1], k1_i), k2_k3(R[-1], k1_r))

        k3_s = dt * dsdt(beta_dt, mu_dt, nu_dt, n_dt,
                         k2_k3(S[-1], k2_s), k2_k3(I[-1], k2_i))
        k3_e = dt * dedt(beta_dt, sigma_dt, mu_dt, n_dt,
                         k2_k3(S[-1], k2_s), k2_k3(I[-1], k2_i), k2_k3(E[-1], k2_e))
        k3_i = dt * didt(sigma_dt, gamma_dt, mu_dt,
                         k2_k3(I[-1], k2_i), k2_k3(E[-1], k2_e))
        k3_r = dt * drdt(gamma_dt, mu_dt, nu_dt,
                         k2_k3(S[-1], k2_s), k2_k3(I[-1], k2_i), k2_k3(R[-1], k2_r))

        sum_sigma_and_dt = sigma+dt
        sum_gamma_and_dt = gamma+dt
        sum_beta_and_dt = beta+dt
        sum_mu_and_dt = mu+dt
        sum_nu_and_dt = nu+dt
        sum_n_and_dt = n+dt
        
        k4_s = dt * dsdt(sum_beta_and_dt, sum_mu_and_dt,
                         sum_nu_and_dt, sum_n_and_dt, S[-1]+k3_s, I[-1]+k3_i)
        k4_e = dt * dedt(sum_beta_and_dt, sum_sigma_and_dt, sum_mu_and_dt, sum_n_and_dt,
                         S[-1]+k3_s, I[-1]+k3_i, E[-1]+k3_e)
        k4_i = dt * didt(sum_sigma_and_dt, sum_gamma_and_dt,
                         sum_mu_and_dt, I[-1]+k3_i, E[-1]+k3_e)
        k4_r = dt * drdt(sum_gamma_and_dt, sum_mu_and_dt, sum_nu_and_dt,
                         S[-1]+k3_s, I[-1]+k3_i, R[-1]+k3_r)

        next_S = S[-1] + calculate_next_step(k1_s, k2_s, k3_s, k4_s)
        next_E = E[-1] + calculate_next_step(k1_e, k2_e, k3_e, k4_e)
        next_I = I[-1] + calculate_next_step(k1_i, k2_i, k3_i, k4_i)
        next_R = R[-1] + calculate_next_step(k1_r, k2_r, k3_r, k4_r)

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
runge_results = runge_seir_model(
    init_values, beta, gamma, sigma, mu, nu, t, N)

plt.figure(figsize=(12, 8))
plt.plot(runge_results)
plt.legend(['Susceptible', 'Exposed', 'Infected', 'Recovered'])
plt.xlabel('Time Steps')

plt.show()
