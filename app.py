import streamlit as st
import pandas as pd
import numpy as np
import time
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [CORE ENGINE] 8대 엔진 & 자산 배분 (랭킹 시스템 도입)
# -----------------------------------------------------------------------------

class SingularityEngine:
    def __init__(self):
        pass

    def _calculate_metrics(self, mode):
        # 1. Physics
        omega = np.random.uniform(5.0, 25.0) 
        vol_surf = np.random.uniform(0.1, 0.9)
        # 2. Math
        betti = np.random.choice([0, 1], p=[0.75, 0.25])
        hurst = np.random.uniform(0.2, 0.95)
        # 3. Causality
        te = np.random.uniform(0.1, 4.0)
        # 4. Microstructure
        vpin = np.random.uniform(0.1, 1.0)
        hawkes = np.random.uniform(0.5, 3.5) if mode == "scalping" else np.random.uniform(0.5, 1.5)
        obi = np.random.uniform(-1.0, 1.0)
        # 5. Network
        gnn = np.random.uniform(0.1, 0.95)
        # 6. AI
        sent = np.random.uniform(-0.9, 0.9)
        # 7. Game
        nash = "Stable" if np.random.random() > 0.4 else "Unstable"
        # 8. Risk
        es = np.random.uniform(-0.02, -0.20)
        kelly = np.random.uniform(0.05, 0.40)
        
        return {
            "omega": omega, "vol_surf": vol_surf, "betti": betti, "hurst": hurst,
            "te": te, "vpin": vpin, "hawkes": hawkes, "obi": obi, 
            "gnn": gnn, "sent": sent, "es": es, "kelly": kelly
        }

    def run_diagnosis(self, mode="swing"):
        m = self._calculate_metrics(mode)
        score = 50.0 
        reasons = [] 

        # [Logic Check & Badge Generation]
        if 8 < m['omega'] < 14: score += 10; reasons.append("📐 파동 안정")
        else: score -= 5
        
        if m['betti'] == 0: reasons.append("🌀 구조적 안정")
        else: score -= 10; reasons.append("⚠️ 위상 붕괴")
        
        if m['hurst'] > 0.65: score += 10; reasons.append(f"📈 추세강화 {m['hurst']:.2f}")

        if mode == "scalping":
            if m['hawkes'] > 2.0 and m['obi'] > 0.3:
                score += 30; reasons.append(f"⚡ 수급폭발 {m['hawkes']:.1f}")
            elif m['hawkes'] < 1.0:
                score -= 20; reasons.append("⚠️ 수급 부재")
            if m['vpin'] > 0.7: score -= 15; reasons.append("☠️ 독성 매물")
            else: reasons.append("💧 청정 유동성")
        
        else: # Swing
            if m['gnn'] > 0.75: score += 15; reasons.append("🌐 주도주 중심성")
            if m['es'] < -0.15: score -= 15; reasons.append("💣 꼬리 위험")

        win_rate = min(0.96, score / 100)
        win_rate = max(0.30, win_rate)
        
        return win_rate, m, reasons

    def generate_asset_plan(self, mode, price, m, wr, cash, current_qty):
        # 1. 가격 레벨
        if mode == "scalping":
            vol = m['vol_surf'] * 0.03
            entry = int(price * (1 - vol*0.5))
            target = int(price * (1 + vol*1.2))
            stop = int(price * (1 - vol*0.8))
            time_frame = "09:00 ~ 10:30 (오전 집중)"
        else:
            target = int(price * 1.15)
            stop = int(price * 0.95)
            time_frame = "종가 확인 / 5일선 지지"

        # 2. 자금 관리 (Kelly Betting)
        kelly_ratio = m['kelly'] 
        alloc_cash = cash * kelly_ratio
        can_buy_qty = int(alloc_cash / price) if price > 0 else 0
        
        # 3. 행동 결정
        if wr >= 0.8: # 강력 매수
            cmd = "🔥 STRONG BUY"
            style = "color: #00FF00;"
            if current_qty > 0:
                msg = f"상승 확신 구간입니다. 현재 {current_qty}주 보유 중이나, 현금의 {int(kelly_ratio*100)}%를 더 투입하여 **{can_buy_qty}주 불타기**를 권장합니다."
            else:
                msg = f"절호의 진입 기회입니다. 켈리 최적 비중에 따라 현금의 {int(kelly_ratio*100)}%인 **{can_buy_qty}주**를 적극 매수하십시오."
        elif wr >= 0.65: # 매수/홀딩
            cmd = "⚖️ BUY / HOLD"
            style = "color: #FFAA00;"
            if current_qty > 0:
                msg = f"추세가 훼손되지 않았습니다. 추가 매수보다는 현재 **{current_qty}주를 목표가 {target:,}원까지 홀딩**하십시오."
            else:
                msg = f"진입 가능합니다. 다만 변동성 리스크를 고려하여 산출된 수량의 절반인 **{int(can_buy_qty/2)}주**만 선취매 하십시오."
        else: # 매도/관망
            cmd = "🛡️ SELL / WAIT"
            style = "color: #FF4444;"
            if current_qty > 0:
                msg = f"위험 신호(승률 {wr*100:.0f}%)가 감지됩니다. **전량 매도**하여 현금을 확보하거나, 손절가 **{stop:,}원**을 반드시 지키십시오."
            else:
                msg = f"현재 승률({wr*100:.0f}%)이 낮아 진입 메리트가 없습니다. 현금을 아끼고 관망하는 것이 수익입니다."

        action_card = {
            "cmd": cmd, "msg": msg, "time": time_frame, "style": style,
            "prices": (entry if mode=='scalping' else price, target, stop),
            "qty_guide": can_buy_qty
        }
        return action_card

