
# streamlit_app.py

import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from metrics_config import summarized_metrics
from radar_utils import cumple_rol, calcular_percentiles, generar_radar

# Configuración de página y fuente moderna
st.set_page_config(page_title="Radar Scouting CONMEBOL", layout="wide")
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

# Función para convertir país en bandera + nombre
def country_to_flag(country):
    flags = {
        "Argentina": "🇦🇷 Argentina", "Brazil": "🇧🇷 Brazil", "Colombia": "🇨🇴 Colombia", "Uruguay": "🇺🇾 Uruguay",
        "Chile": "🇨🇱 Chile", "Paraguay": "🇵🇾 Paraguay", "Peru": "🇵🇪 Peru", "Ecuador": "🇪🇨 Ecuador",
        "Venezuela": "🇻🇪 Venezuela", "Bolivia": "🇧🇴 Bolivia"
    }
    return flags.get(country, country)

# Selector de idioma
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

# Logo CONMEBOL
st.image("https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/images/CONMEBOL_logo.png", width=100)
st.title(t['titulo'])

# Carga de archivo desde GitHub
url_excel = "https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/CONMEBOL%20QUALI.xlsx"
df = pd.read_excel(BytesIO(requests.get(url_excel).content))

# Diccionario para detección de posición principal
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

# Mostrar selectbox de rol traducido
roles_display = [roles_map[r]['es'] if idioma == 'Español' else roles_map[r]['en'] for r in roles_map]
rol_display = st.selectbox(t['rol'], roles_display)

# Obtener rol interno a partir del display traducido
for key, val in roles_map.items():
    if val['es' if idioma == 'Español' else 'en'] == rol_display:
        selected_role = key
        translated_role = val['es' if idioma == 'Español' else 'en']

# Filtro país
countries = ['Todos' if idioma == 'Español' else 'All'] + sorted(df['Birth country'].dropna().unique())
selected_country = st.selectbox(t['pais'], countries)

# Filtro minutos
min_minutes = st.slider(t['min'], 0, 1500, 100, 100)

# Filtro edad
min_edad = int(df['Age'].min())
max_edad = int(df['Age'].max())
rango_edad = st.slider(t['edad'], min_edad, max_edad, (min_edad, max_edad))

# Cuántos mostrar en radar
top_n = st.slider(t['top'], 1, 5, 3)

# Obtener todos los jugadores válidos para ELO (percentiles globales)
df_all_role = df[df['Position'].apply(lambda x: cumple_rol(str(x).split(',')[0].strip(), selected_role, keywords_by_role))]
resumen = summarized_metrics[selected_role]['es' if idioma == 'Español' else 'en']
df_percentiles, categorias = calcular_percentiles(df_all_role, resumen)
df_percentiles = df_percentiles.rename(columns={'Promedio': 'ELO'})

# Aplicar filtros visuales sobre datos ya calculados
df_filtered = df_all_role.copy()
if selected_country not in ['Todos', 'All']:
    df_filtered = df_filtered[df_filtered['Birth country'] == selected_country]
df_filtered = df_filtered[
    (df_filtered['Minutes played'] >= min_minutes) &
    (df_filtered['Age'].between(rango_edad[0], rango_edad[1]))
]

# Unir ELO y datos
tabla = df_filtered.merge(df_percentiles[['Player', 'ELO']], on='Player', how='left')
tabla = tabla.sort_values('ELO', ascending=False)

# Si no hay jugadores, mostrar alerta
if tabla.empty:
    st.warning(t['no_data'])
else:
    top_df = tabla.head(top_n)
    top_players = [(row['Player'], {cat: row[cat] for cat in categorias}) for _, row in top_df.iterrows()]
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

    st.markdown(t['tabla'])

    # Mostrar tabla visual
    columnas_info = ['Player', 'Team', 'Age', 'Birth country', 'Contract expires', 'ELO']
    mostrar = tabla[columnas_info].copy()
    mostrar['Birth country'] = mostrar['Birth country'].apply(country_to_flag)

    if idioma == 'Español':
        mostrar = mostrar.rename(columns={
            'Player': 'Jugador',
            'Team': 'Club',
            'Age': 'Edad',
            'Birth country': 'País',
            'Contract expires': 'Contrato',
            'ELO': 'ELO'
        })
        mostrar = mostrar[['Jugador', 'Club', 'Edad', 'País', 'Contrato', 'ELO']]
    else:
        mostrar = mostrar[['Player', 'Team', 'Age', 'Birth country', 'Contract expires', 'ELO']]

    st.dataframe(mostrar.style.format(precision=1).applymap(
        lambda v: 'background-color: #347aeb; color: black; font-weight: bold;' if isinstance(v, float) else '',
        subset=['ELO']
    ))

    st.download_button(t['csv'], mostrar.to_csv(index=False).encode('utf-8'),
                       file_name="ranking_elo.csv", mime="text/csv")

