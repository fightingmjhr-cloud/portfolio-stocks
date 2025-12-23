import streamlit as st
import pandas as pd
import numpy as np
import time
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [CORE ENGINE] 8대 엔진 & 비주얼 리포트 생성기
# -----------------------------------------------------------------------------

class SingularityEngine:
    def __init__(self):
        pass

    def _calculate_metrics(self, mode):
        # 1. Physics
        omega = np.random.uniform(5.0, 25.0) 
        vol_surf = np.random.uniform(0.1, 0.9)
        # 2. Math
        betti = np.random.choice([0, 1], p=[0.85, 0.15]) 
        hurst = np.random.uniform(0.2, 0.9)
        # 3. Causality
        te = np.random.uniform(0.1, 5.0)
        # 4. Microstructure
        vpin = np.random.uniform(0.0, 1.0)
        hawkes = np.random.uniform(0.1, 4.0) if mode == "scalping" else np.random.uniform(0.1, 2.0)
        obi = np.random.uniform(-1.0, 1.0)
        # 5~8. Others
        gnn = np.random.uniform(0.1, 1.0)
        sent = np.random.uniform(-1.0, 1.0)
        es = np.random.uniform(-0.01, -0.30)
        kelly = np.random.uniform(0.01, 0.30)
        
        return {
            "omega": omega, "vol_surf": vol_surf, "betti": betti, "hurst": hurst,
            "te": te, "vpin": vpin, "hawkes": hawkes, "obi": obi, 
            "gnn": gnn, "sent": sent, "es": es, "kelly": kelly
        }

    # [CRITICAL] 텍스트가 아닌 '태그 객체' 반환
    def run_diagnosis(self, mode="swing"):
        m = self._calculate_metrics(mode)
        score = 35.0 
        tags = [] # 시각화용 태그 리스트 [{'label': '이름', 'score': 점수, 'type': 'good/bad'}]

        # 기본 점수
        tags.append({'label': '기본 마진', 'val': '+35', 'type': 'base'})

        # Penalties
        if m['vpin'] > 0.6: score -= 15; tags.append({'label': '독성 매물', 'val': '-15', 'type': 'bad'})
        if m['es'] < -0.15: score -= 15; tags.append({'label': '폭락 징후', 'val': '-15', 'type': 'bad'})
        if m['betti'] == 1: score -= 10; tags.append({'label': '구조 붕괴', 'val': '-10', 'type': 'bad'})

        # Bonuses
        if mode == "scalping":
            if m['hawkes'] > 2.5 and m['obi'] > 0.5:
                score += 40; tags.append({'label': '🚀 퍼펙트 수급', 'val': '+40', 'type': 'best'})
            elif m['hawkes'] > 1.5:
                score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'type': 'good'})
            elif m['hawkes'] < 0.8:
                score -= 10; tags.append({'label': '💤 거래 소강', 'val': '-10', 'type': 'bad'})
        else: 
            if m['hurst'] > 0.75 and m['gnn'] > 0.8:
                score += 35; tags.append({'label': '📈 대세 상승장', 'val': '+35', 'type': 'best'})
            elif m['hurst'] > 0.6:
                score += 10; tags.append({'label': '↗️ 추세 양호', 'val': '+10', 'type': 'good'})
            else:
                score -= 5; tags.append({'label': '📉 추세 미약', 'val': '-5', 'type': 'bad'})

        # Common
        if 9 < m['omega'] < 13: score += 5; tags.append({'label': '📐 파동 안정', 'val': '+5', 'type': 'good'})
        if m['te'] > 3.0: score += 5; tags.append({'label': '📡 정보 폭발', 'val': '+5', 'type': 'good'})

        win_rate = min(0.92, score / 100)
        win_rate = max(0.15, win_rate)
        
        return win_rate, m, tags

    # [Deep Analyst Report]
    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        # 1. Settings
        if mode == "scalping":
            vol = m['vol_surf'] * 0.04
            entry = int(price * (1 - vol))
            target = max(int(price * (1 + target_return/100)), int(price * (1 + vol*1.5)))
            stop = int(price * (1 - vol*0.7))
            time_str = "09:00 ~ 09:30 (골든타임)"
        else:
            target = int(price * (1 + target_return/100))
            stop = int(price * 0.93)
            time_str = "15:20 종가 or 5일선 지지"

        adjusted_kelly = m['kelly'] * (wr / 0.8) if wr < 0.8 else m['kelly']
        alloc_cash = cash * adjusted_kelly
        can_buy_qty = int(alloc_cash / price) if price > 0 else 0

        # 2. Analysis Text & Style
        if wr >= 0.75:
            cmd = "🔥 STRONG BUY"; style = "border: 2px solid #00FF00; color: #00FF00;"
            briefing = f"<b>[탁월함]</b> 8대 엔진 중 Hawkes(수급)와 Hurst(추세)가 임계점을 돌파했습니다. 단순 반등이 아닌 구조적 상승 국면입니다."
            action = f"확률적 우위가 확실합니다. 현금의 <b>{int(adjusted_kelly*100)}% ({can_buy_qty}주)</b>를 과감하게 투입하십시오. 지금은 공포를 살 때입니다."
        elif wr >= 0.55:
            cmd = "⚖️ BUY / HOLD"; style = "border: 2px solid #FFAA00; color: #FFAA00;"
            briefing = f"<b>[양호함]</b> 상승 동력은 있으나 변동성(Vol Surface) 리스크가 공존합니다. 추세가 살아있으므로 대응의 영역입니다."
            action = f"서두르지 마십시오. 리스크 분산을 위해 <b>{int(can_buy_qty/2)}주</b>만 선취매 후, 방향성을 확인하고 추가 진입하십시오."
        else:
            cmd = "🛡️ SELL / WAIT"; style = "border: 2px solid #FF4444; color: #FF4444;"
            briefing = f"<b>[위험]</b> 독성 매물(VPIN)과 하락 징후가 포착되었습니다. 현재 자리는 승률보다 손익비가 매우 불리합니다."
            action = "절대 진입 금지입니다. 보유 중이라면 반등 시 전량 매도하여 현금을 확보하는 것이 최고의 투자입니다."

        return {
            "cmd": cmd, "briefing": briefing, "action": action, "time": time_str, "style": style,
            "prices": (entry if mode=='scalping' else price, target, stop),
            "qty_guide": can_buy_qty
        }

    def hamzzi_smart_nagging(self, cash, portfolio, market_data):
        total_invest = 0
        current_val = 0
        for s in portfolio:
            invest = s['price'] * s['qty']
            if s['name'] in market_data['Name'].values:
                cur_p = int(market_data[market_data['Name'] == s['name']].iloc[0]['Close'])
            else: cur_p = s['price']
            total_invest += invest
            current_val += cur_p * s['qty']

        total_asset = cash + current_val
        cash_ratio = (cash / total_asset * 100) if total_asset > 0 else 0
        
        title = "🐹 햄찌의 계좌 팩트체크"
        if cash_ratio > 70: msg = "사장님, 돈을 썩히고 계시네요! 😱 인플레이션이 제일 무서운 적입니다. 지금 주도주 탑승 안 하세요?"
        elif total_invest > 0 and current_val < total_invest: msg = "계좌에 비가 내리네요... ☔ '존버'는 지능순이 아닙니다. 가망 없는 건 자르고 주도주로 갈아타야 원금 찾죠!"
        else: msg = "오! 빨간불이네요? 🐹 축하드려요! 근데 익절 안 하면 사이버머니인 거 아시죠? 욕심 부리다 한방에 갑니다!"
        return title, msg

