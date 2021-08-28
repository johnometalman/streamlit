import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

st.write("""
# Una app simple de predicción de la flor de iris

Esta aplicación predice el tipo de flor de iris!
""")

st.sidebar.header('Ingreso de parametros para el usuario')

def ingreso_caracteristicas():
    sepalo_largo = st.sidebar.slider('Largo del sepalo', 4.3, 7.9, 5.4)
    sepalo_ancho = st.sidebar.slider('Ancho del sepalo', 2.0, 4.4, 3.4)
    petalo_largo = st.sidebar.slider('Largo del petalo', 1.0, 6.9, 1.3)
    petalo_ancho = st.sidebar.slider('Ancho del petalo', 0.1, 2.5, 0.2)
    data = {'sepalo_largo': sepalo_largo,
            'sepalo_ancho': sepalo_ancho,
            'petalo_largo': petalo_largo,
            'petalo_ancho': petalo_ancho}
    features = pd.DataFrame(data, index=[0])
    return features

df = ingreso_caracteristicas()

st.subheader('Ingreso de Parámetros')
st.write(df)

iris = datasets.load_iris()
X = iris.data
Y = iris.target

clasificador = RandomForestClassifier()
clasificador.fit(X, Y)

prediccion = clasificador.predict(df)
prediccion_proba = clasificador.predict_proba(df)

st.subheader('Tipo de flor y su correspondiente número de indexacción')
st.write(iris.target_names)

st.subheader('Predicción')
st.write(iris.target_names[prediccion])
#st.write(predicción)

st.subheader('Probabilidad de predicción')
st.write(prediccion_proba)