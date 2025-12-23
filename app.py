import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random

# -----------------------------------------------------------------------------
# [0] SETUP & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

# [Custom CSS: Luxury Dark Theme]
st.markdown("""
<style>
    /* Global Background */
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    
    /* Luxury Gold Buttons */
    .stButton>button { 
        width: 100%; border-radius: 10px; font-weight: 700; height: 50px; font-size: 16px;
        background: linear-gradient(135deg, #2b2b2b 0%, #1a1a1a 100%); 
        border: 1px solid #444; color: #d4af37; /* Gold Text */
        box-shadow: 0 4px 10px rgba(0,0,0,0.5); transition: 0.3s;
    }
    .stButton>button:hover { 
        border-color: #d4af37; box-shadow: 0 0 15px rgba(212, 175, 55, 0.3); transform: translateY(-2px);
    }
    
    /* Input Fields */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #121212 !important; color: #fff !important; 
        border: 1px solid #333 !important; border-radius: 6px;
    }
    
    /* Stock Card Container */
    .stock-card { 
        background: #121212; border: 1px solid #333; border-radius: 12px; 
        padding: 20px; margin-bottom: 25px; box-shadow: 0 8px 20px rgba(0,0,0,0.6);
    }
    
    /* Progress Bar */
    .prog-bg { background: #333; height: 8px; border-radius: 4px; width: 100%; margin: 10px 0; }
    .prog-fill { height: 100%; border-radius: 4px; }
    
    /* Badge & Tags */
    .score-badge { 
        background: #222; border: 1px solid; padding: 4px 12px; 
        border-radius: 20px; font-size: 13px; font-weight: bold; 
    }
    .tag { 
        display: inline-block; padding: 3px 8px; border-radius: 4px; 
        font-size: 11px; margin-right: 5px; font-weight: bold; background: #1a1a1a; 
    }
    
    /* Persona Box */
    .persona-box { padding: 15px; border-radius: 8px; margin-top: 10px; background: #1a1a1a; border-left-width: 3px; border-left-style: solid;}
    
    /* Info Grid */
    .info-grid { display: flex; justify-content: space-between; border-top: 1px solid #333; margin-top: 15px; padding-top: 10px; }
    .info-item { text-align: center; width: 48%; }
    
    /* Font sizes */
    .small-text { font-size: 12px; color: #888; }
    .big-text { font-size: 18px; font-weight: bold; color: #fff; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #d4af37;'>🐯 Tiger&Hamzzi Quant 🐹</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [1] INITIALIZE STATE (Fixing AttributeError)
# -----------------------------------------------------------------------------
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'ideal_list' not in st.session_state: st.session_state.ideal_list = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 
if 'target_return' not in st.session_state: st.session_state.target_return = 5.0
if 'my_diagnosis' not in st.session_state: st.session_state.my_diagnosis = []
# [CRITICAL FIX] Ensure this key exists
if 'market_view_mode' not in st.session_state: st.session_state.market_view_mode = None 
if 'l_my' not in st.session_state: st.session_state.l_my = 0
if 'l_top3' not in st.session_state: st.session_state.l_top3 = 0
if 'l_sep' not in st.session_state: st.session_state.l_sep = 0
if 'trigger_my' not in st.session_state: st.session_state.trigger_my = False
if 'trigger_top3' not in st.session_state: st.session_state.trigger_top3 = False
if 'trigger_sep' not in st.session_state: st.session_state.trigger_sep = False

TIME_OPTS = {"⛔ 수동": 0, "⏱️ 3분": 180, "⏱️ 10분": 600, "⏱️ 30분": 1800}

# -----------------------------------------------------------------------------
# [2] DATA & LOGIC ENGINE
# -----------------------------------------------------------------------------
@st.cache_data(ttl=86400)
def get_stock_list():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df['Name'].tolist()
    except: return ["삼성전자", "SK하이닉스", "LG에너지솔루션", "POSCO홀딩스", "NAVER"]

@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

class SingularityEngine:
    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H')}"
        seed_val = zlib.crc32(unique_key.encode())
        np.random.seed(seed_val)
        return {
            "omega": np.random.uniform(5.0, 25.0), "vol_surf": np.random.uniform(0.1, 0.9),
            "betti": np.random.choice([0, 1], p=[0.85, 0.15]), "hurst": np.random.uniform(0.2, 0.99),
            "te": np.random.uniform(0.1, 5.0), "vpin": np.random.uniform(0.0, 1.0),
            "hawkes": np.random.uniform(0.1, 4.0), "obi": np.random.uniform(-1.0, 1.0),
            "gnn": np.random.uniform(0.1, 1.0), "sent": np.random.uniform(-1.0, 1.0),
            "es": np.random.uniform(-0.01, -0.30), "kelly": np.random.uniform(0.01, 0.30)
        }

    def run_diagnosis(self, name, mode="swing"):
        m = self._calculate_metrics(name, mode)
        score = 35.0 
        tags = [{'label': '기본 마진', 'val': '+35', 'type': 'base'}]

        if m['vpin'] > 0.6: score -= 20; tags.append({'label': '독성 매물(VPIN)', 'val': '-20', 'type': 'bad'})
        if m['es'] < -0.20: score -= 15; tags.append({'label': 'Tail Risk(ES)', 'val': '-15', 'type': 'bad'})
        if m['betti'] == 1: score -= 10; tags.append({'label': '위상 붕괴(TDA)', 'val': '-10', 'type': 'bad'})
        
        if mode == "scalping":
            if m['hawkes'] > 2.5: score += 45; tags.append({'label': '🚀 Hawkes 폭발', 'val': '+45', 'type': 'best'})
            elif m['hawkes'] > 1.5: score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'type': 'good'})
        else: 
            if m['hurst'] > 0.75: score += 40; tags.append({'label': '📈 추세 지속(Hurst)', 'val': '+40', 'type': 'best'})
            elif m['hurst'] > 0.6: score += 10; tags.append({'label': '↗️ 모멘텀 양호', 'val': '+10', 'type': 'good'})

        if m['gnn'] > 0.8: score += 10; tags.append({'label': '👑 GNN 대장주', 'val': '+10', 'type': 'good'})

        win_rate = min(0.95, max(0.10, score / 100))
        return win_rate, m, tags

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        volatility = m['vol_surf'] * 0.05
        if mode == "scalping":
            target = int(price * (1 + max(volatility, 0.02)))
            stop = int(price * (1 - volatility * 0.5))
        else:
            target = int(price * (1 + (target_return/100)))
            stop = int(price * 0.93)
        
        can_buy = int((cash * m['kelly']) / price) if price > 0 else 0

        # Persona Logic (Detailed)
        if wr >= 0.70:
            h_brief = f"사장님! <b>[Hawkes {m['hawkes']:.2f}]</b> 수치 봤어?! 이건 단순 수급이 아니라 '폭발'이야! 🚀 <b>[GNN]</b> 중심성도 높아서 돈이 다 여기로 쏠리고 있어!"
            h_act = f"쫄지마! <b>{can_buy}주</b> 시장가 매수! <b>{target:,}원</b> 뚫으면 불타기 가즈아!"
            h_why = "변동성(Vol)이 살아있고 모멘텀(Hurst)이 확실해. 리스크 감수하고 수익 극대화할 타이밍이야!"
            
            t_brief = f"허허, <b>[내재가치]</b> 대비 저평가로군. 수급과 펀더멘털이 조화로워. <b>[JLS 모델]</b>상 임계점까지 여유가 있어."
            t_act = f"안전마진이 확보됐네. <b>{int(can_buy*0.8)}주</b> 정도 비중을 실어서 진득하게 동행하게."
            t_why = "기업 펀더멘털이 훼손되지 않았고, 기술적으로도 과열권이 아니야. 편안한 자리일세."
        elif wr >= 0.50:
            h_brief = f"음~ <b>[Hurst {m['hurst']:.2f}]</b> 추세 살아있네! 단타 놀이터야! 🎢 <b>[OBI]</b> 호가창 매수세가 꿈틀대고 있어."
            h_act = f"일단 <b>{int(can_buy/3)}주</b>만 정찰병 보내고, <b>{price:,}원</b> 지지하면 나머지 태워!"
            h_why = "모멘텀은 좋은데 눈치 싸움 중이야. 짧게 치고 빠지는 게릴라 전술이 유효해."
            
            t_brief = f"계륵일세. 🐅 <b>[변동성 {m['vol_surf']:.2f}]</b>이 너무 심해. '내우외환'이 걱정되는군. <b>[꼬리 위험]</b>이 도사리고 있어."
            t_act = f"욕심 버리고 <b>{int(can_buy*0.2)}주</b>만 분할로 담게. '유비무환'의 자세가 필요해."
            t_why = "변동성이 너무 커. 자칫하면 큰 내상을 입을 수 있어. 리스크 관리가 우선이야."
        else:
            h_brief = f"으악! 돔황챠!! 😱 <b>[VPIN {m['vpin']:.2f}]</b> 경고등 켜졌어! 폭탄 돌리기 중이야! 💣"
            h_act = "절대 매수 금지! ❌ 탈출은 지능순이야! 현금 쥐고 숨어!"
            h_why = "독성 매물이 쏟아지고 있어. 지금 들어가면 계좌 녹는다. 파산 확률 99%."
            
            t_brief = f"에잉 쯧쯧! 😡 <b>[독성 매물]</b>이 넘쳐나는구먼! 사상누각이야! 기초가 부실한데 어찌 오르겠나!"
            t_act = "쳐다도 보지 말게. 현금이 곧 최고의 종목이야. 🛡️"
            t_why = "스마트 머니는 이미 떠났어. 떨어지는 칼날을 맨손으로 잡으려 하지 말게."

        return {
            "prices": (price, target, stop),
            "hamzzi": {"brief": h_brief, "act": h_act, "why": h_why},
            "hojji": {"brief": t_brief, "act": t_act, "why": t_why}
        }

    def diagnose_portfolio(self, portfolio, cash, target_return):
        asset_val = sum([s['price'] * s['qty'] for s in portfolio])
        total_val = asset_val + cash
        cash_ratio = (cash / total_val * 100) if total_val > 0 else 100
        
        beta = np.random.uniform(0.5, 2.0)
        mdd = np.random.uniform(-5.0, -35.0)
        
        h_msg = f"사장님! 현금 <b>{cash_ratio:.1f}%</b> 실화야? 😱 <b>[Cash Drag]</b> 때문에 수익률 갉아먹고 있어!<br><b>[Beta {beta:.2f}]</b>도 너무 낮아. 야수의 심장으로 <b>[주도주]</b> 태워야지! 🔥"
        t_msg = f"자네 현금이 <b>{cash_ratio:.1f}%</b>뿐인가? 😡 하락장 오면 <b>[MDD {mdd:.1f}%]</b> 맞고 깡통 찰 텐가? '유비무환'을 잊지 말게!<br>리스크 관리가 엉망이야. <b>[우량주]</b> 비중을 늘리게."
        return h_msg, t_msg

# -----------------------------------------------------------------------------
# [3] RENDERER (Clean HTML)
# -----------------------------------------------------------------------------
def render_card_ui(d, idx=None, is_rank=False):
    p = d['plan']
    win_pct = d['win'] * 100
    
    # Colors
    color = "#00FF00" if d['win'] >= 0.7 else "#FFAA00" if d['win'] >= 0.5 else "#FF4444"
    
    # Rank Badge
    rank_html = f"<div style='position:absolute; top:0; left:0; background:linear-gradient(45deg, #FF416C, #FF4B2B); color:white; padding:4px 10px; border-radius:10px 0 10px 0; font-weight:bold; font-size:12px; z-index:1;'>{idx+1}위</div>" if is_rank else ""
    
    # Tags
    tag_html = ""
    for t in d['tags']:
        tc = "#00FF00" if t['type'] == 'best' else "#00C9FF" if t['type'] == 'good' else "#FF4444"
        tag_html += f"<span class='tag' style='color:{tc}; border:1px solid {tc};'>{t['label']} {t['val']}</span>"

    # MAIN CARD HTML
    st.markdown(f"""
    <div class='stock-card' style='position:relative; border-color:{color};'>
        {rank_html}
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; padding-left:{50 if is_rank else 0}px;'>
            <div><span class='stock-name'>{d['name']}</span> <span class='small-text'>{d.get('mode','')}</span></div>
            <span class='score-badge' style='color:{color}; border-color:{color};'>Score {win_pct:.1f}</span>
        </div>
        
        <div class='prog-bg'><div class='prog-fill' style='width:{win_pct}%; background:{color};'></div></div>
        
        <div style='margin: 10px 0;'>{tag_html}</div>
        
        <div class='info-grid'>
            <div class='info-item'>
                <span class='small-text'>현재가</span><br>
                <span class='big-text'>{d['price']:,}</span>
            </div>
            <div class='info-item'>
                <span class='small-text'>수익률</span><br>
                <span class='big-text' style='color:{"#FF4444" if d.get("pnl", 0) < 0 else "#00FF00"}'>{d.get("pnl", 0):.2f}%</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # TABS
    t1, t2, t3 = st.tabs(["🐹 햄찌", "🐯 호찌", "📊 엔진 HUD"])
    
    with t1:
        h = p['hamzzi']
        st.markdown(f"""
        <div class='persona-box' style='border-left-color: #FFAA00;'>
            <div class='persona-title' style='color:#FFAA00;'>🐹 햄찌의 야수 본능 (인생 한방! 🔥)</div>
            <div style='margin-bottom:10px;'>{h['brief']}</div>
            <div style='background:#222; padding:10px; border-radius:8px; margin-bottom:10px;'><b>💡 행동 지침:</b> {h['act']}</div>
            <div class='small-text'><b>🎯 근거:</b> {h['why']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with t2:
        t = p['hojji']
        st.markdown(f"""
        <div class='persona-box' style='border-left-color: #FF4444;'>
            <div class='persona-title' style='color:#FF4444;'>🐯 호찌의 유비무환 (방어형 🛡️)</div>
            <div style='margin-bottom:10px;'>{t['brief']}</div>
            <div style='background:#222; padding:10px; border-radius:8px; margin-bottom:10px;'><b>💡 어르신 말씀:</b> {t['act']}</div>
            <div class='small-text'><b>🎯 근거:</b> {t['why']}</div>
        </div>
        """, unsafe_allow_html=True)

    with t3:
        m = d['m']
        st.markdown(f"""
        <div class='hud-grid'>
            <div class='hud-item'><span class='small-text'>JLS 파동</span><br><span class='big-text' style='font-size:14px;'>{m['omega']:.1f}</span></div>
            <div class='hud-item'><span class='small-text'>독성(VPIN)</span><br><span class='big-text' style='font-size:14px;'>{m['vpin']:.2f}</span></div>
            <div class='hud-item'><span class='small-text'>수급(Hawkes)</span><br><span class='big-text' style='font-size:14px;'>{m['hawkes']:.2f}</span></div>
            <div class='hud-item'><span class='small-text'>호가(OBI)</span><br><span class='big-text' style='font-size:14px;'>{m['obi']:.2f}</span></div>
            <div class='hud-item'><span class='small-text'>추세(Hurst)</span><br><span class='big-text' style='font-size:14px;'>{m['hurst']:.2f}</span></div>
            <div class='hud-item'><span class='small-text'>네트워크(GNN)</span><br><span class='big-text' style='font-size:14px;'>{m['gnn']:.2f}</span></div>
        </div>
        """, unsafe_allow_html=True)

    # TIMELINE
    st.markdown(f"""
    <div class='stock-card' style='margin-top:-20px; border-top:none; border-radius:0 0 12px 12px; padding: 15px;'>
        <div class='timeline'>
            <div class='t-item'><span class='small-text'>진입/평단</span><br><span class='t-val' style='color:#00C9FF'>{p['prices'][0]:,}</span></div>
            <div class='t-item'><span class='small-text'>목표가</span><br><span class='t-val' style='color:#00FF00'>{p['prices'][1]:,}</span></div>
            <div class='t-item'><span class='small-text'>손절가</span><br><span class='t-val' style='color:#FF4444'>{p['prices'][2]:,}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [4] UI LOGIC
# -----------------------------------------------------------------------------
stock_names = get_stock_list()

with st.expander("💰 내 자산 및 포트폴리오 설정", expanded=True):
    st.markdown("#### 📸 OCR 이미지 스캔 (시뮬레이션)")
    uploaded = st.file_uploader("", type=['png','jpg'], label_visibility="collapsed")
    if uploaded:
        with st.spinner("OCR 분석 중..."): time.sleep(1)
        st.success("스캔 완료! 포트폴리오가 업데이트되었습니다.")
        st.session_state.portfolio = [
            {'name':'삼성전자', 'price':70000, 'qty':100, 'strategy':'추세추종'},
            {'name':'SK하이닉스', 'price':135000, 'qty':20, 'strategy':'추세추종'}
        ]

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.caption("**예수금 (KRW)**")
        st.session_state.cash = st.number_input("cash", value=st.session_state.cash, step=100000, label_visibility="collapsed")
    with c2: 
        st.caption("**목표 수익률 (%)**")
        st.session_state.target_return = st.number_input("target", value=st.session_state.target_return, step=1.0, label_visibility="collapsed")
    with c3:
        st.caption("**종목 추가**")
        if st.button("➕ 추가"):
            st.session_state.portfolio.append({'name':'삼성전자', 'price':0, 'qty':0, 'strategy':'추세추종'})
            st.rerun()

    st.markdown("---")
    if st.session_state.portfolio:
        for i, s in enumerate(st.session_state.portfolio):
            cols = st.columns([3, 2, 1.5, 2, 0.5])
            with cols[0]: 
                st.caption(f"**종목명 {i+1}**")
                try: idx = stock_names.index(s['name'])
                except: idx = 0
                s['name'] = st.selectbox(f"n_{i}", stock_names, index=idx, label_visibility="collapsed")
            with cols[1]: 
                st.caption("**평단가**")
                s['price'] = st.number_input(f"p_{i}", value=float(s['price']), label_visibility="collapsed")
            with cols[2]: 
                st.caption("**수량**")
                s['qty'] = st.number_input(f"q_{i}", value=int(s['qty']), label_visibility="collapsed")
            with cols[3]: 
                st.caption("**전략**")
                s['strategy'] = st.selectbox(f"s_{i}", ["추세추종", "초단타"], index=0 if s['strategy']=="추세추종" else 1, label_visibility="collapsed")
            with cols[4]: 
                st.caption("삭제")
                if st.button("🗑️", key=f"d_{i}"): 
                    st.session_state.portfolio.pop(i)
                    st.rerun()

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# Main Actions
c_btn, c_timer = st.columns([2, 1])
with c_btn:
    if st.button("📝 내 종목 및 포트폴리오 정밀 진단"):
        st.session_state.trigger_my = True
        st.rerun()
with c_timer:
    auto_my = st.selectbox("자동진단", list(TIME_OPTS.keys()), index=0, label_visibility="collapsed")

if st.session_state.my_diagnosis:
    st.markdown("---")
    if 'port_analysis' in st.session_state:
        pa = st.session_state.port_analysis
        st.markdown(f"""
        <div class='stock-card' style='border:1px solid #aaa;'>
            <div style='font-size:18px; font-weight:bold; margin-bottom:15px; color:#fff;'>📊 포트폴리오 종합 진단</div>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:15px;'>
                <div class='persona-box' style='border-left-color: #FFAA00; margin-top:0;'>
                    <div style='color:#FFAA00; font-weight:bold; margin-bottom:5px;'>🐹 햄찌 (공격형)</div>
                    <div style='font-size:13px; color:#ccc; line-height:1.5;'>{pa['hamzzi']}</div>
                </div>
                <div class='persona-box' style='border-left-color: #FF4444; margin-top:0;'>
                    <div style='color:#FF4444; font-weight:bold; margin-bottom:5px;'>🐯 호찌 (방어형)</div>
                    <div style='font-size:13px; color:#ccc; line-height:1.5;'>{pa['hojji']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("👤 보유 종목 상세 분석")
    for d in st.session_state.my_diagnosis: render_card_ui(d)

st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)
st.subheader("📡 시장 정밀 타격 (Market Intelligence)")

c1, c2 = st.columns(2)
with c1:
    if st.button("🏆 타이거&햄찌 출격! (Top 3)"):
        st.session_state.trigger_top3 = True
        st.session_state.market_view_mode = 'TOP3'
        st.rerun()
    auto_top3 = st.selectbox("Top3 타이머", list(TIME_OPTS.keys()), index=0, label_visibility="collapsed")

with c2:
    if st.button("📊 단타 / 추세 (전략별 보기)"):
        st.session_state.trigger_sep = True
        st.session_state.market_view_mode = 'SEPARATE'
        st.rerun()
    auto_sep = st.selectbox("전략별 타이머", list(TIME_OPTS.keys()), index=0, label_visibility="collapsed")

if st.session_state.market_view_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("<h5>🏆 금일의 Singularity Ideal Pick (Top 3)</h5>", unsafe_allow_html=True)
    for i, d in enumerate(st.session_state.ideal_list): render_card_ui(d, i, is_rank=True)

elif st.session_state.market_view_mode == 'SEPARATE' and st.session_state.sc_list:
    st.markdown("<h5>📊 전략별 절대 랭킹 (Top 3)</h5>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["⚡ 초단타", "🌊 추세추종"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_card_ui(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_card_ui(d, i, is_rank=True)

# -----------------------------------------------------------------------------
# [5] LOGIC RUNNER
# -----------------------------------------------------------------------------
now = time.time()
need_rerun = False

# My Diagnosis Trigger
if st.session_state.trigger_my or (TIME_OPTS[auto_my] > 0 and now - st.session_state.l_my > TIME_OPTS[auto_my]):
    engine = SingularityEngine(); market_data = load_top50_data(); my_res = []
    
    # Port Diagnosis
    h_port, t_port = engine.diagnose_portfolio(st.session_state.portfolio, st.session_state.cash, st.session_state.target_return)
    st.session_state.port_analysis = {'hamzzi': h_port, 'hojji': t_port}
    
    with st.spinner("내 포트폴리오 정밀 해부 중..."):
        for s in st.session_state.portfolio:
            if not s['name']: continue
            mode = "scalping" if s['strategy'] == "초단타" else "swing"
            price = s['price']
            match = market_data[market_data['Name'] == s['name']]
            if not match.empty: price = int(match.iloc[0]['Close'])
            else: price = int(s['price']) if s['price'] > 0 else 10000
            
            wr, m, tags = engine.run_diagnosis(s['name'], mode)
            plan = engine.generate_report(mode, price, m, wr, st.session_state.cash, s['qty'], st.session_state.target_return)
            pnl = ((price - s['price'])/s['price']*100) if s['price']>0 else 0
            my_res.append({'name': s['name'], 'price': price, 'pnl': pnl, 'win': wr, 'm': m, 'tags': tags, 'plan': plan, 'mode': mode})
    
    st.session_state.my_diagnosis = my_res
    st.session_state.l_my = now
    st.session_state.trigger_my = False
    need_rerun = True

# Market Scan Trigger
if st.session_state.trigger_top3 or (TIME_OPTS[auto_top3] > 0 and now - st.session_state.l_top3 > TIME_OPTS[auto_top3]):
    run_market_scan('TOP3')
    st.session_state.l_top3 = now
    need_rerun = True

if st.session_state.trigger_sep or (TIME_OPTS[auto_sep] > 0 and now - st.session_state.l_sep > TIME_OPTS[auto_sep]):
    run_market_scan('SEPARATE')
    st.session_state.l_sep = now
    need_rerun = True

if need_rerun: st.rerun()
if TIME_OPTS[auto_my]>0 or TIME_OPTS[auto_top3]>0 or TIME_OPTS[auto_sep]>0: time.sleep(1); st.rerun()
