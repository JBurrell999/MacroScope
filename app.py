import streamlit as st
import yaml
import base64
import plotly.graph_objects as go
import openai
import os

# Load dynamic scenarios from YAML
with open("config/scenarios.yaml") as f:
    scenarios = yaml.safe_load(f)

st.set_page_config(page_title="Civic Macroeconomics Lab", layout="centered")

# Sidebar Help
with st.sidebar.expander("ℹ️ About this simulation"):
    st.write("""
    This interactive lab lets you explore economic tradeoffs in real-world policy scenarios.
    Adjust policy levers like interest rates, taxes, and spending. Simulate macroeconomic outcomes
    and receive AI-generated tradeoff feedback.
    """)

# Title & Scenario Selection
st.title("Civic Macroeconomics Lab")
scenario_names = [s['name'] for s in scenarios]
selected = st.selectbox("Choose a Scenario", scenario_names)
scenario = next(s for s in scenarios if s['name'] == selected)

st.markdown(scenario["description"])

# Dynamically Render Levers
user_inputs = {}
for lever in scenario["levers"]:
    value = st.slider(
        f"{lever['name']} ({lever['unit']})",
        min_value=lever["min"],
        max_value=lever["max"],
        value=lever["default"]
    )
    user_inputs[lever["name"]] = value

# Simulate Outputs
def run_simulation(scenario_name, inputs):
    # Simple mock model — upgrade to data-driven later
    gdp = 1000 + sum(inputs.values()) * 0.5
    inflation = max(1, 4 + 0.01 * inputs.get("Fiscal Stimulus", 0) - 0.25 * inputs.get("Interest Rate", 0))
    inequality = 40 + 0.1 * inputs.get("Minimum Wage", 0) - 0.05 * inputs.get("Corporate Tax Rate", 0)
    return {
        "GDP (billions)": gdp,
        "Inflation Rate (%)": inflation,
        "Gini Coefficient": inequality
    }

# LLM Feedback
def get_feedback(scenario, levers, outputs):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    lever_str = "\n".join([f"{k}: {v}" for k, v in levers.items()])
    outcome_str = "\n".join([f"{k}: {v:.2f}" for k, v in outputs.items()])
    prompt = f"""
You are an economic policy analyst. A student has just simulated the following:

Scenario: {scenario}

Policy Levers:
{lever_str}

Economic Outcomes:
{outcome_str}

Write a short analysis explaining the tradeoffs in their decision, focusing on inflation, inequality, and growth. Highlight equity implications.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )
    return response.choices[0].message.content

# Downloadable Report
def generate_report(scenario, inputs, outputs, feedback):
    report = f"### Scenario: {scenario}\n\n"
    report += "**Policy Levers:**\n" + "\n".join([f"- {k}: {v}" for k, v in inputs.items()]) + "\n\n"
    report += "**Outcomes:**\n" + "\n".join([f"- {k}: {round(v, 2)}" for k, v in outputs.items()]) + "\n\n"
    report += "**AI Feedback:**\n" + feedback
    return report

# Simulate button
if st.button("Simulate"):
    outputs = run_simulation(scenario["name"], user_inputs)

    # Show metrics
    st.subheader("📊 Economic Outcomes")
    for k, v in outputs.items():
        st.metric(label=k, value=round(v, 2))

    # Graph
    st.subheader("📈 Visualization")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(outputs.keys()),
        y=list(outputs.values()),
        marker_color=["green", "red", "blue"]
    ))
    st.plotly_chart(fig)

    # Feedback
    st.subheader("🧠 AI Feedback")
    feedback = get_feedback(scenario["name"], user_inputs, outputs)
    st.write(feedback)

    # Report
    report_txt = generate_report(scenario["name"], user_inputs, outputs, feedback)
    b64 = base64.b64encode(report_txt.encode()).decode()
    st.markdown(f'<a href="data:file/text;base64,{b64}" download="simulation_report.txt">📥 Download Your Report</a>', unsafe_allow_html=True)
