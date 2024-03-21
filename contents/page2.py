from contents import *

def villes():
    st.header("Villes")

    file = st.file_uploader("Télécharger fichier villes.txt", type=["txt"])

    if file is not None:
        st.title("Apercu des données")
        villes = pd.read_csv(file, delimiter='\t')

        # rename cols / transform names (cf. focntion dans /pages/__init__.py)
        transform_names(villes)

        # apercu  ----------------------------------------------------------------------
        show_k = st.slider("Nombre de lignes aperçu", 
                           min_value=1, 
                           max_value=len(villes),
                           value=1)
        data_apercu = villes.tail(show_k)
        st.write(data_apercu)

        # nbre de codes insee différents en suppr les doublons -------------------------
        insee = list(set(villes['Code_INSEE'].values))
        res_3=f"Il y a {len(insee)} Codes INSEE différents."
        st.write(res_3)

        # -------------------------------------------------------------------
        res_4="Les données numériques sont : Latitude, Longitude et Eloignement de chaque ville."
        st.text(res_4)

        numeric = ['Latitude', 'Longitude', 'Eloignement']
        numeric_cast(villes, cols=numeric)
        st.write(round(villes[numeric].describe().iloc[[0,1,7],:], 2))

        # nbre de villes par région   -------------------------------------------------
        res_5 ="Le nombre de villes par régions est donnée par :"
        regions = villes[['NomVille', 'Code_Région']]
        regions = regions.groupby('Code_Région').size().to_dict()
        regions = dict(sorted(regions.items(), key=lambda v: v[0]))
        st.text(res_5)
        st.write(regions)
    
        france = folium.Map(location = [47, 3], zoom_start = 6)
        transform_villes(villes)
        liste_selection_villes = ['PARIS', 'MARSEILLE', 'RENNES', 'NIORT']
        selection_villes = [st.radio("Choisir les villes à afficher", liste_selection_villes)]
        
        for i,row in villes.loc[villes['MAJ'].isin(selection_villes),['NomVille', 'MAJ', 'Latitude', 'Longitude']].dropna().iterrows():
            print(row)
            folium.Marker([row['Latitude'], row['Longitude']],
                          popup=row['NomVille']).add_to(france)
            
        fig = st_folium(france, width=1000)