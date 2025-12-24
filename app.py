import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random
import textwrap

# -----------------------------------------------------------------------------
# [0] SYSTEM CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Hojji & Hamzzi Quant", page_icon="🐯", layout="centered")

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
# 요청하신 원래 시간 목록
TIME_OPTS = {"⛔ 수동 (멈춤)": 0, "⏱️ 3분마다": 180, "⏱️ 10분마다": 600, "⏱️ 30분마다": 1800}

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
# [1] STYLING (Neon Gold & Cute)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #ffffff; font-family: 'Pretendard', sans-serif; }
    
    /* Neon Gold Buttons */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 55px; font-size: 18px;
        background-color: #111; 
        border: 2px solid #d4af37; color: #d4af37; 
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color: #d4af37; color: #000; 
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.8); border-color: #fff;
    }
    
    /* Input Labels */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-size: 15px !important; font-weight: 900 !important; color: #FFD700 !important;
        margin-bottom: 5px !important;
    }
    
    /* Card UI */
    .stock-card { 
        background: #111; border: 1px solid #333; border-radius: 16px; 
        padding: 0; margin-bottom: 30px; box-shadow: 0 8px 30px rgba(0,0,0,0.8); overflow: hidden;
    }
    
    /* Analysis Box */
    .analysis-box {
        background-color: #0f0f0f; border-radius: 10px; padding: 25px; margin-top: 15px; 
        line-height: 1.8; color: #eee; border: 1px solid #333;
        border-left-width: 5px; border-left-style: solid;
    }
    .box-hamzzi { border-left-color: #FF9900; }
    .box-hojji { border-left-color: #FF4444; }
    
    .persona-title { font-size: 17px; font-weight: 900; margin-bottom: 12px; display: block; border-bottom: 1px dashed #444; padding-bottom: 8px; }
    
    /* Timetable */
    .timetable {
        background: #1a1a1a; padding: 15px; border-radius: 8px; border-left: 3px solid #00C9FF; margin-top: 15px;
        font-size: 14px;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] { font-size: 24px !important; color: #fff !important; font-weight: 800 !important; }
    
    /* Tags */
    .tag { display: inline-block; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-right: 5px; color: #000; }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -15px !important; margin-top: 23px; }
</style>
""", unsafe_allow_html=True)

# [TITLE RESTORED]
st.markdown("<h1 style='text-align: center; color: #FFD700;'>🐯 햄찌와 호찌의 퀀트 대작전 🚀</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [2] SINGULARITY OMEGA ENGINE (Infinite Persona Logic)
# -----------------------------------------------------------------------------
class SingularityEngine:
    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H-%M-%S')}-{random.randint(0,1000)}"
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

    # 🐹 햄찌: 메스가끼 + 공격적
    def _get_hamzzi_msg(self, wr, m, can_buy, target, price):
        intros = [
            "흐~접♡ 아직도 안 샀어?", "어머? 이 차트를 보고도 가만히 있어?", 
            "야, 쫄보야! 눈 떠!", "오빠, 바보야? 돈 복사기인데?", 
            "메롱~ 나만 부자될 거야!", "멍청하게 쳐다만 볼 거야?"
        ]
        
        logic_good = [
            f"**Hawkes 강도** {m['hawkes']:.2f} 뚫었잖아! 기계들이 미친 듯이 사는데 넌 뭐해?",
            f"**Omega** {m['omega']:.1f}Hz로 폭발 직전이라구! 우주 끝까지 간다니까?",
            f"**GNN** {m['gnn']:.2f}로 시장 돈 다 빨아들이는 중! 블랙홀이야 블랙홀!"
        ]
        
        action_buy = [
            f"잔말 말고 **시장가**로 **{can_buy}주** 긁어! 늦으면 네 손해야♡",
            f"지금 당장 **{can_buy}주** 풀매수해! **{target:,}원** 가면 칭찬해줄게!",
            f"인생 역전 하고 싶지 않아? 눈 딱 감고 질러! 불타기 가즈아!"
        ]
        
        logic_bad = [
            f"으악! **VPIN** {m['vpin']:.2f}야! 설거지 당하고 싶어? 바보야?",
            f"**Betti Number** 1 떴어. 구멍 숭숭 뚫린 차트라구. 지지선? 그딴 거 없어.",
            f"**Tail Risk** {m['es']:.2f} 실화냐? 한방에 깡통 차고 싶어?"
        ]
        
        action_sell = [
            "당장 갖다 버려! 꼴도 보기 싫어! 돔황챠!!",
            "들고 있으면 바보 인증이야. 전량 매도해! 지금 당장!",
            "절대 사지 마. 내 말 안 들으면 평생 후회한다?"
        ]

        if wr >= 0.70:
            return f"""
            **[🐹 햄찌의 도발 & 분석]**\n
            "{random.choice(intros)} {random.choice(logic_good)} 완전 슈퍼 떡상각이라구!"\n
            **[⏰ 햄찌의 타임테이블]**\n
            * 09:00: 갭상승 2% 이내면 **시장가 풀매수**!\n* 09:30: 눌리면 **불타기**로 물량 2배!\n* 14:00: **{target:,}원** 뚫으면 홀딩!\n
            **👉 {random.choice(action_buy)}**
            """
        elif wr >= 0.50:
            return f"""
            **[🐹 햄찌의 단타 훈수]**\n
            "흥, **Hurst** {m['hurst']:.2f}라 추세는 있는데 **OBI**가 구려. 세력들이 간 보네? 단타로나 먹고 빠져."\n
            **[⏰ 햄찌의 타임테이블]**\n
            * 09:00: 관망해. 들어가면 물린다.\n* 10:30: **{price:,}원** 지지하면 **{int(can_buy/3)}주**만 사.\n* 13:00: 슈팅 나오면 바로 튀어!\n
            **👉 욕심 부리지 마♡ 짧게 먹고 튀는 거야.**
            """
        else:
            return f"""
            **[🐹 햄찌의 경멸]**\n
            "{random.choice(logic_bad)} {random.choice(logic_bad)} 이딴 걸 주식이라고 보고 있어?"\n
            **[⏰ 햄찌의 타임테이블]**\n
            * 지금 당장: **시장가 투매!** 뒤도 돌아보지 마.\n* 장중 내내: HTS 꺼. 쳐다도 보지 마.\n
            **👉 {random.choice(action_sell)}**
            """

    # 🐯 호찌: 꼰대 + 사자성어 + 방어적
    def _get_hojji_msg(self, wr, m, can_buy, target, price):
        idioms_good = ["금상첨화(錦上添花)", "낭중지추(囊中之錐)", "파죽지세(破竹之勢)", "일취월장(日就月將)"]
        idioms_bad = ["사상누각(砂上樓閣)", "내우외환(內憂外患)", "풍전등화(風前燈火)", "설상가상(雪上加霜)"]
        
        intros = [
            "에헴! 요즘 젊은 것들은 차트만 보고 설치지.", "라떼는 말이야, 재무제표 안 보고 사면 뺨을 맞았어.", 
            "허허, 자네. 투자는 도박이 아닐세.", "쯧쯧, 급할수록 돌아가라 했거늘."
        ]
        
        logic_good = [
            f"**GNN 중심성** {m['gnn']:.2f}를 보게. 진정한 대장주야. 근본이 있어.",
            f"**전이 엔트로피** 흐름이 양호해. 실적과 수급의 조화가 {random.choice(idioms_good)}로세.",
            f"**JLS 모델**상 거품 붕괴 위험이 없어. 탄탄대로야."
        ]
        
        action_buy = [
            f"안전마진이 확보되었으니 **{int(can_buy*0.8)}주** 정도 진입하게.",
            f"오후 장에 **{int(can_buy*0.8)}주**를 분할로 매수하여 평단을 맞추게.",
            f"**{target:,}원**까지는 '우보천리'의 마음으로 진득하게 가져가게나."
        ]
        
        logic_bad = [
            f"**내재 변동성** {m['vol_surf']:.2f} 좀 보게. {random.choice(idioms_bad)}이 따로 없네.",
            f"**Going Concern** 이슈가 있어. 기초가 부실한 {random.choice(idioms_bad)}일세.",
            f"과거 지지선이 저항선으로 변했어. 뚫기 힘들 거야."
        ]
        
        action_sell = [
            "욕심은 화를 부르네. 관망하는 게 상책이야.",
            "**비에르고딕** 파산 위험을 피하게. 쉬는 것도 투자네.",
            "포트폴리오에서 지우게. 현금이 최고의 종목이야."
        ]

        if wr >= 0.70:
            return f"""
            **[🐯 호찌의 훈장님 말씀]**\n
            "{random.choice(intros)} **{random.choice(idioms_good)}**! {random.choice(logic_good)}"\n
            **[⏳ 호찌의 시계열 지침]**\n
            * 진입: 변동성 줄어드는 14시경.\n* 운용: 흔들려도 펀더멘털 믿고 홀딩.\n* 목표: **{target:,}원** 도달 시 분할 매도.\n
            **👉 {random.choice(action_buy)}**
            """
        elif wr >= 0.50:
            return f"""
            **[🐯 호찌의 우려]**\n
            "계륵일세. **꼬리 위험(ES)**이 {m['es']:.2f}로 감지돼. 돌다리도 두들겨 보고 건너야지. 쯧쯧."\n
            **[⏳ 호찌의 시계열 지침]**\n
            * 진입: 오늘은 관망. 내일 시초가 확인.\n* 운용: 정 사고 싶다면 **{int(can_buy*0.2)}주**만.\n
            **👉 유비무환(有備無患)일세. 리스크 관리에 치중하게.**
            """
        else:
            return f"""
            **[🐯 호찌의 불호령]**\n
            "어허! **{random.choice(idioms_bad)}**! {random.choice(logic_bad)} 어디서 이런 걸 가져왔나!"\n
            **[⏳ 호찌의 시계열 지침]**\n
            * 즉시: 관심 종목 삭제.\n* 향후: 쳐다도 보지 말게.\n
            **👉 {random.choice(action_sell)}**
            """

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        volatility = m['vol_surf'] * 0.05
        if mode == "scalping":
            target = int(price * (1 + max(volatility, 0.02)))
            stop = int(price * (1 - volatility * 0.6))
            rationale = f"스캘핑: Vol {m['vol_surf']:.2f} 기반 1.5σ 상단 목표"
        else:
            target = int(price * (1 + (target_return/100)))
            stop = int(price * 0.93)
            rationale = f"스윙: 목표 {target_return}% 및 Hurst 추세 반영"
        
        safe_kelly = m['kelly'] * 0.5 
        can_buy = int((cash * safe_kelly) / price) if price > 0 else 0

        h_txt = self._get_hamzzi_msg(wr, m, can_buy, target, price)
        t_txt = self._get_hojji_msg(wr, m, can_buy, target, price)

        return {
            "prices": (price, target, stop),
            "hamzzi": h_txt, "hojji": t_txt, "rationale": rationale
        }

    def diagnose_portfolio(self, portfolio, cash):
        if not portfolio: return "포트폴리오 없음", "데이터 없음"
        total = cash + sum(s['price']*s['qty'] for s in portfolio)
        cash_r = (cash/total*100) if total else 100
        pnl_list = [((s['price'] * 1.02) - s['price'])/s['price']*100 for s in portfolio if s['price'] > 0]
        avg_pnl = np.mean(pnl_list) if pnl_list else 0.0
        stock_count = len(portfolio)
        beta = np.random.uniform(0.5, 2.0)
        
        # Hamzzi Portfolio Logic
        h_msgs = [
            f"사장님! 현금 **{cash_r:.1f}%** 실화야? 쫄보야? **Beta {beta:.2f}**로 언제 부자 될래? 허접~♡ 당장 **레버리지** 태워!",
            f"보유 종목이 **{stock_count}개**? 백화점 차렸어? 다 정리하고 **주도주** 하나에 몰빵해! 인생 한방이라구!",
            f"수익률 **{avg_pnl:.2f}%**... 귀엽네? 나였으면 벌써 2배 불렸다. 내일 시초가에 **TQQQ** 풀매수 가즈아!"
        ]
        
        # Hojji Portfolio Logic
        t_msgs = [
            f"자네, 현금 비중이 **{cash_r:.1f}%**라니... **유비무환(有備無患)**을 모르는가? 하락장 오면 패가망신하네.",
            f"종목 수가 **{stock_count}개**... 너무 방만해. **과유불급(過猶不及)**이야. 똘똘한 놈 남기고 정리하고 **국채**를 사게.",
            f"수익률에 취해있군. **호사다마(好事多魔)**라 했어. 지금 절반 익절하고 **금(Gold)**을 사서 방어벽을 세우게."
        ]
        
        return random.choice(h_msgs), random.choice(t_msgs)

# -----------------------------------------------------------------------------
# [3] NATIVE UI RENDERER
# -----------------------------------------------------------------------------
def render_native_card(d, idx=None, is_rank=False):
    win_pct = d['win'] * 100
    p = d['plan']
    m = d['m']
    
    with st.container(border=True):
        # Header
        c1, c2 = st.columns([3, 1])
        with c1:
            prefix = f"🏆 {idx+1}위 " if is_rank else ""
            st.markdown(f"### {prefix}{d['name']} <span style='font-size:14px; color:#aaa;'>({d['mode']})</span>", unsafe_allow_html=True)
        with c2:
            st.metric("Score", f"{win_pct:.1f}", delta=None)
        
        st.progress(int(win_pct))
        
        # Tags
        tcols = st.columns(len(d['tags']))
        for i, tag in enumerate(d['tags']):
            tcols[i].caption(f"🏷️ {tag['label']}")
            
        st.divider()
        
        # Info
        i1, i2, i3 = st.columns(3)
        pnl = d['pnl']
        i1.metric("현재가", f"{d['price']:,}원")
        i2.metric("수익률", f"{pnl:.2f}%", delta=f"{pnl:.2f}%")
        i3.metric("AI 목표가", f"{p['prices'][1]:,}원")
        
        st.markdown(f"""
        <div class='price-strategy'>
            <div class='ps-item'><span class='ps-label' style='color:#00C9FF;'>🔵 진입/평단</span><span class='ps-val' style='color:#00C9FF;'>{p['prices'][0]:,}원</span></div>
            <div class='ps-item'><span class='ps-label' style='color:#00FF00;'>🟢 목표가</span><span class='ps-val' style='color:#00FF00;'>{p['prices'][1]:,}원</span></div>
            <div class='ps-item'><span class='ps-label' style='color:#FF4444;'>🔴 손절가</span><span class='ps-val' style='color:#FF4444;'>{p['prices'][2]:,}원</span></div>
        </div>
        <div style='margin-top:10px; font-size:12px; color:#888; text-align:center;'>💡 {p['rationale']}</div>
        """, unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["🐹 햄찌의 잔소리", "🐯 호찌의 훈계", "📊 8대 엔진"])
        
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
# [4] MAIN APP
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
    if st.button("📊 햄찌와 호찌의 계좌 참견 시점 (진단 시작)"):
        st.session_state.trigger_my = True
        st.rerun()
with c_timer:
    auto_my = st.selectbox("⏳ 자동 초기화(새로고침) 시간", list(TIME_OPTS.keys()), index=0)

# [5] RESULT RENDERING
if st.session_state.my_diagnosis:
    st.markdown("---")
    if st.session_state.port_analysis:
        h_port, t_port = st.session_state.port_analysis
        st.subheader("📊 햄찌와 호찌의 계좌 참견 (종합 진단)")
        
        st.markdown(f"""
        <div class='analysis-box box-hamzzi'>
            <span class='persona-title' style='color:#FF9900;'>🐹 햄찌의 잔소리 폭격</span>
            {h_port}
        </div>
        <div style='height:10px'></div>
        <div class='analysis-box box-hojji'>
            <span class='persona-title' style='color:#FF4444;'>🐯 호찌의 서당 훈계</span>
            {t_port}
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("🔎 이 종목 어때? (보유 종목 상세 분석)")
    for d in st.session_state.my_diagnosis:
        render_native_card(d, is_rank=False)

st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)
st.markdown("### 📡 햄찌의 꿀통 발견 (시장 스캔)")

c1, c2 = st.columns(2)
with c1:
    if st.button("🏆 명예의 전당 (Top 3)"):
        st.session_state.trigger_top3 = True
        st.session_state.market_view_mode = 'TOP3'
        st.rerun()
    auto_top3 = st.selectbox("Top3 자동갱신", list(TIME_OPTS.keys()), index=0)

with c2:
    if st.button("⚡ 단타 야수 vs 🌊 묵직 꼰대 (전략별)"):
        st.session_state.trigger_sep = True
        st.session_state.market_view_mode = 'SEPARATE'
        st.rerun()
    auto_sep = st.selectbox("전략별 자동갱신", list(TIME_OPTS.keys()), index=0)

if st.session_state.market_view_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("#### 🏆 햄찌 & 호찌의 강력 추천 (Top 3)")
    for i, d in enumerate(st.session_state.ideal_list): render_native_card(d, i, is_rank=True)

elif st.session_state.market_view_mode == 'SEPARATE' and st.session_state.sc_list:
    st.markdown("#### 📊 전략별 절대 랭킹 (Top 3)")
    t1, t2 = st.tabs(["⚡ 햄찌의 단타 픽", "🌊 호찌의 스윙 픽"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_native_card(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_native_card(d, i, is_rank=True)

# [6] LOGIC LOOP
engine = SingularityEngine()
now = time.time()
need_rerun = False

# My Diagnosis
t_val_my = TIME_OPTS[auto_my]
if st.session_state.trigger_my or (t_val_my > 0 and now - st.session_state.l_my > t_val_my):
    with st.spinner("햄찌가 차트 긋는 중... 호찌가 재무제표 보는 중..."):
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

# Market Scan
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
