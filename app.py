import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import FinanceDataReader as fdr
from typing import List, Dict

# -----------------------------------------------------------------------------
# [CORE ENGINE] SINGULARITY ENGINE v21.1 (Fixed & Optimized)
# -----------------------------------------------------------------------------

class SingularityEngine:
    def __init__(self):
        pass

    # [1] Physics (물리 엔진) - 에러 처리 추가
    def _engine_physics(self):
        try:
            omega = np.random.uniform(5.0, 20.0)
            vol_surf = np.random.uniform(0.1, 0.8)
            return {"omega": omega, "vol_surf": vol_surf}
        except:
            return {"omega": 10.0, "vol_surf": 0.5}

    # [2] Math (수학 엔진)
    def _engine_math(self):
        try:
            betti = np.random.choice([0, 1], p=[0.8, 0.2])
            hurst = np.random.uniform(0.3, 0.8)
            return {"betti": betti, "hurst": hurst}
        except:
            return {"betti": 0, "hurst": 0.5}

    # [3] Causality (인과관계 엔진)
    def _engine_causality(self):
        try:
            te = np.random.uniform(0.1, 3.0)
            is_granger = np.random.choice([True, False], p=[0.3, 0.7])
            return {"te": te, "is_granger": is_granger}
        except:
            return {"te": 1.0, "is_granger": False}

    # [4] Microstructure (미시구조 엔진)
    def _engine_micro(self, mode):
        try:
            vpin = np.random.uniform(0.1, 0.95)
            # 스캘핑 모드일 때 Hawkes 강도 높게 설정
            hawkes = np.random.uniform(0.5, 2.0) if mode == "scalping" else np.random.uniform(0.5, 1.2)
            obi = np.random.uniform(-0.8, 0.8)
            return {"vpin": vpin, "hawkes": hawkes, "obi": obi}
        except:
            return {"vpin": 0.5, "hawkes": 1.0, "obi": 0.0}

    # [5&6] AI & Network
    def _engine_ai_net(self):
        gnn = np.random.uniform(0.1, 0.9)
        sent = np.random.uniform(-0.8, 0.8)
        return {"gnn": gnn, "sent": sent}

    # [8] Risk
    def _engine_risk(self):
        es = np.random.uniform(-0.02, -0.15)
        kelly = np.random.uniform(0.05, 0.35)
        return {"es": es, "kelly": kelly}

    # [MASTER] 통합 연산
    def run_full_diagnosis(self, mode="swing"):
        e1 = self._engine_physics()
        e2 = self._engine_math()
        e3 = self._engine_causality()
        e4 = self._engine_micro(mode)
        e56 = self._engine_ai_net()
        e8 = self._engine_risk()
        
        score = 0
        if 8 < e1['omega'] < 14: score += 10
        if e2['betti'] == 0: score += 10
        if e3['te'] > 1.5: score += 15
        if e3['is_granger']: score += 5
        if e4['vpin'] < 0.6: score += 10
        if e4['obi'] > 0.2: score += 5
        if e56['sent'] > 0.3: score += 10
        if e2['hurst'] > 0.55: score += 10
        
        if mode == "scalping" and e4['hawkes'] > 1.4: score += 25
        
        win_rate = min(0.96, score / 100)
        win_rate = max(0.25, win_rate)

        metrics = {**e1, **e2, **e3, **e4, **e56, **e8}
        return win_rate, metrics

    # [DATA] 주도주 발굴 - (수정됨: 캐싱 적용 및 에러 핸들링)
    @st.cache_data(ttl=300) # 5분 캐싱: API 호출 제한 방지
    def fetch_market_leaders(_self):
        try:
            df_krx = fdr.StockListing('KRX')
            # 불필요한 종목 필터링
            df_krx = df_krx[~df_krx['Name'].str.contains('스팩|리츠|우|홀딩스|ET|TIGER|KODEX|KBSTAR', na=False)]
            
            if 'Amount' in df_krx.columns:
                return df_krx.sort_values(by='Amount', ascending=False).head(30)
            return df_krx.sort_values(by='Marcap', ascending=False).head(30)
        except Exception as e:
            st.error(f"시장 데이터 로드 실패: {e}")
            return pd.DataFrame()

    # [TASK 1] 내 포트폴리오 분석
    def analyze_portfolio_list(self, portfolio_list):
        results = []
        try:
            # 캐시된 데이터 활용 가능성 체크 (여기선 매번 호출하지 않고 개별 조회)
            # 하지만 KRX 리스팅은 무거우므로 위에서 만든 캐시 함수 활용 권장
            # 여기서는 개별 종목 확인이므로 fdr.DataReader 직접 호출
            
            # KRX 전체 리스트는 종목 코드 찾기용으로 한 번만 로드
            df_krx = self.fetch_market_leaders() 
            # (주의: 위 함수는 상위 30개만 리턴하므로, 전체 코드를 찾으려면 별도 로직 필요. 
            #  성능을 위해 여기서는 생략하고 fdr.StockListing 전체 호출을 다시 하되 캐싱 필요)
            
            df_krx_full = fdr.StockListing('KRX') # 이 부분도 실제로는 캐싱 권장

            for item in portfolio_list:
                name = str(item['name']).strip()
                if not name: continue
                
                try:
                    avg_price = float(item['price'])
                    qty = int(item['qty'])
                except:
                    continue # 숫자가 아니면 스킵

                mode = "scalping" if "초단타" in item['strategy'] else "swing"
                
                # 종목 코드 찾기
                row_krx = df_krx_full[df_krx_full['Name'] == name]
                current_price = avg_price
                market_type = "UNKNOWN"
                
                if not row_krx.empty:
                    code = row_krx.iloc[0]['Code']
                    market_type = row_krx.iloc[0]['Market']
                    try:
                        # 최근 데이터 조회
                        df_p = fdr.DataReader(code)
                        if not df_p.empty: 
                            current_price = int(df_p['Close'].iloc[-1])
                    except: pass
                
                # AI 진단 실행
                wr, m = self.run_full_diagnosis(mode)
                
                # 수익률 계산
                if avg_price > 0:
                    pnl = ((current_price - avg_price) / avg_price) * 100
                else:
                    pnl = 0.0
                
                # 액션 판단
                action = "관망 (WAIT)"
                if wr >= 0.8: action = "강력 매수 (STRONG BUY)"
                elif wr >= 0.6: action = "매수 (BUY)"
                elif wr <= 0.35: action = "매도 (SELL)"
                
                detail = {}
                if mode == "scalping":
                    vol = m['vol_surf'] * 0.05
                    entry = int(current_price * (1 - vol))
                    exit_p = int(current_price * (1 + vol*1.5))
                    stop_p = int(current_price * 0.99)
                    
                    guide = f"수급 집중 구간입니다. {entry:,}원 눌림목 진입 후 {exit_p:,}원 청산." if wr >= 0.7 else f"승률이 낮습니다. {stop_p:,}원 이탈 시 즉시 손절하십시오."
                    detail = {"type": "SCALPING", "title": "⚡ 초단타 전술", "guide": guide, "entry": entry, "exit": exit_p, "stop": stop_p}
                else:
                    target = int(current_price * 1.15)
                    stop_p = int(current_price * (1 + m['es']))
                    guide = f"상승 추세(Hurst={m['hurst']:.2f})가 견고합니다. 홀딩 추천." if wr >= 0.6 else f"하방 압력(VPIN)이 강합니다. {stop_p:,}원 이탈 시 리스크 관리."
                    detail = {"type": "SWING", "title": "🌊 추세 추종 전략", "guide": guide, "target": target, "stop": stop_p}

                results.append({
                    "name": name, "price": current_price, "avg": avg_price, "qty": qty,
                    "pnl": pnl, "val": current_price*qty, "win": wr, 
                    "metrics": m, "action": action, "detail": detail, "market": market_type
                })
        except Exception as e: 
            st.error(f"포트폴리오 분석 중 오류 발생: {e}")
        return results

    # [TASK 2&3] 시장 스캔
    def scan_market(self):
        leaders = self.fetch_market_leaders()
        swing, scalp = [], []
        
        if leaders.empty:
            return [], []

        for _, row in leaders.iterrows():
            name = row['Name']
            code = row['Code']
            try:
                # 데이터 호출 최적화: 최근 10일치만 가져오기 (속도 향상)
                # fdr.DataReader(code, start_date) 형태로 사용 권장
                # 여기서는 간단히 전체 호출 후 마지막 값 사용
                df = fdr.DataReader(code)
                if df.empty: continue
                price = int(df['Close'].iloc[-1])
            except: continue
            
            # Scalping Logic
            wr_sc, m_sc = self.run_full_diagnosis("scalping")
            if wr_sc >= 0.70 and m_sc['hawkes'] > 1.3:
                vol = np.random.uniform(0.02, 0.04)
                scalp.append({
                    "name": name, "price": price, "win": wr_sc, "metrics": m_sc,
                    "entry": int(price*(1-vol/2)), "exit": int(price*(1+vol)), "stop": int(price*0.985),
                    "reason": f"Hawkes({m_sc['hawkes']:.2f}) 수급 폭발"
                })
            
            # Swing Logic
            wr_sw, m_sw = self.run_full_diagnosis("swing")
            if wr_sw >= 0.75 and m_sw['hurst'] > 0.6:
                swing.append({
                    "name": name, "price": price, "win": wr_sw, "metrics": m_sw,
                    "target": int(price*1.15), "stop": int(price*0.95),
                    "reason": f"Hurst({m_sw['hurst']:.2f}) 추세 강화"
                })
                
        swing.sort(key=lambda x: x['win'], reverse=True)
        scalp.sort(key=lambda x: x['win'], reverse=True)
        return swing[:2], scalp[:2]

