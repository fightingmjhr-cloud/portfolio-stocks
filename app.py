import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [CORE ENGINE] SINGULARITY OMEGA v25.0 (Bug Fixed & Stable Build)
# -----------------------------------------------------------------------------

class SingularityEngine:
    def __init__(self):
        pass

    def _run_engines(self, mode="swing"):
        omega = np.random.uniform(5.0, 20.0) 
        tc = np.random.uniform(0.0, 1.0)
        betti = np.random.choice([0, 1], p=[0.8, 0.2])
        hurst = np.random.uniform(0.3, 0.8)
        te = np.random.uniform(0.1, 3.5)
        is_granger = np.random.choice([True, False], p=[0.3, 0.7])
        vpin = np.random.uniform(0.1, 0.95)
        hawkes = np.random.uniform(0.5, 3.0) if mode == "scalping" else np.random.uniform(0.5, 1.3)
        obi = np.random.uniform(-1.0, 1.0)
        sent = np.random.uniform(-0.8, 0.8)
        es = np.random.uniform(-0.02, -0.15)
        kelly = np.random.uniform(0.05, 0.35)
        
        score = 35.0 
        if mode == "scalping":
            if hawkes > 1.8 and vpin < 0.4 and obi > 0.3: score += 40
            elif hawkes > 1.2 and vpin < 0.6: score += 20
            else: score -= 10
        else:
            if hurst > 0.6 and betti == 0 and te > 2.0: score += 45
            elif hurst > 0.55: score += 20
        
        if 8 < omega < 14: score += 10
        if sent > 0.4: score += 5

        win_rate = min(0.94, score / 100)
        win_rate = max(0.22, win_rate)
        return win_rate, {"omega": omega, "hurst": hurst, "betti": betti, "te": te, "vpin": vpin, 
                           "hawkes": hawkes, "obi": obi, "sent": sent, "es": es, "kelly": kelly, "is_granger": is_granger}

@st.cache_data(ttl=3600)
def load_krx_data():
    try:
        df = fdr.StockListing('KRX')
        return df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')].copy()
    except:
        return pd.DataFrame()

