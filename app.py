import streamlit as st
import pandas as pd
import re
import os
import time
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from streamlit_gsheets import GSheetsConnection

# --- 1. Configuração da Página e Estilo ---
st.set_page_config(
    page_title="Análise de Sentimentos CPWPI 2025",
    page_icon="🤖",
    layout="wide",
)

# CSS para o tema da Campus Party
st.markdown("""
<style>
    .stApp { background-color: #0A1A33; color: #FFFFFF; }
    h1, h2, h3 { color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #1E293B; }
    .main .block-container { padding: 2rem; }
    .stButton > button {
        border: 2px solid #EC008C; color: #FFFFFF; background-color: #EC008C;
        border-radius: 8px;
    }
    .stButton > button:hover {
        border-color: #D1E038; color: #0A1A33; background-color: #D1E038;
    }
    .stTextArea > div > div > textarea {
        background-color: #1E293B; color: #FFFFFF; border: 1px solid #EC008C;
    }
    [data-testid="stProgressBar"] > div > div {
        background-image: linear-gradient(to right, #EC008C, #D1E038);
    }
</style>
""", unsafe_allow_html=True)


# --- 2. Funções do Mock Model e Análise de Texto ---
def predict_mock_sentiment(texto_input):
    if not isinstance(texto_input, str) or not texto_input.strip(): return "Indefinido", 0.0
    texto = texto_input.lower()
    palavras_positivas = ['bom', 'ótimo', 'excelente', 'incrível', 'maravilhoso', 'adorei', 'gostei', 'recomendo', 'perfeito', 'fantástico', 'amei', 'sucesso', 'parabéns', 'top', 'show', 'curti']
    palavras_negativas = ['ruim', 'péssimo', 'horrível', 'terrível', 'odeio', 'detestei', 'lixo', 'fraude', 'enganação', 'não gostei', 'decepcionado', 'decepção', 'frustrante', 'esperava mais', 'lamentável', 'desagradável', 'deixou a desejar', 'problema', 'atraso', 'quebrado', 'falha', 'erro', 'defeito', 'complicado', 'não funciona', 'fraco', 'mal feito', 'desorganizado', 'confuso', 'difícil', 'pouco']
    if any(palavra in texto for palavra in palavras_positivas): return "Positivo", 0.95
    if any(palavra in texto for palavra in palavras_negativas): return "Negativo", 0.92
    return "Neutro", 0.85

# --- 3. Conexão com a Planilha Google ---
# !!! LINK DA SUA PLANILHA INSERIDO ABAIXO !!!
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1J9x2c5js1FvVrLl5juaQSJPXn_tIvmsv5ee6slwqjbk/edit?usp=sharing"

# Função para carregar e processar os dados da planilha
@st.cache_data(ttl=60) # Atualiza os dados a cada 60 segundos
def carregar_dados():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        dados = conn.read(spreadsheet=GOOGLE_SHEET_URL, usecols=[1]) # Lê apenas a segunda coluna (Comentário)
        # O Google Forms pode criar colunas vazias, vamos limpá-las
        dados.dropna(inplace=True)
        # Renomear a coluna para algo mais amigável
        if not dados.empty:
            dados.columns = ['Comentário']
        return dados
    except Exception as e:
        st.error(f"Não foi possível carregar os dados da planilha. Verifique o link e as permissões de partilha. Erro: {e}")
        return pd.DataFrame(columns=['Comentário'])

# --- 4. Páginas da Aplicação ---

# Navegação na Barra Lateral
st.sidebar.title("🚀 Navegação")
pagina = st.sidebar.radio("Escolha uma página:", ["Dashboard ao Vivo", "Analisador Individual"])

# ----- PÁGINA 1: DASHBOARD AO VIVO -----
if pagina == "Dashboard ao Vivo":
    st.title("📊 Dashboard de Sentimentos ao Vivo")
    st.markdown("Veja em tempo real o que as pessoas estão a comentar sobre o evento!")

    # Botão para atualizar os dados manualmente
    if st.button("🔄 Atualizar Dados"):
        st.cache_data.clear() # Limpa o cache para forçar a recarga

    dados_comentarios = carregar_dados()

    if dados_comentarios.empty:
        st.info("Ainda não há comentários. Seja o primeiro a participar!")
    else:
        # Análise de Sentimentos em Lote
        sentimentos = dados_comentarios['Comentário'].apply(lambda x: predict_mock_sentiment(x)[0])
        contagem_sentimentos = sentimentos.value_counts()

        # Layout em Colunas
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Sentimento Geral")
            # Verifica se há dados para plotar
            if not contagem_sentimentos.empty:
                fig, ax = plt.subplots()
                ax.pie(contagem_sentimentos, labels=contagem_sentimentos.index, autopct='%1.1f%%', startangle=90, colors=['#D1E038', '#ff4b4b', '#ffc107'])
                ax.axis('equal')  # Garante que a pizza seja um círculo.
                st.pyplot(fig)
            else:
                st.warning("Não há dados de sentimento para exibir.")

        with col2:
            st.subheader("Nuvem de Palavras")
            texto_completo = " ".join(comentario for comentario in dados_comentarios['Comentário'])
            # Verifica se há texto para gerar a nuvem
            if texto_completo.strip():
                stopwords_pt = set(STOPWORDS)
                stopwords_pt.update(["pra", "pro", "tá", "né", "da", "de", "do", "na", "no", "uma", "um", "que", "se", "por"])
                wordcloud = WordCloud(stopwords=stopwords_pt, background_color="#0A1A33", colormap="viridis", width=800, height=400).generate(texto_completo)
                
                fig_wc, ax_wc = plt.subplots()
                ax_wc.imshow(wordcloud, interpolation='bilinear')
                ax_wc.axis("off")
                st.pyplot(fig_wc)
            else:
                st.warning("Não há palavras suficientes para gerar a nuvem.")

        st.markdown("---")
        st.subheader("Últimos Comentários")
        st.dataframe(dados_comentarios.tail(10), use_container_width=True)


# ----- PÁGINA 2: ANALISADOR INDIVIDUAL -----
elif pagina == "Analisador Individual":
    st.title("🧠 Classificador de Sentimentos em Português")
    st.subheader("Teste o nosso modelo com qualquer texto que desejar.")

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
            if sentimento == "Positivo": st.markdown("- **Prioridade:** Baixa\n- **Recomendações:** Agradecer o feedback.")
            elif sentimento == "Negativo": st.markdown("- **Prioridade:** Alta\n- **Recomendações:** Contacto urgente, analisar causa raiz.")
            else: st.markdown("- **Prioridade:** Média\n- **Recomendações:** Monitorizar a conversa.")

# --- 5. Barra Lateral ---
st.sidebar.markdown("---")
st.sidebar.success("Modelo de Demonstração Ativo!")
st.sidebar.info("Este é um projeto educacional desenvolvido para fins de demonstração.")

