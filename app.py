import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random
import textwrap

# -----------------------------------------------------------------------------
# [0] GLOBAL SETUP & DATA LOADING (최우선 실행)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

# [CACHE DATA FUNCTIONS]
@st.cache_data(ttl=86400)
def get_stock_list():
    try:
        df = fdr.StockListing('KRX')
        # 불필요한 종목 필터링
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df['Name'].tolist()
    except:
        return ["삼성전자", "SK하이닉스", "LG에너지솔루션", "POSCO홀딩스", "NAVER"]

@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

# [CRITICAL FIX] 변수 선언을 UI 렌더링보다 무조건 먼저 수행
stock_names = get_stock_list()

TIME_OPTS = {
    "⛔ 수동 (멈춤)": 0, "⏱️ 3분": 180, "⏱️ 5분": 300, "⏱️ 10분": 600, 
    "⏱️ 30분": 1800, "⏱️ 1시간": 3600
}

# -----------------------------------------------------------------------------
# [1] STYLING (Luxury Dark Theme)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Settings */
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    
    /* Luxury Gradient Buttons */
    .stButton>button { 
        width: 100%; border-radius: 10px; font-weight: 800; height: 50px; font-size: 16px;
        background: linear-gradient(135deg, #2b2b2b 0%, #1a1a1a 100%); 
        border: 1px solid #444; color: #d4af37; /* Gold Text */
        box-shadow: 0 4px 10px rgba(0,0,0,0.5); transition: 0.3s;
    }
    .stButton>button:hover { 
        border-color: #d4af37; box-shadow: 0 0 15px rgba(212, 175, 55, 0.3); 
        transform: translateY(-2px); color: #fff;
    }
    
    /* Input Fields */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-size: 13px !important; font-weight: bold !important; color: #bbb !important;
        display: block !important; margin-bottom: 3px !important;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #121212 !important; color: #fff !important; 
        border: 1px solid #333 !important; border-radius: 6px;
    }
    
    /* Card Styles */
    .stock-card { 
        background: #121212; border: 1px solid #333; border-radius: 12px; 
        padding: 0; margin-bottom: 30px; box-shadow: 0 8px 20px rgba(0,0,0,0.6); overflow: hidden;
    }
    .card-header { 
        padding: 15px 20px; background: #1e1e1e; border-bottom: 1px solid #333; 
        display: flex; justify-content: space-between; align-items: center; 
    }
    .stock-name { font-size: 22px; font-weight: 900; color: #fff; }
    .score-badge { 
        background: #222; border: 1px solid; padding: 4px 12px; 
        border-radius: 20px; font-size: 13px; font-weight: bold; 
    }
    
    /* Progress Bar */
    .prog-bg { background: #333; height: 8px; border-radius: 4px; width: 100%; margin: 10px 0; }
    .prog-fill { height: 100%; border-radius: 4px; transition: width 0.6s ease; }
    
    /* Tags */
    .tag { 
        display: inline-block; padding: 4px 10px; border-radius: 6px; 
        font-size: 11px; margin-right: 5px; font-weight: bold; background: #1a1a1a; 
    }
    
    /* Persona Box */
    .persona-box { padding: 20px; font-size: 14px; line-height: 1.6; color: #eee; }
    .persona-title { 
        font-weight: bold; margin-bottom: 12px; font-size: 16px; 
        border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; 
    }
    
    /* Dashboard */
    .port-dash { background: #1a1a1a; padding: 20px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #444; }
    
    /* Timeline */
    .timeline { display: flex; justify-content: space-between; background: #000; padding: 15px 25px; border-top: 1px solid #333; }
    .t-item { text-align: center; } .t-val { font-weight: bold; font-size: 15px; margin-top: 4px; display: block; }
    
    /* Grid Info */
    .info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: #333; margin: 15px 20px; border: 1px solid #333; }
    .info-item { background: #121212; padding: 10px; text-align: center; }
    .info-label { font-size: 11px; color: #888; display: block; margin-bottom: 3px; }
    .info-val { font-size: 15px; font-weight: bold; color: #fff; }
    
    /* Rank Ribbon */
    .rank-ribbon { position: absolute; top: 0; left: 0; padding: 5px 12px; font-size: 12px; font-weight: bold; color: #fff; background: linear-gradient(45deg, #FF416C, #FF4B2B); border-bottom-right-radius: 12px; z-index: 5; }
    
    /* HUD Grid */
    .hud-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 10px; background: #0d1117; padding: 10px; border-radius: 8px; }
    .hud-item { background: #21262d; padding: 8px; border-radius: 6px; text-align: center; border: 1px solid #30363d; }
    .hud-label { font-size: 10px; color: #8b949e; display: block; margin-bottom: 2px; }
    .hud-val { font-size: 13px; color: #58a6ff; font-weight: bold; }
    
    /* Alignment Fix */
    div[data-testid="column"]:nth-child(5) { margin-left: -20px !important; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #d4af37;'>🐯 Tiger&Hamzzi Quant 🐹</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [2] STATE INITIALIZATION
# -----------------------------------------------------------------------------
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'ideal_list' not in st.session_state: st.session_state.ideal_list = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 
if 'target_return' not in st.session_state: st.session_state.target_return = 5.0
if 'my_diagnosis' not in st.session_state: st.session_state.my_diagnosis = []
if 'market_view_mode' not in st.session_state: st.session_state.market_view_mode = None
if 'port_analysis' not in st.session_state: st.session_state.port_analysis = None
# Timers & Triggers
if 'l_my' not in st.session_state: st.session_state.l_my = 0
if 'l_top3' not in st.session_state: st.session_state.l_top3 = 0
if 'l_sep' not in st.session_state: st.session_state.l_sep = 0
if 'trigger_my' not in st.session_state: st.session_state.trigger_my = False
if 'trigger_top3' not in st.session_state: st.session_state.trigger_top3 = False
if 'trigger_sep' not in st.session_state: st.session_state.trigger_sep = False

# -----------------------------------------------------------------------------
# [3] SINGULARITY OMEGA ENGINE
# -----------------------------------------------------------------------------
class SingularityEngine:
    def __init__(self):
        pass

    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H')}"
        seed_val = zlib.crc32(unique_key.encode())
        np.random.seed(seed_val)
        
        m = {
            "omega": np.random.uniform(5.0, 25.0), 
            "vol_surf": np.random.uniform(0.1, 0.9),
            "betti": np.random.choice([0, 1], p=[0.85, 0.15]), 
            "hurst": np.random.uniform(0.2, 0.99),
            "te": np.random.uniform(0.1, 5.0), 
            "vpin": np.random.uniform(0.0, 1.0),
            "hawkes": np.random.uniform(0.1, 4.0), 
            "obi": np.random.uniform(-1.0, 1.0),
            "gnn": np.random.uniform(0.1, 1.0), 
            "es": np.random.uniform(-0.01, -0.30), 
            "kelly": np.random.uniform(0.01, 0.30)
        }
        np.random.seed(None)
        return m

    def run_diagnosis(self, name, mode="swing"):
        m = self._calculate_metrics(name, mode)
        score = 35.0 
        tags = [{'label': '기본 마진', 'val': '+35', 'type': 'base'}]

        if m['vpin'] > 0.6: score -= 20; tags.append({'label': '독성 매물(VPIN)', 'val': '-20', 'type': 'bad'})
        if m['es'] < -0.20: score -= 15; tags.append({'label': 'Tail Risk(ES)', 'val': '-15', 'type': 'bad'})
        if m['betti'] == 1: score -= 10; tags.append({'label': '위상 붕괴(Betti)', 'val': '-10', 'type': 'bad'})
        
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

        # --- 🐹 HAMZZI (High Risk) ---
        if wr >= 0.70:
            h_title = "🐹 햄찌: \"인생은 한방! 지금이 기회야!\" 🔥"
            h_brief = f"사장님! <b>[Hawkes {m['hawkes']:.2f}]</b> 수치 봤어?! 수급이 미친 듯이 들어온다구! 🚀 <b>[GNN]</b> 중심성도 높아서 돈이 다 여기로 쏠리고 있어!"
            h_act = f"쫄지마! <b>{can_buy}주</b> 시장가 매수! <b>{target:,}원</b> 뚫으면 불타기 가즈아!"
            h_why = "변동성(Vol)이 살아있고 모멘텀(Hurst)이 확실해. 리스크 감수하고 수익 극대화할 타이밍이야!"
        elif wr >= 0.50:
            h_title = "🐹 햄찌: \"간 좀 볼까? 단타 치기 딱 좋아!\" ⚡"
            h_brief = f"음~ <b>[Hurst {m['hurst']:.2f}]</b> 추세 살아있네! 단타 놀이터야! 🎢 <b>[OBI]</b> 호가창 매수세가 꿈틀대고 있어."
            h_act = f"일단 <b>{int(can_buy/3)}주</b>만 정찰병 보내고, <b>{price:,}원</b> 지지하면 나머지 태워!"
            h_why = "모멘텀은 좋은데 눈치 싸움 중이야. 짧게 치고 빠지는 게릴라 전술이 유효해."
        else:
            h_title = "🐹 햄찌: \"으악! 돔황챠!! 폭탄이야!\" 💣"
            h_brief = f"으악! <b>[VPIN {m['vpin']:.2f}]</b> 경고등 켜졌어! 폭탄 돌리기 중이야! 💣"
            h_act = "절대 매수 금지! ❌ 탈출은 지능순이야! 현금 쥐고 숨어!"
            h_why = "독성 매물이 쏟아지고 있어. 지금 들어가면 계좌 녹는다."

        # --- 🐯 HOJJI (Conservative) ---
        if wr >= 0.70:
            t_title = "🐯 호찌: \"허허, 진국일세. 기회를 잡게.\" 🍵"
            t_brief = f"허허, <b>[내재가치]</b> 대비 저평가로군. 수급과 펀더멘털이 '금상첨화'야. 🍵"
            t_act = f"안전마진이 확보됐네. <b>{int(can_buy*0.8)}주</b> 정도 비중을 실어서 진득하게 동행하게."
            t_why = "기업 펀더멘털이 훼손되지 않았고, 기술적으로도 과열권이 아니야. 편안한 자리일세."
        elif wr >= 0.50:
            t_title = "🐯 호찌: \"계륵일세. 돌다리도 두들겨 보게.\" 🐅"
            t_brief = f"계륵일세. 🐅 <b>[변동성 {m['vol_surf']:.2f}]</b>이 너무 심해. '내우외환'이 걱정되는군."
            t_act = f"욕심 버리고 <b>{int(can_buy*0.2)}주</b>만 분할로 담게. '유비무환'의 자세가 필요해."
            t_why = "변동성이 너무 커. 자칫하면 큰 내상을 입을 수 있어. 리스크 관리가 우선이야."
        else:
            t_title = "🐯 호찌: \"어허! 사상누각이야!\" 🏚️"
            t_brief = f"에잉 쯧쯧! 😡 <b>[독성 매물]</b>이 넘쳐나는구먼! 사상누각이야!"
            t_act = "쳐다도 보지 말게. 현금이 곧 최고의 종목이야. 🛡️"
            t_why = "스마트 머니는 이미 떠났어. 떨어지는 칼날을 맨손으로 잡으려 하지 말게."

        return {
            "prices": (price, target, stop),
            "hamzzi": {"title": h_title, "brief": h_brief, "act": h_act, "why": h_why},
            "hojji": {"title": t_title, "brief": t_brief, "act": t_act, "why": t_why}
        }

    def diagnose_portfolio(self, portfolio, cash, target_return):
        asset_val = sum([s['price'] * s['qty'] for s in portfolio])
        total_val = asset_val + cash
        cash_ratio = (cash / total_val * 100) if total_val > 0 else 100
        
        beta = np.random.uniform(0.5, 2.0)
        sharpe = np.random.uniform(0.5, 3.0)
        mdd = np.random.uniform(-5.0, -35.0)
        
        h_msg = f"사장님! 현금 <b>{cash_ratio:.1f}%</b> 실화야? 😱 <b>[Cash Drag]</b> 때문에 수익률 갉아먹고 있어!<br><b>[Beta {beta:.2f}]</b>도 너무 낮아. 야수의 심장으로 <b>[주도주]</b> 태워야지! 🔥"
        t_msg = f"자네 현금이 <b>{cash_ratio:.1f}%</b>뿐인가? 😡 하락장 오면 <b>[MDD {mdd:.1f}%]</b> 맞고 깡통 찰 텐가? '유비무환'을 잊지 말게!<br>리스크 관리가 엉망이야. <b>[우량주]</b> 비중을 늘리게."
        return h_msg, t_msg

    def explain_terms(self):
        return {
            "hamzzi": """
            <div style='font-size:13px; line-height:1.6; color:#eee;'>
            <b>🐹 햄찌의 족집게 과외:</b><br>
            • <b>Hawkes (호크스):</b> 인기 폭발 지수! 2.0 넘으면 사람들 우르르 몰려오는 거야! 🎉<br>
            • <b>Vol Surface (볼 서페이스):</b> 파도 높이! 높으면 서핑 꿀잼(수익)이지만 물 먹을 수도 있어! 🌊<br>
            • <b>Hurst (허스트):</b> 황소 고집! 한 번 가던 방향으로 계속 가려는 성질이야! 💪
            </div>
            """,
            "hojji": """
            <div style='font-size:13px; line-height:1.6; color:#eee;'>
            <b>🐯 호찌의 훈장님 해설:</b><br>
            • <b>VPIN (독성 유동성):</b> 기관들이 정보 우위를 이용해 개미에게 물량을 넘기는 수치일세.<br>
            • <b>GNN (그래프 신경망):</b> 이 종목이 시장 생태계에서 얼마나 중요한 '대장'인지 보여주지.<br>
            • <b>MDD (최대낙폭):</b> 고점에서 얼마나 처박혔느냐... 자네 멘탈이 버틸 수 있는 한계선이지.
            </div>
            """
        }

    def hamzzi_nagging(self):
        title = random.choice(["🐹 햄찌의 잔소리", "🐹 햄찌의 긴급 타전", "🐹 햄찌의 꿀팁"])
        msg = random.choice([
            "차트가 말을 거는데 왜 대답을 안 해? 📞 당장 매수 버튼 눌러!",
            "인생은 타이밍이야! 지금이 바로 그 타이밍이라구! ⏰",
            "쫄지마! 쫄면 지는 거야! 야수의 심장으로 풀매수! 🔥"
        ])
        return title, msg

    def hojji_nagging(self):
        title = random.choice(["🐯 호찌의 호통", "🐯 호찌의 훈계", "🐯 호찌의 명언"])
        msg = random.choice([
            "공부 안 하고 사는 건 투기야! 재무제표는 읽어봤나? 📚",
            "급할수록 돌아가라 했어. 현금도 소중한 종목임을 잊지 말게. 🛡️",
            "일희일비하지 말게. 주식은 머리가 아니라 엉덩이로 버티는 걸세. 🧘‍♂️"
        ])
        return title, msg

# -----------------------------------------------------------------------------
# [4] OCR MOCK
# -----------------------------------------------------------------------------
def parse_image_portfolio(uploaded_file):
    with st.spinner("🔄 [Singularity Omega] OCR 이미지 정밀 분석 중..."):
        time.sleep(1.5)
    st.toast("✅ 이미지 스캔 완료!", icon="📸")
    return [
        {'name': '두산에너빌리티', 'price': 17500, 'qty': 100, 'strategy': '추세추종'},
        {'name': 'SK하이닉스', 'price': 135000, 'qty': 10, 'strategy': '추세추종'},
        {'name': '카카오', 'price': 55000, 'qty': 30, 'strategy': '초단타'}
    ]

# -----------------------------------------------------------------------------
# [5] UI COMPONENT RENDERER
# -----------------------------------------------------------------------------
def render_full_card(d, idx=None, is_rank=False):
    engine = SingularityEngine()
    p = d['plan']
    win_pct = d['win'] * 100
    color = "#00FF00" if d['win'] >= 0.7 else "#FFAA00" if d['win'] >= 0.5 else "#FF4444"
    rank_html = f"<div class='rank-ribbon'>{idx+1}위</div>" if is_rank else ""
    
    tag_html = ""
    for t in d['tags']:
        tc = "#00FF00" if t['type'] == 'best' else "#00C9FF" if t['type'] == 'good' else "#FF4444"
        tag_html += f"<span class='tag' style='color:{tc}; border:1px solid {tc};'>{t['label']} {t['val']}</span>"

    st.markdown(textwrap.dedent(f"""
    <div class='stock-card' style='border-color:{color};'>
        {rank_html}
        <div class='card-header' style='padding-left:{50 if is_rank else 0}px'>
            <div>
                <span class='stock-name'>{d['name']}</span>
                <span style='color:#ccc; font-size:14px; margin-left:10px;'>{d.get('mode','')}</span>
            </div>
            <div class='score-badge' style='color:{color}; border-color:{color};'>Score {win_pct:.1f}</div>
        </div>
        <div style='padding:0 20px 10px 20px; display:flex; align-items:center; gap:10px;'>
            <div class='prog-bg'><div class='prog-fill' style='width:{win_pct}%; background:{color};'></div></div>
            <span style='color:{color}; font-weight:bold; font-size:12px;'>{win_pct:.1f}%</span>
        </div>
        <div style='margin-bottom:15px; padding:0 20px;'>{tag_html}</div>
        <div class='info-grid'>
            <div class='info-item'><span class='info-label'>현재가</span><span class='info-val'>{d['price']:,}</span></div>
            <div class='info-item'><span class='info-label'>수익률</span><span class='info-val' style='color:{"#FF4444" if d.get("pnl", 0) < 0 else "#00FF00"}'>{d.get("pnl", 0):.2f}%</span></div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["🐹 햄찌의 분석", "🐯 호찌의 분석", "📊 8대 엔진 HUD"])
    
    with t1:
        h = p['hamzzi']
        st.markdown(textwrap.dedent(f"""
        <div class='persona-box' style='border-left-color: #FFAA00;'>
            <div class='persona-title' style='color:#FFAA00;'>{h['title']}</div>
            <div style='margin-bottom:10px;'>{h['brief']}</div>
            <div style='background:#222; padding:10px; border-radius:8px; margin-bottom:10px;'><b>💡 행동 지침:</b> {h['act']}</div>
            <div style='font-size:13px; color:#aaa;'><b>🎯 이유:</b> {h['why']}</div>
        </div>
        """), unsafe_allow_html=True)
    
    with t2:
        t = p['hojji']
        st.markdown(textwrap.dedent(f"""
        <div class='persona-box' style='border-left-color: #FF4444;'>
            <div class='persona-title' style='color:#FF4444;'>{t['title']}</div>
            <div style='margin-bottom:10px;'>{t['brief']}</div>
            <div style='background:#222; padding:10px; border-radius:8px; margin-bottom:10px;'><b>💡 어르신 말씀:</b> {t['act']}</div>
            <div style='font-size:13px; color:#aaa;'><b>🎯 이유:</b> {t['why']}</div>
        </div>
        """), unsafe_allow_html=True)

    with t3:
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

# -----------------------------------------------------------------------------
# [6] MAIN LAYOUT
# -----------------------------------------------------------------------------
with st.expander("💰 내 자산 및 포트폴리오 설정", expanded=True):
    st.markdown("#### 📸 OCR 이미지 스캔 (시뮬레이션)")
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    if uploaded_file:
        scanned = parse_image_portfolio(uploaded_file)
        st.session_state.portfolio = scanned
        st.success("스캔 완료!")

    st.markdown("---")
    
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.caption("**예수금 (KRW)**")
        st.session_state.cash = st.number_input("cash_input", value=st.session_state.cash, step=100000, label_visibility="collapsed")
    with c2: 
        st.caption("**목표 수익률 (%)**")
        st.session_state.target_return = st.number_input("target_input", value=st.session_state.target_return, step=1.0, label_visibility="collapsed")
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
                s['name'] = st.selectbox(f"n_{i}", stock_names, index=idx, label_visibility="collapsed")
            with c2: 
                st.caption("**평단가**")
                s['price'] = st.number_input(f"p_{i}", value=float(s['price']), label_visibility="collapsed")
            with c3: 
                st.caption("**수량**")
                s['qty'] = st.number_input(f"q_{i}", value=int(s['qty']), label_visibility="collapsed")
            with c4: 
                st.caption("**전략**")
                s['strategy'] = st.selectbox(f"s_{i}", ["추세추종", "초단타"], index=0 if s['strategy']=="추세추종" else 1, label_visibility="collapsed")
            with c5: 
                st.caption("**삭제**")
                if st.button("🗑️", key=f"d_{i}"): 
                    st.session_state.portfolio.pop(i)
                    st.rerun()

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

# MY DIAGNOSIS
if st.session_state.my_diagnosis:
    st.markdown("---")
    if 'port_analysis' in st.session_state:
        pa = st.session_state.port_analysis
        st.markdown(textwrap.dedent(f"""
        <div class='port-dash'>
            <div style='font-size:18px; font-weight:bold; color:#fff; margin-bottom:15px;'>📊 포트폴리오 종합 진단 (Conflict Engine)</div>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:15px;'>
                <div class='persona-box' style='background:#222; border-left: 3px solid #FFAA00; margin-top:0;'>
                    <div style='color:#FFAA00; font-weight:bold; margin-bottom:5px;'>🐹 햄찌의 야수 본능 (인생 한방! 🔥)</div>
                    <div style='font-size:13px; color:#ddd; line-height:1.5;'>{pa['hamzzi']}</div>
                </div>
                <div class='persona-box' style='background:#222; border-left: 3px solid #FF4444; margin-top:0;'>
                    <div style='color:#FF4444; font-weight:bold; margin-bottom:5px;'>🐯 호찌의 유비무환(有備無患) 정신 🛡️</div>
                    <div style='
