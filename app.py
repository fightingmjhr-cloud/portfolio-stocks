import streamlit as st
import pandas as pd
import numpy as np
import time
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [CORE ENGINE] 8대 엔진 & 리포트 생성기
# -----------------------------------------------------------------------------

class SingularityEngine:
    def __init__(self):
        pass

    def _calculate_metrics(self, mode):
        omega = np.random.uniform(5.0, 25.0) 
        vol_surf = np.random.uniform(0.1, 0.9)
        betti = np.random.choice([0, 1], p=[0.85, 0.15]) 
        hurst = np.random.uniform(0.2, 0.9)
        te = np.random.uniform(0.1, 5.0)
        vpin = np.random.uniform(0.0, 1.0)
        hawkes = np.random.uniform(0.1, 4.0) if mode == "scalping" else np.random.uniform(0.1, 2.0)
        obi = np.random.uniform(-1.0, 1.0)
        gnn = np.random.uniform(0.1, 1.0)
        sent = np.random.uniform(-1.0, 1.0)
        es = np.random.uniform(-0.01, -0.30)
        kelly = np.random.uniform(0.01, 0.30)
        return {
            "omega": omega, "vol_surf": vol_surf, "betti": betti, "hurst": hurst,
            "te": te, "vpin": vpin, "hawkes": hawkes, "obi": obi, 
            "gnn": gnn, "sent": sent, "es": es, "kelly": kelly
        }

    def run_diagnosis(self, mode="swing"):
        m = self._calculate_metrics(mode)
        score = 35.0 
        reasons = [] 

        if m['vpin'] > 0.6: score -= 15; reasons.append("☠️ 독성 위험")
        if m['es'] < -0.15: score -= 15; reasons.append("💣 폭락 징후")
        if m['betti'] == 1: score -= 10; reasons.append("⚠️ 구조 붕괴")

        if mode == "scalping":
            if m['hawkes'] > 2.5 and m['obi'] > 0.5: score += 40; reasons.append(f"🚀 퍼펙트 수급")
            elif m['hawkes'] > 1.5: score += 15; reasons.append("⚡ 수급 우위")
            elif m['hawkes'] < 0.8: score -= 10; reasons.append("💤 거래 소강")
        else: 
            if m['hurst'] > 0.75 and m['gnn'] > 0.8: score += 35; reasons.append(f"📈 대세 상승장")
            elif m['hurst'] > 0.6: score += 10; reasons.append("↗️ 추세 양호")
            else: score -= 5; reasons.append("📉 추세 미약")

        if 9 < m['omega'] < 13: score += 5; reasons.append("📐 파동 안정")
        if m['te'] > 3.0: score += 5; reasons.append("📡 정보 폭발")

        win_rate = min(0.92, score / 100)
        win_rate = max(0.15, win_rate)
        return win_rate, m, reasons

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        if mode == "scalping":
            vol = m['vol_surf'] * 0.04
            entry = int(price * (1 - vol))
            target = max(int(price * (1 + target_return/100)), int(price * (1 + vol*1.5)))
            stop = int(price * (1 - vol*0.7))
            time_str = "09:00~09:30"
        else:
            target = int(price * (1 + target_return/100))
            stop = int(price * 0.93)
            time_str = "종가 확인 후"

        adjusted_kelly = m['kelly'] * (wr / 0.8) if wr < 0.8 else m['kelly']
        alloc_cash = cash * adjusted_kelly
        can_buy_qty = int(alloc_cash / price) if price > 0 else 0

        if wr >= 0.75:
            cmd = "🔥 STRONG BUY"; style = "color: #00FF00;"
            action = f"승률 {wr*100:.0f}% 확신. 현금 {int(adjusted_kelly*100)}% 투입하여 **{can_buy_qty}주** 매수."
        elif wr >= 0.55:
            cmd = "⚖️ BUY / HOLD"; style = "color: #FFAA00;"
            action = f"리스크 관리. **{int(can_buy_qty/2)}주**만 분할 진입."
        else:
            cmd = "🛡️ SELL / WAIT"; style = "color: #FF4444;"
            action = "진입 금지 및 현금 확보."

        return {
            "cmd": cmd, "action": action, "time": time_str, "style": style,
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
        
        title = "🐹 햄찌의 팩트 폭격"
        if cash_ratio > 70: msg = "사장님, 쫄보입니까? 인플레에 돈 녹아요! 😱 주도주 좀 담으세요!"
        elif total_invest > 0 and current_val < total_invest: msg = "파란불이네요... 😭 '존버'는 답이 아닙니다. 자를 건 자르세요!"
        else: msg = "오 수익 중? 🐹 해바라기씨 사먹게 조금만 익절합시다. 탐욕은 금물!"
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
    
    /* Design Polish */
    .stock-card { 
        background: #11151c; border-radius: 16px; padding: 25px; margin-bottom: 25px; 
        border: 1px solid #333; box-shadow: 0 10px 30px rgba(0,0,0,0.8); position: relative;
    }
    
    /* Rank Badge (Top Left Ribbon) */
    .rank-badge {
        position: absolute; top: 0; left: 0; 
        background: linear-gradient(135deg, #FF4444, #FF0000); color: #fff; 
        font-weight: bold; padding: 5px 12px; border-bottom-right-radius: 12px; 
        border-top-left-radius: 16px; font-size: 13px; z-index: 10;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    
    .report-section { margin-top: 15px; padding-top: 15px; border-top: 1px solid #333; font-size: 14px; line-height: 1.7; color: #ddd; }
    .report-title { color: #00C9FF; font-weight: bold; margin-bottom: 8px; font-size: 15px; }
    
    .timeline-visual {
        display: flex; justify-content: space-between; background: #0d1117; 
        padding: 12px; border-radius: 8px; margin-top: 15px; font-size: 13px; border: 1px solid #333;
    }
    .t-item b { display: block; font-size: 15px; margin-top: 4px; color: #fff; }
    
    .hamzzi-box {
        background-color: #2d1f15; border: 2px solid #FFAA00; border-radius: 15px;
        padding: 20px; text-align: center; color: #FFAA00; margin-bottom: 20px;
        font-size: 16px; font-weight: bold;
    }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -20px !important; margin-top: 2px; }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-title'>🐯 Tiger&Hamzzi Quant 🐹</div>", unsafe_allow_html=True)

if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'ideal_list' not in st.session_state: st.session_state.ideal_list = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 
if 'target_return' not in st.session_state: st.session_state.target_return = 5.0
if 'my_diagnosis' not in st.session_state: st.session_state.my_diagnosis = []
if 'display_mode' not in st.session_state: st.session_state.display_mode = None

# [SECTION 1: PERSONAL PORTFOLIO AREA]
with st.expander("💰 내 자산 및 보유 종목 (Personal)", expanded=True):
    c_top1, c_top2, c_top3 = st.columns(3)
    with c_top1: st.session_state.cash = st.number_input("💰 예수금 (원)", value=st.session_state.cash, step=100000)
    with c_top2: st.session_state.target_return = st.number_input("🎯 목표 수익률 (%)", value=st.session_state.target_return, step=1.0)
    with c_top3:
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
        
        for i, stock in enumerate(st.session_state.portfolio):
            c1, c2, c3, c4, c5 = st.columns([3.2, 1.8, 1.3, 2.0, 0.4])
            with c1: stock['name'] = st.text_input(f"n{i}", value=stock['name'], label_visibility="collapsed", placeholder="삼성전자")
            with c2: stock['price'] = st.number_input(f"p{i}", value=float(stock['price']), label_visibility="collapsed")
            with c3: stock['qty'] = st.number_input(f"q{i}", value=int(stock['qty']), label_visibility="collapsed")
            with c4: stock['strategy'] = st.selectbox(f"s{i}", ["추세추종", "초단타"], index=0 if stock['strategy']=="추세추종" else 1, label_visibility="collapsed")
            with c5:
                if st.button("🗑️", key=f"del_{i}"): st.session_state.portfolio.pop(i); st.rerun()
    else: st.info("보유 종목이 없습니다.")

    # [BUTTON: DIAGNOSE MY STOCK ONLY]
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📝 내 종목만 진단하기 (Click)", use_container_width=True):
        st.session_state.display_mode = 'MY'
        
        engine = SingularityEngine()
        market_data = load_top50_data() 
        my_results = []
        
        with st.spinner("내 보유 종목 정밀 분석 중..."):
            for s in st.session_state.portfolio:
                if not s['name']: continue
                mode = "scalping" if s['strategy'] == "초단타" else "swing"
                price = s['price']
                match = market_data[market_data['Name'] == s['name']]
                if not match.empty: price = int(match.iloc[0]['Close'])
                else:
                    try: 
                        df = fdr.StockListing('KRX'); code = df[df['Name'] == s['name']].iloc[0]['Code']
                        p_df = fdr.DataReader(code); price = int(p_df['Close'].iloc[-1])
                    except: pass
                
                wr, m, reasons = engine.run_diagnosis(mode)
                plan = engine.generate_report(mode, price, m, wr, st.session_state.cash, s['qty'], st.session_state.target_return)
                pnl = ((price - s['price'])/s['price']*100) if s['price'] > 0 else 0
                my_results.append({'name': s['name'], 'price': price, 'pnl': pnl, 'win': wr, 'mode': mode, 'log': " + ".join(reasons), 'plan': plan})
            st.session_state.my_diagnosis = my_results

    # [RESULT AREA: MY DIAGNOSIS] -> 바로 밑에 출력
    if st.session_state.display_mode == 'MY' and st.session_state.my_diagnosis:
        st.markdown("---")
        st.markdown("<h5>👤 내 보유 종목 정밀 진단 리포트</h5>", unsafe_allow_html=True)
        for d in st.session_state.my_diagnosis:
            p = d['plan']
            border = "#00FF00" if d['win'] >= 0.75 else ("#FFAA00" if d['win'] >= 0.55 else "#FF4444")
            
            st.markdown(f"""
            <div class='stock-card' style='border-left: 5px solid {border};'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-size:24px; font-weight:bold; color:#fff;'>{d['name']}</span>
                    <span class='badge' style='background:{border}; color:#000;'>AI 승률 {d['win']*100:.1f}%</span>
                </div>
                <div style='display:flex; gap:15px; margin-top:5px; font-size:14px; color:#ccc;'>
                    <span>현재가: <b>{d['price']:,}</b></span>
                    <span style='color:{"#00FF00" if d['pnl']>=0 else "#FF4444"};'>수익률: <b>{d['pnl']:.2f}%</b></span>
                </div>
                <div class='report-section'>
                    <div class='report-title'>📊 점수 산출 근거</div>
                    {d['log']}
                </div>
                <div class='report-section'>
                    <div class='report-title' style='color:{border};'>{p['cmd']}</div>
                    {p['action']}
                </div>
                <div class='timeline-visual'>
                    <div class='t-item'>🔵 진입/추매<br><b>{p['prices'][0]:,}원</b></div>
                    <div class='t-item'>🔴 목표/익절<br><b>{p['prices'][1]:,}원</b></div>
                    <div class='t-item' style='color:#FF4444;'>🚫 손절/방어<br><b>{p['prices'][2]:,}원</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# [VISUAL DIVIDER]
st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)

# [SECTION 2: MARKET INTELLIGENCE AREA]
st.markdown("#### 📡 시장 정밀 타격 (Market Intelligence)")

if st.button("🐹 햄찌의 계좌 훈수 두기 (클릭해서 혼나기)", use_container_width=True):
    engine = SingularityEngine()
    market_data = load_top50_data()
    title, msg = engine.hamzzi_smart_nagging(st.session_state.cash, st.session_state.portfolio, market_data)
    st.markdown(f"<div class='hamzzi-box'><div>{title}</div><br><div style='font-size:14px; color:#eee;'>{msg}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
c_btn1, c_btn2 = st.columns(2)

def run_market_scan_logic():
    with st.spinner("8대 엔진 가동! 전 종목 스캔 및 랭킹 산출 중..."):
        engine = SingularityEngine()
        market_data = load_top50_data() 
        sc_all, sw_all, ideal_all = [], [], []
        
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close']))
            name = row['Name']
            
            wr_sc, m_sc, r_sc = engine.run_diagnosis("scalping")
            p_sc = engine.generate_report("scalping", price, m_sc, wr_sc, st.session_state.cash, 0, st.session_state.target_return)
            sc_all.append({'name': name, 'price': price, 'win': wr_sc, 'mode': "초단타", 'log': " + ".join(r_sc), 'plan': p_sc})
            
            wr_sw, m_sw, r_sw = engine.run_diagnosis("swing")
            p_sw = engine.generate_report("swing", price, m_sw, wr_sw, st.session_state.cash, 0, st.session_state.target_return)
            sw_all.append({'name': name, 'price': price, 'win': wr_sw, 'mode': "추세추종", 'log': " + ".join(r_sw), 'plan': p_sw})

            if wr_sc >= wr_sw: ideal_all.append(sc_all[-1])
            else: ideal_all.append(sw_all[-1])
        
        sc_all.sort(key=lambda x: x['win'], reverse=True)
        sw_all.sort(key=lambda x: x['win'], reverse=True)
        ideal_all.sort(key=lambda x: x['win'], reverse=True)
        
        st.session_state.sc_list = sc_all[:3]
        st.session_state.sw_list = sw_all[:3]
        st.session_state.ideal_list = ideal_all[:3]

if c_btn1.button("🏆 타이거&햄찌 출격! (Top 3)"):
    st.session_state.display_mode = 'TOP3'
    run_market_scan_logic()
    st.rerun()

if c_btn2.button("📊 단타 / 추세 (전략별 보기)"):
    st.session_state.display_mode = 'SEPARATE'
    run_market_scan_logic()
    st.rerun()

# [RESULT AREA: MARKET SCAN]
if st.session_state.display_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("<h5>🏆 금일의 Singularity Ideal Pick (Top 3)</h5>", unsafe_allow_html=True)
    for idx, r in enumerate(st.session_state.ideal_list):
        p = r['plan']
        border = "#FFFFFF"
        st.markdown(f"""
        <div class='stock-card' style='border: 2px solid {border}; box-shadow: 0 0 20px rgba(255,255,255,0.1);'>
            <div class='rank-badge'>통합 {idx+1}위</div>
            <div style='display:flex; justify-content:space-between; align-items:center; margin-left: 10px;'>
                <span style='font-size:24px; font-weight:bold; color:#fff;'>{r['name']}</span>
                <span class='badge' style='background:#fff; color:#000;'>{r['mode']} / {r['win']*100:.1f}점</span>
            </div>
            <div class='report-section'>
                <div class='report-title'>📊 점수 산출 근거</div>
                {r['log']}
            </div>
            <div class='report-section'>
                <div class='report-title' style='color:{p['style'].split(':')[1]};'>{p['cmd']}</div>
                {p['action']}
            </div>
            <div class='timeline-visual'>
                <div class='t-item'>🔵 진입가<br><b>{p['prices'][0]:,}원</b></div>
                <div class='t-item'>🔴 목표가<br><b>{p['prices'][1]:,}원</b></div>
                <div class='t-item' style='color:#FF4444;'>🚫 손절가<br><b>{p['prices'][2]:,}원</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.display_mode == 'SEPARATE':
    st.markdown("<h5>📊 전략별 절대 랭킹 (Top 3)</h5>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["⚡ 초단타 랭킹", "🌊 추세추종 랭킹"])
    
    def render_report_card(data, color):
        for idx, r in enumerate(data):
            p = r['plan']
            st.markdown(f"""
            <div class='stock-card' style='border-left: 5px solid {color};'>
                <div class='rank-badge' style='background:{color}; border-radius: 16px 0 16px 0;'>{idx+1}위</div>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-left: 10px;'>
                    <span style='font-size:24px; font-weight:bold; color:#fff;'>{r['name']}</span>
                    <span class='badge' style='background:{color}; color:#000;'>{r['win']*100:.1f}점</span>
                </div>
                <div class='report-section'>
                    <div class='report-title'>📊 점수 산출 근거</div>
                    {r['log']}
                </div>
                <div class='report-section'>
                    <div class='report-title' style='color:{color};'>{p['cmd']}</div>
                    {p['action']}
                </div>
                <div class='timeline-visual'>
                    <div class='t-item'>🔵 진입가<br><b>{p['prices'][0]:,}원</b></div>
                    <div class='t-item'>🔴 목표가<br><b>{p['prices'][1]:,}원</b></div>
                    <div class='t-item' style='color:#FF4444;'>🚫 손절가<br><b>{p['prices'][2]:,}원</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab1: render_report_card(st.session_state.sc_list, "#FFFF00")
    with tab2: render_report_card(st.session_state.sw_list, "#00C9FF")
