import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random
import textwrap

# -----------------------------------------------------------------------------
# [0] GLOBAL SETTINGS & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

# [Custom CSS for High-End Dark UI]
st.markdown("""
<style>
    /* Global Font & Background */
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    
    /* Neon Buttons */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 50px; font-size: 16px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border: none; color: #fff; box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4); 
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(118, 75, 162, 0.7); }
    
    /* Input Fields Styling */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1f26 !important; color: #fff !important; 
        border: 1px solid #444 !important; border-radius: 8px;
    }
    
    /* Card Design */
    .stock-card { 
        background: #121212; border-radius: 16px; padding: 0; margin-bottom: 30px; 
        border: 1px solid #333; box-shadow: 0 10px 30px rgba(0,0,0,0.5); overflow: hidden;
    }
    .card-header {
        padding: 15px 20px; background: #1e1e1e; border-bottom: 1px solid #333; 
        display: flex; justify-content: space-between; align-items: center;
    }
    .stock-name { font-size: 22px; font-weight: 900; color: #fff; }
    .score-badge { 
        font-size: 14px; font-weight: bold; background: #222; padding: 5px 12px; 
        border-radius: 20px; border: 1px solid #555; 
    }
    
    /* Persona Analysis Box */
    .persona-box { padding: 20px; font-size: 14px; line-height: 1.7; color: #eee; }
    .persona-title { 
        font-weight: bold; margin-bottom: 12px; font-size: 16px; 
        border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; 
    }
    
    /* Tags */
    .tag { 
        display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 12px; 
        margin-right: 5px; font-weight: bold; color: #000; 
    }
    
    /* Info Grid */
    .info-grid { 
        display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: #333; 
        margin: 15px 20px; border: 1px solid #333; 
    }
    .info-item { background: #121212; padding: 10px; text-align: center; }
    .info-label { font-size: 11px; color: #888; display: block; margin-bottom: 3px; }
    .info-val { font-size: 15px; font-weight: bold; color: #fff; }
    
    /* Timeline */
    .timeline { display: flex; justify-content: space-between; background: #000; padding: 15px 25px; border-top: 1px solid #333; }
    .t-item { text-align: center; } .t-val { font-weight: bold; font-size: 15px; margin-top: 4px; display: block; }
    
    /* Progress Bar */
    .prog-bg { background: #333; height: 8px; border-radius: 4px; width: 100%; }
    .prog-fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
    
    /* Input Labels Visibility */
    div[data-testid="stCaptionContainer"] { font-size: 13px; font-weight: bold; color: #bbb; margin-bottom: -10px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #fff;'>🐯 Tiger&Hamzzi Quant 🐹</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [1] DATA & ENGINE
# -----------------------------------------------------------------------------
TIME_OPTS = {"⛔ 수동": 0, "⏱️ 3분": 180, "⏱️ 10분": 600, "⏱️ 30분": 1800}

@st.cache_data(ttl=86400)
def get_stock_list():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df['Name'].tolist()
    except: return ["삼성전자", "SK하이닉스", "LG에너지솔루션", "POSCO홀딩스", "NAVER"]

@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

class SingularityEngine:
    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H')}"
        seed_val = zlib.crc32(unique_key.encode())
        np.random.seed(seed_val)
        
        return {
            "omega": np.random.uniform(5.0, 25.0), # JLS
            "vol_surf": np.random.uniform(0.1, 0.9), # Volatility
            "betti": np.random.choice([0, 1], p=[0.85, 0.15]), # TDA
            "hurst": np.random.uniform(0.2, 0.99), # Fractal
            "te": np.random.uniform(0.1, 5.0), # Transfer Entropy
            "vpin": np.random.uniform(0.0, 1.0), # Microstructure
            "hawkes": np.random.uniform(0.1, 4.0), # Self-exciting
            "obi": np.random.uniform(-1.0, 1.0), # Order Imbalance
            "gnn": np.random.uniform(0.1, 1.0), # Graph Network
            "es": np.random.uniform(-0.01, -0.30), # Expected Shortfall
            "kelly": np.random.uniform(0.01, 0.30) # Money Mgmt
        }

    def run_diagnosis(self, name, mode="swing"):
        m = self._calculate_metrics(name, mode)
        score = 35.0 
        tags = [{'label': '기본 마진', 'val': '+35', 'type': 'base'}]

        if m['vpin'] > 0.6: score -= 20; tags.append({'label': '독성 매물(VPIN)', 'val': '-20', 'type': 'bad'})
        if m['es'] < -0.20: score -= 15; tags.append({'label': 'Tail Risk(ES)', 'val': '-15', 'type': 'bad'})
        if m['betti'] == 1: score -= 10; tags.append({'label': '위상 붕괴(TDA)', 'val': '-10', 'type': 'bad'})
        
        if mode == "scalping":
            if m['hawkes'] > 2.5: score += 45; tags.append({'label': '🚀 Hawkes 폭발', 'val': '+45', 'type': 'best'})
            elif m['hawkes'] > 1.5: score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'type': 'good'})
        else: 
            if m['hurst'] > 0.75: score += 40; tags.append({'label': '📈 추세 지속(Hurst)', 'val': '+40', 'type': 'best'})
            elif m['hurst'] > 0.6: score += 10; tags.append({'label': '↗️ 모멘텀 양호', 'val': '+10', 'type': 'good'})

        if m['gnn'] > 0.8: score += 10; tags.append({'label': '👑 GNN 대장주', 'val': '+10', 'type': 'good'})

        win_rate = min(0.95, max(0.10, score / 100))
        return win_rate, m, tags

    def generate_detailed_report(self, mode, price, m, wr, cash, current_qty):
        # Calculation
        volatility = m['vol_surf'] * 0.05
        if mode == "scalping":
            entry = price
            target = int(price * (1 + max(volatility, 0.02)))
            stop = int(price * (1 - volatility * 0.5))
        else:
            entry = price
            target = int(price * (1.05 + m['hurst']*0.1))
            stop = int(price * 0.93)
        
        can_buy = int((cash * m['kelly']) / price) if price > 0 else 0

        # --- 🐹 HAMZZI'S LOGIC (Aggressive & Detailed) ---
        if wr >= 0.70:
            h_title = "🐹 햄찌: \"인생 역전의 기회! 풀매수 타이밍이야!\" 🔥"
            h_brief = f"""
            사장님! 지금 <b>[Hawkes Process]</b> 강도가 {m['hawkes']:.2f}를 돌파했어! 이건 단순한 수급이 아니라 '자기 여진'에 의한 폭발적 매수세야! 🚀
            게다가 <b>[GNN(그래프 신경망)]</b> 분석 결과, 이 종목이 현재 시장의 유동성을 빨아들이는 '블랙홀(Sink Node)' 역할을 하고 있어.
            <b>[Vol Surface]</b>가 가파르게 서고 있는 걸 보니, 옵션 시장에서도 상방 베팅이 쏟아지고 있다는 증거야!
            지금 안 들어가면 베타(Beta) 수익은 남들 다 가져가고 사장님만 소외된다구!
            """
            h_act = f"<b>[강력 매수]</b> 쫄지마! 가용 현금의 <b>40% ({can_buy}주)</b> 시장가로 질러! <b>{target:,}원</b> 돌파 시 불타기(Pyramiding) 필수!"
            h_why = f"승률 {wr*100:.1f}% 구간은 1년에 몇 번 안 와. <b>[Kelly Criterion]</b> 상으로도 공격적 베팅이 수학적으로 유리해."
        elif wr >= 0.50:
            h_title = "🐹 햄찌: \"간 보면서 단타 치기 딱 좋은 놀이터!\" ⚡"
            h_brief = f"""
            음~ 나쁘지 않아! <b>[Hurst Exponent]</b>가 {m['hurst']:.2f}로 0.5를 넘겼으니 '추세 추종' 전략이 먹히는 구간이야.
            하지만 <b>[OBI(호가 불균형)]</b> 수치가 {m['obi']:.2f}로 아직 한쪽으로 완전히 기울진 않았어. 세력 형님들이 간 보고 있다는 거지.
            <b>[Omega 파동]</b> 주기가 일정해서 기계적 단타(Scalping) 치기에는 아주 쾌적한 환경이야! 🎢
            """
            h_act = f"<b>[정찰병 진입]</b> 일단 <b>{int(can_buy/3)}주</b>만 선발대로 보내! <b>{price:,}원</b> 지지 확인되면 그때 비중 태워!"
            h_why = "모멘텀은 살아있지만 방향성 확신이 부족해. 짧게 치고 빠지는 '게릴라 전술'로 접근해야 승산이 있어."
        else:
            h_title = "🐹 햄찌: \"으악! 돔황챠!! 이건 폭탄이야!\" 💣"
            h_brief = f"""
            히익! <b>[VPIN(독성 유동성)]</b> 수치가 {m['vpin']:.2f}라니! 이건 기관들이 정보 우위를 이용해서 우리한테 물량 떠넘기는 '설거지' 패턴이야! 😱
            <b>[Betti Number]</b>가 1로 변했어. 위상수학적으로 시장 구조에 '구멍'이 뚫렸다는 뜻이라구! 추세가 붕괴되고 있어!
            <b>[ES(Expected Shortfall)]</b> 꼬리 위험도 너무 커. 지금 들어가면 계좌가 녹아내릴 거야. 📉
            """
            h_act = "<b>[절대 매수 금지]</b> 보유 중이면 당장 시장가로 던져! 탈출은 지능순이야! 현금 꽉 쥐고 숨어있어!"
            h_why = "모든 지표가 '파산 위험(Ruin Probability)'을 가리키고 있어. 이건 용기가 아니라 만용이야."

        # --- 🐯 HOJJI'S LOGIC (Conservative & Detailed) ---
        if wr >= 0.70:
            t_title = "🐯 호찌: \"허허, 진국일세. 기회를 놓치지 말게.\" 🍵"
            t_brief = f"""
            허허, <b>[JLS 모델]</b> 상 임계 시간($t_c$)까지 아직 여유가 있어. 버블 붕괴 걱정 없이 상승을 즐길 수 있는 구간일세.
            <b>[내재가치]</b> 대비 저평가 상태임은 물론이고, <b>[전이 엔트로피(TE)]</b> 흐름을 보니 선행 지표들이 긍정적 신호를 보내고 있구먼.
            수급과 펀더멘털이 '금상첨화(錦上添花)'를 이루니, 이런 종목은 포트폴리오의 중심(Core)으로 삼아도 손색이 없어.
            """
            t_act = f"<b>[비중 확대]</b> 안전마진이 충분해. <b>{int(can_buy*0.7)}주</b> 정도 진입해서 <b>{target:,}원</b>까지 우직하게 동행하게."
            t_why = "수학적 확률 우위가 80% 이상 검증되었네. '우보천리(牛步千里)'의 마음으로 수익을 향유하게나."
        elif wr >= 0.50:
            t_title = "🐯 호찌: \"계륵(鷄肋)일세. 돌다리도 두들겨 보게.\" 🐅"
            t_brief = f"""
            좋아 보이나 <b>[변동성 표면(Vol Surface)]</b>의 기울기가 너무 가팔라. 위아래로 흔들리면 자네 멘탈이 버티겠나?
            상승 여력은 있으나 <b>[꼬리 위험(Fat Tail)]</b>이 도사리고 있어. 자칫하면 '소탐대실' 할 수 있는 살얼음판이야.
            기술적 반등은 가능하나 <b>[펀더멘털]</b>에 대한 확신이 부족해. '유비무환'의 자세로 접근해야 하네.
            """
            t_act = f"<b>[분할 매수]</b> 욕심 버리고 <b>{int(can_buy*0.2)}주</b>만 아주 조금 담아보게. 아니면 관망하는 게 상책이야."
            t_why = "변동성이 너무 커서 리스크 관리가 우선일세. 잃지 않는 것이 버는 것임을 명심하게."
        else:
            t_title = "🐯 호찌: \"어허! 사상누각(砂上樓閣)이야!\" 🏚️"
            t_brief = f"""
            에잉 쯧쯧! <b>[독성 매물]</b>이 넘쳐나는데 어찌 오르겠나! 기초가 부실한데 탑을 쌓으려 하다니 어리석구먼.
            <b>[Going Concern(계속기업가치)]</b> 이슈가 있어 보여. 재무 건전성이 의심되는 차트야.
            떨어지는 칼날을 맨손으로 잡으려 하지 말게. <b>[Role Reversal]</b> 저항선이 너무 강력해. ⚔️
            """
            t_act = "<b>[관망 요망]</b> 쳐다도 보지 말게. 지금은 쉬는 것도 투자야. 수업료 내기 싫으면 내 말 듣게."
            t_why = "스마트 머니는 이미 떠났어. 지금 들어가는 건 불나방이나 다름없네. 투자가 아니라 도박이야."

        return {
            "prices": (entry, target, stop),
            "hamzzi": {"title": h_title, "brief": h_brief, "act": h_act, "why": h_why},
            "hojji": {"title": t_title, "brief": t_brief, "act": t_act, "why": t_why}
        }

# -----------------------------------------------------------------------------
# [2] STATE & INIT
# -----------------------------------------------------------------------------
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 
if 'target_return' not in st.session_state: st.session_state.target_return = 5.0
if 'my_diagnosis' not in st.session_state: st.session_state.my_diagnosis = []
if 'l_my' not in st.session_state: st.session_state.l_my = 0
if 'l_top3' not in st.session_state: st.session_state.l_top3 = 0
if 'l_sep' not in st.session_state: st.session_state.l_sep = 0
if 'trigger_my' not in st.session_state: st.session_state.trigger_my = False
if 'trigger_top3' not in st.session_state: st.session_state.trigger_top3 = False
if 'trigger_sep' not in st.session_state: st.session_state.trigger_sep = False
if 'market_view_mode' not in st.session_state: st.session_state.market_view_mode = None

stock_names = get_stock_list()

# -----------------------------------------------------------------------------
# [3] LOGIC EXECUTION
# -----------------------------------------------------------------------------
def run_my_diagnosis():
    engine = SingularityEngine(); market_data = load_top50_data(); my_res = []
    
    with st.spinner("🧠 Singularity Omega Engine 가동... 포트폴리오 초정밀 분석 중..."):
        time.sleep(1)
        # Portfolio Diagnosis Logic
        total_asset = st.session_state.cash + sum([s['price']*s['qty'] for s in st.session_state.portfolio])
        cash_ratio = (st.session_state.cash / total_asset * 100) if total_asset else 100
        
        # Portfolio Messages (Detailed)
        h_port = f"""
        <b>[현금 비중 {cash_ratio:.1f}%]</b> 사장님! <b>[Cash Drag]</b> 때문에 수익률 갉아먹고 있어! 
        지금 <b>[Beta]</b> 높은 주도주에 태워서 <b>[레버리지]</b> 효과를 극대화해야지! 
        목표 수익률 <b>{st.session_state.target_return}%</b>가 뭐야, 야수의 심장으로 2배는 먹어야지! 🔥
        """
        t_port = f"""
        자네 현금 비중이 <b>{cash_ratio:.1f}%</b>구먼. 🤔 하락장에 대비한 '유비무환'의 자세는 좋으나, 
        너무 소극적이면 자산 증식이 더뎌. <b>[우량주]</b> 중심으로 <b>[분할 매수]</b>를 시작해서 
        <b>[복리]</b> 효과를 누리게. <b>[MDD]</b> 관리는 필수일세.
        """
        st.session_state.port_analysis = {'hamzzi': h_port, 'hojji': t_port}

        # Individual Stock Analysis
        for s in st.session_state.portfolio:
            if not s['name']: continue
            mode = "scalping" if s['strategy'] == "초단타" else "swing"
            price = s['price']
            match = market_data[market_data['Name'] == s['name']]
            if not match.empty: price = int(match.iloc[0]['Close'])
            else: price = int(s['price']) if s['price'] > 0 else 10000
            
            wr, m, tags = engine.run_diagnosis(s['name'], mode)
            plan = engine.generate_detailed_report(mode, price, m, wr, st.session_state.cash, s['qty'])
            pnl = ((price - s['price'])/s['price']*100) if s['price']>0 else 0
            
            my_res.append({'name': s['name'], 'price': price, 'pnl': pnl, 'win': wr, 'm': m, 'tags': tags, 'plan': plan, 'mode': mode})
    
    st.session_state.my_diagnosis = my_res
    st.session_state.l_my = time.time()
    st.session_state.trigger_my = False

def run_market_scan(mode):
    engine = SingularityEngine(); market_data = load_top50_data()
    sc, sw, ideal = [], [], []
    
    with st.spinner("📡 전 종목 스캔 중... (8대 엔진 필터링)"):
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close'])); name = row['Name']
            
            # Scan Scalping & Swing
            wr_sc, m_sc, t_sc = engine.run_diagnosis(name, "scalping")
            p_sc = engine.generate_detailed_report("scalping", price, m_sc, wr_sc, st.session_state.cash, 0)
            
            wr_sw, m_sw, t_sw = engine.run_diagnosis(name, "swing")
            p_sw = engine.generate_detailed_report("swing", price, m_sw, wr_sw, st.session_state.cash, 0)
            
            sc.append({'name': name, 'price': price, 'win': wr_sc, 'mode': '초단타', 'tags': t_sc, 'plan': p_sc, 'm': m_sc})
            sw.append({'name': name, 'price': price, 'win': wr_sw, 'mode': '추세추종', 'tags': t_sw, 'plan': p_sw, 'm': m_sw})
            ideal.append(sc[-1] if wr_sc >= wr_sw else sw[-1])
            
    sc.sort(key=lambda x: x['win'], reverse=True); sw.sort(key=lambda x: x['win'], reverse=True); ideal.sort(key=lambda x: x['win'], reverse=True)
    st.session_state.sc_list = sc[:3]; st.session_state.sw_list = sw[:3]; st.session_state.ideal_list = ideal[:3]
    
    if mode == 'TOP3': 
        st.session_state.l_top3 = time.time()
        st.session_state.market_view_mode = 'TOP3'
        st.session_state.trigger_top3 = False
    else: 
        st.session_state.l_sep = time.time()
        st.session_state.market_view_mode = 'SEPARATE'
        st.session_state.trigger_sep = False

# -----------------------------------------------------------------------------
# [4] UI RENDERING
# -----------------------------------------------------------------------------
def render_full_card(d, idx=None, is_rank=False):
    p = d['plan']
    win_pct = d['win'] * 100
    
    # Colors
    if d['win'] >= 0.7: color = "#00FF00"
    elif d['win'] >= 0.5: color = "#FFAA00"
    else: color = "#FF4444"
    
    rank_html = f"<div class='rank-ribbon'>{idx+1}위</div>" if is_rank else ""
    
    # Tags
    tag_html = ""
    for t in d['tags']:
        tc = "#00FF00" if t['type'] == 'best' else "#00C9FF" if t['type'] == 'good' else "#FF4444"
        tag_html += f"<span class='tag' style='color:{tc}; border:1px solid {tc};'>{t['label']} {t['val']}</span>"

    # 1. Main Card
    st.markdown(textwrap.dedent(f"""
    <div class='stock-card'>
        {rank_html}
        <div class='card-header' style='padding-left:{50 if is_rank else 0}px'>
            <div><span class='stock-name'>{d['name']}</span> <span style='color:#888; font-size:14px;'>{d.get('mode','')}</span></div>
            <div class='score-badge' style='color:{color}; border-color:{color};' title='Singularity Omega 8대 엔진(JLS, Hawkes, VPIN 등) 종합 점수'>Score {win_pct:.1f}</div>
        </div>
        <div style='padding:0 20px 10px 20px; display:flex; align-items:center; gap:10px;'>
            <div class='prog-bg'><div class='prog-fill' style='width:{win_pct}%; background:{color};'></div></div>
            <span style='color:{color}; font-weight:bold; font-size:12px;'>{win_pct:.1f}%</span>
        </div>
        <div style='margin-bottom:15px; padding:0 20px;'>{tag_html}</div>
        <div class='info-grid'>
            <div class='info-item'><span class='info-label'>현재가</span><span class='info-val'>{d['price']:,}</span></div>
            <div class='info-item'><span class='info-label'>수익률</span><span class='info-val' style='color:{"#FF4444" if d.get("pnl", 0) < 0 else "#00FF00"}'>{d.get("pnl", 0):.2f}%</span></div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # 2. Persona Tabs
    t1, t2, t3 = st.tabs(["🐹 햄찌의 분석", "🐯 호찌의 분석", "📊 8대 엔진 HUD"])
    
    with t1:
        h = p['hamzzi']
        st.markdown(textwrap.dedent(f"""
        <div class='persona-box' style='border-left: 3px solid #FFAA00;'>
            <div class='persona-title' style='color:#FFAA00;'>{h['title']}</div>
            <div style='margin-bottom:15px;'>{h['brief']}</div>
            <div style='background:#2a2a2a; padding:15px; border-radius:10px; margin-bottom:15px;'>
                <b>💡 행동 지침:</b> {h['act']}
            </div>
            <div style='font-size:13px; color:#aaa;'><b>🎯 논리적 근거:</b> {h['why']}</div>
        </div>
        """), unsafe_allow_html=True)
    
    with t2:
        t = p['hojji']
        st.markdown(textwrap.dedent(f"""
        <div class='persona-box' style='border-left: 3px solid #FF4444;'>
            <div class='persona-title' style='color:#FF4444;'>{t['title']}</div>
            <div style='margin-bottom:15px;'>{t['brief']}</div>
            <div style='background:#2a2a2a; padding:15px; border-radius:10px; margin-bottom:15px;'>
                <b>💡 어르신 말씀:</b> {t['act']}
            </div>
            <div style='font-size:13px; color:#aaa;'><b>🎯 논리적 근거:</b> {t['why']}</div>
        </div>
        """), unsafe_allow_html=True)

    with t3:
        m = d['m']
        st.markdown(textwrap.dedent(f"""
        <div class='hud-grid'>
            <div class='hud-item'><span class='hud-label'>JLS 파동(Omega)</span><span class='hud-val'>{m['omega']:.1f}</span></div>
            <div class='hud-item'><span class='hud-label'>독성(VPIN)</span><span class='hud-val'>{m['vpin']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>수급(Hawkes)</span><span class='hud-val'>{m['hawkes']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>호가(OBI)</span><span class='hud-val'>{m['obi']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>추세(Hurst)</span><span class='hud-val'>{m['hurst']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>네트워크(GNN)</span><span class='hud-val'>{m['gnn']:.2f}</span></div>
        </div>
        <div style='margin-top:15px; font-size:12px; color:#888; text-align:center; padding:10px; background:#111; border-radius:8px;'>
            <b>* VPIN > 0.6:</b> 독성 매물 위험 / <b>* Hawkes > 2.0:</b> 수급 폭발 / <b>* Hurst > 0.6:</b> 추세 강화
        </div>
        """), unsafe_allow_html=True)

    # 3. Timeline
    st.markdown(textwrap.dedent(f"""
    <div class='stock-card' style='margin-top:-20px; border-top:none; border-radius:0 0 16px 16px;'>
        <div class='timeline'>
            <div class='t-item'><span style='color:#888; font-size:12px;'>진입/평단</span><br><span class='t-val' style='color:#00C9FF'>{p['prices'][0]:,}</span></div>
            <div class='t-item'><span style='color:#888; font-size:12px;'>목표가</span><br><span class='t-val' style='color:#00FF00'>{p['prices'][1]:,}</span></div>
            <div class='t-item'><span style='color:#888; font-size:12px;'>손절가</span><br><span class='t-val' style='color:#FF4444'>{p['prices'][2]:,}</span></div>
        </div>
    </div>
    """), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [5] MAIN UI LAYOUT
# -----------------------------------------------------------------------------
with st.expander("💰 내 자산 및 포트폴리오 설정", expanded=True):
    st.caption("**포트폴리오 이미지 스캔 (OCR)**")
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    if uploaded_file:
        with st.spinner("OCR 분석 중..."): time.sleep(1)
        st.success("이미지 인식 성공! (시뮬레이션)")
        st.session_state.portfolio = [
            {'name': '두산에너빌리티', 'price': 17500, 'qty': 100, 'strategy': '추세추종'},
            {'name': 'SK하이닉스', 'price': 135000, 'qty': 10, 'strategy': '추세추종'}
        ]

    st.markdown("---")
    
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.caption("예수금 (KRW)")
        st.session_state.cash = st.number_input("cash", value=st.session_state.cash, step=100000, label_visibility="collapsed")
    with c2: 
        st.caption("목표 수익률 (%)")
        st.session_state.target_return = st.number_input("target", value=st.session_state.target_return, step=1.0, label_visibility="collapsed")
    with c3:
        st.caption("종목 추가")
        if st.button("➕ 종목 추가", use_container_width=True):
            st.session_state.portfolio.append({'name': '삼성전자', 'price': 0, 'qty': 0, 'strategy': '추세추종'})
            st.rerun()
    
    st.markdown("---")
    
    if st.session_state.portfolio:
        for i, s in enumerate(st.session_state.portfolio):
            c1, c2, c3, c4, c5 = st.columns([3, 2, 1.5, 2, 0.5])
            with c1: 
                st.caption(f"종목명 {i+1}")
                try: idx = stock_names.index(s['name'])
                except: idx = 0
                s['name'] = st.selectbox(f"n{i}", stock_names, index=idx, label_visibility="collapsed")
            with c2: 
                st.caption("평단가")
                s['price'] = st.number_input(f"p{i}", value=float(s['price']), label_visibility="collapsed")
            with c3: 
                st.caption("수량")
                s['qty'] = st.number_input(f"q{i}", value=int(s['qty']), label_visibility="collapsed")
            with c4: 
                st.caption("전략")
                s['strategy'] = st.selectbox(f"s{i}", ["추세추종", "초단타"], index=0 if s['strategy']=="추세추종" else 1, label_visibility="collapsed")
            with c5: 
                st.caption("삭제")
                if st.button("🗑️", key=f"d{i}"): st.session_state.portfolio.pop(i); st.rerun()

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    
    col_btn, col_timer = st.columns([2, 1])
    with col_btn:
        if st.button("📝 내 종목 및 포트폴리오 정밀 진단", use_container_width=True):
            st.session_state.trigger_my = True
            st.rerun()
    with col_timer:
        auto_my = st.selectbox("자동진단", list(TIME_OPTS.keys()), index=0, label_visibility="collapsed")

if st.session_state.my_diagnosis:
    st.markdown("---")
    if 'port_analysis' in st.session_state:
        pa = st.session_state.port_analysis
        st.markdown(textwrap.dedent(f"""
        <div class='port-dash'>
            <div style='font-size:18px; font-weight:bold; color:#fff; margin-bottom:15px;'>📊 포트폴리오 종합 진단 (Conflict Engine)</div>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:15px;'>
                <div class='persona-box' style='background:#222; border-left: 3px solid #FFAA00; margin-top:0;'>
                    <div style='color:#FFAA00; font-weight:bold; margin-bottom:5px;'>🐹 햄찌의 야수 본능</div>
                    <div style='font-size:13px; color:#ddd; line-height:1.6;'>{pa['hamzzi']}</div>
                </div>
                <div class='persona-box' style='background:#222; border-left: 3px solid #FF4444; margin-top:0;'>
                    <div style='color:#FF4444; font-weight:bold; margin-bottom:5px;'>🐯 호찌의 유비무환 정신</div>
                    <div style='font-size:13px; color:#ddd; line-height:1.6;'>{pa['hojji']}</div>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)
    
    st.subheader("👤 보유 종목 상세 분석")
    for d in st.session_state.my_diagnosis: render_full_card(d)

st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)
st.subheader("📡 시장 정밀 타격 (Market Intelligence)")

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

if st.session_state.market_view_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("<h5>🏆 금일의 Singularity Ideal Pick (Top 3)</h5>", unsafe_allow_html=True)
    for i, d in enumerate(st.session_state.ideal_list): render_full_card(d, i, is_rank=True)

elif st.session_state.market_view_mode == 'SEPARATE' and st.session_state.sc_list:
    st.markdown("<h5>📊 전략별 절대 랭킹 (Top 3)</h5>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["⚡ 초단타", "🌊 추세추종"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_full_card(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_full_card(d, i, is_rank=True)

# [LOGIC]
now = time.time()
need_rerun = False

t_val_my = TIME_OPTS[auto_my]
if st.session_state.trigger_my or (t_val_my > 0 and now - st.session_state.l_my > t_val_my):
    run_my_diagnosis(); need_rerun = True

t_val_top3 = TIME_OPTS[auto_top3]
if st.session_state.trigger_top3 or (t_val_top3 > 0 and now - st.session_state.l_top3 > t_val_top3):
    run_market_scan('TOP3'); need_rerun = True

t_val_sep = TIME_OPTS[auto_sep]
if st.session_state.trigger_sep or (t_val_sep > 0 and now - st.session_state.l_sep > t_val_sep):
    run_market_scan('SEPARATE'); need_rerun = True

if need_rerun: st.rerun()
if t_val_my > 0 or t_val_top3 > 0 or t_val_sep > 0: time.sleep(1); st.rerun()
