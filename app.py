import time
import streamlit as st
import yfinance as yf
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA (Tela Cheia e Escura)
st.set_page_config(
    page_title="XAUUSD Dashboard VIP",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# STYLING CSS: Design Premium Dark com proteção visual
st.markdown(
    """
    <style>
    /* Configuração do Fundo da Página Inteira */
    .stApp {
        background-image: linear-gradient(rgba(17, 19, 26, 0.94), rgba(17, 19, 26, 0.94)), 
                          url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=1200&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #FFFFFF !important;
    }
    
    /* Customização dos Blocos de Conteúdo */
    .bloco-premium {
        background-color: rgba(28, 32, 46, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px !important;
        border-radius: 12px !important;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
        min-height: 380px;
    }
    
    /* Caixa de Bloqueio Centralizada */
    .caixa-autenticacao {
        background-color: rgba(28, 32, 46, 0.95) !important;
        border: 2px solid #FFD700;
        padding: 40px !important;
        border-radius: 15px !important;
        max-width: 500px;
        margin: 50px auto !important;
        text-align: center;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.7);
    }
    
    div[data-testid="stMetric"] {
        background-color: rgba(38, 43, 62, 0.5) !important;
        padding: 10px !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stTable table {
        background-color: rgba(28, 32, 46, 0.85) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
    }
    .stTable th {
        background-color: rgba(38, 43, 62, 0.9) !important;
        color: #FFD700 !important;
    }
    .stTable td {
        color: #FFFFFF !important;
    }
    
    h1, h2, h3, p, span, label, .stSelectbox label {
        color: #FFFFFF !important;
    }
    
    .stSelectbox div[data-baseweb="select"], .stNumberInput input, .stTextInput input {
        background-color: #1C202E !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🔒 SISTEMA DE AUTENTICAÇÃO COM A SUA SENHA DEFINIDA
SENHA_CORRETA = "1401"

# Inicializa a memória do sistema para controlar o acesso se não existir
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

# Se o usuário NÃO estiver autenticado, mostra apenas a tela de bloqueio
if not st.session_state["autenticado"]:
    st.markdown("<div class='caixa-autenticacao'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #FFD700; margin-bottom: 5px;'>🔒 SISTEMA PROTEGIDO</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8A94A6; font-size: 14px;'>XAUUSD RADAR ELITE v1.0</p>", unsafe_allow_html=True)
    st.markdown("<p style='margin-top: 20px;'>Insira sua chave de acesso para liberar o terminal:</p>", unsafe_allow_html=True)
    
    senha_digitada = st.text_input("", type="password", placeholder="Digite a senha de 4 dígitos...")
    botao_entrar = st.button("Liberar Painel VIP 🦅")
    
    if botao_entrar:
        if senha_digitada == SENHA_CORRETA:
            st.session_state["autenticado"] = True
            st.success("Acesso autorizado! Carregando...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Chave inválida ou expirada! Fale com o suporte no WhatsApp.")
            
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin-top:30px;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px; color:#8A94A6;'>Aviso: Este painel possui licença temporária de uso individual.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Se o usuário digitar a senha certa, o sistema pula para cá e carrega a máquina completa
else:
    # Botão discreto no topo para deslogar se necessário
    col_topo1, col_topo2 = st.columns([9, 1])
    with col_topo2:
        if st.button("Sair 🔓"):
            st.session_state["autenticado"] = False
            st.rerun()

    # Título principal estilizado
    st.markdown("<h1 style='text-align: center; color: #FFD700 !important;'>🦅 XAUUSD RADAR ELITE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8A94A6 !important;'>TERMINAL QUANTITATIVO & CALCULADORA DE RISCO INSTITUCIONAL</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Seletor de Tempo Gráfico principal
    opcao = st.selectbox(
        "Selecione o Tempo Gráfico para Operação:",
        (
            "1 Minuto (M1)",
            "5 Minutos (M5)",
            "15 Minutos (M15)",
            "30 Minutos (M30)",
            "1 Hora (H1)",
            "1 Dia (D1)",
        ),
    )

    mapa_tempos = {
        "1 Minuto (M1)": ("1m", "M1", 15, "2d"),      
        "5 Minutos (M5)": ("5m", "M5", 25, "5d"),     
        "15 Minutos (M15)": ("15m", "M15", 45, "5d"),   
        "30 Minutos (M30)": ("30m", "M30", 60, "5d"),   
        "1 Hora (H1)": ("1h", "H1", 240, "60d"),       
        "1 Dia (D1)": ("1d", "D1", 1440, "60d"),       
    }
    tempo_grafico, texto_tempo, minutos_sugeridos, periodo_maximo = mapa_tempos[opcao]

    st.markdown("---")

    # ESPAÇO DA CALCULADORA DE RISCO FIXA NA TELA
    col_calc1, col_calc2, col_calc3, col_calc4 = st.columns(4)
    with col_calc1:
        banca = st.number_input("Tamanho da Banca ($):", min_value=10.0, value=1000.0, step=100.0)
    with col_calc2:
        pct_risco = st.number_input("Risco por Operação (%):", min_value=0.1, max_value=5.0, value=1.0, step=0.5)
    with col_calc3:
        stop_pips = st.number_input("Tamanho do Stop (Pips/Pontos):", min_value=10, value=300, step=50)
    with col_calc4:
        risco_financeiro = banca * (pct_risco / 100.0)
        lote_sugerido = risco_financeiro / stop_pips if stop_pips > 0 else 0.01
        lote_sugerido = max(0.01, round(lote_sugerido, 2))
        
        st.markdown("<p style='margin-bottom:0px; font-weight:bold; color:#FFD700;'>📐 LOTE RECOMENDADO:</p>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='margin-top:0px; color:#00FF7F;'>{lote_sugerido:.2f}</h2>", unsafe_allow_html=True)

    st.markdown("---")

    # Espaço dinâmico onde os cálculos gráficos vão rodar
    espaco_dashboard = st.empty()

    ativo = "GC=F"

    while st.session_state["autenticado"]:
        try:
            gold = yf.Ticker(ativo)
            
            hist = gold.history(period=periodo_maximo, interval=tempo_grafico)
            hist_h1 = gold.history(period="60d", interval="1h")

            if not hist.empty and len(hist) > 15 and not hist_h1.empty:
                fechamentos = hist["Close"]
                preco_atual = fechamentos.iloc[-1]

                # 1. CÁLCULOS DO GRAFICO ATUAL
                pontos_alta = 0
                pontos_baixa = 0

                ma9 = fechamentos.rolling(window=9).mean().iloc[-1]
                ma21 = fechamentos.rolling(window=21).mean().iloc[-1]
                status_media = "🟢 COMPRA" if ma9 > ma21 else "🔴 VENDA"
                if ma9 > ma21: pontos_alta += 3
                else: pontos_baixa += 3

                delta = fechamentos.diff()
                ganho = delta.clip(lower=0).rolling(window=14).mean()
                perda = (-delta.clip(upper=0)).rolling(window=14).mean()
                rs = ganho / (perda + 1e-10)
                rsi_atual = (100 - (100 / (1 + rs))).iloc[-1]

                status_rsi = "⚪ NEUTRO"
                if rsi_atual < 30:
                    status_rsi = "🔵 REVERSÃO ALTA"
                    pontos_alta += 2
                elif rsi_atual > 70:
                    status_rsi = "🟠 REVERSÃO BAIXA"
                    pontos_baixa += 2

                ema12 = fechamentos.ewm(span=12, adjust=False).mean()
                ema26 = fechamentos.ewm(span=26, adjust=False).mean()
                macd_linha = ema12 - ema26
                sinal_linha = macd_linha.ewm(span=9, adjust=False).mean()

                status_macd = "🟢 IMPULSO COMP" if macd_linha.iloc[-1] > sinal_linha.iloc[-1] else "🔴 IMPULSO VEND"
                if macd_linha.iloc[-1] > sinal_linha.iloc[-1]: pontos_alta += 2
                else: pontos_baixa += 2

                total_pontos = pontos_alta + pontos_baixa
                chance_alta = int((pontos_alta / total_pontos) * 100) if total_pontos > 0 else 50
                chance_alta = max(10, min(90, chance_alta))
                chance_baixa = 100 - chance_alta

                # 2. CÁLCULO DA CONFLUÊNCIA MACRO (H1)
                fechamentos_h1 = hist_h1["Close"]
                ma9_h1 = fechamentos_h1.rolling(window=9).mean().iloc[-1]
                ma21_h1 = fechamentos_h1.rolling(window=21).mean().iloc[-1]
                tendencia_macro = "ALTA" if ma9_h1 > ma21_h1 else "BAIXA"

                # MONTAGEM DA TELA EM LINHAS E COLUNAS MAIORES (2x2)
                with espaco_dashboard.container():
                    linha1_col1, linha1_col2 = st.columns(2)
                    linha2_col1, linha2_col2 = st.columns(2)
                    
                    # BLOCO 1: ANÁLISE TÉCNICA ATUAL
                    with linha1_col1:
                        st.markdown("<div class='bloco-premium'>", unsafe_allow_html=True)
                        st.markdown("### 📊 Sinais Técnicos Atuais")
                        st.metric(label=f"Preço Ouro Atual ({texto_tempo})", value=f"${preco_atual:.2f}")
                        st.markdown(f"**Direção das Médias:** {status_media}")
                        st.markdown(f"**RSI (14):** {rsi_atual:.1f} ({status_rsi})")
                        st.markdown(f"**Força MACD:** {status_macd}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # BLOCO 2: PROBABILIDADE & CONFLUÊNCIA DE TEMPO
                    with linha1_col2:
                        st.markdown("<div class='bloco-premium'>", unsafe_allow_html=True)
                        st.markdown("### 🎯 Probabilidade & Filtro de Tendência")
                        st.success(f"🟢 CHANCE DE ALTA: {chance_alta}%")
                        st.error(f"🔴 CHANCE DE BAIXA: {chance_baixa}%")
                        st.markdown("---")
                        
                        st.markdown("🌐 **Filtro Macro (Gráfico de 1 Hora):**")
                        if tendencia_macro == "ALTA":
                            st.markdown("📈 Tendência de H1 está em **ALTA**. Operações de Compra têm maior probabilidade de ganho.")
                        else:
                            st.markdown("📉 Tendência de H1 está em **BAIXA**. Operações de Venda têm maior probabilidade de ganho.")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # BLOCO 3: INSIGHTS DE ENTRADA DO ASSISTENTE
                    with linha2_col2:
        st.markdown("<div class='bloco-premium'>", unsafe_allow_html=True)
        st.markdown("### 📢 Calendário Fundamentalista")
        st.write("Fique de olho nos horários (Brasília) para não tomar sustos:")
        
        noticias = pd.DataFrame({
            "Horário": ["09:30", "10:30", "11:00", "15:00"],
            "Notícia Macro (USD)": ["Payroll / Desemprego EUA", "Abertura de Nova York", "CPI / Inflação EUA", "Discurso do FOMC / Fed"],
            "Risco": ["🔴 CRÍTICO", "🟠 VOLÁTIL", "🔴 ALTO", "🔴 CRÍTICO"]
        })
        st.table(noticias)
        st.markdown("</div>", unsafe_allow_html=True)

    except Exception:
        pass

    time.sleep(10)
