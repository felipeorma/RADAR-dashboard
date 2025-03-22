# radar_utils.py

import numpy as np
import pandas as pd
from scipy.stats import rankdata
import plotly.graph_objects as go

# Esta función verifica si una posición coincide con los keywords del rol
# Se usa para filtrar a los jugadores según su primera posición

def cumple_rol(pos, rol, keywords_by_role):
    if pd.isna(pos):
        return False
    pos = str(pos).split(',')[0].strip()
    keywords = keywords_by_role.get(rol, [])
    return any(k in pos for k in keywords)

# Esta función calcula los percentiles y ELO de cada jugador
# Toma un DataFrame, las métricas resumidas por categoría y una columna única opcional para evitar duplicados

def calcular_percentiles(df, resumen, unique_col=None):
    category_names = list(resumen.keys())
    category_scores = []

    # Si se pasa una columna única, eliminamos duplicados
    if unique_col and unique_col in df.columns:
        df = df.drop_duplicates(subset=unique_col, keep='first')

    for _, row in df.iterrows():
        cat_scores = {}
        for category, weights in resumen.items():
            score = 0
            valid_weights = 0
            for metric, weight in weights.items():
                value = row.get(metric)
                if pd.notna(value):
                    score += value * weight
                    valid_weights += abs(weight)
            cat_scores[category] = score / valid_weights if valid_weights > 0 else 0
        category_scores.append((row['Player'], cat_scores))

    category_df = pd.DataFrame([dict(Player=name, **scores) for name, scores in category_scores])

    for cat in category_names:
        values = category_df[cat].values
        category_df[cat] = rankdata(values, method='average') / len(values) * 100

    category_df['Promedio'] = category_df[category_names].mean(axis=1)

    return category_df, category_names


# Esta función genera el gráfico radar con los jugadores seleccionados
# Utiliza Plotly y permite mostrar hasta 5 jugadores con colores diferenciados y diseño moderno

def generar_radar(top_players, df, categorias, rol, top_n, idioma):
    colores = ['#00C1D4', '#FF6F91', '#845EC2', '#FFC75F', '#008E9B']

    def abreviado(pais):
        codigos = {
            "Argentina": "ARG", "Brazil": "BRA", "Colombia": "COL", "Uruguay": "URU",
            "Chile": "CHL", "Paraguay": "PAR", "Peru": "PER", "Ecuador": "ECU",
            "Venezuela": "VEN", "Bolivia": "BOL"
        }
        return codigos.get(pais, pais[:3].upper())

    fig = go.Figure()

    for i, (name, values) in enumerate(top_players):
        jugador_row = df[df['Player'] == name].head(1)
        country = jugador_row['Birth country'].values[0] if not jugador_row.empty else ""
        cod = abreviado(country)
        name_label = f"{name} [{cod}]"

        r = [values[c] for c in categorias] + [values[categorias[0]]]
        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=categorias + [categorias[0]],
            fill='toself',
            name=name_label,
            line=dict(color=colores[i % len(colores)], width=3),
            opacity=0.85
        ))

    fig.update_layout(
        title=dict(
            text=f"<b>Radar Resumido<br>Top {top_n} {rol}s</b>",
            x=0.5,
            y=0.93,
            xanchor='center',
            yanchor='top',
            font=dict(color='white', size=22, family='Poppins')
        ),
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.2)'
            ),
            angularaxis=dict(
                tickfont=dict(color='white', size=14),
                direction='clockwise',
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.2)'
            )
        ),
        paper_bgcolor='#0d0d0d',
        plot_bgcolor='#0d0d0d',
        showlegend=True,
        legend=dict(
            font=dict(color='white', size=12),
            orientation='v',
            x=1,
            y=1
        ),
        margin=dict(l=60, r=60, t=100, b=100),
        annotations=[
            dict(
                text="By: Felipe Ormazabal<br>Football Scout - Data Analyst",
                showarrow=False,
                x=0.5,
                y=-0.32,
                xref="paper",
                yref="paper",
                font=dict(color='white', size=12),
                align='center'
            )
        ]
    )

    return fig
