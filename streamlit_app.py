
# streamlit_app.py

import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from metrics_config import summarized_metrics
from radar_utils import cumple_rol, calcular_percentiles, generar_radar

st.set_page_config(page_title="Radar Scouting CONMEBOL", layout="wide")

idioma = st.sidebar.radio("🌐 Idioma / Language", ['Español', 'English'])

textos = {
    'Español': {
        'titulo': "📊 Radar Scouting Básico - Visualización resumida",
        'rol': "🔎 Selecciona el rol",
        'pais': "🌎 Filtrar por país",
        'min': "⏱️ Minutos jugados mínimos",
        'edad': "🎂 Edad (rango)",
        'top': "🏅 Top jugadores a mostrar",
        'no_data': "⚠️ No hay jugadores que cumplan los filtros.",
        'tabla': "### 📋 Tabla de jugadores",
        'csv': "⬇️ Descargar tabla en CSV",
        'png': "🖼️ Descargar radar como imagen PNG"
    },
    'English': {
        'titulo': "📊 Radar Scouting CONMEBOL - Summary Visualization",
        'rol': "🔎 Select role",
        'pais': "🌎 Filter by country",
        'min': "⏱️ Minimum minutes played",
        'edad': "🎂 Age range",
        'top': "🏅 Top players to show",
        'no_data': "⚠️ No players match the filters.",
        'tabla': "### 📋 Player Table",
        'csv': "⬇️ Download table as CSV",
        'png': "🖼️ Download radar as PNG image"
    }
}
t = textos[idioma]

st.title(t['titulo'])

# Cargar archivo desde GitHub
url_github_excel = "https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/CONMEBOL%20QUALI.xlsx"  # <-- EDITA AQUÍ
response = requests.get(url_github_excel)
df = pd.read_excel(BytesIO(response.content))

keywords_by_role = {
    'Goalkeeper': ['GK'],
    'Defender': ['CB', 'RCB', 'LCB'],
    'Fullback': ['LB', 'RB', 'LWB', 'RWB'],
    'Midfielder': ['CMF', 'DMF', 'AMF', 'LMF', 'RMF'],
    'Wingers': ['LW', 'RW', 'LAMF', 'RAMF'],
    'Forward': ['CF', 'ST', 'SS']
}

roles_map = {
    'Goalkeeper': {'es': 'Portero', 'en': 'Goalkeeper'},
    'Defender': {'es': 'Defensor', 'en': 'Defender'},
    'Fullback': {'es': 'Lateral', 'en': 'Fullback'},
    'Midfielder': {'es': 'Mediocampista', 'en': 'Midfielder'},
    'Wingers': {'es': 'Extremo', 'en': 'Winger'},
    'Forward': {'es': 'Delantero', 'en': 'Forward'}
}

roles_display = [roles_map[role]['es'] if idioma == 'Español' else roles_map[role]['en'] for role in roles_map]
rol_display = st.selectbox(t['rol'], roles_display)

for role_key, traducciones in roles_map.items():
    if traducciones['es' if idioma == 'Español' else 'en'] == rol_display:
        selected_role = role_key
        break

if 'Birth country' in df.columns:
    countries = ['Todos' if idioma == 'Español' else 'All'] + sorted(df['Birth country'].dropna().unique())
    selected_country = st.selectbox(t['pais'], countries)
else:
    selected_country = 'Todos' if idioma == 'Español' else 'All'

min_minutes = st.slider(t['min'], 0, 1500, 500, 100)

if 'Age' in df.columns:
    min_edad = int(df['Age'].min())
    max_edad = int(df['Age'].max())
    rango_edad = st.slider(t['edad'], min_edad, max_edad, (min_edad, max_edad))
else:
    rango_edad = (0, 100)

top_n = st.slider(t['top'], 1, 5, 3)

df_filtered = df[df['Position'].apply(lambda x: cumple_rol(x, selected_role, keywords_by_role))]

if selected_country not in ['Todos', 'All'] and 'Birth country' in df.columns:
    df_filtered = df_filtered[df_filtered['Birth country'] == selected_country]

df_filtered = df_filtered[
    (df_filtered['Minutes played'] >= min_minutes) &
    (df_filtered['Age'].between(rango_edad[0], rango_edad[1]))
]

if df_filtered.empty:
    st.warning(t['no_data'])
else:
    resumen = summarized_metrics[selected_role]['es' if idioma == 'Español' else 'en']
    df_percentiles, categorias = calcular_percentiles(df_filtered, resumen)
    df_percentiles = df_percentiles.rename(columns={'Promedio': 'ELO'})
    top_df = df_percentiles.sort_values("ELO", ascending=False).head(top_n)
    top_players = [(row['Player'], {cat: row[cat] for cat in categorias}) for _, row in top_df.iterrows()]

    fig = generar_radar(top_players, df, categorias, selected_role, top_n, idioma)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(t['tabla'])

    columnas_info = ['Player', 'Team', 'Age', 'Value', 'Contract expires', 'ELO']
    columnas_info = [col for col in columnas_info if col in top_df.columns]

    st.dataframe(top_df[columnas_info].set_index("Player").round(1))

    st.download_button(t['csv'], top_df[columnas_info].to_csv(index=False).encode('utf-8'),
                       file_name="ranking_percentiles.csv", mime="text/csv")

    try:
        st.download_button(
            label=t['png'],
            data=fig.to_image(format="png"),
            file_name="radar.png",
            mime="image/png"
        )
    except Exception:
        st.info("Para exportar imagen, instala `kaleido`: pip install kaleido")
