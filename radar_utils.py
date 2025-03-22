
# radar_utils.py

import pandas as pd
import numpy as np
from scipy.stats import rankdata
import plotly.graph_objects as go

def cumple_rol(pos, rol, keywords_by_role):
    if pd.isna(pos): return False
    keywords = keywords_by_role.get(rol, [])
    return any(k in pos for k in keywords)

def calcular_percentiles(df_filtered, summary_dict):
    summary_scores = []
    for _, row in df_filtered.iterrows():
        cat_scores = {}
        for category, weights in summary_dict.items():
            score = 0
            valid_weights = 0
            for metric, weight in weights.items():
                value = row.get(metric)
                if pd.notna(value):
                    score += value * weight
                    valid_weights += abs(weight)
            cat_scores[category] = score / valid_weights if valid_weights > 0 else 0
        summary_scores.append((row['Player'], cat_scores))

    category_names = list(summary_dict.keys())
    category_df = pd.DataFrame([dict(Player=name, **scores) for name, scores in summary_scores])
    for cat in category_names:
        values = category_df[cat].values
        category_df[cat] = rankdata(values, method='average') / len(values) * 100
    category_df['Promedio'] = category_df[category_names].mean(axis=1)

    return category_df, category_names

def generar_radar(top_players, df, category_names, role, top_n, idioma):
    colores = ['#00FFFF', '#FF6F61', '#6A5ACD', '#FFD700', '#00FF7F']
    fig = go.Figure()

    def abreviado(pais):
        codigos = {
            "Argentina": "ARG", "Brazil": "BRA", "Colombia": "COL", "Uruguay": "URU",
            "Chile": "CHL", "Paraguay": "PAR", "Peru": "PER", "Ecuador": "ECU",
            "Venezuela": "VEN", "Bolivia": "BOL"
        }
        return codigos.get(pais, pais[:3].upper())

    for i, (name, values) in enumerate(top_players):
        jugador_row = df[df['Player'] == name].head(1)
        country = jugador_row['Birth country'].values[0] if not jugador_row.empty else ""
        cod = abreviado(country)
        name_label = f"{name} [{cod}]"
        r = [values[c] for c in category_names] + [values[category_names[0]]]
        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=category_names + [category_names[0]],
            fill='toself',
            name=name_label,
            line=dict(color=colores[i % len(colores)], width=3),
            opacity=0.85
        ))

    titulo = "Radar Resumido<br>Top {top_n} {role}s" if idioma == 'Español' else "Radar Summary<br>Top {top_n} {role}s"
    firma = "By: Felipe Ormazabal<br>Football Scout - Data Analyst"

    fig.update_layout(
        title=dict(
            text=titulo.format(top_n=top_n, role=role),
            x=0.5,
            y=0.95,
            xanchor='center',
            font=dict(color='white', size=22)
        ),
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False,
                            gridcolor='rgba(255,255,255,0.1)', linecolor='rgba(255,255,255,0.2)'),
            angularaxis=dict(tickfont=dict(color='white', size=14), direction='clockwise',
                             gridcolor='rgba(255,255,255,0.1)', linecolor='rgba(255,255,255,0.2)')
        ),
        paper_bgcolor='#0d0d0d',
        plot_bgcolor='#0d0d0d',
        showlegend=True,
        legend=dict(font=dict(color='white', size=12), orientation='v', x=1, y=1),
        margin=dict(l=60, r=60, t=100, b=100),
        annotations=[
            dict(
                text=firma,
                showarrow=False,
                x=0.5,
                y=-0.3,
                xref="paper",
                yref="paper",
                font=dict(color='white', size=12),
                align='center'
            )
        ]
    )
    return fig
