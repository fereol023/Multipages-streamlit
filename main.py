from contents import *
from contents import page1, page2, page3

st.set_option('deprecation.showPyplotGlobalUse', False)

pages = {
    "Page 1 - CDM": page1.manipulation_text,
    "Page 2 - Villes": page2.villes,
    "Page 3 - Vélibs": page3.velibs
}

st.sidebar.title('Navigation')
p = st.sidebar.radio('Aller à ', list(pages.keys()))

pages[p]()