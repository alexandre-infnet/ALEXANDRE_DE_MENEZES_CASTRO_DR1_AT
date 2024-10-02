import streamlit as st
from io import StringIO
from visualizations import plot_pass_map, plot_shot_map, plot_pressure_map


def display_match_info(events):
    goals = events[events["type"] == "Shot"][events["shot_outcome"] == "Goal"].shape[0]
    shots = events[events["type"] == "Shot"].shape[0]
    passes = events[events["type"] == "Pass"].shape[0]
    tackles = events[events["type"] == "Duel"][events["duel_type"] == "Tackle"].shape[0]

    st.write(f"**Gols:** {goals}")
    st.write(f"**Chutes:** {shots}")
    st.write(f"**Passes:** {passes}")
    st.write(f"**Desarmes:** {tackles}")


def display_player_selection(events):
    players = events["player"].unique()
    selected_player = st.selectbox("Selecione um jogador", players)

    if st.button("Mostrar Mapa de Passes"):
        plot_pass_map(events, selected_player, False)

    if st.button("Mostrar Mapa de Chutes"):
        plot_shot_map(events, selected_player, False)

    if st.button("Mostrar Mapa de Pressão"):
        plot_pressure_map(events, selected_player, False)


def display_event_form(events):
    with st.form("event_form"):
        st.write("Escolha a quantidade de eventos a serem visualizados")
        event_count = st.text_input("Digite a quantidade de eventos", value="20")
        submit_button = st.form_submit_button("Aplicar")

    if submit_button:
        try:
            event_count = int(event_count)
            st.write(f"Exibindo {event_count} eventos")
            st.dataframe(events.head(event_count))
        except ValueError:
            st.error("Por favor, insira um número válido.")


def display_time_interval_form(events):
    with st.form("time_interval_form"):
        st.write("Selecione o intervalo de tempo da partida")
        time_option = st.radio(
            "Selecione a opção de intervalo",
            options=["Primeiro tempo", "Segundo tempo", "Personalizado"],
        )

        if time_option == "Primeiro tempo":
            start_time, end_time = 0, 45
        elif time_option == "Segundo tempo":
            start_time, end_time = 46, 90
        else:
            start_time = st.slider("Minuto inicial", min_value=0, max_value=90, value=0)
            end_time = st.slider("Minuto final", min_value=0, max_value=90, value=90)

        submit_time_button = st.form_submit_button("Aplicar")

    if submit_time_button:
        st.write(f"Exibindo eventos do minuto {start_time} ao {end_time}")

        time_filtered_events = events[
            (events["minute"] >= start_time) & (events["minute"] <= end_time)
        ]

        st.dataframe(time_filtered_events)


def display_comparison_form(events):
    players = events["player"].unique()

    with st.form("compare_players_form"):
        st.write("Comparar dois jogadores")
        player_1 = st.selectbox("Selecionar Jogador 1", players, index=0)
        player_2 = st.selectbox("Selecionar Jogador 2", players, index=1)

        compare_passes = st.checkbox("Comparar Passes", value=True)
        compare_shots = st.checkbox("Comparar Chutes", value=True)

        submit_compare_button = st.form_submit_button("Comparar")

    if submit_compare_button:
        st.write(f"Comparando {player_1} e {player_2}")
        if compare_passes:
            st.write(f"Comparando Passes de {player_1} e {player_2}")
            events_player_1_passes = events[
                (events["player"] == player_1) & (events["type"] == "Pass")
            ]

            events_player_2_passes = events[
                (events["player"] == player_2) & (events["type"] == "Pass")
            ]

            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Passes de {player_1}")
                st.dataframe(events_player_1_passes)

            with col2:
                st.write(f"Passes de {player_2}")
                st.dataframe(events_player_2_passes)

        if compare_shots:
            st.write(f"Comparando Chutes de {player_1} e {player_2}")
            events_player_1_shots = events[
                (events["player"] == player_1) & (events["type"] == "Shot")
            ]

            events_player_2_shots = events[
                (events["player"] == player_2) & (events["type"] == "Shot")
            ]

            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Chutes de {player_1}")
                st.dataframe(events_player_1_shots)

            with col2:
                st.write(f"Chutes de {player_2}")
                st.dataframe(events_player_2_shots)


def generate_csv(dataframe):
    csv = StringIO()
    dataframe.to_csv(csv, index=False)
    return csv.getvalue()


def display_player_data_for_download(events, player):
    passes_player = events[(events["player"] == player) & (events["type"] == "Pass")]
    shots_player = events[(events["player"] == player) & (events["type"] == "Shot")]
    pressure_player = events[
        (events["player"] == player) & (events["type"] == "Pressure")
    ]

    passes_csv = generate_csv(passes_player)
    shots_csv = generate_csv(shots_player)
    pressure_csv = generate_csv(pressure_player)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="Baixar Dados de Passes",
            data=passes_csv,
            file_name=f"passes_{player}.csv",
            mime="text/csv",
        )

    with col2:
        st.download_button(
            label="Baixar Dados de Chutes",
            data=shots_csv,
            file_name=f"chutes_{player}.csv",
            mime="text/csv",
        )

    with col3:
        st.download_button(
            label="Baixar Dados de Pressão",
            data=pressure_csv,
            file_name=f"pressao_{player}.csv",
            mime="text/csv",
        )
