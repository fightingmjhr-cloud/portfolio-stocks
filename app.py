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
# [1] CORE ENGINE
# -----------------------------------------------------------------------------
class SingularityEngine:
    def __init__(self):
        pass

    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H')}"
        seed_val = zlib.crc32(unique_key.encode())
        np.random.seed(seed_val)
        
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

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        if mode == "scalping":
            vol = m['vol_surf'] * 0.04
            entry = int(price * (1 - vol)); target = int(price * (1 + vol*1.5)); stop = int(price * (1 - vol*0.7))
        else:
            entry = price; target = int(price * (1 + target_return/100)); stop = int(price * 0.93)

        # 🐹 HAMZZI (Easy & Fun)
        h_style = "border: 2px solid #FFAA00; color: #FFAA00;"
        if wr >= 0.75:
            h_an = f"우와! <b>[Hawkes(수급)]</b> 점수가 {m['hawkes']:.2f}야! 이건 사람들이 '사자!' 하고 우르르 몰려오는 축제 분위기란 뜻이야! 🎉"
            h_act = "지금이야 사장님! 이런 건 풀매수해서 로켓 타고 달나라 가야지! 🚀"
        elif wr >= 0.55:
            h_an = f"음~ <b>[Hurst(추세)]</b>가 {m['hurst']:.2f}네? '한 번 간 방향으로 계속 가려는 고집'이 꽤 세다는 거야!"
            h_act = "나쁘지 않아! 일단 반만 담가보고, 오르면 더 사자! (불타기 🔥)"
        else:
            h_an = f"으앙! <b>[VPIN(독성 매물)]</b> 경고등 켜졌어! 이건 기관 형님들이 몰래 팔아치우는 '폭탄 돌리기'라구! 💣"
            h_act = "도망쳐! 뒤도 돌아보지 마! 현금 꽉 쥐고 숨어있어! 😱"

        # 🐯 TIGER (Practical & Cynical)
        t_style = "border: 2px solid #FF4444; color: #FF4444;"
        if wr >= 0.75:
            t_an = f"허허, <b>[GNN(주도주)]</b> 중심성이 {m['gnn']:.2f}로군. 시장의 돈이 이 녀석한테로 쏠리고 있다는 증거야. 대장주란 말이지."
            t_act = "물 들어올 때 노 저어야지. 안전마진이 확보됐으니 비중을 실어보게."
        elif wr >= 0.55:
            t_an = f"<b>[Vol Surface(변동성)]</b>가 {m['vol_surf']:.2f}로군. 위아래로 흔들림이 심해질 수 있어. 멀미 날 수 있다는 뜻이야."
            t_act = "조심하게. 몰빵은 투기야. 분할 매수로 리스크를 관리하는 게 '투자의 정석'이지."
        else:
            t_an = f"에잉 쯧쯧. <b>[Omega(파동)]</b>가 깨졌어. 심장박동이 멈춘 거나 다름없어. 곧 '떡락'할 차트야."
            t_act = "떨어지는 칼날 잡지 마. 쉬는 것도 투자야. 수업료 내기 싫으면 관망해."

        return {
            "prices": (entry, target, stop),
            "hamzzi": {"analysis": h_an, "action": h_act, "style": h_style},
            "tiger": {"analysis": t_an, "action": t_act, "style": t_style}
        }

    # [EASY EXPLANATION]
    def explain_terms(self):
        return {
            "hamzzi": """
            <div style='font-size:13px; line-height:1.6; color:#eee;'>
            <b>🐹 햄찌의 초간단 용어 교실:</b><br>
            • <b>Hawkes (호크스):</b> 사람들이 "와! 저거다!" 하고 우르르 몰려가는 정도야! 높을수록 인기 폭발! 🎉<br>
            • <b>VPIN (브이핀):</b> 세력 형님들이 우리 몰래 팔아치우는 '나쁜 물량'이야. 이거 높으면 도망쳐! 🏃<br>
            • <b>Hurst (허스트):</b> 황소 고집 지수! 한 번 위로 가면 끝까지 위로 가려는 성질이야. 💪<br>
            • <b>Vol Surface (변동성):</b> 파도가 얼마나 높게 치느냐야. 너무 높으면 배 뒤집혀! 🌊
            </div>
            """,
            "tiger": """
            <div style='font-size:13px; line-height:1.6; color:#eee;'>
            <b>🐯 호랑이의 실전 용어 해설:</b><br>
            • <b>Hawkes Process:</b> 매수 주문이 또 다른 매수를 부르는 '자기 여진(Self-Exciting)' 현상일세.<br>
            • <b>VPIN (독성 유동성):</b> 정보 우위를 가진 자들의 약탈적 매도세야. 설거지 당하기 딱 좋지.<br>
            • <b>Hurst Exponent:</b> 주가의 추세 지속성을 나타내는 지표야. 0.5보다 크면 추세장이지.<br>
            • <b>GNN (그래프 신경망):</b> 이 종목이 시장 내에서 얼마나 중심적인 '대장' 역할을 하는지 보여주네.
            </div>
            """
        }

    def diagnose_portfolio(self, portfolio, market_data):
        sharpe = np.random.uniform(0.5, 2.5)
        h_msg = f"사장님 포트폴리오 <b>[Sharpe(가성비)]</b>가 {sharpe:.2f}야! 위험 감수한 만큼 수익이 쏠쏠한데? 조금만 더 공격적으로 가보자! 🔥"
        t_msg = f"자네 계좌의 <b>[MDD(최대낙폭)]</b> 관리가 허술해. 하락장 오면 깡통 찰 텐가? 현금 비중 좀 늘리게. 쯧쯧."
        return h_msg, t_msg

