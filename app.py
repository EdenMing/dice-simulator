# Dice Map Completion Simulator Streamlit App
# Filename: app.py
# 
# 1. GitHub Setup:
#    - Initialize local repo: `git init`
#    - Create .gitignore (e.g., ignore __pycache__, .streamlit/, *.pyc)
#    - Add files: `git add app.py`
#    - Commit: `git commit -m "Initial commit: dice map simulator app"`
#    - Create GitHub repo (via web or gh CLI): `gh repo create your-username/dice-map-sim --public`
#    - Push: `git push -u origin main`
#    - Enable Github Actions or connect to Streamlit Cloud if desired.

import streamlit as st
import numpy as np
import pandas as pd
import io

st.set_page_config(page_title="Dice Map Simulator", layout="centered")
st.title("Dice Map Completion Simulator")

# Sidebar inputs
st.sidebar.header("Simulation Parameters")
dice_count = st.sidebar.number_input("Number of dice", min_value=1, value=1)
faces = st.sidebar.number_input("Faces per die", min_value=2, value=6)
blocks = st.sidebar.number_input("Number of blocks on map", min_value=2, value=10)
simulations = st.sidebar.number_input("Number of simulations", min_value=100, value=10000)

# Run simulation
if st.sidebar.button("Run Simulation"):
    steps_list = []
    for _ in range(simulations):
        visited = set()
        pos = 0
        steps = 0
        while len(visited) < blocks:
            # roll all dice
            roll = sum(np.random.randint(1, faces+1, size=dice_count))
            pos = (pos + roll) % blocks
            visited.add(pos)
            steps += 1
        steps_list.append(steps)

    # Convert to DataFrame
    df_steps = pd.DataFrame({"steps": steps_list})
    st.subheader("Raw Steps per Simulation")
    st.dataframe(df_steps)

    # Download raw data
    buf_raw = io.BytesIO()
    df_steps.to_csv(buf_raw, index=False)
    buf_raw.seek(0)
    st.download_button("Download raw steps CSV", buf_raw, "raw_steps.csv")

    # Distribution: probability of completion at each step count
    dist = df_steps["steps"].value_counts().sort_index()
    df_dist = pd.DataFrame({"steps": dist.index, "probability": dist.values / simulations})
    st.subheader("Completion Probability by Steps")
    st.dataframe(df_dist)

    # Cumulative probability
    df_dist["cumulative"] = df_dist["probability"].cumsum()
    st.write("_Cumulative probability of completion by step_")
    st.dataframe(df_dist)

    # Download distribution
    buf_dist = io.BytesIO()
    df_dist.to_csv(buf_dist, index=False)
    buf_dist.seek(0)
    st.download_button("Download distribution CSV", buf_dist, "distribution.csv")

else:
    st.info("Adjust parameters in the sidebar and click 'Run Simulation'.")
