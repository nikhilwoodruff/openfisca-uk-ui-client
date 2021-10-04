from policy_engine_uk.populations.metrics import poverty_rate, pct_change
from policy_engine_uk.utils.charts import *
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from openfisca_uk import Microsimulation
import pandas as pd


def decile_chart(baseline: Microsimulation, reformed: Microsimulation) -> dict:
    income = baseline.calc("household_net_income", map_to="person")
    equiv_income = baseline.calc("equiv_household_net_income", map_to="person")
    gain = reformed.calc("household_net_income", map_to="person") - income
    changes = (
        gain.groupby(equiv_income.decile_rank()).sum()
        / income.groupby(equiv_income.decile_rank()).sum()
    )
    df = pd.DataFrame({"Decile": changes.index, "Change": changes.values})
    fig = (
        px.bar(df, x="Decile", y="Change")
        .update_layout(
            title="Change to net income by decile",
            xaxis_title="Equivalised disposable income decile",
            yaxis_title="Percentage change",
            yaxis_tickformat="%",
            showlegend=False,
            xaxis_tickvals=list(range(1, 11)),
        )
        .update_traces(marker_color=BLUE)
    )
    add_zero_line(fig)
    return format_fig(fig)


def pov_chg(
    baseline: Microsimulation, reform: Microsimulation, criterion: str
) -> float:
    return pct_change(
        poverty_rate(baseline, criterion), poverty_rate(reform, criterion)
    )


def poverty_chart(baseline: Microsimulation, reform: Microsimulation) -> dict:
    df = pd.DataFrame(
        {
            "group": ["Child", "Working-age", "Senior", "All"],
            "pov_chg": [
                pov_chg(baseline, reform, i)
                for i in ["is_child", "is_WA_adult", "is_SP_age", "people"]
            ],
        }
    )
    df["abs_chg_str"] = df.pov_chg.abs().map("{:.1%}".format)
    df["label"] = (
        np.where(df.group == "All", "Total", df.group)
        + " poverty "
        + np.where(
            df.abs_chg_str == "0.0%",
            "does not change",
            (np.where(df.pov_chg < 0, "falls ", "rises ") + df.abs_chg_str),
        )
    )
    fig = px.bar(
        df,
        x="group",
        y="pov_chg",
        custom_data=["label"],
        labels={"group": "Group", "pov_chg": "Poverty rate change"},
    )
    fig.update_layout(
        title="Poverty impact by age",
        xaxis_title=None,
        yaxis=dict(title="Percent change", tickformat="%"),
    )
    fig.update_traces(
        marker_color=BLUE, hovertemplate="%{customdata[0]}<extra></extra>"
    )
    add_zero_line(fig)
    return format_fig(fig)


def spending(baseline: Microsimulation, reformed: Microsimulation) -> float:
    return (
        reformed.calc("net_income").sum() - baseline.calc("net_income").sum()
    )


def get_partial_funding(
    reform: Microsimulation, baseline: Microsimulation, **kwargs
) -> list:
    expenditure = []
    for i in range(1, len(reform) + 1):
        expenditure += [
            spending(baseline, Microsimulation(reform[:i], **kwargs))
        ]
    return expenditure


def total_income(sim: Microsimulation) -> float:
    return sim.calc("net_income").sum()


def population_waterfall_chart(
    baseline: Microsimulation, reformed: Microsimulation
) -> dict:
    return waterfall_chart(baseline, reformed)


NAMES = (
    "Gain more than 5%",
    "Gain less than 5%",
    "No change",
    "Lose less than 5%",
    "Lose more than 5%",
)


def intra_decile_graph_data(
    baseline: Microsimulation, reformed: Microsimulation
) -> pd.DataFrame:
    l = []
    income = baseline.calc("equiv_household_net_income", map_to="person")
    decile = income.decile_rank()
    baseline_hh_net_income = baseline.calc(
        "household_net_income", map_to="person"
    )
    reformed_hh_net_income = reformed.calc(
        "household_net_income", map_to="person"
    )
    gain = reformed_hh_net_income - baseline_hh_net_income
    rel_gain = (gain / baseline_hh_net_income).dropna()
    bands = (None, 0.05, 1e-3, -1e-3, -0.05, None)
    for upper, lower, name in zip(bands[:-1], bands[1:], NAMES):
        fractions = []
        for j in range(1, 11):
            subset = rel_gain[decile == j]
            if lower is not None:
                subset = subset[rel_gain > lower]
            if upper is not None:
                subset = subset[rel_gain <= upper]
            fractions += [subset.count() / rel_gain[decile == j].count()]
        tmp = pd.DataFrame(
            {
                "fraction": fractions,
                "decile": list(map(str, range(1, 11))),
                "outcome": name,
            }
        )
        l.append(tmp)
        subset = rel_gain
        if lower is not None:
            subset = subset[rel_gain > lower]
        if upper is not None:
            subset = subset[rel_gain <= upper]
        all_row = pd.DataFrame(
            {
                "fraction": [subset.count() / rel_gain.count()],
                "decile": "All",
                "outcome": name,
            }
        )
        l.append(all_row)
    return pd.concat(l).reset_index()


INTRA_DECILE_COLORS = (
    DARK_GRAY,
    GRAY,
    LIGHT_GRAY,
    LIGHT_GREEN,
    DARK_GREEN,
)[::-1]


def intra_decile_label(fraction, decile, outcome):
    res = "{:.0%}".format(fraction) + " of "  # x% of
    if decile == "All":
        res += "all people "
    else:
        res += "people in the " + ordinal(int(decile)) + " decile "
    if outcome == "No change":
        return res + "experience no change"
    else:
        return res + outcome.lower()


def single_intra_decile_graph(df):
    return px.bar(
        df,
        x="fraction",
        y="decile",
        color="outcome",
        custom_data=["hover"],
        color_discrete_sequence=INTRA_DECILE_COLORS,
        orientation="h",
    ).update_traces(hovertemplate="%{customdata[0]}<extra></extra>")


def intra_decile_chart(
    baseline: Microsimulation, reformed: Microsimulation
) -> dict:
    df = intra_decile_graph_data(baseline, reformed)
    df["hover"] = df.apply(
        lambda x: intra_decile_label(x.fraction, x.decile, x.outcome), axis=1
    )
    # Create the decile figure first, then the total to go above it.
    decile_fig = single_intra_decile_graph(df[df.decile != "All"])
    total_fig = single_intra_decile_graph(df[df.decile == "All"])
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[1, 10],
        vertical_spacing=0.05,
        x_title="Population share",
        y_title="Income decile",
    )
    fig.update_xaxes(showgrid=False)
    fig.add_traces(total_fig.data, 1, 1)
    fig.add_traces(decile_fig.data, 2, 1)
    fig.update_layout(
        barmode="stack",
        title="Distribution of gains and losses",
    )
    fig.update_xaxes(tickformat="%")
    for i in range(5):
        fig.data[i].showlegend = False
    return format_fig(fig)
