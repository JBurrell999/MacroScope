import streamlit as st
import yaml
from models.simulation import run_simulation
from utils.openai_feedback import get_feedback

with open("config/scenarios.yaml") as f:
    scenarios = yaml.safe_load(f)

st.title("Civic Macroeconomics Lab")

scenario_names = [s['name'] for s in scenarios]
selected = st.selectbox("Select a Scenario", scenario_names)

scenario = next(s for s in scenarios if s["name"] == selected)
st.markdown(scenario["description"])

user_inputs = {}
for lever in scenario["levers"]:
    value = st.slider(
        f"{lever['name']} ({lever['unit']})",
        min_value=lever["min"],
        max_value=lever["max"],
        value=lever["default"]
    )
    user_inputs[lever["name"]] = value

if st.button("Simulate"):
    outputs = run_simulation(scenario["name"], user_inputs)
    st.subheader("📊 Economic Outcomes")
    for k, v in outputs.items():
        st.metric(label=k, value=round(v, 2))

    st.subheader("🧠 AI Feedback")
    st.write(get_feedback(scenario["name"], user_inputs, outputs))
