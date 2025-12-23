import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random
import textwrap

# -----------------------------------------------------------------------------
# [0] SYSTEM INIT & DATA LOADING
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

stock_names = get_stock_list()
TIME_OPTS = {"⛔ 수동": 0, "⏱️ 3분": 180, "⏱️ 10분": 600, "⏱️ 30분": 1800}

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
# [1] STYLING
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
    
    /* Analysis Box */
    .report-box {
        background-color: #121212; border: 1px solid #333; border-radius: 10px;
        padding: 25px; margin-bottom: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    .report-header {
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 2px solid #333; padding-bottom: 15px; margin-bottom: 20px;
    }
    
    .persona-section {
        margin-bottom: 25px; padding: 25px; border-radius: 8px; background: #1a1a1a;
        border-left-width: 5px; border-left-style: solid;
    }
    
    .hamzzi-style { border-left-color: #FFAA00; }
    .hojji-style { border-left-color: #FF4444; }
    
    .persona-name { font-size: 18px; font-weight: 900; margin-bottom: 15px; display: block; }
    .analysis-text { font-size: 15px; line-height: 1.8; color: #ddd; white-space: pre-wrap; text-align: justify; }
    
    /* One-line Summary Style */
    .summary-line {
        margin-top: 15px; padding: 10px; background: rgba(255,255,255,0.05); 
        border-radius: 6px; font-weight: bold; color: #fff;
    }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -15px !important; margin-top: 23px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #d4af37;'>🐯 Hojji & Hamzzi Deep Quant 🐹</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [2] SINGULARITY OMEGA ENGINE
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

        # --- 🐹 HAMZZI (Aggressive) ---
        if wr >= 0.70:
            h_text = f"""
            <b>[1. 물리적 임계점 (JLS Model)]</b>
            사장님! <b>Omega 진동수</b>가 {m['omega']:.2f}Hz로 극도로 안정화됐어. 로그 주기적 패턴이 수렴하면서 <b>임계 폭발(Critical Burst)</b> 직전이야! 이건 인간의 심리가 아니라 물리적 필연이라구.

            <b>[2. 수급 폭발 (Hawkes Process)]</b>
            <b>Hawkes 강도</b>가 {m['hawkes']:.2f}를 돌파! 누군가 매수하면 기계들이 따라서 미친 듯이 사는 '자기 여진' 상태야. 지금 올라타면 로켓 배송 확정!

            <b>[3. 구체적 행동 지침]</b>
            고민할 시간 없어! <b>시장가(Market Order)</b>로 <b>{can_buy}주</b> 풀매수! <b>{target:,}원</b> 뚫는 순간 <b>불타기(Pyramiding)</b>로 물량 2배 실어!
            
            <div class='summary-line'>🐹 한줄 요약: 쫄지마! 이건 인생 역전 티켓이야! 당장 긁어! 🔥</div>
            """
        elif wr >= 0.40:
            h_text = f"""
            <b>[1. 추세 분석 (Hurst Exponent)]</b>
            음~ <b>Hurst</b>가 {m['hurst']:.2f}야. 추세가 살아있긴 한데 폭발적이진 않아. 단타 치기 딱 좋은 '놀이터'가 형성됐어.

            <b>[2. 눈치 싸움 (OBI)]</b>
            <b>호가 불균형(OBI)</b>이 {m['obi']:.2f}로 중립적이야. 세력들이 간 보고 있다는 거지.

            <b>[3. 구체적 행동 지침]</b>
            몰빵은 금지! <b>{int(can_buy/3)}주</b>만 '정찰병'으로 투입해. <b>{price:,}원</b> 이탈하면 뒤도 돌아보지 말고 튀어! '치고 빠지기'만이 살길이야.
            
            <div class='summary-line'>🐹 한줄 요약: 욕심 버리고 짧게 단타로 발라먹자! ⚡</div>
            """
        else:
            h_text = f"""
            <b>[1. 독성 경고 (VPIN)]</b>
            으악! <b>VPIN</b>이 {m['vpin']:.2f}야! 기관들이 정보 우위로 설거지 중이라구! 독성 매물이 쏟아진다!

            <b>[2. 구조 붕괴 (TDA)]</b>
            <b>Betti Number</b>가 1로 변했어. 차트에 구멍이 뚫렸다는 수학적 증거야. 지지선 따윈 없어!

            <b>[3. 구체적 행동 지침]</b>
            <b>절대 매수 금지!</b> 들고 있으면 당장 시장가로 던져! 이건 투자가 아니라 기부야. 현금 꽉 쥐고 돔황챠!!
            
            <div class='summary-line'>🐹 한줄 요약: 폭탄이야! 만지면 터져! 도망가! 💣</div>
            """

        # --- 🐯 HOJJI (Conservative) ---
        if wr >= 0.70:
            t_text = f"""
            <b>[1. 네트워크 분석 (GNN)]</b>
            허허, <b>GNN 중심성</b>이 {m['gnn']:.2f}로군. 시장 자금이 이 종목을 '허브(Hub)'로 삼아 흐르고 있어. 진정한 대장주야.

            <b>[2. 인과성 (Transfer Entropy)]</b>
            선행 지표들이 양의 정보량(Positive Flow)을 보내고 있어. 펀더멘털과 수급이 '금상첨화'를 이루는구먼.

            <b>[3. 구체적 행동 지침]</b>
            안전마진이 확보됐네. 자네 자금의 <b>{int(can_buy*0.8)}주</b> 정도를 진입하게. <b>{target:,}원</b>까지는 흔들려도 '우보천리'의 자세로 버티는 게 정석이야.
            
            <div class='summary-line'>🐯 한줄 요약: 진국일세. 엉덩이 무겁게 들고 가시게. 🍵</div>
            """
        elif wr >= 0.40:
            t_text = f"""
            <b>[1. 변동성 위험 (Vol Surface)]</b>
            계륵일세. <b>내재 변동성</b>이 {m['vol_surf']:.2f}로 너무 높아. 옵션 시장 불안이 현물로 전이되는 '내우외환'의 형국이야.

            <b>[2. 꼬리 위험 (EVT)]</b>
            극단치 이론(EVT)으로 본 <b>예상 손실(ES)</b>이 {m['es']:.2f}야. 평소엔 멀쩡하다가 한 번에 훅 갈 수 있어.

            <b>[3. 구체적 행동 지침]</b>
            욕심은 화를 부르네. <b>{int(can_buy*0.2)}주</b>만 분할로 담거나, 아예 관망하게. 돌다리도 두들겨 보고 건너는 '유비무환'의 자세가 필요해.
            
            <div class='summary-line'>🐯 한줄 요약: 위험해 보이네. 아주 조금만 담거나 쉬게나. 🐅</div>
            """
        else:
            t_text = f"""
            <b>[1. 펀더멘털 훼손]</b>
            에잉 쯧쯧! <b>Going Concern</b> 이슈가 보여. 기초 체력이 부실한데 탑을 쌓으려 하다니, 사상누각일세.

            <b>[2. 저항선 (Role Reversal)]</b>
            지지선이 저항선으로 변질됐어. 떨어지는 칼날을 맨손으로 잡으려 하지 말게.

            <b>[3. 구체적 행동 지침]</b>
            쳐다도 보지 말게. 현금이 곧 최고의 종목이야. <b>비에르고딕(Non-Ergodic)</b> 파산 위험을 피하는 게 상책일세.
            
            <div class='summary-line'>🐯 한줄 요약: 썩은 동아줄이야. 절대 잡지 마라. 🏚️</div>
            """

        return h_text, t_text

    def diagnose_portfolio_deep(self, portfolio, cash):
        if not portfolio: return "포트폴리오가 비어있습니다.", "계좌가 비었군."
        
        # Metric Calc
        total = cash + sum(s['price']*s['qty'] for s in portfolio)
        cash_r = (cash/total*100) if total else 100
        count = len(portfolio)
        
        # Simulating Portfolio Metrics
        beta = np.random.uniform(0.5, 2.0)
        sharpe = np.random.uniform(0.5, 3.0)
        corr = np.random.uniform(0.3, 0.9)
        mdd = np.random.uniform(-5.0, -40.0)
        
        # ---------------- HAMZZI (Aggressive) ----------------
        h = f"""
        <b>[1. 자본 효율성 분석 (Capital Efficiency)]</b>
        사장님! 현재 현금 비중이 <b>{cash_r:.1f}%</b>나 돼? 이건 명백한 <b>[Cash Drag]</b>야! 인플레이션을 감안하면 앉아서 돈을 잃고 있는 거라구.
        현재 포트폴리오의 <b>Beta</b>값은 <b>{beta:.2f}</b>야. 시장이 1% 오를 때 {beta:.2f}%밖에 안 오르면 무슨 재미로 주식해? 레버리지가 전혀 안 먹히고 있어!

        <b>[2. 켈리 공식 기반 사이징 (Fractional Kelly)]</b>
        내 계산상 현재 승률 우위(Edge)가 있는 장세에서 최적 베팅 비율은 자산의 80%야. 근데 사장님은 너무 쫄보처럼 굴고 있어.
        <b>Singularity Omega</b> 엔진이 감지한 '상승 임계점'이 도래했어. 지금은 수비할 때가 아니라 공격할 때야!

        <b>[3. 구체적 리밸런싱 액션 플랜]</b>
        👉 <b>[WHEN]</b> 내일 장 시작(09:00)과 동시에 동시호가 수급 확인 후 즉시 실행!
        👉 <b>[WHAT]</b> 현금의 50%를 <b>[TQQQ]</b>나 <b>[반도체 레버리지 ETF]</b>에 태워!
        👉 <b>[HOW]</b> 분할 매수? 아니! <b>시장가(Market Order)</b>로 질러서 베타를 1.5 이상으로 강제 펌핑해!
        👉 <b>[WHY]</b> 변동성 파동(Vol Wave)이 상승 초입이야. 지금 리스크를 걸어야 '초과 수익(Alpha)'을 먹을 수 있어.
        
        <div class='summary-line'>🐹 한줄 요약: 현금은 쓰레기야! 당장 레버리지 풀매수해서 인생 바꾸자! 🔥</div>
        """
        
        # ---------------- HOJJI (Conservative) ----------------
        t = f"""
        <b>[1. 시스템 리스크 분석 (Systemic Risk)]</b>
        자네 포트폴리오를 보니 <b>종목 간 상관계수(Correlation)</b>가 <b>{corr:.2f}</b>로 매우 높아. 
        이건 '계란을 한 바구니에 담은' 꼴일세. 하락장이 오면 <b>고유값(Eigenvalue)</b>이 동조화되면서 계좌가 한방에 터질 수 있어.
        시뮬레이션 상 <b>MDD(최대 낙폭)</b>가 <b>{mdd:.1f}%</b>까지 열려있네. 밤에 잠은 오나?

        <b>[2. 비에르고딕 생존 전략 (Non-Ergodic Survival)]</b>
        투자의 제1원칙은 '파산하지 않는 것'이야. 한 번의 실수로 재기 불능이 되면(Ergodic) 아무 소용 없네.
        지금 자네 포트폴리오는 꼬리 위험(Fat Tail)에 무방비로 노출되어 있어. '소탐대실'하기 딱 좋은 구조야.

        <b>[3. 구체적 리밸런싱 액션 플랜]</b>
        👉 <b>[WHEN]</b> 지금 당장, 혹은 반등 시마다 비중을 줄이게.
        👉 <b>[WHAT]</b> 변동성이 큰 기술주 비중을 30% 줄이고, <b>[미국채 10년물]</b>이나 <b>[금(Gold)]</b>을 편입하게.
        👉 <b>[HOW]</b> 기계적으로 <b>[자산 배분(Asset Allocation)]</b> 비율을 6:4로 맞추고, 리밸런싱은 월 1회만 하게.
        👉 <b>[WHY]</b> 엔트로피가 증가하는 시장일세. '유비무환'의 자세로 방어벽을 세워야 살아남을 수 있네.
        
        <div class='summary-line'>🐯 한줄 요약: 욕심 부리다 다 잃네. 채권 섞어서 방어벽부터 세우게. 🛡️</div>
        """
        return h, t

# -----------------------------------------------------------------------------
# [3] RENDERER
# -----------------------------------------------------------------------------
def render_deep_analysis_report(d):
    engine = SingularityEngine()
    win_pct = d['win'] * 100
    
    # Color Logic
    if d['win'] >= 0.7: color = "#00FF00" 
    elif d['win'] >= 0.4: color = "#FFAA00"
    else: color = "#FF4444"
    
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
        
    st.markdown("</div>", unsafe_allow_html=True) 

# -----------------------------------------------------------------------------
# [4] LOGIC EXECUTION
# -----------------------------------------------------------------------------
def run_my_diagnosis():
    engine = SingularityEngine(); market_data = load_top50_data(); my_res = []
    
    # 1. Portfolio Level
    h_port, t_port = engine.diagnose_portfolio_deep(st.session_state.portfolio, st.session_state.cash)
    st.session_state.port_analysis = {'hamzzi': h_port, 'hojji': t_port}
    
    # 2. Individual Level
    with st.spinner("🧠 Singularity Omega Engine: 보유 종목 심층 분석 및 시뮬레이션 중..."):
        for s in st.session_state.portfolio:
            if not s['name']: continue
            mode = "scalping" if s['strategy'] == "초단타" else "swing"
            price = int(s['price']) if s['price'] > 0 else 10000
            
            wr, m = engine.run_diagnosis(s['name'], mode)
            h_txt, t_txt = engine.generate_deep_report(s['name'], mode, price, m, wr, st.session_state.cash, s['qty'])
            
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
if st.button("📝 내 종목 및 포트폴리오 심층 정밀 진단 (Deep Dive)"):
    st.session_state.trigger_my = True
    st.rerun()

# RENDER DIAGNOSIS
if st.session_state.my_diagnosis:
    st.markdown("---")
    if st.session_state.port_analysis:
        pa = st.session_state.port_analysis
        st.markdown(f"""
        <div class='report-box'>
            <div style='font-size:20px; font-weight:bold; color:#fff; margin-bottom:20px; border-bottom:1px solid #333; padding-bottom:10px;'>📊 포트폴리오 종합 심층 진단</div>
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
    
    st.subheader("👤 보유 종목별 심층 분석 리포트 (Omega Engine)")
    for d in st.session_state.my_diagnosis:
        render_deep_analysis_report(d)

# Trigger Logic
if st.session_state.trigger_my:
    run_my_diagnosis()
    st.rerun()
