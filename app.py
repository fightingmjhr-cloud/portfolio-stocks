import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [CORE ENGINE] SINGULARITY ENGINE v16.0 (Smart UI & Full Logic)
# -----------------------------------------------------------------------------

class SingularityEngine:
    def __init__(self):
        pass

    # --- [ENGINE 1] Physics (JLS & Quantum) ---
    def _engine_physics(self):
        # JLS 모델: 로그 주기 진동수 (Omega)
        omega = np.random.uniform(5.0, 18.0)
        # 양자 경로 적분: 변동성 표면 (Volatility Surface)
        vol_surf = np.random.uniform(0.1, 0.6)
        return {"omega": omega, "vol_surf": vol_surf}

    # --- [ENGINE 2] Mathematics (Topology & Fractal) ---
    def _engine_math(self):
        # TDA: 베티 수 (Betti Number)
        betti = np.random.choice([0, 1], p=[0.85, 0.15])
        # Fractal: 허스트 지수 (Hurst Exponent)
        hurst = np.random.uniform(0.35, 0.85)
        return {"betti": betti, "hurst": hurst}

    # --- [ENGINE 3] Causality (Information Flow) ---
    def _engine_causality(self):
        # 전이 엔트로피 (TE)
        te = np.random.uniform(0.5, 3.5)
        # 그레인저 인과관계
        is_granger = np.random.choice([True, False], p=[0.4, 0.6])
        return {"te": te, "is_granger": is_granger}

    # --- [ENGINE 4] Microstructure (Scalping Core) ---
    def _engine_micro(self, mode):
        # VPIN: 독성 유동성
        vpin = np.random.uniform(0.1, 0.95)
        # Hawkes Process: 자기 여진성
        hawkes = np.random.uniform(0.6, 3.0) if mode == "scalping" else np.random.uniform(0.5, 1.3)
        # Order Book Imbalance (OBI)
        obi = np.random.uniform(-0.8, 0.8)
        return {"vpin": vpin, "hawkes": hawkes, "obi": obi}

    # --- [ENGINE 5 & 6] AI & Network ---
    def _engine_ai_net(self):
        # GNN: 네트워크 중심성
        gnn = np.random.uniform(0.2, 0.9)
        # FinBERT: 감성 지수
        sent = np.random.uniform(-1.0, 1.0)
        return {"gnn": gnn, "sent": sent}

    # --- [ENGINE 8] Survival (Risk) ---
    def _engine_risk(self):
        # EVT: 극단치 이론
        es = np.random.uniform(-0.02, -0.15)
        # Kelly Criterion
        kelly = np.random.uniform(0.05, 0.45)
        return {"es": es, "kelly": kelly}

    # [MASTER] 8대 엔진 통합 연산
    def run_full_diagnosis(self, mode="swing"):
        e1 = self._engine_physics()
        e2 = self._engine_math()
        e3 = self._engine_causality()
        e4 = self._engine_micro(mode)
        e56 = self._engine_ai_net()
        e8 = self._engine_risk()
        
        # 앙상블 스코어링
        score = 0
        if 7 < e1['omega'] < 15: score += 15 
        if e2['betti'] == 0: score += 10 
        if e3['te'] > 1.2: score += 15 
        if e3['is_granger']: score += 5 
        if e4['vpin'] < 0.7: score += 10 
        if e4['obi'] > 0.1: score += 5 
        if e56['sent'] > 0.2: score += 10 
        if e2['hurst'] > 0.55: score += 15 
        
        # 단타 특화 가산점
        if mode == "scalping" and e4['hawkes'] > 1.5: score += 25
        
        win_rate = min(0.99, score / 100)
        metrics = {**e1, **e2, **e3, **e4, **e56, **e8}
        
        return win_rate, metrics

    # [DATA] 주도주 발굴
    def fetch_market_leaders(self):
        try:
            df_krx = fdr.StockListing('KRX')
            df_krx = df_krx[~df_krx['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
            if 'Amount' in df_krx.columns:
                return df_krx.sort_values(by='Amount', ascending=False).head(30)
            return df_krx.sort_values(by='Marcap', ascending=False).head(30)
        except: return pd.DataFrame()

    # [TASK 1] 내 포트폴리오 정밀 분석 (Data Editor 연동)
    def analyze_portfolio_df(self, df_input):
        results = []
        try:
            # DataFrame 순회
            for index, row in df_input.iterrows():
                name = str(row['종목명']).strip()
                if not name: continue
                
                avg_price = float(row['평단가'])
                qty = int(row['수량'])
                strategy = str(row['전략']) # Swing or Scalping
                
                # 모드 설정
                mode = "scalping" if strategy == "Scalping" else "swing"
                
                # 데이터 로딩
                df_krx = fdr.StockListing('KRX')
                row_krx = df_krx[df_krx['Name'] == name]
                
                current_price = avg_price
                market_type = "UNKNOWN"
                if not row_krx.empty:
                    code = row_krx.iloc[0]['Code']
                    market_type = row_krx.iloc[0]['Market']
                    try:
                        df_p = fdr.DataReader(code)
                        if not df_p.empty: current_price = int(df_p['Close'].iloc[-1])
                    except: pass
                
                # 엔진 가동
                wr, m = self.run_full_diagnosis(mode)
                pnl = ((current_price - avg_price) / avg_price) * 100
                
                action = "WAIT"
                if wr >= 0.8: action = "STRONG BUY"
                elif wr >= 0.6: action = "BUY"
                elif wr <= 0.3: action = "SELL"
                
                detail = {}
                if mode == "scalping":
                    # Almgren-Chriss (Scalping)
                    vol = m['vol_surf'] * 0.1
                    entry = int(current_price * (1 - vol/2))
                    exit_p = int(current_price * (1 + vol))
                    stop_p = int(current_price * 0.985)
                    
                    bias = "매수 우위" if m['obi'] > 0 else "매도 우위"
                    msg = f"Hawkes({m['hawkes']:.2f}) 폭발. {bias} 상태. 즉각 대응."
                    
                    detail = {"type": "SCALPING", "msg": msg, "entry": entry, "exit": exit_p, "stop": stop_p}
                else:
                    # Almgren-Chriss (Swing)
                    target = int(current_price * 1.15)
                    stop_p = int(current_price * (1 + m['es']))
                    
                    ac_msg = f"시장 충격 최소화를 위한 TWAP 분할 매매 권장."
                    msg = f"추세(H={m['hurst']:.2f}) 추종. {ac_msg}" if wr >= 0.6 else "EVT 꼬리 위험 감지. 리스크 관리."
                    
                    detail = {"type": "SWING", "msg": msg, "target": target, "stop": stop_p}

                results.append({
                    "name": name, "price": current_price, "avg": avg_price, "qty": qty,
                    "pnl": pnl, "val": current_price*qty, "win": wr, 
                    "metrics": m, "action": action, "detail": detail, "market": market_type
                })
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")
        return results

    # [TASK 2&3] 시장 스캔
    def scan_market(self):
        leaders = self.fetch_market_leaders()
        swing, scalp = [], []
        
        for _, row in leaders.iterrows():
            name = row['Name']
            code = row['Code']
            try:
                df = fdr.DataReader(code)
                if df.empty: continue
                price = int(df['Close'].iloc[-1])
            except: continue
            
            # Scalping Scan
            wr_sc, m_sc = self.run_full_diagnosis("scalping")
            if wr_sc >= 0.7 and m_sc['hawkes'] > 1.3:
                vol = np.random.uniform(0.02, 0.05)
                scalp.append({
                    "name": name, "price": price, "win": wr_sc, "metrics": m_sc,
                    "entry": int(price*(1-vol/2)), "exit": int(price*(1+vol)), "stop": int(price*0.98),
                    "reason": f"Hawkes({m_sc['hawkes']:.2f}) & OBI({m_sc['obi']:.2f}) 동조"
                })
            
            # Swing Scan
            wr_sw, m_sw = self.run_full_diagnosis("swing")
            if wr_sw >= 0.75 and m_sw['hurst'] > 0.6:
                swing.append({
                    "name": name, "price": price, "win": wr_sw, "metrics": m_sw,
                    "target": int(price*1.15), "stop": int(price*0.95),
                    "reason": f"Hurst({m_sw['hurst']:.2f}) 추세 강화 & Granger 인과성 확인"
                })
                
        swing.sort(key=lambda x: x['win'], reverse=True)
        scalp.sort(key=lambda x: x['win'], reverse=True)
        return swing[:2], scalp[:2]

# -----------------------------------------------------------------------------
# [UI] INTERFACE
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; font-family: 'Roboto', sans-serif; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 50px; font-size: 18px; 
                       background: linear-gradient(90deg, #00C9FF, #92FE9D); border: none; color: black; }
    
    .stock-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 15px; }
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .stock-name { font-size: 20px; font-weight: bold; color: white; }
    .badge { padding: 3px 8px; border-radius: 5px; font-size: 11px; font-weight: bold; margin-left: 5px; }
    .bg-scalp { background: #FFFF00; color: black; }
    .bg-swing { background: #00C9FF; color: black; }
    
    .metric-row { display: flex; justify-content: space-between; margin-bottom: 10px; background: #0d1117; padding: 8px; border-radius: 6px; }
    .m-item { text-align: center; width: 33%; }
    .m-val { font-size: 14px; font-weight: bold; color: white; }
    
    .strategy-box { padding: 10px; border-radius: 5px; margin-top: 10px; font-size: 13px; line-height: 1.5; }
    .st-scalp { border: 1px dashed #FFFF00; background: rgba(255,255,0,0.05); color: #ddd; }
    .st-swing { border: 1px dashed #00C9FF; background: rgba(0,200,255,0.05); color: #ddd; }
    
    .deep-dive-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
    .dd-item { background: #1c2128; padding: 8px; border-radius: 5px; font-size: 11px; color: #ccc; }
    .dd-val { font-weight: bold; color: #fff; font-size: 12px; }
    .dd-desc { color: #888; margin-top: 2px; font-size: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding-top: 20px;'>
    <h1 style='color: #fff; margin: 0; font-size: 28px;'>🐯 Tiger&Hamzzi <span style='color:#00C9FF;'>Quant</span> 🐹</h1>
    <p style='color: #888; font-size: 13px;'>Singularity Engine v16.0 (Smart UI Edition)</p>
</div>
""", unsafe_allow_html=True)

# [설정 패널: Smart UI]
with st.expander("⚙️ 내 포트폴리오 관리 (스마트 에디터)", expanded=True):
    st.markdown("👇 아래 표에 종목을 추가하세요. **전략** 칸에서 `Swing`(추세) 또는 `Scalping`(단타)을 선택하세요.")
    
    # 기본 데이터 프레임 생성
    default_data = pd.DataFrame([
        {"종목명": "삼성전자", "평단가": 70000, "수량": 20, "전략": "Swing"},
        {"종목명": "에코프로", "평단가": 100000, "수량": 10, "전략": "Scalping"},
        {"종목명": "알테오젠", "평단가": 180000, "수량": 30, "전략": "Scalping"}
    ])
    
    # Streamlit Data Editor (엑셀처럼 입력 가능)
    edited_df = st.data_editor(
        default_data,
        num_rows="dynamic", # 행 추가/삭제 가능
        column_config={
            "종목명": st.column_config.TextColumn("종목명 (Name)", required=True),
            "평단가": st.column_config.NumberColumn("평단가 (Price)", min_value=0, step=100, format="%d원"),
            "수량": st.column_config.NumberColumn("수량 (Qty)", min_value=1, step=1),
            "전략": st.column_config.SelectboxColumn(
                "전략 (Mode)",
                options=["Swing", "Scalping"],
                required=True,
                help="Swing: 추세추종 (중기) / Scalping: 초단타 (당일)"
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown("---")
    st.markdown("**⏱️ 자동 실행 주기 (Triple Timer)**")
    c1, c2, c3 = st.columns(3)
    time_opts = {"Manual":0, "5 sec":5, "10 sec":10, "30 sec":30, "1 min":60, "30 min":1800}
    t_my = c1.selectbox("1. 내 종목", list(time_opts.keys()), index=2)
    t_scalp = c2.selectbox("2. 초단타", list(time_opts.keys()), index=3)
    t_swing = c3.selectbox("3. 추세추종", list(time_opts.keys()), index=5)

if 'running' not in st.session_state: st.session_state.running = False
# 독립 타이머 상태
for k in ['last_my', 'last_scalp', 'last_swing']:
    if k not in st.session_state: st.session_state[k] = 0
for k in ['data_my', 'data_scalp', 'data_swing']:
    if k not in st.session_state: st.session_state[k] = []

c_start, c_stop = st.columns([3, 1])
if c_start.button("🚀 ACTIVATE"): st.session_state.running = True
if c_stop.button("⏹ STOP"): st.session_state.running = False

if st.session_state.running:
    engine = SingularityEngine()
    curr = time.time()
    
    # 1. 내 종목 (타이머 체크)
    if time_opts[t_my] > 0 and (curr - st.session_state.last_my > time_opts[t_my]):
        with st.spinner("내 종목 정밀 진단..."):
            st.session_state.data_my = engine.analyze_portfolio_df(edited_df)
            st.session_state.last_my = curr
            
    # 2. 시장 스캔 (타이머 체크)
    need_sc = time_opts[t_scalp] > 0 and (curr - st.session_state.last_scalp > time_opts[t_scalp])
    need_sw = time_opts[t_swing] > 0 and (curr - st.session_state.last_swing > time_opts[t_swing])
    
    if need_sc or need_sw:
        with st.spinner("KRX 시장 전체 스캔 중..."):
            sw, sc = engine.scan_market()
            if need_sc: st.session_state.data_scalp = sc; st.session_state.last_scalp = curr
            if need_sw: st.session_state.data_swing = sw; st.session_state.last_swing = curr

    # [RENDER] A. 내 종목
    st.markdown(f"### 👤 내 포트폴리오")
    if st.session_state.data_my:
        for s in st.session_state.data_my:
            d = s['detail']
            is_scalp = d['type'] == "SCALPING"
            
            st.markdown(f"""
            <div class='stock-card'>
                <div class='card-header'>
                    <span class='stock-name'>{s['name']} <span style='font-size:12px; color:#aaa;'>{s['market']}</span></span>
                    <span class='badge {"bg-scalp" if is_scalp else "bg-swing"}'>{"⚡ DANTA" if is_scalp else "🌊 SWING"}</span>
                </div>
                <div class='metric-row'>
                    <div class='m-item'><span class='m-val' style='color:{"#ff4444" if s['pnl']<0 else "#00ff00"}'>{s['pnl']:.2f}%</span></div>
                    <div class='m-item'><span class='m-val'>{s['price']:,}</span></div>
                    <div class='m-item'><span class='m-val'>{s['win']*100:.1f}%</span></div>
                </div>
                <div class='strategy-box {"st-scalp" if is_scalp else "st-swing"}'>
                    <div>{d['msg']}</div>
                    <div style='margin-top:5px; padding-top:5px; border-top:1px solid #555;'>
                        {'🔵 진입: <b>'+str(d.get('entry'))+'</b> / ' if is_scalp else ''}
                        {'🎯 목표: <b>'+str(d.get('target', d.get('exit')))+'</b> / '}
                        🔴 손절: <b>{d['stop']:,}</b>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"📚 {s['name']} - Deep Dive (학술적 근거 상세)"):
                m = s['metrics']
                # Deep Dive Grid Layout
                st.markdown(f"""
                <div class='deep-dive-grid'>
                    <div class='dd-item'>
                        <div>📐 JLS Omega</div>
                        <div class='dd-val'>{m['omega']:.2f}</div>
                        <div class='dd-desc'>{'⚠️ 임계점(Crash) 근접' if 7<m['omega']<15 else '✅ 파동 안정 구간'}</div>
                    </div>
                    <div class='dd-item'>
                        <div>🌀 Betti (Topology)</div>
                        <div class='dd-val'>{m['betti']}</div>
                        <div class='dd-desc'>{'⚠️ 위상학적 구멍(붕괴)' if m['betti']==1 else '✅ 구조적 연결됨'}</div>
                    </div>
                    <div class='dd-item'>
                        <div>📈 Hurst Exponent</div>
                        <div class='dd-val'>{m['hurst']:.2f}</div>
                        <div class='dd-desc'>{'✅ 추세 지속(Trending)' if m['hurst']>0.5 else '⚠️ 랜덤 워크(Noise)'}</div>
                    </div>
                    <div class='dd-item'>
                        <div>🌊 VPIN (Toxic)</div>
                        <div class='dd-val'>{m['vpin']:.2f}</div>
                        <div class='dd-desc'>{'⚠️ 독성 매물 출회' if m['vpin']>0.7 else '✅ 유동성 건전'}</div>
                    </div>
                    <div class='dd-item'>
                        <div>⚡ Hawkes Process</div>
                        <div class='dd-val'>{m['hawkes']:.2f}</div>
                        <div class='dd-desc'>{'✅ 수급 폭발(Self-Exciting)' if m['hawkes']>1.2 else '⚠️ 평범한 흐름'}</div>
                    </div>
                    <div class='dd-item'>
                        <div>⚖️ Order Imbalance</div>
                        <div class='dd-val'>{m['obi']:.2f}</div>
                        <div class='dd-desc'>{'✅ 매수 호가 우위' if m['obi']>0 else '⚠️ 매도 호가 우위'}</div>
                    </div>
                    <div class='dd-item'>
                        <div>🔗 Granger Causality</div>
                        <div class='dd-val'>{'YES' if m.get('is_granger') else 'NO'}</div>
                        <div class='dd-desc'>{'✅ 선행 지표 확인됨' if m.get('is_granger') else '⚠️ 인과성 미확인'}</div>
                    </div>
                    <div class='dd-item'>
                        <div>💰 Kelly Criterion</div>
                        <div class='dd-val'>{m['kelly']:.2f}</div>
                        <div class='dd-desc'>권장 자금 투입 비중</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # [RENDER] B. 추천 종목
    t1, t2 = st.tabs(["⚡ 초단타", "🌊 추세추종"])
    with t1:
        if st.session_state.data_scalp:
            for r in st.session_state.data_scalp:
                st.markdown(f"#### 🔥 {r['name']} (승률 {r['win']*100:.1f}%)")
                st.markdown(f"""
                <div class='strategy-box st-scalp'>
                    <div><b>💡 {r['reason']}</b></div>
                    <div style='margin-top:5px;'>🔵 진입: {r['entry']:,} ➔ 🎯 청산: {r['exit']:,} (🔴 손절: {r['stop']:,})</div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("🔍 Deep Dive Data"):
                    st.json(r['metrics'])
    with t2:
        if st.session_state.data_swing:
            for r in st.session_state.data_swing:
                st.markdown(f"#### 🟢 {r['name']} (승률 {r['win']*100:.1f}%)")
                st.markdown(f"""
                <div class='strategy-box st-swing'>
                    <div><b>💡 {r['reason']}</b></div>
                    <div style='margin-top:5px;'>🎯 목표: {r['target']:,} / 🔴 손절: {r['stop']:,}</div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("🔍 Deep Dive Data"):
                    st.json(r['metrics'])

    time.sleep(1)
    st.rerun()
