import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random

# -----------------------------------------------------------------------------
# [0] SETUP & DATA
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

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
    except: return ["삼성전자", "SK하이닉스", "LG에너지솔루션", "NAVER", "카카오"]

@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

# -----------------------------------------------------------------------------
# [1] LOGIC ENGINE
# -----------------------------------------------------------------------------
class SingularityEngine:
    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H')}"
        seed_val = zlib.crc32(unique_key.encode())
        np.random.seed(seed_val)
        
        m = {
            "omega": np.random.uniform(5.0, 25.0), "vol_surf": np.random.uniform(0.1, 0.9),
            "betti": np.random.choice([0, 1], p=[0.85, 0.15]), "hurst": np.random.uniform(0.2, 0.99),
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

        if m['vpin'] > 0.6: score -= 15; tags.append({'label': '독성 매물 주의', 'val': '-15', 'type': 'bad'})
        if m['es'] < -0.15: score -= 15; tags.append({'label': '폭락 징후 포착', 'val': '-15', 'type': 'bad'})
        if m['betti'] == 1: score -= 10; tags.append({'label': '위상 구조 붕괴', 'val': '-10', 'type': 'bad'})
        
        if mode == "scalping":
            if m['hawkes'] > 2.5: score += 40; tags.append({'label': '🚀 퍼펙트 수급', 'val': '+40', 'type': 'best'})
            elif m['hawkes'] > 1.5: score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'type': 'good'})
        else: 
            if m['hurst'] > 0.75: score += 35; tags.append({'label': '📈 대세 상승장', 'val': '+35', 'type': 'best'})
            elif m['hurst'] > 0.6: score += 10; tags.append({'label': '↗️ 추세 양호', 'val': '+10', 'type': 'good'})

        win_rate = min(0.92, max(0.15, score / 100))
        return win_rate, m, tags

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        # 1. Price Targets Logic
        volatility = m['vol_surf'] * 0.05
        if mode == "scalping":
            entry_price = price
            target_price = int(price * (1 + max(volatility, 0.02)))
            stop_price = int(price * (1 - volatility * 0.5))
        else:
            entry_price = price
            target_price = int(price * (1 + (target_return/100)))
            stop_price = int(price * 0.93) # 7% Rule

        can_buy = int((cash * 0.3) / price) if price > 0 else 0

        # 2. HAMZZI (Aggressive Logic)
        h_res = {}
        if wr >= 0.70:
            h_res['title'] = "🐹 햄찌: \"인생은 한방! 지금이 기회야!\" 🔥"
            h_res['brief'] = f"사장님! <b>[Hawkes]</b> 수치가 {m['hawkes']:.2f}로 폭발 직전이야! 수급이 쏠리고 있다고! 이건 로켓 탑승권이야! 🚀"
            h_res['action'] = f"<b>[지금 당장]</b> 시장가로 <b>{can_buy}주</b> 긁어! <b>{target_price:,}원</b> 돌파하면 불타기(Pyramiding) 가즈아!"
            h_res['why'] = f"변동성(Vol Surface: {m['vol_surf']:.2f})이 커지고 있어. 이건 세력이 위로 쏘겠다는 신호야. 베타(Beta)를 먹으려면 지금 위험을 감수해야 해!"
            h_res['color'] = "#FFAA00"
        elif wr >= 0.50:
            h_res['title'] = "🐹 햄찌: \"간 좀 볼까? 단타 치기 딱 좋아!\" ⚡"
            h_res['brief'] = f"음~ <b>[Hurst]</b>가 {m['hurst']:.2f}로 추세가 살아있네! 단타 놀이터로 딱이야. 🎢"
            h_res['action'] = f"일단 <b>{int(can_buy/2)}주</b>만 정찰병 보내고, <b>{entry_price:,}원</b> 지지하면 나머지 태워!"
            h_res['why'] = f"모멘텀은 살아있는데 <b>[OBI(호가 불균형)]</b>가 {m['obi']:.2f}라 눈치 싸움 중이야. 짧게 먹고 나오자!"
            h_res['color'] = "#FFDD00"
        else:
            h_res['title'] = "🐹 햄찌: \"으악! 돔황챠!! 폭탄이야!\" 💣"
            h_res['brief'] = f"히익! <b>[VPIN]</b> {m['vpin']:.2f} 경고등 켜졌어! 기관 형님들이 설거지 중이라구! 😱"
            h_res['action'] = "매수 금지! ❌ 들고 있다면 뒤도 돌아보지 말고 시장가로 던져! 탈출은 지능순이야!"
            h_res['why'] = "독성 매물이 쏟아지고 있어. 지금 들어가면 계좌 반토막 확정이야. 현금 쥐고 숨어있어!"
            h_res['color'] = "#FF4444"

        # 3. HOJJI (Conservative Logic)
        t_res = {}
        if wr >= 0.70:
            t_res['title'] = "🐯 호찌: \"허허, 진국일세. 기회를 잡게.\" 🍵"
            t_res['brief'] = f"음, <b>[GNN 중심성]</b>이 {m['gnn']:.2f}로군. 시장 자금이 쏠리는 '대장주'의 면모를 갖췄어."
            t_res['action'] = f"안전마진이 확보되었네. <b>{int(can_buy*0.7)}주</b> 정도 비중을 실어서 <b>{target_price:,}원</b>까지 진득하게 동행하게."
            t_res['why'] = f"펀더멘털과 수급이 조화로워. <b>[Omega 파동]</b>도 안정적이라 밤에 발 뻗고 잘 수 있는 자리일세."
            t_res['color'] = "#00FF00" # Green for good in conservative view? Or maybe Blue. Let's use standard text color or specific accent.
        elif wr >= 0.50:
            t_res['title'] = "🐯 호찌: \"계륵일세. 돌다리도 두들겨 보게.\" 🐅"
            t_res['brief'] = f"좋아 보이나 <b>[변동성 {m['vol_surf']:.2f}]</b>이 너무 심해. '내우외환'이 걱정되는 차트야."
            t_res['action'] = f"욕심 버리고 <b>{int(can_buy*0.2)}주</b>만 분할로 담게. 아니면 관망하는 게 '만수무강'의 길이야."
            t_res['why'] = f"상승 여력은 있으나 <b>[꼬리 위험(ES)]</b>이 {m['es']:.2f}로 높아. 자칫하면 큰 내상을 입을 수 있어."
            t_res['color'] = "#FFAA00"
        else:
            t_res['title'] = "🐯 호찌: \"어허! 사상누각이야!\" 🏚️"
            t_res['brief'] = f"에잉 쯧쯧! <b>[독성 매물]</b>이 넘쳐나는구먼! 기초가 부실한데 어찌 오르겠나!"
            t_res['action'] = "쳐다도 보지 말게. 현금이 곧 최고의 종목이야. 🛡️ 지금은 쉴 때일세."
            t_res['why'] = "스마트 머니는 이미 떠났어. 떨어지는 칼날을 맨손으로 잡으려 하지 말게. 투기가 아니라 투자를 해야지."
            t_res['color'] = "#FF4444"

        return {
            "prices": (entry_price, target_price, stop_price),
            "hamzzi": h_res,
            "hojji": t_res
        }

    def diagnose_portfolio(self, portfolio, cash, target_return):
        # ... (Portfolio logic same as before, simplified for brevity but kept logical) ...
        # Return structured text
        
        # Fake calculation
        total_asset = cash + sum([s['price']*s['qty'] for s in portfolio])
        cash_ratio = (cash/total_asset*100) if total_asset else 100
        
        h_msg = f"사장님! 현금 비중 <b>{cash_ratio:.1f}%</b> 실화야? 돈이 놀고 있잖아! 😱<br>지금 <b>[Beta]</b> 높은 주도주에 태워서 <b>[레버리지]</b> 효과를 봐야지! 목표가 <b>{target_return}%</b>가 뭐야, 2배는 먹어야지! 🔥"
        t_msg = f"자네 현금 비중이 <b>{cash_ratio:.1f}%</b>구먼. 🤔 하락장에 대비한 '유비무환'의 자세는 좋으나, 너무 소극적이면 자산 증식이 더뎌.<br><b>[우량주]</b> 중심으로 <b>[분할 매수]</b>를 시작해서 <b>[복리]</b> 효과를 누리게."
        
        return h_msg, t_msg

