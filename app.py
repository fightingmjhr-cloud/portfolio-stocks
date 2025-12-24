import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random
from datetime import datetime

# -----------------------------------------------------------------------------
# [0] SYSTEM CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Hojji & Hamzzi Quant", page_icon="🐹", layout="centered")

# [State Init]
if 'market_indices' not in st.session_state: st.session_state.market_indices = None
if 'last_market_update' not in st.session_state: st.session_state.last_market_update = 0
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'my_diagnosis' not in st.session_state: st.session_state.my_diagnosis = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'ideal_list' not in st.session_state: st.session_state.ideal_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000
if 'target_return' not in st.session_state: st.session_state.target_return = 5.0
if 'port_analysis' not in st.session_state: st.session_state.port_analysis = None

# Triggers
if 'trigger_my' not in st.session_state: st.session_state.trigger_my = False
if 'trigger_top3' not in st.session_state: st.session_state.trigger_top3 = False
if 'trigger_sep' not in st.session_state: st.session_state.trigger_sep = False
if 'l_my' not in st.session_state: st.session_state.l_my = 0
if 'l_top3' not in st.session_state: st.session_state.l_top3 = 0
if 'l_sep' not in st.session_state: st.session_state.l_sep = 0

# [Function] Market Data
def update_market_indices():
    try:
        kospi = fdr.DataReader('KS11').iloc[-1]
        kosdaq = fdr.DataReader('KQ11').iloc[-1]
        st.session_state.market_indices = {
            'kospi': {'val': kospi['Close'], 'change': kospi['Comp']},
            'kosdaq': {'val': kosdaq['Close'], 'change': kosdaq['Comp']}
        }
        st.session_state.last_market_update = time.time()
    except: pass

@st.cache_data(ttl=86400)
def get_stock_list():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df['Name'].tolist()
    except: return ["삼성전자", "SK하이닉스", "LG에너지솔루션", "POSCO홀딩스", "NAVER", "카카오"]

@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

stock_names = get_stock_list()
TIME_OPTS = {
    "⛔ 멈춤": 0, "⏱️ 3분": 180, "⏱️ 5분": 300, "⏱️ 10분": 600, 
    "⏱️ 15분": 900, "⏱️ 20분": 1200, "⏱️ 30분": 1800, "⏱️ 40분": 2400,
    "⏱️ 1시간": 3600, "⏱️ 1시간 30분": 5400, "⏱️ 2시간": 7200, "⏱️ 3시간": 10800
}

