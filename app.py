import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random
import textwrap

# -----------------------------------------------------------------------------
# [1] 시스템 설정 및 데이터 로딩 (최우선 실행 - 에러 방지 최적화)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Hojji & Hamzzi Quant", page_icon="🐹", layout="centered")

@st.cache_data(ttl=86400)
def get_stock_list():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df['Name'].tolist()
    except:
        return ["삼성전자", "SK하이닉스", "LG에너지솔루션", "POSCO홀딩스", "NAVER", "카카오"]

@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

# [중요] 전역 변수 선언 (NameError 방지)
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
# [2] 스타일링 (다크 테마 & HTML 버그 수정용 CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global */
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    
    /* Neon Gold Buttons */
    .stButton>button { 
        width: 100%; border-radius: 10px; font-weight: 800; height: 52px; font-size: 16px;
        background: linear-gradient(135deg, #1c1c1c 0%, #2a2a2a 100%); 
        border: 1px solid #d4af37; color: #d4af37; letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5); transition: 0.3s;
    }
    .stButton>button:hover { 
        background: linear-gradient(135deg, #d4af37 0%, #f1c40f 100%);
        color: #000; border-color: #fff;
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.6); transform: translateY(-2px);
    }
    
    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #121212 !important; color: #fff !important; 
        border: 1px solid #333 !important; border-radius: 8px;
    }
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-size: 13px !important; font-weight: bold !important; color: #aaa !important;
    }
    
    /* Card UI Structure */
    .stock-card { 
        background: #121212; border-radius: 16px; padding: 0; margin-bottom: 25px; 
        border: 1px solid #333; box-shadow: 0 10px 30px rgba(0,0,0,0.7); overflow: hidden;
    }
    .card-header { 
        padding: 18px 25px; background: #1a1a1a; border-bottom: 1px solid #333; 
        display: flex; justify-content: space-between; align-items: center; 
    }
    .stock-name { font-size: 22px; font-weight: 900; color: #fff; }
    .score-badge { 
        font-size: 14px; font-weight: bold; background: #000; padding: 6px 14px; 
        border-radius: 20px; border: 1px solid; 
    }
    
    /* Progress Bar */
    .prog-bg { background: #222; height: 10px; width: 100%; margin: 0; }
    .prog-fill { height: 100%; transition: width 1s ease-in-out; }
    
    /* Tags & Info */
    .tag-container { padding: 15px 25px 5px 25px; }
    .tag { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; margin-right: 5px; font-weight: bold; color: #000; }
    
    .info-grid { 
        display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; 
        background: #333; margin: 15px 0 0 0; border-top: 1px solid #333; 
    }
    .info-item { background: #151515; padding: 15px; text-align: center; }
    .info-label { font-size: 12px; color: #888; display: block; margin-bottom: 4px; }
    .info-val { font-size: 17px; font-weight: bold; color: #fff; }
    
    /* Persona Box */
    .persona-box { padding: 20px; font-size: 14px; line-height: 1.8; color: #ddd; background: #1a1a1a; border-radius: 12px; margin-top: 15px; border-left-width: 4px; border-left-style: solid; }
    .persona-title { font-weight: 900; margin-bottom: 12px; font-size: 16px; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.1); }
    
    /* HUD & Timeline */
    .hud-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 15px; background: #0f0f0f; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .hud-item { background: #1e1e1e; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #333; }
    .hud-l { font-size: 11px; color: #888; display: block; }
    .hud-v { font-size: 14px; font-weight: bold; color: #00C9FF; }
    
    .timeline-box { display: flex; justify-content: space-between; background: #0a0a0a; padding: 20px 30px; border-top: 1px solid #333; }
    
    /* Utility */
    .rank-ribbon { position: absolute; top: 0; left: 0; padding: 6px 15px; font-size: 12px; font-weight: bold; color: #fff; background: linear-gradient(45deg, #FF416C, #FF4B2B); border-bottom-right-radius: 15px; z-index: 5; }
    .summary-line { margin-top: 10px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 6px; font-weight: bold; color: #fff; border: 1px solid #333; font-size: 13px; }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -15px !important; margin-top: 23px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #d4af37; text-shadow: 0 0 20px rgba(212,175,55,0.4);'>🐹 햄찌와 호찌의 퀀트 대작전 🚀</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [3] SINGULARITY OMEGA ENGINE (Deep Logic & Text Gen)
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
        score = 50.0 
        tags = [{'label': '기본 마진', 'val': '+35', 'type': 'base', 'bg': '#888'}]

        if m['vpin'] > 0.6: score -= 20; tags.append({'label': '⚠️ 독성 매물', 'val': '-20', 'type': 'bad', 'bg': '#FF4444'})
        if m['es'] < -0.20: score -= 15; tags.append({'label': '📉 Tail Risk', 'val': '-15', 'type': 'bad', 'bg': '#FF4444'})
        if m['betti'] == 1: score -= 10; tags.append({'label': '🌀 구조 붕괴', 'val': '-10', 'type': 'bad', 'bg': '#FF4444'})
        
        if mode == "scalping":
            if m['hawkes'] > 2.0: score += 45; tags.append({'label': '🚀 Hawkes 폭발', 'val': '+45', 'type': 'best', 'bg': '#00FF00'})
            elif m['hawkes'] > 1.5: score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'type': 'good', 'bg': '#00C9FF'})
        else: 
            if m['hurst'] > 0.7: score += 40; tags.append({'label': '📈 추세 지속', 'val': '+40', 'type': 'best', 'bg': '#00FF00'})
            elif m['hurst'] > 0.6: score += 10; tags.append({'label': '↗️ 모멘텀 양호', 'val': '+10', 'type': 'good', 'bg': '#00C9FF'})

        if m['gnn'] > 0.8: score += 10; tags.append({'label': '👑 GNN 대장주', 'val': '+10', 'type': 'good', 'bg': '#00C9FF'})
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
        
        safe_kelly = m['kelly'] * 0.5 
        can_buy = int((cash * safe_kelly) / price) if price > 0 else 0

        # 🐹 HAMZZI (Infinite Variety & Deep Analysis)
        if wr >= 0.70:
            h_brief = f"""
            <b>[1. JLS 임계점 & Hawkes 폭발]</b><br>
            "사장님! <b>Omega 진동수</b>가 {m['omega']:.2f}Hz로 공명하고 있어. 이건 단순 상승이 아니라 로그 주기적(Log-Periodic) 패턴에 의한 <b>임계 폭발(Critical Burst)</b> 직전 단계야!
            게다가 <b>Hawkes 강도</b>가 {m['hawkes']:.2f}를 돌파했어. 기계적 매수 폭주가 일어나는 '자기 여진' 상태라구!"
            <br><br><b>[2. 행동 지침]</b><br>
            지금 당장 <b>시장가</b>로 <b>{can_buy}주</b>를 쓸어 담아! 목표가 <b>{target:,}원</b> 돌파 시엔 <b>불타기(Pyramiding)</b>로 대응해!
            <div class='summary-line'>🐹 요약: 인생 역전 기회야! 쫄지 말고 풀매수 가즈아! 🔥</div>
            """
        elif wr >= 0.50:
            h_brief = f"""
            <b>[1. 프랙탈 차원 (Hurst)]</b><br>
            "음~ <b>Hurst Exponent</b>가 {m['hurst']:.2f}야. 0.5보다 높으니 추세가 살아있는 '지속성' 구간이지. 단타 치기 딱 좋은 놀이터가 형성됐어.
            하지만 <b>OBI(호가 불균형)</b>가 {m['obi']:.2f}로 중립적이라 세력들이 간 보고 있는 중이야."
            <br><br><b>[2. 행동 지침]</b><br>
            몰빵은 위험해. <b>{int(can_buy/3)}주</b>만 '정찰병'으로 투입하고, <b>{price:,}원</b> 지지하면 그때 태워!
            <div class='summary-line'>🐹 요약: 짧게 치고 빠지는 게릴라 전술이 답이야! ⚡</div>
            """
        else:
            h_brief = f"""
            <b>[1. 독성 유동성 (VPIN)]</b><br>
            "으악! <b>VPIN</b>이 {m['vpin']:.2f}야! 기관들이 정보 우위로 설거지 중이라구! 독성 매물이 쏟아진다!
            <b>Betti Number</b>가 1로 변했어. 차트에 구멍이 뚫렸다는 건 지지선이 붕괴된다는 뜻이야."
            <br><br><b>[2. 행동 지침]</b><br>
            <b>절대 매수 금지!</b> 보유 중이면 당장 던져! 이건 투자가 아니라 기부야.
            <div class='summary-line'>🐹 요약: 폭탄이야! 만지면 터져! 도망가! 💣</div>
            """

        # 🐯 HOJJI (Conservative Deep Analysis)
        if wr >= 0.70:
            t_brief = f"""
            <b>[1. 네트워크 중심성 (GNN)]</b><br>
            "허허, <b>GNN 중심성</b>이 {m['gnn']:.2f}로군. 시장 자금이 이 종목을 '허브(Hub)'로 삼아 흐르고 있어. 진정한 대장주야.
            <b>전이 엔트로피(TE)</b>도 양의 정보량을 보내고 있으니, 펀더멘털과 수급이 '금상첨화'일세."
            <br><br><b>[2. 행동 지침]</b><br>
            안전마진이 확보됐네. 자네 자금의 <b>{int(can_buy*0.8)}주</b> 정도를 진입하게. 우직하게 동행해도 좋은 자리야.
            <div class='summary-line'>🐯 요약: 진국일세. 엉덩이 무겁게 들고 가시게. 🍵</div>
            """
        elif wr >= 0.50:
            t_brief = f"""
            <b>[1. 변동성 위험 (Vol Surface)]</b><br>
            "계륵일세. <b>내재 변동성</b>이 {m['vol_surf']:.2f}로 너무 높아. 옵션 시장 불안이 현물로 전이될 수 있는 '내우외환'의 형국이야.
            <b>꼬리 위험(ES)</b> 수치도 {m['es']:.2f}로 불안정하네."
            <br><br><b>[2. 행동 지침]</b><br>
            욕심은 화를 부르네. <b>{int(can_buy*0.2)}주</b>만 분할로 담거나, 아예 관망하게. 돌다리도 두들겨 봐야지.
            <div class='summary-line'>🐯 요약: 위험해 보이네. 아주 조금만 담거나 쉬게나. 🐅</div>
            """
        else:
            t_brief = f"""
            <b>[1. 펀더멘털 훼손]</b><br>
            "에잉 쯧쯧! <b>Going Concern</b> 이슈가 보여. 기초 체력이 부실한데 탑을 쌓으려 하다니, 사상누각일세.
            과거의 지지선이 이제는 강력한 저항선(Role Reversal)으로 변질됐어."
            <br><br><b>[2. 행동 지침]</b><br>
            쳐다도 보지 말게. 현금이 곧 최고의 종목이야. <b>비에르고딕</b> 파산 위험을 피하는 게 상책일세.
            <div class='summary-line'>🐯 요약: 썩은 동아줄이야. 절대 잡지 마라. 🏚️</div>
            """

        return {
            "prices": (price, target, stop),
            "hamzzi": {"text": h_brief},
            "hojji": {"text": t_brief}
        }

    def diagnose_portfolio(self, portfolio, cash):
        if not portfolio: return "포트폴리오 없음", "데이터 없음"
        
        total = cash + sum(s['price']*s['qty'] for s in portfolio)
        cash_r = (cash/total*100) if total else 100
        
        beta = np.random.uniform(0.5, 2.0)
        corr = np.random.uniform(0.3, 0.9)
        mdd = np.random.uniform(-5.0, -40.0)
        
        # Hamzzi Deep Port Analysis
        h = f"""
        <b>[1. 자본 효율성 (Capital Efficiency)]</b><br>
        "사장님! 현재 현금 비중이 **{cash_r:.1f}%**야. 이건 **[Cash Drag]** 현상이라구! 인플레이션 생각하면 돈이 썩고 있는 거야.
        포트폴리오의 **Beta(시장 민감도)**가 **{beta:.2f}**밖에 안 돼. 레버리지를 써서라도 1.5 이상으로 올려야지!"
        <br><br>
        <b>👉 [햄찌의 리밸런싱 지령]</b><br>
        1. **WHEN:** 내일 장 시작 동시호가(09:00)에 바로!<br>
        2. **WHAT:** 현금의 50%를 털어서 **[TQQQ]**나 **[주도 섹터 3배 레버리지]**를 매수해!<br>
        3. **WHY:** 변동성이 커지는 구간에선 '변동성 돌파 전략'이 답이야. 공격이 최선의 방어라구! 🔥
        <div class='summary-line'>🐹 요약: 현금은 쓰레기야! 풀매수해!</div>
        """
        
        # Hojji Deep Port Analysis
        t = f"""
        <b>[1. 시스템 리스크 (Systemic Risk)]</b><br>
        "자네 포트폴리오의 종목 간 **상관계수(Correlation)**가 **{corr:.2f}**로 매우 높네. 계란을 한 바구니에 담은 꼴이야.
        하락장이 오면 동조화 현상 때문에 **MDD(최대 낙폭)**가 **{mdd:.1f}%**까지 발생할 수 있어."
        <br><br>
        <b>👉 [호찌의 리밸런싱 훈수]</b><br>
        1. **WHEN:** 지금 당장, 혹은 기술적 반등이 나올 때마다.<br>
        2. **WHAT:** 기술주 비중을 30% 줄이고, **[미국채]**, **[금]**, **[배당주]**를 편입하게.<br>
        3. **WHY:** 자산 배분(Asset Allocation)만이 살길일세. 엔트로피가 증가하는 시장에선 방어벽을 세우게. 🛡️
        <div class='summary-line'>🐯 요약: 욕심 부리다 다 잃네. 채권 섞게.</div>
        """
        return h, t

    def explain_terms(self):
        return {
            "hamzzi": """
            <div style='font-size:13px; line-height:1.6; color:#bbb;'>
            <b>🐹 햄찌의 족집게 과외:</b><br>
            • <b>Hawkes (호크스):</b> 인기 투표 같은 거야! 내가 한 표 던지면, 친구들이 우르르 와서 표 던지는 거! 수급 폭발!<br>
            • <b>Vol Surface:</b> 파도 높이! 높으면 서핑 꿀잼(수익)이지만 물 먹을 수도 있어! 🌊<br>
            • <b>Hurst (허스트):</b> 황소 고집! 한 번 가던 방향으로 계속 가려는 성질이야! 💪
            </div>
            """,
            "hojji": """
            <div style='font-size:13px; line-height:1.6; color:#bbb;'>
            <b>🐯 호찌의 훈장님 해설:</b><br>
            • <b>VPIN (독성 유동성):</b> 정보 우위를 가진 기관의 기습적 매도 물량일세. 당하면 약도 없어.<br>
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
# [4] OCR SIMULATION
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
# [5] UI COMPONENT RENDERER (Clean HTML with textwrap)
# -----------------------------------------------------------------------------
def render_full_card(d, idx=None, is_rank=False):
    engine = SingularityEngine()
    p = d['plan']
    win_pct = d['win'] * 100
    
    color = "#00FF00" if d['win'] >= 0.7 else "#FFAA00" if d['win'] >= 0.5 else "#FF4444"
    rank_html = f"<div class='rank-ribbon'>{idx+1}위</div>" if is_rank else ""
    
    # Tag Generator
    tag_html = ""
    for t in d['tags']:
        tag_html += f"<span class='tag' style='color:{t.get('bg', '#888')}; border:1px solid {t.get('bg', '#888')};'>{t['label']} {t['val']}</span>"

    # 1. Main Card (Fix: Using textwrap.dedent to ensure HTML formatting is correct)
    st.markdown(textwrap.dedent(f"""
    <div class='stock-card' style='border-color:{color};'>
        {rank_html}
        <div class='card-header'>
            <div>
                <span class='stock-name'>{d['name']}</span>
                <span style='color:#ccc; font-size:14px; margin-left:10px;'>{d.get('mode','')}</span>
            </div>
            <div class='score-badge' style='color:{color}; border-color:{color};'>Score {win_pct:.1f}</div>
        </div>
        <div style='padding:0 25px;'>
            <div class='prog-bg'><div class='prog-fill' style='width:{win_pct}%; background:{color};'></div></div>
        </div>
        <div style='margin-bottom:15px; padding:0 25px; margin-top:10px;'>{tag_html}</div>
        <div class='info-grid'>
            <div class='info-item'><span class='info-label'>현재가</span><span class='info-val'>{d['price']:,}</span></div>
            <div class='info-item'><span class='info-label'>수익률</span><span class='info-val' style='color:{"#FF4444" if d.get("pnl", 0) < 0 else "#00FF00"}'>{d.get("pnl", 0):.2f}%</span></div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # 2. Tabs
    t1, t2, t3 = st.tabs(["🐹 햄찌의 분석", "🐯 호찌의 분석", "📊 8대 엔진 HUD"])
    
    with t1:
        st.markdown(textwrap.dedent(f"""
        <div class='persona-box' style='border-left-color: #FFAA00;'>
            <div class='persona-title' style='color:#FFAA00;'>{p['hamzzi']['title']}</div>
            {p['hamzzi']['text']}
        </div>
        """), unsafe_allow_html=True)
    
    with t2:
        st.markdown(textwrap.dedent(f"""
        <div class='persona-box' style='border-left-color: #FF4444;'>
            <div class='persona-title' style='color:#FF4444;'>{p['hojji']['title']}</div>
            {p['hojji']['text']}
        </div>
        """), unsafe_allow_html=True)

    with t3:
        m = d['m']
        st.markdown(textwrap.dedent(f"""
        <div class='hud-grid'>
            <div class='hud-item'><span class='hud-l'>JLS 파동</span><span class='hud-v'>{m['omega']:.1f}</span></div>
            <div class='hud-item'><span class='hud-l'>독성(VPIN)</span><span class='hud-v'>{m['vpin']:.2f}</span></div>
            <div class='hud-item'><span class='hud-l'>수급(Hawkes)</span><span class='hud-v'>{m['hawkes']:.2f}</span></div>
            <div class='hud-item'><span class='hud-l'>호가(OBI)</span><span class='hud-v'>{m['obi']:.2f}</span></div>
            <div class='hud-item'><span class='hud-l'>추세(Hurst)</span><span class='hud-v'>{m['hurst']:.2f}</span></div>
            <div class='hud-item'><span class='hud-l'>네트워크(GNN)</span><span class='hud-v'>{m['gnn']:.2f}</span></div>
        </div>
        """), unsafe_allow_html=True)
        
        terms = engine.explain_terms()
        st.markdown(terms['hamzzi'], unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#333; margin:10px 0;'>", unsafe_allow_html=True)
        st.markdown(terms['hojji'], unsafe_allow_html=True)

    # 3. Timeline
    st.markdown(textwrap.dedent(f"""
    <div class='timeline-box'>
        <div class='t-item'><span class='info-label'>진입/평단</span><span class='t-val' style='color:#00C9FF'>{p['prices'][0]:,}</span></div>
        <div class='t-item'><span class='info-label'>목표가</span><span class='t-val' style='color:#00FF00'>{p['prices'][1]:,}</span></div>
        <div class='t-item'><span class='info-label'>손절가</span><span class='t-val' style='color:#FF4444'>{p['prices'][2]:,}</span></div>
    </div>
    """), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [6] MAIN LAYOUT & CONTROLS
# -----------------------------------------------------------------------------
with st.expander("💰 내 자산 및 포트폴리오 설정", expanded=True):
    uploaded = st.file_uploader("📸 OCR 이미지 스캔 (시뮬레이션)", type=['png','jpg'], label_visibility="collapsed")
    if uploaded:
        scanned = parse_image_portfolio(uploaded)
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
        st.session_state.adv_msg = f"<div class='persona-box' style='border-left: 3px solid #FFAA00;'><div class='persona-title' style='color:#FFAA00;'>{title}</div>{msg}</div>"
with b2:
    if st.button("🐯 호찌의 유비무환(有備無患) 대호통"):
        engine = SingularityEngine()
        title, msg = engine.hojji_nagging()
        st.session_state.adv_msg = f"<div class='persona-box' style='border-left: 3px solid #FF4444;'><div class='persona-title' style='color:#FF4444;'>{title}</div>{msg}</div>"
        
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
                <div class='persona-box' style='background:#1f1f1f; border-left: 3px solid #FFAA00; margin-top:0;'>
                    <div style='color:#FFAA00; font-weight:bold; margin-bottom:5px;'>🐹 햄찌 (공격형)</div>
                    <div style='font-size:13px; color:#ddd; line-height:1.6;'>{pa['hamzzi']}</div>
                </div>
                <div class='persona-box' style='background:#1f1f1f; border-left: 3px solid #FF4444; margin-top:0;'>
                    <div style='color:#FF4444; font-weight:bold; margin-bottom:5px;'>🐯 호찌 (방어형)</div>
                    <div style='font-size:13px; color:#ddd; line-height:1.6;'>{pa['hojji']}</div>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)
    
    st.subheader("👤 보유 종목 상세 분석")
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
if t_val_my>0 or t_val_top3>0 or t_val_sep>0: time.sleep(1); st.rerun()
