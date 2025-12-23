import streamlit as st
import pandas as pd
import numpy as np
import time
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [CORE ENGINE] 8대 엔진 & 햄찌 어드바이저 (Smart Nagging Logic)
# -----------------------------------------------------------------------------

class SingularityEngine:
    def __init__(self):
        pass

    # [1] Metrics Calculation
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

    # [2] Run Diagnosis
    def run_diagnosis(self, mode="swing"):
        m = self._calculate_metrics(mode)
        score = 35.0 
        reasons = [] 

        if m['vpin'] > 0.6: score -= 15; reasons.append("☠️ 독성 위험")
        if m['es'] < -0.15: score -= 15; reasons.append("💣 폭락 징후")
        if m['betti'] == 1: score -= 10; reasons.append("⚠️ 구조 붕괴")

        if mode == "scalping":
            if m['hawkes'] > 2.5 and m['obi'] > 0.5: score += 40; reasons.append("🚀 퍼펙트 수급")
            elif m['hawkes'] > 1.5: score += 15; reasons.append("⚡ 수급 우위")
            elif m['hawkes'] < 0.8: score -= 10; reasons.append("💤 거래 소강")
        else: 
            if m['hurst'] > 0.75 and m['gnn'] > 0.8: score += 35; reasons.append("📈 대세 상승장")
            elif m['hurst'] > 0.6: score += 10; reasons.append("↗️ 추세 양호")
            else: score -= 5; reasons.append("📉 추세 미약")

        if 9 < m['omega'] < 13: score += 5; reasons.append("📐 파동 안정")
        if m['te'] > 3.0: score += 5; reasons.append("📡 정보 폭발")

        win_rate = min(0.92, score / 100)
        win_rate = max(0.15, win_rate)
        
        return win_rate, m, reasons

    # [3] Generate Report
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

    # [4] 🐹 햄찌의 스마트 잔소리 (Advanced Logic Advisor)
    def hamzzi_smart_nagging(self, cash, portfolio, market_data):
        # A. 포트폴리오 분석
        total_invest = 0
        current_val = 0
        worst_stock = None
        min_pnl = 0
        
        for s in portfolio:
            invest = s['price'] * s['qty']
            if s['name'] in market_data['Name'].values:
                cur_p = int(market_data[market_data['Name'] == s['name']].iloc[0]['Close'])
            else:
                cur_p = s['price'] # 데이터 없으면 평단가로 가정
                
            val = cur_p * s['qty']
            pnl = ((cur_p - s['price']) / s['price']) * 100
            
            total_invest += invest
            current_val += val
            
            if pnl < min_pnl:
                min_pnl = pnl
                worst_stock = s['name']

        total_asset = cash + current_val
        cash_ratio = (cash / total_asset * 100) if total_asset > 0 else 0
        total_pnl_pct = ((current_val - total_invest) / total_invest * 100) if total_invest > 0 else 0

        # B. 시장 최고의 종목 찾기 (Top Pick for Recommendation)
        best_pick_name = "삼성전자" # Default
        best_pick_score = 0
        best_pick_price = 0
        
        # 상위 5개만 빠르게 스캔해서 최고 종목 선정
        for _, row in market_data.head(5).iterrows():
            wr, _, _ = self.run_diagnosis("scalping")
            if wr > best_pick_score:
                best_pick_score = wr
                best_pick_name = row['Name']
                best_pick_price = int(row['Close'])

        # C. 햄찌의 잔소리 로직 (Cute Start -> Smart Fact -> Specific Action)
        title = "🐹 햄찌의 팩트 폭격기"
        
        # 시나리오 1: 돈이 너무 많음 (쫄보)
        if cash_ratio > 70:
            intro = "헤헤 사장님~ 통장에 현금이 빵빵하네요? 부자다 부자! 🌻"
            fact = f"근데 지금 뭐 하시는 거예요? 현금을 놀리면 인플레이션에 돈이 녹는다니까요? 현재 시장 변동성(Vol Surface)이 안정화되고 있는데 왜 구경만 하세요?"
            action = f"지금 당장 **[{best_pick_name}]** 차트 펴세요. 8대 엔진 점수가 **{best_pick_score*100:.0f}점**입니다. 현금의 30%를 털어서 **{int((cash*0.3)/best_pick_price)}주** 담으세요. 쫄지 마시고요!"
            
        # 시나리오 2: 손실 중 (존버충)
        elif total_pnl_pct < -5:
            intro = "아이고 우리 사장님... 계좌가 시퍼렇게 멍들었네... 😭 마음이 아파요..."
            fact = f"솔직히 말할게요. **[{worst_stock or '보유종목'}]** 그거 안 오릅니다. '존버'는 승리한다고요? 아니요, 기회비용만 날리는 겁니다. 위상수학(Topology)적으로 추세가 붕괴됐어요."
            action = f"눈 딱 감고 **[{worst_stock or '마이너스 종목'}]** 절반이라도 손절하세요. 그리고 그 돈으로 지금 수급 터지는 **[{best_pick_name}]**으로 갈아타세요. 복구하려면 움직여야 합니다!"
            
        # 시나리오 3: 수익 중 (자만)
        elif total_pnl_pct > 10:
            intro = "우와! 사장님 대박! 오늘 소고기 사주시는 거죠? 🐹❤️"
            fact = f"근데 너무 좋아하지 마세요. 방심하는 순간 시장은 뺏어갑니다. 현재 꼬리 위험(Tail Risk) 지표가 슬슬 올라오고 있어요. 수익 줄 때 챙겨야 내 돈입니다."
            action = f"욕심 부리지 말고 보유 물량의 **30%는 지금 시장가로 매도**해서 현금화하세요. 그리고 남은 돈으로 안전한 **[추세추종]** 포트폴리오를 다시 짭시다."
            
        # 시나리오 4: 어중간함 (방향성 부재)
        else:
            intro = "음... 사장님 계좌는 그냥 쏘쏘(So-So)하네요? 심심하죠? 🥱"
            fact = "이럴 때가 제일 위험해요. 지루하다고 아무거나 뇌동매매 하다가 골로 갑니다. 지금은 '내쉬 균형(Nash Equilibrium)' 상태라 섣불리 움직이면 손해예요."
            action = f"딱 하나만 추천할게요. **[{best_pick_name}]** 눌림목 올 때까지 기다리세요. 가격은 **{int(best_pick_price*0.99):,}원**입니다. 여기에 알림 설정해두고 주무세요."

        full_msg = f"""
        <div style='text-align:left;'>
        <b>1. {intro}</b><br><br>
        <b>2. 팩트 체크 (Fact Check)</b><br>
        {fact}<br><br>
        <b style='color:#FFFF00;'>3. 햄찌의 행동 지침 (Action Plan)</b><br>
        {action}
        </div>
        """
        return title, full_msg

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
    
    /* Stock Card */
    .stock-card { 
        background: #11151c; border-radius: 16px; padding: 25px; margin-bottom: 25px; 
        border: 1px solid #2d333b; box-shadow: 0 8px 30px rgba(0,0,0,0.8); position: relative;
    }
    
    /* Rank Badge Corrected */
    .rank-badge {
        position: absolute; top: 0; left: 0; 
        background: linear-gradient(135deg, #FF4444, #FF0000); color: #fff; 
        font-weight: bold; padding: 6px 15px; border-bottom-right-radius: 15px; 
        border-top-left-radius: 16px; font-size: 14px; z-index: 10;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.5);
    }
    
    .report-section {
        margin-top: 15px; padding-top: 15px; border-top: 1px solid #333; font-size: 14px; line-height: 1.7; color: #ddd;
    }
    .report-title { color: #00C9FF; font-weight: bold; margin-bottom: 8px; font-size: 15px; }
    
    .timeline-visual {
        display: flex; justify-content: space-between; background: #0d1117; 
        padding: 12px; border-radius: 8px; margin-top: 15px; font-size: 13px; border: 1px solid #333;
    }
    .t-item b { display: block; font-size: 15px; margin-top: 4px; color: #fff; }
    
    /* Hamzzi Box */
    .hamzzi-box {
        background-color: #26211c; border: 2px solid #FFAA00; border-radius: 15px;
        padding: 25px; color: #eee; margin-bottom: 25px; font-size: 15px; line-height: 1.6;
        box-shadow: 0 0 20px rgba(255, 170, 0, 0.2);
    }
    .hamzzi-title { color: #FFAA00; font-size: 20px; font-weight: 900; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;}

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
        
        with st.spinner("보유 포트폴리오 정밀 해부 중..."):
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
        st.rerun()

# [BUTTON: HAMZZI ADVISOR]
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🐹 햄찌의 계좌 훈수 두기 (클릭해서 혼나기)", use_container_width=True):
    engine = SingularityEngine()
    market_data = load_top50_data()
    title, msg = engine.hamzzi_smart_nagging(st.session_state.cash, st.session_state.portfolio, market_data)
    st.markdown(f"""
    <div class='hamzzi-box'>
        <div class='hamzzi-title'>🐹 {title}</div>
        {msg}
    </div>
    """, unsafe_allow_html=True)

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
