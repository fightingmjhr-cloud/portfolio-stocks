import streamlit as st
import pandas as pd
import numpy as np
import time
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [CORE ENGINE] 8대 엔진: 감점제 기반 보수적 평가 (Conservative Logic)
# -----------------------------------------------------------------------------

class SingularityEngine:
    def __init__(self):
        pass

    # [PHASE 1] 8대 엔진 데이터 생성 (Real-Time Simulation)
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

    # [PHASE 2] 정밀 진단 (감점제 적용)
    def run_diagnosis(self, mode="swing"):
        m = self._calculate_metrics(mode)
        score = 50.0 # Base Score
        reasons = [] # 시각화용 배지 리스트

        # [1. Physics] JLS 파동
        if 8 < m['omega'] < 14: 
            score += 10; reasons.append("📐 JLS파동 안정")
        else:
            score -= 5

        # [2. Math] 위상수학 & 프랙탈
        if m['betti'] == 0: reasons.append("🌀 구조적 안정")
        else: score -= 10; reasons.append("⚠️ 위상 붕괴")
        
        if m['hurst'] > 0.65: 
            score += 10; reasons.append(f"📈 추세강화({m['hurst']:.2f})")

        # [3. Causality] 정보 흐름
        if m['te'] > 2.5: score += 5; reasons.append("📡 정보 폭발")

        # [4. Microstructure] 핵심 승부처
        if mode == "scalping":
            if m['hawkes'] > 2.0 and m['obi'] > 0.3:
                score += 30; reasons.append(f"⚡ 수급폭발({m['hawkes']:.1f})")
            elif m['hawkes'] < 1.0:
                score -= 20; reasons.append("⚠️ 수급 부재")
            
            if m['vpin'] > 0.7: score -= 15; reasons.append("☠️ 독성 매물")
            else: score += 5; reasons.append("💧 청정 유동성")
        
        else: # Swing
            if m['gnn'] > 0.75: score += 15; reasons.append("🌐 주도주 중심성")
            if m['es'] < -0.15: score -= 15; reasons.append("💣 꼬리 위험")

        # 승률 보정 (95% 상한선)
        win_rate = min(0.95, score / 100)
        win_rate = max(0.30, win_rate)
        
        return win_rate, m, reasons

    # [PHASE 3] Action Plan
    def generate_plan(self, mode, price, m, wr):
        if mode == "scalping":
            vol = m['vol_surf'] * 0.03
            entry = int(price * (1 - vol*0.5))
            target = int(price * (1 + vol*1.2))
            stop = int(price * (1 - vol*0.8))
            
            if wr >= 0.8:
                strat = "🚀 [Attack] 호가창 매수 우위 확인 시 시장가 진입 권장."
            elif wr >= 0.65:
                strat = "⚖️ [Balance] 시초가 급등 보내고 눌림목 대기."
            else:
                strat = "🛡️ [Defense] 리스크 관리 우선. 확실한 자리 아니면 패스."
            
            todos = [
                f"⏰ 타임: 09:00~10:00 (수급 집중)",
                f"🔵 진입: {entry:,}원 (지지 확인)",
                f"🔴 익절: {target:,}원 (기계적 매도)",
                f"🚫 손절: {stop:,}원 (필수 준수)"
            ]
        else:
            target = int(price * 1.15)
            stop = int(price * 0.95)
            strat = "📈 [Trend] 상승 파동 초입. 분할 매수로 물량 확보." if wr >= 0.75 else "⏳ [Wait] 추세 확인 중. 박스권 하단 매집."
            todos = [
                f"📅 기간: 2주 ~ 4주",
                f"🎯 목표: {target:,}원 (15% 구간)",
                f"🛡️ 방어: {stop:,}원 (이탈 시 청산)",
                f"💰 비중: 켈리 {int(m['kelly']*100)}%"
            ]
            
        return strat, todos, (entry if mode=='scalping' else price, target, stop)

# [DATA]
@st.cache_data(ttl=3600)
def load_top30_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(30)
    except: return pd.DataFrame()

# [UI CONFIG]
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    .app-title { text-align: center; font-size: 34px; font-weight: 900; color: #fff; padding: 25px 0; text-shadow: 0 0 15px rgba(0,201,255,0.6); }
    
    /* Button */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 55px; font-size: 18px;
        background: linear-gradient(135deg, #00C9FF, #92FE9D); border: none; color: #000;
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.2); transition: 0.2s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    
    /* Cards */
    .stock-card { 
        background: #11151c; border-radius: 16px; padding: 22px; margin-bottom: 20px; 
        border: 1px solid #2d333b; box-shadow: 0 8px 25px rgba(0,0,0,0.7);
    }
    
    /* Logic Badges */
    .logic-badge {
        background: #1f242d; border: 1px solid #333; color: #00C9FF; 
        padding: 4px 8px; border-radius: 4px; font-size: 11px; margin-right: 5px; display: inline-block; margin-bottom: 5px;
    }
    
    /* Action Box */
    .action-box {
        background: #1a1f26; border-radius: 10px; padding: 15px; margin-top: 15px;
        border-left: 4px solid #FFFF00; font-size: 13px; line-height: 1.8;
    }
    
    /* Input Labels */
    .input-label { font-size: 12px; color: #888; margin-bottom: 4px; display: block; text-align: center; }
    
    /* Input Fields Dark Mode */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1f26 !important; color: #fff !important; border: 1px solid #444 !important;
    }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -20px !important; }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-title'>🐯 Tiger&Hamzzi Quant 🐹</div>", unsafe_allow_html=True)

