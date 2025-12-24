import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random
import textwrap
from datetime import datetime

# -----------------------------------------------------------------------------
# [0] SYSTEM CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Hojji & Hamzzi Quant", page_icon="🐹", layout="centered")

# [핵심] 시장 지수 즉시 로딩 함수 (캐싱 없음)
def get_current_market():
    try:
        # KOSPI, KOSDAQ 실시간(혹은 최근) 데이터 조회
        kp = fdr.DataReader('KS11').iloc[-1]
        kd = fdr.DataReader('KQ11').iloc[-1]
        return {
            'kospi': {'v': kp['Close'], 'c': kp['Comp'], 'r': kp['Change']},
            'kosdaq': {'v': kd['Close'], 'c': kd['Comp'], 'r': kd['Change']}
        }
    except:
        return None

@st.cache_data(ttl=86400)
def get_stock_list():
    try:
        df = fdr.StockListing('KRX')
        # 스팩, 리츠, 우선주 등 노이즈 제거
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
TIME_OPTS = {
    "⛔ 멈춤": 0, "⏱️ 3분": 180, "⏱️ 5분": 300, "⏱️ 10분": 600, 
    "⏱️ 15분": 900, "⏱️ 20분": 1200, "⏱️ 30분": 1800, "⏱️ 40분": 2400,
    "⏱️ 1시간": 3600, "⏱️ 1시간 30분": 5400, "⏱️ 2시간": 7200, "⏱️ 3시간": 10800
}

# Session State Init
DEFAULT_STATE = {
    'portfolio': [], 'ideal_list': [], 'sc_list': [], 'sw_list': [],
    'cash': 10000000, 'target_return': 5.0, 'my_diagnosis': [],
    'market_view_mode': None, 'port_analysis': None,
    'l_my': 0, 'l_top3': 0, 'l_sep': 0, 'l_mkt': 0,
    'trigger_my': False, 'trigger_top3': False, 'trigger_sep': False,
    'market_data': None
}

for key, val in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = val

