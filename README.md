
# 📊 Radar Scouting CONMEBOL

> 🇪🇸 Herramienta de análisis visual para comparar jugadores durante las Eliminatorias Sudamericanas.
>  
> 🇬🇧 A visual scouting tool to compare players during the South American World Cup Qualifiers.

---

## 🧠 ¿Qué es esto? / What is this?

Una aplicación interactiva hecha en [Streamlit](https://streamlit.io) para visualizar el rendimiento de jugadores de fútbol sudamericanos usando gráficos de radar **resumidos por rol**.

An interactive app built with Streamlit to visualize South American football players using **role-based summarized radar charts**.

---

## 🧰 Características / Features

- 🌐 Interfaz bilingüe (Español / English)
- ⚽ Comparación de jugadores por **posición táctica**
- 📊 Radar gráfico por categorías resumidas (ataque, defensa, creación, etc.)
- 🧮 Percentiles normalizados por métrica
- 📁 Archivo cargado automáticamente desde GitHub (actualizado)
- 🔍 Filtros por país, edad, minutos jugados
- 🏅 Tabla detallada con ELO personalizado
- 📥 Exportación como PNG o CSV

---

## 🗂️ Estructura del Proyecto / Project Structure

```
📁 data/
    └─ CONMEBOL QUALI.xlsx         <- Archivo de datos de jugadores
    └─ images/CONMEBOL_logo.png    <- Logo oficial
📄 streamlit_app.py                <- Aplicación principal
📄 metrics_config.py              <- Configuración de métricas por rol
📄 radar_utils.py                 <- Funciones para cálculo y radar
📄 requirements.txt               <- Dependencias del proyecto
```

---

## 🚀 Cómo ejecutarlo / How to Run It

1. 📦 Instala las dependencias:
```bash
pip install -r requirements.txt
```

2. ▶️ Ejecuta la app:
```bash
streamlit run streamlit_app.py
```

3. 🌐 Abre en tu navegador el enlace que te aparece en consola.

---

## 🆕 Actualizaciones / Updates

📅 Este radar será actualizado **fecha a fecha** a lo largo de las clasificatorias sudamericanas rumbo al Mundial 2026.

This radar will be updated **match by match** during the CONMEBOL World Cup Qualifiers.

---

## 🙌 Uso con sabiduría / Use with Wisdom

Este dashboard está diseñado como una herramienta para analistas, scouts y fanáticos que desean profundizar en los datos del rendimiento de jugadores. El contexto siempre importa. ⚠️

This dashboard is designed for analysts, scouts, and fans who want to go deeper into player performance data. Always consider context. ⚠️

---

## ✍️ Autor / Author

**Felipe Ormazábal**  
_Football Scout & Data Analyst_  
📧 [LinkedIn](https://linkedin.com/in/felipeorma)

---
