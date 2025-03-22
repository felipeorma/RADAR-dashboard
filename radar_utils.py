from scipy.stats import rankdata
import pandas as pd
import plotly.graph_objects as go

# Esta función verifica si la posición del jugador coincide con el rol seleccionado
# Considera solo la primera posición listada en caso de múltiples

def cumple_rol(posicion, rol, keywords_by_role):
    if pd.isna(posicion):
        return False
    primera_pos = str(posicion).split(',')[0].strip()
    return any(keyword in primera_pos for keyword in keywords_by_role.get(rol, []))

# Esta función calcula los percentiles de todos los jugadores del dataset original,
# y luego devuelve únicamente los jugadores que están en el dataframe filtrado.
# Así los percentiles y ELO no se distorsionan aunque se apliquen filtros visuales.

def calcular_percentiles(df_filtrado, resumen_metricas, df_completo=None, unique_col="Player"):
    df_base = df_completo if df_completo is not None else df_filtrado.copy()
    nombres_categorias = list(resumen_metricas.keys())
    data = []

    for _, fila in df_base.iterrows():
        jugador = fila[unique_col]
        resultados = {unique_col: jugador}
        for categoria, pesos in resumen_metricas.items():
            puntaje = 0
            peso_total = 0
            for metrica, peso in pesos.items():
                valor = fila.get(metrica)
                if pd.notna(valor):
                    puntaje += valor * peso
                    peso_total += abs(peso)
            resultados[categoria] = puntaje / peso_total if peso_total > 0 else 0
        data.append(resultados)

    df_resultados = pd.DataFrame(data)

    for categoria in nombres_categorias:
        valores = df_resultados[categoria].values
        df_resultados[categoria] = rankdata(valores, method='average') / len(valores) * 100

    df_resultados['Promedio'] = df_resultados[nombres_categorias].mean(axis=1)

    # Filtramos el resultado final si se pasó un df filtrado
    if df_filtrado is not None:
        ids_filtrados = df_filtrado[unique_col].unique()
        df_resultados = df_resultados[df_resultados[unique_col].isin(ids_filtrados)].copy()

    return df_resultados, nombres_categorias

# Esta función genera un radar chart en Plotly para los jugadores seleccionados
# Utiliza sus métricas resumidas y los muestra con colores modernos

def generar_radar(jugadores_top, df_original, categorias, rol, top_n, idioma, id_column="Player"):
    fig = go.Figure()

    # Paleta de colores moderna y suave
    colores = ['#30C5FF', '#FF6B6B', '#FFD93D', '#6BCB77', '#D3ADF7']

    # Diccionario para asignar banderas a países comunes
    banderas = {
        "Argentina": "🇦🇷", "Brazil": "🇧🇷", "Colombia": "🇨🇴", "Uruguay": "🇺🇾",
        "Chile": "🇨🇱", "Paraguay": "🇵🇾", "Peru": "🇵🇪", "Ecuador": "🇪🇨",
        "Venezuela": "🇻🇪", "Bolivia": "🇧🇴"
    }

    for i, (uid, valores) in enumerate(jugadores_top):
        fila = df_original[df_original[id_column] == uid]
        if fila.empty:
            continue
        fila = fila.iloc[0]
        pais = fila.get("Birth country", "")
        bandera = banderas.get(pais, "")
        nombre = fila["Player"]
        etiqueta = f"{bandera} {nombre}" if bandera else nombre

        r = [valores[c] for c in categorias] + [valores[categorias[0]]]
        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=categorias + [categorias[0]],
            fill='toself',
            name=etiqueta,
            line=dict(color=colores[i % len(colores)], width=3),
            opacity=0.85
        ))

    # Título dinámico con salto de línea
    titulo = f"Radar Scouting CONMEBOL<br>Top {top_n} {rol}s" if idioma == 'English' else f"Radar Scouting CONMEBOL<br>Top {top_n} {rol}s"

    fig.update_layout(
        title=dict(
            text=f"<b>{titulo}</b>",
            x=0.5,
            y=0.93,
            xanchor='center',
            font=dict(size=22, color='white')
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
                tickfont=dict(size=14, color='white'),
                direction='clockwise',
                gridcolor='rgba(255,255,255,0.1)',
                linecolor='rgba(255,255,255,0.2)'
            )
        ),
        paper_bgcolor='#0d0d0d',
        plot_bgcolor='#0d0d0d',
        showlegend=True,
        legend=dict(font=dict(color='white', size=12))
    )

    return fig