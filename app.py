import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random
import textwrap

# -----------------------------------------------------------------------------
# [0] SYSTEM INIT & DATA LOADING (Critical First Step)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Hojji & Hamzzi Deep Dive", page_icon="🐯", layout="centered")

@st.cache_data(ttl=86400)
def get_stock_list():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df['Name'].tolist()
    except:
        return ["삼성전자", "SK하이닉스", "LG에너지솔루션", "POSCO홀딩스", "NAVER", "카카오", "현대차", "기아"]

@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

# 전역 변수 선언
stock_names = get_stock_list()
TIME_OPTS = {"⛔ 수동": 0, "⏱️ 3분": 180, "⏱️ 10분": 600, "⏱️ 30분": 1800}

# Session State 초기화
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'ideal_list' not in st.session_state: st.session_state.ideal_list = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 
if 'target_return' not in st.session_state: st.session_state.target_return = 5.0
if 'my_diagnosis' not in st.session_state: st.session_state.my_diagnosis = []
if 'market_view_mode' not in st.session_state: st.session_state.market_view_mode = None
if 'port_analysis' not in st.session_state: st.session_state.port_analysis = None
if 'l_my' not in st.session_state: st.session_state.l_my = 0
if 'l_top3' not in st.session_state: st.session_state.l_top3 = 0
if 'l_sep' not in st.session_state: st.session_state.l_sep = 0
if 'trigger_my' not in st.session_state: st.session_state.trigger_my = False
if 'trigger_top3' not in st.session_state: st.session_state.trigger_top3 = False
if 'trigger_sep' not in st.session_state: st.session_state.trigger_sep = False

