
# streamlit_app.py

import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from metrics_config import summarized_metrics
from radar_utils import cumple_rol, calcular_percentiles, generar_radar

# Configuración inicial
st.set_page_config(page_title="Radar Scouting CONMEBOL", layout="wide")

# Fuente moderna y ocultar menús
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Diccionario de banderas con nombre
def country_to_flag(country):
    flags = {
        "Argentina": "🇦🇷 Argentina", "Brazil": "🇧🇷 Brazil", "Colombia": "🇨🇴 Colombia", "Uruguay": "🇺🇾 Uruguay",
        "Chile": "🇨🇱 Chile", "Paraguay": "🇵🇾 Paraguay", "Peru": "🇵🇪 Peru", "Ecuador": "🇪🇨 Ecuador",
        "Venezuela": "🇻🇪 Venezuela", "Bolivia": "🇧🇴 Bolivia"
    }
    return flags.get(country, country)

# Selección de idioma
idioma = st.sidebar.radio("🌐 Idioma / Language", ['Español', 'English'])

textos = {
    'Español': {
        'titulo': "📊 Radar Scouting CONMEBOL - Resumido",
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

# Logo
st.image("https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/images/CONMEBOL_logo.png", width=100)
st.title(t['titulo'])

# Cargar archivo desde GitHub
url_github_excel = "https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/CONMEBOL%20QUALI.xlsx"
response = requests.get(url_github_excel)
df = pd.read_excel(BytesIO(response.content))

# Definir keywords y roles
keywords_by_role = {
    'Goalkeeper': ['GK'],
    'Defender': ['CB', 'RCB', 'LCB'],
    'Fullback': ['LB', 'RB', 'LWB', 'RWB'],
    'Midfielder': ['CMF', 'DMF', 'AMF', 'LMF', 'RMF'],
    'Wingers': ['LW', 'LWF', 'RWF', 'RW', 'LAMF', 'RAMF'],
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

# Detectar rol seleccionado
for role_key, traducciones in roles_map.items():
    if traducciones['es' if idioma == 'Español' else 'en'] == rol_display:
        selected_role = role_key
        translated_role = traducciones['es' if idioma == 'Español' else 'en']
        break

# Filtros de país
if 'Birth country' in df.columns:
    countries = ['Todos' if idioma == 'Español' else 'All'] + sorted(df['Birth country'].dropna().unique())
    selected_country = st.selectbox(t['pais'], countries)
else:
    selected_country = 'Todos' if idioma == 'Español' else 'All'

# Sliders
min_minutes = st.slider(t['min'], 0, 1500, 100, 100)
if 'Age' in df.columns:
    min_edad = int(df['Age'].min())
    max_edad = int(df['Age'].max())
    rango_edad = st.slider(t['edad'], min_edad, max_edad, (min_edad, max_edad))
else:
    rango_edad = (0, 100)
top_n = st.slider(t['top'], 1, 5, 3)

# Calcular percentiles y ELO con TODO el dataset
resumen = summarized_metrics[selected_role]['es' if idioma == 'Español' else 'en']
df_percentiles, categorias = calcular_percentiles(df, resumen)
df_percentiles = df_percentiles.rename(columns={'Promedio': 'ELO'})

# Filtrar DataFrame para visualización (no afecta ELO)
df_filtered = df[df['Position'].apply(lambda x: cumple_rol(str(x).split(',')[0].strip(), selected_role, keywords_by_role))]
if selected_country not in ['Todos', 'All']:
    df_filtered = df_filtered[df_filtered['Birth country'] == selected_country]
df_filtered = df_filtered[
    (df_filtered['Minutes played'] >= min_minutes) &
    (df_filtered['Age'].between(rango_edad[0], rango_edad[1]))
]
if df_filtered.empty:
    st.warning(t['no_data'])
else:
    # Tomar los top jugadores dentro del subset visual
    top_df = df_percentiles.merge(df[['Player']], on="Player")
    top_df = top_df[top_df['Player'].isin(df_filtered['Player'])].sort_values("ELO", ascending=False).head(top_n)
    top_players = [(row['Player'], {cat: row.get(cat, 0) for cat in categorias}) for _, row in top_df.iterrows()]

    # Radar
    fig = generar_radar(top_players, df, categorias, translated_role, top_n, idioma)
    fig.update_layout(images=[dict(
        source="https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/images/CONMEBOL_logo.png",
        xref="paper", yref="paper",
        x=0, y=1.15,
        sizex=0.3, sizey=0.3,
        xanchor="left", yanchor="top",
        opacity=0.8,
        layer="above"
    )])
    st.plotly_chart(fig, use_container_width=True)

    # Tabla
    st.markdown(t['tabla'])
    columnas_info = ['Team', 'Age', 'Value', 'Contract expires', 'Birth country']
    columnas_existentes = [col for col in columnas_info if col in df.columns]
    mostrar = df_percentiles[['Player', 'ELO']].merge(df[['Player'] + columnas_existentes], on='Player', how='left')
    if 'Birth country' in mostrar.columns:
        mostrar['Birth country'] = mostrar['Birth country'].apply(country_to_flag)
    columnas_ordenadas = ['Player', 'Team', 'Age', 'Birth country', 'Contract expires', 'ELO']
    if idioma == 'Español':
        mostrar = mostrar.rename(columns={
            'Player': 'Jugador',
            'Team': 'Club',
            'Age': 'Edad',
            'Birth country': 'País',
            'Contract expires': 'Contrato',
            'ELO': 'ELO'
        })
        columnas_ordenadas = ['Jugador', 'Club', 'Edad', 'País', 'Contrato', 'ELO']
    styled_df = mostrar[columnas_ordenadas].style.format(precision=1)        .applymap(lambda v: 'background-color: #347aeb; color: black; font-weight: bold;', subset=['ELO'])
    st.dataframe(styled_df)

    # Descargar
    st.download_button(t['csv'], mostrar[columnas_ordenadas].to_csv(index=False).encode('utf-8'),
                       file_name="ranking_elo.csv", mime="text/csv")
    try:
        st.download_button(
            label=t['png'],
            data=fig.to_image(format="png"),
            file_name="radar.png",
            mime="image/png"
        )
    except Exception:
        st.info("Para exportar imagen, instala `kaleido`: pip install kaleido")
