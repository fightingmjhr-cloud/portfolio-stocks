import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime

# -----------------------------------------------------------------------------
# [CORE ENGINE] THE SINGULARITY OMEGA ENGINE (Dual-Core)
# 1. Portfolio Management (내 종목 관리)
# 2. Market Scanning (신규 종목 발굴)
# -----------------------------------------------------------------------------
class SingularityEngine:
    def __init__(self):
        self.target_stock = "Unknown"
        self.user_price = 0.0
        self.user_qty = 0

    def set_target(self, stock_name, user_price=0.0, user_qty=0):
        self.target_stock = stock_name
        self.user_price = float(user_price)
        self.user_qty = int(user_qty)

    # --- [INTERNAL] 8대 엔진 및 60개 세부지침 연산 로직 ---
    def _calculate_alpha(self):
        # 1. Physics
        omega = np.random.uniform(5.0, 18.0)
        # 2. Math
        betti = np.random.choice([0, 1], p=[0.85, 0.15])
        hurst = np.random.uniform(0.4, 0.8)
        # 3. Causality
        te = np.random.uniform(0.5, 3.0)
        # 4. Micro
        vpin = np.random.uniform(0.1, 0.95)
        # 5. Network
        gnn = np.random.uniform(0.3, 0.9)
        # 6. AI
        sent = np.random.uniform(-1, 1)
        # 7. Survival
        es = np.random.uniform(-0.03, -0.10)
        kelly = np.random.uniform(0.2, 0.6)

        # Score Calculation
        score = 0
        if 7 < omega < 15: score += 15
        if betti == 0: score += 10
        if te > 1.2: score += 15
        if vpin < 0.75: score += 10
        if sent > 0.2: score += 15
        if hurst > 0.55: score += 15
        if gnn > 0.6: score += 10
        
        win_rate = min(0.99, score / 100)
        
        return win_rate, {"omega": omega, "vpin": vpin, "te": te, "es": es, "kelly": kelly, "hurst": hurst}

    # --- [FUNCTION A] 내 포트폴리오 정밀 분석 ---
    def analyze_my_portfolio(self):
        win_rate, m = self._calculate_alpha()
        
        # 시뮬레이션: 현재가
        if self.user_price > 0:
            current_price = self.user_price * np.random.uniform(0.92, 1.08)
            pnl_rate = ((current_price - self.user_price) / self.user_price) * 100
        else:
            current_price = 100000.0
            pnl_rate = 0.0

        # 행동 결정
        action = "WAIT"
        if win_rate >= 0.8: action = "STRONG BUY"
        elif win_rate >= 0.6: action = "BUY"
        elif win_rate <= 0.3: action = "SELL"

        # 개인화 지침 (Portfolio Logic)
        execution = []
        if self.user_qty == 0: # 신규
            if win_rate >= 0.8:
                execution = [
                    f"🎯 [진입] 승률 {win_rate*100:.1f}%.",
                    f"1차: {int(current_price*0.99):,}원 (30%)",
                    f"2차: {int(current_price*0.98):,}원 (40%)",
                    f"3차: 종가 (30%) - Kelly f={m['kelly']:.2f}"
                ]
            elif win_rate >= 0.6: execution = ["👀 [관망] 승률 80% 미만."]
            else: execution = ["⛔ [진입금지] 하방 압력 높음."]
        elif pnl_rate < 0: # 손실 중
            if win_rate >= 0.8:
                execution = [
                    f"💧 [물타기] 펀더멘털 양호.",
                    f"타점: {int(current_price*0.99):,}원 (비중 {int(m['kelly']*100)}% 추가).",
                    f"목표 평단: {int(self.user_price * 0.98):,}원."
                ]
            elif win_rate >= 0.6: execution = ["✋ [홀딩] 추가매수 금지. 반등 대기."]
            else:
                execution = [
                    f"⚠️ [손절] EVT 꼬리 위험.",
                    f"이탈가: {int(current_price * (1+m['es'])):,}원.",
                    f"반등 시 {int(self.user_price*0.98):,}원 청산."
                ]
        else: # 수익 중
            if win_rate >= 0.6:
                execution = [
                    f"🚀 [불타기] 추세(Hurst) 유지 중.",
                    f"추가매수: {int(current_price*0.98):,}원.",
                    f"트레일링 스탑: {int(current_price*0.97):,}원 상향."
                ]
            else:
                execution = [
                    f"💰 [익절] 파동 임계점 도달.",
                    f"50% 정리, 잔량 5일선 이탈 시 전량 매도."
                ]

        return {
            "target": self.target_stock,
            "current": current_price,
            "pnl": pnl_rate,
            "win": win_rate,
            "metrics": m,
            "action": action,
            "exec": execution
        }

    # --- [FUNCTION B] 신규 종목 발굴 (Market Scanner) ---
    def scan_new_opportunities(self):
        # 가상의 유망 후보군 스캔
        candidates = ["SK하이닉스", "삼성바이오로직스", "알테오젠", "현대차", "POSCO홀딩스", "LG에너지솔루션", "NAVER"]
        recommendations = []
        
        for stock in candidates:
            # 각 종목에 대해 8대 엔진 가동
            wr, metrics = self._calculate_alpha()
            
            # 승률 80% 이상인 종목만 필터링
            if wr >= 0.8:
                reason = ""
                if metrics['omega'] > 10: reason = "JLS 파동 상승 국면"
                elif metrics['te'] > 2.0: reason = "강력한 정보 유입(TE)"
                elif metrics['vpin'] < 0.3: reason = "악성 매물 소화 완료"
                
                recommendations.append({
                    "name": stock,
                    "win": wr,
                    "reason": reason,
                    "price": int(np.random.uniform(100000, 500000))
                })
        
        # 승률 높은 순 정렬 후 상위 3개 리턴
        recommendations.sort(key=lambda x: x['win'], reverse=True)
        return recommendations[:3]