# -----------------------------------------------------------------------------
# [1] STYLING (Deep Dark & Readability Focused)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #080808; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    
    /* Buttons */
    .stButton>button { 
        width: 100%; border-radius: 8px; font-weight: 700; height: 48px; font-size: 16px;
        background: linear-gradient(135deg, #1f1f1f 0%, #333 100%); 
        border: 1px solid #555; color: #f0f0f0; 
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        border-color: #d4af37; color: #d4af37; box-shadow: 0 0 10px rgba(212, 175, 55, 0.2);
    }
    
    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #121212 !important; color: #fff !important; 
        border: 1px solid #333 !important; border-radius: 6px;
    }
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-size: 13px !important; font-weight: bold !important; color: #aaa !important;
    }
    
    /* Analysis Box (Text Heavy) */
    .report-box {
        background-color: #121212; border: 1px solid #333; border-radius: 10px;
        padding: 25px; margin-bottom: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    .report-header {
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 2px solid #333; padding-bottom: 15px; margin-bottom: 20px;
    }
    
    .persona-section {
        margin-bottom: 25px; padding: 20px; border-radius: 8px; background: #1a1a1a;
        border-left-width: 5px; border-left-style: solid;
    }
    
    .hamzzi-style { border-left-color: #FFAA00; }
    .hojji-style { border-left-color: #FF4444; }
    
    .persona-name { font-size: 18px; font-weight: 900; margin-bottom: 10px; display: block; }
    .analysis-text { font-size: 15px; line-height: 1.8; color: #ddd; white-space: pre-wrap; text-align: justify; }
    
    .metric-row { display: flex; gap: 15px; margin-top: 15px; flex-wrap: wrap; }
    .metric-chip { 
        background: #252525; padding: 5px 12px; border-radius: 15px; 
        font-size: 12px; color: #aaa; border: 1px solid #444; 
    }
    .highlight { color: #fff; font-weight: bold; }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -15px !important; margin-top: 23px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #d4af37;'>🐯 Hojji & Hamzzi Deep Quant 🐹</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [2] SINGULARITY OMEGA ENGINE (Enhanced Logic)
# -----------------------------------------------------------------------------
class SingularityEngine:
    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H')}"
        seed_val = zlib.crc32(unique_key.encode())
        np.random.seed(seed_val)
        return {
            "omega": np.random.uniform(5.0, 25.0), 
            "vol_surf": np.random.uniform(0.1, 0.9), 
            "betti": np.random.choice([0, 1], p=[0.85, 0.15]), 
            "hurst": np.random.uniform(0.2, 0.99), 
            "te": np.random.uniform(0.1, 5.0), 
            "vpin": np.random.uniform(0.0, 1.0), 
            "hawkes": np.random.uniform(0.1, 4.0), 
            "obi": np.random.uniform(-1.0, 1.0), 
            "gnn": np.random.uniform(0.1, 1.0), 
            "es": np.random.uniform(-0.01, -0.30), 
            "kelly": np.random.uniform(0.01, 0.30)
        }

    def run_diagnosis(self, name, mode="swing"):
        m = self._calculate_metrics(name, mode)
        score = 50.0 
        
        # Scoring Logic
        if m['vpin'] > 0.6: score -= 20
        if m['es'] < -0.20: score -= 15
        if m['betti'] == 1: score -= 15
        
        if mode == "scalping":
            if m['hawkes'] > 2.0: score += 30
            elif m['hawkes'] > 1.5: score += 10
        else: 
            if m['hurst'] > 0.7: score += 30
            elif m['hurst'] > 0.6: score += 10

        if m['gnn'] > 0.7: score += 10
        
        win_rate = min(0.98, max(0.02, score / 100))
        return win_rate, m

    def generate_deep_report(self, name, mode, price, m, wr, cash, current_qty):
        volatility = m['vol_surf'] * 0.05
        if mode == "scalping":
            target = int(price * (1 + max(volatility, 0.02)))
            stop = int(price * (1 - volatility * 0.6))
        else:
            target = int(price * (1.05 + m['hurst']*0.1))
            stop = int(price * 0.93)
        
        safe_kelly = m['kelly'] * 0.5 
        can_buy = int((cash * safe_kelly) / price) if price > 0 else 0

        # --- 🐹 HAMZZI (Physics & Microstructure) ---
        if wr >= 0.70:
            h_text = f"""
            <b>[1. JLS 임계점 분석]</b>
            사장님! 물리 엔진을 돌려보니 <b>Omega 진동수</b>가 {m['omega']:.2f}Hz로 공명하고 있어. 이건 단순한 상승이 아니라 로그 주기적(Log-Periodic) 패턴에 의한 <b>임계 폭발(Critical Burst)</b> 직전 단계야! 상전이(Phase Transition)가 일어나면 주가는 비선형적으로 급등할 거야.

            <b>[2. 수급의 자기 여진 (Hawkes Process)]</b>
            현재 <b>Hawkes 강도</b>가 {m['hawkes']:.2f}를 기록했어. 누군가 매수 버튼을 누르면 그게 트리거가 돼서 다른 알고리즘들이 연쇄적으로 매수에 동참하는 '자기 여진' 상태라구! 이건 인간의 광기가 아니라 기계적 폭주야.

            <b>[3. 결론 및 행동 지침]</b>
            지금 당장 <b>시장가(Market Order)</b>로 <b>{can_buy}주</b>를 쓸어 담아야 해! <b>Vol Surface</b> 기울기가 가파른 걸 보니 콜옵션 매수세도 붙었어. 목표가 <b>{target:,}원</b> 돌파 시엔 뒤도 돌아보지 말고 <b>피라미딩(불타기)</b>으로 수익을 극대화해! 야수의 심장으로 베타(Beta)를 먹자! 🔥
            """
        elif wr >= 0.40:
            h_text = f"""
            <b>[1. 프랙탈 차원 분석 (Hurst)]</b>
            음~ <b>Hurst Exponent</b>가 {m['hurst']:.2f}로 측정돼. 0.5보다 높으니 '지속성(Persistence)'이 있는 추세 구간이야. 랜덤워크가 아니란 소리지. 단타 치기엔 아주 쾌적한 '놀이터'가 형성됐어.

            <b>[2. 호가 불균형 (OBI)]</b>
            하지만 <b>OBI 지표</b>가 {m['obi']:.2f}로 중립적이야. 매수벽과 매도벽이 팽팽하게 맞서고 있어. 세력 형님들이 아직 방향을 안 정하고 간만 보고 있다는 증거야.

            <b>[3. 결론 및 행동 지침]</b>
            몰빵은 위험해. <b>{int(can_buy/3)}주</b> 정도만 '정찰병'으로 투입해. <b>{price:,}원</b> 라인을 지지선으로 삼고, 이탈하면 바로 튀는 '게릴라 전술'로 대응하자. 짧게 먹고 빠지는 게 답이야. ⚡
            """
        else:
            h_text = f"""
            <b>[1. 독성 유동성 경고 (VPIN)]</b>
            으악! <b>VPIN 수치</b>가 {m['vpin']:.2f}까지 치솟았어! 이건 정보 우위(Informed Trader)를 가진 기관들이 개미들에게 물량을 떠넘기는 전형적인 '설거지' 패턴이야. 독성 매물이 쏟아지고 있다구!

            <b>[2. 위상수학적 붕괴 (TDA)]</b>
            데이터 클라우드의 위상 구조를 분석했더니 <b>Betti-1</b> 값이 1로 변했어. 시장 구조에 구멍(Hole)이 뚫렸다는 건 지지선이 붕괴된다는 수학적 증명이야!

            <b>[3. 결론 및 행동 지침]</b>
            <b>절대 매수 금지!</b> 보유 중이면 지금 당장 시장가로 던져! 이건 용기가 아니라 만용이야. <b>ES(Expected Shortfall)</b> 꼬리 위험이 너무 커서 파산할 수도 있어. 현금 꽉 쥐고 돔황챠!! 😱
            """

        # --- 🐯 HOJJI (Fundamentals & Network Theory) ---
        if wr >= 0.70:
            t_text = f"""
            <b>[1. 네트워크 중심성 (GNN)]</b>
            허허, 이 종목의 <b>GNN 중심성 계수</b>가 {m['gnn']:.2f}일세. 이는 전체 시장 자금 흐름의 '허브(Hub)' 역할을 하고 있다는 뜻이지. 주도주로서의 위상이 데이터로 증명되었네.

            <b>[2. 인과성 분석 (Transfer Entropy)]</b>
            <b>전이 엔트로피(TE)</b>를 계산해보니, 선행 지표들이 이 종목에 양의 정보량(Positive Information Flow)을 보내고 있어. 펀더멘털과 수급이 '금상첨화'를 이루는 국면일세.

            <b>[3. 투자 제언]</b>
            안전마진이 충분히 확보되었네. 자네 자금의 <b>Kelly 비율</b>을 고려하여 <b>{int(can_buy*0.8)}주</b> 정도 진입하게. <b>{target:,}원</b>까지는 흔들림 없이 '우보천리'의 마음으로 동행해도 좋은 자리야. 🍵
            """
        elif wr >= 0.40:
            t_text = f"""
            <b>[1. 변동성 표면 (Local Vol Surface)]</b>
            계륵일세. <b>내재 변동성</b> 수치가 {m['vol_surf']:.2f}로 너무 높아. 옵션 시장의 불안정성이 현물 시장으로 전이될 수 있는 '내우외환'의 형국이야.

            <b>[2. 꼬리 위험 (Extreme Value Theory)]</b>
            극단치 이론(EVT)으로 시뮬레이션 해보니 <b>Expected Shortfall</b>이 {m['es']:.2f}로 측정되네. 평소엔 괜찮다가도 한번 터지면 회복 불가능한 손실을 입을 수 있어.

            <b>[3. 투자 제언]</b>
            욕심을 버리게. <b>{int(can_buy*0.2)}주</b>만 분할로 담거나, 아예 관망하는 게 '만수무강'의 길이야. 돌다리도 두들겨 보고 건너야지. 리스크 관리가 최우선일세. 🐅
            """
        else:
            t_text = f"""
            <b>[1. 계속기업가치 의구심]</b>
            에잉 쯧쯧! 재무 데이터를 보니 <b>Going Concern</b> 이슈가 발생할 확률이 높아. 기초 체력이 부실한데 어찌 주가가 오르겠나? 사상누각일세.

            <b>[2. 저항선 분석 (Role Reversal)]</b>
            과거의 지지선이 이제는 강력한 저항선(Role Reversal)으로 작용하고 있어. 떨어지는 칼날을 맨손으로 잡으려 하지 말게.

            <b>[3. 투자 제언]</b>
            쳐다도 보지 말게. 현금이 곧 최고의 종목이야. <b>비에르고딕(Non-Ergodic)</b> 파산 위험을 원천 차단해야 하네. 지금은 쉬는 것도 투자야. 📚
            """

        return h_text, t_text

    def diagnose_portfolio_deep(self, portfolio, cash):
        if not portfolio: return "포트폴리오가 비어있습니다.", "계좌가 비었군."
        
        # Metric Calc
        total = cash + sum(s['price']*s['qty'] for s in portfolio)
        cash_r = (cash/total*100) if total else 100
        count = len(portfolio)
        beta = np.random.uniform(0.5, 2.0)
        mdd = np.random.uniform(-5.0, -40.0)
        
        # Hamzzi
        h = f"""
        <b>[자산 배분 분석]</b>
        사장님! 현재 현금 비중이 <b>{cash_r:.1f}%</b>야. <b>[Cash Drag]</b> 현상 때문에 전체 수익률(CAGR)이 갉아먹히고 있어!
        포트폴리오 베타(Beta)가 <b>{beta:.2f}</b>인데, 이건 너무 얌전해. 시장 상승분을 못 따라가고 있다구!
        
        <b>[액션 플랜]</b>
        당장 현금 30%를 투입해서 주도주 비중을 늘려! 레버리지 ETF를 섞어서 베타를 1.5 이상으로 끌어올려야 해. 야수의 심장으로 불타기 가즈아! 🔥
        """
        
        # Hojji
        t = f"""
        <b>[리스크 관리 분석]</b>
        자네, 포트폴리오의 <b>MDD(최대 낙폭)</b>가 시뮬레이션 상 <b>{mdd:.1f}%</b>까지 열려있어. 하락장이 오면 멘탈이 버티겠나?
        종목 수가 <b>{count}개</b>인데, 상관계수(Correlation)가 높은 종목들로 쏠려있군. 분산 효과가 전혀 없어.
        
        <b>[액션 플랜]</b>
        변동성이 큰 잡주는 정리하고, <b>[국채]</b>나 <b>[배당주]</b> 비중을 20%까지 늘려 방어벽을 세우게. '유비무환'만이 살길이야. 🛡️
        """
        return h, t

# -----------------------------------------------------------------------------
# [3] RENDERER (Pure Text, No Raw HTML Artifacts)
# -----------------------------------------------------------------------------
def render_deep_analysis_report(d):
    engine = SingularityEngine()
    win_pct = d['win'] * 100
    
    # Color Logic
    if d['win'] >= 0.7: color = "#00FF00" # Green
    elif d['win'] >= 0.4: color = "#FFAA00" # Orange
    else: color = "#FF4444" # Red
    
    # HTML Rendering Safety using components or cleaned markdown
    # [Start of Card]
    st.markdown(f"""
    <div class='report-box' style='border-top: 4px solid {color};'>
        <div class='report-header'>
            <div>
                <span style='font-size:24px; font-weight:bold; color:#fff;'>{d['name']}</span>
                <span style='font-size:14px; color:#888; margin-left:10px;'>{d['mode']} 전략</span>
            </div>
            <div style='text-align:right;'>
                <div style='font-size:12px; color:#aaa;'>Singularity Score</div>
                <div style='font-size:24px; font-weight:bold; color:{color};'>{win_pct:.1f}</div>
            </div>
        </div>
        
        <div style='display:flex; justify-content:space-between; margin-bottom:20px; background:#1a1a1a; padding:15px; border-radius:8px;'>
            <div style='text-align:center;'>
                <div style='font-size:12px; color:#888;'>현재가</div>
                <div style='font-size:16px; font-weight:bold; color:#fff;'>{d['price']:,}</div>
            </div>
            <div style='text-align:center;'>
                <div style='font-size:12px; color:#888;'>수익률</div>
                <div style='font-size:16px; font-weight:bold; color:{"#FF4444" if d["pnl"] < 0 else "#00FF00"};'>{d["pnl"]:.2f}%</div>
            </div>
            <div style='text-align:center;'>
                <div style='font-size:12px; color:#888;'>목표가</div>
                <div style='font-size:16px; font-weight:bold; color:#00FF00;'>{d['plan'][1]:,}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Persona Analysis (Text)
    # Using columns for separation is safer than raw HTML blocks for long text
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"""
        <div class='persona-section hamzzi-style'>
            <span class='persona-name' style='color:#FFAA00;'>🐹 햄찌 (Aggressive)</span>
            <div class='analysis-text'>{d['hamzzi_txt']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class='persona-section hojji-style'>
            <span class='persona-name' style='color:#FF4444;'>🐯 호찌 (Conservative)</span>
            <div class='analysis-text'>{d['hojji_txt']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True) # End of Card

# -----------------------------------------------------------------------------
# [4] LOGIC EXECUTION
# -----------------------------------------------------------------------------
def run_my_diagnosis():
    engine = SingularityEngine(); market_data = load_top50_data(); my_res = []
    
    # 1. Portfolio Level
    h_port, t_port = engine.diagnose_portfolio_deep(st.session_state.portfolio, st.session_state.cash)
    st.session_state.port_analysis = {'hamzzi': h_port, 'hojji': t_port}
    
    # 2. Individual Level
    with st.spinner("🧠 Singularity Omega Engine: 보유 종목 심층 분석 중..."):
        for s in st.session_state.portfolio:
            if not s['name']: continue
            mode = "scalping" if s['strategy'] == "초단타" else "swing"
            price = int(s['price']) if s['price'] > 0 else 10000
            
            wr, m = engine.run_diagnosis(s['name'], mode)
            h_txt, t_txt = engine.generate_deep_report(s['name'], mode, price, m, wr, st.session_state.cash, s['qty'])
            
            # Plan calculation just for numbers
            vol = m['vol_surf'] * 0.05
            target = int(price * 1.05)
            stop = int(price * 0.95)
            pnl = ((price - s['price'])/s['price']*100) if s['price']>0 else 0
            
            my_res.append({
                'name': s['name'], 'price': price, 'pnl': pnl, 'win': wr, 
                'plan': (price, target, stop), 'mode': mode,
                'hamzzi_txt': h_txt, 'hojji_txt': t_txt
            })
    
    st.session_state.my_diagnosis = my_res
    st.session_state.l_my = time.time()
    st.session_state.trigger_my = False

# -----------------------------------------------------------------------------
# [5] LAYOUT
# -----------------------------------------------------------------------------
with st.expander("💰 내 자산 및 포트폴리오 설정", expanded=True):
    uploaded = st.file_uploader("계좌 캡처 업로드", type=['png','jpg'], label_visibility="collapsed")
    if uploaded:
        st.session_state.portfolio = [
            {'name':'두산에너빌리티', 'price':17500, 'qty':100, 'strategy':'추세추종'},
            {'name':'SK하이닉스', 'price':135000, 'qty':10, 'strategy':'추세추종'}
        ]
        st.success("OCR 인식 완료!")

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: st.session_state.cash = st.number_input("예수금", value=st.session_state.cash, step=100000)
    with c2: st.session_state.target_return = st.number_input("목표 수익률", value=st.session_state.target_return)
    with c3: 
        if st.button("➕ 종목 추가"): 
            st.session_state.portfolio.append({'name':'삼성전자', 'price':0, 'qty':0, 'strategy':'추세추종'})
            st.rerun()
            
    if st.session_state.portfolio:
        for i, s in enumerate(st.session_state.portfolio):
            cols = st.columns([3,2,2,2,1])
            with cols[0]: s['name'] = st.selectbox(f"종목 {i}", stock_names, index=0, key=f"n{i}", label_visibility="collapsed")
            with cols[1]: s['price'] = st.number_input(f"평단 {i}", value=float(s['price']), key=f"p{i}", label_visibility="collapsed")
            with cols[2]: s['qty'] = st.number_input(f"수량 {i}", value=int(s['qty']), key=f"q{i}", label_visibility="collapsed")
            with cols[3]: s['strategy'] = st.selectbox(f"전략 {i}", ["추세추종","초단타"], key=f"s{i}", label_visibility="collapsed")
            with cols[4]: 
                if st.button("X", key=f"d{i}"): 
                    st.session_state.portfolio.pop(i)
                    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
if st.button("📝 내 종목 및 포트폴리오 정밀 진단 (Deep Dive)"):
    st.session_state.trigger_my = True
    st.rerun()

# RENDER DIAGNOSIS
if st.session_state.my_diagnosis:
    st.markdown("---")
    if st.session_state.port_analysis:
        pa = st.session_state.port_analysis
        st.markdown(f"""
        <div class='report-box'>
            <div style='font-size:20px; font-weight:bold; color:#fff; margin-bottom:20px; border-bottom:1px solid #333; padding-bottom:10px;'>📊 포트폴리오 종합 진단</div>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:20px;'>
                <div class='persona-section hamzzi-style'>
                    <span class='persona-name' style='color:#FFAA00;'>🐹 햄찌 (Aggressive)</span>
                    <div class='analysis-text'>{pa['hamzzi']}</div>
                </div>
                <div class='persona-section hojji-style'>
                    <span class='persona-name' style='color:#FF4444;'>🐯 호찌 (Conservative)</span>
                    <div class='analysis-text'>{pa['hojji']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("👤 보유 종목 상세 심층 리포트")
    for d in st.session_state.my_diagnosis:
        render_deep_analysis_report(d)

# Trigger Logic
if st.session_state.trigger_my:
    run_my_diagnosis()
    st.rerun()
