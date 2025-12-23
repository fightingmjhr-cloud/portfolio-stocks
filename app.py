import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [0] GLOBAL SETTINGS
# -----------------------------------------------------------------------------
TIME_OPTS = {
    "⛔ 수동 (멈춤)": 0, "⏱️ 3분": 180, "⏱️ 5분": 300, "⏱️ 10분": 600, 
    "⏱️ 30분": 1800, "⏱️ 1시간": 3600
}

@st.cache_data(ttl=86400)
def get_stock_list():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df['Name'].tolist()
    except: return ["삼성전자", "SK하이닉스", "LG에너지솔루션"]

@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

# -----------------------------------------------------------------------------
# [1] CORE ENGINE: EXPERT ANALYSIS
# -----------------------------------------------------------------------------
class SingularityEngine:
    def __init__(self):
        pass

    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H')}"
        seed_val = zlib.crc32(unique_key.encode())
        np.random.seed(seed_val)
        
        # 8대 엔진 (Simulation)
        m = {
            "omega": np.random.uniform(5.0, 25.0), "vol_surf": np.random.uniform(0.1, 0.9),
            "betti": np.random.choice([0, 1], p=[0.85, 0.15]), "hurst": np.random.uniform(0.2, 0.95),
            "te": np.random.uniform(0.1, 5.0), "vpin": np.random.uniform(0.0, 1.0),
            "hawkes": np.random.uniform(0.1, 4.0), "obi": np.random.uniform(-1.0, 1.0),
            "gnn": np.random.uniform(0.1, 1.0), "sent": np.random.uniform(-1.0, 1.0),
            "es": np.random.uniform(-0.01, -0.30), "kelly": np.random.uniform(0.01, 0.30)
        }
        np.random.seed(None)
        return m

    def run_diagnosis(self, name, mode="swing"):
        m = self._calculate_metrics(name, mode)
        score = 35.0 
        tags = [{'label': '기본 마진', 'val': '+35', 'type': 'base'}]

        if m['vpin'] > 0.6: score -= 15; tags.append({'label': '독성 매물', 'val': '-15', 'type': 'bad'})
        if m['es'] < -0.15: score -= 15; tags.append({'label': '폭락 징후', 'val': '-15', 'type': 'bad'})
        
        if mode == "scalping":
            if m['hawkes'] > 2.5: score += 40; tags.append({'label': '🚀 퍼펙트 수급', 'val': '+40', 'type': 'best'})
            elif m['hawkes'] > 1.5: score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'type': 'good'})
        else: 
            if m['hurst'] > 0.75: score += 35; tags.append({'label': '📈 대세 상승장', 'val': '+35', 'type': 'best'})
            elif m['hurst'] > 0.6: score += 10; tags.append({'label': '↗️ 추세 양호', 'val': '+10', 'type': 'good'})

        win_rate = min(0.92, max(0.15, score / 100))
        return win_rate, m, tags

    # [EXPERT REPORT GENERATOR] - 어려운 용어 사용
    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        if mode == "scalping":
            vol = m['vol_surf'] * 0.04
            entry = int(price * (1 - vol)); target = int(price * (1 + vol*1.5)); stop = int(price * (1 - vol*0.7))
        else:
            entry = price; target = int(price * (1 + target_return/100)); stop = int(price * 0.93)

        # 🐹 HAMZZI (Quant Expert)
        h_style = "border: 2px solid #FFAA00; color: #FFAA00;"
        if wr >= 0.75:
            h_an = f"현재 <b>[Hawkes Process]</b>의 강도가 {m['hawkes']:.2f}로 Self-Exciting 임계치를 초과했습니다. 이는 <b>[Order Flow Imbalance]</b>가 양의 방향으로 극대화된 상태입니다."
            h_act = "Alpha 창출 기회입니다. 레버리지를 활용하여 Aggressive하게 진입하십시오."
        elif wr >= 0.55:
            h_an = f"<b>[Hurst Exponent]</b>가 {m['hurst']:.2f}로 Mean Reversion보다는 Trend Following이 유리한 구간입니다. 단, <b>[Vol Surface]</b>의 Skew가 다소 가파릅니다."
            h_act = "Position Sizing을 조절하여 분할 매수(Scale-in) 하십시오."
        else:
            h_an = f"<b>[VPIN]</b>(Volume-Synchronized Probability of Informed Trading) 수치가 위험 수준입니다. 이는 Adverse Selection Risk가 높음을 시사합니다."
            h_act = "Liquidity를 회수하고 Market Neutral 포지션을 유지하십시오."

        # 🐯 TIGER (Fundamental Expert)
        t_style = "border: 2px solid #FF4444; color: #FF4444;"
        if wr >= 0.75:
            t_an = f"내재가치(Intrinsic Value) 대비 저평가 구간이며, <b>[PEG Ratio]</b> 측면에서도 성장성이 담보되어 있네. <b>[Economic Moat]</b>가 견고해 보이는군."
            t_act = "안전마진(Margin of Safety)이 충분하니 비중을 확대하게."
        elif wr >= 0.55:
            t_an = f"펀더멘털은 양호하나 <b>[Systematic Risk]</b>(체계적 위험)가 남아있어. <b>[CAPEX]</b> 투자 효율성을 좀 더 지켜봐야겠네."
            t_act = "돌다리도 두들겨 보고 건너게. 분산 투자(Diversification) 원칙을 지켜."
        else:
            t_an = f"이 기업은 <b>[Going Concern]</b>(계속기업)으로서의 가치가 의심되네. 부채비율과 <b>[Cash Flow]</b>가 악화되고 있어. 사상누각일세."
            t_act = "손실 회피(Loss Aversion) 편향을 버리고 과감히 청산하게."

        return {
            "prices": (entry, target, stop),
            "hamzzi": {"analysis": h_an, "action": h_act, "style": h_style},
            "tiger": {"analysis": t_an, "action": t_act, "style": t_style}
        }

    # [PORTFOLIO DIAGNOSIS]
    def diagnose_portfolio(self, portfolio, market_data):
        # Simulated Portfolio Metrics
        sharpe = np.random.uniform(0.5, 2.5)
        beta = np.random.uniform(0.8, 1.5)
        alpha = np.random.uniform(-0.05, 0.10)
        
        h_msg = f"포트폴리오의 <b>[Sharpe Ratio]</b>가 {sharpe:.2f}입니다. <b>[Beta]</b>가 {beta:.2f}로 시장 민감도가 높으니, <b>[Hedging]</b> 전략이 필요해요. <b>[Idiosyncratic Risk]</b>(비체계적 위험) 관리가 시급합니다!"
        t_msg = f"자네 포트폴리오는 <b>[Safety Margin]</b>이 부족해. <b>[Asset Allocation]</b>(자산 배분)이 너무 공격적이야. 경기 방어주(Defensive Stock) 비중을 높여 <b>[MDD]</b>를 낮추게."
        
        return h_msg, t_msg

    # [TERM TRANSLATOR]
    def explain_term(self):
        return """
        <div style='background:#111; padding:15px; border-radius:10px; border:1px solid #333; font-size:13px; color:#ccc;'>
        <b>📚 용어 해설 (Translator)</b><br>
        • <b>Hawkes Process:</b> 매수세가 또 다른 매수를 부르는 '주문 폭주' 현상<br>
        • <b>VPIN:</b> 기관들이 정보 우위를 이용해 몰래 팔아치우는 '독성 매물' 비율<br>
        • <b>Hurst Exponent:</b> 추세의 강도. 0.5보다 크면 추세 지속, 작으면 평균 회귀<br>
        • <b>Economic Moat (경제적 해자):</b> 경쟁사가 넘볼 수 없는 독점적 경쟁 우위<br>
        • <b>Sharpe Ratio:</b> 위험 한 단위당 얻는 초과 수익 (높을수록 좋음)<br>
        • <b>Idiosyncratic Risk:</b> 시장 전체가 아닌, 그 종목만의 고유한 악재 위험
        </div>
        """

