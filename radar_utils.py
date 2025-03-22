
from scipy.stats import rankdata
import plotly.graph_objects as go

# Esta función verifica si una posición pertenece al rol seleccionado
def cumple_rol(posicion, rol, keywords_por_rol):
    if not isinstance(posicion, str):
        return False
    for keyword in keywords_por_rol.get(rol, []):
        if keyword in posicion:
            return True
    return False

# Esta función calcula los percentiles para cada categoría resumida
def calcular_percentiles(df_filtrado, resumen_metricas):
    categorias = list(resumen_metricas.keys())
    scores = []

    for _, fila in df_filtrado.iterrows():
        puntajes = {}
        for categoria, pesos in resumen_metricas.items():
            puntaje = 0
            suma_pesos = 0
            for metrica, peso in pesos.items():
                valor = fila.get(metrica)
                if pd.notna(valor):
                    puntaje += valor * peso
                    suma_pesos += abs(peso)
            puntajes[categoria] = puntaje / suma_pesos if suma_pesos > 0 else 0
        scores.append({'UniqueID': fila['UniqueID'], 'Player': fila['Player'], **puntajes})

    df_scores = pd.DataFrame(scores)

    for categoria in categorias:
        valores = df_scores[categoria].values
        df_scores[categoria] = rankdata(valores, method='average') / len(valores) * 100

    df_scores['Promedio'] = df_scores[categorias].mean(axis=1)
    return df_scores, categorias

# Esta función genera el gráfico de radar Plotly con opciones estilizadas
def generar_radar(jugadores_top, df, categorias, rol_traducido, top_n, idioma):
    colores = ['#00C9A7', '#FF6B6B', '#845EC2', '#FFC75F', '#008E9B']
    fig = go.Figure()

    for i, (uid, valores) in enumerate(jugadores_top):
        fila_jugador = df[df['UniqueID'] == uid].head(1)
        nombre = fila_jugador['Player'].values[0] if not fila_jugador.empty else uid
        pais = fila_jugador['Birth country'].values[0] if 'Birth country' in fila_jugador.columns else ''
        club = fila_jugador['Team'].values[0] if 'Team' in fila_jugador.columns else ''
        nombre_grafico = f"{nombre} ({club})"

        r = [valores[c] for c in categorias] + [valores[categorias[0]]]
        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=categorias + [categorias[0]],
            fill='toself',
            name=nombre_grafico,
            line=dict(color=colores[i % len(colores)], width=3),
            opacity=0.85
        ))

    fig.update_layout(
        title=dict(
            text=f"<b>Radar Scouting CONMEBOL - Top {top_n} {rol_traducido}s</b>",
            x=0.5, y=0.95, xanchor='center', yanchor='top',
            font=dict(size=22, color='white')
        ),
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False),
            angularaxis=dict(tickfont=dict(size=13, color='white'))
        ),
        paper_bgcolor='#0d0d0d',
        plot_bgcolor='#0d0d0d',
        legend=dict(font=dict(color='white', size=12), orientation='v'),
        margin=dict(l=60, r=60, t=100, b=100)
    )

    return fig
