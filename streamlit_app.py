import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Radar Scouting CONMEBOL", layout="wide")
st.title("📊 Radar Scouting CONMEBOL - Visualización resumida")

uploaded_file = st.file_uploader("Sube tu archivo Excel con datos de jugadores", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Keywords para detección de rol
    keywords_by_role = {
        'Goalkeeper': ['GK'],
        'Defender': ['CB', 'RCB', 'LCB'],
        'Fullback': ['LB', 'RB', 'LWB', 'RWB'],
        'Midfielder': ['CMF', 'DMF', 'AMF', 'LMF', 'RMF'],
        'Wingers': ['LW', 'RW', 'LAMF', 'RAMF'],
        'Forward': ['CF', 'ST', 'SS']
    }

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

    roles = list(summarized_metrics.keys())
    selected_role = st.selectbox("Selecciona el rol", roles)
    countries = ['Todos'] + sorted(df['Birth country'].dropna().unique())
    selected_country = st.selectbox("Filtrar por país", countries)
    min_minutes = st.slider("Minutos jugados mínimos", 0, 1500, 500, 100)
    top_n = st.slider("Top jugadores a mostrar", 1, 5, 3)

    # Filtro mejorado por keywords
    def cumple_rol(pos, rol):
        if pd.isna(pos): return False
        keywords = keywords_by_role.get(rol, [])
        return any(k in pos for k in keywords)

    df_filtered = df[df['Position'].apply(lambda x: cumple_rol(x, selected_role))]
    if selected_country != 'Todos':
        df_filtered = df_filtered[df_filtered['Birth country'] == selected_country]
    df_filtered = df_filtered[df_filtered['Minutes played'] >= min_minutes]

    if df_filtered.empty:
        st.warning("⚠️ No hay jugadores que cumplan los filtros.")
    else:
        summary = summarized_metrics[selected_role]
        summary_scores = []

        for _, row in df_filtered.iterrows():
            cat_scores = {}
            for category, weights in summary.items():
                score = 0
                valid_weights = 0
                for metric, weight in weights.items():
                    value = row.get(metric)
                    if pd.notna(value):
                        score += value * weight
                        valid_weights += abs(weight)
                cat_scores[category] = score / valid_weights if valid_weights > 0 else 0
            summary_scores.append((row['Player'], cat_scores))

        summary_scores.sort(key=lambda x: -np.mean(list(x[1].values())))
        top_players = summary_scores[:top_n]

        # ✅ Arreglar esto: definir categorías
        categories = list(summary.keys())

        # Radar Plot
        fig = go.Figure()

        # Paleta de colores vibrantes
        colores = ['#FF4B91', '#FF884B', '#4BCFFA', '#B15EFF', '#3AE37B']
        
        for i, (name, values) in enumerate(top_players):
            r = [values[c] for c in categories]
            r += [r[0]]  # cerrar el radar
            fig.add_trace(go.Scatterpolar(
                r=r,
                theta=categories + [categories[0]],
                fill='toself',
                name=name,
                line=dict(color=colores[i % len(colores)], width=2),
                opacity=0.8
            ))
        
        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(
                    visible=True,
                    range=[0, max(1.0, max([max(v[1].values()) for v in top_players]))],
                    showline=False,
                    ticks='',
                    showticklabels=False,
                    gridcolor='lightgray',
                ),
                angularaxis=dict(
                    tickfont=dict(size=13, color='gray'),
                    rotation=90,
                    direction='clockwise'
                )
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=True,
            title=dict(
                text=f"<b>Radar resumido - Top {top_n} {selected_role}s</b>",
                font=dict(size=20)
            ),
            margin=dict(l=40, r=40, t=80, b=40)
        )
        
        st.plotly_chart(fig, use_container_width=True)
