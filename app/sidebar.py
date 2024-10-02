import streamlit as st
from data.loaders import load_competitions, load_matches


def display_sidebar():
    competitions = load_competitions()

    unique_competitions = competitions.drop_duplicates(subset=["competition_name"])

    st.sidebar.header("Selecione o Campeonato")
    selected_competition = st.sidebar.selectbox(
        "Competição", unique_competitions["competition_name"]
    )

    competition_id = unique_competitions[
        unique_competitions["competition_name"] == selected_competition
    ]["competition_id"].values[0]

    seasons = competitions[competitions["competition_id"] == competition_id]
    selected_season = st.sidebar.selectbox("Temporada", seasons["season_name"])

    season_id = seasons[seasons["season_name"] == selected_season]["season_id"].values[
        0
    ]
    matches = load_matches(competition_id=competition_id, season_id=season_id)

    selected_match = st.sidebar.selectbox(
        "Partida", matches["home_team"] + " vs " + matches["away_team"]
    )

    match_id = matches[
        matches["home_team"] + " vs " + matches["away_team"] == selected_match
    ]["match_id"].values[0]

    return competition_id, selected_match, match_id
