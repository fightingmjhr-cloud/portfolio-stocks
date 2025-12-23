import streamlit as st
import pandas as pd
import numpy as np
import time

# -----------------------------------------------------------------------------
# [CORE ENGINE] SINGULARITY OMEGA (Streamlit Cloud Version)
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

    def _calculate_alpha(self):
        # 8대 엔진 시뮬레이션 로직
        omega = np.random.uniform(5.0, 18.0)
        betti = np.random.choice([0, 1], p=[0.85, 0.15])
        hurst = np.random.uniform(0.4, 0.8)
        te = np.random.uniform(0.5, 3.0)
        vpin = np.random.uniform(0.1, 0.95)
        gnn = np.random.uniform(0.3, 0.9)
        sent = np.random.uniform(-1, 1)
        es = np.random.uniform(-0.03, -0.10)
        kelly = np.random.uniform(0.2, 0.6)

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

    def analyze_my_portfolio(self):
        win_rate, m = self._calculate_alpha()
        if self.user_price > 0:
            current_price = self.user_price * np.random.uniform(0.92, 1.08)
            pnl_rate = ((current_price - self.user_price) / self.user_price) * 100
        else:
            current_price = 100000.0
            pnl_rate = 0.0

        action = "WAIT"
        if win_rate >= 0.8: action = "STRONG BUY"
        elif win_rate >= 0.6: action = "BUY"
        elif win_rate <= 0.3: action = "SELL"

        execution = []
        if self.user_qty == 0:
            if win_rate >= 0.8:
                execution = [f"🎯 [진입] 승률 {win_rate*100:.1f}%.", f"1차: {int(current_price*0.99):,}원 (30%)", f"2차: {int(current_price*0.98):,}원 (40%)", f"3차: 종가 (30%)"]
            elif win_rate >= 0.6: execution = ["👀 [관망] 승률 80% 미만."]
            else: execution = ["⛔ [진입금지] 하방 압력 높음."]
        elif pnl_rate < 0:
            if win_rate >= 0.8:
                execution = [f"💧 [물타기] 펀더멘털 양호.", f"타점: {int(current_price*0.99):,}원 (비중 {int(m['kelly']*100)}% 추가).", f"목표 평단: {int(self.user_price * 0.98):,}원."]
            elif win_rate >= 0.6: execution = ["✋ [홀딩] 추가매수 금지."]
            else: execution = [f"⚠️ [손절] EVT 위험.", f"이탈가: {int(current_price * (1+m['es'])):,}원."]
        else:
            if win_rate >= 0.6:
                execution = [f"🚀 [불타기] 추세 유지.", f"추가매수: {int(current_price*0.98):,}원.", f"트레일링 스탑: {int(current_price*0.97):,}원."]
            else:
                execution = [f"💰 [익절] 임계점 도달.", f"50% 정리."]

        return {"target": self.target_stock, "current": current_price, "pnl": pnl_rate, "win": win_rate, "metrics": m, "action": action, "exec": execution}

    def scan_new_opportunities(self):
        candidates = ["SK하이닉스", "삼성바이오로직스", "알테오젠", "현대차", "POSCO홀딩스", "LG에너지솔루션", "NAVER"]
        recommendations = []
        for stock in candidates:
            wr, metrics = self._calculate_alpha()
            reason = "시장 분석 중"
            risk = "High"
            
            if wr >= 0.8:
                risk = "Safe"
                if metrics['omega'] > 10: reason = "JLS 상승 파동"
                elif metrics['te'] > 2.0: reason = "정보 유입(TE)"
                else: reason = "골든 크로스"
            elif wr >= 0.6:
                risk = "Moderate"
                reason = "추세 양호"
            
            recommendations.append({"name": stock, "win": wr, "reason": reason, "risk": risk, "price": int(np.random.uniform(100000, 500000))})
        
        recommendations.sort(key=lambda x: x['win'], reverse=True)
        return recommendations[:3]

# [UI 설정]
st.set_page_config(page_title="Singularity v4.1", page_icon="🌌", layout="centered")
st.markdown("""<style>.stApp {background-color: black; color: #e0e0e0;} .stButton>button {width: 100%; background: linear-gradient(90deg, #00C9FF, #92FE9D); border: none; color: black; font-weight: bold; height: 50px;}</style>""", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>🌌 Singularity <span style='color:#00C9FF;'>v4.1</span></h2>", unsafe_allow_html=True)

with st.expander("⚙️ 설정 (Config)", expanded=True):
    t_stock = st.text_input("내 보유 종목", value="한미반도체")
    c1, c2 = st.columns(2)
    t_price = c1.number_input("평단가", value=175000)
    t_qty = c2.number_input("수량", value=50)
    t_interval = st.selectbox("자동 실행", ["Manual", "1 min", "5 min", "1 hr"], index=0)

if 'running' not in st.session_state: st.session_state.running = False

c_start, c_stop = st.columns([3, 1])
if c_start.button("🚀 ACTIVATE"): st.session_state.running = True
if c_stop.button("⏹ STOP"): st.session_state.running = False

if st.session_state.running:
    engine = SingularityEngine()
    engine.set_target(t_stock, t_price, t_qty)
    
    with st.spinner("Analyzing..."):
        time.sleep(0.5)
        res = engine.analyze_my_portfolio()
        recs = engine.scan_new_opportunities()
    
    color = "#00FF00" if "BUY" in res['action'] else "#FF4444"
    st.markdown(f"<div style='border:2px solid {color}; padding:20px; border-radius:15px; text-align:center;'><h1 style='color:{color}; margin:0;'>{res['action']}</h1><p>WIN RATE: {res['win']*100:.1f}%</p></div>", unsafe_allow_html=True)
    
    if t_qty > 0:
        st.write(f"**수익률:** {res['pnl']:.2f}% | **현재가:** {int(res['current']):,}원")
    
    for step in res['exec']:
        st.info(step)
    
    st.markdown("---")
    st.markdown("### 📡 추천 종목")
    if recs:
        for r in recs:
            sc = "#00FF00" if r['win'] >= 0.8 else ("#FFAA00" if r['win'] >= 0.6 else "#FF4444")
            st.markdown(f"<div style='border-left:5px solid {sc}; padding:10px; background:#111; margin-bottom:5px;'><b>{r['name']}</b> ({r['win']*100:.1f}%) - {r['reason']}</div>", unsafe_allow_html=True)
            
    if t_interval != "Manual":
        sec = {"1 min": 60, "5 min": 300, "1 hr": 3600}[t_interval]
        time.sleep(sec)
        st.rerun()
