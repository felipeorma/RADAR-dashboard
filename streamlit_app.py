import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from metrics_config import summarized_metrics
from radar_utils import cumple_rol, calcular_percentiles, generar_radar

# Configuración de página
st.set_page_config(page_title="Radar Scouting CONMEBOL", layout="wide")

# Estilos visuales
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

# Bandera + país

def country_to_flag(country):
    flags = {
        "Argentina": "🇦🇷 Argentina", "Brazil": "🇧🇷 Brazil", "Colombia": "🇨🇴 Colombia", "Uruguay": "🇺🇾 Uruguay",
        "Chile": "🇨🇱 Chile", "Paraguay": "🇵🇾 Paraguay", "Peru": "🇵🇪 Peru", "Ecuador": "🇪🇨 Ecuador",
        "Venezuela": "🇻🇪 Venezuela", "Bolivia": "🇧🇴 Bolivia"
    }
    return flags.get(country, country)

# Texto multilenguaje
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
        'png': "🖼️ Descargar radar como imagen PNG",
        'firma': "<div style='text-align:center; font-size:13px; color:gray;'>By: Felipe Ormazabal - Football Scout & Data Analyst</div>"
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
        'png': "🖼️ Download radar as PNG image",
        'firma': "<div style='text-align:center; font-size:13px; color:gray;'>By: Felipe Ormazabal - Football Scout & Data Analyst</div>"
    }
}
t = textos[idioma]

# Mostrar logo
st.image("https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/images/CONMEBOL_logo.png", width=100)

st.title(t['titulo'])

# Cargar archivo Excel desde GitHub
url_github_excel = "https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/CONMEBOL%20QUALI.xlsx"
response = requests.get(url_github_excel)
df = pd.read_excel(BytesIO(response.content))

# Crear identificador único por jugador + club
df["UniqueID"] = df["Player"] + " (" + df["Team"] + ")"

# Diccionario de roles por keywords
keywords_by_role = {
    'Goalkeeper': ['GK'],
    'Defender': ['CB', 'RCB', 'LCB'],
    'Fullback': ['LB', 'RB', 'LWB', 'RWB'],
    'Midfielder': ['CMF', 'DMF', 'AMF', 'LMF', 'RMF'],
    'Wingers': ['LW', 'LWF', 'RWF', 'RW', 'LAMF', 'RAMF'],
    'Forward': ['CF', 'ST', 'SS']
}

# Traducción de roles
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
        translated_role = traducciones['es' if idioma == 'Español' else 'en']
        break

# Filtros
if 'Birth country' in df.columns:
    countries = ['Todos' if idioma == 'Español' else 'All'] + sorted(df['Birth country'].dropna().unique())
    selected_country = st.selectbox(t['pais'], countries)
else:
    selected_country = 'Todos' if idioma == 'Español' else 'All'

min_minutes = st.slider(t['min'], 0, 1500, 100, 100)

if 'Age' in df.columns:
    min_edad = int(df['Age'].min())
    max_edad = int(df['Age'].max())
    rango_edad = st.slider(t['edad'], min_edad, max_edad, (min_edad, max_edad))
else:
    rango_edad = (0, 100)

top_n = st.slider(t['top'], 1, 5, 3)

# Calcular percentiles sobre TODO el dataframe
total_resumen = summarized_metrics[selected_role]['es' if idioma == 'Español' else 'en']
df_percentiles, categorias = calcular_percentiles(df, total_resumen, unique_col="UniqueID")
df_percentiles = df_percentiles.rename(columns={'Promedio': 'ELO'})

# Aplicar filtros al df original solo para mostrar
filtro_df = df[df['Position'].apply(lambda x: cumple_rol(str(x).split(',')[0].strip(), selected_role, keywords_by_role))]

if selected_country not in ['Todos', 'All'] and 'Birth country' in filtro_df.columns:
    filtro_df = filtro_df[filtro_df['Birth country'] == selected_country]

filtro_df = filtro_df[
    (filtro_df['Minutes played'] >= min_minutes) &
    (filtro_df['Age'].between(rango_edad[0], rango_edad[1]))
]

if filtro_df.empty:
    st.warning(t['no_data'])
else:
    df_merged = df_percentiles.merge(df, on="UniqueID", how="left")
    mostrar = df_merged[df_merged['UniqueID'].isin(filtro_df['UniqueID'])].drop_duplicates("UniqueID")

    top_df = mostrar.sort_values("ELO", ascending=False).head(top_n)
    top_players = [(row['UniqueID'], {cat: row[cat] for cat in categorias}) for _, row in top_df.iterrows()]

    fig = generar_radar(top_players, df, categorias, translated_role, top_n, idioma, id_column="UniqueID")

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

    try:
        st.download_button(
            label=t['png'],
            data=fig.to_image(format="png"),
            file_name="radar.png",
            mime="image/png"
        )
    except Exception:
        st.info("Para exportar imagen, instala `kaleido`: pip install kaleido")

    st.markdown(t['tabla'])

    if 'Birth country' in mostrar.columns:
        mostrar['Birth country'] = mostrar['Birth country'].apply(country_to_flag)

    if idioma == 'Español':
        mostrar = mostrar.rename(columns={
            'Player': 'Jugador', 'Team': 'Club', 'Age': 'Edad',
            'Birth country': 'País', 'Contract expires': 'Contrato'
        })

    columnas_final = ['Jugador' if idioma == 'Español' else 'Player',
                      'Club' if idioma == 'Español' else 'Team',
                      'Edad' if idioma == 'Español' else 'Age',
                      'País' if idioma == 'Español' else 'Country',
                      'Contrato' if idioma == 'Español' else 'Contract expires',
                      'ELO']

    mostrar = mostrar.sort_values("ELO", ascending=False)

    styled = mostrar[columnas_final].style \
        .format(precision=1) \
        .applymap(lambda v: 'background-color: #DDEBFF; color: black; font-weight: bold;', subset=['ELO'])

    st.dataframe(styled, use_container_width=True)

    st.download_button(t['csv'], mostrar[columnas_final].to_csv(index=False).encode('utf-8'),
                       file_name="ranking_elo.csv", mime="text/csv")

    # Agregar firma
    st.markdown(t['firma'], unsafe_allow_html=True)
