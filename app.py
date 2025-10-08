import streamlit as st
import re
import time # Usado para simular um pequeno atraso
import os   # Importado para verificar a existência dos ficheiros de imagem

# --- 1. Configuração da Página ---
st.set_page_config(
    page_title="Análise de Sentimentos CPWPI 2025",
    page_icon="🤖",
    layout="centered",
)

# --- FUNÇÃO SIMPLIFICADA PARA APLICAR O FUNDO ---
def set_page_background(image_file):
    if os.path.exists(image_file):
        # Apenas injeta o CSS para usar o ficheiro de imagem local como fundo
        page_bg_css = f'''
        <style>
        .stApp {{
            background-image: url("app/static/{image_file}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* Adicionar uma sobreposição para melhorar a legibilidade do texto */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(10, 26, 51, 0.7); /* Sobreposição Azul Escuro com 70% de opacidade */
            z-index: -1;
        }}
        </style>
        '''
        st.markdown(page_bg_css, unsafe_allow_html=True)

# Aplicar a imagem de fundo com o novo nome do ficheiro
# IMPORTANTE: Certifique-se de que o nome do ficheiro aqui é exatamente igual ao do seu repositório.
set_page_background('banner_home-CPWeekendPiaui2-1.png')


# --- CSS CUSTOMIZADO COM O TEMA OFICIAL DA CAMPUS PARTY PIAUÍ ---
st.markdown("""
<style>
    /* Remover a cor de fundo sólida, pois agora temos uma imagem */
    .stApp {
        background-color: transparent;
    }

    /* Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #0A1A33; /* Azul Escuro */
    }
    
    /* Cor do texto geral e na barra lateral */
    .stApp, [data-testid="stSidebar"] * {
        color: #FFFFFF;
    }
    
    /* Títulos e Subtítulos no corpo principal */
    h1, h2, h3 {
        color: #FFFFFF;
    }

    /* Botão Principal */
    .stButton > button {
        border: 2px solid #EC008C; /* Magenta */
        color: #FFFFFF;
        background-color: #EC008C;
        border-radius: 8px;
    }
    .stButton > button:hover {
        border-color: #D1E038; /* Amarelo-Limão */
        color: #0A1A33;
        background-color: #D1E038;
    }
    
    /* Cor de fundo da caixa de texto */
    .stTextArea > div > div > textarea {
        background-color: rgba(10, 26, 51, 0.8); /* Fundo da caixa de texto mais opaco */
        color: #FFFFFF;
        border: 1px solid #EC008C;
    }
    
    /* Barra de Progresso */
    [data-testid="stProgressBar"] > div > div {
        background-image: linear-gradient(to right, #EC008C, #D1E038);
    }
</style>
""", unsafe_allow_html=True)


# --- 2. O NOSSO "MOCK MODEL" (MODELO SIMULADO) ---
def predict_mock_sentiment(texto_input):
    if not isinstance(texto_input, str) or not texto_input.strip():
        return "Indefinido", 0.0
    texto = texto_input.lower()
    palavras_positivas = [
        'bom', 'ótimo', 'excelente', 'incrível', 'maravilhoso', 'adorei',
        'gostei', 'recomendo', 'perfeito', 'fantástico', 'amei', 'sucesso',
        'parabéns', 'top', 'show', 'curti'
    ]
    palavras_negativas = [
        'ruim', 'péssimo', 'horrível', 'terrível', 'odeio', 'detestei',
        'lixo', 'fraude', 'enganação', 'não gostei', 'decepcionado', 'decepção', 
        'frustrante', 'esperava mais', 'lamentável', 'desagradável', 'deixou a desejar',
        'problema', 'atraso', 'quebrado', 'falha', 'erro', 'defeito', 'complicado',
        'não funciona', 'fraco', 'mal feito', 'desorganizado', 'confuso', 'difícil', 'pouco'
    ]
    if any(palavra in texto for palavra in palavras_positivas):
        return "Positivo", 0.95
    if any(palavra in texto for palavra in palavras_negativas):
        return "Negativo", 0.92
    return "Neutro", 0.85

# --- 3. Interface Gráfica do Streamlit ---

# --- CABEÇALHO COM LOGO PRINCIPAL ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("CPWeekend_Piaui.png"):
        st.image("CPWeekend_Piaui.png", width=300)

st.title("🧠 Classificador de Sentimentos em Português")
st.subheader("Projeto de Extensão: CP Weekend Piauí 2025")

texto_usuario = st.text_area(
    "Insira um texto para análise:",
    "A Campus Party Weekend Piauí é um evento incrível, mal posso esperar!",
    height=150
)

if st.button("Analisar Sentimento"):
    with st.spinner('A analisar o texto...'):
        time.sleep(1)
        sentimento, confianca = predict_mock_sentiment(texto_usuario)

    st.markdown("---")
    st.write("### Resultado da Análise:")
    
    # As cores aqui agora serão usadas apenas para o texto de resultado
    cor_sentimento = "#D1E038" if sentimento == "Positivo" else "#ff4b4b" if sentimento == "Negativo" else "#ffc107"
    st.markdown(f"**Sentimento Identificado:** <span style='color:{cor_sentimento}; font-weight: bold;'>{sentimento}</span>", unsafe_allow_html=True)
    
    st.progress(float(confianca), text=f"Confiança: {confianca:.1%}")

    with st.expander("Ver Plano de Ação Sugerido", expanded=True):
        if sentimento == "Positivo":
            st.markdown("- **Prioridade:** Baixa")
            st.markdown("- **Recomendações:** Agradecer o feedback, partilhar com a equipa como motivação.")
        elif sentimento == "Negativo":
            st.markdown("- **Prioridade:** Alta")
            st.markdown("- **Recomendações:** Contacto urgente, analisar causa raiz, oferecer solução.")
        else: # Neutro
            st.markdown("- **Prioridade:** Média")
            st.markdown("- **Recomendações:** Monitorizar a conversa, obter mais detalhes com pesquisa de satisfação.")

# --- 4. Barra Lateral e Rodapé ---
st.sidebar.success("Modelo de Demonstração Ativo!")
st.sidebar.info("Este é um projeto educacional desenvolvido para fins de demonstração.")
st.sidebar.markdown("---")


st.sidebar.markdown("### Sobre o Projeto")
st.sidebar.markdown(f"**Desenvolvimento:** Equipe do Projeto de Extensão do Curso de Bacharelado em Engenharia de Computação com IA do Centro Universitário Tecnológico de Teresina - UNI-CET")

if os.path.exists("unicet_white.png"):
    col1, col2, col3 = st.sidebar.columns([1,2,1])
    with col2:
        st.image("unicet_white.png", width=150)

if os.path.exists("ENG-CIA logo.png"):
    col1, col2, col3 = st.sidebar.columns([1,2,1])
    with col2:
        st.image("ENG-CIA logo.png", width=150)

