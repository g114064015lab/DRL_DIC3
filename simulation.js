const math = Math;

const means = { A: 0.8, B: 0.7, C: 0.5 };
const arms = ['A', 'B', 'C'];
const budget = 10000;
const numRuns = 10;

function randomBeta(alpha, beta) {
    // Basic approximation of Beta sampling using Gamma sampling
    // Or just use a simple rejection sampler for small alpha, beta
    // For Thompson sampling in class, we can just use a simpler model or assume these libraries exist.
    // Let's implement a simple approximation for Beta since we only have successes/failures.
    function gamma(alpha) {
        let res = 0;
        for (let i = 0; i < alpha; i++) {
            res += -math.log(math.random());
        }
        return res;
    }
    const x = gamma(alpha);
    const y = gamma(beta);
    return x / (x + y);
}

function simulate() {
    const sims = {
        'A/B Test': () => {
            const expBudget = 2000;
            const decBudget = 8000;
            const trialsPerArm = math.floor(expBudget / 3);
            let rewards = { A: 0, B: 0, C: 0 };
            for (let arm of arms) {
                for (let i = 0; i < trialsPerArm; i++) {
                    if (math.random() < means[arm]) rewards[arm]++;
                }
            }
            const winner = arms.reduce((a, b) => (rewards[a] / trialsPerArm >= rewards[b] / trialsPerArm ? a : b));
            let decReward = 0;
            for (let i = 0; i < decBudget; i++) {
                if (math.random() < means[winner]) decReward++;
            }
            return Object.values(rewards).reduce((s, r) => s + r, 0) + decReward;
        },
        'ε-Greedy': () => {
            const epsilon = 0.1;
            let rewardsSum = { A: 0, B: 0, C: 0 };
            let counts = { A: 0, B: 0, C: 0 };
            let total = 0;
            for (let t = 0; t < budget; t++) {
                let arm;
                if (math.random() < epsilon) {
                    arm = arms[math.floor(math.random() * arms.length)];
                } else {
                    arm = arms.reduce((a, b) => {
                        let qa = counts[a] > 0 ? rewardsSum[a] / counts[a] : 1.0;
                        let qb = counts[b] > 0 ? rewardsSum[b] / counts[b] : 1.0;
                        return qa >= qb ? a : b;
                    });
                }
                const reward = math.random() < means[arm] ? 1 : 0;
                rewardsSum[arm] += reward;
                counts[arm]++;
                total += reward;
            }
            return total;
        },
        'Optimistic': () => {
            const initialQ = 2.0;
            let rewardsSum = { A: 0, B: 0, C: 0 };
            let counts = { A: 0, B: 0, C: 0 };
            let total = 0;
            let qValues = { A: initialQ, B: initialQ, C: initialQ };
            for (let t = 0; t < budget; t++) {
                const arm = arms.reduce((a, b) => (qValues[a] >= qValues[b] ? a : b));
                const reward = math.random() < means[arm] ? 1 : 0;
                rewardsSum[arm] += reward;
                counts[arm]++;
                qValues[arm] = (rewardsSum[arm] + initialQ) / (counts[arm] + 1);
                total += reward;
            }
            return total;
        },
        'Softmax': () => {
            const tau = 0.1;
            let rewardsSum = { A: 0, B: 0, C: 0 };
            let counts = { A: 1, B: 1, C: 1 };
            let total = 0;
            for (let t = 0; t < budget; t++) {
                let expQs = arms.map(a => math.exp((rewardsSum[a] / counts[a]) / tau));
                let sumExp = expQs.reduce((s, e) => s + e, 0);
                let probs = expQs.map(e => e / sumExp);
                let r = math.random();
                let acc = 0;
                let arm = arms[arms.length - 1];
                for (let i = 0; i < probs.length; i++) {
                    acc += probs[i];
                    if (r < acc) {
                        arm = arms[i];
                        break;
                    }
                }
                const reward = math.random() < means[arm] ? 1 : 0;
                rewardsSum[arm] += reward;
                counts[arm]++;
                total += reward;
            }
            return total;
        },
        'UCB': () => {
            let rewardsSum = { A: 0, B: 0, C: 0 };
            let counts = { A: 0, B: 0, C: 0 };
            let total = 0;
            for (let arm of arms) {
                const reward = math.random() < means[arm] ? 1 : 0;
                rewardsSum[arm] += reward;
                counts[arm]++;
                total += reward;
            }
            for (let t = arms.length; t < budget; t++) {
                const arm = arms.reduce((a, b) => {
                    let ua = (rewardsSum[a] / counts[a]) + math.sqrt(2 * math.log(t) / counts[a]);
                    let ub = (rewardsSum[b] / counts[b]) + math.sqrt(2 * math.log(t) / counts[b]);
                    return ua >= ub ? a : b;
                });
                const reward = math.random() < means[arm] ? 1 : 0;
                rewardsSum[arm] += reward;
                counts[arm]++;
                total += reward;
            }
            return total;
        },
        'Thompson': () => {
            let successes = { A: 1, B: 1, C: 1 };
            let failures = { A: 1, B: 1, C: 1 };
            let total = 0;
            for (let t = 0; t < budget; t++) {
                const arm = arms.reduce((a, b) => {
                    let sa = randomBeta(successes[a], failures[a]);
                    let sb = randomBeta(successes[b], failures[b]);
                    return sa >= sb ? a : b;
                });
                const reward = math.random() < means[arm] ? 1 : 0;
                if (reward) successes[arm]++; else failures[arm]++;
                total += reward;
            }
            return total;
        }
    };

    let summary = {};
    const optimalReward = 8000;
    for (let [name, func] of Object.entries(sims)) {
        let rewards = [];
        for (let i = 0; i < numRuns; i++) rewards.push(func());
        let avg = rewards.reduce((s, r) => s + r, 0) / numRuns;
        summary[name] = {
            avgReward: avg.toFixed(2),
            regret: (optimalReward - avg).toFixed(2)
        };
    }
    console.log(JSON.stringify(summary, null, 2));
}

simulate();
