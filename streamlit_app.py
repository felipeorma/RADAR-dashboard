
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Cargar datos
st.title("Radar Scouting CONMEBOL - Streamlit App")
uploaded_file = st.file_uploader("Sube tu archivo Excel con datos de jugadores", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Diccionario de métricas resumidas por rol
    summarized_metrics = {
        'Goalkeeper': {
            'Prevención': {
                'Save rate, %': 0.4,
                'Prevented goals per 90': 0.3,
                'Conceded goals per 90': -0.3
            },
            'Distribución': {
                'Accurate forward passes, %': 0.5,
                'Accurate long passes, %': 0.5
            },
            'Juego con Balón': {
                'Received passes per 90': 0.3,
                'Accurate lateral passes, %': 0.3,
                'Accurate forward passes, %': 0.4
            },
            'Movimiento': {
                'Aerial duels per 90': 0.6,
                'Exits per 90': 0.4
            },
            'Posicionamiento': {
                'xG against per 90': -0.6,
                'Exits per 90': 0.4
            }
        },
        'Defender': {
            'Ataque': {
                'Progressive runs per 90': 0.5,
                'Accelerations per 90': 0.5
            },
            'Construcción': {
                'Accurate passes, %': 0.6,
                'Accurate long passes, %': 0.4
            },
            'Progresión': {
                'Progressive runs per 90': 0.5,
                'Accelerations per 90': 0.5
            },
            'Defensa': {
                'Defensive duels won, %': 0.4,
                'Sliding tackles per 90': 0.3,
                'Interceptions per 90': 0.3
            },
            'Posicionamiento': {
                'Interceptions per 90': 0.6,
                'Defensive duels won, %': 0.4
            }
        },
        'Fullback': {
            'Ataque': {
                'Successful attacking actions per 90': 0.4,
                'Crosses to goalie box per 90': 0.3,
                'Offensive duels won, %': 0.3
            },
            'Construcción': {
                'Accurate through passes, %': 0.4,
                'Passes per 90': 0.3,
                'Received passes per 90': 0.3
            },
            'Progresión': {
                'xA per 90': 0.6,
                'Accurate through passes, %': 0.4
            },
            'Movimiento': {
                'Accelerations per 90': 0.5,
                'Progressive runs per 90': 0.5
            },
            'Defensa': {
                'Defensive duels won, %': 0.6,
                'Interceptions per 90': 0.4
            }
        },
        'Midfielder': {
            'Ataque': {
                'xG per 90': 0.5,
                'Goals per 90': 0.5
            },
            'Construcción': {
                'Received passes per 90': 0.4,
                'Accurate short / medium passes, %': 0.6
            },
            'Progresión': {
                'Successful dribbles, %': 0.4,
                'Accurate short / medium passes, %': 0.3,
                'Accurate passes to final third, %': 0.3
            },
            'Creación': {
                'Assists per 90': 0.5,
                'xA per 90': 0.5
            },
            'Defensa': {
                'Defensive duels won, %': 0.5,
                'Interceptions per 90': 0.5
            }
        },
        'Wingers': {
            'Ataque': {
                'xG per 90': 0.4,
                'Goals per 90': 0.4,
                'Touches in box per 90': 0.2
            },
            'Construcción': {
                'Accurate passes to final third, %': 1.0
            },
            'Progresión': {
                'Offensive duels won, %': 0.5,
                'Successful dribbles, %': 0.5
            },
            'Creación': {
                'xA per 90': 0.4,
                'Assists per 90': 0.4,
                'Accurate passes to final third, %': 0.2
            },
            'Defensa': {
                'Defensive duels won, %': 0.6,
                'Interceptions per 90': 0.4
            }
        },
        'Forward': {
            'Ataque': {
                'xG per 90': 0.3,
                'Goals per 90': 0.4,
                'Non-penalty goals per 90': 0.3
            },
            'Construcción': {
                'Passes to penalty area per 90': 0.5,
                'Accurate passes to final third, %': 0.5
            },
            'Progresión': {
                'Head goals per 90': 0.5,
                'Aerial duels won, %': 0.5
            },
            'Creación': {
                'xA per 90': 0.5,
                'Assists per 90': 0.5
            },
            'Movimiento': {
                'Touches in box per 90': 0.6,
                'Passes to penalty area per 90': 0.4
            }
        }
    }

    # Interfaz
    roles = list(summarized_metrics.keys())
    selected_role = st.selectbox("Selecciona el rol", roles)
    countries = ['Todos'] + sorted(df['Birth country'].dropna().unique())
    selected_country = st.selectbox("Filtra por país", countries)
    min_minutes = st.slider("Minutos jugados mínimos", 0, 1500, 500, 100)
    top_n = st.slider("Número de jugadores en radar", 1, 5, 3)

    # Filtro por rol, país y minutos
    df_filtered = df[df['Position'].str.contains(selected_role, na=False)]
    if selected_country != 'Todos':
        df_filtered = df_filtered[df_filtered['Birth country'] == selected_country]
    df_filtered = df_filtered[df_filtered['Minutes played'] >= min_minutes]

    if df_filtered.empty:
        st.warning("No hay jugadores con esos filtros.")
    else:
        summary = summarized_metrics[selected_role]
        summary_scores = []

        for i, row in df_filtered.iterrows():
            cat_scores = {}
            for category, weights in summary.items():
                score = 0
                valid_weights = 0
                for metric, weight in weights.items():
                    value = row.get(metric)
                    if pd.notna(value):
                        score += value * weight
                        valid_weights += abs(weight)
                if valid_weights > 0:
                    cat_scores[category] = score / valid_weights
                else:
                    cat_scores[category] = 0
            summary_scores.append((row['Player'], cat_scores))

        # Ordenar por promedio
        summary_scores.sort(key=lambda x: -np.mean(list(x[1].values())))
        top_players = summary_scores[:top_n]

        # Graficar radar
        fig = go.Figure()
        categories = list(summary.keys())
        for name, values in top_players:
            r = [values[c] for c in categories]
            r += [r[0]]
            fig.add_trace(go.Scatterpolar(
                r=r,
                theta=categories + [categories[0]],
                fill='toself',
                name=name
            ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            title=f"Radar resumido - Top {top_n} {selected_role}s",
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