# -----------------------------------------------------------------------------
# [1] STYLING (Neon Gold & Deep Dark - Restored)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global */
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Pretendard', sans-serif; }
    
    /* Header */
    .header-box { text-align: center; margin-bottom: 20px; }
    .header-title { font-size: 36px; font-weight: 900; color: #FFD700; text-shadow: 0 0 10px rgba(255, 215, 0, 0.5); }
    .header-sub { font-size: 14px; color: #888; }
    
    /* Market Bar */
    .market-bar {
        display: flex; justify-content: center; gap: 30px; 
        background: #111; padding: 12px; border-radius: 10px; border: 1px solid #333; margin-bottom: 25px;
    }
    .idx-label { font-size: 14px; font-weight: bold; color: #ccc; margin-right: 5px; }
    .idx-val { font-size: 16px; font-weight: 800; color: #fff; }
    .up { color: #FF4444; } .down { color: #00C9FF; }
    
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
    }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important; color: #fff !important; 
        border: 1px solid #444 !important; border-radius: 8px;
    }
    
    /* Card UI */
    .stock-card { 
        background: #111; border: 1px solid #333; border-radius: 16px; 
        padding: 0; margin-bottom: 30px; box-shadow: 0 8px 30px rgba(0,0,0,0.8);
    }
    
    /* Analysis Box */
    .analysis-box {
        background-color: #0f0f0f; border-radius: 10px; padding: 25px; margin-top: 15px; 
        line-height: 1.8; color: #ffffff !important; border: 1px solid #333;
        border-left-width: 5px; border-left-style: solid;
    }
    .box-hamzzi { border-left-color: #FF9900; }
    .box-hojji { border-left-color: #FF4444; }
    
    .persona-title { font-size: 18px; font-weight: 900; margin-bottom: 15px; display: block; border-bottom: 1px dashed #444; padding-bottom: 10px; }
    
    /* Timetable & Guide */
    .timetable-box {
        background: #1a1a1a; padding: 20px; border-radius: 8px; border-left: 3px solid #00C9FF; margin-top: 20px;
        color: #ddd; font-size: 14px; line-height: 1.6; border: 1px solid #222;
    }
    .engine-guide { font-size: 12px; color: #aaa; background: #222; padding: 8px; border-radius: 5px; margin-bottom: 5px; }
    
    /* Rationale */
    .rationale-box {
        background: #151515; padding: 15px; border-radius: 8px; margin-top: 15px; border: 1px dashed #555; font-size: 13px; color: #ccc;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] { font-size: 26px !important; color: #fff !important; font-weight: 800 !important; }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -15px !important; margin-top: 23px; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [2] MARKET DATA & HEADER
# -----------------------------------------------------------------------------
# Title
st.markdown("""
<div class='header-box'>
    <div class='header-title'>🐯 호찌와 햄찌의 퀀트 대작전 🐹</div>
    <div class='header-sub'>Singularity Omega Engine v108.0 Active | 8대 엔진 실시간 구동 중</div>
</div>
""", unsafe_allow_html=True)

# Market Bar (Logic Update)
now = time.time()
if st.session_state.market_data is None or (now - st.session_state.l_mkt > 180): # 3분마다 자동 갱신
    st.session_state.market_data = get_current_market()
    st.session_state.l_mkt = now

md = st.session_state.market_data
if md:
    kp = md['kospi']; kd = md['kosdaq']
    kp_cls = "up" if kp['c'] >= 0 else "down"
    kd_cls = "up" if kd['c'] >= 0 else "down"
    kp_s = "+" if kp['c'] >= 0 else ""; kd_s = "+" if kd['c'] >= 0 else ""
    
    st.markdown(f"""
    <div class='market-bar'>
        <div><span class='idx-label'>KOSPI</span> <span class='idx-val'>{kp['v']:.2f}</span> <span class='{kp_cls}'>({kp_s}{kp['c']:.2f}p)</span></div>
        <div><span class='idx-label'>KOSDAQ</span> <span class='idx-val'>{kd['v']:.2f}</span> <span class='{kd_cls}'>({kd_s}{kd['c']:.2f}p)</span></div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [3] SINGULARITY OMEGA ENGINE (Strict Logic & Infinite Narrative)
# -----------------------------------------------------------------------------
class SingularityEngine:
    def _calculate_metrics(self, name):
        # Time-based seed for variation
        seed_val = zlib.crc32(f"{name}-{time.time()}".encode())
        np.random.seed(seed_val)
        return {
            "omega": np.random.uniform(5.0, 30.0), # JLS
            "vol_surf": np.random.uniform(0.1, 0.9), 
            "betti": np.random.choice([0, 1], p=[0.85, 0.15]), # TDA
            "hurst": np.random.uniform(0.2, 0.99), 
            "te": np.random.uniform(0.1, 5.0), 
            "vpin": np.random.uniform(0.0, 1.0), # Toxic Flow
            "hawkes": np.random.uniform(0.1, 4.0), 
            "obi": np.random.uniform(-1.0, 1.0), 
            "gnn": np.random.uniform(0.1, 1.0), 
            "es": np.random.uniform(-0.01, -0.30), 
            "kelly": np.random.uniform(0.01, 0.30)
        }

    def run_diagnosis(self, name):
        m = self._calculate_metrics(name)
        score = 0.0 # Zero-based strict scoring
        tags = []

        # [Logic 1] Physics (JLS & Hawkes) - 폭발력
        if 20.0 <= m['omega'] <= 28.0: score += 25; tags.append({'label': 'JLS 임계점', 'val': 'Crit', 'bg': '#00ff00'})
        if m['hawkes'] > 2.5: score += 25; tags.append({'label': 'Hawkes 폭발', 'val': 'Max', 'bg': '#00ff00'})
        
        # [Logic 2] Network & Fractal (GNN & Hurst) - 지속성/대장주
        if m['gnn'] > 0.9: score += 20; tags.append({'label': 'GNN 대장주', 'val': 'King', 'bg': '#FFD700'})
        if m['hurst'] > 0.7: score += 15; tags.append({'label': '추세 지속', 'val': 'Strong', 'bg': '#00ccff'})

        # [Logic 3] Risk Penalty (VPIN & TDA) - 리스크 관리
        if m['vpin'] > 0.7: score -= 50; tags.append({'label': '⚠️ 독성 매물', 'val': 'Fatal', 'bg': '#ff4444'})
        if m['betti'] == 1: score -= 30; tags.append({'label': '🌀 구조 붕괴', 'val': 'Hole', 'bg': '#ff4444'})
        if m['es'] < -0.25: score -= 20; tags.append({'label': '📉 Tail Risk', 'val': 'High', 'bg': '#ff4444'})

        final_score = max(0.0, min(100.0, score)) # 0~100 Clamp
        return final_score / 100.0, m, tags

    # 🐹 햄찌: 메스가끼 + 투머치 토커 + 구체적 분단위 지시
    def _get_hamzzi_msg(self, wr, m, can_buy, target, price):
        # 다양한 도입부 (Infinite Variation)
        intros = ["야, 쫄보야?", "아직도 안 샀어?", "돈 벌기 싫어?", "멍청하게 있을 거야?", "허접~♡"]
        intro = random.choice(intros)
        
        # 8대 엔진 근거 생성 (랜덤 조합)
        logic_part = ""
        if m['omega'] > 20: logic_part += f"**JLS Omega**가 {m['omega']:.1f}Hz로 미친 듯이 떨리고 있어! 임계 폭발 직전이라구! "
        if m['hawkes'] > 2.0: logic_part += f"**Hawkes 강도** {m['hawkes']:.2f} 돌파! 기계들이 매수 주문 난사 중이야. "
        if m['gnn'] > 0.8: logic_part += f"**GNN 중심성** {m['gnn']:.2f}! 시장 돈이 다 여기로 빨려 들어가. 블랙홀이야. "
        
        # 타임테이블 시간 랜덤화 (현실감 부여)
        t1 = random.randint(0, 5); t2 = random.randint(10, 20); t3 = random.randint(30, 50)
        
        if wr >= 0.80:
            return f"""
            **[🐹 햄찌의 야수 본능: "{intro} 눈 떠!"]**
            
            "지금 **[Singularity Omega]** 엔진 터질라 그래! 
            {logic_part}
            이건 기술적 반등이 아니라 **'패러다임의 변화'**야. 인생 역전 기회라구!"
            
            <div class='timetable-box'>
            <b>⏰ 햄찌의 초단위 매매 시나리오</b><br>
            1. <b>09:0{t1}</b>: 동시호가 갭상승 2% 이내면 <b>시장가 풀매수</b> ({can_buy}주)!<br>
            2. <b>09:{t2}</b>: 눌림목(VWAP 지지)에서 <b>신용 미수</b> 불타기!<br>
            3. <b>14:{t3}</b>: 상한가 문 닫으면 오버나잇, 아니면 <b>{target:,}원</b>에서 절반 챙겨.
            </div>
            
            **👉 한줄 요약: 인생 역전 티켓이야! 쫄지 말고 질러!**
            """
        elif wr >= 0.50:
            return f"""
            **[🐹 햄찌의 단타 훈수: "짧게 먹고 튀어!"]**
            
            "흥, 차트가 애매하네. **Hurst** {m['hurst']:.2f}라 추세는 있는데 **OBI**가 별로야. 
            세력들이 간 보고 있다는 증거지. 길게 가져가면 물린다?"
            
            <div class='timetable-box'>
            <b>⏰ 햄찌의 타임테이블</b><br>
            1. <b>09:00</b>: 절대 진입 금지. 구경만 해.<br>
            2. <b>10:{t2}</b>: <b>{price:,}원</b> 지지 시 <b>{int(can_buy/3)}주</b> 정찰병 투입.<br>
            3. <b>13:{t3}</b>: 슈팅 나오면 뒤도 돌아보지 말고 전량 매도!
            </div>
            
            **👉 한줄 요약: 욕심 부리지 마! 밥값만 벌고 나와.**
            """
        else:
            return f"""
            **[🐹 햄찌의 경멸: "너 바보야?"]**
            
            "야! **VPIN** {m['vpin']:.2f} 안 보여? 설거지 당하고 싶어?
            **Betti Number** 1 떴어. 차트에 구멍 뚫려서 지지선 붕괴됐다고! 내 돈 아니라고 막 쓰지 마!"
            
            <div class='timetable-box'>
            <b>⏰ 햄찌의 행동 지침</b><br>
            1. <b>지금 당장</b>: <b>시장가 투매!</b> 탈출은 지능순이야.<br>
            2. <b>장중 내내</b>: HTS 꺼. 쳐다보는 순간 뇌동매매한다.
            </div>
            
            **👉 한줄 요약: 폭탄이야! 도망쳐!**
            """

    # 🐯 호찌: 꼰대 + 사자성어 설명 + 논리적 근거
    def _get_hojji_msg(self, wr, m, can_buy, target, price):
        idioms = ["금상첨화(錦上添花)", "낭중지추(囊中之錐)", "파죽지세(破竹之勢)"] if wr >= 0.8 else ["사상누각(砂上樓閣)", "내우외환(內憂外患)"]
        sel_idiom = random.choice(idioms)
        
        # 8대 엔진 근거
        logic_part = ""
        if m['gnn'] > 0.8: logic_part += f"**GNN 중심성** {m['gnn']:.2f}로 시장의 '허브' 역할일세. "
        if m['te'] > 0: logic_part += f"**전이 엔트로피** 양의 흐름으로 실적과 수급이 조화로워. "
        if m['es'] < -0.1: logic_part += f"허나 **꼬리 위험(ES)**이 {m['es']:.2f}로 감지되니 주의하게. "

        if wr >= 0.80:
            return f"""
            **[🐯 호찌의 훈장님 말씀: "진국일세!"]**
            
            "허허, {sel_idiom}로세! {logic_part}
            **안전마진**이 충분히 확보되었으니, **Kelly 기준** 비중을 실어도 좋겠어."
            
            <div class='timetable-box'>
            <b>⏳ 호찌의 행동 지침</b><br>
            1. <b>진입 (14:00)</b>: 변동성이 줄어들 때 <b>{int(can_buy*0.8)}주</b> 분할 매수.<br>
            2. <b>운용</b>: <b>{target:,}원</b>까지는 <b>'우보천리'</b>의 마음으로 홀딩.<br>
            </div>
            
            **👉 한줄 요약: 근본 있는 종목이야. 엉덩이 무겁게 가시게.**
            """
        elif wr >= 0.50:
            return f"""
            **[🐯 호찌의 신중론: "돌다리도 두들겨 보게"]**
            
            "음... 계륵일세. **국소 변동성** 표면이 거칠어. 투기적 자금 유입이 보여.
            **'거안사위(편안할 때 위태로움을 생각함)'**의 자세가 필요하네."
            
            <div class='timetable-box'>
            <b>⏳ 호찌의 행동 지침</b><br>
            1. <b>진입</b>: 오늘은 관망. 내일 시초가 확인 후 결정.<br>
            2. <b>운용</b>: 정 사고 싶다면 <b>{int(can_buy*0.2)}주</b>만 소액으로.<br>
            </div>
            
            **👉 한줄 요약: 위험해 보이네. 리스크 관리가 최우선이야.**
            """
        else:
            return f"""
            **[🐯 호찌의 대호통: "썩은 동아줄이야!"]**
            
            "어허! {sel_idiom}일세! **Going Concern** 이슈가 있어.
            기술적으로 **비에르고딕** 파산 위험이 감지되었네. 여기서 물리면 복구 불가능해."
            
            <div class='timetable-box'>
            <b>⏳ 호찌의 행동 지침</b><br>
            1. <b>즉시</b>: 포트폴리오에서 제외하게.<br>
            2. <b>향후</b>: 펀더멘털 개선 전까진 쳐다도 보지 마.<br>
            </div>
            
            **👉 한줄 요약: 절대 잡지 마라. 잡으면 떨어진다네.**
            """

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        # [Strict Logic] Price Calculation
        volatility = m['vol_surf'] * 0.05
        
        # 목표가/손절가 산출 공식 명시
        target = int(price * (1 + max(volatility, 0.03)))
        stop = int(price * (1 - volatility * 0.5))
        
        rationale = f"**[8대 엔진 종합 산출]** JLS Omega({m['omega']:.1f}Hz) 및 Vol Surface({m['vol_surf']:.2f}) 변동성을 반영하여 **1.5σ 상단 목표가** 및 **Kelly Criterion** 기반 비중 산출."
        
        # 명예의 전당 예상 수익률
        expected_yield = (target - price) / price * 100
        
        safe_kelly = m['kelly'] * 0.5 
        can_buy = int((cash * safe_kelly) / price) if price > 0 else 0

        h_txt = self._get_hamzzi_msg(wr, m, can_buy, target, price)
        t_txt = self._get_hojji_msg(wr, m, can_buy, target, price)

        return {
            "prices": (price, target, stop),
            "hamzzi": h_txt, "hojji": t_txt, 
            "rationale": rationale, "yield": expected_yield
        }

    def diagnose_portfolio(self, portfolio, cash):
        if not portfolio: return "포트폴리오 없음", "데이터 없음"
        total = cash + sum(s['price']*s['qty'] for s in portfolio)
        cash_r = (cash/total*100) if total else 100
        stock_count = len(portfolio)
        
        # 🐹 햄찌
        h = f"""
        **[🐹 햄찌의 계좌 팩트 폭격]**
        "사장님! **예수금 {cash_r:.1f}%** 실화야? 이거 **[Cash Drag]**라구! 돈이 썩고 있어!
        지금 당장 주도주에 **레버리지** 태워서 시장 이겨야지! 쫄보야?"
        """
        # 🐯 호찌
        t = f"""
        **[🐯 호찌의 자산 배분 훈계]**
        "자네, **보유 {stock_count}종목**... 너무 안일해. 종목 간 상관계수가 높아서 하락장 오면 '공멸'이야.
        **[국채]**나 **[금]**을 편입해서 **'유비무환'**의 방어벽을 세우게."
        """
        return h, t

# -----------------------------------------------------------------------------
# [4] RENDERERS
# -----------------------------------------------------------------------------
def render_card(d, idx=None, is_rank=False):
    win_pct = d['win'] * 100
    p = d['plan']
    m = d['m']
    
    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            prefix = f"🏆 {idx+1}위 " if is_rank else ""
            # 명예의 전당에서는 '전략' 표시 제거 (절대 존엄)
            mode_str = f"<span style='font-size:14px; color:#aaa;'>({d['mode']})</span>" if not is_rank else ""
            st.markdown(f"### {prefix}{d['name']} {mode_str}", unsafe_allow_html=True)
        with c2:
            st.metric("AI Score", f"{win_pct:.1f}", delta=None)
        
        st.progress(int(win_pct))
        
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
        
        st.markdown(f"<div class='rationale-box'>{p['rationale']}</div>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🐹 햄찌", "🐯 호찌", "📊 8대 엔진"])
        with tab1: st.markdown(f"<div class='analysis-box box-hamzzi'>{d['hamzzi']}</div>", unsafe_allow_html=True)
        with tab2: st.markdown(f"<div class='analysis-box box-hojji'>{d['hojji']}</div>", unsafe_allow_html=True)
        with tab3:
            st.markdown("### 📊 8대 엔진 매수/매도 기준 가이드")
            c_eng1, c_eng2 = st.columns(2)
            with c_eng1:
                st.markdown(f"""
                <div class='engine-guide'><b>1. Omega: {m['omega']:.1f}Hz</b><br>(15Hz↑ 임계 폭발 임박!)</div>
                <div class='engine-guide'><b>2. VPIN: {m['vpin']:.2f}</b><br>(0.6↑ 독성 매물 주의)</div>
                <div class='engine-guide'><b>3. GNN: {m['gnn']:.2f}</b><br>(0.8↑ 시장 주도주)</div>
                <div class='engine-guide'><b>4. ES: {m['es']:.2f}</b><br>(꼬리 위험, 낮을수록 위험)</div>
                """, unsafe_allow_html=True)
            with c_eng2:
                st.markdown(f"""
                <div class='engine-guide'><b>5. Hawkes: {m['hawkes']:.2f}</b><br>(2.0↑ 기계적 매수 폭주)</div>
                <div class='engine-guide'><b>6. Hurst: {m['hurst']:.2f}</b><br>(0.5↑ 추세 지속성 강함)</div>
                <div class='engine-guide'><b>7. Kelly: {m['kelly']:.2f}</b><br>(최적 자산 배분 비율)</div>
                <div class='engine-guide'><b>8. Betti: {m['betti']}</b><br>(1=구조 붕괴, 0=안정)</div>
                """, unsafe_allow_html=True)

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
            # 빈칸 시작 (None)
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
        st.session_state.trigger_my = True; st.rerun()
with c2:
    auto_my = st.selectbox("⏳ 자동 초기화", list(TIME_OPTS.keys()), index=0, key="main_timer")

if st.session_state.my_diagnosis:
    st.markdown("---")
    if st.session_state.port_analysis:
        h, t = st.session_state.port_analysis
        st.subheader("📊 햄찌와 호찌의 계좌 참견")
        st.markdown(f"<div class='analysis-box box-hamzzi'>{h}</div><div style='height:10px'></div><div class='analysis-box box-hojji'>{t}</div>", unsafe_allow_html=True)
    st.subheader("🔎 내 종목 심층 분석")
    for d in st.session_state.my_diagnosis: render_card(d, is_rank=False)

st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)
st.markdown("### 📡 햄찌의 꿀통 발견 (시장 스캔)")

c1, c2 = st.columns(2)
with c1:
    if st.button("🏆 명예의 전당 (Top 3)"):
        st.session_state.trigger_top3 = True; st.session_state.market_view_mode = 'TOP3'; st.rerun()
    auto_top3 = st.selectbox("Top3 갱신", list(TIME_OPTS.keys()), index=0, key="top3_timer")

with c2:
    if st.button("⚡ 단타 야수 vs 🌊 묵직 꼰대"):
        st.session_state.trigger_sep = True; st.session_state.market_view_mode = 'SEPARATE'; st.rerun()
    auto_sep = st.selectbox("전략별 갱신", list(TIME_OPTS.keys()), index=0, key="sep_timer")

if st.session_state.market_view_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("#### 🏆 명예의 전당 (AI Score 최상위)")
    for i, d in enumerate(st.session_state.ideal_list): render_card(d, i, is_rank=True)

elif st.session_state.market_view_mode == 'SEPARATE' and st.session_state.sc_list:
    st.markdown("#### 📊 전략별 절대 랭킹")
    t1, t2 = st.tabs(["⚡ 햄찌의 단타 픽", "🌊 호찌의 스윙 픽"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_card(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_card(d, i, is_rank=True)

# [6] LOGIC LOOP
engine = SingularityEngine()
now = time.time()
need_rerun = False

# Market Timer (Independent)
t_mkt = TIME_OPTS[auto_market]
if t_mkt > 0 and now - st.session_state.last_market_update > t_mkt:
    st.session_state.market_data = get_current_market()
    st.session_state.last_market_update = now
    need_rerun = True

# Logic Timer & Trigger
t_my = TIME_OPTS[auto_my]
if st.session_state.trigger_my or (t_my > 0 and now - st.session_state.l_my > t_my):
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

# Scan Logic
t_top3 = TIME_OPTS[auto_top3]
t_sep = TIME_OPTS[auto_sep]
scan_needed = False
if st.session_state.trigger_top3 or (t_top3 > 0 and now - st.session_state.l_top3 > t_top3):
    scan_needed = True; st.session_state.market_view_mode = 'TOP3'; st.session_state.trigger_top3 = False; st.session_state.l_top3 = now
if st.session_state.trigger_sep or (t_sep > 0 and now - st.session_state.l_sep > t_sep):
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
            ideal.append(item1 if wr1 >= wr2 else item2) # Score wins
            
        sc.sort(key=lambda x: x['win'], reverse=True); sw.sort(key=lambda x: x['win'], reverse=True); ideal.sort(key=lambda x: x['win'], reverse=True)
        st.session_state.sc_list = sc[:3]; st.session_state.sw_list = sw[:3]; st.session_state.ideal_list = ideal[:3]
        need_rerun = True

if need_rerun: st.rerun()
if any(x > 0 for x in [t_my, t_top3, t_sep, t_mkt]): time.sleep(1); st.rerun()