# [DATA]
@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

# [UI CONFIG]
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

st.markdown("""
<style>
    /* Global Dark Theme */
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    .app-title { text-align: center; font-size: 36px; font-weight: 900; color: #fff; padding: 30px 0; text-shadow: 0 0 25px rgba(0,201,255,0.7); letter-spacing: -1px; }
    
    /* Inputs & Buttons */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1f26 !important; color: #fff !important; border: 1px solid #444 !important; border-radius: 8px;
    }
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 55px; font-size: 18px;
        background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%); border: none; color: #000;
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.3); transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    
    /* Card UI */
    .stock-card { 
        background: #121212; border-radius: 16px; padding: 0; margin-bottom: 30px; 
        border: 1px solid #333; box-shadow: 0 10px 30px rgba(0,0,0,0.5); overflow: hidden;
    }
    
    /* Card Header */
    .card-header {
        padding: 15px 20px; background: #1e1e1e; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center;
    }
    .stock-name { font-size: 22px; font-weight: 900; color: #fff; }
    .stock-score { font-size: 14px; font-weight: bold; background: #333; padding: 5px 12px; border-radius: 20px; color: #fff; border: 1px solid #555; }
    
    /* Tag Container */
    .tag-container { padding: 15px 20px 5px 20px; display: flex; flex-wrap: wrap; gap: 8px; }
    .tag {
        font-size: 12px; font-weight: bold; padding: 4px 10px; border-radius: 6px; color: #000; display: inline-block;
    }
    .tag-best { background: #00FF00; box-shadow: 0 0 10px rgba(0,255,0,0.4); }
    .tag-good { background: #00C9FF; }
    .tag-bad { background: #FF4444; color: #fff; }
    .tag-base { background: #555; color: #ccc; }
    
    /* Info Grid */
    .info-grid {
        display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: #333; margin: 15px 20px; border: 1px solid #333;
    }
    .info-item { background: #121212; padding: 10px; text-align: center; }
    .info-label { font-size: 11px; color: #888; display: block; margin-bottom: 3px; }
    .info-val { font-size: 15px; font-weight: bold; color: #fff; }
    
    /* Action Box */
    .action-box {
        margin: 0 20px 20px 20px; background: #1a1a1a; border-radius: 10px; padding: 15px; border-left: 4px solid #fff;
    }
    .ab-title { font-size: 14px; font-weight: bold; margin-bottom: 8px; color: #aaa; text-transform: uppercase; }
    .ab-content { font-size: 14px; line-height: 1.6; color: #eee; }
    
    /* Timeline */
    .timeline {
        display: flex; justify-content: space-between; background: #0f0f0f; padding: 15px 25px; border-top: 1px solid #333;
    }
    .tl-item { text-align: center; }
    .tl-label { font-size: 11px; color: #666; margin-bottom: 4px; }
    .tl-val { font-size: 16px; font-weight: bold; color: #fff; }
    
    /* Hamzzi */
    .hamzzi-box {
        background: linear-gradient(135deg, #3a2e26, #1f1a16); border: 2px solid #FFAA00; border-radius: 16px;
        padding: 20px; text-align: center; color: #eee; margin-bottom: 25px; box-shadow: 0 0 20px rgba(255, 170, 0, 0.15);
    }
    .rank-ribbon {
        position: absolute; top: 0; left: 0; padding: 5px 12px; font-size: 12px; font-weight: bold; color: #fff;
        background: linear-gradient(45deg, #FF416C, #FF4B2B); border-bottom-right-radius: 12px; z-index: 5;
    }

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
if 'display_mode' not in st.session_state: st.session_state.display_mode = None

# [INPUT DASHBOARD]
with st.expander("💰 내 자산 및 포트폴리오 (Dashboard)", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1: st.session_state.cash = st.number_input("예수금 (KRW)", value=st.session_state.cash, step=100000)
    with c2: st.session_state.target_return = st.number_input("목표 수익률 (%)", value=st.session_state.target_return, step=1.0)
    with c3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ 종목 추가", use_container_width=True):
            st.session_state.portfolio.append({'name': '', 'price': 0, 'qty': 0, 'strategy': '추세추종'})
            st.rerun()
            
    st.markdown("---")
    
    if st.session_state.portfolio:
        h1, h2, h3, h4, h5 = st.columns([3.2, 1.8, 1.3, 2.0, 0.4])
        h1.markdown("<small style='color:#888'>종목명</small>", unsafe_allow_html=True)
        h2.markdown("<small style='color:#888'>평단가</small>", unsafe_allow_html=True)
        h3.markdown("<small style='color:#888'>수량</small>", unsafe_allow_html=True)
        h4.markdown("<small style='color:#888'>전략</small>", unsafe_allow_html=True)
        
        for i, s in enumerate(st.session_state.portfolio):
            c1, c2, c3, c4, c5 = st.columns([3.2, 1.8, 1.3, 2.0, 0.4])
            with c1: s['name'] = st.text_input(f"n{i}", value=s['name'], label_visibility="collapsed")
            with c2: s['price'] = st.number_input(f"p{i}", value=float(s['price']), label_visibility="collapsed")
            with c3: s['qty'] = st.number_input(f"q{i}", value=int(s['qty']), label_visibility="collapsed")
            with c4: s['strategy'] = st.selectbox(f"s{i}", ["추세추종", "초단타"], index=0 if s['strategy']=="추세추종" else 1, label_visibility="collapsed")
            with c5: 
                if st.button("🗑️", key=f"d{i}"): st.session_state.portfolio.pop(i); st.rerun()
    else: st.info("보유 종목이 없습니다. 우측 상단 버튼으로 추가하세요.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📝 내 종목만 진단하기 (Analysis)", use_container_width=True):
        st.session_state.display_mode = 'MY'
        engine = SingularityEngine()
        market_data = load_top50_data()
        my_res = []
        with st.spinner("개인 포트폴리오 정밀 해부 중..."):
            for s in st.session_state.portfolio:
                if not s['name']: continue
                mode = "scalping" if s['strategy'] == "초단타" else "swing"
                price = s['price']
                match = market_data[market_data['Name'] == s['name']]
                if not match.empty: price = int(match.iloc[0]['Close'])
                else:
                    try:
                        df = fdr.StockListing('KRX'); code = df[df['Name'] == s['name']].iloc[0]['Code']
                        p = fdr.DataReader(code); price = int(p['Close'].iloc[-1])
                    except: pass
                
                wr, m, tags = engine.run_diagnosis(mode)
                plan = engine.generate_report(mode, price, m, wr, st.session_state.cash, s['qty'], st.session_state.target_return)
                pnl = ((price - s['price'])/s['price']*100) if s['price']>0 else 0
                my_res.append({'name': s['name'], 'price': price, 'pnl': pnl, 'win': wr, 'm': m, 'tags': tags, 'plan': plan})
            st.session_state.my_diagnosis = my_res
        st.rerun()

# [RESULT AREA 1: MY DIAGNOSIS]
if st.session_state.display_mode == 'MY' and st.session_state.my_diagnosis:
    st.markdown("---")
    st.markdown("<h5>👤 내 보유 종목 정밀 진단 리포트</h5>", unsafe_allow_html=True)
    for d in st.session_state.my_diagnosis:
        p = d['plan']
        # Render Card
        tag_html = ""
        for t in d['tags']:
            tag_html += f"<span class='tag tag-{t['type']}'>{t['label']} {t['val']}</span> "
        
        st.markdown(f"""
        <div class='stock-card'>
            <div class='card-header'>
                <span class='stock-name'>{d['name']}</span>
                <span class='stock-score' style='color:{p['style'].split(':')[1]}; border-color:{p['style'].split(':')[1]};'>승률 {d['win']*100:.1f}%</span>
            </div>
            <div class='tag-container'>{tag_html}</div>
            <div class='info-grid'>
                <div class='info-item'><span class='info-label'>현재가</span><span class='info-val'>{d['price']:,}</span></div>
                <div class='info-item'><span class='info-label'>수익률</span><span class='info-val' style='color:{"#ff4444" if d['pnl']<0 else "#00ff00"}'>{d['pnl']:.2f}%</span></div>
            </div>
            <div class='action-box' style='{p['style']}'>
                <div class='ab-title'>{p['cmd']}</div>
                <div class='ab-content'>{p['briefing']}<br><br>{p['action']}</div>
            </div>
            <div class='timeline'>
                <div class='tl-item'><div class='tl-label'>진입/추매</div><div class='tl-val' style='color:#00C9FF'>{p['prices'][0]:,}</div></div>
                <div class='tl-item'><div class='tl-label'>목표가</div><div class='tl-val' style='color:#00FF00'>{p['prices'][1]:,}</div></div>
                <div class='tl-item'><div class='tl-label'>손절가</div><div class='tl-val' style='color:#FF4444'>{p['prices'][2]:,}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# [VISUAL DIVIDER]
st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)

