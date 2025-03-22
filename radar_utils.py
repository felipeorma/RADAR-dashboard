from scipy.stats import rankdata
import pandas as pd

# Esta función verifica si la posición del jugador coincide con el rol seleccionado
# Considera solo la primera posición listada en caso de múltiples

def cumple_rol(posicion, rol, keywords_by_role):
    if pd.isna(posicion):
        return False
    primera_pos = str(posicion).split(',')[0].strip()
    return any(keyword in primera_pos for keyword in keywords_by_role.get(rol, []))

# Esta función calcula los percentiles de los jugadores con base en las métricas resumidas
# Permite usar una columna única para evitar jugadores duplicados (por nombre + club, por ejemplo)

def calcular_percentiles(df, resumen_metricas, unique_col="Player"):
    nombres_categorias = list(resumen_metricas.keys())
    data = []

    # Iteramos por cada jugador
    for _, fila in df.iterrows():
        jugador = fila[unique_col]
        resultados = {unique_col: jugador}
        for categoria, pesos in resumen_metricas.items():
            puntaje = 0
            peso_total = 0
            for metrica, peso in pesos.items():
                valor = fila.get(metrica)
                if pd.notna(valor):
                    puntaje += valor * peso
                    peso_total += abs(peso)
            resultados[categoria] = puntaje / peso_total if peso_total > 0 else 0
        data.append(resultados)

    df_resultados = pd.DataFrame(data)

    # Normalizamos cada categoría a percentiles
    for categoria in nombres_categorias:
        valores = df_resultados[categoria].values
        df_resultados[categoria] = rankdata(valores, method='average') / len(valores) * 100

    df_resultados['Promedio'] = df_resultados[nombres_categorias].mean(axis=1)
    return df_resultados, nombres_categorias
