import time
import streamlit as st

from visualizations import (
    plot_correlation,
    plot_pass_map,
    plot_passes_vs_goals,
    plot_pressure_map,
    plot_shot_map,
    plot_shot_xg_map,
    plot_shots_distribution,
)

from layout import (
    display_match_info,
    display_player_data_for_download,
    display_player_selection,
    display_event_form,
    display_time_interval_form,
    display_comparison_form,
)

from sidebar import display_sidebar

from data.loaders import load_match_events


st.title("Análise de Partidas")
competition_id, selected_match, match_id = display_sidebar()
st.header(f"Análise da Partida: {selected_match}")
with st.spinner("Carregando os dados da partida..."):
    time.sleep(2)
    events = load_match_events(match_id)
st.success("Dados da partida carregados!")

display_match_info(events)

plot_pass_map(events, selected_match, True)
plot_shot_map(events, selected_match, True)
plot_passes_vs_goals(events)
plot_shots_distribution(events)
plot_correlation(events)
plot_pressure_map(events, selected_match, True)
plot_shot_xg_map(events, selected_match)

display_player_selection(events)

players = events["player"].unique()
selected_player = st.selectbox("Selecione um jogador para baixar os dados", players)
display_player_data_for_download(events, selected_player)

display_event_form(events)
display_time_interval_form(events)
display_comparison_form(events)