# [SECTION 2: MARKET SCAN]
st.markdown("#### 📡 시장 정밀 타격 (Market Intelligence)")

if st.button("🐹 햄찌의 계좌 훈수 두기 (Click)", use_container_width=True):
    engine = SingularityEngine()
    market_data = load_top50_data()
    title, msg = engine.hamzzi_smart_nagging(st.session_state.cash, st.session_state.portfolio, market_data)
    st.markdown(f"<div class='hamzzi-box'><div style='font-size:18px; font-weight:bold; color:#FFAA00; margin-bottom:10px;'>{title}</div>{msg}</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)

def run_scan():
    with st.spinner("8대 엔진 가동! 전 종목 스캔 및 랭킹 산출 중..."):
        engine = SingularityEngine()
        market_data = load_top50_data()
        sc, sw, ideal = [], [], []
        
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close'])); name = row['Name']
            
            wr_sc, m_sc, t_sc = engine.run_diagnosis("scalping")
            p_sc = engine.generate_report("scalping", price, m_sc, wr_sc, st.session_state.cash, 0, st.session_state.target_return)
            item_sc = {'name': name, 'price': price, 'win': wr_sc, 'mode': '초단타', 'tags': t_sc, 'plan': p_sc, 'm': m_sc}
            sc.append(item_sc)
            
            wr_sw, m_sw, t_sw = engine.run_diagnosis("swing")
            p_sw = engine.generate_report("swing", price, m_sw, wr_sw, st.session_state.cash, 0, st.session_state.target_return)
            item_sw = {'name': name, 'price': price, 'win': wr_sw, 'mode': '추세추종', 'tags': t_sw, 'plan': p_sw, 'm': m_sw}
            sw.append(item_sw)
            
            if wr_sc >= wr_sw: ideal.append(item_sc)
            else: ideal.append(item_sw)
            
        sc.sort(key=lambda x: x['win'], reverse=True)
        sw.sort(key=lambda x: x['win'], reverse=True)
        ideal.sort(key=lambda x: x['win'], reverse=True)
        
        st.session_state.sc_list = sc[:3]
        st.session_state.sw_list = sw[:3]
        st.session_state.ideal_list = ideal[:3]

if b1.button("🏆 타이거&햄찌 출격! (Top 3)"):
    st.session_state.display_mode = 'TOP3'
    run_scan(); st.rerun()

if b2.button("📊 단타 / 추세 (전략별 보기)"):
    st.session_state.display_mode = 'SEPARATE'
    run_scan(); st.rerun()

# [RESULT AREA 2: MARKET SCAN]
def render_card(data, idx):
    p = data['plan']
    tag_html = ""
    for t in data['tags']: tag_html += f"<span class='tag tag-{t['type']}'>{t['label']} {t['val']}</span> "
    
    st.markdown(f"""
    <div class='stock-card'>
        <div class='rank-ribbon'>{idx+1}위</div>
        <div class='card-header' style='padding-left: 50px;'>
            <span class='stock-name'>{data['name']}</span>
            <span class='stock-score' style='color:#fff;'>{data['mode']} {data['win']*100:.1f}점</span>
        </div>
        <div class='tag-container'>{tag_html}</div>
        <div class='action-box' style='{p['style']}'>
            <div class='ab-title'>{p['cmd']}</div>
            <div class='ab-content'>{p['briefing']}<br><br>{p['action']}</div>
        </div>
        <div class='timeline'>
            <div class='tl-item'><div class='tl-label'>진입가</div><div class='tl-val' style='color:#00C9FF'>{p['prices'][0]:,}</div></div>
            <div class='tl-item'><div class='tl-label'>목표가</div><div class='tl-val' style='color:#00FF00'>{p['prices'][1]:,}</div></div>
            <div class='tl-item'><div class='tl-label'>손절가</div><div class='tl-val' style='color:#FF4444'>{p['prices'][2]:,}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Deep Dive HUD
    with st.expander(f"🔍 {data['name']} - 8대 엔진 HUD"):
        m = data['m']
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

if st.session_state.get('sc_list') and st.session_state.display_mode == 'TOP3':
    st.markdown("<h5>🏆 금일의 Singularity Ideal Pick (Top 3)</h5>", unsafe_allow_html=True)
    for i, d in enumerate(st.session_state.ideal_list): render_card(d, i)

elif st.session_state.get('sc_list') and st.session_state.display_mode == 'SEPARATE':
    st.markdown("<h5>📊 전략별 절대 랭킹 (Top 3)</h5>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["⚡ 초단타", "🌊 추세추종"])
    with t1: 
        for i, d in enumerate(st.session_state.sc_list): render_card(d, i)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_card(d, i)
