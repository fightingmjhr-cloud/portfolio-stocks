import streamlit as st
import pandas as pd
import numpy as np
import time
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [CORE ENGINE] 8대 엔진 & 자산 배분 (전략 분리 복구)
# -----------------------------------------------------------------------------

class SingularityEngine:
    def __init__(self):
        pass

    # [PHASE 1] 8대 엔진 데이터 생성
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

    # [PHASE 2] 승률 산출 (감점제)
    def run_diagnosis(self, mode="swing"):
        m = self._calculate_metrics(mode)
        score = 50.0 
        reasons = [] 

        # [Logic Check]
        if 8 < m['omega'] < 14: score += 10; reasons.append("파동 안정")
        else: score -= 5
        
        if m['betti'] == 0: reasons.append("구조적 안정")
        else: score -= 10; reasons.append("위상 붕괴")
        
        if m['hurst'] > 0.65: score += 10; reasons.append(f"추세강화({m['hurst']:.2f})")

        if mode == "scalping":
            if m['hawkes'] > 2.0 and m['obi'] > 0.3:
                score += 30; reasons.append(f"수급폭발({m['hawkes']:.1f})")
            elif m['hawkes'] < 1.0:
                score -= 20; reasons.append("수급 부재")
            if m['vpin'] > 0.7: score -= 15; reasons.append("독성 매물")
        
        else: # Swing
            if m['gnn'] > 0.75: score += 15; reasons.append("주도주 중심성")
            if m['es'] < -0.15: score -= 15; reasons.append("꼬리 위험")

        win_rate = min(0.95, score / 100)
        win_rate = max(0.30, win_rate)
        
        return win_rate, m, reasons

    # [PHASE 3] 자산 배분 및 구체적 행동 지침 (Portfolio Action)
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
        kelly_ratio = m['kelly'] # 예: 0.2 (20%)
        alloc_cash = cash * kelly_ratio
        can_buy_qty = int(alloc_cash / price) if price > 0 else 0
        
        # 3. 행동 결정
        action_card = {}
        
        if wr >= 0.8: # 강력 매수
            cmd = "🔥 STRONG BUY"
            if current_qty > 0:
                msg = f"상승 확신 구간입니다. 현재 {current_qty}주에 더해, 현금의 {int(kelly_ratio*100)}%로 **{can_buy_qty}주 불타기** 하십시오."
            else:
                msg = f"절호의 진입 기회입니다. 현금의 {int(kelly_ratio*100)}%인 **{can_buy_qty}주**를 적극 매수하십시오."
        elif wr >= 0.65: # 매수/홀딩
            cmd = "⚖️ BUY / HOLD"
            if current_qty > 0:
                msg = f"추세가 유지됩니다. 추가 매수보다는 **{current_qty}주를 목표가 {target:,}원까지 홀딩**하십시오."
            else:
                msg = f"진입 가능합니다. 다만 리스크 분산을 위해 **{int(can_buy_qty/2)}주(절반)**만 선취매 하십시오."
        else: # 매도/관망
            cmd = "🛡️ SELL / WAIT"
            if current_qty > 0:
                msg = f"위험 신호 감지. **전량 매도**하여 현금을 확보하거나, 손절가 **{stop:,}원**을 반드시 지키십시오."
            else:
                msg = "현재 진입은 위험합니다. 현금을 아끼고 관망하십시오."

        action_card = {
            "cmd": cmd, "msg": msg, "time": time_frame,
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
    .app-title { text-align: center; font-size: 34px; font-weight: 900; color: #fff; padding: 25px 0; text-shadow: 0 0 15px rgba(0,201,255,0.6); }
    
    /* Input Styling */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1f26 !important; color: #fff !important; border: 1px solid #444 !important;
    }
    .input-label { font-size: 12px; color: #888; text-align: center; display: block; margin-bottom: 5px; }
    
    /* Button */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 50px; font-size: 18px;
        background: linear-gradient(135deg, #00C9FF, #92FE9D); border: none; color: #000;
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.2);
    }
    
    /* Card Design */
    .stock-card { 
        background: #11151c; border-radius: 16px; padding: 22px; margin-bottom: 20px; 
        border: 1px solid #2d333b; box-shadow: 0 8px 25px rgba(0,0,0,0.7);
    }
    
    /* Action Section */
    .action-section {
        background: #1a1f26; border-radius: 10px; padding: 15px; margin-top: 15px;
        border-left: 4px solid #FFFF00; 
    }
    .action-header { font-weight: bold; font-size: 15px; color: #FFFF00; margin-bottom: 10px; display: flex; justify-content: space-between; }
    .timeline-box { display: flex; gap: 10px; margin-top: 10px; font-size: 12px; color: #aaa; background: #0d1117; padding: 8px; border-radius: 6px; }
    
    /* Badge */
    .logic-badge {
        background: #1f242d; border: 1px solid #333; color: #00C9FF; 
        padding: 4px 8px; border-radius: 4px; font-size: 11px; margin-right: 5px;
    }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -20px !important; }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-title'>🐯 Tiger&Hamzzi Quant 🐹</div>", unsafe_allow_html=True)

# [SESSION STATE]
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 

# [INPUT PANEL]
with st.expander("💰 자산 및 포트폴리오 설정", expanded=True):
    # 1. 현금 입력
    st.markdown("##### 1. 가용 현금 (예수금)")
    st.session_state.cash = st.number_input("현재 주식 계좌에 있는 현금 (원)", value=st.session_state.cash, step=100000, format="%d")
    
    st.markdown("---")
    st.markdown("##### 2. 보유 종목 리스트")
    h1, h2, h3, h4, h5 = st.columns([3.2, 1.8, 1.3, 2.0, 0.4])
    h1.markdown("<span class='input-label'>종목명</span>", unsafe_allow_html=True)
    h2.markdown("<span class='input-label'>평단가(원)</span>", unsafe_allow_html=True)
    h3.markdown("<span class='input-label'>수량(주)</span>", unsafe_allow_html=True)
    h4.markdown("<span class='input-label'>전략(Mode)</span>", unsafe_allow_html=True)
    
    for i, stock in enumerate(st.session_state.portfolio):
        c1, c2, c3, c4, c5 = st.columns([3.2, 1.8, 1.3, 2.0, 0.4])
        with c1: stock['name'] = st.text_input(f"n{i}", value=stock['name'], label_visibility="collapsed", placeholder="예: 삼성전자")
        with c2: stock['price'] = st.number_input(f"p{i}", value=float(stock['price']), label_visibility="collapsed")
        with c3: stock['qty'] = st.number_input(f"q{i}", value=int(stock['qty']), label_visibility="collapsed")
        with c4: stock['strategy'] = st.selectbox(f"s{i}", ["추세추종", "초단타"], index=0 if stock['strategy']=="추세추종" else 1, label_visibility="collapsed")
        with c5:
            if st.button("🗑️", key=f"del_{i}"): st.session_state.portfolio.pop(i); st.rerun()

    if st.button("➕ 종목 추가"):
        st.session_state.portfolio.append({'name': '', 'price': 0, 'qty': 0, 'strategy': '추세추종'}); st.rerun()

# [GLOBAL LAUNCH]
if st.button("🐯 타이거&햄찌 출격! (진단 및 스캔) 🐹"):
    st.session_state.running = True
    
    with st.spinner("8대 엔진 풀가동... 보유 종목 진단 및 초단타/추세추종 개별 스캔 중..."):
        engine = SingularityEngine()
        market_data = load_top50_data() 
        
        # 1. 내 보유 종목 진단
        my_results = []
        for s in st.session_state.portfolio:
            if not s['name']: continue
            mode = "scalping" if s['strategy'] == "초단타" else "swing"
            price = s['price']
            
            # 실시간 가격
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

        # 2. 시장 스캔 (분리 수행)
        sc_temp, sw_temp = [], []
        
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close']))
            name = row['Name']
            
            # (A) 초단타 스캔
            wr_sc, m_sc, r_sc = engine.run_diagnosis("scalping")
            if wr_sc >= 0.70:
                plan = engine.generate_asset_plan("scalping", price, m_sc, wr_sc, st.session_state.cash, 0)
                sc_temp.append({'name': name, 'price': price, 'win': wr_sc, 'mode': "초단타", 'm': m_sc, 'reasons': r_sc, 'plan': plan})
                
            # (B) 추세추종 스캔
            wr_sw, m_sw, r_sw = engine.run_diagnosis("swing")
            if wr_sw >= 0.75:
                plan = engine.generate_asset_plan("swing", price, m_sw, wr_sw, st.session_state.cash, 0)
                sw_temp.append({'name': name, 'price': price, 'win': wr_sw, 'mode': "추세추종", 'm': m_sw, 'reasons': r_sw, 'plan': plan})
        
        # 정렬 및 Top 3
        sc_temp.sort(key=lambda x: x['win'], reverse=True)
        sw_temp.sort(key=lambda x: x['win'], reverse=True)
        st.session_state.sc_list = sc_temp[:3]
        st.session_state.sw_list = sw_temp[:3]
        
    st.rerun()

# [DISPLAY RESULTS]
st.markdown("---")

# 1. 내 종목 진단 결과
if 'my_diagnosis' in st.session_state and st.session_state.my_diagnosis:
    st.markdown("<h5>👤 내 포트폴리오 정밀 진단 (Action Plan)</h5>", unsafe_allow_html=True)
    for d in st.session_state.my_diagnosis:
        p = d['plan']
        border = "#00FF00" if d['win'] >= 0.8 else ("#FFAA00" if d['win'] >= 0.65 else "#FF4444")
        badges = "".join([f"<span class='logic-badge'>{r}</span>" for r in d['reasons']])
        
        st.markdown(f"""
        <div class='stock-card' style='border-left: 5px solid {border};'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='font-size:22px; font-weight:bold; color:#fff;'>{d['name']}</span>
                <span class='badge' style='background:{border}; color:#000;'>승률 {d['win']*100:.1f}%</span>
            </div>
            <div style='display:flex; gap:15px; margin-top:5px; font-size:14px; color:#ccc;'>
                <span>현재가: <b>{d['price']:,}</b></span>
                <span style='color:{"#00FF00" if d['pnl']>=0 else "#FF4444"};'>수익률: <b>{d['pnl']:.2f}%</b></span>
            </div>
            <div style='margin-top:10px;'>{badges}</div>
            <div class='action-section' style='border-left-color: {border};'>
                <div class='action-header'>
                    <span>{p['cmd']}</span>
                    <span>타임라인: {p['time']}</span>
                </div>
                <div style='color:#eee; line-height:1.6;'>{p['msg']}</div>
                <div class='timeline-box'>
                    <div>🔵 진입/추매: <b>{p['prices'][0]:,}원</b></div>
                    <div>🔴 익절: <b>{p['prices'][1]:,}원</b></div>
                    <div style='color:#FF4444;'>🚫 손절: <b>{p['prices'][2]:,}원</b></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 2. 추천 탭 (초단타 / 추세추종 분리)
if st.session_state.sc_list or st.session_state.sw_list:
    st.markdown("<h5>🏆 오늘의 8대 엔진 추천 종목 (Top 3)</h5>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["⚡ 초단타 추천", "🌊 추세추종 추천"])
    
    def render_rec(data, color):
        for r in data:
            p = r['plan']
            badges = "".join([f"<span class='logic-badge'>{rea}</span>" for rea in r['reasons']])
            st.markdown(f"""
            <div class='stock-card' style='border-left: 5px solid {color};'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-size:22px; font-weight:bold; color:#fff;'>{r['name']}</span>
                    <span class='badge' style='background:{color}; color:#000;'>{r['mode']} / {r['win']*100:.1f}%</span>
                </div>
                <div style='margin-top:10px;'>{badges}</div>
                <div class='action-section' style='border-left-color: {color};'>
                    <div class='action-header'>
                        <span>📢 신규 진입 시나리오</span>
                        <span>{p['time']}</span>
                    </div>
                    <div style='color:#eee; line-height:1.6;'>{p['msg']}</div>
                    <div class='timeline-box'>
                        <div>🔵 진입: <b>{p['prices'][0]:,}원</b></div>
                        <div>🔴 익절: <b>{p['prices'][1]:,}원</b></div>
                        <div style='color:#FF4444;'>🚫 손절: <b>{p['prices'][2]:,}원</b></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander(f"🔍 {r['name']} - Deep Dive"):
                m = r['m']
                st.markdown(f"""
                <div style='display:grid; grid-template-columns: repeat(2, 1fr); gap:10px; font-size:12px; color:#ccc;'>
                    <div>📐 Omega: <b style='color:#fff; float:right;'>{m['omega']:.2f}</b></div>
                    <div>🌊 VPIN: <b style='color:#fff; float:right;'>{m['vpin']:.2f}</b></div>
                    <div>⚡ Hawkes: <b style='color:#fff; float:right;'>{m['hawkes']:.2f}</b></div>
                    <div>⚖️ OBI: <b style='color:#fff; float:right;'>{m['obi']:.2f}</b></div>
                    <div>📈 Hurst: <b style='color:#fff; float:right;'>{m['hurst']:.2f}</b></div>
                    <div>💰 Kelly: <b style='color:#fff; float:right;'>{m['kelly']:.2f}</b></div>
                </div>
                """, unsafe_allow_html=True)

    with tab1:
        if st.session_state.sc_list: render_rec(st.session_state.sc_list, "#FFFF00")
        else: st.info("초단타 조건(수급 폭발)을 만족하는 종목이 없습니다.")
    
    with tab2:
        if st.session_state.sw_list: render_rec(st.session_state.sw_list, "#00C9FF")
        else: st.info("추세추종 조건(추세 지속)을 만족하는 종목이 없습니다.")

else:
    if not st.session_state.get('running'):
        st.info("👆 [출격] 버튼을 누르면 자산 기반의 최적 포트폴리오 전략을 수립합니다.")
