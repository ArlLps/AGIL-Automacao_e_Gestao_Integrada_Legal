import streamlit as st
from modules.core import settings as core_settings
from modules.ui.sidebar import render_sidebar

product_name = core_settings.get_product_name()

st.set_page_config(
    page_title=f"{product_name} | Início",
    page_icon="⚙️",
    layout="wide",
)

render_sidebar(active_page="inicio")

st.title(f"⚙️ {product_name} | Início")
st.caption(core_settings.get_homepage_caption())

st.subheader("Interface inicial")

module_options = {
    "ATAs": {
        "description": "Automação de geração, revisão e gestão de ATAs da organização.",
        "page": "pages/01_ATAs.py",
        "status": "Disponível",
    },
    "Contratos": {
        "description": "Preenchimento automático de contratos e envio para assinatura via Authentique.",
        "page": "pages/02_Contratos.py",
        "status": "Disponível",
    },
    "Gerenciamento": {
        "description": "Central administrativa para gerenciar prompts, membros, templates e acervos do sistema.",
        "page": "pages/03_Gerenciamento.py",
        "status": "Disponível",
    }
}

selected_module = st.selectbox(
    "Escolha o módulo que deseja acessar:",
    options=list(module_options.keys()),
    index=0,
)

selected_info = module_options[selected_module]
st.write(f"**Status:** {selected_info['status']}")
st.write(selected_info["description"])

if selected_info["page"]:
    if st.button("Acessar módulo", type="primary"):
        st.switch_page(selected_info["page"])
else:
    st.info("Este módulo ainda não está disponível.")
