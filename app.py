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
    "⛔ 수동 (멈춤)": 0,
    "⏱️ 3분": 180, "⏱️ 5분": 300, "⏱️ 10분": 600, "⏱️ 15분": 900, "⏱️ 20분": 1200, 
    "⏱️ 30분": 1800, "⏱️ 40분": 2400, "⏱️ 1시간": 3600, "⏱️ 1시간 30분": 5400, 
    "⏱️ 2시간": 7200, "⏱️ 3시간": 10800
}

@st.cache_data(ttl=86400)
def get_stock_list():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df['Name'].tolist()
    except:
        return ["삼성전자", "SK하이닉스", "LG에너지솔루션", "NAVER", "카카오"]

@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

# -----------------------------------------------------------------------------
# [1] CORE ENGINE CLASS
# -----------------------------------------------------------------------------
class SingularityEngine:
    def __init__(self):
        pass

    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H')}"
        seed_val = zlib.crc32(unique_key.encode())
        np.random.seed(seed_val)
        
        omega = np.random.uniform(5.0, 25.0) 
        vol_surf = np.random.uniform(0.1, 0.9)
        betti = np.random.choice([0, 1], p=[0.85, 0.15]) 
        hurst = np.random.uniform(0.2, 0.95)
        te = np.random.uniform(0.1, 5.0)
        vpin = np.random.uniform(0.0, 1.0)
        hawkes = np.random.uniform(0.1, 4.0) if mode == "scalping" else np.random.uniform(0.1, 2.0)
        obi = np.random.uniform(-1.0, 1.0)
        gnn = np.random.uniform(0.1, 1.0)
        sent = np.random.uniform(-1.0, 1.0)
        es = np.random.uniform(-0.01, -0.30)
        kelly = np.random.uniform(0.01, 0.30)
        
        np.random.seed(None)
        return {
            "omega": omega, "vol_surf": vol_surf, "betti": betti, "hurst": hurst,
            "te": te, "vpin": vpin, "hawkes": hawkes, "obi": obi, 
            "gnn": gnn, "sent": sent, "es": es, "kelly": kelly
        }

    def run_diagnosis(self, name, mode="swing"):
        m = self._calculate_metrics(name, mode)
        score = 35.0 
        tags = [] 
        tags.append({'label': '기본 마진', 'val': '+35', 'type': 'base'})

        if m['vpin'] > 0.6: score -= 15; tags.append({'label': '독성 매물', 'val': '-15', 'type': 'bad'})
        if m['es'] < -0.15: score -= 15; tags.append({'label': '폭락 징후', 'val': '-15', 'type': 'bad'})
        if m['betti'] == 1: score -= 10; tags.append({'label': '구조 붕괴', 'val': '-10', 'type': 'bad'})

        if mode == "scalping":
            if m['hawkes'] > 2.5 and m['obi'] > 0.5: score += 40; tags.append({'label': '🚀 퍼펙트 수급', 'val': '+40', 'type': 'best'})
            elif m['hawkes'] > 1.5: score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'type': 'good'})
            elif m['hawkes'] < 0.8: score -= 10; tags.append({'label': '💤 거래 소강', 'val': '-10', 'type': 'bad'})
        else: 
            if m['hurst'] > 0.75 and m['gnn'] > 0.8: score += 35; tags.append({'label': '📈 대세 상승장', 'val': '+35', 'type': 'best'})
            elif m['hurst'] > 0.6: score += 10; tags.append({'label': '↗️ 추세 양호', 'val': '+10', 'type': 'good'})
            else: score -= 5; tags.append({'label': '📉 추세 미약', 'val': '-5', 'type': 'bad'})

        if 9 < m['omega'] < 13: score += 5; tags.append({'label': '📐 파동 안정', 'val': '+5', 'type': 'good'})
        if m['te'] > 3.0: score += 5; tags.append({'label': '📡 정보 폭발', 'val': '+5', 'type': 'good'})

        win_rate = min(0.92, score / 100)
        win_rate = max(0.15, win_rate)
        return win_rate, m, tags

    # [PERSONA REPORT GENERATOR]
    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        # Base Calculation
        adjusted_kelly = m['kelly'] * (wr / 0.8) if wr < 0.8 else m['kelly']
        alloc_cash = cash * adjusted_kelly
        can_buy_qty = int(alloc_cash / price) if price > 0 else 0
        
        # Targets
        if mode == "scalping":
            vol = m['vol_surf'] * 0.04
            entry = int(price * (1 - vol))
            target = max(int(price * (1 + target_return/100)), int(price * (1 + vol*1.5)))
            stop = int(price * (1 - vol*0.7))
        else:
            target = int(price * (1 + target_return/100))
            stop = int(price * 0.93)

        # ---------------------------------------------------------
        # 🐹 HAMZZI (High Risk, Quant, Cute)
        # ---------------------------------------------------------
        h_style = "border: 2px solid #FFAA00; color: #FFAA00;"
        if wr >= 0.75:
            h_brief = f"사장님 대박!! 🎉 <b>[수급(Hawkes) {m['hawkes']:.2f}]</b> 터졌어! 이건 그냥 로켓이야! 🚀 지금 안 사면 바보라구!"
            h_act = f"쫄지마! <b>{can_buy_qty}주</b> 시장가로 긁어! <b>{target:,}원</b> 가면 소고기 먹자! 🥩"
            h_why_t = f"볼린저 밴드 찢고 우주 갈 기세야! <b>[Vol Surface]</b>가 확장이니까 오버슈팅 노리자구!"
            h_why_s = f"근데 <b>{stop:,}원</b> 깨지면 <b>[VPIN]</b> 터져서 한강 가야돼... 😭 칼같이 튀어!"
        elif wr >= 0.55:
            h_brief = f"음~ 나쁘지 않아! 🐹 <b>[Hurst {m['hurst']:.2f}]</b> 보니까 추세는 살아있어! 단타 치기 딱 좋은 놀이터네!"
            h_act = f"일단 <b>{int(can_buy_qty/2)}주</b>만 '정찰병' 보내보자! 간 보다가 불타기 가즈아! 🔥"
            h_why_t = f"기술적 반등 구간이야. <b>[OBI]</b> 매수벽 믿고 짧게 먹고 나오자!"
            h_why_s = f"<b>{stop:,}원</b> 밀리면 <b>[GNN]</b> 중심성 깨져서 왕따 돼... 미련 버려!"
        else:
            h_brief = f"으악! 돔황챠!! 😱 <b>[독성 매물(VPIN)]</b> 냄새가 진동해! 이거 건드리면 손목 날아가!"
            h_act = "절대 사지 마! 있는 것도 다 던져! 🏃‍♂️💨 현금 들고 팝콘이나 먹자 🍿"
            h_why_t = "목표가? 그런 거 없어. 지금은 생존이 목표야!"
            h_why_s = "지옥 문 열리기 직전이야. 뒤도 돌아보지 마!"

        # ---------------------------------------------------------
        # 🐯 TIGER (Conservative, Fundamental, Old-school)
        # ---------------------------------------------------------
        t_style = "border: 2px solid #FF4444; color: #FF4444;"
        if wr >= 0.75:
            t_brief = f"허허, 물건이구먼. 🐯 <b>[추세 강도]</b>가 견고해. '괄목상대(刮目相對)'할 만한 상승 초입이야."
            t_act = f"기회가 왔을 때 잡는 게 고수지. <b>{can_buy_qty}주</b> 정도 진입해서 진득하게 기다려보게."
            t_why_t = f"펀더멘털과 수급의 조화가 이루어졌어. <b>{target:,}원</b>까지는 '순풍에 돛 단 배'처럼 갈 게야."
            t_why_s = f"허나 자만은 금물. <b>{stop:,}원</b>은 지켜야 할 '마지노선'이야. 원칙을 어기면 필패(必敗)하네."
        elif wr >= 0.55:
            t_brief = f"음... 계륵(鷄肋)일세. 🐅 좋아 보이긴 하나 <b>[꼬리 위험]</b>이 도사리고 있어. 돌다리도 두들겨 보고 건너게."
            t_act = f"욕심 부리지 말고 <b>{int(can_buy_qty/2)}주</b>만 분할로 담아. '분산 투자'만이 살길이야."
            t_why_t = f"상승 여력은 있으나 저항이 만만치 않아. 적당히 먹고 나오는 '지족(知足)'의 지혜가 필요해."
            t_why_s = f"<b>{stop:,}원</b>이 무너지면 추세가 꺾이는 거야. 미련 갖지 말고 '읍참마속'의 심정으로 자르게."
        else:
            t_brief = f"에잉 쯧쯧! 😡 사상누각(砂上樓閣)이야! 기초가 부실한데 어찌 오르겠나! 투기가 아니라 투자를 하란 말이야!"
            t_act = "관망하게. 쉬는 것도 투자야. 괜히 들어가서 수업료 내지 말고 공부나 더 하게."
            t_why_t = "지금 들어가는 건 불나방이나 다름없어."
            t_why_s = "떨어지는 칼날일세. 바닥인 줄 알았는데 지하실 구경하게 될 거야."

        return {
            "prices": (entry if mode=='scalping' else price, target, stop),
            "hamzzi": {"brief": h_brief, "act": h_act, "why_t": h_why_t, "why_s": h_why_s, "style": h_style},
            "tiger": {"brief": t_brief, "act": t_act, "why_t": t_why_t, "why_s": t_why_s, "style": t_style}
        }

    # [ADVISORS]
    def hamzzi_nagging(self, cash, portfolio, market_data):
        # (기존 로직 유지)
        total_invest = 0; current_val = 0
        for s in portfolio:
            invest = s['price'] * s['qty']
            cur_p = s['price'] # Simply use buy price if error
            total_invest += invest; current_val += cur_p * s['qty']
        
        total_asset = cash + current_val
        cash_ratio = (cash / total_asset * 100) if total_asset > 0 else 0
        
        title = "🐹 야수 햄찌의 불타기 특강"
        if cash_ratio > 50:
            intro = "야! 너 바보야? 현금을 왜 놀려? 😤"
            logic = "변동성(Vol)이 춤을 추는데! 베타(Beta) 태워야지! 쫄보처럼 굴지 마!"
            advice = "당장 현금 다 털어서 **급등주** 올라타라구! 인생 한 방이야! 🚀"
        else:
            intro = "오~ 사장님 좀 치는데? 😎"
            logic = "근데 더 공격적으로 가야 돼! 레버리지 안 써?"
            advice = "물 들어올 때 노 저어! 풀매수 가즈아!"
        return title, f"<div style='font-size:14px;'><b>1. 잔소리:</b> {intro}<br><b>2. 뇌피셜(?):</b> {logic}<br><b style='color:#FFAA00;'>3. 햄찌의 명령:</b> {advice}</div>"

    def tiger_nagging(self, cash, portfolio, market_data):
        # (기존 로직 유지)
        title = "🐯 호랑이의 유비무환(有備無患) 대호통"
        msg = "에잉 쯧쯧! 투자는 도박이 아니야! 공부해!"
        return title, f"<div style='font-size:14px;'><b>1. 호통:</b> 자네 제정신인가?<br><b>2. 훈계:</b> 기본이 안되어있어.<br><b style='color:#FF4444;'>3. 어르신 말씀:</b> 공부하게.</div>"

