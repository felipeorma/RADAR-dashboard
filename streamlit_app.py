import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from metrics_config import summarized_metrics
from radar_utils import cumple_rol, calcular_percentiles, generar_radar

# Configuración de página
st.set_page_config(page_title="Radar Scouting CONMEBOL", layout="wide")

# Estilo visual moderno
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

# Función para convertir país a bandera
def country_to_flag(country):
    flags = {
        "Argentina": "🇦🇷 Argentina", "Brazil": "🇧🇷 Brazil", "Colombia": "🇨🇴 Colombia", "Uruguay": "🇺🇾 Uruguay",
        "Chile": "🇨🇱 Chile", "Paraguay": "🇵🇾 Paraguay", "Peru": "🇵🇪 Peru", "Ecuador": "🇪🇨 Ecuador",
        "Venezuela": "🇻🇪 Venezuela", "Bolivia": "🇧🇴 Bolivia"
    }
    return flags.get(country, country)

# Texto por idioma
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

# Cargar Excel desde GitHub
url_excel = "https://raw.githubusercontent.com/felipeorma/RADAR-dashboard/main/data/CONMEBOL%20QUALI.xlsx"
df = pd.read_excel(BytesIO(requests.get(url_excel).content))

# Crear ID único
df["UniqueID"] = df["Player"] + " (" + df["Team"] + ")"

# Diccionario de roles
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

# Interfaz de rol
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

# Calcular percentiles globales para el rol completo
df_rol = df[df['Position'].apply(lambda x: cumple_rol(str(x).split(',')[0].strip(), selected_role, keywords_by_role))]
resumen = summarized_metrics[selected_role]['es' if idioma == 'Español' else 'en']
df_percentiles, categorias = calcular_percentiles(df_rol, resumen, unique_col="UniqueID")
df_percentiles = df_percentiles.rename(columns={'Promedio': 'ELO'})

# Filtrar para visualización sin recalcular
df_filtered = df_rol.copy()
if selected_country not in ['Todos', 'All']:
    df_filtered = df_filtered[df_filtered['Birth country'] == selected_country]
df_filtered = df_filtered[(df_filtered['Minutes played'] >= min_minutes) & df_filtered['Age'].between(*rango_edad)]

if df_filtered.empty:
    st.warning(t['no_data'])
else:
    df_filtered_ids = df_filtered['UniqueID'].tolist()
    tabla_visible = df_percentiles[df_percentiles["UniqueID"].isin(df_filtered_ids)].merge(
        df[['UniqueID', 'Player', 'Team', 'Age', 'Birth country', 'Contract expires']],
        on='UniqueID',
        how='left'
    ).drop_duplicates('UniqueID')

    # Mostrar radar
    top_df = tabla_visible.sort_values("ELO", ascending=False).head(top_n)
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

    # Botón descarga radar
    try:
        st.download_button(
            label=t['png'],
            data=fig.to_image(format="png"),
            file_name="radar.png",
            mime="image/png"
        )
    except Exception:
        st.info("Para exportar imagen, instala `kaleido`: pip install kaleido")

    # Mostrar tabla
    st.markdown(t['tabla'])
    tabla_visible['Country'] = tabla_visible['Birth country'].apply(country_to_flag)
    tabla_visible = tabla_visible.drop(columns='Birth country')

    columnas_final = ['Player', 'Team', 'Age', 'Country', 'Contract expires', 'ELO']
    if idioma == 'Español':
        tabla_visible = tabla_visible.rename(columns={
            'Player': 'Jugador',
            'Team': 'Club',
            'Age': 'Edad',
            'Country': 'País',
            'Contract expires': 'Contrato'
        })
        columnas_final = ['Jugador', 'Club', 'Edad', 'País', 'Contrato', 'ELO']

    # Ordenar por ELO descendente
    tabla_visible = tabla_visible.sort_values("ELO", ascending=False)

    # Pintar columna ELO
    styled = tabla_visible.style.applymap(
        lambda x: 'background-color: #D6E4FF; color: black; font-weight: bold;', subset=['ELO']
    )
    st.dataframe(styled[columnas_final], use_container_width=True)

    # Botón CSV
    st.download_button(t['csv'], tabla_visible[columnas_final].to_csv(index=False).encode('utf-8'),
                       file_name="ranking_elo.csv", mime="text/csv")