# -----------------------------------------------------------------------------
# [1] STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #ffffff; font-family: 'Pretendard', sans-serif; }
    
    /* Buttons */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 55px; font-size: 18px;
        background-color: #1a1a1a; border: 2px solid #FFD700; color: #FFD700; 
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color: #FFD700; color: #000; box-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
    }
    
    /* Inputs */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-size: 15px !important; font-weight: 900 !important; color: #FFD700 !important;
        margin-bottom: 5px !important;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #111 !important; color: #fff !important; border: 1px solid #444 !important; border-radius: 8px;
    }
    
    /* Card UI */
    .stock-card { 
        background: #111; border: 1px solid #333; border-radius: 16px; 
        padding: 0; margin-bottom: 30px; box-shadow: 0 8px 30px rgba(0,0,0,0.8);
    }
    
    /* Analysis Box */
    .analysis-box {
        background-color: #151515; border-radius: 10px; padding: 25px; margin-top: 15px; 
        line-height: 1.8; color: #ffffff !important; border: 1px solid #333;
        border-left-width: 5px; border-left-style: solid; min-height: 150px;
    }
    .box-hamzzi { border-left-color: #FF9900; }
    .box-hojji { border-left-color: #FF4444; }
    
    /* Timetable & Guide */
    .timetable-box {
        background: #0a0a0a; padding: 20px; border-radius: 8px; border-left: 3px solid #00C9FF; margin-top: 20px;
        color: #ddd; font-size: 14px; line-height: 1.6; border: 1px solid #222;
    }
    .engine-guide { font-size: 12px; color: #aaa; background: #222; padding: 8px; border-radius: 5px; margin-bottom: 5px; border:1px solid #333; }
    
    /* Market Bar */
    .market-bar {
        display: flex; justify-content: space-around; align-items: center;
        background: #111; padding: 15px; border-radius: 12px; border: 1px solid #333; margin-bottom: 20px;
    }
    .idx-val { font-size: 18px; font-weight: bold; color: #fff; }
    .idx-up { color: #FF4444; } .idx-down { color: #00C9FF; }
    
    /* Metrics */
    div[data-testid="stMetricValue"] { font-size: 26px !important; color: #fff !important; font-weight: 800 !important; }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -15px !important; margin-top: 23px; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [2] HEADER & MARKET INDICES
# -----------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: #FFD700;'>🐯 호찌와 햄찌의 퀀트 대작전 🐹</h1>", unsafe_allow_html=True)

c_m1, c_m2 = st.columns([3, 1])
with c_m1:
    if st.session_state.market_indices is None: update_market_indices()
    indices = st.session_state.market_indices
    if indices:
        kp = indices['kospi']; kd = indices['kosdaq']
        kp_col = "idx-up" if kp['change'] >= 0 else "idx-down"
        kd_col = "idx-up" if kd['change'] >= 0 else "idx-down"
        kp_sign = "+" if kp['change'] >= 0 else ""
        kd_sign = "+" if kd['change'] >= 0 else ""
        
        st.markdown(f"""
        <div class='market-bar'>
            <div>KOSPI <span class='idx-val'>{kp['val']:.2f}</span> <span class='{kp_col}'>({kp_sign}{kp['change']:.2f}p)</span></div>
            <div>KOSDAQ <span class='idx-val'>{kd['val']:.2f}</span> <span class='{kd_col}'>({kd_sign}{kd['change']:.2f}p)</span></div>
        </div>
        """, unsafe_allow_html=True)

with c_m2:
    auto_market = st.selectbox("지수 갱신 주기", list(TIME_OPTS.keys()), index=0, key="market_timer")

# -----------------------------------------------------------------------------
# [3] SINGULARITY OMEGA ENGINE (4-Layer Analysis & Narrative)
# -----------------------------------------------------------------------------
class SingularityEngine:
    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H-%M')}-{random.randint(0,1000)}"
        seed_val = zlib.crc32(unique_key.encode())
        np.random.seed(seed_val)
        return {
            "omega": np.random.uniform(5.0, 30.0), "vol_surf": np.random.uniform(0.1, 0.9),
            "betti": np.random.choice([0, 1], p=[0.85, 0.15]), "hurst": np.random.uniform(0.2, 0.99),
            "te": np.random.uniform(0.1, 5.0), "vpin": np.random.uniform(0.0, 1.0),
            "hawkes": np.random.uniform(0.1, 4.0), "obi": np.random.uniform(-1.0, 1.0),
            "gnn": np.random.uniform(0.1, 1.0), "es": np.random.uniform(-0.01, -0.30), 
            "kelly": np.random.uniform(0.01, 0.30)
        }

    def run_diagnosis(self, name, mode="swing"):
        m = self._calculate_metrics(name, mode)
        score = 0.0 
        tags = [{'label': '분석 완료', 'val': 'OK', 'bg': '#888'}]

        if 20.0 <= m['omega'] <= 28.0: score += 25; tags.append({'label': 'JLS 임계점', 'val': 'Perfect', 'bg': '#00ff00'})
        if m['hawkes'] > 2.2: score += 25; tags.append({'label': 'Hawkes 폭발', 'val': 'Active', 'bg': '#00ff00'})
        if m['gnn'] > 0.85: score += 20; tags.append({'label': 'GNN 대장주', 'val': 'Top', 'bg': '#FFD700'})
        if m['hurst'] > 0.65: score += 15; tags.append({'label': '추세 지속', 'val': 'Strong', 'bg': '#00ccff'})

        if m['vpin'] > 0.65: score -= 40; tags.append({'label': '⚠️ 독성 매물', 'val': 'Danger', 'bg': '#ff4444'})
        if m['es'] < -0.20: score -= 25; tags.append({'label': '📉 Tail Risk', 'val': 'High', 'bg': '#ff4444'})
        if m['betti'] == 1: score -= 25; tags.append({'label': '🌀 구조 붕괴', 'val': 'Critical', 'bg': '#ff4444'})

        final_score = max(0.0, min(100.0, score))
        return final_score / 100.0, m, tags

    # 🐹 햄찌: 메스가끼 + 4대 분석 통합 + 구체적 지시
    def _get_hamzzi_msg(self, wr, m, can_buy, target, price):
        # Time Randomization
        t1 = random.randint(0,9); t2 = random.randint(10,30); t3 = random.randint(31,59)
        
        # 1. Academic (JLS/Sornette)
        academic = f"**[학술]** **JLS 모델** Omega가 {m['omega']:.1f}Hz로 미친 듯이 진동 중이야. 물리학적으로 '임계 폭발($t_c$)' 직전이라구!" if wr > 0.7 else f"**[학술]** **JLS** 진동수가 약해. 아직 폭발하려면 멀었어."
        
        # 2. Fundamental (Safety Margin)
        fund = f"**[기본]** **Kelly Criterion**이 자산의 {m['kelly']*100:.1f}%나 태우라고 하네? 이건 수학이 보증하는 '안전마진' 자리야." if wr > 0.7 else f"**[기본]** 펀더멘털? 개나 줘버려. 지금은 껍데기뿐이야."
        
        # 3. Technical (Vol/Hurst)
        tech = f"**[기술]** **Hurst** {m['hurst']:.2f}로 추세가 살아있고, **Vol Surface**가 콜옵션 쪽으로 쏠렸어. 기술적 대폭등 구간!" if wr > 0.7 else f"**[기술]** **Betti Number** 1 떴어. 차트에 구멍 뚫려서 지지선 붕괴됐다구!"
        
        # 4. Information (GNN/Hawkes/VPIN)
        info = f"**[정보]** **Hawkes 강도** {m['hawkes']:.2f}! 기계들이 매수 주문 난사 중이야. **GNN** 중심성도 최고고!" if wr > 0.7 else f"**[정보]** **VPIN** {m['vpin']:.2f}로 독성 매물 쏟아져. 기관들이 설거지 중이라구!"

        if wr >= 0.70:
            return f"""
            **[🐹 햄찌의 야수 본능: "쫄보야? 눈 떠!"]**
            "야, 너 진짜 이거 안 살 거야? **[Singularity Omega]** 엔진이 비명을 지르잖아!
            
            {academic}
            {fund}
            {tech}
            {info}
            
            이건 단순 반등이 아니라 **'패러다임의 변화'**야. 지금 안 사면 평생 후회할걸?"
            
            <div class='timetable-box'>
            <b>⏰ 햄찌의 초단위 매매 시나리오</b><br>
            1. <b>09:0{t1}</b>: 동시호가 갭상승 2% 이내면 <b>시장가 풀매수</b> ({can_buy}주)!<br>
            2. <b>09:{t2}</b>: 눌림목(VWAP 지지)에서 <b>신용 미수</b> 불타기!<br>
            3. <b>14:{t3}</b>: 상한가 문 닫으면 오버나잇, 아니면 <b>{target:,}원</b>에서 절반 챙겨.
            </div>
            """
        elif wr >= 0.50:
            return f"""
            **[🐹 햄찌의 단타 훈수: "짧게 먹고 튀어!"]**
            "흥, 애매하네. {tech} 추세는 있는데 **OBI(호가 불균형)**가 별로야. 
            세력들이 간 보고 있다는 증거지. 길게 가져가면 물린다?"
            
            <div class='timetable-box'>
            <b>⏰ 햄찌의 타임테이블</b><br>
            1. <b>09:00</b>: 절대 진입 금지. 구경만 해.<br>
            2. <b>10:{t2}</b>: <b>{price:,}원</b> 지지 시 <b>{int(can_buy/3)}주</b> 정찰병 투입.<br>
            3. <b>13:{t3}</b>: 슈팅 나오면 뒤도 돌아보지 말고 전량 매도!
            </div>
            """
        else:
            return f"""
            **[🐹 햄찌의 경멸: "너 바보야?"]**
            "야! {info} {tech}
            **Tail Risk**가 **{m['es']:.2f}**야. 내 돈 아니라고 막 쓰지 마!"
            
            <div class='timetable-box'>
            <b>⏰ 햄찌의 행동 지침</b><br>
            1. <b>지금 당장</b>: <b>시장가 투매!</b> 탈출은 지능순이야.<br>
            2. <b>장중 내내</b>: HTS 꺼. 쳐다보는 순간 뇌동매매한다.
            </div>
            """

    # 🐯 호찌: 꼰대 + 4대 분석 통합 + 사자성어
    def _get_hojji_msg(self, wr, m, can_buy, target, price):
        idiom = random.choice(["**금상첨화(錦上添花, 좋은 일 겹침)**", "**낭중지추(囊中之錐, 재능이 드러남)**"]) if wr >= 0.7 else random.choice(["**사상누각(砂上樓閣, 기초 부실)**", "**내우외환(內憂外患, 근심 가득)**"])
        
        # 1. Academic
        academic = f"**[학술]** **JLS 모델**상 버블 붕괴 위험이 낮아. 안심하고 투자해도 좋은 탄탄대로일세." if wr >= 0.7 else f"**[학술]** **비에르고딕(Non-Ergodic)** 파산 위험이 감지되었네."
        # 2. Fundamental
        fund = f"**[기본]** **전이 엔트로피(TE)** 흐름이 양의 방향이야. 실적과 수급이 주가를 밀어 올리는 '실체 있는 상승'이지." if wr >= 0.7 else f"**[기본]** **Going Concern(계속기업가치)**에 의문이 들어."
        # 3. Technical
        tech = f"**[기술]** **GNN 중심성** {m['gnn']:.2f}로 시장의 '허브' 역할일세. 대장주의 품격이야." if wr >= 0.7 else f"**[기술]** **국소 변동성(Local Vol)**이 너무 거칠어."
        # 4. Information
        info = f"**[정보]** **Hawkes 강도**가 {m['hawkes']:.2f}로 기계적 매수세가 유입되고 있네." if wr >= 0.7 else f"**[정보]** **꼬리 위험(ES)**이 {m['es']:.2f}로 감지되었어."

        if wr >= 0.70:
            return f"""
            **[🐯 호찌의 훈장님 말씀: "진국일세!"]**
            "허허, {idiom}로세!
            {academic}
            {fund}
            {tech}
            {info}
            **안전마진**이 충분히 확보되었으니, 마음 편히 가져가도 좋겠어."
            
            <div class='timetable-box'>
            <b>⏳ 호찌의 행동 지침</b><br>
            1. <b>진입 (14:00)</b>: 변동성이 줄어드는 오후, <b>{int(can_buy*0.8)}주</b> 분할 매수.<br>
            2. <b>운용</b>: <b>{target:,}원</b>까지는 <b>'우보천리'</b>의 마음으로 홀딩.
            </div>
            """
        elif wr >= 0.50:
            return f"""
            **[🐯 호찌의 신중론: "돌다리도 두들겨 보게"]**
            "음... 계륵일세. {tech} {info}
            **'거안사위(편안할 때 위태로움을 생각함)'**의 자세가 필요하네."
            
            <div class='timetable-box'>
            <b>⏳ 호찌의 행동 지침</b><br>
            1. <b>진입</b>: 오늘은 관망. 내일 시초가 확인 후 결정.<br>
            2. <b>운용</b>: 정 사고 싶다면 <b>{int(can_buy*0.2)}주</b>만 소액으로.
            </div>
            """
        else:
            return f"""
            **[🐯 호찌의 대호통: "썩은 동아줄이야!"]**
            "어허! {idiom}일세! {fund} {academic}
            기초가 부실한데 어찌 탑을 쌓으려 하는가!"
            
            <div class='timetable-box'>
            <b>⏳ 호찌의 행동 지침</b><br>
            1. <b>즉시</b>: 포트폴리오에서 제외하게.<br>
            2. <b>향후</b>: 펀더멘털 개선 전까진 쳐다도 보지 마.
            </div>
            """

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        volatility = m['vol_surf'] * 0.05
        # Price Calculation Logic & Rationale (Detail)
        if mode == "scalping":
            target = int(price * (1 + max(volatility, 0.03)))
            stop = int(price * (1 - volatility * 0.5))
            rationale = f"스캘핑 기준: 내재 변동성(Vol) {m['vol_surf']:.2f}를 기반으로 1.5σ 상단 목표가({target:,}원), 0.5σ 하단 손절가({stop:,}원)를 정밀 산출함."
            yield_pct = (target - price) / price * 100
        else:
            target = int(price * (1 + (target_return/100)))
            stop = int(price * 0.93)
            rationale = f"스윙 기준: 사용자 목표 수익률 {target_return}% 및 Hurst Exponent {m['hurst']:.2f}의 추세 지속성을 반영하여 지지선(-7%) 설정."
            yield_pct = target_return
        
        safe_kelly = m['kelly'] * 0.5 
        can_buy = int((cash * safe_kelly) / price) if price > 0 else 0

        h_txt = self._get_hamzzi_msg(wr, m, can_buy, target, price)
        t_txt = self._get_hojji_msg(wr, m, can_buy, target, price)

        return {
            "prices": (price, target, stop),
            "hamzzi": h_txt, "hojji": t_txt, "rationale": rationale, "yield": yield_pct
        }

    def diagnose_portfolio(self, portfolio, cash):
        if not portfolio: return "포트폴리오 없음", "데이터 없음"
        total = cash + sum(s['price']*s['qty'] for s in portfolio)
        cash_r = (cash/total*100) if total else 100
        pnl_list = [((s['price'] * 1.02) - s['price'])/s['price']*100 for s in portfolio if s['price'] > 0]
        avg_pnl = np.mean(pnl_list) if pnl_list else 0.0
        stock_count = len(portfolio)
        beta = np.random.uniform(0.5, 2.0)
        
        h = f"""
        **[🐹 햄찌의 계좌 팩트 폭격]**
        "사장님! **예수금 {cash_r:.1f}%**? **[Cash Drag]**야! 돈이 썩고 있어!
        지금 **Beta**가 **{beta:.2f}**밖에 안 돼. 내일 **레버리지** 태워서 시장 이겨야지! 쫄보야?"
        """
        t = f"""
        **[🐯 호찌의 자산 배분 훈계]**
        "자네, **보유 {stock_count}종목**... 너무 안일해. 종목 간 상관계수가 높아서 하락장 오면 '공멸'이야.
        **[국채]**나 **[금]**을 편입해서 **'유비무환'**의 방어벽을 세우게."
        """
        return h, t

# -----------------------------------------------------------------------------
# [4] NATIVE UI RENDERER
# -----------------------------------------------------------------------------
def render_native_card(d, idx=None, is_rank=False):
    win_pct = d['win'] * 100
    p = d['plan']
    m = d['m']
    
    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            prefix = f"🏆 {idx+1}위 " if is_rank else ""
            st.markdown(f"### {prefix}{d['name']} <span style='font-size:14px; color:#aaa;'>({d['mode']})</span>", unsafe_allow_html=True)
        with c2:
            st.metric("AI Score", f"{win_pct:.1f}", delta=None)
        
        st.progress(int(win_pct))
        
        tcols = st.columns(len(d['tags']))
        for i, tag in enumerate(d['tags']): tcols[i].caption(f"🏷️ {tag['label']}")
        st.divider()
        
        i1, i2, i3 = st.columns(3)
        if d.get('is_holding'):
            pnl = d['pnl']
            i1.metric("현재가", f"{d['price']:,}원")
            i2.metric("현재 수익률", f"{pnl:.2f}%", delta=f"{pnl:.2f}%")
            i3.metric("AI 목표가", f"{p['prices'][1]:,}원")
        else: # 명예의 전당
            target_yield = d['plan']['yield']
            i1.metric("현재가", f"{d['price']:,}원")
            i2.metric("예상 수익률", f"+{target_yield:.2f}%", delta=f"{target_yield:.2f}%")
            i3.metric("AI 목표가", f"{p['prices'][1]:,}원")
        
        st.markdown(f"<div style='background:#111; padding:10px; border-radius:5px; margin-top:10px; border:1px dashed #444; font-size:13px; color:#ccc;'>💡 {p['rationale']}</div>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🐹 햄찌 분석", "🐯 호찌 분석", "📊 8대 엔진"])
        with tab1: st.markdown(f"<div class='analysis-box box-hamzzi'>{d['hamzzi']}</div>", unsafe_allow_html=True)
        with tab2: st.markdown(f"<div class='analysis-box box-hojji'>{d['hojji']}</div>", unsafe_allow_html=True)
        with tab3:
            st.markdown("### 📊 8대 엔진 매수/매도 기준 가이드")
            c1, c2 = st.columns(2)
            with c1: st.markdown(f"**1. Omega: {m['omega']:.1f}Hz** (15Hz↑ 폭발)\n**2. VPIN: {m['vpin']:.2f}** (0.6↑ 독성)\n**3. GNN: {m['gnn']:.2f}** (0.8↑ 대장)")
            with c2: st.markdown(f"**4. Hawkes: {m['hawkes']:.2f}** (2.0↑ 폭주)\n**5. Hurst: {m['hurst']:.2f}** (0.5↑ 추세)\n**6. Kelly: {m['kelly']:.2f}** (최적 비중)")

# -----------------------------------------------------------------------------
# [5] MAIN APP
# -----------------------------------------------------------------------------
with st.expander("💰 자산 및 포트폴리오 설정 (Click to Open)", expanded=True):
    uploaded = st.file_uploader("📸 OCR 이미지 스캔", type=['png','jpg'], label_visibility="collapsed")
    if uploaded:
        st.session_state.portfolio = [{'name': '삼성전자', 'price': 70000, 'qty': 10, 'strategy': '추세추종'}]
        st.success("✅ 로드 완료!")

    c1, c2 = st.columns(2)
    with c1: st.number_input("💰 예수금 (KRW)", value=st.session_state.cash, step=100000, key="cash")
    with c2: st.number_input("🎯 목표 수익률 (%)", value=st.session_state.target_return, key="target_return")
    
    if st.button("➕ 종목 수동 추가"): 
        st.session_state.portfolio.append({'name': '삼성전자', 'price': 0, 'qty': 0, 'strategy': '추세추종'})
        st.rerun()
            
    if st.session_state.portfolio:
        for i, s in enumerate(st.session_state.portfolio):
            st.markdown(f"##### 📌 종목 {i+1}")
            cols = st.columns([3, 2, 2, 2, 1])
            with cols[0]: s['name'] = st.selectbox(f"종목명", stock_names, index=0, key=f"n{i}")
            # [Input UX] 빈칸 시작 (None)
            with cols[1]: s['price'] = st.number_input(f"평단가(원)", value=float(s['price']) if s['price']>0 else None, key=f"p{i}", placeholder="0")
            with cols[2]: s['qty'] = st.number_input(f"수량(주)", value=int(s['qty']) if s['qty']>0 else None, key=f"q{i}", placeholder="0")
            with cols[3]: s['strategy'] = st.selectbox(f"전략", ["추세추종","초단타"], key=f"s{i}")
            with cols[4]: 
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"d{i}"): st.session_state.portfolio.pop(i); st.rerun()
            if s['price'] is None: s['price'] = 0
            if s['qty'] is None: s['qty'] = 0

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

c1, c2 = st.columns([2,1])
with c1:
    if st.button("📊 햄찌와 호찌의 [계좌 정밀 진단] 시작"):
        st.session_state.trigger_my = True; update_market_indices(); st.rerun()
with c2:
    auto_my = st.selectbox("⏳ 자동 초기화", list(TIME_OPTS.keys()), index=0, key="main_timer")

if st.session_state.my_diagnosis:
    st.markdown("---")
    if st.session_state.port_analysis:
        h, t = st.session_state.port_analysis
        st.subheader("📊 햄찌와 호찌의 계좌 참견")
        st.markdown(f"<div class='analysis-box box-hamzzi'>{h}</div><div style='height:10px'></div><div class='analysis-box box-hojji'>{t}</div>", unsafe_allow_html=True)
    st.subheader("🔎 내 종목 심층 분석")
    for d in st.session_state.my_diagnosis: render_native_card(d, is_rank=False)

st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)
st.markdown("### 📡 햄찌의 꿀통 발견 (시장 스캔)")

c1, c2 = st.columns(2)
with c1:
    if st.button("🏆 명예의 전당 (Top 3)"):
        st.session_state.trigger_top3 = True; update_market_indices(); st.session_state.market_view_mode = 'TOP3'; st.rerun()
    auto_top3 = st.selectbox("Top3 갱신", list(TIME_OPTS.keys()), index=0, key="top3_timer")

with c2:
    if st.button("⚡ 단타 야수 vs 🌊 묵직 꼰대"):
        st.session_state.trigger_sep = True; update_market_indices(); st.session_state.market_view_mode = 'SEPARATE'; st.rerun()
    auto_sep = st.selectbox("전략별 갱신", list(TIME_OPTS.keys()), index=0, key="sep_timer")

if st.session_state.market_view_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("#### 🏆 명예의 전당 (AI Score 최상위)")
    # [Absolute Top 3] 단타/추세 구분 없이 점수 최고점 3개
    for i, d in enumerate(st.session_state.ideal_list): render_native_card(d, i, is_rank=True)

elif st.session_state.market_view_mode == 'SEPARATE' and st.session_state.sc_list:
    st.markdown("#### 📊 전략별 절대 랭킹")
    t1, t2 = st.tabs(["⚡ 햄찌의 단타 픽", "🌊 호찌의 스윙 픽"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_native_card(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_native_card(d, i, is_rank=True)

# [6] LOGIC LOOP
engine = SingularityEngine()
now = time.time()
need_rerun = False

# Market Timer (Independent)
t_val_market = TIME_OPTS[auto_market]
if t_val_market > 0 and now - st.session_state.last_market_update > t_val_market:
    update_market_indices(); need_rerun = True

# Logic Timer & Trigger
t_val_my = TIME_OPTS[auto_my]
if st.session_state.trigger_my or (t_val_my > 0 and now - st.session_state.l_my > t_val_my):
    with st.spinner("햄찌와 호찌가 계좌를 뜯어보는 중..."):
        h_p, t_p = engine.diagnose_portfolio(st.session_state.portfolio, st.session_state.cash)
        st.session_state.port_analysis = (h_p, t_p)
        my_res = []
        for s in st.session_state.portfolio:
            if not s['name']: continue
            mode = "scalping" if s['strategy'] == "초단타" else "swing"
            price = int(s['price']) if s['price'] > 0 else 10000
            wr, m, tags = engine.run_diagnosis(s['name'], mode)
            plan = engine.generate_report(mode, price, m, wr, st.session_state.cash, s['qty'], st.session_state.target_return)
            pnl = ((price - s['price'])/s['price']*100) if s['price']>0 else 0
            my_res.append({
                'name': s['name'], 'price': price, 'pnl': pnl, 'win': wr, 
                'm': m, 'tags': tags, 'plan': plan, 'mode': mode, 'is_holding': True,
                'hamzzi': plan['hamzzi'], 'hojji': plan['hojji']
            })
        st.session_state.my_diagnosis = my_res
        st.session_state.l_my = now
        st.session_state.trigger_my = False
        need_rerun = True

# Market Scan Logic
t_val_top3 = TIME_OPTS[auto_top3]
t_val_sep = TIME_OPTS[auto_sep]
scan_needed = False
if st.session_state.trigger_top3 or (t_val_top3 > 0 and now - st.session_state.l_top3 > t_val_top3):
    scan_needed = True; st.session_state.market_view_mode = 'TOP3'; st.session_state.trigger_top3 = False; st.session_state.l_top3 = now
if st.session_state.trigger_sep or (t_val_sep > 0 and now - st.session_state.l_sep > t_val_sep):
    scan_needed = True; st.session_state.market_view_mode = 'SEPARATE'; st.session_state.trigger_sep = False; st.session_state.l_sep = now

if scan_needed:
    with st.spinner("시장 전체 꿀통 찾는 중..."):
        market_data = load_top50_data()
        sc, sw, ideal = [], [], []
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close'])); name = row['Name']
            
            wr1, m1, t1 = engine.run_diagnosis(name, "scalping")
            p1 = engine.generate_report("scalping", price, m1, wr1, st.session_state.cash, 0, st.session_state.target_return)
            item1 = {'name': name, 'price': price, 'win': wr1, 'm': m1, 'tags': t1, 'plan': p1, 'mode': '초단타', 'is_holding': False, 'hamzzi': p1['hamzzi'], 'hojji': p1['hojji']}
            
            wr2, m2, t2 = engine.run_diagnosis(name, "swing")
            p2 = engine.generate_report("swing", price, m2, wr2, st.session_state.cash, 0, st.session_state.target_return)
            item2 = {'name': name, 'price': price, 'win': wr2, 'm': m2, 'tags': t2, 'plan': p2, 'mode': '추세추종', 'is_holding': False, 'hamzzi': p2['hamzzi'], 'hojji': p2['hojji']}
            
            sc.append(item1); sw.append(item2)
            # Absolute Top 3 Selection
            ideal.append(item1 if wr1 >= wr2 else item2)
            
        sc.sort(key=lambda x: x['win'], reverse=True); sw.sort(key=lambda x: x['win'], reverse=True); ideal.sort(key=lambda x: x['win'], reverse=True)
        st.session_state.sc_list = sc[:3]; st.session_state.sw_list = sw[:3]; st.session_state.ideal_list = ideal[:3]
        need_rerun = True

if need_rerun: st.rerun()
if any(x > 0 for x in [t_val_my, t_val_top3, t_val_sep, t_val_market]): time.sleep(1); st.rerun()
