
# 📊 Radar Scouting CONMEBOL

## 🇪🇸 Español

### 🧠 ¿Qué es esto?

Una aplicación interactiva hecha en [Streamlit](https://streamlit.io) para visualizar el rendimiento de jugadores de fútbol sudamericanos usando gráficos de radar **resumidos por rol**.

### 🧰 Características

- 🌐 Interfaz en español e inglés
- ⚽ Comparación de jugadores por **posición táctica**
- 📊 Radar por categorías resumidas: ataque, defensa, creación, etc.
- 🧮 Percentiles normalizados por métrica
- 📁 Archivo de datos cargado automáticamente desde GitHub
- 🔍 Filtros por país, edad y minutos jugados
- 🏅 Tabla con ELO personalizado
- 📥 Exportar radar como PNG y tabla como CSV

### 🗂️ Estructura del Proyecto

```
📁 data/
    └─ CONMEBOL QUALI.xlsx         <- Datos de jugadores
    └─ images/CONMEBOL_logo.png    <- Logo oficial
📄 streamlit_app.py                <- App principal
📄 metrics_config.py               <- Config. de métricas por rol
📄 radar_utils.py                  <- Funciones de radar y cálculo
📄 requirements.txt                <- Dependencias
```

### 🚀 Cómo ejecutarlo

1. 📦 Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. ▶️ Ejecutar la app:
```bash
streamlit run streamlit_app.py
```

3. 🌐 Abre el enlace generado en tu navegador.

### 🆕 Actualizaciones

📅 Esta app se actualizará **fecha a fecha** durante las Clasificatorias Sudamericanas rumbo al Mundial 2026.

### 🙌 Uso con sabiduría

Este radar está diseñado como una herramienta para **Fanáticos** que desean profundizar en el rendimiento de jugadores.  
**¡Recuerda que el contexto siempre importa! ⚠️**

---

## 🇬🇧 English

### 🧠 What is this?

An interactive [Streamlit](https://streamlit.io) app to visualize South American football players using **role-based summarized radar charts**.

### 🧰 Features

- 🌐 Spanish & English interface
- ⚽ Compare players by **tactical role**
- 📊 Radar by summarized categories: attack, defense, creation, etc.
- 🧮 Percentile normalization by metric
- 📁 Player data loaded from GitHub
- 🔍 Filters by country, age and minutes
- 🏅 Table with custom ELO
- 📥 Export radar (PNG) and table (CSV)

### 🗂️ Project Structure

```
📁 data/
    └─ CONMEBOL QUALI.xlsx         <- Player data
    └─ images/CONMEBOL_logo.png    <- Logo
📄 streamlit_app.py                <- Main app
📄 metrics_config.py               <- Role metrics config
📄 radar_utils.py                  <- Radar & calc functions
📄 requirements.txt                <- Dependencies
```

### 🚀 How to run it

1. 📦 Install dependencies:
```bash
pip install -r requirements.txt
```

2. ▶️ Run the app:
```bash
streamlit run streamlit_app.py
```

3. 🌐 Open the browser link provided by Streamlit.

### 🆕 Updates

📅 This tool will be **updated after each matchday** of the CONMEBOL World Cup Qualifiers.

### 🙌 Use wisely

This dashboard is built for **Football fans** seeking deeper player insights.  
**Context always matters! ⚠️**

---

## ✍️ Autor / Author

**Felipe Ormazábal**  
_Football Scout & Data Analyst_  
🔗 [LinkedIn]([https://linkedin.com/in/felipeorma](https://www.linkedin.com/in/felipe-ormazabal-835037226/))
