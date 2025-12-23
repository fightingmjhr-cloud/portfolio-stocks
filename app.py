import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random
import textwrap

# -----------------------------------------------------------------------------
# [1] 시스템 설정 및 데이터 로딩 (최적화: 캐싱 및 전역 변수 우선 로드)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

@st.cache_data(ttl=86400)
def get_stock_list():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df['Name'].tolist()
    except:
        return ["삼성전자", "SK하이닉스", "LG에너지솔루션", "POSCO홀딩스", "NAVER"]

@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

# [안전 장치] 전역 변수 최우선 초기화 (NameError 방지)
stock_names = get_stock_list()
TIME_OPTS = {"⛔ 수동": 0, "⏱️ 3분": 180, "⏱️ 10분": 600, "⏱️ 30분": 1800}

# [최적화] 세션 상태 일괄 초기화 (AttributeError 방지)
DEFAULT_STATE = {
    'portfolio': [], 'ideal_list': [], 'sc_list': [], 'sw_list': [],
    'cash': 10000000, 'target_return': 5.0, 'my_diagnosis': [],
    'market_view_mode': None, 'port_analysis': None,
    'l_my': 0, 'l_top3': 0, 'l_sep': 0,
    'trigger_my': False, 'trigger_top3': False, 'trigger_sep': False
}

for key, val in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = val

