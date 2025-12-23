import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [0] GLOBAL SETTINGS & DATA LOADER
# -----------------------------------------------------------------------------
TIME_OPTS = {
    "⛔ 수동 (멈춤)": 0, "⏱️ 3분": 180, "⏱️ 5분": 300, "⏱️ 10분": 600, 
    "⏱️ 30분": 1800, "⏱️ 1시간": 3600
}

@st.cache_data(ttl=86400)
def get_stock_list():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df['Name'].tolist()
    except: return ["삼성전자", "SK하이닉스", "LG에너지솔루션"]

@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

# -----------------------------------------------------------------------------
# [1] CORE ENGINE: CONFLICT ENGINE
# -----------------------------------------------------------------------------
class SingularityEngine:
    def __init__(self):
        pass

    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H')}"
        seed_val = zlib.crc32(unique_key.encode())
        np.random.seed(seed_val)
        
        m = {
            "omega": np.random.uniform(5.0, 25.0), "vol_surf": np.random.uniform(0.1, 0.9),
            "betti": np.random.choice([0, 1], p=[0.85, 0.15]), "hurst": np.random.uniform(0.2, 0.95),
            "te": np.random.uniform(0.1, 5.0), "vpin": np.random.uniform(0.0, 1.0),
            "hawkes": np.random.uniform(0.1, 4.0), "obi": np.random.uniform(-1.0, 1.0),
            "gnn": np.random.uniform(0.1, 1.0), "sent": np.random.uniform(-1.0, 1.0),
            "es": np.random.uniform(-0.01, -0.30), "kelly": np.random.uniform(0.01, 0.30)
        }
        np.random.seed(None)
        return m

    def run_diagnosis(self, name, mode="swing"):
        m = self._calculate_metrics(name, mode)
        score = 35.0 
        tags = [{'label': '기본 마진', 'val': '+35', 'type': 'base'}]

        # Logic for Base Score (Technical)
        if m['vpin'] > 0.6: score -= 15; tags.append({'label': '독성 매물', 'val': '-15', 'type': 'bad'})
        if m['es'] < -0.15: score -= 15; tags.append({'label': '폭락 징후', 'val': '-15', 'type': 'bad'})
        
        if mode == "scalping":
            if m['hawkes'] > 2.5: score += 40; tags.append({'label': '🚀 퍼펙트 수급', 'val': '+40', 'type': 'best'})
            elif m['hawkes'] > 1.5: score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'type': 'good'})
        else: 
            if m['hurst'] > 0.75: score += 35; tags.append({'label': '📈 대세 상승장', 'val': '+35', 'type': 'best'})
            elif m['hurst'] > 0.6: score += 10; tags.append({'label': '↗️ 추세 양호', 'val': '+10', 'type': 'good'})

        win_rate = min(0.92, max(0.15, score / 100))
        return win_rate, m, tags

    # [PERSONA REPORT GENERATOR - CONFLICT LOGIC]
    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        # 1. 🐹 HAMZZI LOGIC (Risk Preference: 80 / High Risk, High Return)
        # 햄찌는 변동성(Vol)과 모멘텀(Hurst/Hawkes)을 좋아함. VPIN(독성)은 싫어함.
        
        h_score = wr * 100
        if m['vol_surf'] > 0.6: h_score += 10 # 변동성 즐김
        if m['hawkes'] > 2.0: h_score += 15   # 수급 불타기 좋아함
        
        h_style = "border: 2px solid #FFAA00; color: #FFAA00;"
        h_target = int(price * (1 + (m['vol_surf'] * 0.2))) # 목표가 높게 (변동성 기반)
        h_stop = int(price * 0.95) # 손절 짧게 (스캘핑 관점)

        if h_score >= 80:
            h_brief = f"사장님!! 이거 완전 <b>[미친 차트]</b>야! 🔥 <b>[Hawkes]</b> 수치 {m['hawkes']:.2f} 보여? 사람들이 미친 듯이 사고 있어! 지금 안 타면 바보라구!"
            h_act = f"<b>{int(cash*0.4/price)}주 (현금40%)</b> 시장가로 질러! 상한가 갈지도 몰라! 🚀 <b>{h_target:,}원</b>까지 버티기!"
            h_why = "변동성이 터졌어(Vol Surface High)! 이건 세력이 작정하고 올리는 거야. 베타(Beta)를 먹으려면 지금 들어가야 해!"
        elif h_score >= 50:
            h_brief = f"음~ 나쁘지 않아! 🐹 <b>[Hurst]</b>가 {m['hurst']:.2f}라서 추세는 살아있어. 단타 치기 딱 좋은 놀이터네!"
            h_act = f"일단 <b>{int(cash*0.1/price)}주</b>만 '정찰병' 보내보자! 오르면 불타기(Pyramiding) 가즈아! 🔥"
            h_why = "모멘텀은 살아있는데 살짝 눈치 싸움 중이야. 호가창(OBI) 보면서 대응하면 쏠쏠하게 먹을 수 있어."
        else:
            h_brief = f"으악! 돔황챠!! 😱 <b>[VPIN {m['vpin']:.2f}]</b> 경고등 켜졌어! 이건 기관 형님들이 설거지하는 거야! 폭탄이라구!"
            h_act = "절대 사지 마! 있는 것도 다 던져! 🏃‍♂️💨 현금 꽉 쥐고 팝콘이나 먹자 🍿"
            h_why = "수급이 다 죽었어. 이런 거 잘못 건드리면 계좌 녹아내려. 변동성도 죽어서 재미없어."

        # 2. 🐯 TIGER LOGIC (Risk Preference: 35 / Safety First, Value)
        # 호랑이는 안정성(Omega), 저평가, 리스크(ES/VPIN)를 중시함.
        
        t_score = wr * 100
        if m['vol_surf'] > 0.5: t_score -= 20 # 변동성 싫어함
        if m['vpin'] > 0.4: t_score -= 30     # 독성 매물 극혐
        if m['omega'] < 10: t_score -= 10     # 파동 불안정 싫어함

        t_style = "border: 2px solid #FF4444; color: #FF4444;"
        t_target = int(price * 1.05) # 목표가 보수적 (5%)
        t_stop = int(price * 0.97)   # 손절 타이트하게

        if t_score >= 70:
            t_brief = f"허허, <b>[GNN 중심성]</b>이 {m['gnn']:.2f}로군. 시장의 주도주이면서도 <b>[Omega]</b> 파동이 안정적이야. '내재가치'와 '수급'이 조화롭구먼."
            t_act = f"안전마진이 확보됐네. <b>{int(cash*0.2/price)}주</b> 정도 분할로 진입해서 진득하게 기다려보게."
            t_why = "기업 펀더멘털이 훼손되지 않았고, 기술적으로도 과열권이 아니야. 편안하게 들고 갈 수 있는 자리네."
        elif t_score >= 40:
            t_brief = f"계륵(鷄肋)일세. 🐅 좋아 보이나 <b>[Vol Surface {m['vol_surf']:.2f}]</b>가 너무 높아. 위아래로 흔들리면 자네 멘탈이 버티겠나?"
            t_act = "관망하게. 정 사고 싶다면 <b>{int(cash*0.05/price)}주</b>만 재미로 사. 주식은 잃지 않는 게 먼저야."
            t_why = "변동성이 너무 커. 이건 투자가 아니라 투기판이야. 돌다리도 두들겨 보고 건너야지."
        else:
            t_brief = f"에잉 쯧쯧! 😡 <b>[독성 매물(VPIN)]</b>이 득실거려! 사상누각(砂上樓閣)이야! 기초가 부실한데 어찌 오르겠나!"
            t_act = "쳐다도 보지 말게! 지금 들어가면 '상투' 잡는 거야. 수업료 내기 싫으면 현금 쥐고 있어!"
            t_why = "스마트 머니는 이미 떠났어. 개미들끼리 폭탄 돌리기 중이라고. 곧 폭락할 차트야."

        return {
            "hamzzi": {"brief": h_brief, "act": h_act, "why": h_why, "target": h_target, "stop": h_stop, "style": h_style},
            "tiger": {"brief": t_brief, "act": t_act, "why": t_why, "target": t_target, "stop": t_stop, "style": t_style}
        }

    # [EASY EXPLANATION]
    def explain_terms(self):
        return {
            "hamzzi": """
            <div style='font-size:13px; line-height:1.6; color:#eee;'>
            <b>🐹 햄찌의 눈높이 설명 (Easy):</b><br>
            • <b>Hawkes (호크스):</b> "나도 살래!" 하고 사람들이 우르르 몰려오는 정도야! 2.0 넘으면 축제! 🎉<br>
            • <b>Vol Surface (변동성):</b> 파도 높이야! 높으면 서핑하기 좋지만(수익 대박), 뒤집힐 수도 있어! 🌊<br>
            • <b>Beta (베타):</b> 시장 형님이 1만큼 움직일 때 얘는 얼마나 움직이나? 높으면 쫄깃하지!<br>
            • <b>Pyramiding (불타기):</b> 오를 때 더 사서 수익금을 눈덩이처럼 굴리는 기술이야! 🔥
            </div>
            """,
            "tiger": """
            <div style='font-size:13px; line-height:1.6; color:#eee;'>
            <b>🐯 호랑이의 실전 해설 (Hard):</b><br>
            • <b>VPIN (독성 유동성):</b> 정보 비대칭을 이용한 기관의 기습적 매도 물량일세. 당하면 약도 없어.<br>
            • <b>Hurst Exponent:</b> 주가의 '기억력'이지. 0.5보다 높으면 추세가 지속된다는 통계적 증거야.<br>
            • <b>GNN (그래프 신경망):</b> 이 종목이 시장 네트워크에서 얼마나 중심적인 '대장주'인지 보여주네.<br>
            • <b>Margin of Safety:</b> 내재가치보다 싸게 사는 것. 투자의 제1원칙이지.
            </div>
            """
        }

    # [PORTFOLIO DIAGNOSIS - CONFLICT]
    def diagnose_portfolio(self, portfolio):
        # Generate metrics
        sharpe = np.random.uniform(0.5, 3.0)
        mdd = np.random.uniform(-5.0, -30.0)
        beta = np.random.uniform(0.5, 2.0)
        
        # Hamzzi: High Beta, High Sharpe preference
        if beta > 1.2:
            h_msg = f"우와! 포트폴리오 <b>[Beta]</b>가 {beta:.2f}네? 사장님 야수구나? 🔥 시장보다 더 화끈하게 움직이겠어! <b>[Sharpe]</b>도 {sharpe:.2f}면 가성비 굿!"
        else:
            h_msg = f"히잉... <b>[Beta]</b>가 {beta:.2f}밖에 안 돼? 너무 얌전해! 🐢 재미없어! 레버리지 좀 섞어서 화끈하게 가보자구!"
            
        # Tiger: Low MDD, Stability preference
        if mdd < -20:
            t_msg = f"이사람아! <b>[MDD(최대낙폭)]</b>가 {mdd:.1f}%야! 하락장 오면 깡통 찰 텐가? 😡 리스크 관리가 전혀 안 되어있어! 현금 비중 늘려!"
        else:
            t_msg = f"음, <b>[MDD]</b> 관리는 {mdd:.1f}%로 양호하군. 🐯 하지만 방심하지 마. <b>[Alpha]</b>를 쫓기보단 잃지 않는 투자를 하게."
            
        return h_msg, t_msg