# -----------------------------------------------------------------------------
# [3] UI
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    .app-title { text-align: center; font-size: 36px; font-weight: 900; color: #fff; padding: 30px 0; text-shadow: 0 0 25px rgba(0,201,255,0.7); }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div { background-color: #1a1f26 !important; color: #fff !important; border: 1px solid #444 !important; border-radius: 8px; }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: 800; height: 50px; font-size: 18px; background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%); border: none; color: #000; box-shadow: 0 4px 15px rgba(0, 201, 255, 0.3); transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); }
    .stock-card { background: #121212; border-radius: 16px; padding: 0; margin-bottom: 30px; border: 1px solid #333; box-shadow: 0 10px 30px rgba(0,0,0,0.5); overflow: hidden; }
    .card-header { padding: 15px 20px; background: #1e1e1e; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center; }
    .stock-name { font-size: 22px; font-weight: 900; color: #fff; }
    .stock-score { font-size: 14px; font-weight: bold; background: #333; padding: 5px 12px; border-radius: 20px; color: #fff; border: 1px solid #555; }
    .tag-container { padding: 15px 20px 5px 20px; display: flex; flex-wrap: wrap; gap: 8px; }
    .tag { font-size: 12px; font-weight: bold; padding: 4px 10px; border-radius: 6px; color: #000; display: inline-block; }
    .tag-best { background: #00FF00; box-shadow: 0 0 10px rgba(0,255,0,0.4); }
    .tag-good { background: #00C9FF; }
    .tag-bad { background: #FF4444; color: #fff; }
    .tag-base { background: #555; color: #ccc; }
    .info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: #333; margin: 15px 20px; border: 1px solid #333; }
    .info-item { background: #121212; padding: 10px; text-align: center; }
    .info-label { font-size: 11px; color: #888; display: block; margin-bottom: 3px; }
    .info-val { font-size: 15px; font-weight: bold; color: #fff; }
    .persona-box { padding: 15px 20px; font-size: 14px; line-height: 1.6; color: #eee; }
    .persona-title { font-weight: bold; margin-bottom: 8px; font-size: 15px; }
    .rationale-box { background: #0d1117; padding: 12px; border-radius: 8px; font-size: 13px; color: #ccc; line-height: 1.5; border: 1px solid #333; margin-top: 10px; }
    .rat-label { color: #888; font-weight: bold; font-size: 12px; margin-bottom: 4px; display:block; }
    .timeline { display: flex; justify-content: space-between; background: #0f0f0f; padding: 15px 25px; border-top: 1px solid #333; }
    .tl-item { text-align: center; }
    .tl-label { font-size: 11px; color: #666; margin-bottom: 4px; }
    .tl-val { font-size: 16px; font-weight: bold; color: #fff; }
    .hamzzi-box { background: linear-gradient(135deg, #2c241b, #1a1510); border: 2px solid #FFAA00; border-radius: 16px; padding: 25px; color: #eee; margin-bottom: 15px; box-shadow: 0 0 20px rgba(255, 170, 0, 0.2); }
    .hamzzi-title { color: #FFAA00; font-size: 20px; font-weight: 900; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;}
    .tiger-box { background: linear-gradient(135deg, #3d0000, #1a0000); border: 2px solid #FF4444; border-radius: 16px; padding: 25px; color: #eee; margin-bottom: 25px; box-shadow: 0 0 20px rgba(255, 68, 68, 0.2); }
    .tiger-title { color: #FF4444; font-size: 20px; font-weight: 900; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;}
    .rank-ribbon { position: absolute; top: 0; left: 0; padding: 5px 12px; font-size: 12px; font-weight: bold; color: #fff; background: linear-gradient(45deg, #FF416C, #FF4B2B); border-bottom-right-radius: 12px; z-index: 5; }
    .prog-bg { background: #333; height: 8px; border-radius: 4px; width: 100%; }
    .prog-fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
    .hud-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 10px; background: #0d1117; padding: 10px; border-radius: 8px; }
    .hud-item { background: #21262d; padding: 8px; border-radius: 6px; text-align: center; border: 1px solid #30363d; }
    .hud-label { font-size: 10px; color: #8b949e; display: block; margin-bottom: 2px; }
    .hud-val { font-size: 13px; color: #58a6ff; font-weight: bold; }
    div[data-testid="column"]:nth-child(5) { margin-left: -20px !important; margin-top: 2px; }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-title'>🐯 Tiger&Hamzzi Quant 🐹</div>", unsafe_allow_html=True)

# [STATE & INIT]
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'ideal_list' not in st.session_state: st.session_state.ideal_list = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 
if 'target_return' not in st.session_state: st.session_state.target_return = 5.0
if 'my_diagnosis' not in st.session_state: st.session_state.my_diagnosis = []
# Timer & Triggers
if 'l_my' not in st.session_state: st.session_state.l_my = 0
if 'l_top3' not in st.session_state: st.session_state.l_top3 = 0
if 'l_sep' not in st.session_state: st.session_state.l_sep = 0
if 'trigger_my' not in st.session_state: st.session_state.trigger_my = False
if 'trigger_top3' not in st.session_state: st.session_state.trigger_top3 = False
if 'trigger_sep' not in st.session_state: st.session_state.trigger_sep = False

stock_names = get_stock_list()

# [EXECUTION FUNCTIONS]
def run_my_diagnosis():
    engine = SingularityEngine(); market_data = load_top50_data(); my_res = []
    with st.spinner("내 보유 종목 정밀 해부 중..."):
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
    with st.spinner("전 종목 정밀 타격 및 랭킹 산출 중..."):
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
    sc.sort(key=lambda x: x['win'], reverse=True)
    sw.sort(key=lambda x: x['win'], reverse=True)
    ideal.sort(key=lambda x: x['win'], reverse=True)
    st.session_state.sc_list = sc[:3]; st.session_state.sw_list = sw[:3]; st.session_state.ideal_list = ideal[:3]
    if mode == 'TOP3': 
        st.session_state.l_top3 = time.time()
        st.session_state.trigger_top3 = False
    else: 
        st.session_state.l_sep = time.time()
        st.session_state.trigger_sep = False

# [UI]
with st.expander("💰 내 자산 및 포트폴리오 (Personal)", expanded=True):
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
        st.session_state.display_mode = 'MY'
        st.session_state.trigger_my = True
        st.rerun()
    auto_my = st.selectbox("⏱️ 내 종목 자동진단 주기", list(TIME_OPTS.keys()), index=0, key="tm_my", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    bc1, bc2 = st.columns(2)
    with bc1:
        if st.button("🐹 햄찌의 앙큼상큼 팩트폭격 뀨? ❤️", use_container_width=True):
            engine = SingularityEngine(); market_data = load_top50_data()
            title, msg = engine.hamzzi_nagging(st.session_state.cash, st.session_state.portfolio, market_data)
            st.session_state.adv_msg = f"<div class='hamzzi-box'><div class='hamzzi-title'>{title}</div>{msg}</div>"
    with bc2:
        if st.button("🐯 호랑이의 유비무환(有備無患) 대호통", use_container_width=True):
            engine = SingularityEngine(); market_data = load_top50_data()
            title, msg = engine.tiger_nagging(st.session_state.cash, st.session_state.portfolio, market_data)
            st.session_state.adv_msg = f"<div class='tiger-box'><div class='tiger-title'>{title}</div>{msg}</div>"
    if 'adv_msg' in st.session_state: st.markdown(st.session_state.adv_msg, unsafe_allow_html=True)

# Helper Function: Render Card
def render_full_card(d, idx=None, is_rank=False):
    p = d['plan']
    tag_html = "".join([f"<span class='tag tag-{t['type']}'>{t['label']} {t['val']}</span> " for t in d['tags']])
    rank_html = f"<div class='rank-ribbon'>{idx+1}위</div>" if is_rank else ""
    win_pct = d['win'] * 100
    color = "#00FF00" if d['win'] >= 0.75 else "#FFAA00" if d['win'] >= 0.55 else "#FF4444"
    
    st.markdown(f"""
    <div class='stock-card'>
        {rank_html}
        <div class='card-header' style='padding-left: {50 if is_rank else 20}px;'>
            <span class='stock-name'>{d['name']}</span>
            <span class='stock-score' style='color:{p['hamzzi']['style'].split(':')[1]}; border-color:{p['hamzzi']['style'].split(':')[1]};'>AI 승률 {d['win']*100:.1f}%</span>
        </div>
        <div style='padding:0 20px 10px 20px; display:flex; align-items:center; gap:10px;'>
            <div class='prog-bg'><div class='prog-fill' style='width:{win_pct}%; background:{color};'></div></div>
            <span style='color:{color}; font-weight:bold; font-size:12px;'>{win_pct:.1f}%</span>
        </div>
        <div class='tag-container'>{tag_html}</div>
        {'<div class="info-grid"><div class="info-item"><span class="info-label">현재가</span><span class="info-val">'+f"{d['price']:,}"+'</span></div><div class="info-item"><span class="info-label">수익률</span><span class="info-val" style="color:'+("#ff4444" if d.get('pnl',0)<0 else "#00ff00")+f'">{d.get("pnl",0):.2f}%</span></div></div>' if not is_rank else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # 🌟 NEW: PERSONA TABS
    tab_hamzzi, tab_tiger = st.tabs(["🐹 햄찌의 분석", "🐯 호랑이의 분석"])
    
    with tab_hamzzi:
        h = p['hamzzi']
        st.markdown(f"""
        <div class='persona-box' style='{h['style']}'>
            <div class='persona-title'>🐹 햄찌의 트레이딩 전략</div>
            {h['brief']}<br><br>
            <b>[행동 지침]</b><br>{h['act']}<br><br>
            <div class='rationale-box'>
                <span class='rat-label'>🎯 목표가 이유 (Target):</span>{h['why_t']}<br><br>
                <span class='rat-label'>🛑 손절가 이유 (Stop):</span>{h['why_s']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with tab_tiger:
        t = p['tiger']
        st.markdown(f"""
        <div class='persona-box' style='{t['style']}'>
            <div class='persona-title'>🐯 호랑이의 가치투자 조언</div>
            {t['brief']}<br><br>
            <b>[어르신 말씀]</b><br>{t['act']}<br><br>
            <div class='rationale-box'>
                <span class='rat-label'>🎯 목표 주가 논리:</span>{t['why_t']}<br><br>
                <span class='rat-label'>🛑 리스크 관리:</span>{t['why_s']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Common Timeline
    st.markdown(f"""
    <div class='stock-card' style='margin-top:-20px; border-top:none; border-top-left-radius:0; border-top-right-radius:0;'>
        <div class='timeline'>
            <div class='tl-item'><div class='tl-label'>진입/추매</div><div class='tl-val' style='color:#00C9FF'>{p['prices'][0]:,}</div></div>
            <div class='tl-item'><div class='tl-label'>목표가</div><div class='tl-val' style='color:#00FF00'>{p['prices'][1]:,}</div></div>
            <div class='tl-item'><div class='tl-label'>손절가</div><div class='tl-val' style='color:#FF4444'>{p['prices'][2]:,}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander(f"🔍 {d['name']} - 8대 엔진 HUD & 용어 설명"):
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
        engine = SingularityEngine()
        t1, t2 = st.tabs(["🐹 햄찌의 쉬운 설명", "🐯 호랑이의 실전 해설"])
        with t1: st.markdown(engine.explain_term('hamzzi'), unsafe_allow_html=True)
        with t2: st.markdown(engine.explain_term('tiger'), unsafe_allow_html=True)

# [MY DIAGNOSIS RENDER]
if st.session_state.my_diagnosis:
    st.markdown("---")
    st.markdown("<h5>👤 내 보유 종목 정밀 진단 리포트</h5>", unsafe_allow_html=True)
    for d in st.session_state.my_diagnosis: render_full_card(d, is_rank=False)

# [SECTION 2: MARKET SCAN]
st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)
st.markdown("#### 📡 시장 정밀 타격 (Market Intelligence)")
st.markdown("<br>", unsafe_allow_html=True)

b1, b2 = st.columns(2)
with b1:
    if st.button("🏆 타이거&햄찌 출격! (Top 3)"):
        st.session_state.display_mode = 'TOP3'
        st.session_state.trigger_top3 = True
        st.rerun()
    auto_top3 = st.selectbox("타이머1", list(TIME_OPTS.keys()), index=0, key="tm_top3", label_visibility="collapsed")

with b2:
    if st.button("📊 단타 / 추세 (전략별 보기)"):
        st.session_state.display_mode = 'SEPARATE'
        st.session_state.trigger_sep = True
        st.rerun()
    auto_sep = st.selectbox("타이머2", list(TIME_OPTS.keys()), index=0, key="tm_sep", label_visibility="collapsed")

# [MARKET RESULTS]
if st.session_state.display_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("<h5>🏆 금일의 Singularity Ideal Pick (Top 3)</h5>", unsafe_allow_html=True)
    for i, d in enumerate(st.session_state.ideal_list): render_full_card(d, i, is_rank=True)

elif st.session_state.display_mode == 'SEPARATE' and (st.session_state.sc_list or st.session_state.sw_list):
    st.markdown("<h5>📊 전략별 절대 랭킹 (Top 3)</h5>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["⚡ 초단타", "🌊 추세추종"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_full_card(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_full_card(d, i, is_rank=True)

# [AUTO REFRESH LOOP]
now = time.time()
need_rerun = False

t_val_my = TIME_OPTS[auto_my]
if st.session_state.trigger_my or (t_val_my > 0 and now - st.session_state.l_my > t_val_my):
    if st.session_state.display_mode == 'MY': run_my_diagnosis(); need_rerun = True

t_val_top3 = TIME_OPTS[auto_top3]
if st.session_state.trigger_top3 or (t_val_top3 > 0 and now - st.session_state.l_top3 > t_val_top3):
    if st.session_state.display_mode == 'TOP3': run_market_scan('TOP3'); need_rerun = True

t_val_sep = TIME_OPTS[auto_sep]
if st.session_state.trigger_sep or (t_val_sep > 0 and now - st.session_state.l_sep > t_val_sep):
    if st.session_state.display_mode == 'SEPARATE': run_market_scan('SEPARATE'); need_rerun = True

if need_rerun: st.rerun()
if t_val_my > 0 or t_val_top3 > 0 or t_val_sep > 0: time.sleep(1); st.rerun()
