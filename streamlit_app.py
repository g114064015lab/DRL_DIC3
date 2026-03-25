import streamlit as st
import pandas as pd
import random
import math

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Multi-Armed Bandit Strategy Comparison",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (Quantum Flux Theme) ---
st.markdown("""
<style>
/* Base Theme */
body { background-color: #050b18; color: #e0e6ed; }
.main { background-color: #050b18; }
.stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: transparent; }
.stTabs [data-baseweb="tab"] { background-color: rgba(255,255,255,0.05); border-radius: 8px; padding: 10px 20px; border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; transition: all 0.3s; }
.stTabs [data-baseweb="tab"]:hover { border-color: #00f2ff; color: #00f2ff; }
.stTabs [aria-selected="true"] { background-color: #00f2ff !important; color: #000 !important; font-weight: 700 !important; }

/* Custom Headings */
h1 { font-family: 'Montserrat', sans-serif; font-size: 3.5rem !important; font-weight: 800; background: linear-gradient(135deg, #00f2ff 0%, #7000ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0.5rem; }
h2 { color: #00f2ff; font-family: 'Montserrat', sans-serif; }
.subtitle { text-align: center; color: #94a3b8; font-size: 1.25rem; margin-bottom: 3rem; }
.subtitle b { color: #00f2ff; }

/* Cards & Stats */
.metric-card { background: rgba(255,255,255,0.05); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 25px; text-align: center; transition: transform 0.3s; }
.metric-card:hover { transform: translateY(-5px); border-color: rgba(255,255,255,0.2); }
.metric-val { font-size: 2.5rem; font-weight: 700; font-family: 'Montserrat', sans-serif; line-height: 1; margin: 10px 0; }
.metric-label { font-size: 0.875rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }

/* SWOT Analysis */
.swot-box { padding: 20px; border-radius: 16px; height: 100%; }
.plus { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); }
.minus { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); }
.swot-title { font-weight: 700; display: block; margin-bottom: 10px; }

/* Discussion Section */
.stExpander { background-color: rgba(255,255,255,0.02) !important; border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# --- DATA REPRESENTATION ---
# Same data points as the JS version, representing a 10,000 budget summary
SUMMARY_DATA = [
    {"Method": "A/B Testing", "Style": "Static Split", "Reward": 7734, "Regret": 266, "Trend": [0, 400, 1400, 3000, 4600, 6200, 7800]},
    {"Method": "ε-Greedy", "Style": "Fixed Random", "Reward": 7866, "Regret": 134, "Trend": [0, 600, 1400, 3100, 4750, 6400, 7950]},
    {"Method": "Optimistic", "Style": "Implicit Early", "Reward": 7940, "Regret": 60, "Trend": [0, 500, 1500, 3150, 4850, 6500, 8050]},
    {"Method": "Softmax", "Style": "Probabilistic", "Reward": 7880, "Regret": 120, "Trend": [0, 550, 1450, 3120, 4800, 6450, 8000]},
    {"Method": "UCB", "Style": "Confidence-bound", "Reward": 7965, "Regret": 35, "Trend": [0, 700, 1550, 3180, 4900, 6550, 8100]},
    {"Method": "Thompson", "Style": "Bayesian", "Reward": 7980, "Regret": 20, "Trend": [0, 750, 1580, 3200, 4950, 6600, 8150]}
]

DETAIL_DATA = {
    "A/B Testing": {
        "exploration": "Fixed $2,000 budget split equally ($667 per arm).",
        "exploitation": "Remaining $8,000 spent entirely on the arm with the highest sample mean.",
        "pros": ["Simple to explain", "Stable results with large samples"],
        "cons": ["Inefficient budget allocation", "Not adaptive to early results"]
    },
    "ε-Greedy": {
        "exploration": "Fixed probability (ε=10%) to pull random arms.",
        "exploitation": "Picks best known arm 90% of the time.",
        "pros": ["Continuous learning", "Extremely robust baseline"],
        "cons": ["Explores bad arms forever", "Wasteful in the limit"]
    },
    "Optimistic": {
        "exploration": "Starts with estimates far above real values (e.g., Q=2.0).",
        "exploitation": "Greedy choice forces exploration due to initial disappointment.",
        "pros": ["Very fast convergence", "Zero specific exploration cost"],
        "cons": ["Values must be tuned carefully", "Fails if environment changes"]
    },
    "Softmax": {
        "exploration": "Probabilistic sampling based on relative performance.",
        "exploitation": "Better arms get exponentially more budget.",
        "pros": ["Smooth control with temperature τ", "Rank-aware exploration"],
        "cons": ["Sensitive to reward scale", "Hyperparameter tuning needed"]
    },
    "UCB": {
        "exploration": "Adds an 'uncertainty bonus' to arm estimates.",
        "exploitation": "Picks the arm with the highest optimistic potential.",
        "pros": ["Optimal regret theory", "Efficient confidence tracking"],
        "cons": ["Complex calculation", "Assumes stationary distributions"]
    },
    "Thompson": {
        "exploration": "Models every arm as a Bayesian Beta distribution.",
        "exploitation": "Stochastic sampling picks the most likely best arm.",
        "pros": ["Excellent real-world performance", "Handles sparse data well"],
        "cons": ["Computationally more expensive", "Requires Bayesian priors"]
    }
}

# --- HEADER ---
st.markdown("<h1>Multi-Armed Bandit Comparison</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Total Budget: <b>$10,000</b> | Bandit Arms: <b>A(0.8), B(0.7), C(0.5)</b></p>", unsafe_allow_html=True)

# --- TOP METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class='metric-card'><div class='metric-label'>Optimal Reward</div><div class='metric-val' style='color:#e0e6ed'>$8,000</div><div class='metric-label'>Perfect selection of Arm A</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class='metric-card'><div class='metric-label'>Best Strategy</div><div class='metric-val' style='color:#00f2ff'>$7,980</div><div class='metric-label'>Thompson Sampling</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class='metric-card'><div class='metric-label'>Least Regret</div><div class='metric-val' style='color:#7000ff'>$20</div><div class='metric-label'>Thompson Sampling</div></div>""", unsafe_allow_html=True)