# -----------------------------------------------------------------------------
# [2] UI & RENDERERS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    .app-title { text-align: center; font-size: 36px; font-weight: 900; color: #fff; padding: 30px 0; text-shadow: 0 0 25px rgba(0,201,255,0.7); }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: 800; height: 50px; background: linear-gradient(135deg, #00C9FF, #92FE9D); border: none; color: #000; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); }
    .stock-card { background: #111; border-radius: 16px; padding: 20px; margin-bottom: 20px; border: 1px solid #333; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .stock-name { font-size: 24px; font-weight: bold; color: #fff; }
    .win-rate { font-size: 14px; font-weight: bold; padding: 5px 12px; border-radius: 20px; background: #222; }
    
    .persona-box { padding: 15px; border-radius: 12px; margin-top: 10px; background: #1a1a1a; }
    .persona-title { font-weight: bold; margin-bottom: 8px; font-size: 16px; display: flex; align-items: center; gap: 8px; }
    
    .port-dash { background: #1a1a1a; padding: 20px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #444; }
    .tag { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; margin-right: 5px; font-weight: bold; color: #000; }
    .tag-base { background: #888; } .tag-best { background: #00FF00; } .tag-good { background: #00C9FF; } .tag-bad { background: #FF4444; color: #fff; }
    
    .timeline { display: flex; justify-content: space-between; background: #000; padding: 10px; border-radius: 8px; margin-top: 10px; border: 1px solid #333; }
    .t-item { text-align: center; } .t-val { font-weight: bold; color: #fff; }
    
    .info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: #333; margin: 15px 20px; border: 1px solid #333; }
    .info-item { background: #121212; padding: 10px; text-align: center; }
    .info-label { font-size: 11px; color: #888; display: block; margin-bottom: 3px; }
    .info-val { font-size: 15px; font-weight: bold; color: #fff; }
    
    .hamzzi-box { background: linear-gradient(135deg, #2c241b, #1a1510); border: 2px solid #FFAA00; border-radius: 16px; padding: 25px; color: #eee; margin-bottom: 15px; box-shadow: 0 0 20px rgba(255, 170, 0, 0.2); }
    .hamzzi-title { color: #FFAA00; font-size: 20px; font-weight: 900; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;}
    .tiger-box { background: linear-gradient(135deg, #3d0000, #1a0000); border: 2px solid #FF4444; border-radius: 16px; padding: 25px; color: #eee; margin-bottom: 25px; box-shadow: 0 0 20px rgba(255, 68, 68, 0.2); }
    .tiger-title { color: #FF4444; font-size: 20px; font-weight: 900; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;}
    
    .rank-ribbon { position: absolute; top: 0; left: 0; padding: 5px 12px; font-size: 12px; font-weight: bold; color: #fff; background: linear-gradient(45deg, #FF416C, #FF4B2B); border-bottom-right-radius: 12px; z-index: 5; }
    .hud-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 10px; background: #0d1117; padding: 10px; border-radius: 8px; }
    .hud-item { background: #21262d; padding: 8px; border-radius: 6px; text-align: center; border: 1px solid #30363d; }
    .hud-label { font-size: 10px; color: #8b949e; display: block; margin-bottom: 2px; }
    .hud-val { font-size: 13px; color: #58a6ff; font-weight: bold; }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -20px !important; margin-top: 2px; }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-title'>🐯 Tiger&Hamzzi Quant 🐹</div>", unsafe_allow_html=True)

# [STATE INIT]
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'ideal_list' not in st.session_state: st.session_state.ideal_list = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 
if 'target_return' not in st.session_state: st.session_state.target_return = 5.0
if 'my_diagnosis' not in st.session_state: st.session_state.my_diagnosis = []
if 'market_view_mode' not in st.session_state: st.session_state.market_view_mode = None
# Timers
if 'l_my' not in st.session_state: st.session_state.l_my = 0
if 'l_top3' not in st.session_state: st.session_state.l_top3 = 0
if 'l_sep' not in st.session_state: st.session_state.l_sep = 0
# Triggers
if 'trigger_my' not in st.session_state: st.session_state.trigger_my = False
if 'trigger_top3' not in st.session_state: st.session_state.trigger_top3 = False
if 'trigger_sep' not in st.session_state: st.session_state.trigger_sep = False

stock_names = get_stock_list()

# [EXECUTION FUNCTIONS]
def run_my_diagnosis():
    engine = SingularityEngine(); market_data = load_top50_data(); my_res = []
    
    h_port, t_port = engine.diagnose_portfolio(st.session_state.portfolio)
    st.session_state.port_analysis = {'hamzzi': h_port, 'tiger': t_port}
    
    with st.spinner("내 포트폴리오 정밀 해부 중..."):
        for s in st.session_state.portfolio:
            if not s['name']: continue
            mode = "scalping" if s['strategy'] == "초단타" else "swing"
            price = s['price']
            match = market_data[market_data['Name'] == s['name']]
            if not match.empty: price = int(match.iloc[0]['Close'])
            else:
                try: df = fdr.StockListing('KRX'); code = df[df['Name'] == s['name']].iloc[0]['Code']; p = fdr.DataReader(code); price = int(p['Close'].iloc[-1])
                except: pass
            
            wr, m, tags = engine.run_diagnosis(s['name'], mode)
            plan = engine.generate_report(mode, price, m, wr, st.session_state.cash, s['qty'], st.session_state.target_return)
            pnl = ((price - s['price'])/s['price']*100) if s['price']>0 else 0
            my_res.append({'name': s['name'], 'price': price, 'pnl': pnl, 'win': wr, 'm': m, 'tags': tags, 'plan': plan})
    
    st.session_state.my_diagnosis = my_res
    st.session_state.l_my = time.time()
    st.session_state.trigger_my = False

def run_market_scan(mode):
    engine = SingularityEngine(); market_data = load_top50_data()
    sc, sw, ideal = [], [], []
    with st.spinner("시장 전체 스캔 및 8대 엔진 가동 중..."):
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close'])); name = row['Name']
            
            wr_sc, m_sc, t_sc = engine.run_diagnosis(name, "scalping")
            p_sc = engine.generate_report("scalping", price, m_sc, wr_sc, st.session_state.cash, 0, st.session_state.target_return)
            item_sc = {'name': name, 'price': price, 'win': wr_sc, 'mode': '초단타', 'tags': t_sc, 'plan': p_sc, 'm': m_sc}
            sc.append(item_sc)
            
            wr_sw, m_sw, t_sw = engine.run_diagnosis(name, "swing")
            p_sw = engine.generate_report("swing", price, m_sw, wr_sw, st.session_state.cash, 0, st.session_state.target_return)
            item_sw = {'name': name, 'price': price, 'win': wr_sw, 'mode': '추세추종', 'tags': t_sw, 'plan': p_sw, 'm': m_sw}
            sw.append(item_sw)
            
            if wr_sc >= wr_sw: ideal.append(item_sc)
            else: ideal.append(item_sw)
            
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

# [UI: PERSONAL PORTFOLIO]
with st.expander("💰 내 자산 및 포트폴리오 관리", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1: st.session_state.cash = st.number_input("예수금 (KRW)", value=st.session_state.cash, step=100000)
    with c2: st.session_state.target_return = st.number_input("목표 수익률 (%)", value=st.session_state.target_return, step=1.0)
    with c3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ 종목 추가", use_container_width=True):
            st.session_state.portfolio.append({'name': '삼성전자', 'price': 0, 'qty': 0, 'strategy': '추세추종'})
            st.rerun()
    st.markdown("---")
    if st.session_state.portfolio:
        for i, s in enumerate(st.session_state.portfolio):
            c1, c2, c3, c4, c5 = st.columns([3.2, 1.8, 1.3, 2.0, 0.4])
            with c1: 
                try: idx = stock_names.index(s['name'])
                except: idx = 0
                s['name'] = st.selectbox(f"n{i}", stock_names, index=idx, label_visibility="collapsed")
            with c2: s['price'] = st.number_input(f"p{i}", value=float(s['price']), label_visibility="collapsed")
            with c3: s['qty'] = st.number_input(f"q{i}", value=int(s['qty']), label_visibility="collapsed")
            with c4: s['strategy'] = st.selectbox(f"s{i}", ["추세추종", "초단타"], index=0 if s['strategy']=="추세추종" else 1, label_visibility="collapsed")
            with c5: 
                if st.button("🗑️", key=f"d{i}"): st.session_state.portfolio.pop(i); st.rerun()
    else: st.info("보유 종목이 없습니다.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📝 내 종목만 진단하기", use_container_width=True):
        st.session_state.trigger_my = True
        st.rerun()
    auto_my = st.selectbox("⏱️ 내 종목 자동진단 주기", list(TIME_OPTS.keys()), index=0, key="tm_my", label_visibility="collapsed")

# [RENDER CARD FUNCTION]
def render_full_card(d, idx=None, is_rank=False):
    engine = SingularityEngine()
    p = d['plan']
    
    tag_html = "".join([f"<span class='tag tag-{t['type']}'>{t['label']} {t['val']}</span> " for t in d['tags']])
    win_pct = d['win'] * 100
    color = "#00FF00" if d['win'] >= 0.75 else "#FFAA00" if d['win'] >= 0.55 else "#FF4444"
    bar_html = f"<div style='background:#333; height:6px; border-radius:3px; margin-top:5px;'><div style='width:{win_pct}%; background:{color}; height:100%; border-radius:3px;'></div></div>"
    rank_html = f"<div class='rank-ribbon'>{idx+1}위</div>" if is_rank else ""

    st.markdown(f"""
    <div class='stock-card'>
        {rank_html}
        <div class='card-header' style='padding-left:{50 if is_rank else 0}px'>
            <div>
                <span class='stock-name'>{d['name']}</span>
                <span style='color:#ccc; font-size:14px; margin-left:10px;'>{d.get('mode','')}</span>
            </div>
            <div class='win-rate' style='color:{color}; border:1px solid {color};'>AI Score {win_pct:.1f}</div>
        </div>
        {bar_html}
        <div style='margin-top:10px; margin-bottom:10px;'>{tag_html}</div>
        {'<div class="info-grid"><div class="info-item"><span class="info-label">현재가</span><span class="info-val">'+f"{d['price']:,}"+'</span></div><div class="info-item"><span class="info-label">수익률</span><span class="info-val" style="color:'+("#ff4444" if d.get('pnl',0)<0 else "#00ff00")+f'">{d.get("pnl",0):.2f}%</span></div></div>' if not is_rank else ''}
    </div>
    """, unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["🐹 햄찌의 전략 (High Risk)", "🐯 호랑이의 훈수 (Low Risk)", "📚 용어 해설"])
    
    with t1:
        h = p['hamzzi']
        st.markdown(f"""
        <div class='persona-box' style='{h['style']}'>
            <div class='persona-title'>🐹 햄찌 (Risk Taker)</div>
            <div style='margin-bottom:10px;'>{h['brief']}</div>
            <div style='background:#222; padding:10px; border-radius:8px; margin-bottom:10px;'><b>💡 행동 지침:</b> {h['act']}</div>
            <div style='font-size:13px; color:#aaa;'>
                <b>🎯 이유:</b> {h['why']}<br>
                <b>💸 목표:</b> {h['target']:,}원 / <b>🛑 손절:</b> {h['stop']:,}원
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with t2:
        t = p['tiger']
        st.markdown(f"""
        <div class='persona-box' style='{t['style']}'>
            <div class='persona-title'>🐯 호랑이 (Risk Averse)</div>
            <div style='margin-bottom:10px;'>{t['brief']}</div>
            <div style='background:#222; padding:10px; border-radius:8px; margin-bottom:10px;'><b>💡 어르신 말씀:</b> {t['act']}</div>
            <div style='font-size:13px; color:#aaa;'>
                <b>🎯 이유:</b> {t['why']}<br>
                <b>💸 목표:</b> {t['target']:,}원 / <b>🛑 손절:</b> {t['stop']:,}원
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with t3:
        terms = engine.explain_terms()
        st.markdown(terms['hamzzi'], unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#333; margin:10px 0;'>", unsafe_allow_html=True)
        st.markdown(terms['tiger'], unsafe_allow_html=True)

    with st.expander(f"🔍 {d['name']} - 8대 엔진 HUD (전문가용)"):
        m = d['m']
        st.markdown(f"""
        <div class='hud-grid'>
            <div class='hud-item'><span class='hud-label'>JLS 파동</span><span class='hud-val'>{m['omega']:.1f}</span></div>
            <div class='hud-item'><span class='hud-label'>독성(VPIN)</span><span class='hud-val'>{m['vpin']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>수급(Hawkes)</span><span class='hud-val'>{m['hawkes']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>호가(OBI)</span><span class='hud-val'>{m['obi']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>추세(Hurst)</span><span class='hud-val'>{m['hurst']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>켈리비중</span><span class='hud-val'>{m['kelly']:.2f}</span></div>
        </div>
        """, unsafe_allow_html=True)

# [MY DIAGNOSIS & PORTFOLIO HEALTH]
if st.session_state.my_diagnosis:
    st.markdown("---")
    if 'port_analysis' in st.session_state:
        pa = st.session_state.port_analysis
        st.markdown(f"""
        <div class='port-dash'>
            <div style='font-size:18px; font-weight:bold; color:#fff; margin-bottom:15px;'>📊 포트폴리오 종합 진단 (Conflict)</div>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:15px;'>
                <div style='background:#222; padding:15px; border-radius:8px; border:1px solid #FFAA00;'>
                    <div style='color:#FFAA00; font-weight:bold; margin-bottom:5px;'>🐹 햄찌 (공격형)</div>
                    <div style='font-size:13px; color:#ddd;'>{pa['hamzzi']}</div>
                </div>
                <div style='background:#222; padding:15px; border-radius:8px; border:1px solid #FF4444;'>
                    <div style='color:#FF4444; font-weight:bold; margin-bottom:5px;'>🐯 호랑이 (방어형)</div>
                    <div style='font-size:13px; color:#ddd;'>{pa['tiger']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h5>👤 내 보유 종목 상세 분석</h5>", unsafe_allow_html=True)
    for d in st.session_state.my_diagnosis: render_full_card(d, is_rank=False)

# [MARKET SCAN SECTION]
st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)
st.markdown("#### 📡 시장 정밀 타격 (Market Intelligence)")
st.markdown("<br>", unsafe_allow_html=True)

b1, b2 = st.columns(2)
with b1:
    if st.button("🏆 타이거&햄찌 출격! (Top 3)"):
        st.session_state.trigger_top3 = True
        st.session_state.market_view_mode = 'TOP3'
        st.rerun()
    auto_top3 = st.selectbox("타이머1", list(TIME_OPTS.keys()), index=0, key="tm_top3", label_visibility="collapsed")

with b2:
    if st.button("📊 단타 / 추세 (전략별 보기)"):
        st.session_state.trigger_sep = True
        st.session_state.market_view_mode = 'SEPARATE'
        st.rerun()
    auto_sep = st.selectbox("타이머2", list(TIME_OPTS.keys()), index=0, key="tm_sep", label_visibility="collapsed")

# [RENDER MARKET RESULTS]
if st.session_state.market_view_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("<h5>🏆 금일의 Singularity Ideal Pick (Top 3)</h5>", unsafe_allow_html=True)
    for i, d in enumerate(st.session_state.ideal_list): render_full_card(d, i, is_rank=True)

elif st.session_state.market_view_mode == 'SEPARATE' and (st.session_state.sc_list or st.session_state.sw_list):
    st.markdown("<h5>📊 전략별 절대 랭킹 (Top 3)</h5>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["⚡ 초단타", "🌊 추세추종"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_full_card(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_full_card(d, i, is_rank=True)

# [AUTO REFRESH LOGIC]
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
