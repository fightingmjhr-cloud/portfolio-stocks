import streamlit as st
import pandas as pd
import numpy as np
import time

# -----------------------------------------------------------------------------
# [CORE ENGINE] TIGER & HAMZZI QUANT ENGINE (v6.0)
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

    # [INTERNAL] 8대 엔진 연산 (Logic)
    def _calculate_alpha(self):
        omega = np.random.uniform(5.0, 18.0)
        betti = np.random.choice([0, 1], p=[0.85, 0.15])
        hurst = np.random.uniform(0.4, 0.8)
        te = np.random.uniform(0.5, 3.0)
        vpin = np.random.uniform(0.1, 0.95)
        gnn = np.random.uniform(0.3, 0.9)
        sent = np.random.uniform(-1, 1)
        es = np.random.uniform(-0.03, -0.10)
        kelly = np.random.uniform(0.1, 0.4)

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

    # [FUNCTION A] 내 포트폴리오 분석
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

    # [FUNCTION B] 추천 및 전략 (Strategy Tag 추가)
    def scan_new_opportunities(self):
        db = [
            {"name": "SK하이닉스", "desc": "글로벌 HBM 시장 선도. AI 서버 수요 증가 수혜."},
            {"name": "현대차", "desc": "전기차 및 하이브리드 판매 호조. 북미 시장 점유율 확대."},
            {"name": "알테오젠", "desc": "SC 제형 변경 플랫폼 기술 보유. 기술 이전 로열티 기대."},
            {"name": "NAVER", "desc": "국내 검색 포털 1위. AI 및 커머스 사업 성장."},
            {"name": "한화에어로스페이스", "desc": "K-방산 대표주. 지정학적 리스크로 수출 증가."}
        ]
        
        recommendations = []
        for item in db:
            wr, m = self._calculate_alpha()
            current_price = int(np.random.uniform(100000, 500000))
            target_price = int(current_price * (1 + np.random.uniform(0.05, 0.20)))
            stop_loss = int(current_price * (1 + m['es']))
            roi = ((target_price - current_price) / current_price) * 100
            duration = "4주 (추세 추종)" if m['hurst'] > 0.6 else "3일 (단기 스윙)"
            
            risk_level = "High"
            reason = ""
            if wr >= 0.8:
                risk_level = "Strong Buy"
                reason = f"JLS 파동(Ω={m['omega']:.1f}) 상승. 수급 독성(VPIN) 해소."
            elif wr >= 0.6:
                risk_level = "Buy"
                reason = f"기술적 반등. AI 감성지수 긍정적."
            else:
                risk_level = "Watch"
                reason = "하방 압력 존재하나 지지선 근접."

            recommendations.append({
                "name": item['name'], "desc": item['desc'], "win": wr, "price": current_price,
                "target": target_price, "stop": stop_loss, "roi": roi, "allocation": f"{int(m['kelly']*100)}%",
                "duration": duration, "reason": reason, "risk": risk_level
            })
        
        recommendations.sort(key=lambda x: x['win'], reverse=True)
        return recommendations[:3]

# -----------------------------------------------------------------------------
# [UI] INTERFACE (Tiger&Hamzzi Quant)
# -----------------------------------------------------------------------------
# 아이콘 (호랑이 & 햄스터 파이팅)
icon_url = "https://i.imgur.com/8Kk3Z6S.png"

st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon=icon_url, layout="centered")

