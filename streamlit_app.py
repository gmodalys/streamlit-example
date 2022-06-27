import streamlit as st
import pandas as pd
import numpy as np

st.title(' Simulation Audrey')

st.subheader('Paramètres généraux Simulation:')
col1, col2, col3, col8 = st.columns(4)
with col1:
    nb_equipe = st.slider("Combien dans l'équipe ?", 1, 6,4)
with col2:
    nb_mois = st.slider('Sur combien de mois ?', 1, 24,12)
with col3:
    tjm = st.slider("TJM Moyen runner", 100,200,110,10,"%d €")

with col8:
    pourcent_perso = st.slider("% Perso Team", 10,100,40,10,"%d Prct")

st.subheader("Paramètres d'activité sur la période:")
col4, col5, col6 = st.columns(3)
with col4:
    nb_runner_month = st.slider('Nb Runner par mois par membre',0.5,5.0,1.0,0.1,"%s Runner")
with col5:
    tx_renouv = st.slider('Taux renouvellement Runner', 0, 100,10,10,"%s Prct") / 100
with col6:
    duree_moy_contrat = st.slider('Durée Moyenne Contrat', 3, 6,3,1,"%d Mois")


from_d = pd.date_range(start='07/01/2022', periods=nb_mois, freq='M')
print(from_d, duree_moy_contrat)
st.title('Résultats')


runners = []
nb_runner = 0
for x, m in enumerate(from_d): 

    nb_nx = nb_equipe * nb_runner_month
    
    l_r = len(runners)
    if l_r >= duree_moy_contrat:
        fin_pour = int(runners[l_r-duree_moy_contrat]['Nx Runner'] * (1-tx_renouv))
        delta = nb_nx - fin_pour
        nb_runner += delta
    else: 
        nb_runner += nb_nx
        delta = nb_nx
    
    
    res = {
        
        "Date":m,
        "Comm. Perso":int(nb_runner*tjm*(pourcent_perso/100)),
        "Nb Runner Total" :int(nb_runner),
        "Nx Runner":int(nb_nx),
        "Variation Runner":int(delta),
        "CA Total":int(nb_runner*tjm),
        

    }
    runners.append(res)

    
    
    
           
    
df = pd.DataFrame.from_dict(runners)
df.set_index('Date',inplace=True)
df['Total Perso'] = df['Comm. Perso'].cumsum()

if st.checkbox('Voir le détail des données'):
    st.dataframe(df) 

chart_data = df['Total Perso']
chart_data2 = df['Comm. Perso']

st.subheader("Comm. Perso Cumulées:")
col1, col2  = st.columns(2)
col1.metric("Total Comm", f"{df['Total Perso'].values[-1]} €")
col2.metric("Nb Runner Final", f"{df['Nb Runner Total'].values[-1]} Dev")
st.subheader("Graphique Commissions Perso Cumulées")

st.line_chart(chart_data)
if st.checkbox('Show detail Total'):
    st.write(chart_data)

st.subheader("Graphique Commissions Perso Mensuelles")
st.line_chart(chart_data2, use_container_width=True)
if st.checkbox('Show detail Mensuel'):
    st.write(chart_data2)


