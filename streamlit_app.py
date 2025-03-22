# streamlit_app.py

import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from metrics_config import summarized_metrics
from radar_utils import cumple_rol, calcular_percentiles, generar_radar

# Configuración inicial de Streamlit
st.set_page_config(page_title="Radar Scouting CONMEBOL", layout="wide")

# Estilos personalizados para ocultar Streamlit UI y aplicar fuente moderna
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Función para mostrar bandera junto al país
def country_to_flag(country):
    flags = {
        "Argentina": "🇦🇷 Argentina", "Brazil": "🇧🇷 Brazil", "Colombia": "🇨🇴 Colombia", "Uruguay": "🇺🇾 Uruguay",
        "Chile": "🇨🇱 Chile", "Paraguay": "🇵🇾 Paraguay", "Peru": "🇵🇪 Peru", "Ecuador": "🇪🇨 Ecuador",
        "Venezuela": "🇻🇪 Venezuela", "Bolivia": "🇧🇴 Bolivia"
    }
    return flags.get(country, country)

# Textos por idioma
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

# Mostrar logo CONMEBOL
st.image("https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/images/CONMEBOL_logo.png", width=100)

# Título
st.title(t['titulo'])

# Cargar archivo Excel desde GitHub
url_excel = "https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/CONMEBOL%20QUALI.xlsx"
df = pd.read_excel(BytesIO(requests.get(url_excel).content))

# Crear ID único: nombre + club
df["UniqueID"] = df["Player"] + " (" + df["Team"] + ")"

# Definir roles por posición
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

# Selector de rol
roles_display = [roles_map[r]['es'] if idioma == 'Español' else roles_map[r]['en'] for r in roles_map]
rol_display = st.selectbox(t['rol'], roles_display)
for key, val in roles_map.items():
    if val['es' if idioma == 'Español' else 'en'] == rol_display:
        selected_role = key
        translated_role = val['es' if idioma == 'Español' else 'en']
        break

# Filtros
countries = ['Todos' if idioma == 'Español' else 'All'] + sorted(df['Birth country'].dropna().unique())
selected_country = st.selectbox(t['pais'], countries)
min_minutes = st.slider(t['min'], 0, 1500, 100, 100)
rango_edad = st.slider(t['edad'], int(df['Age'].min()), int(df['Age'].max()), (int(df['Age'].min()), int(df['Age'].max())))
top_n = st.slider(t['top'], 1, 5, 3)

# Filtrar según posición (solo primera posición si hay múltiples)
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
    resumen = summarized_metrics[selected_role]['es' if idioma == 'Español' else 'en']
    df_percentiles, categorias = calcular_percentiles(df_filtered, resumen, unique_col="UniqueID")
    df_percentiles = df_percentiles.rename(columns={'Promedio': 'ELO'})
    top_df = df_percentiles.sort_values("ELO", ascending=False).head(top_n)

    top_players = [(row['UniqueID'], {cat: row[cat] for cat in categorias}) for _, row in top_df.iterrows()]
    fig = generar_radar(top_players, df, categorias, translated_role, top_n, idioma, id_column="UniqueID")

    fig.update_layout(images=[dict(
        source="https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/images/CONMEBOL_logo.png",
        xref="paper", yref="paper", x=0, y=1.15, sizex=0.3, sizey=0.3,
        xanchor="left", yanchor="top", opacity=0.8, layer="above"
    )])

    st.plotly_chart(fig, use_container_width=True)
    st.markdown(t['tabla'])

    columnas_info = ['Player', 'Team', 'Age', 'Birth country', 'Contract expires']
    mostrar = df_percentiles.merge(df[columnas_info + ['UniqueID']], on="UniqueID", how="left").drop_duplicates("UniqueID")

    if 'Birth country' in mostrar.columns:
        mostrar['Birth country'] = mostrar['Birth country'].apply(country_to_flag)

    if idioma == 'Español':
        mostrar = mostrar.rename(columns={
            'Player': 'Jugador', 'Team': 'Club', 'Age': 'Edad',
            'Birth country': 'País', 'Contract expires': 'Contrato'
        })

    mostrar = mostrar.sort_values("ELO", ascending=False)

    columnas_final = ['Jugador' if idioma == 'Español' else 'Player',
                      'Club' if idioma == 'Español' else 'Team',
                      'Edad' if idioma == 'Español' else 'Age',
                      'País' if idioma == 'Español' else 'Birth country',
                      'Contrato' if idioma == 'Español' else 'Contract expires',
                      'ELO']

    # Estilizar columna ELO
    styled = mostrar[columnas_final].style.applymap(
        lambda v: 'background-color: #e0edff; color: black; font-weight: bold;', subset=['ELO']
    )

    st.dataframe(styled.set_index(columnas_final[0]))

    st.download_button(t['csv'], mostrar[columnas_final].to_csv(index=False).encode('utf-8'),
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
