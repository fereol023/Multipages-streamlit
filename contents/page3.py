from contents import *

def velibs():
    st.header('Vélibs à Paris')

    u_velib1 = st.file_uploader("Télécharger vélib1", type=["txt"])
    u_velib2 = st.file_uploader("Télécharger vélib2", type=["txt"])
    #velib1, velib2 = 'data/velib_t1.txt', 'data/velib_t2.txt'


    if u_velib1 and u_velib2:
        # charger ---------------------------------------------------------------
        #with open(StringIO(u_velib1.getvalue())) as f1:
        #content1 = json.load(StringIO(u_velib1.getvalue()).read())
        #velib1 = pd.DataFrame(content1)
        velib1 = pd.DataFrame(json.load(StringIO(u_velib1.getvalue().decode("utf-8"))))

        #with open(StringIO(u_velib2.getvalue())) as f2:
        #content2 = json.load(StringIO(u_velib2.getvalue()).read())
        #velib2 = pd.DataFrame(content2)
        velib2 = pd.DataFrame(json.load(StringIO(u_velib2.getvalue().decode("utf-8"))))
        # apercu -----------------------------------------------------------------
        df_dict = {'velib1': velib1, 'velib2': velib2}
        df_selected = st.radio("Aperçu jdd", list(df_dict.keys()))
        df = df_dict[df_selected]
        show_k = st.slider("Nombre de lignes dans l'aperçu",
                           min_value=1,
                           max_value=len(df),
                           value=1)
        st.write(df.head(show_k))

        # carte 1 -----------------------------------------------------------------
        france = folium.Map(location = [48.85, 2.39],
                zoom_start = 12)

        villes_dispo = list(set(df['contract_name']))
        ville_choisie = st.radio("Choisir la ville", villes_dispo)
        selection_villes = [ville_choisie]

        for i,row in df.loc[df['contract_name'].isin(selection_villes),:].dropna().iterrows():
            folium.CircleMarker([row['position']['lat'], row['position']['lng']], 
                                radius=2,
                                popup=None, 
                                tooltip=row['name'].split('-')[-1]).add_to(france)
            
        fig1 = st_folium(france, width=1000)
        #st.text("Les détails de la sélection sur cette carte sont ci-dessous.")
        #st.write(fig1)

        # carte 2 ------------------------------------------------------------------
        velib = pd.concat([velib1, velib2])

        red = Color("red")
        colors = list(red.range_to(Color("green").hex,10))
        
        def red(brightness):
            brightness = int(round(9 * brightness)) # convert from 0.0-1.0 to 0-255
            return colors[brightness]
        
        france2 = folium.Map(location=[48.856614, 2.39], zoom_start=12)

        for k,row in velib.iterrows():
            folium.CircleMarker(location=[row.position['lat'], row.position['lng']], 
                                fill_color=red(row.available_bikes/float(row.bike_stands)).hex,
                                tooltip=f"{row['name'].split('-')[-1]} : {str(row.available_bikes)} dispo(s) / {str(row.bike_stands)}",       
                                radius=7).add_to(france2)
        
        fig2 = st_folium(france2, width=1000)
        #st.text("Les détails de la sélection sur cette carte sont ci-dessous.")
        #st.write(fig2)