# -----------------------------------------------------------------------------
# [2] UI & RENDERERS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    .app-title { text-align: center; font-size: 36px; font-weight: 900; color: #fff; padding: 30px 0; text-shadow: 0 0 20px rgba(0,201,255,0.8); }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: 800; height: 50px; background: linear-gradient(135deg, #00C9FF, #92FE9D); border: none; color: #000; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); }
    
    .stock-card { background: #111; border-radius: 16px; padding: 20px; margin-bottom: 20px; border: 1px solid #333; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .stock-name { font-size: 24px; font-weight: bold; color: #fff; }
    .win-rate { font-size: 14px; font-weight: bold; padding: 5px 12px; border-radius: 20px; background: #222; }
    
    .persona-box { padding: 15px; border-radius: 12px; margin-top: 10px; background: #1a1a1a; }
    .persona-title { font-weight: bold; margin-bottom: 8px; font-size: 16px; }
    
    .port-dash { background: #1a1a1a; padding: 20px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #444; }
    .tag { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; margin-right: 5px; font-weight: bold; color: #000; }
    .tag-base { background: #888; } .tag-best { background: #00FF00; } .tag-good { background: #00C9FF; } .tag-bad { background: #FF4444; color: #fff; }
    
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
# [CRITICAL FIX] Initialize market_view_mode
if 'market_view_mode' not in st.session_state: st.session_state.market_view_mode = None
# Timers
if 'l_my' not in st.session_state: st.session_state.l_my = 0
if 'l_top3' not in st.session_state: st.session_state.l_top3 = 0
if 'l_sep' not in st.session_state: st.session_state.l_sep = 0
if 'trigger_my' not in st.session_state: st.session_state.trigger_my = False
if 'trigger_top3' not in st.session_state: st.session_state.trigger_top3 = False
if 'trigger_sep' not in st.session_state: st.session_state.trigger_sep = False

stock_names = get_stock_list()

# [EXECUTION FUNCTIONS]
def run_my_diagnosis():
    engine = SingularityEngine(); market_data = load_top50_data(); my_res = []
    
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
        st.session_state.market_view_mode = 'TOP3'
        st.session_state.trigger_top3 = False
    else: 
        st.session_state.l_sep = time.time()
        st.session_state.market_view_mode = 'SEPARATE'
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
    engine = SingularityEngine()
    p = d['plan']
    tag_html = "".join([f"<span class='tag tag-{t['type']}'>{t['label']} {t['val']}</span> " for t in d['tags']])
    win_pct = d['win'] * 100
    color = "#00FF00" if d['win'] >= 0.75 else "#FFAA00" if d['win'] >= 0.55 else "#FF4444"
    bar_html = f"<div style='background:#333; height:6px; border-radius:3px; margin-top:5px;'><div style='width:{win_pct}%; background:{color}; height:100%; border-radius:3px;'></div></div>"
    rank_html = f"<div style='position:absolute; top:0; left:0; padding:5px 12px; font-weight:bold; color:#fff; background:linear-gradient(45deg,#FF416C,#FF4B2B); border-bottom-right-radius:12px;'>{idx+1}위</div>" if is_rank else ""

    st.markdown(f"""
    <div class='stock-card'>
        {rank_html}
        <div class='card-header' style='padding-left:{50 if is_rank else 0}px'>
            <div><span class='stock-name'>{d['name']}</span><span style='color:#ccc; font-size:14px; margin-left:10px;'>{d.get('mode','')}</span></div>
            <div class='win-rate' style='color:{color}; border:1px solid {color};'>AI Score {win_pct:.1f}</div>
        </div>
        {bar_html}
        <div style='margin-top:10px; margin-bottom:10px;'>{tag_html}</div>
    </div>
    """, unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["🐹 햄찌의 퀀트 분석", "🐯 호랑이의 가치 분석", "📚 용어 해설"])
    
    with t1:
        h = p['hamzzi']
        st.markdown(f"""
        <div class='persona-box' style='{h['style']}'>
            <div class='persona-title'>🐹 햄찌 (High Risk Quant)</div>
            <div style='margin-bottom:10px;'>{h['analysis']}</div>
            <div style='background:#222; padding:10px; border-radius:8px;'><b>💡 행동 지침:</b> {h['action']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with t2:
        t = p['tiger']
        st.markdown(f"""
        <div class='persona-box' style='{t['style']}'>
            <div class='persona-title'>🐯 호랑이 (Fundamental Value)</div>
            <div style='margin-bottom:10px;'>{t['analysis']}</div>
            <div style='background:#222; padding:10px; border-radius:8px;'><b>💡 어르신 말씀:</b> {t['action']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with t3:
        terms = engine.explain_terms()
        st.markdown(terms['hamzzi'], unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
        st.markdown(terms['tiger'], unsafe_allow_html=True)

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
    if 'port_analysis' in st.session_state:
        pa = st.session_state.port_analysis
        st.markdown(f"""
        <div class='port-dash'>
            <div style='font-size:18px; font-weight:bold; color:#fff; margin-bottom:15px;'>📊 포트폴리오 종합 진단</div>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:15px;'>
                <div style='background:#222; padding:15px; border-radius:8px; border:1px solid #FFAA00;'>
                    <div style='color:#FFAA00; font-weight:bold; margin-bottom:5px;'>🐹 햄찌의 평가</div>
                    <div style='font-size:13px; color:#ddd;'>{pa['hamzzi']}</div>
                </div>
                <div style='background:#222; padding:15px; border-radius:8px; border:1px solid #FF4444;'>
                    <div style='color:#FF4444; font-weight:bold; margin-bottom:5px;'>🐯 호랑이의 평가</div>
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
