import numpy as np

# Parameters
num_nodes = 1000  # Increase to 10000 for full scale (slower)
num_simulations = 100  # Increase to 1000 for more accuracy
failure_prob = 0.05
alpha, beta, gamma, delta = 1.0, 0.5, 0.3, 0.2

# Centralized simulation
def centralized_simulation():
    throughput = np.random.normal(1.0, 0.2, num_nodes)
    delays = np.random.exponential(0.1, num_nodes)
    failures = np.random.binomial(1, failure_prob, num_nodes)
    
    if np.any(failures):
        global_impact = np.sum(failures) / num_nodes * 10  # Exponential growth
        throughput -= global_impact
        delays += global_impact
    
    jitter = np.std(throughput)
    recovery = np.mean(delays) * 10
    stability = np.var(throughput)
    resilience = np.mean(throughput > 0) * 100
    
    return jitter, recovery, stability, resilience

# Fractal simulation
def fractal_simulation():
    throughput = np.random.normal(1.0, 0.2, num_nodes)
    delays = np.random.exponential(0.1, num_nodes)
    risks = np.random.uniform(0, 0.1, num_nodes)
    failures = np.random.binomial(1, failure_prob, num_nodes)
    
    # Vectorized stress (approx with shifts for mesh)
    shift1 = np.roll(throughput, 1)
    shift2 = np.roll(throughput, -1)
    stress = (np.abs(throughput - shift1) / (shift1 + 1e-6) + np.abs(throughput - shift2) / (shift2 + 1e-6)) / 2
    if num_nodes > 1:
        stress[0] = np.abs(throughput[0] - throughput[1]) / (throughput[1] + 1e-6)
        stress[-1] = np.abs(throughput[-1] - throughput[-2]) / (throughput[-2] + 1e-6)
    
    utility = alpha * throughput - beta * delays - gamma * risks - delta * stress
    
    # Local adaptation
    for i in np.where(failures == 1)[0]:
        throughput[i] *= 0.5
        if i > 0:
            throughput[i-1] += 0.2
        if i < num_nodes - 1:
            throughput[i+1] += 0.2
    
    jitter = np.std(utility)
    recovery = np.mean(delays)
    stability = np.var(utility)
    resilience = np.mean(utility > 0) * 100
    
    return jitter, recovery, stability, resilience

# Run Monte Carlo
cent_data = [centralized_simulation() for _ in range(num_simulations)]
frac_data = [fractal_simulation() for _ in range(num_simulations)]

cent_jitter, cent_recovery, cent_stability, cent_resilience = np.mean(cent_data, axis=0)
frac_jitter, frac_recovery, frac_stability, frac_resilience = np.mean(frac_data, axis=0)

print("Centralized Averages:")
print(f"Jitter: {cent_jitter:.4f}, Recovery: {cent_recovery:.4f}, Stability Var: {cent_stability:.4f}, Resilience: {cent_resilience:.2f}%")

print("\nFractal Averages:")
print(f"Jitter: {frac_jitter:.4f}, Recovery: {frac_recovery:.4f}, Stability Var: {frac_stability:.4f}, Resilience: {frac_resilience:.2f}%")

# Improvements
print("\nImprovements:")
print(f"Jitter Reduction: {((cent_jitter - frac_jitter) / cent_jitter * 100):.2f}%")
print(f"Recovery Reduction: {((cent_recovery - frac_recovery) / cent_recovery * 100):.2f}%")
print(f"Stability Improvement: {((cent_stability - frac_stability) / cent_stability * 100):.2f}%")
print(f"Resilience Improvement: {((frac_resilience - cent_resilience) / cent_resilience * 100):.2f}%")