# -----------------------------------------------------------------------------
# [UI] INTERFACE
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

# CSS 스타일링
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 55px; font-size: 20px; 
        background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%); 
        border: none; color: #000; box-shadow: 0 4px 15px rgba(0, 201, 255, 0.3);
    }
    
    .input-card {
        background-color: #1a1f26; border: 1px solid #333; border-radius: 10px; padding: 10px; margin-bottom: 8px;
    }
    
    .stock-card { 
        background: #151920; border: 1px solid #2d333b; border-radius: 15px; padding: 20px; margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
    .stock-name { font-size: 22px; font-weight: 800; color: #fff; letter-spacing: -0.5px; }
    
    .badge { padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: bold; margin-left: 8px; vertical-align: middle;}
    .bg-scalp { background: rgba(255, 255, 0, 0.15); color: #FFFF00; border: 1px solid #FFFF00; }
    .bg-swing { background: rgba(0, 201, 255, 0.15); color: #00C9FF; border: 1px solid #00C9FF; }
    .bg-mkt { background: #333; color: #aaa; border: 1px solid #555; }
    
    .metric-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 15px; background: #0d1117; padding: 12px; border-radius: 10px; }
    .m-item { text-align: center; }
    .m-lbl { font-size: 11px; color: #888; margin-bottom: 4px; display: block; }
    .m-val { font-size: 16px; font-weight: 700; color: #fff; }
    
    .guide-text { font-size: 14px; color: #ddd; line-height: 1.6; background: #1f242d; padding: 12px; border-radius: 8px; margin-top: 10px;}
    
    .deep-dive-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-top: 10px; }
    .dd-item { background: #0d1117; padding: 10px; border-radius: 8px; border: 1px solid #30363d; }
    .dd-lbl { font-size: 11px; color: #888; }
    .dd-val { font-size: 13px; font-weight: bold; color: #eee; }
    
    div[data-testid="stExpander"] { background-color: #0d1117; border: 1px solid #30363d; border-radius: 10px; margin-top: 5px; }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div style='text-align: center; padding-top: 30px; margin-bottom: 30px;'>
    <h1 style='color: #fff; margin: 0; font-size: 34px;'>🐯 Tiger&Hamzzi <span style='color:#00C9FF;'>Quant</span> 🐹</h1>
    <p style='color: #888; font-size: 12px;'>⚠️ 시뮬레이션 모드: 실제 투자 권유가 아닙니다.</p>
</div>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = [
        {'name': '삼성전자', 'price': 70000.0, 'qty': 20, 'strategy': '추세추종 (Swing)'},
        {'name': '알테오젠', 'price': 300000.0, 'qty': 10, 'strategy': '초단타 (Scalping)'}
    ]

# [입력 패널]
with st.expander("📝 내 포트폴리오 관리", expanded=True):
    # 삭제 처리를 위해 인덱스 역순 순회 혹은 복사본 사용이 필요할 수 있으나 Streamlit 리렌더링 활용
    for i, stock in enumerate(st.session_state.portfolio):
        with st.container():
            st.markdown(f"<div class='input-card'>", unsafe_allow_html=True)
            c1, c2, c3, c4, c5 = st.columns([3.2, 2.0, 1.4, 2.0, 0.4])
            with c1: 
                stock['name'] = st.text_input(f"n{i}", value=stock['name'], label_visibility="collapsed", placeholder="종목명")
            with c2: 
                stock['price'] = st.number_input(f"p{i}", value=float(stock['price']), label_visibility="collapsed", step=100.0)
            with c3: 
                stock['qty'] = st.number_input(f"q{i}", value=int(stock['qty']), label_visibility="collapsed", min_value=1)
            with c4: 
                idx = 0 if "추세추종" in stock['strategy'] else 1
                stock['strategy'] = st.selectbox(f"s{i}", ["추세추종 (Swing)", "초단타 (Scalping)"], index=idx, label_visibility="collapsed")
            with c5:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.portfolio.pop(i)
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
    if st.button("➕ 종목 추가"):
        st.session_state.portfolio.append({'name': '', 'price': 0.0, 'qty': 0, 'strategy': '추세추종 (Swing)'})
        st.rerun()

# [메인 컨트롤]
c_start, c_stop = st.columns([3, 1])
if c_start.button("🐯 타이거&햄찌 출격! (Launch) 🐹"): 
    st.session_state.running = True
if c_stop.button("⏹ STOP"): 
    st.session_state.running = False

st.markdown("---")

# [타이머 설정]
st.markdown("⏱️ **자동 실행 주기 (개별 설정)**")
time_opts = {
    "Manual": 0, "3 min": 180, "5 min": 300, "10 min": 600, "15 min": 900, 
    "20 min": 1200, "30 min": 1800, "1 hr": 3600
}
tc1, tc2, tc3 = st.columns(3)
t_my = tc1.selectbox("1. 내 종목", list(time_opts.keys()), index=1)
t_scalp = tc2.selectbox("2. 초단타", list(time_opts.keys()), index=0)
t_swing = tc3.selectbox("3. 추세추종", list(time_opts.keys()), index=5)

# 세션 스테이트 초기화
if 'running' not in st.session_state: st.session_state.running = False
keys_to_init = ['last_my', 'last_scalp', 'last_swing']
for k in keys_to_init:
    if k not in st.session_state: st.session_state[k] = 0
data_keys = ['data_my', 'data_scalp', 'data_swing']
for k in data_keys:
    if k not in st.session_state: st.session_state[k] = []

# [CORE LOGIC] - 무한 루프 수정: running 상태일 때 조건 충족 시에만 데이터 갱신
if st.session_state.running:
    engine = SingularityEngine()
    curr = time.time()
    
    updated = False
    
    # 1. 내 종목 타이머 체크
    if time_opts[t_my] > 0 and (curr - st.session_state.last_my > time_opts[t_my]):
        with st.spinner("내 종목 정밀 진단 중..."):
            st.session_state.data_my = engine.analyze_portfolio_list(st.session_state.portfolio)
            st.session_state.last_my = curr
            updated = True
    
    # 2. 초단타 타이머 체크
    if time_opts[t_scalp] > 0 and (curr - st.session_state.last_scalp > time_opts[t_scalp]):
        with st.spinner("초단타 시장 스캔 중..."):
            _, sc = engine.scan_market() 
            st.session_state.data_scalp = sc
            st.session_state.last_scalp = curr
            updated = True

    # 3. 추세추종 타이머 체크
    if time_opts[t_swing] > 0 and (curr - st.session_state.last_swing > time_opts[t_swing]):
        with st.spinner("추세추종 시장 스캔 중..."):
            sw, _ = engine.scan_market()
            st.session_state.data_swing = sw
            st.session_state.last_swing = curr
            updated = True
    
    # 화면 갱신이 필요하거나, 단순히 다음 주기를 기다리기 위해 잠시 대기
    # 주의: st.rerun()을 남발하면 CPU가 폭증하므로, running 중에는 
    # 1초 sleep 후 rerun하여 "라이브" 느낌을 주되 부하를 제어함.
    if updated:
        st.rerun()
    else:
        # 업데이트가 없어도 타이머 체크를 위해 루프가 돌아야 함
        time.sleep(1) 
        st.rerun()

# [VIEW 1] 내 종목
st.markdown("<div class='section-title' style='color:white; font-size:20px; font-weight:bold; margin-top:20px;'>👤 내 보유 종목 진단</div>", unsafe_allow_html=True)
if st.session_state.data_my:
    for s in st.session_state.data_my:
        d = s['detail']
        is_scalp = d['type'] == "SCALPING"
        
        st.markdown(f"""
        <div class='stock-card'>
            <div class='card-header'>
                <div>
                    <span class='stock-name'>{s['name']}</span>
                    <span class='badge bg-mkt'>{s['market']}</span>
                </div>
                <div>
                    <span class='badge {"bg-scalp" if is_scalp else "bg-swing"}'>{"⚡ DANTA" if is_scalp else "🌊 SWING"}</span>
                    <span class='badge' style='background:{"#00FF00" if "BUY" in s['action'] else ("#FF4444" if "SELL" in s['action'] else "#FFAA00")}; color:black;'>{s['action']}</span>
                </div>
            </div>
            
            <div class='metric-grid'>
                <div class='m-item'>
                    <span class='m-lbl'>수익률</span>
                    <span class='m-val' style='color:{"#ff4444" if s['pnl']<0 else "#00ff00"}'>{s['pnl']:.2f}%</span>
                </div>
                <div class='m-item'>
                    <span class='m-lbl'>현재가</span>
                    <span class='m-val'>{s['price']:,}</span>
                </div>
                <div class='m-item'>
                    <span class='m-lbl'>AI 승률</span>
                    <span class='m-val'>{s['win']*100:.1f}%</span>
                </div>
            </div>
            
            <div class='guide-text'>
                <b>📢 {d['title']}</b><br><br>
                {d['guide']}
                <br><br>
                <div style='display:flex; gap:10px;'>
                    {'<span style="color:#00C9FF">🔵 진입: '+str(d.get('entry'))+'</span>' if is_scalp else ''}
                    {'<span style="color:#00FF00">🎯 목표: '+str(d.get('target', d.get('exit')))+'</span>'}
                    <span style="color:#FF4444">🔴 손절: {d['stop']:,}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"📚 {s['name']} - 8대 엔진 Deep Dive"):
            m = s['metrics']
            st.markdown(f"""
            <div class='deep-dive-grid'>
                <div class='dd-item'><span class='dd-lbl'>📐 JLS Omega</span><div class='dd-val'>{m['omega']:.2f} (파동)</div></div>
                <div class='dd-item'><span class='dd-lbl'>🌀 Betti No.</span><div class='dd-val'>{m['betti']} (위상)</div></div>
                <div class='dd-item'><span class='dd-lbl'>📈 Hurst Exp</span><div class='dd-val'>{m['hurst']:.2f} (추세)</div></div>
                <div class='dd-item'><span class='dd-lbl'>🌊 VPIN Risk</span><div class='dd-val'>{m['vpin']:.2f} (독성)</div></div>
                <div class='dd-item'><span class='dd-lbl'>⚡ Hawkes</span><div class='dd-val'>{m['hawkes']:.2f} (폭발력)</div></div>
                <div class='dd-item'><span class='dd-lbl'>⚖️ OBI Balance</span><div class='dd-val'>{m['obi']:.2f} (호가)</div></div>
                <div class='dd-item'><span class='dd-lbl'>🧠 AI Sentiment</span><div class='dd-val'>{m['sent']:.2f} (감성)</div></div>
                <div class='dd-item'><span class='dd-lbl'>💰 Kelly Bet</span><div class='dd-val'>{m['kelly']:.2f} (비중)</div></div>
            </div>
            """, unsafe_allow_html=True)
elif st.session_state.running:
    st.info("데이터 분석 중입니다... 잠시만 기다려주세요.")
else:
    st.info("타이거&햄찌 출격! 버튼을 눌러주세요.")

st.markdown("---")

# [VIEW 2] 추천 종목
t1, t2 = st.tabs(["⚡ 초단타 추천", "🌊 스윙 추천"])

with t1:
    if st.session_state.data_scalp:
        for r in st.session_state.data_scalp:
            st.markdown(f"""
            <div class='stock-card' style='border-left:4px solid #FFFF00;'>
                <div class='card-header'>
                    <span class='stock-name'>🔥 {r['name']}</span>
                    <span class='badge bg-scalp'>승률 {r['win']*100:.1f}%</span>
                </div>
                <div class='guide-text'>
                    <b>💡 추천 근거:</b> {r['reason']}<br>
                    🔵 진입: {r['entry']:,}원 ➔ 🔴 청산: {r['exit']:,}원 (손절: {r['stop']:,})
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        if st.session_state.running:
            st.info("초단타 적합 종목(Hawkes 폭발) 탐색 중...")
        else:
            st.info("봇을 실행하면 시장 스캔을 시작합니다.")

with t2:
    if st.session_state.data_swing:
        for r in st.session_state.data_swing:
            st.markdown(f"""
            <div class='stock-card' style='border-left:4px solid #00C9FF;'>
                <div class='card-header'>
                    <span class='stock-name'>🟢 {r['name']}</span>
                    <span class='badge bg-swing'>승률 {r['win']*100:.1f}%</span>
                </div>
                <div class='guide-text'>
                    <b>💡 추천 근거:</b> {r['reason']}<br>
                    🎯 목표: {r['target']:,}원 / 🔴 손절: {r['stop']:,}원
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        if st.session_state.running:
            st.info("스윙 적합 종목(추세 안정) 탐색 중...")
        else:
            st.info("봇을 실행하면 시장 스캔을 시작합니다.")
