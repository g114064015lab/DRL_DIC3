# 🎯 Multi-Armed Bandit Strategy Comparison Dashboard

A comprehensive exploration-exploitation analysis comparing 6 fundamental bandit strategies over a $10,000 budget. This project includes both a **Streamlit Python Application** and a **Premium Static HTML Dashboard**.

## 🧩 Problem Setup
The simulation evaluates 3 bandit arms with the following true reward means:
- **Arm A**: 0.8 (Optimal)
- **Arm B**: 0.7
- **Arm C**: 0.5

**Total Budget**: $10,000

## 🧠 Strategies Analyzed
1.  **A/B Testing**: Static exploration phase ($2,000 split) followed by decision.
2.  **$\epsilon$-Greedy**: Random exploration with a fixed 10% probability.
3.  **Optimistic Initial Values**: Fast discovery through high initial reward estimates.
4.  **Softmax (Boltzmann)**: Probabilistic sampling based on relative arm performance.
5.  **UCB (Upper Confidence Bound)**: Confidence-interval tracking for optimal regret.
6.  **Thompson Sampling**: Bayesian modeling using Beta distributions.

## 📊 Performance Summary ($10k Budget)
| Method | Exploration Style | Expected Reward | Regret | Efficiency |
| :--- | :--- | :--- | :--- | :--- |
| **A/B Testing** | Static Split | $7,734 | $266 | Low |
| **$\epsilon$-Greedy** | Random | $7,866 | $134 | Medium |
| **Optimistic** | Implicit Early | $7,940 | $60 | High |
| **Softmax** | Probabilistic | $7,880 | $120 | Medium |
| **UCB** | Confidence-bound | $7,965 | $35 | Very High |
| **Thompson** | Bayesian | $7,980 | $20 | Best |

---

## 🚀 How to Run (Streamlit)
To run the professional Python dashboard locally:

1.  Clone the repository:
    ```bash
    git clone https://github.com/g114064015lab/DRL_DIC3.git
    cd DRL_DIC3
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Launch Streamlit:
    ```bash
    streamlit run streamlit_app.py
    ```

## 🌐 How to Use (Static Dashboard)
If you prefer a standalone experience or a static presentation:
1.  Open `index.html` in any web browser.
2.  Explore the "Quantum Flux" theme with neon accents and glassmorphism.
3.  Use the interactive tabs for strategy deep-dives.

---

## 🛠️ Tech Stack
-   **Backend/Deployment**: Python, Streamlit, Pandas, NumPy.
*   **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JavaScript, Chart.js.
*   **Version Control**: Git / GitHub.

Developed by **g114064015** for the DRL_DIC3 Academy.
