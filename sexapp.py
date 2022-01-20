from pygame import image
from scipy.optimize import linprog 
import streamlit as st
import sqlite3
from addposture import addposture
from addparticipants import addparticipant
from viewmodel1 import show_modelo_1
from viewmodel2 import show_modelo_2
from viewmodel3 import show_modelo_3

#ECUT : E consumida por unidad de tiempo [][]
#PGUT : Placer generado por unidad de Tiempo [][]
#EIP : Energía inicial del participante []
#PIP : Placer inicial de los participantes  []
#NPPOO : Placer necesario para alcanzar el orgasmo []
# Globals Varaibles
dblocation = None
MAX_LENGTH_DESCIPTION = 400
MIN_LENGTH_DESCIPTION = 10

# Initilize variables
if 'persons' not in st.session_state:
  st.session_state['persons'] = []


# def loadingconfigfile():
#   global dblocation
#   try:
#     file = open ('config.json', 'r')
#     config = json.load(file)
#     dblocation = config['DEFAULT']['DB_DIR']
#   except Exception as err:
#     print ('Error reading configuration file')

# loadingconfigfile()




# configurando las parametros de la pagina 
st.set_page_config( page_title='Sex App',
                    layout='centered',
                    page_icon= 'img\sex_icon.png',
                  )


# dandole un titulo a la Pagina 
st.title('Sex App')

# Titulo  de la barra lateral 
st.sidebar.header("Sex App")

# localizacion de la base de datos
dblocation = "db\\sexapp.db"

choice = st.sidebar.selectbox('Select view' ,['Modelo 1', 'Modelo 2' , 'Modelo 3' , 'Modelo 4' , 'Modelo 5' , 'Mostrar Posturas', 'Adicionar una postura'])

choicemodel1 = st.sidebar.selectbox('Select view', ['sdfsdf', 'afsdf'])


@st.cache
def get_postures_info():
  conn = sqlite3.connect(dblocation)
  cursor = conn.cursor() 
  query = cursor.execute('SELECT name,source,description , image FROM posturas')
  rows = query.fetchall()
  names = list(map(lambda x : x[0], rows))
  sources = list(map(lambda x : x[1], rows))
  descriptions = list(map(lambda x : x[2], rows))
  images = list(map(lambda x : x[3], rows))
  return (names, sources ,descriptions,images)

def show_all_postures():
  names, sources , descriptions ,images =  get_postures_info()
  for i in range (len(names)):
    with st.expander(names[i]):
      st.write(descriptions[i])
      if sources[i] is not None:
        st.image(sources[i])
      elif images[i] is not None:
        st.image(images[i])


if choice == 'Modelo 1':
  show_modelo_1()
elif choice == 'Modelo 2':
  show_modelo_2()
elif choice == 'Modelo 3':
    show_modelo_3()
elif choice == 'Modelo 4':
  show_modelo_4()
elif choice == 'Adicionar una postura':
  addposture()
elif choice == 'Mostrar Posturas':
  show_all_postures()
