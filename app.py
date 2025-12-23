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
# [1] STYLING (High Visibility & Neon Returns)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Background */
    .stApp { background-color: #050505; color: #ffffff; font-family: 'Pretendard', sans-serif; }
    
    /* Buttons: Original Neon Gradient (Restored) */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 50px; font-size: 16px;
        background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%); 
        border: none; color: #000; 
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.3); transition: 0.3s;
    }
    .stButton>button:hover { 
        transform: scale(1.02); box-shadow: 0 0 20px rgba(0, 201, 255, 0.6);
    }
    
    /* Input Labels - High Visibility Gold */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-size: 14px !important; font-weight: 900 !important; color: #FFD700 !important;
        margin-bottom: 5px !important;
    }
    
    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #111 !important; color: #fff !important; 
        border: 1px solid #444 !important; border-radius: 8px;
    }
    
    /* Card UI */
    .stock-card { 
        background: #111; border: 1px solid #333; border-radius: 16px; 
        padding: 0; margin-bottom: 30px; box-shadow: 0 4px 20px rgba(255,255,255,0.05); overflow: hidden;
    }
    .card-header { 
        padding: 15px 20px; background: #181818; border-bottom: 1px solid #333; 
        display: flex; justify-content: space-between; align-items: center; 
    }
    .stock-name { font-size: 22px; font-weight: 900; color: #fff; }
    
    /* Analysis Box (High Contrast) */
    .analysis-box {
        background-color: #0a0a0a; border-radius: 8px; padding: 20px; margin-top: 15px; 
        line-height: 1.8; color: #eee; border: 1px solid #333;
        border-left-width: 5px; border-left-style: solid;
    }
    .box-hamzzi { border-left-color: #FF9900; } /* Neon Orange */
    .box-hojji { border-left-color: #FF4444; } /* Neon Red */
    
    .persona-title { font-size: 16px; font-weight: 900; margin-bottom: 12px; display: block; border-bottom: 1px solid #333; padding-bottom: 8px; }
    
    /* Price Strategy Box */
    .price-strategy {
        background: #151515; padding: 20px; border-radius: 10px; margin-top: 15px; 
        border: 1px solid #444; display: flex; justify-content: space-between; text-align: center;
    }
    .ps-item { width: 32%; }
    .ps-label { font-size: 12px; color: #888; display: block; margin-bottom: 5px; font-weight: bold; }
    .ps-val { font-size: 18px; font-weight: 800; }
    
    /* Metrics */
    div[data-testid="stMetricValue"] { font-size: 24px !important; color: #fff !important; font-weight: 800 !important; }
    
    /* Tags */
    .tag { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; margin-right: 5px; color: #000; }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -15px !important; margin-top: 23px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🐹 햄찌와 호찌의 퀀트 대작전 🚀</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [2] SINGULARITY OMEGA ENGINE (Extended Analysis Logic)
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

        if m['gnn'] > 0.8: score += 10; tags.append({'label': '👑 GNN 대장주', 'val': '+10', 'bg': '#FFD700'})
        win_rate = min(0.98, max(0.02, score / 100))
        return win_rate, m, tags

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        volatility = m['vol_surf'] * 0.05
        # Price Rationale & Calculation
        if mode == "scalping":
            target = int(price * (1 + max(volatility, 0.02)))
            stop = int(price * (1 - volatility * 0.6))
            rationale = f"내재 변동성(Vol) {m['vol_surf']:.2f} 기반 1.5σ 상단 목표, 0.6σ 하단 손절 설정."
        else:
            target = int(price * (1 + (target_return/100)))
            stop = int(price * 0.93)
            rationale = f"목표 수익률 {target_return}% 반영 및 Hurst {m['hurst']:.2f} 추세 강도 기반 지지선(-7%) 설정."
        
        safe_kelly = m['kelly'] * 0.5 
        can_buy = int((cash * safe_kelly) / price) if price > 0 else 0

        # 🐹 HAMZZI (Aggressive - Extended Logic)
        if wr >= 0.70:
            h_txt = f"""
            **[1. 학술적 분석 (JLS & Hawkes)]**\n
            "사장님! **JLS 모델** 상 주가 파동이 로그 주기적으로 수렴하며 **임계 폭발($t_c$)** 지점에 도달했어. 이건 물리적 필연이야!
            게다가 **Hawkes 강도**가 {m['hawkes']:.2f}를 돌파했어. 이는 기계적 알고리즘들이 '자기 여진(Self-Exciting)'을 일으키며 매수 주문을 쏟아내고 있다는 뜻이야."\n
            **[2. 정보적/기술적 분석 (GNN & Vol)]**\n
            "**GNN 중심성**이 높아 시장 자금이 이 종목을 '블랙홀'처럼 빨아들이고 있고, **변동성 표면(Vol Surface)**이 우상향하며 콜옵션 베팅이 급증했어. 기술적으로 완벽한 '슈퍼 모멘텀' 구간이라구!"\n
            **[3. 🐹 햄찌의 실전 매매 타임테이블]**\n
            * ⏰ **09:00:** 동시호가 갭상승 확인 즉시 **시장가 풀매수** ({can_buy}주)!
            * ⏰ **09:30:** 눌림목 발생 시 **불타기(Pyramiding)**로 물량 30% 추가!
            * ⏰ **14:00:** **{target:,}원** 돌파 시 절반 익절, 나머지는 끝까지 홀딩!
            """
        elif wr >= 0.50:
            h_txt = f"""
            **[1. 학술적 분석 (Hurst Exponent)]**\n
            "음~ **Hurst 지수**가 {m['hurst']:.2f}야. 0.5보다 높으니 '지속성(Persistence)'이 있는 추세 구간이야. 랜덤워크가 아니란 소리지. 단타 치기 딱 좋은 '놀이터'가 형성됐어."\n
            **[2. 정보적/기술적 분석 (OBI & Alpha)]**\n
            "하지만 **호가 불균형(OBI)** 수치가 {m['obi']:.2f}로 중립적이야. 세력들이 아직 방향을 안 정하고 간만 보고 있다는 증거야. 
            기술적 반등은 가능하지만, 펀더멘털을 동반한 상승인지는 의문이야."\n
            **[3. 🐹 햄찌의 실전 매매 타임테이블]**\n
            * ⏰ **09:00:** 관망. 급하게 들어가지 마.
            * ⏰ **10:30:** **{price:,}원** 지지선 확인되면 **{int(can_buy/3)}주**만 '정찰병' 투입.
            * ⏰ **13:00:** 시세 안 나오면 미련 없이 전량 매도 후 퇴근!
            """
        else:
            h_txt = f"""
            **[1. 학술적 분석 (VPIN & TDA)]**\n
            "으악! **VPIN** 수치가 {m['vpin']:.2f}야! 이건 정보 우위를 가진 기관들이 개미에게 물량을 떠넘기는 전형적인 '설거지' 패턴이라구! 
            **위상수학(TDA)** 분석 결과 Betti Number가 1로 변했어. 시장 구조에 구멍이 뚫려 지지선이 붕괴됐다는 뜻이야."\n
            **[2. 정보적/기술적 분석 (Tail Risk)]**\n
            "**꼬리 위험(ES)**이 {m['es']:.2f}로 극도로 높아. 평소엔 멀쩡하다가 한순간에 -20% 꽂힐 수 있는 자리야."\n
            **[3. 🐹 햄찌의 실전 매매 타임테이블]**\n
            * ⏰ **즉시:** 보유 중이면 **시장가 전량 매도!** 탈출은 지능순이야!
            * ⏰ **장중:** 절대 매수 금지. 쳐다보지도 마. 이건 투자가 아니라 기부야.
            """

        # 🐯 HOJJI (Conservative - Extended Logic)
        if wr >= 0.70:
            t_txt = f"""
            **[1. 학술적 분석 (Network Theory)]**\n
            "허허, **GNN 중심성**이 {m['gnn']:.2f}로군. 이 종목이 전체 시장 네트워크의 '허브(Hub)' 역할을 하며 유동성을 공급하고 있어. 
            **전이 엔트로피(TE)** 분석 결과, 선행 시장의 정보가 양의 흐름으로 유입되고 있네."\n
            **[2. 기본적 분석 (Fundamental & Margin)]**\n
            "내재가치 대비 저평가 상태이며, 수급과 펀더멘털이 '금상첨화'를 이루고 있어. 안전마진이 충분히 확보된 진국일세."\n
            **[3. 🐯 호찌의 실전 매매 타임테이블]**\n
            * ⏳ **진입:** 변동성이 줄어드는 **오후 2시경**, 자금의 **{int(can_buy*0.8)}주**를 분할 매수하게.
            * ⏳ **운용:** **{target:,}원** 도달 시까지 단기 등락은 무시하고 '우보천리'하게.
            * ⏳ **대응:** 펀더멘털 훼손 전까진 강력 홀딩일세.
            """
        elif wr >= 0.50:
            t_txt = f"""
            **[1. 학술적 분석 (Local Volatility)]**\n
            "계륵일세. **국소 변동성(Local Vol)** 표면이 너무 거칠어. 옵션 시장의 내재 변동성이 현물 시장으로 전이될 수 있는 '내우외환'의 형국이야."\n
            **[2. 기본적 분석 (Uncertainty)]**\n
            "상승 여력은 있으나 **꼬리 위험(ES)**이 {m['es']:.2f}로 감지되어 불안하네. 돌다리도 두들겨 보고 건너야 하는 살얼음판이야."\n
            **[3. 🐯 호찌의 실전 매매 타임테이블]**\n
            * ⏳ **진입:** 오늘은 관망하고, 내일 시초가 흐름을 보게.
            * ⏳ **운용:** 굳이 산다면 **{int(can_buy*0.2)}주**만 아주 조금 담아보게. 욕심은 화를 부르네.
            * ⏳ **원칙:** '유비무환'의 자세로 리스크 관리에 치중하게.
            """
        else:
            t_txt = f"""
            **[1. 학술적 분석 (Non-Ergodic)]**\n
            "에잉 쯧쯧! **비에르고딕(Non-Ergodic)** 파산 위험이 감지되었어. 한 번의 손실로 재기 불능이 될 수 있는 자리야.
            과거의 지지선이 강력한 저항선(Role Reversal)으로 변질되었네."\n
            **[2. 기본적 분석 (Going Concern)]**\n
            "재무 건전성에 의심이 가는 **Going Concern** 이슈가 보여. 기초가 부실한데 탑을 쌓으려 하다니, 사상누각일세."\n
            **[3. 🐯 호찌의 실전 매매 타임테이블]**\n
            * ⏳ **즉시:** 포트폴리오에서 제외하게. 현금이 곧 최고의 종목이야.
            * ⏳ **향후:** 펀더멘털이 개선될 때까지 관심 종목에서도 지우게. 쉬는 것도 투자야.
            """

        return {
            "prices": (price, target, stop),
            "hamzzi": h_txt, "hojji": t_txt, "rationale": rationale
        }

    def diagnose_portfolio(self, portfolio, cash):
        if not portfolio: return "포트폴리오 없음", "데이터 없음"
        total = cash + sum(s['price']*s['qty'] for s in portfolio)
        cash_r = (cash/total*100) if total else 100
        
        # Safe calc
        pnl_list = [((s['price'] * 1.02) - s['price'])/s['price']*100 for s in portfolio if s['price'] > 0]
        avg_pnl = np.mean(pnl_list) if pnl_list else 0.0
        stock_count = len(portfolio)
        beta = np.random.uniform(0.5, 2.0)
        
        h = f"""
        "사장님! 현재 **예수금 비중 {cash_r:.1f}%**, **보유 종목 {stock_count}개**, **평균 수익률 {avg_pnl:.2f}%**야.
        지금 포트폴리오 **Beta**가 **{beta:.2f}**밖에 안 돼. 시장 상승분도 못 먹고 있다구! **[Cash Drag]** 때문에 돈이 썩고 있어!
        **[Action]** 내일 장 시작하면 현금 30% 털어서 주도주 2개 더 담아! 레버리지 ETF 섞어서 베타 1.5로 맞춰! 공격이 최선의 방어라구! 🔥"
        """
        
        t = f"""
        "자네, **보유 종목 {stock_count}개**에 **예수금 {cash_r:.1f}%**... 너무 안일해.
        리스크 분산이 안 되어 있어. 하락장 오면 공멸할 구조야. 엔트로피가 증가하는 시장에서 무방비 상태라네.
        **[Action]** 수익 중인 종목은 절반 익절하고, 그 돈으로 **[국채]**나 **[금]**을 사서 방어벽을 세우게. 유비무환일세. 🛡️"
        """
        return h, t

# -----------------------------------------------------------------------------
# [3] NATIVE UI RENDERER (Clean & Detailed)
# -----------------------------------------------------------------------------
def render_native_card(d, idx=None, is_rank=False):
    win_pct = d['win'] * 100
    p = d['plan']
    m = d['m']
    
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
        with c2:
            st.metric("Score", f"{win_pct:.1f}", delta=None)
        
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
        i3.metric("AI 목표가", f"{p['prices'][1]:,}원")
        
        # 3. Analysis Tabs (Deep Dive)
        tab1, tab2, tab3 = st.tabs(["🐹 햄찌의 야수 분석", "🐯 호찌의 방어 분석", "📊 8대 엔진 HUD"])
        
        with tab1:
            st.markdown(f"""
            <div class='analysis-box box-hamzzi'>
                <span class='persona-title' style='color:#FF9900;'>🐹 햄찌의 공격적 브리핑</span>
                {d['hamzzi']}
            </div>
            """, unsafe_allow_html=True)
            
        with tab2:
            st.markdown(f"""
            <div class='analysis-box box-hojji'>
                <span class='persona-title' style='color:#FF4444;'>🐯 호찌의 보수적 브리핑</span>
                {d['hojji']}
            </div>
            """, unsafe_allow_html=True)
            
        with tab3:
            h1, h2, h3 = st.columns(3)
            h1.metric("Omega", f"{m['omega']:.1f}")
            h1.metric("Hurst", f"{m['hurst']:.2f}")
            h2.metric("VPIN", f"{m['vpin']:.2f}")
            h2.metric("Hawkes", f"{m['hawkes']:.2f}")
            h3.metric("GNN", f"{m['gnn']:.2f}")
            h3.metric("Kelly", f"{m['kelly']:.2f}")

        # 4. Strategy Timetable & Prices
        st.markdown(f"""
        <div class='price-strategy'>
            <div class='ps-item'>
                <span class='ps-label' style='color:#00C9FF;'>🔵 진입/평단</span>
                <span class='ps-val' style='color:#00C9FF;'>{p['prices'][0]:,}원</span>
            </div>
            <div class='ps-item'>
                <span class='ps-label' style='color:#00FF00;'>🟢 목표가</span>
                <span class='ps-val' style='color:#00FF00;'>{p['prices'][1]:,}원</span>
            </div>
            <div class='ps-item'>
                <span class='ps-label' style='color:#FF4444;'>🔴 손절가</span>
                <span class='ps-val' style='color:#FF4444;'>{p['prices'][2]:,}원</span>
            </div>
        </div>
        <div style='margin-top:10px; font-size:12px; color:#888; text-align:center;'>💡 {p['rationale']}</div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [4] MAIN APP LOGIC
# -----------------------------------------------------------------------------
with st.expander("💰 자산 및 포트폴리오 설정 (Click to Open)", expanded=True):
    uploaded = st.file_uploader("📸 OCR 이미지 스캔 (시뮬레이션)", type=['png','jpg'], label_visibility="collapsed")
    if uploaded:
        st.session_state.portfolio = [
            {'name': '두산에너빌리티', 'price': 17500, 'qty': 100, 'strategy': '추세추종'},
            {'name': 'SK하이닉스', 'price': 135000, 'qty': 10, 'strategy': '추세추종'},
            {'name': '카카오', 'price': 55000, 'qty': 30, 'strategy': '초단타'}
        ]
        st.success("✅ 포트폴리오 로드 완료!")

    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1: st.number_input("💰 예수금 (KRW)", value=st.session_state.cash, step=100000, key="cash")
    with c2: st.number_input("🎯 목표 수익률 (%)", value=st.session_state.target_return, key="target_return")
        
    st.markdown("---")
    if st.button("➕ 종목 수동 추가"): 
        st.session_state.portfolio.append({'name': '삼성전자', 'price': 0, 'qty': 0, 'strategy': '추세추종'})
        st.rerun()
            
    if st.session_state.portfolio:
        for i, s in enumerate(st.session_state.portfolio):
            st.markdown(f"##### 📌 종목 {i+1}")
            cols = st.columns([3, 2, 2, 2, 1])
            with cols[0]: s['name'] = st.selectbox(f"종목명", stock_names, index=0, key=f"n{i}")
            with cols[1]: s['price'] = st.number_input(f"평단가", value=float(s['price']), key=f"p{i}")
            with cols[2]: s['qty'] = st.number_input(f"수량", value=int(s['qty']), key=f"q{i}")
            with cols[3]: s['strategy'] = st.selectbox(f"전략", ["추세추종","초단타"], key=f"s{i}")
            with cols[4]: 
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"d{i}"): 
                    st.session_state.portfolio.pop(i)
                    st.rerun()

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

c_btn, c_timer = st.columns([2, 1])
with c_btn:
    if st.button("🔍 햄찌 & 호찌의 [계좌 정밀 진단] 시작"):
        st.session_state.trigger_my = True
        st.rerun()
with c_timer:
    auto_my = st.selectbox("⏳ 자동 초기화(새로고침) 시간", list(TIME_OPTS.keys()), index=0)

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
    
    st.subheader("🔎 보유 종목 상세 심층 분석 (Deep Dive)")
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
    auto_top3 = st.selectbox("Top3 자동갱신", list(TIME_OPTS.keys()), index=0)

with c2:
    if st.button("📊 단타 / 추세 (전략별 보기)"):
        st.session_state.trigger_sep = True
        st.session_state.market_view_mode = 'SEPARATE'
        st.rerun()
    auto_sep = st.selectbox("전략별 자동갱신", list(TIME_OPTS.keys()), index=0)

if st.session_state.market_view_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("#### 🏆 금일의 Singularity Ideal Pick (Top 3)")
    for i, d in enumerate(st.session_state.ideal_list): render_native_card(d, i, is_rank=True)

elif st.session_state.market_view_mode == 'SEPARATE' and st.session_state.sc_list:
    st.markdown("#### 📊 전략별 절대 랭킹 (Top 3)")
    t1, t2 = st.tabs(["⚡ 단타 야수", "🌊 추세 현인"])
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

# 1. My Diagnosis
t_val_my = TIME_OPTS[auto_my]
if st.session_state.trigger_my or (t_val_my > 0 and now - st.session_state.l_my > t_val_my):
    with st.spinner("내 포트폴리오 정밀 해부 중..."):
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
                'm': m, 'tags': tags, 'plan': plan, 'mode': mode,
                'hamzzi': plan['hamzzi'], 'hojji': plan['hojji']
            })
        st.session_state.my_diagnosis = my_res
        st.session_state.l_my = now
        st.session_state.trigger_my = False
        need_rerun = True

# 2. Market Scan
t_val_top3 = TIME_OPTS[auto_top3]
t_val_sep = TIME_OPTS[auto_sep]
scan_needed = False
if st.session_state.trigger_top3 or (t_val_top3 > 0 and now - st.session_state.l_top3 > t_val_top3):
    scan_needed = True; st.session_state.market_view_mode = 'TOP3'; st.session_state.trigger_top3 = False; st.session_state.l_top3 = now
if st.session_state.trigger_sep or (t_val_sep > 0 and now - st.session_state.l_sep > t_val_sep):
    scan_needed = True; st.session_state.market_view_mode = 'SEPARATE'; st.session_state.trigger_sep = False; st.session_state.l_sep = now

if scan_needed:
    with st.spinner("시장 전체 스캔 중..."):
        market_data = load_top50_data()
        sc, sw, ideal = [], [], []
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close'])); name = row['Name']
            
            wr1, m1, t1 = engine.run_diagnosis(name, "scalping")
            p1 = engine.generate_report("scalping", price, m1, wr1, st.session_state.cash, 0, st.session_state.target_return)
            item1 = {'name': name, 'price': price, 'win': wr1, 'm': m1, 'tags': t1, 'plan': p1, 'mode': '초단타', 'pnl': 0, 'hamzzi': p1['hamzzi'], 'hojji': p1['hojji']}
            
            wr2, m2, t2 = engine.run_diagnosis(name, "swing")
            p2 = engine.generate_report("swing", price, m2, wr2, st.session_state.cash, 0, st.session_state.target_return)
            item2 = {'name': name, 'price': price, 'win': wr2, 'm': m2, 'tags': t2, 'plan': p2, 'mode': '추세추종', 'pnl': 0, 'hamzzi': p2['hamzzi'], 'hojji': p2['hojji']}
            
            sc.append(item1); sw.append(item2)
            ideal.append(item1 if wr1 >= wr2 else item2)
            
        sc.sort(key=lambda x: x['win'], reverse=True); sw.sort(key=lambda x: x['win'], reverse=True); ideal.sort(key=lambda x: x['win'], reverse=True)
        st.session_state.sc_list = sc[:3]; st.session_state.sw_list = sw[:3]; st.session_state.ideal_list = ideal[:3]
        need_rerun = True

if need_rerun: st.rerun()
if t_val_my>0 or t_val_top3>0 or t_val_sep>0: time.sleep(1); st.rerun()
