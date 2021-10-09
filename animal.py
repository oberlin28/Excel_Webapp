import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import openpyxl as xl
from pathlib import Path 
import base64

st.set_page_config(page_title='App.Conflits-DFRC', 
					 layout="wide",
				     initial_sidebar_state="expanded")

def main():

    


		header = st.container()
		dataset = st.container()
		model_training = st.container()
		st.sidebar.image("minef.png", use_column_width=False, width=50)
		st.sidebar.header('CONTROLEUR DE DONNEES')

		with header:




				st.title("APP.CONFLITS : Gestion des données CHF")

				st.markdown("""
					Cette Application est une version béta (en cours de developpement). Elle presente
					les données des differents conflits homme-faune de 2011 à Juillet 2021 à travers tout le pays.
					* ** Source de données:** Données fournies par les Directions Régionales des Eaux et Forêts.
					* ** traitement de données:** Direction de la Faune et des Services Cynégétiques (DFRC)
					""")

		with dataset:
				st.subheader("Données des CHF (2011 à Juillet 2021)")


				### --- BARRE LATERALE
				## st.sidebar.header('CONTROLEUR DE DONNEES')
				## selection_annee = st.sidebar.selectbox('Année de conflit', list(reversed(range(2011,2022))))

				### --- CHARGER DONNEES EXCEL

				df = pd.read_excel(io='conflit_faune.xlsx',
				                    sheet_name='DATA',
				                    usecols='A:G',
				                    header=1)
				st.dataframe(df)
				st.download_button(label='Telecharger données', data='conflit_faune.xlsx', file_name='donnees_CHF.xlsx')

				

				df_statistique = pd.read_excel(
									io='conflit_faune.xlsx',
				                    sheet_name='DATA',
				                    usecols='I:M',
				                    header=1)
				
				#CREATION DE COLONNE POUR DISPOSITION ELEMENTS  
				left_column, right_column = st.columns(2)
				#st.subheader('Effectif total par type de conflits')
				pie_chart_complet = pd.DataFrame(df['conflit'].value_counts())					
				left_column.markdown('__Effectif total par conflits__')
				left_column.bar_chart(pie_chart_complet, use_container_width=True)


				#st.subheader('Nombre de conflit par année')
				annee_diagramme = pd.DataFrame(df['annee'].value_counts())
				right_column.markdown('__Nombre de conflit par année__')
				right_column.bar_chart(annee_diagramme, use_container_width=True)


		with model_training:
					
					#AJOUTE BARRE LATERALE
					st.sidebar.subheader('Filtre des données')

					#AJOUT DES DONNEES DU FILTRE
					annee_var = df['annee'].unique().tolist()
					annee_selection = st.sidebar.multiselect('Annee de conflit :', annee_var, default=2020)

					conflit_var = df['conflit'].unique().tolist()
					conflit_selection = st.sidebar.multiselect('Type de conflit :', conflit_var, default='HOMME-ELEPHANTS')

					
					## FILTRE DE DONNEES PAR CONFLIT

					mask = (df['annee'].isin(annee_selection)) & (df['conflit'].isin(conflit_selection))
					number_of_result = df[mask].shape[0]
					st.sidebar.markdown(f'*Resultat disponible:{number_of_result}*')

					## GROUPER BLOC DE DONNEES APRES SELECTION
					df_grouper = df[mask].groupby(by=['conflit']).count()[['annee']]
					df_grouper = df_grouper.rename(columns = {'annee':'Nombre'})
					df_grouper = df_grouper.reset_index()

					
					## AFFICHE LE DIAGRAMME DU FILTRE 
					st.markdown("__Diagramme en Bande des données filtrées__")
					graphique = px.bar(df_grouper,
										x='conflit',
										y='Nombre',
										text='Nombre')
					st.plotly_chart(graphique)


# Run main()

if __name__ == '__main__':
    main()