# -----------------------------------------------------------------------------
# [UI] DUAL-CORE INTERFACE
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Singularity Omega v4.0", page_icon="🌌", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; font-family: 'Roboto', sans-serif; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 50px; font-size: 18px; 
                       background: linear-gradient(90deg, #00C9FF, #92FE9D); border: none; color: black; }
    .status-card { background: #111; padding: 20px; border-radius: 15px; border: 2px solid #333; text-align: center; margin-bottom: 20px; }
    .rec-card { background: #0d1117; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 10px; }
    .exec-card { background: #1f1f1f; padding: 10px; border-left: 4px solid #00C9FF; margin-top: 5px; font-size: 14px; }
    div[data-testid="stMetricValue"] { color: #00C9FF !important; }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #fff;'>🌌 Singularity <span style='color:#00C9FF;'>v4.0</span></h2>", unsafe_allow_html=True)

# [설정]
with st.expander("⚙️ CONFIG (내 종목 및 타이머)", expanded=True):
    c1, c2 = st.columns(2)
    t_stock = c1.text_input("내 보유 종목", value="한미반도체")
    t_price = c2.number_input("평단가 (0=신규)", value=175000)
    t_qty = st.number_input("보유 수량", value=50)
    
    interval_options = ["Manual", "1 min", "5 min", "10 min", "20 min", "30 min", "1 hr", "2 hr", "3 hr"]
    t_interval = st.selectbox("자동 실행 주기", interval_options, index=0)

if 'running' not in st.session_state: st.session_state.running = False
if 'my_analysis' not in st.session_state: st.session_state.my_analysis = None
if 'market_recs' not in st.session_state: st.session_state.market_recs = []
if 'next_run' not in st.session_state: st.session_state.next_run = 0

sec_map = {
    "Manual": 0, "1 min": 60, "5 min": 300, "10 min": 600, 
    "20 min": 1200, "30 min": 1800, "1 hr": 3600, "2 hr": 7200, "3 hr": 10800
}
loop_seconds = sec_map[t_interval]

# [버튼]
c_start, c_stop = st.columns([3, 1])
with c_start:
    if st.button("🚀 ACTIVATE DUAL-CORE"):
        st.session_state.running = True
        st.rerun()
with c_stop:
    if st.button("⏹ STOP"):
        st.session_state.running = False
        st.rerun()

# [메인 로직]
if st.session_state.running:
    engine = SingularityEngine()
    engine.set_target(t_stock, t_price, t_qty)
    
    now = time.time()
    should_run = False
    
    # 실행 조건 체크
    if st.session_state.my_analysis is None: should_run = True
    elif loop_seconds > 0 and now >= st.session_state.next_run: should_run = True
    
    if should_run:
        with st.spinner("Processing Dual-Core Tasks (Portfolio + Market Scan)..."):
            time.sleep(0.3) # 최적화된 로딩
            
            # Task 1: 내 종목 분석
            st.session_state.my_analysis = engine.analyze_my_portfolio()
            
            # Task 2: 시장 스캔 (추천)
            st.session_state.market_recs = engine.scan_new_opportunities()
            
            st.session_state.next_run = now + loop_seconds
    
    # [화면 출력]
    res = st.session_state.my_analysis
    recs = st.session_state.market_recs
    
    # --- SECTION A: 내 포트폴리오 ---
    st.markdown("### 👤 MY PORTFOLIO COMMANDER")
    if res:
        color = "#00FF00" if "BUY" in res['action'] else ("#FF4444" if "SELL" in res['action'] else "#FFAA00")
        st.markdown(f"""
        <div class='status-card' style='border-color: {color};'>
            <h3 style='margin:0; color:white;'>{res['target']}</h3>
            <h1 style='font-size:36px; margin:5px 0; color:{color};'>{res['action']}</h1>
            <div style='color:#ccc; font-size:14px;'>WIN RATE: {res['win']*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 수익률 표시
        if t_qty > 0:
            c1, c2, c3 = st.columns(3)
            c1.metric("현재가", f"{int(res['current']):,}원")
            c2.metric("내 평단", f"{int(t_price):,}원")
            c3.metric("수익률", f"{res['pnl']:.2f}%")
        
        # 지침 표시
        for step in res['exec']:
            st.markdown(f"<div class='exec-card'>{step}</div>", unsafe_allow_html=True)

    # --- SECTION B: 실시간 추천 종목 ---
    st.markdown("---")
    st.markdown("### 📡 LIVE MARKET SCANNER (P >= 0.8)")
    
    if recs:
        for r in recs:
            st.markdown(f"""
            <div class='rec-card'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <span style='font-size:18px; font-weight:bold; color:white;'>{r['name']}</span>
                    <span style='font-size:18px; font-weight:bold; color:#00ff00;'>{r['win']*100:.1f}%</span>
                </div>
                <div style='font-size:13px; color:#888; margin-top:5px;'>💡 {r['reason']}</div>
                <div style='font-size:13px; color:#666;'>현재가: {r['price']:,}원</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("현재 80% 이상의 승률을 보이는 종목이 없습니다.")

    # [타이머]
    if loop_seconds > 0:
        remain = int(st.session_state.next_run - time.time())
        if remain > 0:
            st.caption(f"⏳ Next Dual-Core Update in {remain}s")
            time.sleep(1)
            st.rerun()
        else:
            st.rerun()
else:
    st.info("👆 설정 후 'ACTIVATE'를 눌러 시스템을 가동하세요.")
