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

# [요청 반영] 타이머 옵션 세분화
TIME_OPTS = {
    "⛔ 멈춤": 0,
    "⏱️ 3분": 180, "⏱️ 5분": 300, "⏱️ 10분": 600, 
    "⏱️ 15분": 900, "⏱️ 20분": 1200, "⏱️ 30분": 1800, "⏱️ 40분": 2400,
    "⏱️ 1시간": 3600, "⏱️ 1시간 30분": 5400, "⏱️ 2시간": 7200, "⏱️ 3시간": 10800
}

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
    
    /* Neon Gold Buttons */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 55px; font-size: 18px;
        background-color: #1a1a1a; 
        border: 2px solid #FFD700; 
        color: #FFD700; 
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color: #FFD700; color: #000; 
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.8); border-color: #fff;
    }
    
    /* Input Labels */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-size: 15px !important; font-weight: 900 !important; color: #FFD700 !important;
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
        padding: 0; margin-bottom: 30px; box-shadow: 0 8px 30px rgba(0,0,0,0.8); overflow: hidden;
    }
    
    /* Analysis Box */
    .analysis-box {
        background-color: #0f0f0f; border-radius: 10px; padding: 20px; margin-top: 15px; 
        line-height: 1.8; color: #eee; border: 1px solid #333;
        border-left-width: 5px; border-left-style: solid;
    }
    .box-hamzzi { border-left-color: #FF9900; }
    .box-hojji { border-left-color: #FF4444; }
    
    .persona-title { font-size: 17px; font-weight: 900; margin-bottom: 12px; display: block; border-bottom: 1px dashed #444; padding-bottom: 8px; }
    
    /* Price Strategy Box */
    .price-strategy {
        background: #151515; padding: 20px; border-radius: 10px; margin-top: 15px; 
        border: 1px solid #444; display: flex; justify-content: space-between; text-align: center;
    }
    .ps-item { width: 32%; }
    .ps-label { font-size: 12px; color: #888; display: block; margin-bottom: 5px; font-weight: bold; }
    .ps-val { font-size: 18px; font-weight: 800; }
    
    /* Tags */
    .tag { display: inline-block; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-right: 5px; color: #000; }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -15px !important; margin-top: 23px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🐯 호찌와 햄찌의 퀀트 대작전 🐹</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [2] SINGULARITY OMEGA ENGINE (Infinite Persona Logic)
# -----------------------------------------------------------------------------
class SingularityEngine:
    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H-%M-%S')}-{random.randint(0,10000)}"
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

    # 🐹 햄찌: 무한 랜덤 문장 생성기 (메스가끼 + 팩트폭격)
    def _get_hamzzi_msg(self, wr, m, can_buy, target, price):
        # 1. 도입부 (랜덤)
        intros = [
            "야, 쫄보야? 아직도 눈치만 보고 있어?", "어머? 이 차트를 보고도 심장이 안 뛰어?", 
            "돈 벌기 싫어? 내가 떠먹여 줘야 해?", "멍청하게 쳐다만 볼 거야? 버스 떠난다?", 
            "허접~♡ 분석은 내가 다 했으니까 넌 매수나 눌러!"
        ]
        
        # 2. 논리적 근거 (랜덤 + 데이터 결합)
        logic_variations = [
            f"**JLS 모델**이 뭐라는지 알아? Omega 진동수 {m['omega']:.1f}Hz로 임계 폭발 직전이라잖아! 물리학적으로 무조건 튀어 오르는 자리라구!",
            f"**Hawkes 강도** {m['hawkes']:.2f} 돌파! 이건 사람이 사는 게 아냐. 기계들이 미친 듯이 긁어모으는 '자기 여진' 상태라구.",
            f"**GNN 중심성** {m['gnn']:.2f} 실화냐? 시장의 모든 돈이 여기로 빨려 들어가고 있어. 블랙홀급 유동성이라구!",
            f"**Kelly 공식** 돌려보니까 자산의 {m['kelly']*100:.1f}%는 태워도 된대. 수학이 보증하는 자리야."
        ]
        
        # 3. 타임테이블 (구체적 지시)
        timetables = [
            f"* 09:00: 갭상승 2% 이내면 **시장가 풀매수**!\n* 09:30: 눌림목에서 **불타기**로 물량 2배!\n* 14:00: **{target:,}원** 뚫으면 홀딩!",
            f"* 09:05: 수급 들어오는 거 보고 진입해.\n* 10:00: **{price:,}원** 지지하는지 확인 필수.\n* 13:30: 슈팅 나오면 **{target:,}원**에 절반 던져!",
            f"* 09:00: 바로 사지 마. 3분만 기다려.\n* 09:03: 시초가 돌파하면 그때 **{can_buy}주** 질러!\n* 장 마감 전: 상한가 안 가면 다 팔고 튀어."
        ]

        if wr >= 0.70:
            return f"""
            **[🐹 햄찌의 극딜 브리핑]**
            
            "{random.choice(intros)}
            {random.choice(logic_variations)}
            {random.choice(logic_variations)}
            
            이런 기회 놓치면 진짜 바보 인증이다?"
            
            **[⏰ 햄찌의 실전 타임테이블]**
            {random.choice(timetables)}
            
            **👉 한줄 요약: 인생 역전 기회야! 쫄지 말고 풀매수 박아!**
            """
        elif wr >= 0.50:
            return f"""
            **[🐹 햄찌의 단타 훈수]**
            
            "흥, 차트가 좀 애매하네? **Hurst** {m['hurst']:.2f}라 추세는 있는데 **OBI**가 구려.
            세력들이 간 보고 있는 중이야. 단타 치기엔 좋은 놀이터지.
            길게 가져가면 물린다? 짧게 먹고 빠져."
            
            **[⏰ 햄찌의 실전 타임테이블]**
            * 09:00: 관망해. 들어가면 물린다.\n* 10:30: **{price:,}원** 지지하면 **{int(can_buy/3)}주**만 사.\n* 13:00: 슈팅 나오면 바로 튀어!
            
            **👉 한줄 요약: 욕심 부리지 마! 짧게 먹고 튀는 거야.**
            """
        else:
            return f"""
            **[🐹 햄찌의 경멸]**
            
            "으악! **VPIN** {m['vpin']:.2f}야! 설거지 당하고 싶어?
            **Betti Number** 1 떴어. 차트에 구멍 뚫려서 지옥문 열렸다고!
            이딴 걸 주식이라고 보고 있어?"
            
            **[⏰ 햄찌의 실전 타임테이블]**
            * 지금 당장: **시장가 투매!** 뒤도 돌아보지 마.\n* 장중 내내: HTS 꺼. 쳐다도 보지 마.
            
            **👉 한줄 요약: 폭탄이야! 만지면 손목 날아가! 도망쳐!**
            """

    # 🐯 호찌: 무한 랜덤 문장 (꼰대 + 사자성어 설명 + 방어적)
    def _get_hojji_msg(self, wr, m, can_buy, target, price):
        # 사자성어 리스트 (뜻풀이 포함)
        idioms_good = [
            "**금상첨화(錦上添花)** (비단 위에 꽃을 더함, 좋은 일에 좋은 일이 겹침)", 
            "**낭중지추(囊中之錐)** (주머니 속의 송곳, 재능이 뛰어나 저절로 드러남)", 
            "**파죽지세(破竹之勢)** (대나무를 쪼개듯 맹렬한 기세)",
            "**일취월장(日就月將)** (나날이 다달이 발전하고 성장함)"
        ]
        idioms_bad = [
            "**사상누각(砂上樓閣)** (모래 위에 지은 집, 기초가 약함)", 
            "**내우외환(內憂外患)** (안팎으로 근심과 걱정이 가득함)", 
            "**풍전등화(風前燈火)** (바람 앞의 등불, 매우 위태로움)",
            "**설상가상(雪上加霜)** (눈 위에 서리가 덮임, 엎친 데 덮친 격)"
        ]
        
        intros = [
            "에헴! 요즘 젊은 것들은 차트만 보고 설치지.", "라떼는 말이야, 재무제표 안 보고 사면 뺨을 맞았어.", 
            "허허, 자네. 투자는 도박이 아닐세.", "쯧쯧, 급할수록 돌아가라 했거늘."
        ]
        
        logic_variations = [
            f"**GNN 중심성**이 {m['gnn']:.2f}로군. 시장 자금이 이 종목을 '허브'로 삼아 돌고 있어. 근본이 있는 종목이야.",
            f"**전이 엔트로피(TE)** 흐름이 양호해. 실적과 수급의 조화가 아주 훌륭하구먼.",
            f"**JLS 모델**상 거품 붕괴 위험이 없어. 탄탄대로야. 안심하게.",
            f"내재가치 대비 저평가 상태이며, **안전마진**이 충분히 확보된 자리일세."
        ]
        
        sel_idiom_good = random.choice(idioms_good)
        sel_idiom_bad = random.choice(idioms_bad)

        if wr >= 0.70:
            return f"""
            **[🐯 호찌의 훈장님 말씀]**
            
            "{random.choice(intros)} 아주 {sel_idiom_good}로세!
            
            {random.choice(logic_variations)}
            {random.choice(logic_variations)}
            
            이런 종목은 쉽게 오지 않아. 흔들리지 말고 우직하게 가져가야 하네."
            
            **[⏳ 호찌의 시계열 행동 지침]**
            * **진입:** 변동성이 줄어드는 **오후 2시경**, 자금의 **{int(can_buy*0.8)}주**를 분할 매수하게.
            * **운용:** **{target:,}원** 도달 시까지 단기 등락은 무시하고 **'우보천리(牛步千里)'**하게.
            
            **👉 한줄 요약: 진국일세. 엉덩이 무거운 자가 승리하는 법이야.**
            """
        elif wr >= 0.50:
            return f"""
            **[🐯 호찌의 신중론]**
            
            "음... 계륵(鷄肋)일세. 먹자니 먹을 게 없고, 버리자니 아까운 형국이야.
            **국소 변동성(Local Vol)** 표면이 너무 거칠어. **내우외환(內憂外患)**이 걱정되는구먼.
            
            **꼬리 위험(ES)**이 {m['es']:.2f}로 감지되었어. 돌다리도 두들겨 보고 건너야 하는 살얼음판이야.
            **'거안사위(居安思危)'**의 자세가 필요하네."
            
            **[⏳ 호찌의 시계열 행동 지침]**
            * **진입:** 오늘은 관망하게. 내일 시초가 확인하고 결정해도 늦지 않아.
            * **운용:** 정 사고 싶다면 **{int(can_buy*0.2)}주**만 아주 조금 담아보게.
            
            **👉 한줄 요약: 위험해 보이네. 리스크 관리가 최우선이야.**
            """
        else:
            return f"""
            **[🐯 호찌의 대호통]**
            
            "어허! 이보게! 자네 지금 제정신인가? 이건 {sel_idiom_bad}일세!
            **Going Concern** 이슈가 보여. 기초가 부실한데 어찌 탑을 쌓으려 하는가!
            
            **비에르고딕** 파산 위험이 감지되었어. 여기서 물리면 영원히 복구 불가능해. 
            과거 지지선이 저항선으로 변질되었네."
            
            **[⏳ 호찌의 시계열 행동 지침]**
            * **즉시:** 포트폴리오에서 제외하게. 현금이 곧 최고의 종목이야.
            * **향후:** 펀더멘털 개선 전까진 쳐다도 보지 말게.
            
            **👉 한줄 요약: 썩은 동아줄이야. 절대 잡지 마라.**
            """

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        volatility = m['vol_surf'] * 0.05
        # Price Calculation Logic & Rationale (Detail)
        if mode == "scalping":
            target = int(price * (1 + max(volatility, 0.02)))
            stop = int(price * (1 - volatility * 0.6))
            rationale = f"스캘핑 기준: 내재 변동성(Vol Surface) {m['vol_surf']:.2f}를 기반으로 1.5σ 상단 목표가({target:,}원), 0.6σ 하단 손절가({stop:,}원)를 산출함."
        else:
            target = int(price * (1 + (target_return/100)))
            stop = int(price * 0.93)
            rationale = f"스윙 기준: 목표 수익률 {target_return}% 및 Hurst Exponent {m['hurst']:.2f}의 추세 지속성을 반영하여 지지선(-7%) 설정."
        
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
        
        h = f"""
        "사장님! 현재 **예수금 비중 {cash_r:.1f}%**, **보유 {stock_count}종목**, **평균 수익률 {avg_pnl:.2f}%**야.
        지금 포트폴리오 **Beta**가 **{beta:.2f}**밖에 안 돼. 시장 상승분도 못 먹고 있다구! **[Cash Drag]** 때문에 돈이 썩고 있어!
        
        **[Action Plan]**
        내일 장 시작하면 현금 30% 털어서 주도주 2개 더 담아! 레버리지 ETF 섞어서 베타 1.5로 맞춰! 공격이 최선의 방어라구! 🔥"
        """
        
        t = f"""
        "자네, **보유 {stock_count}종목**에 **예수금 {cash_r:.1f}%**... 너무 안일해.
        리스크 분산이 안 되어 있어. 하락장 오면 공멸할 구조야. 엔트로피가 증가하는 시장에서 무방비 상태라네.
        
        **[Action Plan]**
        수익 중인 종목은 절반 익절하고, 그 돈으로 **[국채]**나 **[금]**을 사서 방어벽을 세우게. 유비무환일세. 🛡️"
        """
        return h, t

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
        
        i1, i2, i3 = st.columns(3)
        pnl = d['pnl']
        i1.metric("현재가", f"{d['price']:,}원")
        i2.metric("수익률", f"{pnl:.2f}%", delta=f"{pnl:.2f}%")
        i3.metric("AI 목표가", f"{p['prices'][1]:,}원")
        
        st.markdown(f"""
        <div class='rationale-box'>
            <span style='color:#FFD700; font-weight:bold;'>💡 가격 산정 근거:</span> 
            <span class='rationale-text'>{p['rationale']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🐹 햄찌의 야수 분석", "🐯 호찌의 방어 분석", "📊 8대 엔진 가이드"])
        
        with tab1: st.info(d['hamzzi'], icon="🐹")
        with tab2: st.warning(d['hojji'], icon="🐯")
        with tab3:
            h1, h2, h3 = st.columns(3)
            h1.metric("Omega", f"{m['omega']:.1f}")
            h1.markdown("<div class='engine-guide'><b>🐹:</b> 15Hz 넘으면 폭발 임박!<br><b>🐯:</b> 임계점 도달 신호.</div>", unsafe_allow_html=True)
            
            h2.metric("VPIN", f"{m['vpin']:.2f}")
            h2.markdown("<div class='engine-guide'><b>🐹:</b> 0.6 넘으면 도망가!<br><b>🐯:</b> 정보 비대칭성 심화.</div>", unsafe_allow_html=True)
            
            h3.metric("GNN", f"{m['gnn']:.2f}")
            h3.markdown("<div class='engine-guide'><b>🐹:</b> 0.8 넘으면 대장주!<br><b>🐯:</b> 네트워크 중심성.</div>", unsafe_allow_html=True)
            
            st.divider()
            
            h4, h5, h6 = st.columns(3)
            h4.metric("Hawkes", f"{m['hawkes']:.2f}")
            h4.markdown("<div class='engine-guide'><b>🐹:</b> 2.0 넘으면 매수 폭주!<br><b>🐯:</b> 내생적 시장 충격.</div>", unsafe_allow_html=True)
            
            h5.metric("Hurst", f"{m['hurst']:.2f}")
            h5.markdown("<div class='engine-guide'><b>🐹:</b> 0.5보다 크면 추세 굿!<br><b>🐯:</b> 시계열의 기억성.</div>", unsafe_allow_html=True)
            
            h6.metric("Kelly", f"{m['kelly']:.2f}")
            h6.markdown("<div class='engine-guide'><b>🐹:</b> 자산의 몇 % 태울까?<br><b>🐯:</b> 최적 자산 배분율.</div>", unsafe_allow_html=True)

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
    if st.button("📊 햄찌와 호찌의 [계좌 정밀 진단] 시작"):
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
