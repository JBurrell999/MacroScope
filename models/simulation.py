def run_simulation(scenario_name, inputs):
    # Mock simulation — later upgrade with real models
    inflation = max(0, 5 - 0.3 * inputs["Interest Rate"] + 0.002 * inputs["Fiscal Stimulus"])
    gdp = 1000 + 3 * inputs["Fiscal Stimulus"] - 15 * inputs["Interest Rate"]
    inequality = 40 + 0.1 * inputs["Minimum Wage"] - 0.05 * inputs["Corporate Tax Rate"]

    return {
        "GDP (billions)": gdp,
        "Inflation Rate (%)": inflation,
        "Gini Coefficient": inequality
    }
