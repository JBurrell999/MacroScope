import openai
import os

openai.api_key = os.getenv("x")

def get_feedback(scenario, levers, outputs):
    lever_str = "\n".join([f"{k}: {v}" for k, v in levers.items()])
    outcome_str = "\n".join([f"{k}: {v:.2f}" for k, v in outputs.items()])

    prompt = f"""
You are an economic policy analyst. A student has just simulated the following:

Scenario: {scenario}

Policy Levers:
{lever_str}

Economic Outcomes:
{outcome_str}

Write a short 4-5 sentence analysis explaining the tradeoffs in their decision, focusing on inflation, inequality, and growth. Highlight equity implications.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )
    return response.choices[0].message.content
