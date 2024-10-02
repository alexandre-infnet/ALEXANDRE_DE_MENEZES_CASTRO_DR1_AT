import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch
import pandas as pd


def plot_pass_map(events, selected_match):
    passes = events[events["type"] == "Pass"]
    pitch = Pitch(
        pitch_type="statsbomb", line_zorder=2, pitch_color="grass", line_color="white"
    )
    fig, ax = pitch.draw(figsize=(10, 7))

    for i, row in passes.iterrows():
        if isinstance(row["location"], list) and isinstance(
            row["pass_end_location"], list
        ):
            pitch.arrows(
                row["location"][0],
                row["location"][1],
                row["pass_end_location"][0],
                row["pass_end_location"][1],
                width=2,
                headwidth=3,
                color="blue",
                ax=ax,
            )

    ax.set_title(f"Mapa de Passes: {selected_match}", fontsize=20)
    st.pyplot(fig)


def plot_shot_map(events, selected_match):
    shots = events[events["type"] == "Shot"]
    pitch = Pitch(
        pitch_type="statsbomb", line_zorder=2, pitch_color="grass", line_color="white"
    )
    fig, ax = pitch.draw(figsize=(10, 7))

    for i, row in shots.iterrows():
        if isinstance(row["location"], list):
            color = "red" if row["shot_outcome"] == "Goal" else "blue"
            pitch.scatter(
                row["location"][0], row["location"][1], color=color, s=100, ax=ax
            )

    ax.set_title(f"Mapa de Chutes: {selected_match}", fontsize=20)
    st.pyplot(fig)


def plot_passes_vs_goals(events):
    passes = events[events["type"] == "Pass"]
    shots = events[events["type"] == "Shot"]

    passes_per_player = passes.groupby("player").size().reset_index(name="num_passes")
    goals_per_player = (
        shots[shots["shot_outcome"] == "Goal"]
        .groupby("player")
        .size()
        .reset_index(name="num_goals")
    )

    passes_goals = pd.merge(
        passes_per_player, goals_per_player, on="player", how="left"
    ).fillna(0)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=passes_goals, x="num_passes", y="num_goals", hue="player", ax=ax, s=100
    )
    ax.set_title("Relação entre Número de Passes e Gols por Jogador", fontsize=16)
    ax.set_xlabel("Número de Passes", fontsize=12)
    ax.set_ylabel("Número de Gols", fontsize=12)
    st.pyplot(fig)


def plot_shots_distribution(events):
    shots = events[events["type"] == "Shot"]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=shots, x="player", y="minute", ax=ax)
    ax.set_title("Distribuição dos Chutes por Jogador (Minuto do Jogo)", fontsize=16)
    ax.set_xlabel("Jogador", fontsize=12)
    ax.set_ylabel("Minuto do Jogo", fontsize=12)
    ax.tick_params(axis="x", rotation=90)
    st.pyplot(fig)


def plot_correlation(events):
    passes = events[events["type"] == "Pass"]
    shots = events[events["type"] == "Shot"]

    passes_per_player = passes.groupby("player").size().reset_index(name="num_passes")
    goals_per_player = (
        shots[shots["shot_outcome"] == "Goal"]
        .groupby("player")
        .size()
        .reset_index(name="num_goals")
    )

    passes_goals = pd.merge(
        passes_per_player, goals_per_player, on="player", how="left"
    ).fillna(0)

    stats_corr = passes_goals[["num_passes", "num_goals"]].corr()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(stats_corr, annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Correlação entre Passes e Gols", fontsize=16)
    st.pyplot(fig)


def plot_pressure_map(events, selected_match):
    pressure = events[events["type"] == "Pressure"]
    pitch = Pitch(
        pitch_type="statsbomb", line_zorder=2, pitch_color="grass", line_color="white"
    )
    fig, ax = pitch.draw(figsize=(10, 7))

    if not pressure.empty:
        bin_statistic = pitch.bin_statistic(
            pressure["location"].apply(lambda x: x[0]),
            pressure["location"].apply(lambda x: x[1]),
            statistic="count",
            bins=(10, 10),
        )
        pitch.heatmap(bin_statistic, ax=ax, cmap="coolwarm", edgecolors="grey")

    ax.set_title(f"Mapa de Pressão: {selected_match}", fontsize=20)
    st.pyplot(fig)


def plot_shot_xg_map(events, selected_match):
    shots = events[events["type"] == "Shot"]
    pitch = Pitch(
        pitch_type="statsbomb", line_zorder=2, pitch_color="grass", line_color="white"
    )
    fig, ax = pitch.draw(figsize=(10, 7))

    for i, row in shots.iterrows():
        if isinstance(row["location"], list):
            color = "red" if row["shot_outcome"] == "Goal" else "blue"
            size = (
                row["shot_statsbomb_xg"] * 1000 if "shot_statsbomb_xg" in row else 100
            )
            pitch.scatter(
                row["location"][0],
                row["location"][1],
                s=size,
                color=color,
                edgecolor="black",
                ax=ax,
                lw=2,
            )

    ax.set_title(f"Tiro ao Gol com xG: {selected_match}", fontsize=20)
    st.pyplot(fig)
