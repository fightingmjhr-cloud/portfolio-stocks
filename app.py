import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random
import textwrap

# -----------------------------------------------------------------------------
# [0] SYSTEM CONFIG & SAFETY INIT
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
# [1] STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Background */
    .stApp { background-color: #050505; color: #ffffff; font-family: 'Pretendard', sans-serif; }
    
    /* Buttons */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 50px; font-size: 16px;
        background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%); 
        border: none; color: #000; 
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.3); transition: 0.3s;
    }
    .stButton>button:hover { 
        transform: scale(1.02); box-shadow: 0 0 20px rgba(0, 201, 255, 0.6);
    }
    
    /* Input Labels */
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
    
    /* Analysis Box */
    .analysis-box {
        background-color: #0a0a0a; border-radius: 8px; padding: 20px; margin-top: 15px; 
        line-height: 1.8; color: #eee; border: 1px solid #333;
        border-left-width: 5px; border-left-style: solid;
    }
    .box-hamzzi { border-left-color: #FF9900; }
    .box-hojji { border-left-color: #FF4444; }
    
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
# [2] SINGULARITY OMEGA ENGINE (Infinite Variety Logic)
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

    def _generate_hamzzi_text(self, wr, m, can_buy, target):
        # 🐹 햄찌의 다양한 말투 패턴 생성기
        intros = [
            "사장님! 대박 사건이야!", "오마이갓! 이 차트 봤어?", "야수의 심장이 뛴다!", 
            "지금 아니면 버스 떠나!", "이건 우주가 보내는 신호야!", "돈 냄새가 진동을 한다!"
        ]
        
        logic_good = [
            f"**Hawkes 강도**가 {m['hawkes']:.2f}를 뚫었어! 기계들이 미친 듯이 매수 버튼 누르는 중이라구!",
            f"**Omega 진동수** {m['omega']:.1f}Hz로 임계 폭발 직전이야! 터지기 일보 직전!",
            f"**GNN 중심성** {m['gnn']:.2f}로 시장 돈이 다 여기로 빨려 들어가고 있어!",
            f"**Vol Surface**가 우상향하고 있어. 콜옵션 쪽에서 난리가 났다구!"
        ]
        
        actions_buy = [
            f"고민은 배송만 늦출 뿐! **시장가**로 **{can_buy}주** 긁어!",
            f"쫄지마! 인생 역전 기회야. **{can_buy}주** 풀매수 가즈아!",
            f"지금 당장 탑승해! **{target:,}원** 뚫으면 불타기로 2배 더 실어!"
        ]
        
        logic_bad = [
            f"으악! **VPIN**이 {m['vpin']:.2f}야! 기관 형님들이 설거지 중이라구!",
            f"**Betti Number**가 1로 변했어. 차트에 구멍 뚫려서 지옥문 열렸어!",
            f"**Tail Risk**가 너무 커. 한방에 계좌 녹을 수 있어!"
        ]
        
        actions_sell = [
            "뒤도 돌아보지 말고 튀어! 돔황챠!! 🏃‍♂️",
            "이건 투자가 아니라 기부야. 당장 전량 매도해!",
            "현금 꽉 쥐고 숨어있어. 소나기는 피해야 해."
        ]

        if wr >= 0.70:
            return f"""
            **[🐹 햄찌의 긴급 타전]**\n
            "{random.choice(intros)} {random.choice(logic_good)} 
            완전 **슈퍼 모멘텀** 구간이야. {random.choice(logic_good)}"\n
            **👉 [행동 지침]**\n{random.choice(actions_buy)}
            """
        elif wr >= 0.50:
            return f"""
            **[🐹 햄찌의 단타 교실]**\n
            "음~ **Hurst**가 {m['hurst']:.2f}로 추세가 살아있긴 한데, **OBI**가 {m['obi']:.2f}로 애매해.
            세력들이 간 보고 있는 중이야. 단타 치기엔 좋은 놀이터지."\n
            **👉 [행동 지침]**\n몰빵은 금지! **{int(can_buy/3)}주**만 정찰병으로 보내고, 반응 오면 그때 태워!
            """
        else:
            return f"""
            **[🐹 햄찌의 경고 경보]**\n
            "{random.choice(logic_bad)} {random.choice(logic_bad)}
            지금 들어가면 진짜 큰일 나!"\n
            **👉 [행동 지침]**\n{random.choice(actions_sell)}
            """

    def _generate_hojji_text(self, wr, m, can_buy, target):
        # 🐯 호찌의 다양한 말투 패턴 생성기
        intros = [
            "허허, 차트를 보게나.", "음, 펀더멘털을 살펴볼까.", "자네, 너무 흥분하지 말게.", 
            "투자의 정석대로 가야 하네.", "데이터는 거짓말을 하지 않지."
        ]
        
        logic_good = [
            f"**GNN 중심성**이 {m['gnn']:.2f}로 진정한 주도주임이 증명되었네.",
            f"**전이 엔트로피(TE)**가 양의 흐름을 보이고 있어. 수급과 실적의 조화가 훌륭해.",
            f"**JLS 모델**상 버블 붕괴 위험 없이 상승 여력이 충분해.",
            f"내재가치 대비 저평가 상태이며, 안전마진이 확보된 자리일세."
        ]
        
        actions_buy = [
            f"자네 자금의 **{int(can_buy*0.8)}주** 정도를 진입하게. 우직하게 동행해도 좋네.",
            f"변동성이 줄어드는 오후 장에 **{int(can_buy*0.8)}주**를 분할로 매수하게.",
            f"**{target:,}원**까지는 흔들려도 '우보천리'의 마음으로 가져가게나."
        ]
        
        logic_bad = [
            f"계륵일세. **내재 변동성**이 {m['vol_surf']:.2f}로 너무 높아. '내우외환'의 형국이야.",
            f"**Going Concern** 이슈가 보여. 재무 건전성이 의심되는 사상누각일세.",
            f"과거의 지지선이 강력한 저항선(Role Reversal)으로 변질되었어."
        ]
        
        actions_sell = [
            "욕심은 화를 부르네. 관망하는 것이 '만수무강'의 길이야.",
            "쳐다도 보지 말게. **비에르고딕** 파산 위험을 피하는 게 상책일세.",
            "포트폴리오에서 제외하게. 현금이 곧 최고의 종목이야."
        ]

        if wr >= 0.70:
            return f"""
            **[🐯 호찌의 가치 분석]**\n
            "{random.choice(intros)} {random.choice(logic_good)} 
            {random.choice(logic_good)}"\n
            **👉 [행동 지침]**\n{random.choice(actions_buy)}
            """
        elif wr >= 0.50:
            return f"""
            **[🐯 호찌의 신중론]**\n
            "계륵일세. 상승 여력은 있으나 **꼬리 위험(ES)**이 {m['es']:.2f}로 감지되어 불안하네.
            돌다리도 두들겨 보고 건너야 하는 살얼음판이야."\n
            **👉 [행동 지침]**\n굳이 산다면 **{int(can_buy*0.2)}주**만 아주 조금 담아보게. 리스크 관리가 최우선일세.
            """
        else:
            return f"""
            **[🐯 호찌의 호통]**\n
            "{random.choice(logic_bad)} {random.choice(logic_bad)} 
            기초가 부실한데 탑을 쌓으려 하다니!"\n
            **👉 [행동 지침]**\n{random.choice(actions_sell)}
            """

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        volatility = m['vol_surf'] * 0.05
        if mode == "scalping":
            target = int(price * (1 + max(volatility, 0.02)))
            stop = int(price * (1 - volatility * 0.6))
            rationale = f"스캘핑 기준: 변동성(Vol) {m['vol_surf']:.2f} 기반 목표/손절 산출"
        else:
            target = int(price * (1 + (target_return/100)))
            stop = int(price * 0.93)
            rationale = f"스윙 기준: 목표수익률 {target_return}% 및 Hurst 추세 강도 반영"
        
        safe_kelly = m['kelly'] * 0.5 
        can_buy = int((cash * safe_kelly) / price) if price > 0 else 0

        h_txt = self._generate_hamzzi_text(wr, m, can_buy, target)
        t_txt = self._generate_hojji_text(wr, m, can_buy, target)

        return {
            "prices": (price, target, stop),
            "hamzzi": h_txt, "hojji": t_txt, "rationale": rationale
        }

    def diagnose_portfolio(self, portfolio, cash):
        if not portfolio: return "포트폴리오 없음", "데이터 없음"
        total = cash + sum(s['price']*s['qty'] for s in portfolio)
        cash_r = (cash/total*100) if total else 100
        
        # [FIX] ZeroDivisionError 방지
        pnl_list = [((s['price'] * 1.02) - s['price'])/s['price']*100 for s in portfolio if s['price'] > 0]
        avg_pnl = np.mean(pnl_list) if pnl_list else 0.0
        stock_count = len(portfolio)
        beta = np.random.uniform(0.5, 2.0)
        
        # Hamzzi Variety
        h_msgs = [
            f"사장님! 현금 비중이 **{cash_r:.1f}%**야. **[Cash Drag]** 때문에 돈이 썩고 있어! **Beta {beta:.2f}**로는 시장 못 이겨!",
            f"아니 수익률이 **{avg_pnl:.2f}%**가 뭐야? 장난해? 지금 당장 **레버리지** 태워서 복구해야지!",
            f"종목이 **{stock_count}개**? 다이소 차렸어? **주도주**에 집중 투자해서 인생 역전 가야지!"
        ]
        
        # Hojji Variety
        t_msgs = [
            f"자네, **보유 종목 {stock_count}개**에 **예수금 {cash_r:.1f}%**... 너무 안일해. 하락장 오면 공멸할 구조야.",
            f"리스크 관리가 엉망이군. **MDD**가 너무 깊어질 수 있어. **[국채]**나 **[금]**을 편입해서 방어벽을 세우게.",
            f"변동성이 큰 장세일세. '유비무환'의 자세로 수익 줄 때 챙기고 현금 비중을 늘리게."
        ]
        
        return random.choice(h_msgs), random.choice(t_msgs)

# -----------------------------------------------------------------------------
# [3] NATIVE UI RENDERER
# -----------------------------------------------------------------------------
def render_native_card(d, idx=None, is_rank=False):
    win_pct = d['win'] * 100
    p = d['plan']
    m = d['m']
    
    if d['win'] >= 0.7: score_color = "green"
    elif d['win'] >= 0.5: score_color = "orange"
    else: score_color = "red"

    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            prefix = f"🏆 {idx+1}위 " if is_rank else ""
            st.markdown(f"### {prefix}{d['name']} <span style='font-size:14px; color:#aaa;'>({d['mode']})</span>", unsafe_allow_html=True)
        with c2:
            st.metric("Score", f"{win_pct:.1f}", delta=None)
        
        st.progress(int(win_pct))
        
        tcols = st.columns(len(d['tags']))
        for i, tag in enumerate(d['tags']):
            tcols[i].caption(f"🏷️ {tag['label']}")
            
        st.divider()
        
        i1, i2, i3 = st.columns(3)
        pnl = d['pnl']
        i1.metric("현재가", f"{d['price']:,}원")
        i2.metric("수익률", f"{pnl:.2f}%", delta=f"{pnl:.2f}%")
        i3.metric("목표가", f"{p['prices'][1]:,}원")
        
        st.markdown(f"""
        <div class='price-strategy'>
            <div class='ps-item'><span class='ps-label' style='color:#00C9FF;'>🔵 진입/평단</span><span class='ps-val' style='color:#00C9FF;'>{p['prices'][0]:,}원</span></div>
            <div class='ps-item'><span class='ps-label' style='color:#00FF00;'>🟢 목표가</span><span class='ps-val' style='color:#00FF00;'>{p['prices'][1]:,}원</span></div>
            <div class='ps-item'><span class='ps-label' style='color:#FF4444;'>🔴 손절가</span><span class='ps-val' style='color:#FF4444;'>{p['prices'][2]:,}원</span></div>
        </div>
        <div style='margin-top:10px; font-size:12px; color:#888; text-align:center;'>💡 {p['rationale']}</div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🐹 햄찌 분석", "🐯 호찌 분석", "📊 8대 엔진"])
        
        with tab1:
            st.markdown(f"<div class='analysis-box box-hamzzi'>{d['hamzzi']}</div>", unsafe_allow_html=True)
        with tab2:
            st.markdown(f"<div class='analysis-box box-hojji'>{d['hojji']}</div>", unsafe_allow_html=True)
        with tab3:
            h1, h2, h3 = st.columns(3)
            h1.metric("Omega", f"{m['omega']:.1f}")
            h1.metric("Hurst", f"{m['hurst']:.2f}")
            h2.metric("VPIN", f"{m['vpin']:.2f}")
            h2.metric("Hawkes", f"{m['hawkes']:.2f}")
            h3.metric("GNN", f"{m['gnn']:.2f}")
            h3.metric("Kelly", f"{m['kelly']:.2f}")

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
                st.markdown(f"<div class='analysis-box box-hamzzi'>{h_port}</div>", unsafe_allow_html=True)
            with c2: 
                st.markdown(f"### 🐯 호찌 (Conservative)")
                st.markdown(f"<div class='analysis-box box-hojji'>{t_port}</div>", unsafe_allow_html=True)
    
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
