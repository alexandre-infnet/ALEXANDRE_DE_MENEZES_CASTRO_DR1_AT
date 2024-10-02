import streamlit as st
from statsbombpy import sb


@st.cache_data
def load_competitions():
    return sb.competitions()


@st.cache_data
def load_matches(competition_id, season_id):
    return sb.matches(competition_id=competition_id, season_id=season_id)


@st.cache_data
def load_match_events(match_id):
    return sb.events(match_id=match_id)