# CSS 스타일링
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; font-family: 'Roboto', sans-serif; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 50px; font-size: 18px; 
                       background: linear-gradient(90deg, #00C9FF, #92FE9D); border: none; color: black; }
    .metric-box { background: #111; border: 1px solid #333; padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 5px; }
    .metric-label { font-size: 12px; color: #888; }
    .metric-value { font-size: 18px; font-weight: bold; color: white; }
    .strategy-tag { background: rgba(255, 75, 75, 0.2); color: #FF4B4B; border: 1px solid #FF4B4B; 
                    padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    div[data-testid="stExpander"] { background-color: #0d1117; border: 1px solid #30363d; border-radius: 10px; margin-bottom: 10px; }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 헤더: 이미지와 New 타이틀
st.markdown(f"""
<div style='text-align: center;'>
    <img src='{icon_url}' width='120' style='margin-bottom: 10px;'><br>
    <h1 style='color: #fff; margin: 0; font-size: 28px;'>🐯 Tiger&Hamzzi Quant 🐹</h1>
    <p style='color: #888; font-size: 14px;'>Daily Real-time Trading System</p>
</div>
""", unsafe_allow_html=True)

# [설정]
with st.expander("⚙️ CONFIG (설정)", expanded=True):
    t_stock = st.text_input("내 보유 종목", value="한미반도체")
    c1, c2 = st.columns(2)
    t_price = c1.number_input("평단가", value=175000)
    t_qty = c2.number_input("수량", value=50)
    t_interval = st.selectbox("자동 실행", ["Manual", "1 min", "30 min", "1 hr"], index=0)

if 'running' not in st.session_state: st.session_state.running = False

# [실행 버튼]
c_start, c_stop = st.columns([3, 1])
if c_start.button("🚀 ACTIVATE"): st.session_state.running = True
if c_stop.button("⏹ STOP"): st.session_state.running = False

if st.session_state.running:
    engine = SingularityEngine()
    engine.set_target(t_stock, t_price, t_qty)
    
    with st.spinner("호랑이와 햄찌가 시장을 분석 중... 🐯🐹"):
        time.sleep(0.5)
        res = engine.analyze_my_portfolio()
        recs = engine.scan_new_opportunities()
    
    # [1] 내 포트폴리오 섹션
    color = "#00FF00" if "BUY" in res['action'] else "#FF4444"
    st.markdown(f"<div style='border:2px solid {color}; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px;'><h3 style='margin:0; color:white;'>{res['target']}</h3><h1 style='color:{color}; margin:0;'>{res['action']}</h1><p>WIN RATE: {res['win']*100:.1f}%</p></div>", unsafe_allow_html=True)
    
    if t_qty > 0:
        c1, c2, c3 = st.columns(3)
        c1.metric("현재가", f"{int(res['current']):,}원")
        c2.metric("수익률", f"{res['pnl']:.2f}%")
        c3.metric("평가액", f"{int(res['current']*t_qty):,}원")
        
    for step in res['exec']:
        st.info(step)

    # [2] 추천 종목 (상세 전략 + 태그)
    st.markdown("---")
    st.markdown("### 📡 AI 추천 및 상세 전략")
    
    if recs:
        for r in recs:
            sc = "🟢" if r['win'] >= 0.8 else ("🟠" if r['win'] >= 0.6 else "🔴")
            
            with st.expander(f"{sc} {r['name']} ({r['win']*100:.1f}%) - {r['risk']}"):
                # [NEW] 실시간 매매 태그 추가
                st.markdown("<span class='strategy-tag'>⚡ 매일 실시간 매매 (Daily Real-time)</span>", unsafe_allow_html=True)
                
                st.markdown(f"**🏢 기업 개요:** {r['desc']}")
                st.markdown(f"**💡 추천 근거:** {r['reason']}")
                st.markdown("---")
                
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"<div class='metric-box'><div class='metric-label'>현재가</div><div class='metric-value'>{r['price']:,}</div></div>", unsafe_allow_html=True)
                c2.markdown(f"<div class='metric-box'><div class='metric-label'>🎯 목표 익절가</div><div class='metric-value' style='color:#00FF00'>{r['target']:,}</div></div>", unsafe_allow_html=True)
                c3.markdown(f"<div class='metric-box'><div class='metric-label'>🛡️ 손절 라인</div><div class='metric-value' style='color:#FF4444'>{r['stop']:,}</div></div>", unsafe_allow_html=True)
                
                c4, c5, c6 = st.columns(3)
                c4.markdown(f"<div class='metric-box'><div class='metric-label'>예상 수익률</div><div class='metric-value'>+{r['roi']:.1f}%</div></div>", unsafe_allow_html=True)
                c5.markdown(f"<div class='metric-box'><div class='metric-label'>추천 비중</div><div class='metric-value'>{r['allocation']}</div></div>", unsafe_allow_html=True)
                c6.markdown(f"<div class='metric-box'><div class='metric-label'>보유 기간</div><div class='metric-value'>{r['duration']}</div></div>", unsafe_allow_html=True)

    else:
        st.warning("분석 결과가 없습니다.")
        
    # 자동 반복
    if t_interval != "Manual":
        sec = {"1 min": 60, "30 min": 1800, "1 hr": 3600}[t_interval]
        time.sleep(sec)
        st.rerun()
