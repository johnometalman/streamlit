import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Explorador estadístico de jugadores de la NBA')

st.markdown("""
Esta aplicación realiza un webscraping simple de los datos de los jugadores de la NBA!
* **Librerías de Python:** base64, pandas, streamlit
* **Fuente:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('Ingreso de Variables')
selected_year = st.sidebar.selectbox('Año', list(reversed(range(1950,2022))))

# Web scraping of NBA player stats
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    data = pd.read_html(url, header = 0)
    df = data[0]
    delete_raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    delete_raw = delete_raw.fillna('0.0')
    data_clean = delete_raw.drop(['Rk'], axis=1)
    return data_clean

playerstats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Equipo', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Posición', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Estadísticas de jugadores de equipo(s) seleccionado(s)')
st.write('Tamaño de Datos: ' + str(df_selected_team.shape[0]) + ' rows & ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="estadisticas-nba.csv">Descargar archivo de CSV</a>'
    return href

st.markdown(file_download(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Mapa de calor de Intercorrelaciones'):
    st.header('Matriz de mapa de calor de la Intercorrelación')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot()
