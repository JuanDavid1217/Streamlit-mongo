from pymongo import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
import pandas as pd 
import matplotlib.pyplot as mp 
import plotly.express as px 
import numpy as np

# replace here with your mongodb url 
uri = "mongodb+srv://JuanDavid1217:JuanDavid#1712@cluster0.m3ei4fv.mongodb.net/?retryWrites=true&w=majority"
# Connect to meme MongoDB database

try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    db = client.fisicoculturismo
    print("MongoDB Connected successfully!")
except:
    print("Could not connect to MongoDB")

# streamlit run streamlit-mongo.py --server.enableCORS false --server.enableXsrfProtection false

#--- PAGE CONFIG ---#
st.set_page_config(page_title="Proyecto: Fisicoculturismo", ##Estas dos lineas
                   page_icon="bodybuilding2.png")      #Modifican el folder (pagina)


#--- PRESENTACION ---#
st.title("mongo db conn (Fisicoculturismo)")
st.markdown("**Realizado por:**")
st.markdown("""Juan David Delgado Muñoz\n
    Matricula: S20006756\n
    email: ZS20006756@estudiantes.uv.mx\n
    Licenciatura en Ingenieria de Software.""")

#--- SIDEBAR ---#
sidebar=st.sidebar
sidebar.image("bodybuilding.png")
sidebar.markdown("##")

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    items = db.reactions_info.find()
    items = list(items)  # make hashable for st.cache_data
    return pd.DataFrame(items)


#--- CHECHKBOX ---#
visualizar=sidebar.checkbox("**Mostrar datos cargados en cache.**")
st.subheader("Datos cargados en cache")
if (visualizar):
    data_general=get_data()
    #count_row = data_general.shape[0]
    #st.write(f"Total de datos cargados: {count_row}")
    #st.dataframe(data_general)
    st.write('results...')
    st.write(data_general)

st.markdown("___")
sidebar.markdown("___")

#--- MULTISELECT: FILTRADO DE CANCIONES POR ARTISTA ---#
#primero obtenemos las publicaciones (id)

"""def getIDs():
    ids=[]
    data=get_data()
    for i in data:
        if(len(ids)==0):
            ids.append(i['publication'])
        else:
            if (ids[len(ids)-1]!=(i['publication'])):
                ids.append(i['publication'])
    st.write(ids)
    return ids
"""
publicationms=sidebar.multiselect("**Filtrar total de reacciones por publicación:**",
                             options=get_data()['publication'].unique())

publicationselection=get_data().query('publication==@publicationms').sort_values(by='publication')
st.subheader('Reacciones por publicación')
st.write("La siguiente tabla muestra todas las reacciones obtenidas por cada publicacion seleccionada")
st.dataframe(publicationselection)
publicationselection2=publicationselection.groupby(by='publication').count()['reaction']
st.write("Posteriormente se realiza un calculo para saber el total de reacciones por publicacion")
st.dataframe(publicationselection2)
graphicbypublicationbutton=sidebar.button('Graficar publicaciones seleccionadas')

def graphicreactionsbypublication(data):
    st.write("La siguiente grafica nos permitira comparar que publicacion tiene más reacciones")
    reactionsbypublicationbar=px.bar(data,
                            x=data.index,
                            y=data.values,
                            title="No. Reacciones por publicacion",
                            template="plotly_white"
                            )
    reactionsbypublicationbar.update_layout(xaxis_title="Publications", yaxis_title="No.Reactions", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(reactionsbypublicationbar)

if (graphicbypublicationbutton):
    graphicreactionsbypublication(publicationselection2)

data=get_data()
selected_publication = sidebar.selectbox("Select piblication", data['publication'].unique())
btnFilterbypublication = sidebar.button('Filter by publication')

def filterbypublication(publication):
    return data[data['publication']==publication]


if (btnFilterbypublication):
    st.write("La siguiente informacion nos permite conocer el cuantas reacciones por tipo (like, love, fun, etc.) tiene la publicacion seleccionada")
    data_filtrada=filterbypublication(selected_publication)
    st.write(f"Publicacion: '{selected_publication}'")
    #data_filtrada=data_filtrada.groupby(['publication']+['reaction']).count()['name']
    #st.dataframe(data_filtrada)
    reactionsofpublications=data_filtrada.groupby(['reaction']).count()['name']
    st.dataframe(reactionsofpublications)
    #fig = px.bar(data_filtrada, x=['publication'], y=['name'], color=['reaction'], title="No. reacciones por tipo")
    reactions=px.scatter(reactionsofpublications,
                    x=reactionsofpublications.index,
                    y=reactionsofpublications.values,
                    title="No. Reacciones por tipo",
                    template="plotly_white"
                    )
    reactions.update_layout(xaxis_title="Reaccion", yaxis_title="No.Reactions", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(reactions)
    


#graphicbutton=sidebar.button('Grafica de barras')
def graphicbypublicationhisto(trackselected):
    if(len(trackselected)!=0):
        tags=["publication"]
        histotrack=px.histogram(trackselected,
            x=['reaction'],
            y=tags,
            barmode='group',
            title="Comparación de los tags presentes por canción",
            labels=dict(publication="Publication"),
            template="plotly_white"
        )
        histotrack.update_layout(yaxis_title="Valor del tag",plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(histotrack)
#if(graphicbutton):
    graphicbypublicationhisto(reactionsofpublications)



#st.write('results...')
#st.write(items)

# Print results.i
#for item in items:
#    st.write(f"{item['_id']} has a :{item['name']}:")
