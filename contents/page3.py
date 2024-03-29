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
        st.text("Avec la carte suivante, nous pouvons visualiser la dispersion des stations de velib dans la ville de Paris.")
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

        st.text("Nous pouvons voir à l'aide de la carte suivante le nombre de velibs disponibles par station.")
        st.text("Sur cette carte les points chauds (orange) sont ceux où il y a plus de vélibs disponibles.")
        st.text("Inversément les points froids (bleus) sont ceux où il y a moins de vélibs.")

        velib['lat'] = velib.apply(lambda r: r['position']['lat'], axis=1)
        velib['lng'] = velib.apply(lambda r: r['position']['lng'], axis=1)
        velib['available_bikes'] = velib.apply(lambda r: float(r['available_bikes']), axis=1)

        start = [velib.lat.mean(), velib.lng.mean()]

        hmap = folium.Map(start, zoom_start=12)

        hm = HeatMap(
                list(zip(velib.lat.values, velib.lng.values, velib.available_bikes.values)),
                min_opacity = .2,
                radius=20, blur=15, max_zoom=1
        )

        hmap.add_child(hm)
        fig2 = st_folium(hmap, width=1000)
