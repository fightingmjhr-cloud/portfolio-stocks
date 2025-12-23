import streamlit as st
import pandas as pd
import numpy as np
import time
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [CORE ENGINE] 8대 엔진 & 정밀 분석 리포트 생성기
# -----------------------------------------------------------------------------

class SingularityEngine:
    def __init__(self):
        pass

    # [1] 8대 엔진 데이터 생성 (시뮬레이션)
    def _calculate_metrics(self, mode):
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
        
        return {
            "omega": omega, "vol_surf": vol_surf, "betti": betti, "hurst": hurst,
            "te": te, "vpin": vpin, "hawkes": hawkes, "obi": obi, 
            "gnn": gnn, "sent": sent, "es": es, "kelly": kelly
        }

    # [2] 승률 산출 및 근거 로그 작성 (Logic Trace)
    def run_diagnosis(self, mode="swing"):
        m = self._calculate_metrics(mode)
        score = 35.0 
        calc_log = ["기본점수(35)"] # 점수 계산 과정 기록

        # Penalties
        if m['vpin'] > 0.6: score -= 15; calc_log.append("독성매물(-15)")
        if m['es'] < -0.15: score -= 15; calc_log.append("폭락징후(-15)")
        if m['betti'] == 1: score -= 10; calc_log.append("구조붕괴(-10)")

        # Bonuses
        if mode == "scalping":
            if m['hawkes'] > 2.5 and m['obi'] > 0.5:
                score += 40; calc_log.append("퍼펙트수급(+40)")
            elif m['hawkes'] > 1.5:
                score += 15; calc_log.append("수급우위(+15)")
            elif m['hawkes'] < 0.8:
                score -= 10; calc_log.append("거래소강(-10)")
        else: 
            if m['hurst'] > 0.75 and m['gnn'] > 0.8:
                score += 35; calc_log.append("대세상승(+35)")
            elif m['hurst'] > 0.6:
                score += 10; calc_log.append("추세양호(+10)")
            else:
                score -= 5; calc_log.append("추세미약(-5)")

        # Common
        if 9 < m['omega'] < 13: score += 5; calc_log.append("파동안정(+5)")
        if m['te'] > 3.0: score += 5; calc_log.append("정보폭발(+5)")

        win_rate = min(0.92, score / 100)
        win_rate = max(0.15, win_rate)
        
        # 근거 텍스트 생성
        calc_str = " + ".join(calc_log) + f" = <b>{int(score)}점</b>"
        
        return win_rate, m, calc_str

    # [3] 심층 분석 리포트 생성 (Deep Analyst)
    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        # A. 가격 및 타임라인 설정
        if mode == "scalping":
            vol = m['vol_surf'] * 0.04
            entry = int(price * (1 - vol))
            target = max(int(price * (1 + target_return/100)), int(price * (1 + vol*1.5)))
            stop = int(price * (1 - vol*0.7))
            time_str = "09:00~09:30 (골든타임)"
        else:
            target = int(price * (1 + target_return/100))
            stop = int(price * 0.93)
            time_str = "15:20 (종가 베팅) 혹은 5일선 터치 시"

        # B. 켈리 베팅 자금 산출
        adjusted_kelly = m['kelly'] * (wr / 0.8) if wr < 0.8 else m['kelly']
        alloc_cash = cash * adjusted_kelly
        can_buy_qty = int(alloc_cash / price) if price > 0 else 0

        # C. 상세 분석 텍스트 (Micro-Level Analysis)
        analysis_text = ""
        if mode == "scalping":
            if wr >= 0.75:
                analysis_text = f"""
                <b>[📈 기술적 프로파일링]</b> 현재 Hawkes 지수가 {m['hawkes']:.2f}로 임계치를 초과했습니다. 이는 단순 반등이 아니라, '자기 여진(Self-Exciting)'에 의한 2차, 3차 수급 폭발이 임박했음을 시사합니다. 특히 호가창 불균형(OBI)이 {m['obi']:.2f}로 매수벽이 두터워 하방 경직성이 매우 강합니다.<br><br>
                <b>[🌊 유동성 분석]</b> VPIN(독성 유동성)이 {m['vpin']:.2f}로 매우 낮습니다. 이는 현재 거래량이 기관이나 스마트 머니의 매집일 가능성이 높으며, 개미 털기성 속임수 패턴이 아님을 의미합니다.
                """
            else:
                analysis_text = f"""
                <b>[📉 리스크 분석]</b> 수급은 일부 보이나 VPIN이 {m['vpin']:.2f}로 높습니다. 이는 고점에서 물량을 떠넘기는 '설거지' 패턴일 수 있습니다. 변동성 표면(Vol Surface)이 불안정하여 급락 위험이 큽니다.
                """
        else: # Swing
            if wr >= 0.75:
                analysis_text = f"""
                <b>[📈 추세 분석]</b> 허스트 지수(Hurst Exponent)가 {m['hurst']:.2f}를 기록했습니다. 이는 주가가 랜덤워크를 벗어나 강력한 '기억(Memory)'을 가지고 추세를 지속하려는 성질이 극대화된 상태입니다. JLS 파동 모델상 로그 주기 진동수도 {m['omega']:.1f}로 붕괴 위험 없이 안정적입니다.<br><br>
                <b>[🌐 네트워크 분석]</b> GNN 중심성 지표가 {m['gnn']:.2f}로 시장 주도주(Key Player)의 지위를 차지하고 있습니다. 주변 종목들이 이 종목의 등락을 따라가는 선행성을 보입니다.
                """
            else:
                analysis_text = f"""
                <b>[⏳ 조정 분석]</b> 상승 추세가 꺾이지는 않았으나, 단기 과열권에 진입했습니다. 위상수학적 구멍(Betti Number)이 감지되어 추세의 연결성이 잠시 끊길 수 있는 조정 구간입니다.
                """

        # D. 실전 행동 강령 (Action Script)
        if wr >= 0.75:
            cmd = "🔥 STRONG BUY (공격적 진입)"
            style = "color: #00FF00;"
            action_guide = f"""
            1. <b>진입:</b> 시초가 갭이 3% 이하라면 <b>시장가로 {int(can_buy_qty*0.5)}주 선진입</b>하십시오. 나머지 물량은 {entry:,}원 부근 눌림목에 걸어두세요.<br>
            2. <b>홀딩:</b> 수익률 {target_return}% 도달 전까지는 웬만한 흔들림에 매도하지 마십시오.<br>
            3. <b>멘탈:</b> 지금은 공포를 살 때가 아니라 탐욕을 부릴 때입니다.
            """
        elif wr >= 0.55:
            cmd = "⚖️ BUY / HOLD (분할 대응)"
            style = "color: #FFAA00;"
            action_guide = f"""
            1. <b>진입:</b> 섣불리 덤비지 마십시오. 호가창 매수 잔량이 매도 잔량을 압도하는 순간 <b>{int(can_buy_qty/3)}주씩 3분할</b>로 접근하세요.<br>
            2. <b>대응:</b> {entry:,}원을 지지하지 못하면 즉시 관망세로 전환하십시오.<br>
            3. <b>비중:</b> 전체 시드의 20%를 넘기지 않는 것이 좋습니다.
            """
        else:
            cmd = "🛡️ SELL / WAIT (현금 확보)"
            style = "color: #FF4444;"
            action_guide = f"""
            1. <b>청산:</b> 보유 중이라면 반등 시마다 물량을 줄이십시오. 지금은 <b>현금이 가장 좋은 종목</b>입니다.<br>
            2. <b>관망:</b> 차라리 맛있는 것을 사 드시고 HTS를 끄십시오. 이길 수 없는 싸움입니다.<br>
            3. <b>조건:</b> 최소한 Hawkes 지수가 1.5 이상으로 올라올 때까지 진입 금지입니다.
            """

        return {
            "cmd": cmd, "analysis": analysis_text, "action": action_guide, 
            "time": time_str, "style": style, "score_log": m,
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
    
    /* Button */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 50px; font-size: 18px;
        background: linear-gradient(135deg, #00C9FF, #92FE9D); border: none; color: #000;
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.2);
    }
    
    /* Stock Card (Premium Report Style) */
    .stock-card { 
        background: #11151c; border-radius: 16px; padding: 25px; margin-bottom: 25px; 
        border: 1px solid #2d333b; box-shadow: 0 8px 30px rgba(0,0,0,0.8); position: relative;
    }
    
    /* Rank Ribbon */
    .rank-badge {
        position: absolute; top: 0; left: 0; 
        background: linear-gradient(135deg, #FF4444, #FF0000); color: #fff; 
        font-weight: bold; padding: 6px 15px; border-bottom-right-radius: 15px; 
        border-top-left-radius: 16px; font-size: 14px; z-index: 10;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.5);
    }
    
    /* Sections inside Card */
    .report-section {
        margin-top: 15px; padding-top: 15px; border-top: 1px solid #333; font-size: 14px; line-height: 1.7; color: #ddd;
    }
    .report-title { color: #00C9FF; font-weight: bold; margin-bottom: 8px; font-size: 15px; }
    
    /* Timeline Visual */
    .timeline-visual {
        display: flex; justify-content: space-between; background: #0d1117; 
        padding: 12px; border-radius: 8px; margin-top: 15px; font-size: 13px; border: 1px solid #333;
    }
    .t-item { text-align: center; }
    .t-item b { display: block; font-size: 15px; margin-top: 4px; color: #fff; }
    
    /* Hamzzi */
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

# [SESSION STATE]
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'ideal_list' not in st.session_state: st.session_state.ideal_list = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 
if 'target_return' not in st.session_state: st.session_state.target_return = 5.0
if 'my_diagnosis' not in st.session_state: st.session_state.my_diagnosis = []
if 'display_mode' not in st.session_state: st.session_state.display_mode = None

# [INPUT PANEL]
with st.expander("💰 자산 및 포트폴리오 관리", expanded=True):
    c_top1, c_top2, c_top3 = st.columns(3)
    with c_top1: st.session_state.cash = st.number_input("💰 예수금 (원)", value=st.session_state.cash, step=100000)
    with c_top2: st.session_state.target_return = st.number_input("🎯 목표 수익률 (%)", value=st.session_state.target_return, step=1.0)
    with c_top3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ 종목 추가", use_container_width=True):
            st.session_state.portfolio.append({'name': '', 'price': 0, 'qty': 0, 'strategy': '추세추종'})
            st.rerun()
            
    st.markdown("---")
    
    if not st.session_state.portfolio:
        st.info("보유 종목이 없습니다.")
    else:
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

    # [BUTTON: MY STOCK DIAGNOSIS]
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📝 내 종목만 진단하기", use_container_width=True):
        st.session_state.display_mode = 'MY'
        st.session_state.running = True
        
        engine = SingularityEngine()
        market_data = load_top50_data() 
        my_results = []
        
        with st.spinner("보유 포트폴리오 정밀 해부 중... (8대 엔진)"):
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
                
                wr, m, log_str = engine.run_diagnosis(mode)
                plan = engine.generate_report(mode, price, m, wr, st.session_state.cash, s['qty'], st.session_state.target_return)
                pnl = ((price - s['price'])/s['price']*100) if s['price'] > 0 else 0
                my_results.append({'name': s['name'], 'price': price, 'pnl': pnl, 'win': wr, 'mode': mode, 'log': log_str, 'plan': plan})
            st.session_state.my_diagnosis = my_results
        st.rerun()

# [BUTTON: HAMZZI]
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🐹 햄찌의 계좌 훈수 두기", use_container_width=True):
    msg = "사장님, 지금 주식창 볼 때가 아니에요! 일하세요 일! 🐹 (농담이고, 현금 비중 좀 챙기세요)"
    st.markdown(f"<div class='hamzzi-box'>🐹 햄찌 왈:<br><br>{msg}</div>", unsafe_allow_html=True)

# [DUAL LAUNCH BUTTONS]
c_btn1, c_btn2 = st.columns(2)

def run_market_scan():
    with st.spinner("전 종목 정밀 타격 및 랭킹 산출 중..."):
        engine = SingularityEngine()
        market_data = load_top50_data() 
        sc_all, sw_all, ideal_all = [], [], []
        
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close']))
            name = row['Name']
            
            wr_sc, m_sc, l_sc = engine.run_diagnosis("scalping")
            p_sc = engine.generate_report("scalping", price, m_sc, wr_sc, st.session_state.cash, 0, st.session_state.target_return)
            sc_all.append({'name': name, 'price': price, 'win': wr_sc, 'mode': "초단타", 'log': l_sc, 'plan': p_sc})
            
            wr_sw, m_sw, l_sw = engine.run_diagnosis("swing")
            p_sw = engine.generate_report("swing", price, m_sw, wr_sw, st.session_state.cash, 0, st.session_state.target_return)
            sw_all.append({'name': name, 'price': price, 'win': wr_sw, 'mode': "추세추종", 'log': l_sw, 'plan': p_sw})

            if wr_sc >= wr_sw: ideal_all.append(sc_all[-1])
            else: ideal_all.append(sw_all[-1])
        
        sc_all.sort(key=lambda x: x['win'], reverse=True)
        sw_all.sort(key=lambda x: x['win'], reverse=True)
        ideal_all.sort(key=lambda x: x['win'], reverse=True)
        
        st.session_state.sc_list = sc_all[:3]
        st.session_state.sw_list = sw_all[:3]
        st.session_state.ideal_list = ideal_all[:3]

if c_btn1.button("🏆 타이거&햄찌 출격! (Top 3)"):
    st.session_state.running = True
    st.session_state.display_mode = 'TOP3'
    run_market_scan()
    st.rerun()

if c_btn2.button("📊 단타 / 추세 (전략별 보기)"):
    st.session_state.running = True
    st.session_state.display_mode = 'SEPARATE'
    run_market_scan()
    st.rerun()

# [DISPLAY RESULTS]
st.markdown("---")

if st.session_state.get('running'):
    
    # 1. MY DIAGNOSIS
    if st.session_state.display_mode == 'MY' and st.session_state.my_diagnosis:
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
                    <div class='report-title'>🔍 8대 엔진 심층 분석</div>
                    {p['analysis']}
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

    # 2. TOP 3 MODE
    elif st.session_state.display_mode == 'TOP3' and st.session_state.ideal_list:
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
                    <div class='report-title'>🔍 8대 엔진 심층 분석</div>
                    {p['analysis']}
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

    # 3. SEPARATE MODE
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
                        <div class='report-title'>🔍 8대 엔진 심층 분석</div>
                        {p['analysis']}
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
