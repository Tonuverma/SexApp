import streamlit as st
import sqlite3
from addparticipants import addparticipant
import numpy as np
import pandas as pd
from scipy.optimize import linprog
import solve5

dblocation = "db\\sexapp.db"


def get_selected_postures():
    conn = sqlite3.connect(dblocation)
    cursor = conn.cursor()

    query = cursor.execute('SELECT name FROM posturas')
    rows = query.fetchall()
    postures = list(map(lambda x: x[0], rows))
    cursor.close()
    conn.close()
    options_positions = st.multiselect('Selecciona las posturas', postures,
    default=postures[0], help="Seleccione las posturas que desea realizar en el acto sexual")
    return options_positions


def show_modelo_5():

    st.title(
        'Maximizar el placer inicial de un participante específico.')

    st.write("""
    En este modelo se intenta maximizar el placer inicial de un
    participante específico, de forma tal que
    todos los participantes, excepto el
    específico, alcancen el orgasmo. Para ello se utiliza una restricción extra sobre la persona que no
    debe alcanzar un orgasmo, y se maximiza una variable arbitraria h, que representa el placer inicial de dicha persona.
  """)

    optionsPositions = get_selected_postures()

    addparticipant()

    participants = st.session_state['persons']

    st.subheader('Energía consumida por unidad de tiempo')
    ECUT = [[] for item in range(len(participants))]
    for i in range(len(participants)):
        with st.expander(participants[i]):
            for j in range(len(optionsPositions)):
                ECUT[i].append(st.slider(optionsPositions[j], min_value=1,
                  max_value=1000, key='ECUT' + str(i*len(optionsPositions) + j)))

    # st.dataframe(ECUT)

    choice = st.sidebar.selectbox(
        'Selecciona la persona a marginar', participants, key='personsSideabar')
    personIndex = 0

    for i in range(len(participants)):
        if choice == participants[i]:
            personIndex = i

    st.subheader('Placer generado por unidad de tiempo')
    PGUT = [[]for item in range(len(participants))]
    for i in range(len(participants)):
        with st.expander(participants[i]):
            for j in range(len(optionsPositions)):
                PGUT[i].append(st.slider(optionsPositions[j], min_value=1,
                               max_value=100, key='ECUT' + str(i*len(optionsPositions) + j)))

    # st.dataframe(PGUT)

    st.subheader('Energía inicial de los participantes')
    EIP = []
    with st.expander('Energía inicial de cada participante'):
        for i in range(len(participants)):
            EIP.append(
                st.slider(participants[i], min_value=1, max_value=100, key='EIP' + str(i)))

    # st.bar_chart(EIP,use_container_width=False)

    st.subheader('Placer inicial de los particiapantes')
    PIP = []
    with st.expander('Placer inicial de los participantes'):
        for i in range(len(participants)):
            PIP.append(
                st.slider(participants[i], min_value=1, max_value=100, key='PIP' + str(i)))

    # st.bar_chart(PIP,use_container_width=False)

    st.subheader(
        'Niveles de placer de cada participante para obtener el orgasmo')
    NPPOO = []
    with st.expander('Niveles de placer para obtener el orgasmo'):
        for i in range(len(participants)):
            NPPOO.append(
                st.slider(participants[i], min_value=150, max_value=300, key='NPPOO' + str(i)))

    # st.bar_chart(NPPOO,use_container_width=False)

    st.empty()
    if st.button("Analyce"):
        result = solve5.Solve5thProblem(
            ECUT, PGUT, EIP, PIP, NPPOO, participants, optionsPositions, personIndex)

        sol = []
        for name in result.variables():
            if name.name == "H":
                continue

            sol.append(name.varValue)

        if result.status == 1:
            timeresult = pd.DataFrame(sol, index=optionsPositions)
            container = st.container()
            container.line_chart(timeresult)
            container.area_chart(timeresult)

            #Guaradando los placeres de todos en una lista de placeres [ persona[placer]]
            pleasureForEverybody = []
            for personIndex in range(len(participants)):
                temp1 = []
                for postureIndex in  range(len(optionsPositions)):
                    temp1.append(sol[postureIndex] * PGUT[personIndex][postureIndex])

                pleasureForEverybody.append(temp1)

                st.subheader('Gráfico de Placer por posición de '+participants[personIndex])
                data = pd.DataFrame({
                'index': optionsPositions,
                'Placer por posición': pleasureForEverybody[personIndex],
                }).set_index('index')
                st.bar_chart(data)

            #Guardando las energías de todos en una lista de energías [ persona[energía]]
            energyForEverybody = []
            for personIndex in range(len(participants)):
                temp1 = []
                for postureIndex in  range(len(optionsPositions)):
                    temp1.append(sol[postureIndex] * ECUT[personIndex][postureIndex])


                energyForEverybody.append(temp1)

                st.subheader('Gráfico de enrgía consumida por posición de '+participants[personIndex])
                data = pd.DataFrame({
                'index': optionsPositions,
                'Energía por posición': energyForEverybody[personIndex],
                }).set_index('index')
                st.bar_chart(data)



        elif result.status == 0:
            st.title('No se resolvió el problema.')

        elif result.status == -1:
            st.title('El problema es inviable.')

        elif result.status == -2:
            st.title('El problema es ilimitado.')

        elif result.status == -3:
            st.title('El problema es indefinido')