st.write("---")

# --- PERFORMANCE CHART ---
st.subheader("Cumulative Reward Performance")
chart_df = pd.DataFrame({
    row["Method"]: row["Trend"] for row in SUMMARY_DATA
}, index=["$0", "$2k", "$4k", "$6k", "$8k", "$10k", "$12k"][:len(SUMMARY_DATA[0]["Trend"])]) # adjusted index to match trend length

st.line_chart(chart_df, height=450)

# --- STRATEGY TABS ---
st.subheader("Strategy Deep Dive")
tabs = st.tabs(list(DETAIL_DATA.keys()))

for i, (name, content) in enumerate(DETAIL_DATA.items()):
    with tabs[i]:
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.markdown(f"### {name}")
            st.write(f"**Exploration:** {content['exploration']}")
            st.write(f"**Exploitation:** {content['exploitation']}")
            
            st.write("")
            swot_col1, swot_col2 = st.columns(2)
            with swot_col1:
                pros_list = "".join([f"<li>{p}</li>" for p in content['pros']])
                st.markdown(f"<div class='swot-box plus'><span class='swot-title' style='color:#10b981'>✅ Strengths</span><ul>{pros_list}</ul></div>", unsafe_allow_html=True)
            with swot_col2:
                cons_list = "".join([f"<li>{c}</li>" for c in content['cons']])
                st.markdown(f"<div class='swot-box minus'><span class='swot-title' style='color:#ef4444'>⚠️ Weaknesses</span><ul>{cons_list}</ul></div>", unsafe_allow_html=True)
                
        with col_right:
            reward = next(r["Reward"] for r in SUMMARY_DATA if r["Method"] == name)
            regret = next(r["Regret"] for r in SUMMARY_DATA if r["Method"] == name)
            st.markdown(f"""<div class='metric-card' style='margin-bottom:10px'><div class='metric-label'>Final Reward</div><div class='metric-val'>${reward}</div></div>""", unsafe_allow_html=True)
            st.markdown(f"""<div class='metric-card'><div class='metric-label'>Total Regret</div><div class='metric-val' style='color:#ef4444'>${regret}</div></div>""", unsafe_allow_html=True)

# --- COMPARISON TABLE ---
st.write("---")
st.subheader("Class Comparison Table")
df_summary = pd.DataFrame(SUMMARY_DATA)[["Method", "Style", "Reward", "Regret"]]
st.table(df_summary)

# --- DISCUSSION ---
st.subheader("Instructor Insights")
with st.expander("Which method performed best? Why?"):
    st.write("Thompson Sampling and UCB. They are adaptive—balancing exploration and exploitation based on real-time feedback.")

with st.expander("Which method wastes the most budget?"):
    st.write("A/B Testing. It forces exploration on ALL arms (including the 0.5 arm) regardless of early data.")

with st.expander("Why is A/B testing not adaptive?"):
    st.write("Because it splits into fixed phases. It doesn't use the 'pulled' data to influence current allocation until the test is over.")

with st.expander("Usage: Ads system vs Clinical trial?"):
    st.write("Ads systems use Thompson (scale/speed); Clinical trials use UCB (guaranteed worst-case bounds/ethics).")

# --- FOOTER ---
st.write("---")
st.caption("Developed by Antigravity AI for DRL_DIC3 Academy")
