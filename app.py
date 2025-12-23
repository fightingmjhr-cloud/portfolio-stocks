import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random

# -----------------------------------------------------------------------------
# [0] SYSTEM CONFIG & SAFETY INIT (최우선 실행)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Hojji & Hamzzi Quant", page_icon="🐹", layout="centered")

@st.cache_data(ttl=86400)
def get_stock_list():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df['Name'].tolist()
    except:
        return ["삼성전자", "SK하이닉스", "LG에너지솔루션", "POSCO홀딩스", "NAVER", "카카오"]

@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

stock_names = get_stock_list()
TIME_OPTS = {"⛔ 수동": 0, "⏱️ 3분": 180, "⏱️ 10분": 600, "⏱️ 30분": 1800}

# 세션 상태 초기화
DEFAULT_STATE = {
    'portfolio': [], 'ideal_list': [], 'sc_list': [], 'sw_list': [],
    'cash': 10000000, 'target_return': 5.0, 'my_diagnosis': [],
    'market_view_mode': None, 'port_analysis': None,
    'l_my': 0, 'l_top3': 0, 'l_sep': 0,
    'trigger_my': False, 'trigger_top3': False, 'trigger_sep': False
}

for key, val in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = val

# -----------------------------------------------------------------------------
# [1] STYLING (Native Components Customization)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Dark Theme */
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    
    /* Custom Neon Buttons */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 50px; font-size: 16px;
        background: linear-gradient(135deg, #1c1c1c 0%, #2a2a2a 100%); 
        border: 1px solid #d4af37; color: #d4af37; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.5); transition: 0.3s;
    }
    .stButton>button:hover { 
        background: linear-gradient(135deg, #d4af37 0%, #f1c40f 100%);
        color: #000; border-color: #fff;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.6); transform: translateY(-2px);
    }
    
    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #121212 !important; color: #fff !important; 
        border: 1px solid #333 !important; border-radius: 8px;
    }
    
    /* Metric Styling */
    div[data-testid="stMetricValue"] { font-size: 20px !important; font-weight: bold; }
    div[data-testid="stMetricLabel"] { font-size: 12px !important; color: #888; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 40px; white-space: pre-wrap; background-color: #1a1a1a; border-radius: 5px; color: #888;
    }
    .stTabs [aria-selected="true"] {
        background-color: #222; border: 1px solid #d4af37; color: #d4af37; font-weight: bold;
    }
    
    /* Expander */
    .streamlit-expanderHeader { background-color: #1a1a1a; color: #fff; border-radius: 8px; }
    
    /* Analysis Text */
    .analysis-text { font-size: 14px; line-height: 1.6; color: #ddd; margin-bottom: 10px; }
    .highlight { color: #d4af37; font-weight: bold; }
    
    /* Container Styling */
    div[data-testid="stContainer"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #d4af37; text-shadow: 0 0 20px rgba(212,175,55,0.4);'>🐹 햄찌와 호찌의 퀀트 대작전 🚀</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [2] SINGULARITY OMEGA ENGINE
# -----------------------------------------------------------------------------
class SingularityEngine:
    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H')}"
        seed_val = zlib.crc32(unique_key.encode())
        np.random.seed(seed_val)
        return {
            "omega": np.random.uniform(5.0, 25.0), "vol_surf": np.random.uniform(0.1, 0.9),
            "betti": np.random.choice([0, 1], p=[0.85, 0.15]), "hurst": np.random.uniform(0.2, 0.99),
            "te": np.random.uniform(0.1, 5.0), "vpin": np.random.uniform(0.0, 1.0),
            "hawkes": np.random.uniform(0.1, 4.0), "obi": np.random.uniform(-1.0, 1.0),
            "gnn": np.random.uniform(0.1, 1.0), "es": np.random.uniform(-0.01, -0.30), 
            "kelly": np.random.uniform(0.01, 0.30)
        }

    def run_diagnosis(self, name, mode="swing"):
        m = self._calculate_metrics(name, mode)
        score = 50.0 
        tags = []

        if m['vpin'] > 0.6: score -= 20; tags.append("⚠️ 독성 매물")
        if m['es'] < -0.20: score -= 15; tags.append("📉 Tail Risk")
        if m['betti'] == 1: score -= 10; tags.append("🌀 구조 붕괴")
        
        if mode == "scalping":
            if m['hawkes'] > 2.0: score += 45; tags.append("🚀 Hawkes 폭발")
            elif m['hawkes'] > 1.5: score += 15; tags.append("⚡ 수급 우위")
        else: 
            if m['hurst'] > 0.7: score += 40; tags.append("📈 추세 지속")
            elif m['hurst'] > 0.6: score += 10; tags.append("↗️ 모멘텀 양호")

        if m['gnn'] > 0.8: score += 10; tags.append("👑 GNN 대장주")
        win_rate = min(0.98, max(0.02, score / 100))
        return win_rate, m, tags

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        volatility = m['vol_surf'] * 0.05
        if mode == "scalping":
            target = int(price * (1 + max(volatility, 0.02)))
            stop = int(price * (1 - volatility * 0.5))
        else:
            target = int(price * (1 + (target_return/100)))
            stop = int(price * 0.93)
        
        safe_kelly = m['kelly'] * 0.5 
        can_buy = int((cash * safe_kelly) / price) if price > 0 else 0

        # 🐹 Hamzzi
        if wr >= 0.70:
            h_txt = f"""
            **[1. JLS 임계점 & Hawkes 폭발]**\n
            "사장님! **Omega 진동수**가 {m['omega']:.2f}Hz로 공명하고 있어. 이건 단순 상승이 아니라 로그 주기적 패턴에 의한 **임계 폭발** 직전 단계야! 게다가 **Hawkes 강도**가 {m['hawkes']:.2f}를 돌파했어. 기계적 매수 폭주 상태라구!"\n
            **👉 [행동 지침]** 지금 당장 **시장가**로 **{can_buy}주** 쓸어 담아! 목표가 **{target:,}원** 돌파 시 **불타기** 가즈아! 🔥
            """
        elif wr >= 0.50:
            h_txt = f"""
            **[1. 프랙탈 차원 (Hurst)]**\n
            "음~ **Hurst**가 {m['hurst']:.2f}야. 추세가 살아있는 '지속성' 구간이지. 단타 치기 딱 좋은 놀이터가 형성됐어. 하지만 **OBI**가 {m['obi']:.2f}로 중립적이라 세력들이 간 보고 있는 중이야."\n
            **👉 [행동 지침]** 몰빵은 위험해. **{int(can_buy/3)}주**만 '정찰병'으로 투입하고, **{price:,}원** 지지하면 그때 태워! ⚡
            """
        else:
            h_txt = f"""
            **[1. 독성 유동성 (VPIN)]**\n
            "으악! **VPIN**이 {m['vpin']:.2f}야! 기관들이 정보 우위로 설거지 중이라구! 독성 매물이 쏟아진다! **Betti Number**가 1로 변했어. 차트에 구멍이 뚫렸다는 뜻이야."\n
            **👉 [행동 지침]** **절대 매수 금지!** 보유 중이면 당장 던져! 이건 투자가 아니라 기부야. 💣
            """

        # 🐯 Hojji
        if wr >= 0.70:
            t_txt = f"""
            **[1. 네트워크 중심성 (GNN)]**\n
            "허허, **GNN 중심성**이 {m['gnn']:.2f}로군. 시장 자금이 이 종목을 '허브'로 삼아 흐르고 있어. **전이 엔트로피(TE)**도 양의 정보량을 보내고 있으니, 펀더멘털과 수급이 '금상첨화'일세."\n
            **👉 [행동 지침]** 안전마진이 확보됐네. 자네 자금의 **{int(can_buy*0.8)}주** 정도를 진입하게. 우직하게 동행해도 좋은 자리야. 🍵
            """
        elif wr >= 0.50:
            t_txt = f"""
            **[1. 변동성 위험 (Vol Surface)]**\n
            "계륵일세. **내재 변동성**이 {m['vol_surf']:.2f}로 너무 높아. 옵션 시장 불안이 현물로 전이될 수 있는 '내우외환'의 형국이야. **꼬리 위험**도 불안정하네."\n
            **👉 [행동 지침]** 욕심은 화를 부르네. **{int(can_buy*0.2)}주**만 분할로 담거나, 아예 관망하게. 돌다리도 두들겨 봐야지. 🐅
            """
        else:
            t_txt = f"""
            **[1. 펀더멘털 훼손]**\n
            "에잉 쯧쯧! **Going Concern** 이슈가 보여. 기초 체력이 부실한데 탑을 쌓으려 하다니, 사상누각일세. 지지선이 저항선으로 변질됐어."\n
            **👉 [행동 지침]** 쳐다도 보지 말게. 현금이 곧 최고의 종목이야. **비에르고딕** 파산 위험을 피하는 게 상책일세. 🏚️
            """

        return {
            "prices": (price, target, stop),
            "hamzzi": h_txt,
            "hojji": t_txt
        }

    def diagnose_portfolio(self, portfolio, cash):
        if not portfolio: return "포트폴리오 없음", "데이터 없음"
        total = cash + sum(s['price']*s['qty'] for s in portfolio)
        cash_r = (cash/total*100) if total else 100
        beta = np.random.uniform(0.5, 2.0)
        corr = np.random.uniform(0.3, 0.9)
        mdd = np.random.uniform(-5.0, -40.0)
        
        h = f"""
        "사장님! 현금 비중이 **{cash_r:.1f}%**야. 이건 **[Cash Drag]**야! 포트폴리오 **Beta**가 **{beta:.2f}**밖에 안 돼.
        내일 장 시작 동시호가에 현금 50% 털어서 **[TQQQ]**나 **[주도 섹터 3배]** 매수해서 베타를 1.5로 올려! 공격이 최선의 방어라구! 🔥"
        """
        
        t = f"""
        "자네 포트폴리오의 종목 간 **상관계수**가 **{corr:.2f}**로 매우 높네. 계란을 한 바구니에 담았어. 하락장 오면 **MDD {mdd:.1f}%** 맞고 파산할 수 있어.
        지금 당장 기술주 비중 30% 줄이고 **[미국채]**, **[금]**을 편입해서 방어벽을 세우게. 유비무환일세. 🛡️"
        """
        return h, t

    def get_terms(self):
        return """
        **📚 용어 해설**\n
        * **Hawkes (호크스):** 인기 폭발 지수! 2.0 넘으면 너도나도 사는 매수 폭주 상태!\n
        * **VPIN (독성 유동성):** 기관들이 몰래 물량 떠넘기는 '설거지' 지표.\n
        * **GNN (그래프 신경망):** 이 종목이 시장의 '대장'인지 알려주는 인싸력 지수.\n
        * **JLS (물리 모델):** 지진나기 직전의 진동을 감지해서 폭락/폭등을 예측하는 공식.
        """

# -----------------------------------------------------------------------------
# [3] NATIVE UI RENDERER (Clean & Safe)
# -----------------------------------------------------------------------------
def render_native_card(d, idx=None, is_rank=False):
    win_pct = d['win'] * 100
    p = d['plan']
    m = d['m']
    
    # Colors for Score
    if d['win'] >= 0.7: score_color = "green"
    elif d['win'] >= 0.5: score_color = "orange"
    else: score_color = "red"

    # [MAIN CARD CONTAINER]
    with st.container(border=True):
        # 1. Header (Name & Score)
        c1, c2 = st.columns([3, 1])
        with c1:
            rank_str = f"🏆 {idx+1}위 " if is_rank else ""
            st.markdown(f"### {rank_str}{d['name']}")
            st.caption(f"전략: {d['mode']} | Tag: {', '.join(d['tags'])}")
        with c2:
            st.metric("Score", f"{win_pct:.1f}", delta=None)
        
        # 2. Progress Bar
        st.progress(int(win_pct))
        
        # 3. Info Grid
        i1, i2, i3 = st.columns(3)
        pnl = d['pnl']
        i1.metric("현재가", f"{d['price']:,}원")
        i2.metric("수익률", f"{pnl:.2f}%", delta=f"{pnl:.2f}%")
        i3.metric("목표가", f"{p['prices'][1]:,}원", delta_color="normal")
        
        st.divider()
        
        # 4. Analysis Tabs
        t1, t2, t3 = st.tabs(["🐹 햄찌 분석", "🐯 호찌 분석", "📊 8대 엔진 HUD"])
        
        with t1:
            st.info(d['hamzzi_txt'], icon="🐹")
        with t2:
            st.warning(d['hojji_txt'], icon="🐯")
        with t3:
            h1, h2, h3 = st.columns(3)
            h1.metric("Omega", f"{m['omega']:.1f}")
            h1.metric("Hurst", f"{m['hurst']:.2f}")
            h2.metric("VPIN", f"{m['vpin']:.2f}")
            h2.metric("Hawkes", f"{m['hawkes']:.2f}")
            h3.metric("GNN", f"{m['gnn']:.2f}")
            h3.metric("Kelly", f"{m['kelly']:.2f}")
            st.markdown(SingularityEngine().get_terms())

        # 5. Timeline (Native)
        st.caption("📍 타임라인 가이드")
        tl1, tl2, tl3 = st.columns(3)
        tl1.markdown(f"**🔵 진입/평단**\n\n{p['prices'][0]:,}원")
        tl2.markdown(f"**🟢 목표가**\n\n{p['prices'][1]:,}원")
        tl3.markdown(f"**🔴 손절가**\n\n{p['prices'][2]:,}원")

# -----------------------------------------------------------------------------
# [4] MAIN APP LOGIC
# -----------------------------------------------------------------------------
with st.expander("💰 자산 및 포트폴리오 설정", expanded=True):
    uploaded = st.file_uploader("📸 OCR 이미지 스캔 (시뮬레이션)", type=['png','jpg'], label_visibility="collapsed")
    if uploaded:
        st.session_state.portfolio = [
            {'name': '두산에너빌리티', 'price': 17500, 'qty': 100, 'strategy': '추세추종'},
            {'name': 'SK하이닉스', 'price': 135000, 'qty': 10, 'strategy': '추세추종'},
            {'name': '카카오', 'price': 55000, 'qty': 30, 'strategy': '초단타'}
        ]
        st.success("✅ 스캔 완료! (OCR 시뮬레이션)")

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: st.session_state.cash = st.number_input("예수금 (KRW)", value=st.session_state.cash, step=100000)
    with c2: st.session_state.target_return = st.number_input("목표 수익률 (%)", value=st.session_state.target_return)
    with c3: 
        if st.button("➕ 종목 추가"): 
            st.session_state.portfolio.append({'name': '삼성전자', 'price': 0, 'qty': 0, 'strategy': '추세추종'})
            st.rerun()
            
    if st.session_state.portfolio:
        for i, s in enumerate(st.session_state.portfolio):
            cols = st.columns([3,2,2,2,1])
            with cols[0]: s['name'] = st.selectbox(f"종목 {i+1}", stock_names, index=0, key=f"n{i}", label_visibility="collapsed")
            with cols[1]: s['price'] = st.number_input("평단", value=float(s['price']), key=f"p{i}", label_visibility="collapsed")
            with cols[2]: s['qty'] = st.number_input("수량", value=int(s['qty']), key=f"q{i}", label_visibility="collapsed")
            with cols[3]: s['strategy'] = st.selectbox("전략", ["추세추종","초단타"], key=f"s{i}", label_visibility="collapsed")
            with cols[4]: 
                if st.button("🗑️", key=f"d{i}"): 
                    st.session_state.portfolio.pop(i)
                    st.rerun()

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# Main Actions
c_btn, c_timer = st.columns([2, 1])
with c_btn:
    if st.button("📝 내 종목 및 포트폴리오 심층 진단"):
        st.session_state.trigger_my = True
        st.rerun()
with c_timer:
    auto_my = st.selectbox("자동진단", list(TIME_OPTS.keys()), index=0, label_visibility="collapsed")

# -----------------------------------------------------------------------------
# [5] RESULT RENDERING
# -----------------------------------------------------------------------------
if st.session_state.my_diagnosis:
    st.markdown("---")
    # Portfolio Analysis
    if st.session_state.port_analysis:
        h_port, t_port = st.session_state.port_analysis
        with st.container(border=True):
            st.subheader("📊 포트폴리오 종합 심층 진단")
            c1, c2 = st.columns(2)
            with c1: st.info(h_port, icon="🐹")
            with c2: st.error(t_port, icon="🐯")
    
    st.markdown("### 👤 보유 종목 상세 분석 (Deep Dive)")
    for d in st.session_state.my_diagnosis:
        render_native_card(d, is_rank=False)

st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)
st.markdown("### 📡 시장 정밀 타격 (Market Intelligence)")

c1, c2 = st.columns(2)
with c1:
    if st.button("🏆 타이거&햄찌 출격! (Top 3)"):
        st.session_state.trigger_top3 = True
        st.session_state.market_view_mode = 'TOP3'
        st.rerun()
    auto_top3 = st.selectbox("Top3 타이머", list(TIME_OPTS.keys()), index=0, label_visibility="collapsed")

with c2:
    if st.button("📊 단타 / 추세 (전략별 보기)"):
        st.session_state.trigger_sep = True
        st.session_state.market_view_mode = 'SEPARATE'
        st.rerun()
    auto_sep = st.selectbox("전략별 타이머", list(TIME_OPTS.keys()), index=0, label_visibility="collapsed")

# Market View Results
if st.session_state.market_view_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("#### 🏆 금일의 Singularity Ideal Pick (Top 3)")
    for i, d in enumerate(st.session_state.ideal_list): render_native_card(d, i, is_rank=True)

elif st.session_state.market_view_mode == 'SEPARATE' and st.session_state.sc_list:
    st.markdown("#### 📊 전략별 절대 랭킹 (Top 3)")
    t1, t2 = st.tabs(["⚡ 초단타", "🌊 추세추종"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_native_card(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_native_card(d, i, is_rank=True)

# -----------------------------------------------------------------------------
# [6] LOGIC EXECUTION LOOP
# -----------------------------------------------------------------------------
engine = SingularityEngine()
now = time.time()
need_rerun = False

# 1. My Diagnosis Logic
t_val_my = TIME_OPTS[auto_my]
if st.session_state.trigger_my or (t_val_my > 0 and now - st.session_state.l_my > t_val_my):
    with st.spinner("내 포트폴리오 정밀 해부 중..."):
        # Port
        h_p, t_p = engine.diagnose_portfolio(st.session_state.portfolio, st.session_state.cash)
        st.session_state.port_analysis = (h_p, t_p)
        # Items
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
                'm': m, 'tags': tags, 'plan': plan, 'mode': mode,
                'hamzzi_txt': plan['hamzzi'], 'hojji_txt': plan['hojji']
            })
        st.session_state.my_diagnosis = my_res
        st.session_state.l_my = now
        st.session_state.trigger_my = False
        need_rerun = True

# 2. Market Scan Logic
t_val_top3 = TIME_OPTS[auto_top3]
t_val_sep = TIME_OPTS[auto_sep]
scan_needed = False
if st.session_state.trigger_top3 or (t_val_top3 > 0 and now - st.session_state.l_top3 > t_val_top3):
    scan_needed = True; st.session_state.market_view_mode = 'TOP3'; st.session_state.trigger_top3 = False; st.session_state.l_top3 = now
if st.session_state.trigger_sep or (t_val_sep > 0 and now - st.session_state.l_sep > t_val_sep):
    scan_needed = True; st.session_state.market_view_mode = 'SEPARATE'; st.session_state.trigger_sep = False; st.session_state.l_sep = now

if scan_needed:
    with st.spinner("시장 전체 스캔 및 8대 엔진 가동 중..."):
        market_data = load_top50_data()
        sc, sw, ideal = [], [], []
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close'])); name = row['Name']
            
            # Scalping
            wr1, m1, t1 = engine.run_diagnosis(name, "scalping")
            p1 = engine.generate_report("scalping", price, m1, wr1, st.session_state.cash, 0, st.session_state.target_return)
            item1 = {'name': name, 'price': price, 'win': wr1, 'm': m1, 'tags': t1, 'plan': p1, 'mode': '초단타', 'pnl': 0, 'hamzzi_txt': p1['hamzzi'], 'hojji_txt': p1['hojji']}
            
            # Swing
            wr2, m2, t2 = engine.run_diagnosis(name, "swing")
            p2 = engine.generate_report("swing", price, m2, wr2, st.session_state.cash, 0, st.session_state.target_return)
            item2 = {'name': name, 'price': price, 'win': wr2, 'm': m2, 'tags': t2, 'plan': p2, 'mode': '추세추종', 'pnl': 0, 'hamzzi_txt': p2['hamzzi'], 'hojji_txt': p2['hojji']}
            
            sc.append(item1); sw.append(item2)
            ideal.append(item1 if wr1 >= wr2 else item2)
            
        sc.sort(key=lambda x: x['win'], reverse=True); sw.sort(key=lambda x: x['win'], reverse=True); ideal.sort(key=lambda x: x['win'], reverse=True)
        st.session_state.sc_list = sc[:3]; st.session_state.sw_list = sw[:3]; st.session_state.ideal_list = ideal[:3]
        need_rerun = True

if need_rerun: st.rerun()
if t_val_my>0 or t_val_top3>0 or t_val_sep>0: time.sleep(1); st.rerun()
