const strategyData = {
    ab: {
        title: "A/B Testing (Static)",
        exploration: "Fixed $2,000 budget split equally ($667 per arm).",
        exploitation: "Remaining $8,000 spent entirely on the arm with the highest sample mean.",
        expectedReward: 7734,
        regret: 266,
        strengths: ["Simple to explain", "Stable results with large samples"],
        weaknesses: ["Inefficient budget allocation", "Not adaptive to early results"],
        notes: "The 'Golden Standard' in traditional research, but often wasteful in dynamic digital environments."
    },
    epsilon: {
        title: "ε-Greedy (Random)",
        exploration: "Explores random arms with a fixed probability (e.g., ε=10%).",
        exploitation: "Always chooses the current best arm 90% of the time.",
        expectedReward: 7866,
        regret: 134,
        strengths: ["Easy to implement", "Guarantees continuous exploration"],
        weaknesses: ["Explores 'bad' arms forever", "Wasteful once the best arm is known"],
        notes: "A robust baseline that is much more efficient than pure A/B testing."
    },
    optimistic: {
        title: "Optimistic Initial Values",
        exploration: "Starts with very high reward estimates (e.g., 2.0).",
        exploitation: "Always picks the arm with the best estimate.",
        expectedReward: 7940,
        regret: 60,
        strengths: ["Fast initial discovery", "Converges quickly"],
        weaknesses: ["Needs careful tuning of initial values", "Hard to adapt if environment changes late"],
        notes: "Encourages exploring every arm at least once because real results will almost always 'disappoint' the high initial estimate."
    },
    softmax: {
        title: "Softmax (Boltzmann)",
        exploration: "Probabilistic. Better arms are explored more often.",
        exploitation: "Smoothly shifts toward the best arm as confidence grows.",
        expectedReward: 7880,
        regret: 120,
        strengths: ["Avoids wasting too much on obviously bad arms", "Controllable randomness"],
        weaknesses: ["Requires tuning the temperature (τ) parameter", "Sensitive to reward scale"],
        notes: "A more refined version of ε-greedy that uses 'Rank-based' or 'Value-based' probabilities."
    },
    ucb: {
        title: "Upper Confidence Bound (UCB)",
        exploration: "Uses uncertainty intervals. Explores arms we are 'unsure' about.",
        exploitation: "Picks the arm with the highest 'Optimistic Potential' (Average + Uncertainty).",
        expectedReward: 7965,
        regret: 35,
        strengths: ["Highly efficient", "Theoretically optimal regret growth"],
        weaknesses: ["Harder to calculate", "Assumes stationary distributions"],
        notes: "The standard for high-performance ML systems where every cent counts."
    },
    thompson: {
        title: "Thompson Sampling (Bayesian)",
        exploration: "Models each arm as a probability distribution (Beta).",
        exploitation: "Samples from each distribution and picks the highest sample.",
        expectedReward: 7980,
        regret: 20,
        strengths: ["Excellent performance in practice", "Handles sparse data well"],
        weaknesses: ["Computationally more complex (Gamma/Beta functions)", "Requires Bayesian priors"],
        notes: "Often wins in real-world scenarios like Google Ads or Amazon recommendations."
    }
};

const fullTableData = [
    { name: "A/B Test", style: "Static Split", reward: 7734, regret: 266, trend: [0, 400, 1400, 3000, 4600, 6200, 7800] },
    { name: "ε-Greedy", style: "Fixed Random", reward: 7866, regret: 134, trend: [0, 600, 1400, 3100, 4750, 6400, 7950] },
    { name: "Optimistic", style: "Implicit Early", reward: 7940, regret: 60, trend: [0, 500, 1500, 3150, 4850, 6500, 8050] },
    { name: "Softmax", style: "Probabilistic", reward: 7880, regret: 120, trend: [0, 550, 1450, 3120, 4800, 6450, 8000] },
    { name: "UCB", style: "Confidence-based", reward: 7965, regret: 35, trend: [0, 700, 1550, 3180, 4900, 6550, 8100] },
    { name: "Thompson", style: "Bayesian Sampling", reward: 7980, regret: 20, trend: [0, 750, 1580, 3200, 4950, 6600, 8150] }
];

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initTable();
    initChart();
    initAccordion();
});

function initAccordion() {
    const items = document.querySelectorAll('.item');
    items.forEach(item => {
        const header = item.querySelector('.accordion-header');
        header.addEventListener('click', () => {
            const isOpen = item.classList.contains('open');
            items.forEach(i => i.classList.remove('open'));
            if (!isOpen) item.classList.add('open');
        });
    });
}

function initTabs() {
    const strategyContent = document.getElementById('strategyContent');
    const tabBtns = document.querySelectorAll('.tab-btn');

    function renderTab(key) {
        const data = strategyData[key];
        strategyContent.innerHTML = `
            <div class="strategy-detail-card">
                <h3>${data.title}</h3>
                <div class="row">
                    <div class="col">
                        <h4>Allocation Strategy</h4>
                        <p><strong>Exploration:</strong> ${data.exploration}</p>
                        <p><strong>Exploitation:</strong> ${data.exploitation}</p>
                    </div>
                    <div class="col stats">
                        <div class="stat-mini"><span>Expected Reward:</span> $${data.expectedReward}</div>
                        <div class="stat-mini regret"><span>Regret:</span> $${data.regret}</div>
                    </div>
                </div>
                <div class="swot">
                    <div class="box plus">
                        <strong>Strengths:</strong>
                        <ul>${data.strengths.map(s => `<li>${s}</li>`).join('')}</ul>
                    </div>
                    <div class="box minus">
                        <strong>Weaknesses:</strong>
                        <ul>${data.weaknesses.map(w => `<li>${w}</li>`).join('')}</ul>
                    </div>
                </div>
                <p class="notes"><em>Note: ${data.notes}</em></p>
            </div>
        `;
    }

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderTab(btn.dataset.tab);
        });
    });

    renderTab('ab');
}

function initTable() {
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = fullTableData.map(d => `
        <tr>
            <td><strong>${d.name}</strong></td>
            <td>${d.style}</td>
            <td style="color: var(--primary)">$${d.reward}</td>
            <td style="color: var(--error)">$${d.regret}</td>
            <td>${getEfficiency(d.regret)}</td>
        </tr>
    `).join('');
}

function getEfficiency(regret) {
    if (regret < 50) return '<span style="color: var(--success)">High</span>';
    if (regret < 150) return '<span style="color: var(--warning)">Medium</span>';
    return '<span style="color: var(--error)">Low</span>';
}

function initChart() {
    const ctx = document.getElementById('performanceChart').getContext('2d');
    const labels = ['$0', '$2,000', '$4,000', '$6,000', '$8,000', '$10,000'];
    
    // Scaling trends for budget levels
    const steps = [0, 2000, 4000, 6000, 8000, 10000];
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: fullTableData.map((d, i) => ({
                label: d.name,
                data: d.trend,
                borderColor: getNeonColor(i),
                backgroundColor: 'transparent',
                tension: 0.3,
                borderWidth: 3,
                pointRadius: 4
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top', labels: { color: '#94a3b8' } }
            },
            scales: {
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
            }
        }
    });
}

function getNeonColor(index) {
    const colors = ['#00f2ff', '#7000ff', '#ff007a', '#f59e0b', '#10b981', '#3b82f6'];
    return colors[index % colors.length];
}
