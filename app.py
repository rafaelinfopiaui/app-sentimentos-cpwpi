import streamlit as st
import re
import time
import os
import base64

# --- 1. Configuração da Página ---
st.set_page_config(
    page_title="Análise de Sentimentos CPWPI 2025",
    page_icon="🤖",
    layout="wide", # Usar layout 'wide' para o banner do cabeçalho
)

# --- 2. Estilo Visual Otimizado ---

# Paleta de Cores (Extraída do site oficial):
# Fundo Principal (Azul Escuro): #0A1A33
# Fundo da Barra Lateral (Azul Escuro, um pouco mais claro): #1E293B
# Acento Principal (Magenta): #EC008C
# Acento Secundário (Amarelo-Limão): #D1E038
# Texto Principal (Branco): #FFFFFF

st.markdown("""
<style>
    /* --- Fundo Sólido e Cores Gerais --- */
    .stApp {
        background-color: #0A1A33; /* Fundo azul escuro principal */
        color: #FFFFFF;
    }
    h1, h2, h3 {
        color: #FFFFFF;
    }

    /* --- Barra Lateral --- */
    [data-testid="stSidebar"] {
        background-color: #1E293B; /* Tom ligeiramente diferente para contraste */
    }

    /* --- Container Principal (para melhor legibilidade) --- */
    /* Remove o padding padrão do bloco principal para o banner ocupar toda a largura */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* --- Componentes Interativos --- */
    .stButton > button {
        border: 2px solid #EC008C;
        color: #FFFFFF;
        background-color: #EC008C;
        border-radius: 8px;
    }
    .stButton > button:hover {
        border-color: #D1E038;
        color: #0A1A33;
        background-color: #D1E038;
    }
    .stTextArea > div > div > textarea {
        background-color: #1E293B;
        color: #FFFFFF;
        border: 1px solid #EC008C;
    }
    [data-testid="stProgressBar"] > div > div {
        background-image: linear-gradient(to right, #EC008C, #D1E038);
    }
</style>
""", unsafe_allow_html=True)


# --- 3. Mock Model (Modelo Simulado) ---
def predict_mock_sentiment(texto_input):
    if not isinstance(texto_input, str) or not texto_input.strip():
        return "Indefinido", 0.0
    texto = texto_input.lower()
    palavras_positivas = [
        'bom', 'ótimo', 'excelente', 'incrível', 'maravilhoso', 'adorei', 'gostei',
        'recomendo', 'perfeito', 'fantástico', 'amei', 'sucesso', 'parabéns', 'top',
        'show', 'curti'
    ]
    palavras_negativas = [
        'ruim', 'péssimo', 'horrível', 'terrível', 'odeio', 'detestei', 'lixo',
        'fraude', 'enganação', 'não gostei', 'decepcionado', 'decepção',
        'frustrante', 'esperava mais', 'lamentável', 'desagradável', 'deixou a desejar',
        'problema', 'atraso', 'quebrado', 'falha', 'erro', 'defeito', 'complicado',
        'não funciona', 'fraco', 'mal feito', 'desorganizado', 'confuso', 'difícil', 'pouco'
    ]
    if any(palavra in texto for palavra in palavras_positivas):
        return "Positivo", 0.95
    if any(palavra in texto for palavra in palavras_negativas):
        return "Negativo", 0.92
    return "Neutro", 0.85

# --- 4. Interface Gráfica do Streamlit ---

# BANNER NO CABEÇALHO
if os.path.exists("banner_home-CPWeekendPiaui2-1.png"):
    # CORREÇÃO APLICADA AQUI:
    st.image("banner_home-CPWeekendPiaui2-1.png", use_container_width=True)

st.title("🧠 Classificador de Sentimentos em Português")
st.subheader("Projeto de Extensão: CP Weekend Piauí 2025")

texto_usuario = st.text_area(
    "Insira um texto para análise:",
    "A Campus Party Weekend Piauí é um evento incrível, mal posso esperar!",
    height=150,
    label_visibility="collapsed"
)

if st.button("Analisar Sentimento"):
    with st.spinner('A analisar o texto...'):
        time.sleep(1)
        sentimento, confianca = predict_mock_sentiment(texto_usuario)

    st.markdown("---")
    st.write("### Resultado da Análise:")

    cor_sentimento = "#D1E038" if sentimento == "Positivo" else "#ff4b4b" if sentimento == "Negativo" else "#ffc107"
    st.markdown(f"**Sentimento Identificado:** <span style='color:{cor_sentimento}; font-weight: bold;'>{sentimento}</span>", unsafe_allow_html=True)

    st.progress(float(confianca), text=f"Confiança: {confianca:.1%}")

    with st.expander("Ver Plano de Ação Sugerido", expanded=True):
        if sentimento == "Positivo":
            st.markdown("- **Prioridade:** Baixa\n- **Recomendações:** Agradecer o feedback, partilhar com a equipa como motivação.")
        elif sentimento == "Negativo":
            st.markdown("- **Prioridade:** Alta\n- **Recomendações:** Contacto urgente, analisar causa raiz, oferecer solução.")
        else: # Neutro
            st.markdown("- **Prioridade:** Média\n- **Recomendações:** Monitorizar a conversa, obter mais detalhes com pesquisa de satisfação.")

# --- 5. Barra Lateral ---
st.sidebar.success("Modelo de Demonstração Ativo!")
st.sidebar.info("Este é um projeto educacional desenvolvido para fins de demonstração.")
st.sidebar.markdown("---")

# Logo da Campus Party na sidebar
if os.path.exists("CPWeekend_Piaui.png"):
    col1_side_cp, col2_side_cp, col3_side_cp = st.sidebar.columns([1,2,1])
    with col2_side_cp:
        st.image("CPWeekend_Piaui.png", width=150)

st.sidebar.markdown("### Sobre o Projeto")
st.sidebar.markdown(f"**Desenvolvimento:** Equipa do Projeto de Extensão do Curso de Bacharelado em Engenharia de Computação com IA do Centro Universitário Tecnológico de Teresina - UNI-CET")

if os.path.exists("unicet_white.png"):
    col1_side, col2_side, col3_side = st.sidebar.columns([1,2,1])
    with col2_side:
        st.image("unicet_white.png", width=150)

if os.path.exists("ENG-CIA logo.png"):
    col1_side2, col2_side2, col3_side2 = st.sidebar.columns([1,2,1])
    with col2_side2:
        st.image("ENG-CIA logo.png", width=150)

