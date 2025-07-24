import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

import json
key_dic = json.loads(st.secrets["textkey"])

creds = service_account.Credentials.from_service_account_info(key_dic)
#db = firestore.Client(credentials=creds, project="names-project-demo.json")
db = firestore.Client(credentials=creds, project="movies-9cbad")
dbProducto = db.collection("movies")


## Lectura de datos con atributo @cache__________________________________________________
@st.cache_data(ttl=60)  # cache por 60 segundos para evitar recargar siempre
def load_data():
    docs = dbMovies.stream()
    data = []
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id  # opcional: incluir ID del documento
        data.append(d)
    return pd.DataFrame(data)

data = load_data()

# título, encabezado y mensaje de la sección principal
st.title("Netflix app")

#Creamos una sección del lado izquierdo que se denomina barra lateral o sidebar
#sidebar = st.sidebar

#título y un parrafo para la sidebar
st.sidebar.header("Elementos de búsqueda")


## Componente checkbox paera visualizar datos_________________________________________
show_data = st.sidebar.checkbox("Mostrar todos los filmes")
if show_data:
    st.dataframe(data)
    nrow = data.shape[0]
    st.write(f"Se encontraron {nrow} filmes")
st.markdown("---")

## Componente de texto y boton de de comando para filtrar título
titulo = st.sidebar.text_input("Título del filme")
if st.sidebar.button("Buscar filmes"):
  filter_titulo= data[data['name'].str.contains(titulo,na=False, case = False)]
  nrow = filter_titulo.shape[0]
  st.write(f"Se encontraron {nrow} filmes que contienen el título {titulo}")
  st.dataframe(filter_titulo)
st.markdown("---")

# Componente selectbox y boton de comando para filtrar director
st.sidebar.subheader("Filtrar por Director")
selected_director = st.sidebar.selectbox("Selecciona director", data['director'].unique())

if st.sidebar.button("Filtrar director"):
  director = data[data['director'] == selected_director]
  nrow = director.shape[0]
  st.write(f"Se encontraron {nrow} filmes con el director {selected_director}")
  st.dataframe(director)
st.markdown("---")

# Componente text input para nuevo registro

st.sidebar.title("Nuevo filme")

company = st.sidebar.text_input("Company")
director = st.sidebar.text_input("Director")
genre = st.sidebar.text_input("Genre")
name = st.sidebar.text_input("Name")

submit = st.sidebar.button("Crear nuevo filme")

if company and director and genre and name and submit:
  doc_ref = dbMovies.document()
  doc_ref.set({
      "company": company,
      "director": director,
      "genre": genre,
      "name": name
  })
  st.sidebar.success("Nuevo filme creado")
