import random
import math

# Bandit Arms (True Means)
means = {'A': 0.8, 'B': 0.7, 'C': 0.5}
arms = list(means.keys())
budget = 10000

# Simulation Parameters
num_runs = 50 

def run_simulation():
    results = {}

    # 1. A/B Testing
    def ab_test():
        exploration_budget = 2000
        decision_budget = 8000
        # Exploration
        trials_per_arm = exploration_budget // 3
        rewards = {arm: 0 for arm in arms}
        for arm in arms:
            for _ in range(trials_per_arm):
                if random.random() < means[arm]:
                    rewards[arm] += 1
        
        counts = {arm: trials_per_arm for arm in arms}
        winner = max(arms, key=lambda a: rewards[a] / (counts[a] or 1))
        
        # Decision
        decision_reward = sum(1 for _ in range(decision_budget) if random.random() < means[winner])
        total_reward = sum(rewards.values()) + decision_reward
        return total_reward

    # 2. ε-Greedy (ε=0.1)
    def epsilon_greedy(epsilon=0.1):
        rewards_sum = {arm: 0 for arm in arms}
        counts = {arm: 0 for arm in arms}
        total_reward = 0
        for _ in range(budget):
            if random.random() < epsilon:
                arm = random.choice(arms)
            else:
                q_values = {a: (rewards_sum[a] / counts[a]) if counts[a] > 0 else 1.0 for a in arms}
                arm = max(arms, key=lambda a: q_values[a])
            
            reward = 1 if random.random() < means[arm] else 0
            rewards_sum[arm] += reward
            counts[arm] += 1
            total_reward += reward
        return total_reward

    # 3. Optimistic Initial Values (OIV=2.0)
    def optimistic_initial_values(initial_q=2.0):
        rewards_sum = {arm: 0 for arm in arms}
        counts = {arm: 0 for arm in arms}
        total_reward = 0
        q_values = {arm: initial_q for arm in arms}
        for _ in range(budget):
            arm = max(arms, key=lambda a: q_values[a])
            reward = 1 if random.random() < means[arm] else 0
            rewards_sum[arm] += reward
            counts[arm] += 1
            q_values[arm] = (rewards_sum[arm] + initial_q) / (counts[arm] + 1) # simple update
            total_reward += reward
        return total_reward

    # 4. Softmax (τ=0.1)
    def softmax(tau=0.1):
        rewards_sum = {arm: 0 for arm in arms}
        counts = {arm: 1 for arm in arms} 
        total_reward = 0
        for _ in range(budget):
            q_values = [rewards_sum[a] / counts[a] for a in arms]
            exp_q = [math.exp(q / tau) for q in q_values]
            sum_exp = sum(exp_q)
            probs = [e / sum_exp for e in exp_q]
            
            r = random.random()
            acc = 0
            arm = arms[-1]
            for i, p in enumerate(probs):
                acc += p
                if r < acc:
                    arm = arms[i]
                    break
            
            reward = 1 if random.random() < means[arm] else 0
            rewards_sum[arm] += reward
            counts[arm] += 1
            total_reward += reward
        return total_reward

    # 5. UCB1
    def ucb():
        rewards_sum = {arm: 0 for arm in arms}
        counts = {arm: 0 for arm in arms}
        total_reward = 0
        for arm in arms:
            reward = 1 if random.random() < means[arm] else 0
            rewards_sum[arm] += reward
            counts[arm] += 1
            total_reward += reward
            
        for t in range(len(arms), budget):
            q_values = {a: (rewards_sum[a] / counts[a]) + math.sqrt(2 * math.log(t) / counts[a]) for a in arms}
            arm = max(arms, key=lambda a: q_values[a])
            reward = 1 if random.random() < means[arm] else 0
            rewards_sum[arm] += reward
            counts[arm] += 1
            total_reward += reward
        return total_reward

    # Thompson Sampling simplified using Beta sampling via random.betavariate
    def thompson():
        successes = {arm: 1 for arm in arms}
        failures = {arm: 1 for arm in arms}
        total_reward = 0
        for _ in range(budget):
            samples = {a: random.betavariate(successes[a], failures[a]) for a in arms}
            arm = max(arms, key=lambda a: samples[a])
            reward = 1 if random.random() < means[arm] else 0
            successes[arm] += reward
            failures[arm] += (1 - reward)
            total_reward += reward
        return total_reward

    sims = {
        'A/B Test': ab_test,
        'ε-Greedy': epsilon_greedy,
        'Optimistic': optimistic_initial_values,
        'Softmax': softmax,
        'UCB': ucb,
        'Thompson': thompson
    }

    results = {name: [] for name in sims}
    for _ in range(num_runs):
        for name, func in sims.items():
            results[name].append(func())

    summary = {}
    optimal_reward = 8000 # 10000 * 0.8
    for name, r_list in results.items():
        avg_reward = sum(r_list) / len(r_list)
        summary[name] = {
            'Avg Reward': round(avg_reward, 2),
            'Regret': round(optimal_reward - avg_reward, 2)
        }
    
    return summary

if __name__ == "__main__":
    print(run_simulation())