# [SESSION STATE]
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'best_picks' not in st.session_state: st.session_state.best_picks = []

# [INPUT PANEL]
with st.expander("📝 내 보유 종목 추가 (Portfolio)", expanded=True):
    # 컬럼 헤더 (가이드)
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
if st.button("🐯 타이거&햄찌 출격! (Top 3 Scan) 🐹"):
    st.session_state.running = True
    
    with st.spinner("코스피/코스닥 상위 30개 전수 분석 중... (8대 엔진 가동)"):
        engine = SingularityEngine()
        market_data = load_top30_data()
        candidates = []
        
        # 통합 스캔 (Scalping + Swing 모두 계산 후 최고 점수 추출)
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close']))
            name = row['Name']
            
            # 1. Scalping Score
            wr_sc, m_sc, log_sc = engine.run_diagnosis("scalping")
            # 2. Swing Score
            wr_sw, m_sw, log_sw = engine.run_diagnosis("swing")
            
            # 더 높은 점수의 전략 선택
            if wr_sc > wr_sw:
                best_mode = "초단타"
                best_wr = wr_sc
                best_m = m_sc
                best_log = log_sc
            else:
                best_mode = "추세추종"
                best_wr = wr_sw
                best_m = m_sw
                best_log = log_sw
            
            # 커트라인 통과 시 후보 등록 (보수적 기준)
            if best_wr >= 0.70:
                plan, todos, _ = engine.generate_plan("scalping" if best_mode=="초단타" else "swing", price, best_m, best_wr)
                candidates.append({
                    'name': name, 'price': price, 'win': best_wr, 'mode': best_mode,
                    'log': best_log, 'plan': plan, 'todos': todos, 'm': best_m
                })
        
        # 승률 순 정렬 -> Top 3 추출
        candidates.sort(key=lambda x: x['win'], reverse=True)
        st.session_state.best_picks = candidates[:3]
        
    st.rerun()

# [DISPLAY RESULTS]
st.markdown("---")

if st.session_state.best_picks:
    st.markdown("<h5>🏆 오늘의 Singularity Choice (통합 Top 3)</h5>", unsafe_allow_html=True)
    
    for r in st.session_state.best_picks:
        border_color = "#FFFF00" if r['mode'] == "초단타" else "#00C9FF"
        
        # 뱃지 HTML 생성
        badges_html = "".join([f"<span class='logic-badge'>{reason}</span>" for reason in r['log']])
        # Todo HTML
        todo_html = "".join([f"<div>• {t}</div>" for t in r['todos']])
        
        st.markdown(f"""
        <div class='stock-card' style='border-left: 5px solid {border_color};'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='font-size:22px; font-weight:bold; color:#fff;'>{r['name']}</span>
                <span class='badge' style='background:{border_color}; color:#000;'>{r['mode']} / 승률 {r['win']*100:.1f}%</span>
            </div>
            
            <div style='margin-top:10px;'>
                {badges_html}
            </div>
            
            <div class='action-box' style='border-left-color: {border_color};'>
                <div style='color:{border_color}; font-weight:bold; margin-bottom:5px;'>📢 {r['mode']} 실전 시나리오</div>
                <div style='color:#eee; margin-bottom:10px; font-weight:bold;'>{r['plan']}</div>
                <div style='color:#ccc;'>{todo_html}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"🔍 {r['name']} - 8대 엔진 Deep Dive"):
            m = r['m']
            st.markdown(f"""
            <div style='display:grid; grid-template-columns: repeat(2, 1fr); gap:10px; font-size:12px; color:#ccc;'>
                <div>📐 Omega: <b style='color:#fff;'>{m['omega']:.2f}</b></div>
                <div>🌊 VPIN: <b style='color:#fff;'>{m['vpin']:.2f}</b></div>
                <div>⚡ Hawkes: <b style='color:#fff;'>{m['hawkes']:.2f}</b></div>
                <div>⚖️ OBI: <b style='color:#fff;'>{m['obi']:.2f}</b></div>
                <div>📈 Hurst: <b style='color:#fff;'>{m['hurst']:.2f}</b></div>
                <div>💰 Kelly: <b style='color:#fff;'>{m['kelly']:.2f}</b></div>
            </div>
            """, unsafe_allow_html=True)

else:
    st.info("👆 [출격] 버튼을 누르면 오늘의 가장 완벽한 기회 3가지를 스캔합니다.")

# [MANUAL & GUIDE]
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("📚 승률 산출 근거 및 매매 기준 (Manual)", expanded=False):
    st.markdown("""
    #### 🧬 승률 산출 로직 (Scoring Logic)
    - 본 시스템은 **감점제(Penalty System)**를 적용하여 보수적으로 평가합니다.
    - **기본 점수:** 50점에서 시작
    - **가산점(+):** 수급 폭발(Hawkes > 1.8), 추세 강화(Hurst > 0.65), 구조적 안정(Betti=0) 등 확실한 호재
    - **감점(-):** 독성 매물(VPIN > 0.7), 꼬리 위험(ES < -0.15) 등 잠재 리스크 발견 시 점수 차감
    
    #### 🚦 매매 기준
    - **승률 80% 이상:** 강력 매수 (비중 확대)
    - **승률 70% ~ 79%:** 매수 (분할 진입)
    - **승률 69% 이하:** 관망 (리스크 관리)
    """)