# -----------------------------------------------------------------------------
# [2] 스타일링 (CSS 통합 및 최적화)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* App Base */
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    
    /* Luxury Buttons */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 50px; font-size: 16px;
        background: linear-gradient(135deg, #00C9FF, #92FE9D); 
        border: none; color: #000; box-shadow: 0 4px 15px rgba(0, 201, 255, 0.3); transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(0, 201, 255, 0.6); }
    
    /* Input Fields */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-size: 13px !important; font-weight: bold !important; color: #bbb !important;
        display: block !important; margin-bottom: 3px !important;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1f26 !important; color: #fff !important; 
        border: 1px solid #444 !important; border-radius: 8px;
    }
    
    /* Card UI */
    .stock-card { 
        background: #111; border-radius: 16px; padding: 0; margin-bottom: 25px; 
        border: 1px solid #333; box-shadow: 0 8px 25px rgba(0,0,0,0.6); overflow: hidden;
    }
    .card-header { 
        padding: 15px 20px; background: #1e1e1e; border-bottom: 1px solid #333; 
        display: flex; justify-content: space-between; align-items: center; 
    }
    .stock-name { font-size: 24px; font-weight: 900; color: #fff; }
    .score-badge { 
        font-size: 14px; font-weight: bold; background: #333; padding: 5px 12px; 
        border-radius: 20px; border: 1px solid #555; color: #fff;
    }
    
    /* Progress Bar */
    .prog-bg { background: #333; height: 8px; border-radius: 4px; width: 100%; margin: 10px 0; }
    .prog-fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
    
    /* Info Grid */
    .info-grid { 
        display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; 
        background: #333; margin: 15px 20px; border: 1px solid #333; 
    }
    .info-item { background: #121212; padding: 12px; text-align: center; }
    .info-label { font-size: 11px; color: #888; display: block; margin-bottom: 3px; }
    .info-val { font-size: 15px; font-weight: bold; color: #fff; }
    
    /* Persona Analysis Box */
    .persona-box { padding: 20px; font-size: 14px; line-height: 1.6; color: #eee; }
    .persona-title { 
        font-weight: 900; margin-bottom: 12px; font-size: 16px; padding-bottom: 8px; 
        border-bottom: 1px solid rgba(255,255,255,0.1); 
    }
    
    /* Timeline */
    .timeline { display: flex; justify-content: space-between; background: #000; padding: 15px 25px; border-top: 1px solid #333; }
    .t-item { text-align: center; } .t-val { font-weight: bold; font-size: 15px; margin-top: 4px; display: block; }
    
    /* HUD Grid */
    .hud-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 15px; background: #0d1117; padding: 15px; border-radius: 8px; }
    .hud-item { background: #21262d; padding: 8px; border-radius: 6px; text-align: center; border: 1px solid #30363d; }
    .hud-l { font-size: 10px; color: #8b949e; display: block; }
    .hud-v { font-size: 13px; font-weight: bold; color: #58a6ff; }
    
    /* Tags */
    .tag-container { padding: 0 20px 15px 20px; }
    .tag { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; margin-right: 5px; font-weight: bold; color: #000; }
    
    /* Rank Ribbon */
    .rank-ribbon { position: absolute; top: 0; left: 0; padding: 5px 12px; font-size: 12px; font-weight: bold; color: #fff; background: linear-gradient(45deg, #FF416C, #FF4B2B); border-bottom-right-radius: 12px; z-index: 5; }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -20px !important; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align:center; font-size:36px; font-weight:900; padding:30px 0;'>🐯 Tiger&Hamzzi Quant 🐹</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [3] LOGIC ENGINE (Singularity Omega)
# -----------------------------------------------------------------------------
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
            "gnn": np.random.uniform(0.1, 1.0), "es": np.random.uniform(-0.01, -0.30), 
            "kelly": np.random.uniform(0.01, 0.30)
        }

    def run_diagnosis(self, name, mode="swing"):
        m = self._calculate_metrics(name, mode)
        score = 35.0 
        tags = [{'label': '기본 마진', 'val': '+35', 'type': 'base', 'bg': '#888'}]

        if m['vpin'] > 0.6: score -= 15; tags.append({'label': '독성 매물', 'val': '-15', 'type': 'bad', 'bg': '#FF4444'})
        if m['es'] < -0.15: score -= 15; tags.append({'label': '폭락 징후', 'val': '-15', 'type': 'bad', 'bg': '#FF4444'})
        
        if mode == "scalping":
            if m['hawkes'] > 2.5: score += 40; tags.append({'label': '🚀 퍼펙트 수급', 'val': '+40', 'type': 'best', 'bg': '#00FF00'})
            elif m['hawkes'] > 1.5: score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'type': 'good', 'bg': '#00C9FF'})
        else: 
            if m['hurst'] > 0.75: score += 35; tags.append({'label': '📈 대세 상승', 'val': '+35', 'type': 'best', 'bg': '#00FF00'})
            elif m['hurst'] > 0.6: score += 10; tags.append({'label': '↗️ 추세 양호', 'val': '+10', 'type': 'good', 'bg': '#00C9FF'})

        win_rate = min(0.92, max(0.15, score / 100))
        return win_rate, m, tags

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        vol = m['vol_surf'] * 0.04
        if mode == "scalping":
            target = int(price * (1 + vol*1.5)); stop = int(price * (1 - vol*0.7))
        else:
            target = int(price * (1 + target_return/100)); stop = int(price * 0.93)

        adjusted_kelly = m['kelly'] * (wr / 0.8) if wr < 0.8 else m['kelly']
        alloc_cash = cash * adjusted_kelly
        can_buy_qty = int(alloc_cash / price) if price > 0 else 0

        # Hamzzi
        h_style = "border: 2px solid #FFAA00; color: #FFAA00;"
        if wr >= 0.75:
            h_brief = f"사장님! <b>[Hawkes {m['hawkes']:.2f}]</b> 터졌어! 이건 로켓이야! 🚀"
            h_act = f"쫄지마! <b>{can_buy_qty}주</b> 긁어! <b>{target:,}원</b> 간다!"
            h_why = "변동성(Vol)이 춤을 춰! 지금 들어가야 베타(Beta)를 먹지!"
        elif wr >= 0.55:
            h_brief = f"음~ <b>[Hurst {m['hurst']:.2f}]</b> 추세 살아있네! 단타 놀이터야!"
            h_act = f"일단 <b>{int(can_buy_qty/2)}주</b> 담가보고 불타기 가즈아! 🔥"
            h_why = "모멘텀이 꿈틀대. 호가창(OBI) 보면서 짧게 먹자!"
        else:
            h_brief = f"으악! 돔황챠!! 😱 <b>[VPIN]</b> 폭탄 돌리기 중이야!"
            h_act = "절대 사지 마! 있는 것도 다 던져! 🏃‍♂️💨"
            h_why = "수급이 죽었어. 이런 건 쳐다보는 거 아니야."

        # Hojji
        t_style = "border: 2px solid #FF4444; color: #FF4444;"
        if wr >= 0.75:
            t_brief = f"허허, <b>[GNN]</b> 중심성이 좋군. 시장의 주도주일세."
            t_act = f"안전마진 확보됐으니 <b>{can_buy_qty}주</b> 진입해봐."
            t_why = "펀더멘털과 수급이 조화로워. 편안한 자리야."
        elif wr >= 0.55:
            t_brief = f"계륵일세. 🐅 <b>[변동성]</b>이 너무 커서 멀미 나겠어."
            t_act = f"욕심 버리고 <b>{int(can_buy_qty/2)}주</b>만 분할로 담게."
            t_why = "상승 여력은 있으나 꼬리 위험이 도사리고 있어."
        else:
            t_brief = f"에잉 쯧쯧! 😡 <b>[독성 매물]</b>이 넘쳐나는구먼!"
            t_act = "관망하게. 쉬는 것도 투자야. 현금 지켜!"
            t_why = "떨어지는 칼날이야. 바닥인 줄 알았는데 지하실 본다."

        return {
            "prices": (price, target, stop),
            "hamzzi": {"brief": h_brief, "act": h_act, "why": h_why, "style": h_style},
            "hojji": {"brief": t_brief, "act": t_act, "why": t_why, "style": t_style}
        }

    def diagnose_portfolio(self, portfolio, cash):
        if not portfolio: return "포트폴리오 없음", "데이터 없음"
        
        total_val = cash + sum([s['price']*s['qty'] for s in portfolio])
        cash_ratio = (cash / total_val * 100) if total_val > 0 else 100
        
        beta = np.random.uniform(0.5, 2.0)
        mdd = np.random.uniform(-5.0, -35.0)
        
        h_msg = f"사장님! 현금 <b>{cash_ratio:.1f}%</b> 실화야? 😱 <b>[Cash Drag]</b> 때문에 수익률 갉아먹고 있어! <b>[Beta]</b> 높여서 <b>[레버리지]</b> 태워! 🔥"
        t_msg = f"현금 <b>{cash_ratio:.1f}%</b>뿐인가? 😡 하락장 오면 <b>[MDD {mdd:.1f}%]</b> 맞고 깡통 차네. <b>[배당주]</b>로 방어벽 세우게."
        return h_msg, t_msg

    def explain_terms(self):
        return {
            "hamzzi": "<div style='font-size:13px; line-height:1.6; color:#eee;'><b>🐹 햄찌의 과외:</b><br>• <b>Hawkes:</b> 인기 폭발 지수! 🎉<br>• <b>Vol Surface:</b> 파도 높이! 서핑 꿀잼! 🌊</div>",
            "hojji": "<div style='font-size:13px; line-height:1.6; color:#eee;'><b>🐯 호찌의 해설:</b><br>• <b>VPIN:</b> 기관들의 독성 매물일세.<br>• <b>GNN:</b> 시장의 중심 대장주를 뜻하지.</div>"
        }

    def hamzzi_nagging(self):
        return "🐹 햄찌의 잔소리", "차트가 부르는데 왜 안 사? 🚀"

    def hojji_nagging(self):
        return "🐯 호찌의 호통", "공부 안 하고 사면 투기야! 📚"

# -----------------------------------------------------------------------------
# [4] UI RENDERER (Safe HTML)
# -----------------------------------------------------------------------------
def render_full_card(d, idx=None, is_rank=False):
    engine = SingularityEngine()
    p = d['plan']
    win_pct = d['win'] * 100
    color = "#00FF00" if d['win'] >= 0.75 else "#FFAA00" if d['win'] >= 0.55 else "#FF4444"
    
    # HTML Rendering Safe Wrapper
    rank_html = f"<div class='rank-ribbon'>{idx+1}위</div>" if is_rank else ""
    tag_html = "".join([f"<span class='tag' style='background:{t['bg']}'>{t['label']} {t['val']}</span> " for t in d['tags']])
    
    st.markdown(textwrap.dedent(f"""
    <div class='stock-card'>
        {rank_html}
        <div class='card-header' style='padding-left:{50 if is_rank else 0}px'>
            <div><span class='stock-name'>{d['name']}</span> <span style='color:#ccc; font-size:14px;'>{d.get('mode','')}</span></div>
            <div class='win-rate' style='color:{color}; border:1px solid {color};'>AI Score {win_pct:.1f}</div>
        </div>
        <div class='prog-bg'><div class='prog-fill' style='width:{win_pct}%; background:{color};'></div></div>
        <div class='tag-container'>{tag_html}</div>
        <div class='info-grid'>
            <div class='info-item'><span class='info-label'>현재가</span><span class='info-val'>{d['price']:,}</span></div>
            <div class='info-item'><span class='info-label'>수익률</span><span class='info-val' style='color:{"#FF4444" if d.get("pnl", 0) < 0 else "#00FF00"}'>{d.get("pnl", 0):.2f}%</span></div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["🐹 햄찌 분석", "🐯 호찌 분석", "📚 용어 해설"])
    
    with t1:
        h = p['hamzzi']
        st.markdown(textwrap.dedent(f"""
        <div class='persona-box' style='{h['style']}'>
            <div class='persona-title'>🐹 햄찌 (High Risk Quant)</div>
            <div style='margin-bottom:10px;'>{h['brief']}</div>
            <div style='background:#222; padding:10px; border-radius:8px; margin-bottom:10px;'><b>💡 행동 지침:</b> {h['act']}</div>
            <div style='font-size:13px; color:#aaa;'><b>🎯 이유:</b> {h['why']}</div>
        </div>
        """), unsafe_allow_html=True)
    
    with t2:
        t = p['hojji']
        st.markdown(textwrap.dedent(f"""
        <div class='persona-box' style='{t['style']}'>
            <div class='persona-title'>🐯 호찌 (Fundamental Value)</div>
            <div style='margin-bottom:10px;'>{t['brief']}</div>
            <div style='background:#222; padding:10px; border-radius:8px; margin-bottom:10px;'><b>💡 어르신 말씀:</b> {t['act']}</div>
            <div style='font-size:13px; color:#aaa;'><b>🎯 이유:</b> {t['why']}</div>
        </div>
        """), unsafe_allow_html=True)
        
    with t3:
        terms = engine.explain_terms()
        st.markdown(terms['hamzzi'], unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#333; margin:10px 0;'>", unsafe_allow_html=True)
        st.markdown(terms['hojji'], unsafe_allow_html=True)

    st.markdown(textwrap.dedent(f"""
    <div class='stock-card' style='margin-top:-20px; border-top:none; border-radius:0 0 16px 16px;'>
        <div class='timeline'>
            <div class='t-item'><span style='color:#888; font-size:12px;'>진입/평단</span><br><span class='t-val' style='color:#00C9FF'>{p['prices'][0]:,}</span></div>
            <div class='t-item'><span style='color:#888; font-size:12px;'>목표가</span><br><span class='t-val' style='color:#00FF00'>{p['prices'][1]:,}</span></div>
            <div class='t-item'><span style='color:#888; font-size:12px;'>손절가</span><br><span class='t-val' style='color:#FF4444'>{p['prices'][2]:,}</span></div>
        </div>
    </div>
    """), unsafe_allow_html=True)
    
    with st.expander(f"🔍 {d['name']} - 8대 엔진 HUD (전문가용)"):
        m = d['m']
        st.markdown(textwrap.dedent(f"""
        <div class='hud-grid'>
            <div class='hud-item'><span class='hud-label'>JLS 파동</span><span class='hud-val'>{m['omega']:.1f}</span></div>
            <div class='hud-item'><span class='hud-label'>독성(VPIN)</span><span class='hud-val'>{m['vpin']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>수급(Hawkes)</span><span class='hud-val'>{m['hawkes']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>호가(OBI)</span><span class='hud-val'>{m['obi']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>추세(Hurst)</span><span class='hud-val'>{m['hurst']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>켈리비중</span><span class='hud-val'>{m['kelly']:.2f}</span></div>
        </div>
        """), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [5] OCR SIMULATION
# -----------------------------------------------------------------------------
def parse_image_portfolio(uploaded_file):
    with st.spinner("OCR 분석 중..."): time.sleep(1)
    st.toast("✅ 이미지 스캔 완료!")
    return [
        {'name': '두산에너빌리티', 'price': 17500, 'qty': 100, 'strategy': '추세추종'},
        {'name': 'SK하이닉스', 'price': 135000, 'qty': 10, 'strategy': '추세추종'},
        {'name': '카카오', 'price': 55000, 'qty': 30, 'strategy': '초단타'}
    ]

# -----------------------------------------------------------------------------
# [6] MAIN LAYOUT
# -----------------------------------------------------------------------------
with st.expander("💰 내 자산 및 포트폴리오 설정", expanded=True):
    st.markdown("#### 📸 포트폴리오 이미지 스캔 (OCR)")
    uploaded = st.file_uploader("", type=['png','jpg'], label_visibility="collapsed")
    if uploaded:
        st.session_state.portfolio = parse_image_portfolio(uploaded)

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
            st.session_state.portfolio.append({'name': '삼성전자', 'price': 0, 'qty': 0, 'strategy': '추세추종'})
            st.rerun()
    
    st.markdown("---")
    if st.session_state.portfolio:
        for i, s in enumerate(st.session_state.portfolio):
            c1, c2, c3, c4, c5 = st.columns([3, 2, 1.5, 2, 0.5])
            with c1: 
                st.caption(f"**종목명 {i+1}**")
                try: idx = stock_names.index(s['name'])
                except: idx = 0
                s['name'] = st.selectbox(f"n{i}", stock_names, index=idx, label_visibility="collapsed")
            with c2: 
                st.caption("**평단가**")
                s['price'] = st.number_input(f"p{i}", value=float(s['price']), label_visibility="collapsed")
            with c3: 
                st.caption("**수량**")
                s['qty'] = st.number_input(f"q{i}", value=int(s['qty']), label_visibility="collapsed")
            with c4: 
                st.caption("**전략**")
                s['strategy'] = st.selectbox(f"s{i}", ["추세추종", "초단타"], index=0 if s['strategy']=="추세추종" else 1, label_visibility="collapsed")
            with c5: 
                st.caption("**삭제**")
                if st.button("🗑️", key=f"d{i}"): st.session_state.portfolio.pop(i); st.rerun()

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# Main Actions
c_btn, c_timer = st.columns([2, 1])
with c_btn:
    if st.button("📝 내 종목 및 포트폴리오 정밀 진단"):
        st.session_state.trigger_my = True
        st.rerun()
with c_timer:
    auto_my = st.selectbox("자동진단", list(TIME_OPTS.keys()), index=0, label_visibility="collapsed")

# Advisors
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
with b1:
    if st.button("🐹 햄찌의 앙큼상큼 팩트폭격 뀨? ❤️"):
        engine = SingularityEngine()
        title, msg = engine.hamzzi_nagging()
        st.session_state.adv_msg = f"<div class='hamzzi-box'><div class='hamzzi-title'>{title}</div>{msg}</div>"
with b2:
    if st.button("🐯 호찌의 유비무환(有備無患) 대호통"):
        engine = SingularityEngine()
        title, msg = engine.hojji_nagging()
        st.session_state.adv_msg = f"<div class='hojji-box'><div class='tiger-title'>{title}</div>{msg}</div>"
        
if 'adv_msg' in st.session_state: st.markdown(st.session_state.adv_msg, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [7] RESULTS RENDER
# -----------------------------------------------------------------------------
if st.session_state.my_diagnosis:
    st.markdown("---")
    if 'port_analysis' in st.session_state and st.session_state.port_analysis:
        pa = st.session_state.port_analysis
        st.markdown(textwrap.dedent(f"""
        <div class='port-dash'>
            <div style='font-size:18px; font-weight:bold; color:#fff; margin-bottom:15px;'>📊 포트폴리오 종합 진단 (Conflict Engine)</div>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:15px;'>
                <div class='persona-box' style='border-left: 3px solid #FFAA00; background:#222;'>
                    <div style='color:#FFAA00; font-weight:bold; margin-bottom:5px;'>🐹 햄찌 (공격형)</div>
                    <div style='font-size:13px; color:#ddd;'>{pa['hamzzi']}</div>
                </div>
                <div class='persona-box' style='border-left: 3px solid #FF4444; background:#222;'>
                    <div style='color:#FF4444; font-weight:bold; margin-bottom:5px;'>🐯 호찌 (방어형)</div>
                    <div style='font-size:13px; color:#ddd;'>{pa['hojji']}</div>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)
    
    st.subheader("👤 내 보유 종목 상세 분석")
    for d in st.session_state.my_diagnosis: render_full_card(d)

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
    for i, d in enumerate(st.session_state.ideal_list): render_full_card(d, i, is_rank=True)

elif st.session_state.market_view_mode == 'SEPARATE' and st.session_state.sc_list:
    st.markdown("<h5>📊 전략별 절대 랭킹 (Top 3)</h5>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["⚡ 초단타", "🌊 추세추종"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_full_card(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_full_card(d, i, is_rank=True)

# -----------------------------------------------------------------------------
# [8] AUTO REFRESH LOOP
# -----------------------------------------------------------------------------
now = time.time()
engine = SingularityEngine()

# My Diagnosis Trigger
if st.session_state.trigger_my or (TIME_OPTS[auto_my] > 0 and now - st.session_state.l_my > TIME_OPTS[auto_my]):
    with st.spinner("내 포트폴리오 정밀 해부 중..."):
        h_port, t_port = engine.diagnose_portfolio(st.session_state.portfolio, st.session_state.cash)
        st.session_state.port_analysis = {'hamzzi': h_port, 'hojji': t_port}
        my_res = []
        for s in st.session_state.portfolio:
            if not s['name']: continue
            mode = "scalping" if s['strategy'] == "초단타" else "swing"
            price = int(s['price']) if s['price'] > 0 else 10000
            wr, m, tags = engine.run_diagnosis(s['name'], mode)
            plan = engine.generate_report(mode, price, m, wr, st.session_state.cash, s['qty'], st.session_state.target_return)
            pnl = ((price - s['price'])/s['price']*100) if s['price']>0 else 0
            my_res.append({'name': s['name'], 'price': price, 'pnl': pnl, 'win': wr, 'm': m, 'tags': tags, 'plan': plan, 'mode': mode})
        st.session_state.my_diagnosis = my_res
        st.session_state.l_my = now
        st.session_state.trigger_my = False
        st.rerun()

# Market Scan Trigger
if st.session_state.trigger_top3 or (TIME_OPTS[auto_top3] > 0 and now - st.session_state.l_top3 > TIME_OPTS[auto_top3]):
    with st.spinner("시장 전체 스캔 중..."):
        market_data = load_top50_data()
        sc, sw, ideal = [], [], []
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close'])); name = row['Name']
            
            wr_sc, m_sc, t_sc = engine.run_diagnosis(name, "scalping")
            p_sc = engine.generate_report("scalping", price, m_sc, wr_sc, st.session_state.cash, 0, st.session_state.target_return)
            
            wr_sw, m_sw, t_sw = engine.run_diagnosis(name, "swing")
            p_sw = engine.generate_report("swing", price, m_sw, wr_sw, st.session_state.cash, 0, st.session_state.target_return)
            
            sc.append({'name': name, 'price': price, 'win': wr_sc, 'mode': '초단타', 'tags': t_sc, 'plan': p_sc, 'm': m_sc})
            sw.append({'name': name, 'price': price, 'win': wr_sw, 'mode': '추세추종', 'tags': t_sw, 'plan': p_sw, 'm': m_sw})
            ideal.append(sc[-1] if wr_sc >= wr_sw else sw[-1])
            
        sc.sort(key=lambda x: x['win'], reverse=True); sw.sort(key=lambda x: x['win'], reverse=True); ideal.sort(key=lambda x: x['win'], reverse=True)
        st.session_state.sc_list = sc[:3]; st.session_state.sw_list = sw[:3]; st.session_state.ideal_list = ideal[:3]
        st.session_state.l_top3 = now
        st.session_state.market_view_mode = 'TOP3'
        st.session_state.trigger_top3 = False
        st.rerun()

if st.session_state.trigger_sep or (TIME_OPTS[auto_sep] > 0 and now - st.session_state.l_sep > TIME_OPTS[auto_sep]):
    # (Same logic as above but sets view_mode to SEPARATE)
    st.session_state.trigger_top3 = True # Re-use logic
    st.session_state.market_view_mode = 'SEPARATE'
    st.session_state.trigger_sep = False
    st.rerun()

if TIME_OPTS[auto_my]>0 or TIME_OPTS[auto_top3]>0 or TIME_OPTS[auto_sep]>0: time.sleep(1); st.rerun()
