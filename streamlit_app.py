
# Este es el archivo principal de la aplicación Streamlit para visualizar datos de jugadores CONMEBOL

import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from metrics_config import summarized_metrics
from radar_utils import cumple_rol, calcular_percentiles, generar_radar

# Configuración inicial de la página y estilos
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

# Función para convertir país a bandera + nombre
def country_to_flag(country):
    flags = {
        "Argentina": "🇦🇷 Argentina", "Brazil": "🇧🇷 Brazil", "Colombia": "🇨🇴 Colombia", "Uruguay": "🇺🇾 Uruguay",
        "Chile": "🇨🇱 Chile", "Paraguay": "🇵🇾 Paraguay", "Peru": "🇵🇪 Peru", "Ecuador": "🇪🇨 Ecuador",
        "Venezuela": "🇻🇪 Venezuela", "Bolivia": "🇧🇴 Bolivia"
    }
    return flags.get(country, country)

# Diccionario que relaciona jugadores con doble nacionalidad y país representado
dual_nationalities = {
    "B. Brereton Díaz": ("Chile", "🇬🇧 England / 🇨🇱 Chile"),
    "G. Lapadula": ("Peru", "🇮🇹 Italy / 🇵🇪 Peru"),
    "O. Sonne": ("Peru", "🇩🇰 Denmark / 🇵🇪 Peru"),
    "E. Morales": ("Bolivia", "🇺🇸 USA / 🇧🇴 Bolivia"),
    "J. Yeboah": ("Ecuador", "🇩🇪 Germany / 🇪🇨 Ecuador"),
    "J. Sarmiento": ("Ecuador", "🇬🇧 England / 🇪🇨 Ecuador"),
    "N. Fonseca": ("Venezuela", "🇮🇹 Italy / 🇻🇪 Venezuela")
}

