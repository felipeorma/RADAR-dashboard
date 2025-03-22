# streamlit_app.py

import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from metrics_config import summarized_metrics
from radar_utils import cumple_rol, calcular_percentiles, generar_radar

# ✅ Configuración básica de la página y estilo visual moderno
st.set_page_config(page_title="Radar Scouting CONMEBOL", layout="wide")

# 🔒 Ocultar elementos de Streamlit para una presentación más limpia
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

# 🎌 Función que convierte el país a un emoji de bandera + nombre
def country_to_flag(country):
    flags = {
        "Argentina": "🇦🇷 Argentina", "Brazil": "🇧🇷 Brazil", "Colombia": "🇨🇴 Colombia", "Uruguay": "🇺🇾 Uruguay",
        "Chile": "🇨🇱 Chile", "Paraguay": "🇵🇾 Paraguay", "Peru": "🇵🇪 Peru", "Ecuador": "🇪🇨 Ecuador",
        "Venezuela": "🇻🇪 Venezuela", "Bolivia": "🇧🇴 Bolivia"
    }
    return flags.get(country, country)

# 🌐 Selector de idioma
idioma = st.sidebar.radio("🌐 Idioma / Language", ['Español', 'English'])

# 🗂️ Diccionario de textos traducidos
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

# 🖼️ Logo superior
st.image("https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/images/CONMEBOL_logo.png", width=100)

# 🧾 Título principal
st.title(t['titulo'])

# 📥 Leer archivo Excel desde GitHub
url_github_excel = "https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/CONMEBOL%20QUALI.xlsx"
response = requests.get(url_github_excel)
df = pd.read_excel(BytesIO(response.content))

# 🧠 Mapeo de posiciones clave para clasificar el rol
keywords_by_role = {
    'Goalkeeper': ['GK'],
    'Defender': ['CB', 'RCB', 'LCB'],
    'Fullback': ['LB', 'RB', 'LWB', 'RWB'],
    'Midfielder': ['CMF', 'DMF', 'AMF', 'LMF', 'RMF'],
    'Wingers': ['LW', 'LWF', 'RWF', 'RW', 'LAMF', 'RAMF'],
    'Forward': ['CF', 'ST', 'SS']
}

# 🗂️ Traducciones de roles
roles_map = {
    'Goalkeeper': {'es': 'Portero', 'en': 'Goalkeeper'},
    'Defender': {'es': 'Defensor', 'en': 'Defender'},
    'Fullback': {'es': 'Lateral', 'en': 'Fullback'},
    'Midfielder': {'es': 'Mediocampista', 'en': 'Midfielder'},
    'Wingers': {'es': 'Extremo', 'en': 'Winger'},
    'Forward': {'es': 'Delantero', 'en': 'Forward'}
}

# 👤 Selector de rol
roles_display = [roles_map[role]['es'] if idioma == 'Español' else roles_map[role]['en'] for role in roles_map]
rol_display = st.selectbox(t['rol'], roles_display)

# 🔁 Obtener el rol original
for role_key, traducciones in roles_map.items():
    if traducciones['es' if idioma == 'Español' else 'en'] == rol_display:
        selected_role = role_key
        translated_role = traducciones['es' if idioma == 'Español' else 'en']
        break

# 🌍 Filtro por país CONMEBOL
if 'Birth country' in df.columns:
    conmebol_paises = ['Argentina', 'Brazil', 'Colombia', 'Uruguay', 'Chile', 'Paraguay', 'Peru', 'Ecuador', 'Venezuela', 'Bolivia']
    paises_en_df = sorted(set(df['Birth country'].dropna()) & set(conmebol_paises))
    countries = ['Todos' if idioma == 'Español' else 'All'] + paises_en_df
    selected_country = st.selectbox(t['pais'], countries)
else:
    selected_country = 'Todos' if idioma == 'Español' else 'All'

# ⏱️ Filtros adicionales
min_minutes = st.slider(t['min'], 100, 1500, 500, 100)
min_edad = int(df['Age'].min())
max_edad = int(df['Age'].max())
rango_edad = st.slider(t['edad'], min_edad, max_edad, (min_edad, max_edad))
top_n = st.slider(t['top'], 1, 5, 3)

# 🧹 Filtrado por posición (solo la primera si hay varias)
df_filtered = df[df['Position'].apply(lambda x: cumple_rol(str(x).split(',')[0].strip(), selected_role, keywords_by_role))]

if selected_country not in ['Todos', 'All'] and 'Birth country' in df.columns:
    df_filtered = df_filtered[df_filtered['Birth country'] == selected_country]

df_filtered = df_filtered[
    (df_filtered['Minutes played'] >= min_minutes) &
    (df_filtered['Age'].between(rango_edad[0], rango_edad[1]))
]

# ⚠️ Si no hay jugadores
if df_filtered.empty:
    st.warning(t['no_data'])
else:
    resumen = summarized_metrics[selected_role]['es' if idioma == 'Español' else 'en']
    df_percentiles, categorias = calcular_percentiles(df_filtered, resumen)
    df_percentiles = df_percentiles.rename(columns={'Promedio': 'ELO'})
    top_df = df_percentiles.sort_values("ELO", ascending=False)
    tabla_completa = top_df.copy()
    top_df = top_df.head(top_n)
    top_players = [(row['Player'], {cat: row[cat] for cat in categorias}) for _, row in top_df.iterrows()]

    # 📈 Gráfico radar
    fig = generar_radar(top_players, df, categorias, translated_role, top_n, idioma)

    # 📌 Logo de CONMEBOL en radar
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

    # 📋 Tabla de jugadores
    st.markdown(t['tabla'])
    columnas_info = ['Team', 'Age', 'Market value', 'Contract expires', 'Birth country']
    columnas_existentes = [col for col in columnas_info if col in df.columns]
    mostrar = tabla_completa[['Player', 'ELO']].merge(df[['Player'] + columnas_existentes], on='Player', how='left')

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
            'Market value': 'Valor',
            'ELO': 'ELO'
        })
        columnas_ordenadas = ['Jugador', 'Club', 'Edad', 'País', 'Contrato', 'ELO']

    styled_df = mostrar[columnas_ordenadas].style.format(precision=1).applymap(
        lambda v: 'background-color: #347aeb; color: black; font-weight: bold;', subset=['ELO' if idioma == 'English' else 'ELO']
    )
    st.dataframe(styled_df)

    # ⬇️ Botón de descarga CSV
    st.download_button(t['csv'], mostrar[columnas_ordenadas].to_csv(index=False).encode('utf-8'),
                       file_name="ranking_elo.csv", mime="text/csv")

    # 🖼️ Botón de descarga del radar
    try:
        st.download_button(
            label=t['png'],
            data=fig.to_image(format="png"),
            file_name="radar.png",
            mime="image/png"
        )
    except Exception:
        st.info("Para exportar imagen, instala `kaleido`: pip install kaleido")