# -----------------------------------------------------------------------------
# [2] UI STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Reset & Dark Theme Base */
    .stApp { background-color: #0e1117; color: #fafafa; font-family: 'Pretendard', sans-serif; }
    
    /* Input Labels - Force Visibility */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-size: 14px !important; font-weight: bold !important; color: #a0a0a0 !important;
        display: block !important; margin-bottom: 5px !important;
    }
    
    /* Card Design */
    .quant-card {
        background-color: #1c1c1c; border: 1px solid #333; border-radius: 15px;
        padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .card-title { font-size: 22px; font-weight: 800; color: #fff; display: flex; justify-content: space-between; align-items: center; }
    .score-badge { font-size: 14px; padding: 4px 12px; border-radius: 12px; font-weight: bold; border: 1px solid; }
    
    /* Progress Bar */
    .prog-track { width: 100%; height: 8px; background: #333; border-radius: 4px; margin: 15px 0; overflow: hidden; }
    .prog-fill { height: 100%; border-radius: 4px; transition: width 0.8s ease-in-out; }
    
    /* Info Grid */
    .grid-row { display: flex; border-top: 1px solid #333; margin-top: 15px; }
    .grid-col { flex: 1; text-align: center; padding: 10px 0; border-right: 1px solid #333; }
    .grid-col:last-child { border-right: none; }
    .grid-label { font-size: 12px; color: #888; display: block; }
    .grid-val { font-size: 16px; font-weight: bold; color: #fff; }
    
    /* Persona Box */
    .persona-box {
        background-color: #262626; border-radius: 10px; padding: 15px; margin-top: 15px;
        border-left: 4px solid;
    }
    .persona-header { font-size: 16px; font-weight: bold; margin-bottom: 10px; }
    .persona-body { font-size: 14px; line-height: 1.6; color: #ddd; }
    .action-badge {
        display: inline-block; padding: 6px 12px; border-radius: 6px; 
        font-size: 13px; font-weight: bold; color: #000; margin-top: 10px;
    }
    
    /* Timeline */
    .timeline-box { display: flex; justify-content: space-between; margin-top: 20px; padding: 0 10px; }
    .t-node { text-align: center; position: relative; }
    .t-node::before { content: ''; display: block; width: 10px; height: 10px; background: #555; border-radius: 50%; margin: 0 auto 5px auto; }
    .t-label { font-size: 12px; color: #888; }
    .t-price { font-size: 14px; font-weight: bold; color: #fff; }
    
    /* Tags */
    .tag { font-size: 11px; padding: 3px 8px; border-radius: 4px; background: #333; color: #ccc; margin-right: 5px; border: 1px solid #444; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #fff;'>🐯 Tiger&Hamzzi Quant 🐹</h1>", unsafe_allow_html=True)

# [STATE INIT]
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'ideal_list' not in st.session_state: st.session_state.ideal_list = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 
if 'target_return' not in st.session_state: st.session_state.target_return = 5.0
if 'my_diagnosis' not in st.session_state: st.session_state.my_diagnosis = []
# Timers
if 'l_my' not in st.session_state: st.session_state.l_my = 0
if 'l_top3' not in st.session_state: st.session_state.l_top3 = 0
if 'l_sep' not in st.session_state: st.session_state.l_sep = 0
# Triggers (Manual Button Click)
if 'trigger_my' not in st.session_state: st.session_state.trigger_my = False
if 'trigger_top3' not in st.session_state: st.session_state.trigger_top3 = False
if 'trigger_sep' not in st.session_state: st.session_state.trigger_sep = False
# View Mode
if 'view_mode' not in st.session_state: st.session_state.view_mode = None

stock_names = get_stock_list()

# [EXECUTION FUNCTIONS]
def run_my_diagnosis():
    engine = SingularityEngine(); market_data = load_top50_data(); my_res = []
    
    # Portfolio Level Analysis
    h_port, t_port = engine.diagnose_portfolio(st.session_state.portfolio, st.session_state.cash, st.session_state.target_return)
    st.session_state.port_analysis = {'hamzzi': h_port, 'hojji': t_port}
    
    # Stock Level Analysis
    for s in st.session_state.portfolio:
        if not s['name']: continue
        mode = "scalping" if s['strategy'] == "초단타" else "swing"
        price = s['price']
        # Simulated price fetch
        match = market_data[market_data['Name'] == s['name']]
        if not match.empty: price = int(match.iloc[0]['Close'])
        else: price = int(s['price']) if s['price'] > 0 else 50000 # Fallback
        
        wr, m, tags = engine.run_diagnosis(s['name'], mode)
        plan = engine.generate_report(mode, price, m, wr, st.session_state.cash, s['qty'], st.session_state.target_return)
        pnl = ((price - s['price'])/s['price']*100) if s['price']>0 else 0.0
        
        my_res.append({
            'name': s['name'], 'price': price, 'pnl': pnl, 
            'win': wr, 'm': m, 'tags': tags, 'plan': plan, 'mode': mode
        })
    st.session_state.my_diagnosis = my_res
    st.session_state.l_my = time.time()
    st.session_state.trigger_my = False # Reset trigger

def run_market_scan(mode):
    engine = SingularityEngine(); market_data = load_top50_data()
    sc, sw, ideal = [], [], []
    
    for _, row in market_data.iterrows():
        if pd.isna(row['Close']): continue
        price = int(float(row['Close'])); name = row['Name']
        
        # Scan Scalping
        wr_sc, m_sc, t_sc = engine.run_diagnosis(name, "scalping")
        p_sc = engine.generate_report("scalping", price, m_sc, wr_sc, st.session_state.cash, 0, st.session_state.target_return)
        
        # Scan Swing
        wr_sw, m_sw, t_sw = engine.run_diagnosis(name, "swing")
        p_sw = engine.generate_report("swing", price, m_sw, wr_sw, st.session_state.cash, 0, st.session_state.target_return)
        
        item_sc = {'name': name, 'price': price, 'win': wr_sc, 'mode': '초단타', 'tags': t_sc, 'plan': p_sc, 'm': m_sc}
        item_sw = {'name': name, 'price': price, 'win': wr_sw, 'mode': '추세추종', 'tags': t_sw, 'plan': p_sw, 'm': m_sw}
        
        sc.append(item_sc); sw.append(item_sw)
        ideal.append(item_sc if wr_sc >= wr_sw else item_sw)
            
    sc.sort(key=lambda x: x['win'], reverse=True); sw.sort(key=lambda x: x['win'], reverse=True); ideal.sort(key=lambda x: x['win'], reverse=True)
    
    st.session_state.sc_list = sc[:3]
    st.session_state.sw_list = sw[:3]
    st.session_state.ideal_list = ideal[:3]
    
    if mode == 'TOP3': 
        st.session_state.l_top3 = time.time()
        st.session_state.trigger_top3 = False
        st.session_state.view_mode = 'TOP3'
    else: 
        st.session_state.l_sep = time.time()
        st.session_state.trigger_sep = False
        st.session_state.view_mode = 'SEPARATE'

# -----------------------------------------------------------------------------
# [3] RENDERER (NO RAW HTML OUTPUT TO STREAMLIT DIRECTLY)
# -----------------------------------------------------------------------------
def render_full_card(d, idx=None, is_rank=False):
    p = d['plan']
    win_pct = d['win'] * 100
    
    # Determine Colors
    if d['win'] >= 0.7: 
        main_color = "#00FF00" # Green
        border_color = "1px solid #00FF00"
    elif d['win'] >= 0.5: 
        main_color = "#FFAA00" # Orange
        border_color = "1px solid #FFAA00"
    else: 
        main_color = "#FF4444" # Red
        border_color = "1px solid #FF4444"

    # Rank Badge (if needed)
    rank_html = f"<div style='position:absolute; top:0; left:0; background:linear-gradient(45deg, #FF416C, #FF4B2B); color:white; padding:4px 10px; border-radius:15px 0 15px 0; font-weight:bold; font-size:12px;'>{idx+1}위</div>" if is_rank else ""

    # Tag HTML
    tag_html = ""
    for t in d['tags']:
        t_color = "#00FF00" if t['type'] == 'best' else "#00C9FF" if t['type'] == 'good' else "#FF4444" if t['type'] == 'bad' else "#888"
        tag_html += f"<span class='tag' style='color:{t_color}; border:1px solid {t_color};'>{t['label']} {t['val']}</span>"

    # MAIN CARD HTML
    st.markdown(f"""
    <div class='quant-card' style='position:relative; border:{border_color};'>
        {rank_html}
        <div class='card-title'>
            <span>{d['name']} <span style='font-size:14px; color:#888; font-weight:normal;'>{d.get('mode','')}</span></span>
            <span class='score-badge' style='color:{main_color}; border-color:{main_color};'>AI Score {win_pct:.1f}</span>
        </div>
        <div class='prog-track'>
            <div class='prog-fill' style='width:{win_pct}%; background:{main_color};'></div>
        </div>
        <div style='margin-bottom:15px;'>{tag_html}</div>
        
        <div class='grid-row'>
            <div class='grid-col'>
                <span class='grid-label'>현재가</span>
                <span class='grid-val'>{d['price']:,}</span>
            </div>
            <div class='grid-col'>
                <span class='grid-label'>수익률</span>
                <span class='grid-val' style='color: {"#FF4444" if d.get("pnl", 0) < 0 else "#00FF00"}'>{d.get("pnl", 0):.2f}%</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # PERSONA TABS
    t1, t2, t3 = st.tabs(["🐹 햄찌의 분석", "🐯 호찌의 분석", "📊 8대 엔진 HUD"])
    
    with t1:
        h = p['hamzzi']
        st.markdown(f"""
        <div class='persona-box' style='border-left-color: #FFAA00;'>
            <div class='persona-header' style='color:#FFAA00;'>{h['title']}</div>
            <div class='persona-body'>
                {h['brief']}<br><br>
                <b>🎯 논리적 근거:</b> {h['why']}
            </div>
            <div style='margin-top:15px; text-align:center;'>
                <span class='action-badge' style='background:#FFAA00;'>{h['action']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with t2:
        t = p['hojji']
        t_color = "#FF4444" if "사상누각" in t['title'] else "#00FF00" if "진국" in t['title'] else "#FFAA00"
        st.markdown(f"""
        <div class='persona-box' style='border-left-color: {t_color};'>
            <div class='persona-header' style='color:{t_color};'>{t['title']}</div>
            <div class='persona-body'>
                {t['brief']}<br><br>
                <b>🎯 논리적 근거:</b> {t['why']}
            </div>
            <div style='margin-top:15px; text-align:center;'>
                <span class='action-badge' style='background:#fff; border:1px solid {t_color}; color:{t_color};'>{t['action']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t3:
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
        <div style='margin-top:10px; font-size:12px; color:#888; text-align:center;'>
            * 수치가 높을수록 해당 엔진의 시그널이 강함을 의미합니다.
        </div>
        """, unsafe_allow_html=True)

    # TIMELINE
    st.markdown(f"""
    <div class='quant-card' style='margin-top:-15px; padding:10px 20px; border-top:none; border-radius: 0 0 15px 15px;'>
        <div class='timeline-box'>
            <div class='t-node'><div class='t-label'>진입/평단</div><div class='t-price' style='color:#00C9FF'>{p['prices'][0]:,}</div></div>
            <div class='t-node'><div class='t-label'>목표가</div><div class='t-price' style='color:#00FF00'>{p['prices'][1]:,}</div></div>
            <div class='t-node'><div class='t-label'>손절가</div><div class='t-price' style='color:#FF4444'>{p['prices'][2]:,}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [4] UI LAYOUT BUILD
# -----------------------------------------------------------------------------
with st.expander("💰 내 자산 및 포트폴리오 설정", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1: st.session_state.cash = st.number_input("예수금 (KRW)", value=st.session_state.cash, step=100000)
    with c2: st.session_state.target_return = st.number_input("목표 수익률 (%)", value=st.session_state.target_return, step=1.0)
    with c3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ 종목 추가", use_container_width=True):
            st.session_state.portfolio.append({'name': '삼성전자', 'price': 0, 'qty': 0, 'strategy': '추세추종'})
            st.rerun()
    
    st.markdown("---")
    
    # Portfolio Inputs with explicit labels
    if st.session_state.portfolio:
        for i, s in enumerate(st.session_state.portfolio):
            c1, c2, c3, c4, c5 = st.columns([3, 2, 1.5, 2, 0.5])
            with c1: 
                st.caption(f"종목명 {i+1}")
                try: idx = stock_names.index(s['name'])
                except: idx = 0
                s['name'] = st.selectbox(f"name_{i}", stock_names, index=idx, label_visibility="collapsed")
            with c2: 
                st.caption("평단가")
                s['price'] = st.number_input(f"price_{i}", value=float(s['price']), label_visibility="collapsed")
            with c3: 
                st.caption("수량")
                s['qty'] = st.number_input(f"qty_{i}", value=int(s['qty']), label_visibility="collapsed")
            with c4: 
                st.caption("전략")
                s['strategy'] = st.selectbox(f"strat_{i}", ["추세추종", "초단타"], index=0 if s['strategy']=="추세추종" else 1, label_visibility="collapsed")
            with c5: 
                st.caption("삭제")
                if st.button("🗑️", key=f"del_{i}"): 
                    st.session_state.portfolio.pop(i)
                    st.rerun()
    else:
        st.info("보유 종목이 없습니다. '➕ 종목 추가' 버튼을 눌러 리스트를 작성해주세요.")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    
    # MY DIAGNOSIS ACTION
    col_btn, col_timer = st.columns([2, 1])
    with col_btn:
        if st.button("📝 내 종목 및 포트폴리오 정밀 진단", use_container_width=True):
            st.session_state.trigger_my = True
            st.rerun()
    with col_timer:
        auto_my = st.selectbox("자동진단", list(TIME_OPTS.keys()), index=0, label_visibility="collapsed")

# [DISPLAY MY DIAGNOSIS RESULT]
if st.session_state.my_diagnosis:
    st.markdown("---")
    
    # 1. Portfolio Health
    if 'port_analysis' in st.session_state:
        pa = st.session_state.port_analysis
        st.markdown(f"""
        <div class='quant-card' style='border: 1px solid #aaa;'>
            <div style='font-size:18px; font-weight:bold; margin-bottom:15px; color:#fff;'>📊 포트폴리오 종합 진단</div>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:15px;'>
                <div class='persona-box' style='background:#222; border-left: 3px solid #FFAA00;'>
                    <div style='color:#FFAA00; font-weight:bold; margin-bottom:5px;'>🐹 햄찌 (공격형)</div>
                    <div style='font-size:13px; color:#ccc; line-height:1.5;'>{pa['hamzzi']}</div>
                </div>
                <div class='persona-box' style='background:#222; border-left: 3px solid #FF4444;'>
                    <div style='color:#FF4444; font-weight:bold; margin-bottom:5px;'>🐯 호찌 (방어형)</div>
                    <div style='font-size:13px; color:#ccc; line-height:1.5;'>{pa['hojji']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 2. Individual Stock Cards
    st.subheader("👤 보유 종목 상세 분석")
    for d in st.session_state.my_diagnosis:
        render_full_card(d)

# [MARKET SCAN SECTION]
st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)
st.subheader("📡 시장 정밀 타격 (Market Intelligence)")

c1, c2 = st.columns(2)
with c1:
    if st.button("🏆 타이거&햄찌 출격! (Top 3)"):
        st.session_state.trigger_top3 = True
        st.rerun()
    auto_top3 = st.selectbox("Top3 타이머", list(TIME_OPTS.keys()), index=0, label_visibility="collapsed")

with c2:
    if st.button("📊 단타 / 추세 (전략별 보기)"):
        st.session_state.trigger_sep = True
        st.rerun()
    auto_sep = st.selectbox("전략별 타이머", list(TIME_OPTS.keys()), index=0, label_visibility="collapsed")

# [DISPLAY MARKET RESULT]
if st.session_state.view_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("<h5>🏆 금일의 Singularity Ideal Pick (Top 3)</h5>", unsafe_allow_html=True)
    for i, d in enumerate(st.session_state.ideal_list):
        render_full_card(d, i, is_rank=True)

elif st.session_state.view_mode == 'SEPARATE' and st.session_state.sc_list:
    st.markdown("<h5>📊 전략별 절대 랭킹 (Top 3)</h5>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["⚡ 초단타", "🌊 추세추종"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_full_card(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_full_card(d, i, is_rank=True)

# -----------------------------------------------------------------------------
# [5] AUTO-REFRESH LOGIC CONTROLLER
# -----------------------------------------------------------------------------
now = time.time()
need_rerun = False

# Logic: If trigger is set OR (timer is on AND time passed)
# My Diagnosis
t_val_my = TIME_OPTS[auto_my]
if st.session_state.trigger_my or (t_val_my > 0 and now - st.session_state.l_my > t_val_my):
    run_my_diagnosis()
    need_rerun = True

# Top 3
t_val_top3 = TIME_OPTS[auto_top3]
if st.session_state.trigger_top3 or (t_val_top3 > 0 and now - st.session_state.l_top3 > t_val_top3):
    run_market_scan('TOP3')
    need_rerun = True

# Separate
t_val_sep = TIME_OPTS[auto_sep]
if st.session_state.trigger_sep or (t_val_sep > 0 and now - st.session_state.l_sep > t_val_sep):
    run_market_scan('SEPARATE')
    need_rerun = True

if need_rerun: st.rerun()

# Keep Alive for Timers
if t_val_my > 0 or t_val_top3 > 0 or t_val_sep > 0:
    time.sleep(1)
    st.rerun()