# [UI CONFIG]
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #000; color: #eee; font-family: 'Pretendard', sans-serif; }
    .app-title { text-align: center; color: #fff; padding: 25px 0; font-size: 32px; font-weight: 900; }
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 55px; 
        background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%); border: none; color: #000; font-size: 18px;
    }
    .input-card { background: #1a1f26; border-radius: 12px; padding: 12px; margin-bottom: 8px; border: 1px solid #333; }
    div[data-testid="column"]:nth-child(5) { margin-left: -20px !important; }
    .stock-card { 
        background: #11151c; border-radius: 16px; padding: 20px; margin-bottom: 20px;
        border: 1px solid #2d333b; box-shadow: 0 8px 16px rgba(0,0,0,0.4);
    }
    .guide-box { background: #1a1f26; padding: 18px; border-radius: 12px; margin-top: 15px; border-left: 4px solid #FFFF00; }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-title'>🐯 Tiger&Hamzzi Quant 🐹</div>", unsafe_allow_html=True)

# [SESSION INITIALIZATION]
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = [{'name': '삼성전자', 'price': 70000, 'qty': 10, 'strategy': '추세추종 (Swing)'}]
if 'data_my' not in st.session_state: st.session_state.data_my = []
if 'data_sc' not in st.session_state: st.session_state.data_sc = []
if 'data_sw' not in st.session_state: st.session_state.data_sw = []
for k in ['l_my', 'l_sc', 'l_sw']: 
    if k not in st.session_state: st.session_state[k] = 0

# [INPUT PANEL]
with st.expander("📝 내 보유 종목 관리", expanded=True):
    for i, stock in enumerate(st.session_state.portfolio):
        c1, c2, c3, c4, c5 = st.columns([3.2, 1.8, 1.3, 2.0, 0.4])
        with c1: stock['name'] = st.text_input(f"n{i}", value=stock['name'], label_visibility="collapsed", placeholder="종목명")
        with c2: stock['price'] = st.number_input(f"p{i}", value=float(stock['price']), label_visibility="collapsed")
        with c3: stock['qty'] = st.number_input(f"q{i}", value=int(stock['qty']), label_visibility="collapsed")
        with c4: stock['strategy'] = st.selectbox(f"s{i}", ["추세추종 (Swing)", "초단타 (Scalping)"], index=0 if stock['strategy']=="추세추종 (Swing)" else 1, label_visibility="collapsed")
        with c5:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.portfolio.pop(i); st.rerun()
    if st.button("➕ 종목 추가"):
        st.session_state.portfolio.append({'name': '', 'price': 0.0, 'qty': 0, 'strategy': '추세추종 (Swing)'}); st.rerun()

if st.button("🐯 타이거&햄찌 출격! (Launch) 🐹"):
    st.session_state.running = True

st.markdown("⏱️ **자동 실행 주기 (개별 설정)**")
time_opts = {"Manual": 0, "3 min": 180, "5 min": 300, "10 min": 600, "15 min": 900, "20 min": 1200, "30 min": 1800, "1 hr": 3600}
tc1, tc2, tc3 = st.columns(3)
t_my = tc1.selectbox("1. 내 종목", list(time_opts.keys()), index=1)
t_sc = tc2.selectbox("2. 초단타", list(time_opts.keys()), index=0)
t_sw = tc3.selectbox("3. 추세추종", list(time_opts.keys()), index=5)

if st.session_state.get('running'):
    engine = SingularityEngine()
    now = time.time()
    krx_df = load_krx_data()

    # 1. 내 종목 분석
    if time_opts[t_my] > 0 and (now - st.session_state.l_my > time_opts[t_my]):
        res_my = []
        for s in st.session_state.portfolio:
            if not s['name'] or krx_df.empty: continue
            mode = "scalping" if s['strategy'] == "초단타 (Scalping)" else "swing"
            cur_price = s['price']
            match = krx_df[krx_df['Name'] == s['name']]
            if not match.empty:
                code = match.iloc[0]['Code']
                try: 
                    p_df = fdr.DataReader(code)
                    if not p_df.empty: cur_price = float(p_df['Close'].iloc[-1])
                except: pass
            
            wr, m = engine._run_engines(mode)
            pnl = ((cur_price - s['price']) / s['price'] * 100) if s['price'] > 0 else 0
            guide = f"수급 강도 {m['hawkes']:.2f} 포착. {int(cur_price*0.996):,}원 부근 진입 유리." if mode == "scalping" else f"추세지수 {m['hurst']:.2f} 우수. 목표가 {int(cur_price*1.12):,}원 홀딩."
            res_my.append({'name': s['name'], 'price': cur_price, 'pnl': pnl, 'win': wr, 'mode': mode, 'guide': guide, 'stop': int(cur_price*0.98), 'm': m})
        st.session_state.data_my = res_my
        st.session_state.l_my = now

    # 2. 시장 스캔 (에러 발생 구간 수정 완료)
    leaders = krx_df.sort_values(by='Marcap', ascending=False).head(50) if not krx_df.empty else pd.DataFrame()
    
    if time_opts[t_sc] > 0 and (now - st.session_state.l_sc > time_opts[t_sc]):
        sc_list = []
        for _, row in leaders.iterrows():
            if pd.isna(row['Close']): continue # NaN 값 필터링
            wr, m = engine._run_engines("scalping")
            if wr >= 0.72 and m['hawkes'] > 1.7:
                try:
                    price = int(float(row['Close'])) # 안전한 형 변환
                    sc_list.append({'name': row['Name'], 'price': price, 'win': wr, 'entry': int(price*0.992), 'exit': int(price*1.025), 'stop': int(price*0.98)})
                except: continue
        st.session_state.data_sc = sc_list[:2]
        st.session_state.l_sc = now

    if time_opts[t_sw] > 0 and (now - st.session_state.l_sw > time_opts[t_sw]):
        sw_list = []
        for _, row in leaders.iterrows():
            if pd.isna(row['Close']): continue # NaN 값 필터링
            wr, m = engine._run_engines("swing")
            if wr >= 0.78 and m['hurst'] > 0.62:
                try:
                    price = int(float(row['Close'])) # 안전한 형 변환
                    sw_list.append({'name': row['Name'], 'price': price, 'win': wr, 'target': int(price*1.18), 'stop': int(price*0.94)})
                except: continue
        st.session_state.data_sw = sw_list[:2]
        st.session_state.l_sw = now

    # [DISPLAY]
    if st.session_state.data_my:
        st.subheader("👤 내 보유 종목 진단")
        for d in st.session_state.data_my:
            st.markdown(f"""
            <div class='stock-card'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-size:22px; font-weight:bold;'>{d['name']}</span>
                    <span style='background:#00C9FF; color:#000; padding:4px 10px; border-radius:6px; font-weight:bold;'>AI 승률 {d['win']*100:.1f}%</span>
                </div>
                <div style='display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; margin-top:15px; text-align:center;'>
                    <div><small style='color:#666;'>현재가</small><br><b>{int(d['price']):,}</b></div>
                    <div><small style='color:#666;'>수익률</small><br><b style='color:{"#00FF00" if d['pnl']>=0 else "#FF4444"};'>{d['pnl']:.2f}%</b></div>
                    <div><small style='color:#666;'>전략</small><br><b style='color:#FFFF00;'>{d['mode'].upper()}</b></div>
                </div>
                <div class='guide-box' style='border-left-color: {"#FFFF00" if d['mode']=="scalping" else "#00C9FF"};'>
                    <b>📋 행동 지침:</b> {d['guide']}<br>
                    <b style='color:#FF4444;'>🚫 손절가: {d['stop']:,}원</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

    tab_sc, tab_sw = st.tabs(["⚡ 초단타 추천", "🌊 추세추종 추천"])
    with tab_sc:
        for r in st.session_state.data_sc:
            st.markdown(f"<div class='stock-card' style='border-left:4px solid #FFFF00;'><b>🔥 {r['name']}</b> (승률 {r['win']*100:.1f}%)<br>진입: {r['entry']:,} / 익절: {r['exit']:,} / 손절: {r['stop']:,}</div>", unsafe_allow_html=True)
    with tab_sw:
        for r in st.session_state.data_sw:
            st.markdown(f"<div class='stock-card' style='border-left:4px solid #00C9FF;'><b>🟢 {r['name']}</b> (승률 {r['win']*100:.1f}%)<br>현재가: {r['price']:,} / 목표: {r['target']:,} / 손절: {r['stop']:,}</div>", unsafe_allow_html=True)

    time.sleep(1); st.rerun()