# -----------------------------------------------------------------------------
# [2] UI & RENDERERS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    .app-title { text-align: center; font-size: 36px; font-weight: 900; color: #fff; padding: 30px 0; text-shadow: 0 0 20px rgba(0,201,255,0.8); }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: 800; height: 50px; background: linear-gradient(135deg, #00C9FF, #92FE9D); border: none; color: #000; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px rgba(0,201,255,0.5); }
    
    /* Card Styles */
    .stock-card { background: #111; border-radius: 16px; padding: 20px; margin-bottom: 20px; border: 1px solid #333; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
    .stock-name { font-size: 24px; font-weight: bold; color: #fff; }
    .win-rate { font-size: 14px; font-weight: bold; padding: 5px 12px; border-radius: 20px; background: #222; }
    
    /* Persona Box */
    .persona-box { padding: 15px; border-radius: 12px; margin-top: 10px; background: #1a1a1a; }
    .persona-title { font-weight: bold; margin-bottom: 8px; font-size: 16px; display: flex; align-items: center; gap: 8px; }
    .analysis-text { font-size: 14px; line-height: 1.6; color: #ddd; margin-bottom: 10px; }
    .action-text { font-size: 14px; font-weight: bold; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; }
    
    /* Portfolio Dashboard */
    .port-dash { background: #1a1a1a; padding: 20px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #444; }
    .port-title { font-size: 18px; font-weight: bold; color: #fff; margin-bottom: 15px; border-bottom: 1px solid #333; padding-bottom: 10px; }
    
    /* Badges */
    .tag { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; margin-right: 5px; font-weight: bold; color: #000; }
    .tag-base { background: #888; } .tag-best { background: #00FF00; } .tag-good { background: #00C9FF; } .tag-bad { background: #FF4444; color: #fff; }
    
    /* Timeline */
    .timeline { display: flex; justify-content: space-between; background: #000; padding: 10px; border-radius: 8px; margin-top: 10px; border: 1px solid #333; }
    .t-item { text-align: center; } .t-val { font-weight: bold; color: #fff; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-title'>🐯 Tiger&Hamzzi Quant 🐹</div>", unsafe_allow_html=True)

# [STATE INIT]
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'ideal_list' not in st.session_state: st.session_state.ideal_list = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 
if 'target_return' not in st.session_state: st.session_state.target_return = 5.0
if 'my_diagnosis' not in st.session_state: st.session_state.my_diagnosis = []
# Timers
if 'l_my' not in st.session_state: st.session_state.l_my = 0
if 'l_top3' not in st.session_state: st.session_state.l_top3 = 0
if 'l_sep' not in st.session_state: st.session_state.l_sep = 0
# Triggers
if 'trigger_my' not in st.session_state: st.session_state.trigger_my = False
if 'trigger_top3' not in st.session_state: st.session_state.trigger_top3 = False
if 'trigger_sep' not in st.session_state: st.session_state.trigger_sep = False
if 'view_mode' not in st.session_state: st.session_state.view_mode = 'BOTH'

stock_names = get_stock_list()

# [EXECUTION FUNCTIONS]
def run_my_diagnosis():
    engine = SingularityEngine(); market_data = load_top50_data(); my_res = []
    
    # Portfolio Analysis First
    h_port, t_port = engine.diagnose_portfolio(st.session_state.portfolio, market_data)
    st.session_state.port_analysis = {'hamzzi': h_port, 'tiger': t_port}
    
    with st.spinner("내 포트폴리오 정밀 해부 중..."):
        for s in st.session_state.portfolio:
            if not s['name']: continue
            mode = "scalping" if s['strategy'] == "초단타" else "swing"
            price = s['price']
            match = market_data[market_data['Name'] == s['name']]
            if not match.empty: price = int(match.iloc[0]['Close'])
            else:
                try: df = fdr.StockListing('KRX'); code = df[df['Name'] == s['name']].iloc[0]['Code']; p = fdr.DataReader(code); price = int(p['Close'].iloc[-1])
                except: pass
            
            wr, m, tags = engine.run_diagnosis(s['name'], mode)
            plan = engine.generate_report(mode, price, m, wr, st.session_state.cash, s['qty'], st.session_state.target_return)
            pnl = ((price - s['price'])/s['price']*100) if s['price']>0 else 0
            my_res.append({'name': s['name'], 'price': price, 'pnl': pnl, 'win': wr, 'm': m, 'tags': tags, 'plan': plan})
    
    st.session_state.my_diagnosis = my_res
    st.session_state.l_my = time.time()
    st.session_state.trigger_my = False

def run_market_scan(mode):
    engine = SingularityEngine(); market_data = load_top50_data()
    sc, sw, ideal = [], [], []
    with st.spinner("시장 전체 스캔 및 8대 엔진 가동 중..."):
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close'])); name = row['Name']
            
            wr_sc, m_sc, t_sc = engine.run_diagnosis(name, "scalping")
            p_sc = engine.generate_report("scalping", price, m_sc, wr_sc, st.session_state.cash, 0, st.session_state.target_return)
            item_sc = {'name': name, 'price': price, 'win': wr_sc, 'mode': '초단타', 'tags': t_sc, 'plan': p_sc, 'm': m_sc}
            sc.append(item_sc)
            
            wr_sw, m_sw, t_sw = engine.run_diagnosis(name, "swing")
            p_sw = engine.generate_report("swing", price, m_sw, wr_sw, st.session_state.cash, 0, st.session_state.target_return)
            item_sw = {'name': name, 'price': price, 'win': wr_sw, 'mode': '추세추종', 'tags': t_sw, 'plan': p_sw, 'm': m_sw}
            sw.append(item_sw)
            
            if wr_sc >= wr_sw: ideal.append(item_sc)
            else: ideal.append(item_sw)
            
    sc.sort(key=lambda x: x['win'], reverse=True); sw.sort(key=lambda x: x['win'], reverse=True); ideal.sort(key=lambda x: x['win'], reverse=True)
    st.session_state.sc_list = sc[:3]; st.session_state.sw_list = sw[:3]; st.session_state.ideal_list = ideal[:3]
    
    if mode == 'TOP3': 
        st.session_state.l_top3 = time.time()
        st.session_state.trigger_top3 = False
    else: 
        st.session_state.l_sep = time.time()
        st.session_state.trigger_sep = False

# [UI: PERSONAL PORTFOLIO]
with st.expander("💰 내 자산 및 포트폴리오 관리", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1: st.session_state.cash = st.number_input("예수금 (KRW)", value=st.session_state.cash, step=100000)
    with c2: st.session_state.target_return = st.number_input("목표 수익률 (%)", value=st.session_state.target_return, step=1.0)
    with c3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ 종목 추가", use_container_width=True):
            st.session_state.portfolio.append({'name': '삼성전자', 'price': 0, 'qty': 0, 'strategy': '추세추종'})
            st.rerun()
    st.markdown("---")
    if st.session_state.portfolio:
        for i, s in enumerate(st.session_state.portfolio):
            c1, c2, c3, c4, c5 = st.columns([3.2, 1.8, 1.3, 2.0, 0.4])
            with c1: 
                try: idx = stock_names.index(s['name'])
                except: idx = 0
                s['name'] = st.selectbox(f"n{i}", stock_names, index=idx, label_visibility="collapsed")
            with c2: s['price'] = st.number_input(f"p{i}", value=float(s['price']), label_visibility="collapsed")
            with c3: s['qty'] = st.number_input(f"q{i}", value=int(s['qty']), label_visibility="collapsed")
            with c4: s['strategy'] = st.selectbox(f"s{i}", ["추세추종", "초단타"], index=0 if s['strategy']=="추세추종" else 1, label_visibility="collapsed")
            with c5: 
                if st.button("🗑️", key=f"d{i}"): st.session_state.portfolio.pop(i); st.rerun()
    else: st.info("보유 종목이 없습니다.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📝 내 종목만 진단하기", use_container_width=True):
        st.session_state.trigger_my = True
        st.rerun()
    auto_my = st.selectbox("⏱️ 내 종목 자동진단 주기", list(TIME_OPTS.keys()), index=0, key="tm_my", label_visibility="collapsed")

# [RENDER CARD FUNCTION]
def render_full_card(d, idx=None, is_rank=False):
    engine = SingularityEngine() # Local instance for translator
    p = d['plan']
    
    # 1. Tags
    tag_html = "".join([f"<span class='tag tag-{t['type']}'>{t['label']} {t['val']}</span> " for t in d['tags']])
    
    # 2. Win Rate Bar
    win_pct = d['win'] * 100
    color = "#00FF00" if d['win'] >= 0.75 else "#FFAA00" if d['win'] >= 0.55 else "#FF4444"
    bar_html = f"<div style='background:#333; height:6px; border-radius:3px; margin-top:5px;'><div style='width:{win_pct}%; background:{color}; height:100%; border-radius:3px;'></div></div>"
    
    # 3. Rank Badge
    rank_html = f"<div class='rank-ribbon'>{idx+1}위</div>" if is_rank else ""

    st.markdown(f"""
    <div class='stock-card'>
        {rank_html}
        <div class='card-header' style='padding-left:{50 if is_rank else 0}px'>
            <div>
                <span class='stock-name'>{d['name']}</span>
                <span style='color:#ccc; font-size:14px; margin-left:10px;'>{d.get('mode','')}</span>
            </div>
            <div class='win-rate' style='color:{color}; border:1px solid {color};'>AI Score {win_pct:.1f}</div>
        </div>
        {bar_html}
        <div style='margin-top:10px; margin-bottom:10px;'>{tag_html}</div>
        {'<div class="info-grid"><div class="info-item"><span class="info-label">현재가</span><span class="info-val">'+f"{d['price']:,}"+'</span></div><div class="info-item"><span class="info-label">수익률</span><span class="info-val" style="color:'+("#ff4444" if d.get('pnl',0)<0 else "#00ff00")+f'">{d.get("pnl",0):.2f}%</span></div></div>' if not is_rank else ''}
    </div>
    """, unsafe_allow_html=True)

    # 4. Persona Tabs
    t1, t2, t3 = st.tabs(["🐹 햄찌의 퀀트 분석", "🐯 호랑이의 가치 분석", "📚 용어 해설"])
    
    with t1:
        h = p['hamzzi']
        st.markdown(f"""
        <div class='persona-box' style='{h['style']}'>
            <div class='persona-title'>🐹 햄찌 (High Risk Quant)</div>
            <div class='analysis-text'>{h['analysis']}</div>
            <div class='action-text'>{h['action']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with t2:
        t = p['tiger']
        st.markdown(f"""
        <div class='persona-box' style='{t['style']}'>
            <div class='persona-title'>🐯 호랑이 (Fundamental Value)</div>
            <div class='analysis-text'>{t['analysis']}</div>
            <div class='action-text'>{t['action']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with t3:
        st.markdown(engine.explain_term(), unsafe_allow_html=True)

    # 5. Timeline
    st.markdown(f"""
    <div class='stock-card' style='margin-top:-20px; border-top:none; border-radius:0 0 16px 16px;'>
        <div class='timeline'>
            <div class='t-item'><span style='color:#888; font-size:12px;'>진입/추매</span><br><span class='t-val' style='color:#00C9FF'>{p['prices'][0]:,}</span></div>
            <div class='t-item'><span style='color:#888; font-size:12px;'>목표가</span><br><span class='t-val' style='color:#00FF00'>{p['prices'][1]:,}</span></div>
            <div class='t-item'><span style='color:#888; font-size:12px;'>손절가</span><br><span class='t-val' style='color:#FF4444'>{p['prices'][2]:,}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# [MY DIAGNOSIS & PORTFOLIO HEALTH]
if st.session_state.my_diagnosis:
    st.markdown("---")
    # Portfolio Dashboard
    if 'port_analysis' in st.session_state:
        pa = st.session_state.port_analysis
        st.markdown(f"""
        <div class='port-dash'>
            <div class='port-title'>📊 포트폴리오 종합 진단 (Portfolio Health)</div>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:15px;'>
                <div style='background:#222; padding:15px; border-radius:8px; border:1px solid #FFAA00;'>
                    <div style='color:#FFAA00; font-weight:bold; margin-bottom:5px;'>🐹 햄찌의 퀀트 평가</div>
                    <div style='font-size:13px; color:#ddd;'>{pa['hamzzi']}</div>
                </div>
                <div style='background:#222; padding:15px; border-radius:8px; border:1px solid #FF4444;'>
                    <div style='color:#FF4444; font-weight:bold; margin-bottom:5px;'>🐯 호랑이의 가치 평가</div>
                    <div style='font-size:13px; color:#ddd;'>{pa['tiger']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h5>👤 내 보유 종목 상세 분석</h5>", unsafe_allow_html=True)
    for d in st.session_state.my_diagnosis: render_full_card(d, is_rank=False)

# [MARKET SCAN SECTION]
st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)
st.markdown("#### 📡 시장 정밀 타격 (Market Intelligence)")
st.markdown("<br>", unsafe_allow_html=True)

b1, b2 = st.columns(2)
with b1:
    if st.button("🏆 타이거&햄찌 출격! (Top 3)"):
        st.session_state.trigger_top3 = True
        st.session_state.market_view_mode = 'TOP3'
        st.rerun()
    auto_top3 = st.selectbox("타이머1", list(TIME_OPTS.keys()), index=0, key="tm_top3", label_visibility="collapsed")

with b2:
    if st.button("📊 단타 / 추세 (전략별 보기)"):
        st.session_state.trigger_sep = True
        st.session_state.market_view_mode = 'SEPARATE'
        st.rerun()
    auto_sep = st.selectbox("타이머2", list(TIME_OPTS.keys()), index=0, key="tm_sep", label_visibility="collapsed")

# [RENDER MARKET RESULTS]
if st.session_state.market_view_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("<h5>🏆 금일의 Singularity Ideal Pick (Top 3)</h5>", unsafe_allow_html=True)
    for i, d in enumerate(st.session_state.ideal_list): render_full_card(d, i, is_rank=True)

elif st.session_state.market_view_mode == 'SEPARATE' and (st.session_state.sc_list or st.session_state.sw_list):
    st.markdown("<h5>📊 전략별 절대 랭킹 (Top 3)</h5>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["⚡ 초단타", "🌊 추세추종"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_full_card(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_full_card(d, i, is_rank=True)

# [AUTO REFRESH LOGIC]
now = time.time()
need_rerun = False

t_val_my = TIME_OPTS[auto_my]
if st.session_state.trigger_my or (t_val_my > 0 and now - st.session_state.l_my > t_val_my):
    run_my_diagnosis(); need_rerun = True

t_val_top3 = TIME_OPTS[auto_top3]
if st.session_state.trigger_top3 or (t_val_top3 > 0 and now - st.session_state.l_top3 > t_val_top3):
    run_market_scan('TOP3'); need_rerun = True

t_val_sep = TIME_OPTS[auto_sep]
if st.session_state.trigger_sep or (t_val_sep > 0 and now - st.session_state.l_sep > t_val_sep):
    run_market_scan('SEPARATE'); need_rerun = True

if need_rerun: st.rerun()
if t_val_my > 0 or t_val_top3 > 0 or t_val_sep > 0: time.sleep(1); st.rerun()
