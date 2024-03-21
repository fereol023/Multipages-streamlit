from contents import *

def manipulation_text():
    st.header("Coupe du monde")
    st.subheader("Réalisé par Féréol")

    file = st.file_uploader("Télécharger fichier excel", type=["xlsx"])
    if file is not None:
        st.title("Data overview")
        data = pd.read_excel(file, engine="openpyxl")
        show_k = st.slider("Nombre de lignes aperçu", 
                           min_value=1, 
                           max_value=len(data),
                           value=1)
        data_apercu = data.tail(show_k)
        st.write(data_apercu)

        st.text("Nombre de joueurs par équipe")
        
        teams = data[['Team', 'Name']]
        teams = teams.groupby('Team').size().to_dict()
        teams = dict(sorted(teams.items(), key=lambda v: v[1]))
        st.write(teams)
        st.text("La plupart des équipes ont 23 joueurs.")

        st.text("Les 3 joueurs avec le plus de distance")
        players = clean_data(data[['Name', 'Distance Covered', 'Location']])
        players = players.sort_values(by=['Distance Covered'], ascending=False, na_position='last') 
        players.head(3)

        st.title('Distance parcourue') 
        players2 = clean_data(data[['Name', 'Distance Covered', 'Location', 'Distance Covered In Possession', 'Distance Covered Not In Possession']])
        players2 = players2.sort_values(by=['Distance Covered', 'Distance Covered In Possession', 'Distance Covered Not In Possession'], 
                                ascending=True, na_position='last')

        fig, axs = plt.subplots(2,1,figsize=(15,30))
        plt.title('Distance parcourue vs Distance parcourue avec le ballon')
        sns.scatterplot(x='Distance Covered', y='Distance Covered In Possession', data=players2, hue='Location', ax=axs[0])
        plt.title('Distance parcourue vs Distance parcourue avec le ballon')
        sns.scatterplot(x='Distance Covered', y='Distance Covered Not In Possession', data=players2, hue='Location', ax=axs[1])
        plt.legend()
        plt.tight_layout()
        st.pyplot()

        st.text("Les joueurs qui parcourent le plus de distance sont aussi sont qui parcourent le plus de distance avec le ballon.")

        
        #4. Identifiez les joueurs qui sont dans le premier décile des joueurs les
        #plus rapides en calculant le décile et sélectionnez les joueurs qui y
        #appartiennent. Ensuite, analysez le temps passé à courir sans la balle
        #pour ces joueurs et identifiez celui qui a passé le plus clair de son
        #temps à courir sans la balle.
        speed = clean_data(data[['Name', 'Location', 'Top Speed']])
        plt.figure(figsize=(10,3))
        plt.title('Boxplot de la vitesse des joueurs.')
        sns.boxplot(speed['Top Speed'], orient='h')
        st.pyplot()

        deciles_steps = np.linspace(0.1, 0.9, 9)
        deciles = list(speed['Top Speed'].quantile(deciles_steps))
        st.text(f"Le 1er décile est {deciles[0]}. 90% des joueurs ont couru plus vite que cette vitesse.") # premier decile

        speed_low=speed.loc[speed['Top Speed'] < deciles[0],:].sort_values(by=['Top Speed'], ascending=True) # les joeurs du permeir decile sorted
        st.text("Les 10% les plus lents")
        st.write(speed_low.head(3))
        
        st.text("Parmis les plus lents, ceux qui ont passé leur temps à courir sans le ballon")
        very_low_lazy = players2[players2['Name'].isin(speed_low['Name'].to_list())]\
                         .sort_values(by=['Distance Covered Not In Possession'], ascending=False)\
                         .head(3)
        st.write(very_low_lazy)


    """
    st.sidebar.header('Params')
    plot_type = st.sidebar.selectbox('Type', ['Histogramme', 'Scatterplot'])

    data = {
        'x': np.random.randint(100, 1000, size=100),
        'y': np.random.randint(100, 1000, size=100)
    }
    data = pd.DataFrame(data)

    st.write(data)
    st.title('Titre')
    if plot_type == 'Histogramme':
        sns.histplot(data['x'], kde=True)
        st.pyplot()
    elif plot_type == 'Scatterplot':
        st.header('Scatterplot')
        sns.scatterplot(x='x', y='y', data=data)
        st.pyplot()
    """
