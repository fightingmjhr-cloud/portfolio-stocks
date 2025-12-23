import streamlit as st
import pandas as pd
import numpy as np
import time
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [CORE ENGINE] 8대 엔진 (Apocalypse Standard + User Target)
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

    # [CRITICAL LOGIC] 보수적 승률 산정
    def run_diagnosis(self, mode="swing"):
        m = self._calculate_metrics(mode)
        score = 35.0 
        reasons = [] 

        # Penalties
        if m['vpin'] > 0.6: score -= 15; reasons.append("☠️ 독성매물 위험")
        if m['es'] < -0.15: score -= 15; reasons.append("💣 폭락 징후")
        if m['betti'] == 1: score -= 10; reasons.append("⚠️ 구조적 붕괴")

        # Bonuses
        if mode == "scalping":
            if m['hawkes'] > 2.5 and m['obi'] > 0.5 and m['vpin'] < 0.3:
                score += 40; reasons.append(f"🚀 퍼펙트 수급({m['hawkes']:.1f})")
            elif m['hawkes'] > 1.5 and m['obi'] > 0.2:
                score += 15; reasons.append("⚡ 수급 우위")
            elif m['hawkes'] < 0.8:
                score -= 10; reasons.append("💤 거래 소강")
        else: 
            if m['hurst'] > 0.75 and m['gnn'] > 0.8:
                score += 35; reasons.append(f"📈 대세 상승장({m['hurst']:.2f})")
            elif m['hurst'] > 0.6:
                score += 10; reasons.append("↗️ 추세 양호")
            else:
                score -= 5; reasons.append("📉 추세 미약")

        # Common
        if 9 < m['omega'] < 13: score += 5; reasons.append("📐 파동 안정")
        if m['te'] > 3.0: score += 5; reasons.append("📡 정보 폭발")

        win_rate = min(0.92, score / 100)
        win_rate = max(0.15, win_rate)
        
        return win_rate, m, reasons

    # 자산 배분 (사용자 목표 수익률 반영)
    def generate_asset_plan(self, mode, price, m, wr, cash, current_qty, user_target_pct):
        adjusted_kelly = m['kelly'] * (wr / 0.8) if wr < 0.8 else m['kelly']
        alloc_cash = cash * adjusted_kelly
        can_buy_qty = int(alloc_cash / price) if price > 0 else 0
        
        # 목표가 설정 (사용자 입력 반영)
        target_mult = 1 + (user_target_pct / 100)
        
        if mode == "scalping":
            vol = m['vol_surf'] * 0.04
            entry = int(price * (1 - vol))
            # 목표가는 사용자가 설정한 것과 변동성 중 큰 값 선택
            target = max(int(price * target_mult), int(price * (1 + vol*1.5)))
            stop = int(price * (1 - vol*0.7))
            time = "09:00 ~ 10:00 (초집중)"
        else:
            target = int(price * target_mult)
            stop = int(price * 0.93)
            time = "종가 확인 후 대응"

        if wr >= 0.75:
            cmd = "🔥 STRONG BUY"
            style = "color: #00FF00;"
            msg = f"승률 {wr*100:.0f}%의 기회입니다. 현금의 {int(adjusted_kelly*100)}%를 투입하여 **{can_buy_qty}주**를 매수하십시오."
        elif wr >= 0.55:
            cmd = "⚖️ BUY / HOLD"
            style = "color: #FFAA00;"
            msg = f"리스크가 존재합니다. **{int(can_buy_qty/2)}주** 정도만 분할 진입하여 평단을 관리하십시오."
        else:
            cmd = "🛡️ SELL / WAIT"
            style = "color: #FF4444;"
            msg = f"현재 승률({wr*100:.0f}%)이 낮습니다. **진입 금지** 및 현금 보유가 최선의 전략입니다."

        return {
            "cmd": cmd, "msg": msg, "time": time, "style": style,
            "prices": (entry if mode=='scalping' else price, target, stop),
            "qty_guide": can_buy_qty
        }

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
    
    /* Button Styling */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 55px; font-size: 18px;
        background: linear-gradient(135deg, #00C9FF, #92FE9D); border: none; color: #000;
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.2); transition: 0.2s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    
    /* Card Design */
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
    
    .timeline-visual {
        display: flex; justify-content: space-between; background: #0d1117; 
        padding: 10px; border-radius: 8px; margin-top: 10px; font-size: 12px; color: #aaa;
    }
    .t-item b { color: #fff; font-size: 13px; }
    
    .rank-badge {
        position: absolute; top: 10px; right: 10px; 
        background: #FF4444; color: #fff; font-weight: bold; padding: 5px 10px; border-radius: 20px; font-size: 12px;
        box-shadow: 0 0 10px rgba(255,0,0,0.5); z-index: 10;
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

    /* Delete Button Alignment */
    div[data-testid="column"]:nth-child(5) { margin-left: -20px !important; margin-top: 2px; }
    
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-title'>🐯 Tiger&Hamzzi Quant 🐹</div>", unsafe_allow_html=True)

# [SESSION STATE]
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'ideal_list' not in st.session_state: st.session_state.ideal_list = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 
if 'target_return' not in st.session_state: st.session_state.target_return = 5.0
if 'display_mode' not in st.session_state: st.session_state.display_mode = None

# [INPUT PANEL: 3-Column Layout]
with st.expander("💰 자산 및 포트폴리오 관리", expanded=True):
    # 상단 3분할: 예수금 / 목표수익 / 종목추가
    c_top1, c_top2, c_top3 = st.columns(3)
    
    with c_top1:
        st.session_state.cash = st.number_input("💰 예수금 (원)", value=st.session_state.cash, step=100000)
    with c_top2:
        st.session_state.target_return = st.number_input("🎯 목표 수익률 (%)", value=st.session_state.target_return, step=1.0)
    with c_top3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True) # Spacer
        if st.button("➕ 종목 추가", use_container_width=True):
            st.session_state.portfolio.append({'name': '', 'price': 0, 'qty': 0, 'strategy': '추세추종'})
            st.rerun()
            
    st.markdown("---")
    
    # 보유 종목 리스트
    if not st.session_state.portfolio:
        st.info("보유 종목이 없습니다. 상단의 '➕ 종목 추가' 버튼을 눌러주세요.")
    else:
        # 헤더
        h1, h2, h3, h4, h5 = st.columns([3.2, 1.8, 1.3, 2.0, 0.4])
        h1.markdown("<small style='color:#888'>종목명</small>", unsafe_allow_html=True)
        h2.markdown("<small style='color:#888'>평단가</small>", unsafe_allow_html=True)
        h3.markdown("<small style='color:#888'>수량</small>", unsafe_allow_html=True)
        h4.markdown("<small style='color:#888'>전략</small>", unsafe_allow_html=True)
        
        # 리스트 루프
        for i, stock in enumerate(st.session_state.portfolio):
            c1, c2, c3, c4, c5 = st.columns([3.2, 1.8, 1.3, 2.0, 0.4])
            with c1: stock['name'] = st.text_input(f"n{i}", value=stock['name'], label_visibility="collapsed", placeholder="삼성전자")
            with c2: stock['price'] = st.number_input(f"p{i}", value=float(stock['price']), label_visibility="collapsed")
            with c3: stock['qty'] = st.number_input(f"q{i}", value=int(stock['qty']), label_visibility="collapsed")
            with c4: stock['strategy'] = st.selectbox(f"s{i}", ["추세추종", "초단타"], index=0 if stock['strategy']=="추세추종" else 1, label_visibility="collapsed")
            with c5:
                if st.button("🗑️", key=f"del_{i}"): st.session_state.portfolio.pop(i); st.rerun()

# [DUAL LAUNCH BUTTONS]
st.markdown("<br>", unsafe_allow_html=True)
c_btn1, c_btn2 = st.columns(2)

def run_full_scan():
    with st.spinner("8대 엔진 정밀 분석 중... (지구 멸망급 안전마진 적용)"):
        engine = SingularityEngine()
        market_data = load_top50_data() 
        
        # 1. 내 종목
        my_results = []
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
            plan = engine.generate_asset_plan(mode, price, m, wr, st.session_state.cash, s['qty'], st.session_state.target_return)
            pnl = ((price - s['price'])/s['price']*100) if s['price'] > 0 else 0
            my_results.append({'name': s['name'], 'price': price, 'pnl': pnl, 'win': wr, 'mode': mode, 'm': m, 'reasons': reasons, 'plan': plan})
        st.session_state.my_diagnosis = my_results

        # 2. 랭킹 스캔
        sc_all, sw_all, ideal_all = [], [], []
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close']))
            name = row['Name']
            
            wr_sc, m_sc, r_sc = engine.run_diagnosis("scalping")
            plan_sc = engine.generate_asset_plan("scalping", price, m_sc, wr_sc, st.session_state.cash, 0, st.session_state.target_return)
            sc_all.append({'name': name, 'price': price, 'win': wr_sc, 'mode': "초단타", 'm': m_sc, 'reasons': r_sc, 'plan': plan_sc})
            
            wr_sw, m_sw, r_sw = engine.run_diagnosis("swing")
            plan_sw = engine.generate_asset_plan("swing", price, m_sw, wr_sw, st.session_state.cash, 0, st.session_state.target_return)
            sw_all.append({'name': name, 'price': price, 'win': wr_sw, 'mode': "추세추종", 'm': m_sw, 'reasons': r_sw, 'plan': plan_sw})

            if wr_sc >= wr_sw: ideal_all.append(sc_all[-1])
            else: ideal_all.append(sw_all[-1])
        
        sc_all.sort(key=lambda x: x['win'], reverse=True)
        sw_all.sort(key=lambda x: x['win'], reverse=True)
        ideal_all.sort(key=lambda x: x['win'], reverse=True)
        
        st.session_state.sc_list = sc_all[:3]
        st.session_state.sw_list = sw_all[:3]
        st.session_state.ideal_list = ideal_all[:3]

# Left: Top 3
if c_btn1.button("🐯 타이거&햄찌 출격! (Top 3) 🐹"):
    st.session_state.running = True
    st.session_state.display_mode = 'TOP3'
    run_full_scan()
    st.rerun()

# Right: Separate
if c_btn2.button("🐯 단타 / 추세 (전략별 보기) 🐹"):
    st.session_state.running = True
    st.session_state.display_mode = 'SEPARATE'
    run_full_scan()
    st.rerun()

# [DISPLAY]
st.markdown("---")

if st.session_state.get('running'):
    
    # 1. My Stocks
    if 'my_diagnosis' in st.session_state and st.session_state.my_diagnosis:
        st.markdown("<h5>👤 내 보유 종목 정밀 진단</h5>", unsafe_allow_html=True)
        for d in st.session_state.my_diagnosis:
            p = d['plan']
            border = "#00FF00" if d['win'] >= 0.75 else ("#FFAA00" if d['win'] >= 0.55 else "#FF4444")
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
                    <div style='display:flex; justify-content:space-between; font-weight:bold; color:{p['style'].split(':')[1]}; margin-bottom:10px;'>
                        <span>{p['cmd']}</span><span>{p['time']}</span>
                    </div>
                    <div style='color:#eee; line-height:1.6;'>{p['msg']}</div>
                    <div class='timeline-visual'>
                        <div class='t-item'>🔵 진입/추매<br><b>{p['prices'][0]:,}원</b></div>
                        <div class='t-item'>🔴 목표/익절<br><b>{p['prices'][1]:,}원</b></div>
                        <div class='t-item' style='color:#FF4444;'>🚫 손절/방어<br><b>{p['prices'][2]:,}원</b></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander(f"🔍 {d['name']} - 8대 엔진 HUD"):
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

    # 2. Case A: Top 3
    if st.session_state.display_mode == 'TOP3' and st.session_state.ideal_list:
        st.markdown("<br><h5>🏆 오늘의 Singularity Ideal Pick (Top 3)</h5>", unsafe_allow_html=True)
        st.info("💡 전략(초단타/추세) 구분 없이 8대 엔진 점수가 가장 높은 절대 강자들입니다.")
        for idx, r in enumerate(st.session_state.ideal_list):
            p = r['plan']
            border = "#FFFFFF"
            badges = "".join([f"<span class='logic-badge'>{rea}</span>" for rea in r['reasons']])
            st.markdown(f"""
            <div class='stock-card' style='border: 2px solid {border}; box-shadow: 0 0 15px rgba(255,255,255,0.15);'>
                <div class='rank-badge' style='background:#fff; color:#000;'>통합 {idx+1}위</div>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-size:24px; font-weight:bold; color:#fff;'>{r['name']}</span>
                    <span class='badge' style='background:#fff; color:#000;'>{r['mode']} / {r['win']*100:.1f}점</span>
                </div>
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
                    <div class='hud-item'><span class='hud-label'>켈리비중</span><span class='hud-val'>{m['kelly']:.2f}</span></div>
                </div>
                """, unsafe_allow_html=True)

    # 3. Case B: Separate
    elif st.session_state.display_mode == 'SEPARATE':
        st.markdown("<br><h5>📊 전략별 절대 랭킹 (Top 3)</h5>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["⚡ 초단타 랭킹", "🌊 추세추종 랭킹"])
        
        def render_rec(data, color):
            for idx, r in enumerate(data):
                p = r['plan']
                badges = "".join([f"<span class='logic-badge'>{rea}</span>" for rea in r['reasons']])
                st.markdown(f"""
                <div class='stock-card' style='border-left: 5px solid {color};'>
                    <div class='rank-badge' style='background:{color}; color:#000;'>{idx+1}위</div>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <span style='font-size:22px; font-weight:bold; color:#fff;'>{r['name']}</span>
                        <span class='badge' style='background:{color}; color:#000;'>{r['win']*100:.1f}%</span>
                    </div>
                    <div style='margin-top:10px;'>{badges}</div>
                    <div class='action-section' style='border-left-color: {color};'>
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
                        <div class='hud-item'><span class='hud-label'>켈리비중</span><span class='hud-val'>{m['kelly']:.2f}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

        with tab1: render_rec(st.session_state.sc_list, "#FFFF00")
        with tab2: render_rec(st.session_state.sw_list, "#00C9FF")

else:
    st.info("👆 상단의 버튼을 눌러 시장을 정밀 타격하십시오.")