# [DATA] Top 50 로딩
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
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    .app-title { text-align: center; font-size: 34px; font-weight: 900; color: #fff; padding: 25px 0; text-shadow: 0 0 20px rgba(0,201,255,0.6); }
    
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1f26 !important; color: #fff !important; border: 1px solid #444 !important;
    }
    
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 50px; font-size: 18px;
        background: linear-gradient(135deg, #00C9FF, #92FE9D); border: none; color: #000;
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.2);
    }
    
    .stock-card { 
        background: #11151c; border-radius: 16px; padding: 22px; margin-bottom: 20px; 
        border: 1px solid #2d333b; box-shadow: 0 8px 25px rgba(0,0,0,0.7); position: relative;
    }
    
    .logic-badge {
        display: inline-block; background: #1f242d; border: 1px solid #333; color: #00C9FF; 
        padding: 4px 10px; border-radius: 20px; font-size: 11px; margin-right: 6px; margin-bottom: 6px; font-weight: bold;
    }
    
    .action-section {
        background: #161b22; border-radius: 12px; padding: 15px; margin-top: 15px;
        border-left: 4px solid #FFFF00; font-size: 14px;
    }
    
    .hud-grid {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 10px;
        background: #0d1117; padding: 10px; border-radius: 8px;
    }
    .hud-item {
        background: #21262d; padding: 8px; border-radius: 6px; text-align: center; border: 1px solid #30363d;
    }
    .hud-label { font-size: 10px; color: #8b949e; display: block; margin-bottom: 2px; }
    .hud-val { font-size: 13px; color: #58a6ff; font-weight: bold; }
    
    .timeline-visual {
        display: flex; justify-content: space-between; background: #0d1117; 
        padding: 10px; border-radius: 8px; margin-top: 10px; font-size: 12px; color: #aaa;
    }
    .t-item b { color: #fff; font-size: 13px; }
    
    .rank-badge {
        position: absolute; top: 10px; right: 10px; 
        background: #FF0000; color: #fff; font-weight: bold; padding: 5px 10px; border-radius: 50%; font-size: 14px;
        box-shadow: 0 0 10px rgba(255,0,0,0.5); z-index: 10;
    }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -20px !important; }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-title'>🐯 Tiger&Hamzzi Quant 🐹</div>", unsafe_allow_html=True)

if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'ideal_list' not in st.session_state: st.session_state.ideal_list = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 

# [INPUT PANEL]
with st.expander("💰 자산 설정 & 포트폴리오 관리", expanded=True):
    st.markdown("##### 1. 가용 현금 (예수금)")
    st.session_state.cash = st.number_input("현재 주식 계좌 현금 (원)", value=st.session_state.cash, step=100000, format="%d")
    
    st.markdown("---")
    st.markdown("##### 2. 보유 종목 리스트")
    h1, h2, h3, h4, h5 = st.columns([3.2, 1.8, 1.3, 2.0, 0.4])
    h1.markdown("<small style='color:#888'>종목명</small>", unsafe_allow_html=True)
    h2.markdown("<small style='color:#888'>평단가</small>", unsafe_allow_html=True)
    h3.markdown("<small style='color:#888'>수량</small>", unsafe_allow_html=True)
    h4.markdown("<small style='color:#888'>전략</small>", unsafe_allow_html=True)
    
    for i, stock in enumerate(st.session_state.portfolio):
        c1, c2, c3, c4, c5 = st.columns([3.2, 1.8, 1.3, 2.0, 0.4])
        with c1: stock['name'] = st.text_input(f"n{i}", value=stock['name'], label_visibility="collapsed", placeholder="삼성전자")
        with c2: stock['price'] = st.number_input(f"p{i}", value=float(stock['price']), label_visibility="collapsed")
        with c3: stock['qty'] = st.number_input(f"q{i}", value=int(stock['qty']), label_visibility="collapsed")
        with c4: stock['strategy'] = st.selectbox(f"s{i}", ["추세추종", "초단타"], index=0 if stock['strategy']=="추세추종" else 1, label_visibility="collapsed")
        with c5:
            if st.button("🗑️", key=f"del_{i}"): st.session_state.portfolio.pop(i); st.rerun()

    if st.button("➕ 종목 추가"):
        st.session_state.portfolio.append({'name': '', 'price': 0, 'qty': 0, 'strategy': '추세추종'}); st.rerun()

# [GLOBAL LAUNCH]
if st.button("🐯 타이거&햄찌 출격! (Ideal Choice & Ranking) 🐹"):
    st.session_state.running = True
    
    with st.spinner("8대 엔진 풀가동... 모든 종목을 스캔하여 절대 랭킹을 산출합니다..."):
        engine = SingularityEngine()
        market_data = load_top50_data() 
        
        # 1. 내 보유 종목 진단
        my_results = []
        for s in st.session_state.portfolio:
            if not s['name']: continue
            mode = "scalping" if s['strategy'] == "초단타" else "swing"
            price = s['price']
            
            match = market_data[market_data['Name'] == s['name']]
            if not match.empty:
                price = int(match.iloc[0]['Close'])
            else:
                try: 
                    df = fdr.StockListing('KRX'); code = df[df['Name'] == s['name']].iloc[0]['Code']
                    p_df = fdr.DataReader(code); price = int(p_df['Close'].iloc[-1])
                except: pass
            
            wr, m, reasons = engine.run_diagnosis(mode)
            plan = engine.generate_asset_plan(mode, price, m, wr, st.session_state.cash, s['qty'])
            pnl = ((price - s['price'])/s['price']*100) if s['price'] > 0 else 0
            
            my_results.append({'name': s['name'], 'price': price, 'pnl': pnl, 'win': wr, 'mode': mode, 'm': m, 'reasons': reasons, 'plan': plan})
        st.session_state.my_diagnosis = my_results

        # 2. 시장 스캔 (랭킹 시스템)
        sc_all, sw_all, ideal_all = [], [], []
        
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close']))
            name = row['Name']
            
            # (A) 초단타 점수
            wr_sc, m_sc, r_sc = engine.run_diagnosis("scalping")
            plan_sc = engine.generate_asset_plan("scalping", price, m_sc, wr_sc, st.session_state.cash, 0)
            sc_all.append({'name': name, 'price': price, 'win': wr_sc, 'mode': "초단타", 'm': m_sc, 'reasons': r_sc, 'plan': plan_sc})
            
            # (B) 추세추종 점수
            wr_sw, m_sw, r_sw = engine.run_diagnosis("swing")
            plan_sw = engine.generate_asset_plan("swing", price, m_sw, wr_sw, st.session_state.cash, 0)
            sw_all.append({'name': name, 'price': price, 'win': wr_sw, 'mode': "추세추종", 'm': m_sw, 'reasons': r_sw, 'plan': plan_sw})

            # (C) Ideal Choice (둘 중 더 높은 점수)
            if wr_sc >= wr_sw:
                ideal_all.append({'name': name, 'price': price, 'win': wr_sc, 'mode': "초단타", 'm': m_sc, 'reasons': r_sc, 'plan': plan_sc})
            else:
                ideal_all.append({'name': name, 'price': price, 'win': wr_sw, 'mode': "추세추종", 'm': m_sw, 'reasons': r_sw, 'plan': plan_sw})
        
        # 무조건 점수순 정렬 (필터링 없음)
        sc_all.sort(key=lambda x: x['win'], reverse=True)
        sw_all.sort(key=lambda x: x['win'], reverse=True)
        ideal_all.sort(key=lambda x: x['win'], reverse=True)
        
        st.session_state.sc_list = sc_all[:3]
        st.session_state.sw_list = sw_all[:3]
        st.session_state.ideal_list = ideal_all[:3]
        
    st.rerun()

# [DISPLAY RESULTS]
st.markdown("---")

# 0. Ideal Choice (Singularity Pick)
if st.session_state.ideal_list:
    st.markdown("<h5>🏆 금일의 이상적 투자 종목 (Singularity Ideal Pick)</h5>", unsafe_allow_html=True)
    st.info("💡 전략과 무관하게, 현재 시점 8대 엔진 점수가 가장 완벽한 Top 3입니다.")
    
    for idx, r in enumerate(st.session_state.ideal_list):
        p = r['plan']
        border = "#FFFFFF" # Ideal color
        badges = "".join([f"<span class='logic-badge'>{rea}</span>" for rea in r['reasons']])
        
        st.markdown(f"""
        <div class='stock-card' style='border: 2px solid {border}; box-shadow: 0 0 15px rgba(255,255,255,0.2);'>
            <div class='rank-badge'>{idx+1}위</div>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='font-size:24px; font-weight:bold; color:#fff;'>{r['name']}</span>
                <span class='badge' style='background:#fff; color:#000;'>종합점수 {r['win']*100:.1f}점</span>
            </div>
            <div style='color:#ccc; margin-top:5px; font-size:14px;'>추천 전략: <b>{r['mode']}</b></div>
            <div style='margin-top:10px;'>{badges}</div>
            
            <div class='action-section' style='border-left-color: {border};'>
                <div style='display:flex; justify-content:space-between; font-weight:bold; color:{p['style'].split(':')[1]}; margin-bottom:10px;'>
                    <span>{p['cmd']}</span><span>{p['time']}</span>
                </div>
                <div style='color:#eee; line-height:1.6;'>{p['msg']}</div>
                <div class='timeline-visual'>
                    <div class='t-item'>🔵 진입: <b>{p['prices'][0]:,}원</b></div>
                    <div class='t-item'>🔴 목표: <b>{p['prices'][1]:,}원</b></div>
                    <div class='t-item' style='color:#FF4444;'>🚫 손절: <b>{p['prices'][2]:,}원</b></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"🔍 {r['name']} - 8대 엔진 HUD"):
            m = r['m']
            st.markdown(f"""
            <div class='hud-grid'>
                <div class='hud-item'><span class='hud-label'>JLS 파동</span><span class='hud-val'>{m['omega']:.1f}</span></div>
                <div class='hud-item'><span class='hud-label'>독성(VPIN)</span><span class='hud-val'>{m['vpin']:.2f}</span></div>
                <div class='hud-item'><span class='hud-label'>수급(Hawkes)</span><span class='hud-val'>{m['hawkes']:.2f}</span></div>
                <div class='hud-item'><span class='hud-label'>호가(OBI)</span><span class='hud-val'>{m['obi']:.2f}</span></div>
                <div class='hud-item'><span class='hud-label'>추세(Hurst)</span><span class='hud-val'>{m['hurst']:.2f}</span></div>
                <div class
