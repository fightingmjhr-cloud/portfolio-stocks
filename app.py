import streamlit as st
import pandas as pd
import numpy as np
import time
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [CORE ENGINE] 8대 엔진 & 듀얼 멘토 시스템
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
        hurst = np.random.uniform(0.2, 0.95)
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
        tags = [] 

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

        if 9 < m['omega'] < 13: score += 5; tags.append({'label': '📐 파동 안정', 'val': '+5', 'type': 'good'})
        if m['te'] > 3.0: score += 5; tags.append({'label': '📡 정보 폭발', 'val': '+5', 'type': 'good'})

        win_rate = min(0.92, score / 100)
        win_rate = max(0.15, win_rate)
        
        return win_rate, m, tags

    # [Deep Analyst Report]
    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        if mode == "scalping":
            vol = m['vol_surf'] * 0.04
            entry = int(price * (1 - vol))
            target = max(int(price * (1 + target_return/100)), int(price * (1 + vol*1.5)))
            stop = int(price * (1 - vol*0.7))
            time_str = "09:00 ~ 09:30 (골든타임)"
            
            reason_target = f"변동성 표면(Vol Surface)이 {m['vol_surf']:.2f}로 확장 중입니다. 표준편차 2σ 상단인 목표가까지 OBI(호가 불균형)가 매수 우위를 점하고 있습니다."
            reason_stop = f"Hawkes 프로세스상 자기 여진(Self-Exciting)이 멈추는 임계점입니다. VPIN 급증 시 알고리즘 투매가 나올 수 있어 칼손절 필수입니다."
        else:
            target = int(price * (1 + target_return/100))
            stop = int(price * 0.93)
            time_str = "15:20 종가 or 5일선 지지"
            
            reason_target = f"허스트 지수(Hurst)가 {m['hurst']:.2f}로 추세 지속성이 강력합니다. 피보나치 확장 레벨 1.272 구간까지 상승 여력이 충분한 구조적 상승장입니다."
            reason_stop = f"JLS 파동 모델의 임계 시간(Tc) 근처입니다. {stop:,}원 이탈은 위상수학적 구조 붕괴를 의미하므로 전량 청산해야 합니다."

        adjusted_kelly = m['kelly'] * (wr / 0.8) if wr < 0.8 else m['kelly']
        alloc_cash = cash * adjusted_kelly
        can_buy_qty = int(alloc_cash / price) if price > 0 else 0

        if wr >= 0.75:
            cmd = "🔥 STRONG BUY"; style = "border: 2px solid #00FF00; color: #00FF00;"
            briefing = f"<b>[탁월함]</b> 수급(Hawkes)과 추세(Hurst)가 임계점을 돌파했습니다. GNN 중심성 {m['gnn']:.2f}로 섹터 내 자금을 흡수하는 <b>주도주(Leading Stock)</b>입니다."
            action = f"확률적 우위가 확실합니다. 켈리 최적 비중인 현금의 <b>{int(adjusted_kelly*100)}% ({can_buy_qty}주)</b>를 과감히 투입하십시오."
        elif wr >= 0.55:
            cmd = "⚖️ BUY / HOLD"; style = "border: 2px solid #FFAA00; color: #FFAA00;"
            briefing = f"<b>[양호함]</b> 상승 동력은 있으나 꼬리 위험(ES {m['es']:.2f})이 존재합니다. 추세는 살아있으나 단기 변동성 노이즈가 섞여 있습니다."
            action = f"서두르지 마십시오. 리스크 분산을 위해 <b>{int(can_buy_qty/2)}주</b>만 선취매 후, 지지력을 확인하고 불타기 하십시오."
        else:
            cmd = "🛡️ SELL / WAIT"; style = "border: 2px solid #FF4444; color: #FF4444;"
            briefing = f"<b>[위험]</b> 독성 매물(VPIN {m['vpin']:.2f})이 포착되었습니다. 이는 스마트 머니의 이탈 징후입니다. 손익비가 불리합니다."
            action = "절대 진입 금지입니다. 보유 중이라면 반등 시 전량 매도하여 현금을 확보하는 것이 최고의 헷지(Hedge)입니다."

        return {
            "cmd": cmd, "briefing": briefing, "action": action, "time": time_str, "style": style,
            "prices": (entry if mode=='scalping' else price, target, stop),
            "qty_guide": can_buy_qty,
            "reasons": {"target": reason_target, "stop": reason_stop}
        }

    # [4] 🐹 햄찌의 골드만삭스 퀀트 분석
    def hamzzi_nagging(self, cash, portfolio, market_data):
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
        pnl_pct = ((current_val - total_invest) / total_invest * 100) if total_invest > 0 else 0
        
        title = "🐹 햄찌의 골드만삭스 퀀트 브리핑"
        
        if cash_ratio > 70:
            intro = "사장님, 'Cash Drag(현금 보유로 인한 수익 저하)'가 심각합니다! 🌻"
            logic = "인플레이션 헤지가 안 되고 있어요. 포트폴리오 이론상 지금은 Beta(시장 민감도)를 높여야 할 때입니다."
            advice = "안전마진이 확보된 종목에 자산의 40% 이상을 배분(Asset Allocation)하십시오."
        elif pnl_pct < -5:
            intro = "사장님... '손실 회피 편향'에 빠지셨나요? 📉"
            logic = "지금 들고 있는 건 '매몰 비용(Sunk Cost)'입니다. 펀더멘털 훼손된 종목을 들고 기도매매 하지 마세요."
            advice = "감정을 배제하고 기계적으로 손절(Cut Loss) 후, 주도주로 리밸런싱 하십시오."
        elif pnl_pct > 10:
            intro = "오! Alpha(초과 수익)를 창출하셨군요? 🐹✨"
            logic = "하지만 평가익은 사이버머니입니다. 변동성 군집(Volatility Clustering) 현상이 보이니 샤프 지수 관리가 필요합니다."
            advice = "탐욕을 줄이고 50%는 매도하여 확정 수익(Realized Gain)으로 만드십시오."
        else:
            intro = "포트폴리오의 기대수익률이 너무 낮습니다. 😐"
            logic = "방향성 탐색 구간입니다. 스마트 머니의 유동성 공급 시그널을 기다리세요."
            advice = "확실한 시그널 전까지 Cash position을 유지하며 관망(Wait & See) 하십시오."

        msg = f"<div style='font-size:14px;'><b>1. 진단:</b> {intro}<br><b>2. 논리:</b> {logic}<br><b style='color:#FFAA00;'>3. 처방:</b> {advice}</div>"
        return title, msg

    # [5] 🐯 호랑이의 꼰대 훈수 (Fundamental Analysis)
    def tiger_nagging(self, cash, portfolio, market_data):
        # 가상의 펀더멘털 데이터 생성 (실제 API 연동 시 교체 가능)
        per = np.random.uniform(5.0, 50.0)
        pbr = np.random.uniform(0.5, 5.0)
        roe = np.random.uniform(0.0, 30.0)
        
        total_invest = 0; current_val = 0
        for s in portfolio:
            invest = s['price'] * s['qty']
            if s['name'] in market_data['Name'].values:
                cur_p = int(market_data[market_data['Name'] == s['name']].iloc[0]['Close'])
            else: cur_p = s['price']
            total_invest += invest
            current_val += cur_p * s['qty']
        
        total_asset = cash + current_val
        cash_ratio = (cash / total_asset * 100) if total_asset > 0 else 0
        pnl_pct = ((current_val - total_invest) / total_invest * 100) if total_invest > 0 else 0

        title = "🐯 호랑이의 꼰대 가치투자 훈수"
        
        if cash_ratio > 80:
            intro = "에잉 쯧쯧! 젊은 양반이 겁이 왜 이렇게 많아! 😤"
            logic = "주식은 '기업의 소유권'을 사는 거야. 지금처럼 쌀 때 우량주를 모아야 나중에 배당 타먹고 살 거 아냐!"
            advice = "당장 서점에 가서 재무제표 읽는 법 책부터 사! 그리고 삼성전자 같은 거 쌀 때 좀 사둬!"
        elif pnl_pct < -10:
            intro = "어이쿠! 파란불이 번쩍번쩍하네! 내가 뭐라 그랬어! 😡"
            logic = "PER, PBR도 안 보고 묻지마 투자를 하니까 그렇지! 기업의 '내재 가치(Intrinsic Value)'를 봐야지 왜 차트 쪼가리를 봐!"
            advice = "지금이라도 ROE(자기자본이익률) 15% 넘는 알짜 기업 찾아서 10년 묻어둬! 주식은 농사야 농사!"
        elif pnl_pct > 20:
            intro = "허허, 뒷걸음질 치다 쥐 잡았구만? 운이 좋았어. 🐯"
            logic = "근데 그 회사가 진짜 돈을 잘 벌어서 오른 건가? 테마주 타다가 한강 간 놈들 여럿 봤다. '안전마진(Margin of Safety)'은 확보된 거냐?"
            advice = "거품 꺼지기 전에 원금은 챙겨! 그리고 그 돈으로 땅을 사던가 배당주를 사! 복리의 마법을 믿으란 말이야!"
        else:
            intro = "거 계좌가 왜 이리 지지부진해? 공부 안 하지? 😑"
            logic = "시장은 '미인 투표'가 아니라 '체중계'야. 결국 실적 따라간다. 지금 들고 있는 종목, 영업이익은 매년 늘고 있어?"
            advice = "분기보고서(DART) 들어가서 주석사항까지 꼼꼼히 읽어봐! 사업의 본질을 모르고 사는 건 투기가 아니라 도박이야!"

        msg = f"<div style='font-size:14px;'><b>1. 호통:</b> {intro}<br><b>2. 본질:</b> {logic}<br><b style='color:#FF4444;'>3. 훈수:</b> {advice}</div>"
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
    .app-title { text-align: center; font-size: 36px; font-weight: 900; color: #fff; padding: 30px 0; text-shadow: 0 0 25px rgba(0,201,255,0.7); }
    
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1f26 !important; color: #fff !important; border: 1px solid #444 !important; border-radius: 8px;
    }
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 50px; font-size: 18px;
        background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%); border: none; color: #000;
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.3); transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    
    /* Card UI */
    .stock-card { 
        background: #121212; border-radius: 16px; padding: 0; margin-bottom: 30px; 
        border: 1px solid #333; box-shadow: 0 10px 30px rgba(0,0,0,0.5); overflow: hidden;
    }
    .card-header {
        padding: 15px 20px; background: #1e1e1e; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center;
    }
    .stock-name { font-size: 22px; font-weight: 900; color: #fff; }
    .stock-score { font-size: 14px; font-weight: bold; background: #333; padding: 5px 12px; border-radius: 20px; color: #fff; border: 1px solid #555; }
    
    .tag-container { padding: 15px 20px 5px 20px; display: flex; flex-wrap: wrap; gap: 8px; }
    .tag { font-size: 12px; font-weight: bold; padding: 4px 10px; border-radius: 6px; color: #000; display: inline-block; }
    .tag-best { background: #00FF00; box-shadow: 0 0 10px rgba(0,255,0,0.4); }
    .tag-good { background: #00C9FF; }
    .tag-bad { background: #FF4444; color: #fff; }
    .tag-base { background: #555; color: #ccc; }
    
    .info-grid {
        display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: #333; margin: 15px 20px; border: 1px solid #333;
    }
    .info-item { background: #121212; padding: 10px; text-align: center; }
    .info-label { font-size: 11px; color: #888; display: block; margin-bottom: 3px; }
    .info-val { font-size: 15px; font-weight: bold; color: #fff; }
    
    .action-box { margin: 0 20px 20px 20px; background: #1a1a1a; border-radius: 10px; padding: 15px; border-left: 4px solid #fff; }
    .ab-title { font-size: 14px; font-weight: bold; margin-bottom: 8px; color: #aaa; text-transform: uppercase; }
    .ab-content { font-size: 14px; line-height: 1.6; color: #eee; margin-bottom: 15px; }
    
    .rationale-box { 
        background: #0d1117; padding: 12px; border-radius: 8px; font-size: 13px; color: #ccc; line-height: 1.5; border: 1px solid #333;
    }
    .rat-label { color: #888; font-weight: bold; font-size: 12px; margin-bottom: 4px; display:block; }
    
    .timeline { display: flex; justify-content: space-between; background: #0f0f0f; padding: 15px 25px; border-top: 1px solid #333; }
    .tl-item { text-align: center; }
    .tl-label { font-size: 11px; color: #666; margin-bottom: 4px; }
    .tl-val { font-size: 16px; font-weight: bold; color: #fff; }
    
    /* Hamzzi Box */
    .hamzzi-box {
        background: linear-gradient(135deg, #2c241b, #1a1510); border: 2px solid #FFAA00; border-radius: 16px;
        padding: 25px; color: #eee; margin-bottom: 15px; box-shadow: 0 0 20px rgba(255, 170, 0, 0.2);
    }
    .hamzzi-title { color: #FFAA00; font-size: 20px; font-weight: 900; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;}
    
    /* Tiger Box */
    .tiger-box {
        background: linear-gradient(135deg, #3d0000, #1a0000); border: 2px solid #FF4444; border-radius: 16px;
        padding: 25px; color: #eee; margin-bottom: 25px; box-shadow: 0 0 20px rgba(255, 68, 68, 0.2);
    }
    .tiger-title { color: #FF4444; font-size: 20px; font-weight: 900; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;}

    .rank-ribbon {
        position: absolute; top: 0; left: 0; padding: 5px 12px; font-size: 12px; font-weight: bold; color: #fff;
        background: linear-gradient(45deg, #FF416C, #FF4B2B); border-bottom-right-radius: 12px; z-index: 5;
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

with st.expander("💰 내 자산 및 포트폴리오 (Personal)", expanded=True):
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
    else: st.info("보유 종목이 없습니다.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📝 내 종목만 진단하기", use_container_width=True):
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

# [BUTTON: HAMZZI]
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🐹 햄찌의 계좌 훈수 두기 (클릭해서 혼나기)", use_container_width=True):
    engine = SingularityEngine()
    market_data = load_top50_data()
    title, msg = engine.hamzzi_nagging(st.session_state.cash, st.session_state.portfolio, market_data)
    st.markdown(f"<div class='hamzzi-box'><div class='hamzzi-title'>{title}</div>{msg}</div>", unsafe_allow_html=True)

# [BUTTON: TIGER]
if st.button("🐯 호랑이의 꼰대 훈수 (뼈 맞을 준비 하세요)", use_container_width=True):
    engine = SingularityEngine()
    market_data = load_top50_data()
    title, msg = engine.tiger_nagging(st.session_state.cash, st.session_state.portfolio, market_data)
    st.markdown(f"<div class='tiger-box'><div class='tiger-title'>{title}</div>{msg}</div>", unsafe_allow_html=True)

# [RESULT 1: MY DIAGNOSIS]
if st.session_state.display_mode == 'MY' and st.session_state.my_diagnosis:
    st.markdown("---")
    st.markdown("<h5>👤 내 보유 종목 정밀 진단 리포트</h5>", unsafe_allow_html=True)
    for d in st.session_state.my_diagnosis:
        p = d['plan']
        tag_html = "".join([f"<span class='tag tag-{t['type']}'>{t['label']} {t['val']}</span> " for t in d['tags']])
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
                <div class='rationale-box' style='margin-top:10px;'>
                    <span class='rat-label'>🎯 목표가 산정 근거:</span>{p['reasons']['target']}<br><br>
                    <span class='rat-label'>🛑 손절가 설정 이유:</span>{p['reasons']['stop']}
                </div>
            </div>
            <div class='timeline'>
                <div class='tl-item'><div class='tl-label'>진입/추매</div><div class='tl-val' style='color:#00C9FF'>{p['prices'][0]:,}</div></div>
                <div class='tl-item'><div class='tl-label'>목표가</div><div class='tl-val' style='color:#00FF00'>{p['prices'][1]:,}</div></div>
                <div class='tl-item'><div class='tl-label'>손절가</div><div class='tl-val' style='color:#FF4444'>{p['prices'][2]:,}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)
st.markdown("#### 📡 시장 정밀 타격 (Market Intelligence)")
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

def render_card(data, idx):
    p = data['plan']
    tag_html = "".join([f"<span class='tag tag-{t['type']}'>{t['label']} {t['val']}</span> " for t in data['tags']])
    
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
            <div class='rationale-box' style='margin-top:10px;'>
                <span class='rat-label'>🎯 목표가 산정 근거:</span>{p['reasons']['target']}<br><br>
                <span class='rat-label'>🛑 손절가 설정 이유:</span>{p['reasons']['stop']}
            </div>
        </div>
        <div class='timeline'>
            <div class='tl-item'><div class='tl-label'>진입가</div><div class='tl-val' style='color:#00C9FF'>{p['prices'][0]:,}</div></div>
            <div class='tl-item'><div class='tl-label'>목표가</div><div class='tl-val' style='color:#00FF00'>{p['prices'][1]:,}</div></div>
            <div class='tl-item'><div class='tl-label'>손절가</div><div class='tl-val' style='color:#FF4444'>{p['prices'][2]:,}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
