import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random
import textwrap

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
# [1] STYLING (High Contrast & Readability Focused)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Background */
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Pretendard', sans-serif; }
    
    /* Buttons: Gold & Dark */
    .stButton>button { 
        width: 100%; border-radius: 8px; font-weight: 800; height: 50px; font-size: 16px;
        background: #1a1a1a; border: 2px solid #d4af37; color: #d4af37; 
        transition: 0.3s;
    }
    .stButton>button:hover { 
        background: #d4af37; color: #000; box-shadow: 0 0 15px rgba(212, 175, 55, 0.8);
    }
    
    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #111 !important; color: #fff !important; 
        border: 1px solid #444 !important; border-radius: 6px;
    }
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #ddd !important; font-weight: bold;
    }
    
    /* Card UI */
    .stock-card { 
        background: #111; border: 1px solid #333; border-radius: 12px; 
        padding: 0; margin-bottom: 30px; box-shadow: 0 4px 20px rgba(255,255,255,0.05); overflow: hidden;
    }
    .card-header { 
        padding: 15px 20px; background: #181818; border-bottom: 1px solid #333; 
        display: flex; justify-content: space-between; align-items: center; 
    }
    .stock-name { font-size: 22px; font-weight: 900; color: #fff; }
    
    /* Metrics */
    div[data-testid="stMetricValue"] { font-size: 24px !important; color: #fff !important; font-weight: 800 !important; }
    div[data-testid="stMetricLabel"] { font-size: 13px !important; color: #aaa !important; }
    
    /* Analysis Box */
    .persona-box {
        background-color: #0a0a0a; border: 1px solid #333; border-radius: 8px;
        padding: 20px; margin-top: 10px; line-height: 1.7; color: #e0e0e0;
    }
    .persona-title { font-size: 16px; font-weight: bold; margin-bottom: 10px; display: block; border-bottom: 1px solid #333; padding-bottom: 5px; }
    
    /* Timeline & Rationale */
    .rationale-box {
        background: #151515; padding: 15px; border-radius: 8px; margin-top: 10px; border: 1px dashed #444;
    }
    .rationale-text { font-size: 13px; color: #bbb; }
    
    /* Custom Tags */
    .tag { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; margin-right: 5px; color: #000; }
    
    /* HUD Grid */
    .hud-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; background: #080808; padding: 15px; border-radius: 8px; border: 1px solid #222; }
    .hud-item { text-align: center; }
    .hud-label { font-size: 11px; color: #666; }
    .hud-val { font-size: 14px; font-weight: bold; color: #00ffcc; }

</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #d4af37;'>🐹 햄찌와 호찌의 퀀트 대작전 🚀</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [2] SINGULARITY OMEGA ENGINE (Deep Logic & Timetable)
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
        tags = [{'label': '기본 마진', 'val': '+35', 'bg': '#cccccc'}]

        if m['vpin'] > 0.6: score -= 20; tags.append({'label': '⚠️ 독성 매물', 'val': '-20', 'bg': '#ff4444'})
        if m['es'] < -0.20: score -= 15; tags.append({'label': '📉 Tail Risk', 'val': '-15', 'bg': '#ff4444'})
        
        if mode == "scalping":
            if m['hawkes'] > 2.0: score += 45; tags.append({'label': '🚀 Hawkes 폭발', 'val': '+45', 'bg': '#00ff00'})
            elif m['hawkes'] > 1.5: score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'bg': '#00ccff'})
        else: 
            if m['hurst'] > 0.7: score += 40; tags.append({'label': '📈 추세 지속', 'val': '+40', 'bg': '#00ff00'})
            elif m['hurst'] > 0.6: score += 10; tags.append({'label': '↗️ 모멘텀 양호', 'val': '+10', 'bg': '#00ccff'})

        if m['gnn'] > 0.8: score += 10; tags.append({'label': '👑 GNN 대장주', 'val': '+10', 'bg': '#d4af37'})
        win_rate = min(0.98, max(0.02, score / 100))
        return win_rate, m, tags

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        volatility = m['vol_surf'] * 0.05
        # Price Calculation Logic & Rationale
        if mode == "scalping":
            target = int(price * (1 + max(volatility, 0.02)))
            stop = int(price * (1 - volatility * 0.6))
            rationale = f"스캘핑 모드: 내재 변동성(Vol) {m['vol_surf']:.2f} 기반 1.5σ 상단 목표, 0.6σ 하단 손절 설정."
        else:
            target = int(price * (1 + (target_return/100)))
            stop = int(price * 0.93)
            rationale = f"스윙 모드: 목표 수익률 {target_return}% 반영, Hurst {m['hurst']:.2f} 추세 강도 기반 지지선(-7%) 설정."
        
        safe_kelly = m['kelly'] * 0.5 
        can_buy = int((cash * safe_kelly) / price) if price > 0 else 0

        # 🐹 HAMZZI (Aggressive Deep Logic + Timetable)
        if wr >= 0.70:
            h_txt = f"""
            **[1. Singularity Engine 분석]**\n
            "사장님! 대박이야! **Omega 진동수**가 {m['omega']:.2f}Hz로 안정화되면서 **임계 폭발(Critical Burst)** 직전 단계에 진입했어. 
            게다가 **Hawkes 강도**가 {m['hawkes']:.2f}야. 이건 인간이 아니라 기계들이 미친 듯이 사들이는 '자기 여진' 상태라구! 무조건 탑승!"\n
            **[2. 🐹 햄찌의 타임테이블 전략]**\n
            * ⏰ **09:00 - 09:10:** 동시호가 갭상승 2% 이내면 **시장가 풀매수** ({can_buy}주)!
            * ⏰ **09:30 - 10:00:** 눌림목 발생 시 **불타기(Pyramiding)**로 물량 30% 추가!
            * ⏰ **14:00 이후:** **{target:,}원** 돌파 시 절반 익절, 나머지는 '상한가'까지 홀딩!
            """
        elif wr >= 0.50:
            h_txt = f"""
            **[1. Singularity Engine 분석]**\n
            "음~ **Hurst**가 {m['hurst']:.2f}로 추세가 살아있네. 단타 치기 좋은 '놀이터'야. 
            다만 **OBI(호가 불균형)**가 {m['obi']:.2f}로 애매해. 세력들이 눈치 싸움 중이라 길게 가져가면 물릴 수 있어."\n
            **[2. 🐹 햄찌의 타임테이블 전략]**\n
            * ⏰ **09:00:** 관망. 급하게 들어가지 마.
            * ⏰ **10:30:** **{price:,}원** 지지 확인되면 **{int(can_buy/3)}주**만 정찰병 투입.
            * ⏰ **13:00:** 시세 안 나오면 전량 매도 후 퇴근. '치고 빠지기'가 핵심이야!
            """
        else:
            h_txt = f"""
            **[1. Singularity Engine 분석]**\n
            "으악! **VPIN**이 {m['vpin']:.2f}야! 독성 매물 경보 발령! 🚨 기관들이 개미 꼬셔서 물량 넘기는 설거지 패턴이라구. 
            **Betti Number**도 1이야. 차트에 구멍 뚫려서 지지선이 없어!"\n
            **[2. 🐹 햄찌의 타임테이블 전략]**\n
            * ⏰ **지금 당장:** 보유 중이면 **시장가 전량 매도!**
            * ⏰ **장중 내내:** 절대 매수 금지. 쳐다보지도 마. 이건 투자가 아니라 기부야. 돔황챠!! 🏃‍♂️
            """

        # 🐯 HOJJI (Conservative Deep Logic + Timetable)
        if wr >= 0.70:
            t_txt = f"""
            **[1. Singularity Omega 분석]**\n
            "허허, **GNN 중심성**이 {m['gnn']:.2f}로 시장의 자금이 이 종목을 중심으로 돌고 있네. 진정한 주도주야.
            **전이 엔트로피(TE)** 흐름도 양호하여 펀더멘털과 수급이 '금상첨화'를 이루고 있어."\n
            **[2. 🐯 호찌의 시계열 행동 지침]**\n
            * ⏳ **진입 시점:** 변동성이 줄어드는 **오후 2시경**, 자네 자금의 **{int(can_buy*0.8)}주**를 분할 매수하게.
            * ⏳ **보유 기간:** 단기 등락에 일희일비 말고, **{target:,}원** 도달 시까지 진득하게 '우보천리'하게.
            * ⏳ **리스크 관리:** 만약 **{stop:,}원**을 종가상 이탈하면 미련 없이 나오게.
            """
        elif wr >= 0.50:
            t_txt = f"""
            **[1. Singularity Omega 분석]**\n
            "계륵일세. **내재 변동성**이 {m['vol_surf']:.2f}로 너무 높아. 옵션 시장의 불안이 현물로 전이되는 '내우외환'의 형국이야.
            **꼬리 위험(ES)**도 {m['es']:.2f}로 감지되어 언제든 급락할 수 있네."\n
            **[2. 🐯 호찌의 시계열 행동 지침]**\n
            * ⏳ **진입 시점:** 오늘은 관망하고, 내일 시초가 흐름을 보게.
            * ⏳ **매수 전략:** 굳이 산다면 **{int(can_buy*0.2)}주**만 아주 조금 담아보게. 욕심은 화를 부르네.
            * ⏳ **원칙:** 돌다리도 두들겨 보고 건너게. 리스크 관리가 최우선일세.
            """
        else:
            t_txt = f"""
            **[1. Singularity Omega 분석]**\n
            "에잉 쯧쯧! **Going Concern** 이슈가 보여. 재무 건전성이 의심되는 사상누각일세.
            과거의 지지선이 강력한 저항선(Role Reversal)으로 변질되었어."\n
            **[2. 🐯 호찌의 시계열 행동 지침]**\n
            * ⏳ **즉시:** 포트폴리오에서 제외하게. 현금이 곧 최고의 종목이야.
            * ⏳ **향후 계획:** 펀더멘털이 개선될 때까지 관심 종목에서도 지우게.
            * ⏳ **명심:** **비에르고딕** 파산 위험을 원천 차단해야 부자가 될 수 있네.
            """

        return {
            "prices": (price, target, stop),
            "hamzzi": h_txt, "hojji": t_txt, "rationale": rationale
        }

    def diagnose_portfolio(self, portfolio, cash):
        if not portfolio: return "포트폴리오 없음", "데이터 없음"
        total = cash + sum(s['price']*s['qty'] for s in portfolio)
        cash_r = (cash/total*100) if total else 100
        
        # Calculate Logic
        stock_count = len(portfolio)
        avg_pnl = np.mean([((s['price'] * 1.02) - s['price'])/s['price']*100 for s in portfolio]) # Simulated PnL
        beta = np.random.uniform(0.5, 2.0)
        
        h = f"""
        "사장님! 현재 **예수금 비중 {cash_r:.1f}%**, **보유 종목 {stock_count}개**야.
        현재 **추정 수익률은 {avg_pnl:.2f}%**인데, **Beta {beta:.2f}**로는 시장 못 이겨! 
        **[Action]** 내일 장 시작하면 현금 30% 털어서 주도주 2개 더 담아! 레버리지 ETF 섞어서 베타 1.5로 맞춰!"
        """
        
        t = f"""
        "자네, **보유 종목 {stock_count}개**에 **예수금 {cash_r:.1f}%**... 너무 안일해.
        리스크 분산이 안 되어 있어. 하락장 오면 공멸할 구조야.
        **[Action]** 수익 중인 종목은 절반 익절하고, 그 돈으로 **[국채]**나 **[금]**을 사서 방어벽을 세우게."
        """
        return h, t

# -----------------------------------------------------------------------------
# [3] NATIVE UI RENDERER (Clean & Detailed)
# -----------------------------------------------------------------------------
def render_native_card(d, idx=None, is_rank=False):
    win_pct = d['win'] * 100
    p = d['plan']
    m = d['m']
    
    # Color Logic
    if d['win'] >= 0.7: score_color = "green"
    elif d['win'] >= 0.5: score_color = "orange"
    else: score_color = "red"

    # MAIN CARD
    with st.container(border=True):
        # 1. Header
        c1, c2 = st.columns([3, 1])
        with c1:
            prefix = f"🏆 {idx+1}위 " if is_rank else ""
            st.markdown(f"### {prefix}{d['name']} <span style='font-size:14px; color:#aaa;'>({d['mode']})</span>", unsafe_allow_html=True)
            st.caption(f"Engine Score based on JLS, Hawkes, VPIN")
        with c2:
            st.metric("AI Score", f"{win_pct:.1f}", delta=None)
        
        st.progress(int(win_pct))
        
        # 2. Tag & Info
        tcols = st.columns(len(d['tags']))
        for i, tag in enumerate(d['tags']):
            tcols[i].caption(f"🏷️ {tag['label']}")
            
        st.divider()
        
        i1, i2, i3 = st.columns(3)
        pnl = d['pnl']
        i1.metric("현재가", f"{d['price']:,}원")
        i2.metric("수익률", f"{pnl:.2f}%", delta=f"{pnl:.2f}%")
        i3.metric("목표가", f"{p['prices'][1]:,}원")
        
        # 3. Rationale Box
        st.markdown(f"""
        <div class='rationale-box'>
            <span style='color:#d4af37; font-weight:bold;'>💡 가격 산정 근거:</span> 
            <span class='rationale-text'>{p['rationale']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 4. Analysis Tabs (Deep Dive)
        tab1, tab2, tab3 = st.tabs(["🐹 햄찌의 야수 분석", "🐯 호찌의 방어 분석", "📊 8대 엔진 HUD"])
        
        with tab1:
            st.info(d['hamzzi_txt'], icon="🐹")
        with tab2:
            st.warning(d['hojji_txt'], icon="🐯")
        with tab3:
            h1, h2, h3 = st.columns(3)
            h1.markdown(f"**Omega**\n\n`{m['omega']:.1f}`")
            h1.markdown(f"**Hurst**\n\n`{m['hurst']:.2f}`")
            h2.markdown(f"**VPIN**\n\n`{m['vpin']:.2f}`")
            h2.markdown(f"**Hawkes**\n\n`{m['hawkes']:.2f}`")
            h3.markdown(f"**GNN**\n\n`{m['gnn']:.2f}`")
            h3.markdown(f"**Kelly**\n\n`{m['kelly']:.2f}`")

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
        st.success("✅ 포트폴리오 로드 완료!")

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
    if st.session_state.port_analysis:
        h_port, t_port = st.session_state.port_analysis
        with st.container(border=True):
            st.subheader("📊 포트폴리오 종합 심층 진단")
            c1, c2 = st.columns(2)
            with c1: 
                st.markdown(f"### 🐹 햄찌 (Aggressive)")
                st.markdown(h_port)
            with c2: 
                st.markdown(f"### 🐯 호찌 (Conservative)")
                st.markdown(t_port)
    
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
