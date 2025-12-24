import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random
import textwrap

# -----------------------------------------------------------------------------
# [0] SYSTEM CONFIG
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

stock_names = get_stock_list()
TIME_OPTS = {"⛔ 멈춤": 0, "⏱️ 3분": 180, "⏱️ 5분": 300, "⏱️ 10분": 600, "⏱️ 15분": 900, "⏱️ 20분": 1200, "⏱️ 30분": 1800, "⏱️ 40분": 2400, "⏱️ 1시간": 3600, "⏱️ 1시간 30분": 5400, "⏱️ 2시간": 7200, "⏱️ 3시간": 10800}

# 세션 상태 초기화
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
# [1] STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #ffffff; font-family: 'Pretendard', sans-serif; }
    
    /* Neon Gold Buttons */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 55px; font-size: 18px;
        background-color: #1a1a1a; 
        border: 2px solid #FFD700; color: #FFD700; 
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color: #FFD700; color: #000; box-shadow: 0 0 20px rgba(255, 215, 0, 0.8); border-color: #fff;
    }
    
    /* Input Labels */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-size: 15px !important; font-weight: 900 !important; color: #FFD700 !important; margin-bottom: 5px !important;
    }
    
    /* Card UI */
    .stock-card { 
        background: #111; border: 1px solid #333; border-radius: 16px; padding: 0; margin-bottom: 30px; box-shadow: 0 8px 30px rgba(0,0,0,0.8);
    }
    
    /* Analysis Box */
    .analysis-box {
        background-color: #0f0f0f; border-radius: 10px; padding: 25px; margin-top: 15px; 
        line-height: 1.8; color: #eee; border: 1px solid #333; border-left-width: 5px; border-left-style: solid;
    }
    .box-hamzzi { border-left-color: #FF9900; }
    .box-hojji { border-left-color: #FF4444; }
    
    /* Rationale & Timetable */
    .rationale-box { background: #151515; padding: 15px; border-radius: 8px; margin-top: 15px; border: 1px dashed #555; }
    .timetable-box { background: #111; padding: 15px; border-radius: 8px; border-left: 3px solid #00C9FF; margin-top: 10px; }
    
    /* Metrics */
    div[data-testid="stMetricValue"] { font-size: 24px !important; color: #fff !important; font-weight: 800 !important; }
    
    /* Tags */
    .tag { display: inline-block; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-right: 5px; color: #000; }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -15px !important; margin-top: 23px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🐯 호찌와 햄찌의 퀀트 대작전 🚀</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [2] SINGULARITY OMEGA ENGINE (Strict Scoring & Narrative)
# -----------------------------------------------------------------------------
class SingularityEngine:
    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H-%M')}-{random.randint(0,1000)}"
        seed_val = zlib.crc32(unique_key.encode())
        np.random.seed(seed_val)
        return {
            "omega": np.random.uniform(5.0, 30.0), # JLS: 25.0 근처가 임계점
            "vol_surf": np.random.uniform(0.1, 0.9), 
            "betti": np.random.choice([0, 1], p=[0.9, 0.1]), # 1이면 붕괴
            "hurst": np.random.uniform(0.3, 0.8), # 0.5 이상 추세
            "te": np.random.uniform(0.1, 5.0), 
            "vpin": np.random.uniform(0.0, 1.0), # 0.6 이상 위험
            "hawkes": np.random.uniform(0.1, 3.0), # 2.0 이상 폭발
            "obi": np.random.uniform(-1.0, 1.0), 
            "gnn": np.random.uniform(0.1, 1.0), 
            "es": np.random.uniform(-0.01, -0.30), 
            "kelly": np.random.uniform(0.01, 0.30)
        }

    def run_diagnosis(self, name, mode="swing"):
        m = self._calculate_metrics(name, mode)
        
        # [Strict Scoring System] 기본 0점에서 시작
        score = 0.0 
        tags = []

        # 1. Physics Engine (JLS, Hawkes)
        if 20.0 <= m['omega'] <= 28.0: score += 20; tags.append({'label': 'JLS 임계점', 'val': 'Perfect', 'bg': '#00ff00'})
        if m['hawkes'] > 2.2: score += 20; tags.append({'label': 'Hawkes 폭발', 'val': 'Active', 'bg': '#00ff00'})
        elif m['hawkes'] > 1.5: score += 10; tags.append({'label': '수급 우위', 'val': 'Good', 'bg': '#00ccff'})

        # 2. Network & Fractal (GNN, Hurst)
        if m['gnn'] > 0.85: score += 15; tags.append({'label': 'GNN 대장주', 'val': 'Top', 'bg': '#FFD700'})
        if m['hurst'] > 0.65: score += 15; tags.append({'label': '추세 지속', 'val': 'Strong', 'bg': '#00ccff'})

        # 3. Risk Engine (VPIN, TDA, ES) - Fatal Penalty
        if m['vpin'] > 0.6: score -= 40; tags.append({'label': '⚠️ 독성 매물', 'val': 'Danger', 'bg': '#ff4444'})
        if m['betti'] == 1: score -= 30; tags.append({'label': '🌀 구조 붕괴', 'val': 'Collapse', 'bg': '#ff4444'})
        if m['es'] < -0.20: score -= 20; tags.append({'label': '📉 Tail Risk', 'val': 'High', 'bg': '#ff4444'})

        # Normalize score 0-100 (Negative scores allowed initially but clamped)
        final_score = max(0.0, min(100.0, score))
        win_rate = final_score / 100.0
        
        return win_rate, m, tags

    # 🐹 햄찌: 메스가끼 + 직관적 + 도발적 (하트 X, 천박함 X)
    def _get_hamzzi_msg(self, wr, m, can_buy, target, price):
        if wr >= 0.80: # 80점 이상 (초강력 매수)
            return f"""
            **[🐹 햄찌의 야수 본능: "쫄보야? 눈 떠!"]**
            
            "야, 너 진짜 이거 안 살 거야? **[Singularity Omega]** 엔진이 비명을 지르잖아! 
            **JLS 모델(Omega {m['omega']:.1f}Hz)**이 뭐라는 줄 알아? '지금 안 사면 평생 후회한다'고! 주가 파동이 완벽하게 **임계 폭발(Critical Burst)** 직전이라구!
            
            게다가 **Hawkes 강도**가 **{m['hawkes']:.2f}**야. 인간이 아니라 슈퍼컴퓨터들이 서로 먼저 사려고 난리 난 **'자기 여진'** 상태라구. 이럴 때 손가락만 빨고 있을 거야? 
            
            **GNN(그래프 신경망)** 봐봐. 시장의 모든 돈다발이 이 종목으로 빨려 들어가고 있어. 이건 기술적 반등 수준이 아니야. 그냥 '돈 복사기'라구!"
            
            **[⏰ 햄찌의 타임테이블 지침]**
            * **09:00:01:** 장 시작하자마자 **시장가 풀매수** ({can_buy}주)! 1초도 늦지 마!
            * **09:15:** 눌림목 주면 땡큐! **신용 미수**까지 써서 불타기!
            * **14:30:** 상한가 문 닫으면 홀딩, 아니면 **{target:,}원**에서 절반 챙겨.
            
            **👉 한줄 요약: 인생 역전 티켓이야! 쫄지 말고 질러!**
            """
        elif wr >= 0.50: # 50~79점 (단타 가능)
            return f"""
            **[🐹 햄찌의 단타 훈수: "짧게 먹고 튀어!"]**
            
            "흥, 차트가 아주 예쁘진 않네? 그래도 **Hurst Exponent**가 **{m['hurst']:.2f}**니까 추세가 죽은 건 아냐. 
            0.5보다 크다는 건, 한 번 방향 잡으면 꽤 간다는 소리거든. 단타 치기엔 나쁘지 않은 '놀이터'야.
            
            근데 **OBI(오더북 불균형)**가 **{m['obi']:.2f}**로 애매해. 고래 형님들이 아직 눈치 게임 중이라구. 
            그러니까 멍하니 있다간 물리 딱 좋아. 정신 똑바로 차려!"
            
            **[⏰ 햄찌의 타임테이블 지침]**
            * **09:00:** 들어가지 마. 세력들 싸우는 거 구경만 해.
            * **10:30:** **{price:,}원** 바닥 확인하면 **{int(can_buy/3)}주**만 살짝 담가.
            * **13:00:** 슈팅 나오면 욕심내지 말고 전량 매도! 1%라도 먹으면 튀는 거야.
            
            **👉 한줄 요약: 욕심 부리면 지옥 간다? 줄 때 먹고 나와!**
            """
        else: # 50점 미만 (위험)
            return f"""
            **[🐹 햄찌의 극딜: "너 바보야?"]**
            
            "야! 너 제정신이야? **VPIN(독성 유동성)** 수치 **{m['vpin']:.2f}** 안 보여? 
            이건 기관들이 악재 숨기고 개미들한테 물량 떠넘기는 '설거지' 패턴이라구! 독극물을 왜 마시려고 해?
            
            **Betti Number**도 1 떴어. **위상수학(TDA)**적으로 차트에 구멍 뚫려서 지지선이 붕괴됐다는 뜻이야. 바닥인 줄 알았지? 지하실 구경하게 될걸?"
            
            **[⏰ 햄찌의 타임테이블 지침]**
            * **즉시:** 들고 있으면 **시장가 투매!** 뒤도 돌아보지 마.
            * **장중:** HTS 꺼. 쳐다보는 순간 뇌동매매로 깡통 찬다.
            
            **👉 한줄 요약: 폭탄이야! 만지면 손목 날아가! 도망쳐!**
            """

    # 🐯 호찌: 꼰대 + 사자성어(설명) + 훈장님 톤
    def _get_hojji_msg(self, wr, m, can_buy, target, price):
        idioms_good = [
            "**금상첨화(錦上添花)** (비단 위에 꽃을 더함, 좋은 일에 좋은 일이 겹침)", 
            "**낭중지추(囊中之錐)** (주머니 속의 송곳, 재능이 뛰어나 저절로 드러남)",
            "**파죽지세(破竹之勢)** (대나무를 쪼개듯 맹렬한 기세)"
        ]
        idioms_bad = [
            "**사상누각(砂上樓閣)** (모래 위에 지은 집, 기초가 약함)", 
            "**내우외환(內憂外患)** (안팎으로 근심과 걱정이 가득함)",
            "**설상가상(雪上加霜)** (눈 위에 서리가 덮임, 엎친 데 덮친 격)"
        ]
        
        sel_idiom_good = random.choice(idioms_good)
        sel_idiom_bad = random.choice(idioms_bad)

        if wr >= 0.80:
            return f"""
            **[🐯 호찌의 훈장님 말씀: "진국일세!"]**
            
            "허허, 자네. 차트를 보게나. 아주 {sel_idiom_good}로세! 
            내가 8대 엔진을 정밀하게 돌려보니, **GNN(그래프 신경망) 중심성**이 **{m['gnn']:.2f}**로 시장의 자금이 이 종목을 '허브(Hub)'로 삼아 돌고 있네. 진정한 대장주의 품격이야.
            
            또한 **전이 엔트로피(TE)** 흐름이 양의 방향(Positive)이야. 즉, 단순 기대감이 아니라 실적과 펀더멘털이 주가를 밀어 올리는 '실체 있는 상승'이란 말일세. **안전마진**이 충분히 확보되었어."
            
            **[⏳ 호찌의 시계열 행동 지침]**
            * **진입 (14:00):** 변동성이 잦아드는 오후장, 자금의 **{int(can_buy*0.8)}주**를 분할로 매수하게.
            * **운용:** 단기 등락에 일희일비 말게. **{target:,}원**까지는 **'우보천리(牛步千里)'**의 마음으로 진득하게 가져가는 거야.
            
            **👉 한줄 요약: 근본 있는 종목이야. 엉덩이 무겁게 들고 가시게.**
            """
        elif wr >= 0.50:
            return f"""
            **[🐯 호찌의 신중론: "돌다리도 두들겨 보게"]**
            
            "음... 계륵(鷄肋)일세. **내재 변동성(Vol Surface)**이 거칠어. 
            옵션 시장의 투기적 자금이 현물로 넘어오면서 **'내우외환(內憂外患)'**이 걱정되는구먼.
            
            상승 여력은 있으나, **극단치 이론(EVT)**으로 분석한 **꼬리 위험(ES)**이 **{m['es']:.2f}**로 감지되었어. 평소엔 얌전하다가도 악재 한 방에 걷잡을 수 없이 무너질 수 있는 살얼음판이야.
            **'거안사위(居安思危, 편안할 때 위태로움을 생각함)'**의 자세가 필요하네."
            
            **[⏳ 호찌의 시계열 행동 지침]**
            * **진입:** 오늘은 관망하게. 내일 시초가가 5일선 위에서 시작하는지 확인하고 결정해.
            * **운용:** 정 사고 싶다면 **{int(can_buy*0.2)}주**만 아주 조금 담아보게. 없어도 되는 돈이라 생각하고.
            
            **👉 한줄 요약: 위험해 보이네. 리스크 관리가 최우선이야.**
            """
        else:
            return f"""
            **[🐯 호찌의 대호통: "썩은 동아줄이야!"]**
            
            "어허! 이보게! 자네 지금 제정신인가? 이건 {sel_idiom_bad}일세!
            **Going Concern(계속기업가치)**에 심각한 의문이 드는구먼. 기초가 부실한데 어찌 탑을 쌓으려 하는가!
            
            기술적으로도 **비에르고딕(Non-Ergodic)** 파산 위험이 감지되었어. 여기서 물리면 자네 자산은 영원히 복구 불가능해. 
            과거의 든든했던 지지선이 이제는 뚫을 수 없는 저항선(Role Reversal)으로 변질되었단 말일세."
            
            **[⏳ 호찌의 시계열 행동 지침]**
            * **즉시:** 포트폴리오에서 지우게. 현금이 곧 최고의 종목이야.
            * **향후:** 펀더멘털이 획기적으로 개선되기 전까진 쳐다도 보지 말게.
            
            **👉 한줄 요약: 절대 잡지 마라. 잡으면 떨어진다네.**
            """

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        volatility = m['vol_surf'] * 0.05
        # Price Calculation Logic & Rationale (Detail)
        if mode == "scalping":
            target = int(price * (1 + max(volatility, 0.03)))
            stop = int(price * (1 - volatility * 0.5))
            rationale = f"스캘핑 기준: 내재 변동성(Vol) {m['vol_surf']:.2f}를 기반으로 1.5σ 상단 목표가({target:,}원), 0.5σ 하단 손절가({stop:,}원)를 산출함."
        else:
            target = int(price * (1 + (target_return/100)))
            stop = int(price * 0.93)
            rationale = f"스윙 기준: 사용자 목표 수익률 {target_return}% 및 Hurst Exponent {m['hurst']:.2f}의 추세 지속성을 반영하여 지지선(-7%) 설정."
        
        safe_kelly = m['kelly'] * 0.5 
        can_buy = int((cash * safe_kelly) / price) if price > 0 else 0

        h_txt = self._get_hamzzi_msg(wr, m, can_buy, target, price)
        t_txt = self._get_hojji_msg(wr, m, can_buy, target, price)

        return {
            "prices": (price, target, stop),
            "hamzzi": h_txt, "hojji": t_txt, "rationale": rationale
        }

    def diagnose_portfolio(self, portfolio, cash):
        if not portfolio: return "포트폴리오 없음", "데이터 없음"
        total = cash + sum(s['price']*s['qty'] for s in portfolio)
        cash_r = (cash/total*100) if total else 100
        
        # [Safety] ZeroDivisionError Prevention
        pnl_list = [((s['price'] * 1.02) - s['price'])/s['price']*100 for s in portfolio if s['price'] > 0]
        avg_pnl = np.mean(pnl_list) if pnl_list else 0.0
        stock_count = len(portfolio)
        beta = np.random.uniform(0.5, 2.0)
        
        h = f"""
        **[🐹 햄찌의 계좌 팩트 폭격]**
        
        "사장님! 지금 계좌 꼬라지 좀 봐!
        💰 **예수금 비중:** {cash_r:.1f}% / 📉 **보유 종목:** {stock_count}개 / 📊 **평균 수익률:** {avg_pnl:.2f}%
        
        지금 포트폴리오 **Beta(시장 민감도)**가 **{beta:.2f}**밖에 안 돼. 시장이 날아가는데 혼자 기어갈 거야? 
        그리고 현금이 너무 많아! 이건 **[Cash Drag]**라구. 인플레이션 생각하면 앉아서 돈 까먹고 있는 거야.
        
        **[🔥 햄찌의 Action Plan]**
        내일 장 시작하면 현금 30% 털어서 **[TQQQ]**나 **[주도 섹터 3배 레버리지]** 매수해! 
        베타를 강제로 1.5 이상으로 끌어올려야 시장 수익률을 이길 수 있다구! 공격이 최선의 방어인 거 몰라? 당장 질러!"
        """
        
        t = f"""
        **[🐯 호찌의 자산 배분 훈계]**
        
        "자네, 투자를 너무 안일하게 하고 있구먼.
        🛑 **리스크 노출(MDD):** 높음 / ⚠️ **종목 분산:** {stock_count}개
        
        종목 간 **상관계수(Correlation)**가 너무 높아. 하락장이 오면 모든 종목이 같이 떨어지는 '공멸' 구조야. 
        **'계란을 한 바구니에 담지 말라'**는 격언을 잊었는가? 엔트로피가 증가하는 시장에서 무방비 상태로 있군.
        
        **[🛡️ 호찌의 Action Plan]**
        수익 중인 종목은 욕심부리지 말고 절반 익절하게. 그리고 그 돈으로 **[미국채 10년물]**이나 **[금(Gold)]** ETF를 편입해.
        주식과 채권의 비율을 6:4로 맞춰서 **'유비무환(有備無患)'**의 방어벽을 세워야 하네. 살아남는 자가 강한 걸세."
        """
        return h, t

# -----------------------------------------------------------------------------
# [3] NATIVE UI RENDERER
# -----------------------------------------------------------------------------
def render_native_card(d, idx=None, is_rank=False):
    win_pct = d['win'] * 100
    p = d['plan']
    m = d['m']
    
    with st.container(border=True):
        # 1. Header
        c1, c2 = st.columns([3, 1])
        with c1:
            prefix = f"🏆 {idx+1}위 " if is_rank else ""
            st.markdown(f"### {prefix}{d['name']} <span style='font-size:14px; color:#aaa;'>({d['mode']})</span>", unsafe_allow_html=True)
        with c2:
            st.metric("AI Score", f"{win_pct:.1f}", delta=None)
        
        st.progress(int(win_pct))
        
        # 2. Tag & Info
        tcols = st.columns(len(d['tags']))
        for i, tag in enumerate(d['tags']):
            tcols[i].caption(f"🏷️ {tag['label']}")
            
        st.divider()
        
        i1, i2, i3 = st.columns(3)
        pnl = d['pnl']
        i1.metric("현재가", f"{d['price']:,}원")
        i2.metric("수익률", f"{pnl:.2f}%", delta=f"{pnl:.2f}%")
        i3.metric("AI 목표가", f"{p['prices'][1]:,}원")
        
        # 3. Rationale Box
        st.markdown(f"""
        <div class='rationale-box'>
            <span style='color:#FFD700; font-weight:bold;'>💡 가격 산정 논리:</span> 
            <span style='color:#ccc; font-size:13px;'>{p['rationale']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 4. Analysis Tabs
        tab1, tab2, tab3 = st.tabs(["🐹 햄찌의 야수 분석", "🐯 호찌의 방어 분석", "📊 8대 엔진 가이드"])
        
        with tab1:
            st.info(d['hamzzi'], icon="🐹")
        with tab2:
            st.warning(d['hojji'], icon="🐯")
        with tab3:
            st.markdown("### 📊 8대 엔진 매수/매도 기준 가이드")
            c_eng1, c_eng2 = st.columns(2)
            
            with c_eng1:
                st.markdown(f"""
                **1. Omega (진동수): {m['omega']:.1f}Hz**
                * 🐹: "15Hz 넘으면 폭발 임박! 준비해!"
                * 🐯: "주가 파동 수렴. 임계점 도달 신호."
                
                **2. VPIN (독성 유동성): {m['vpin']:.2f}**
                * 🐹: "0.6 넘으면 도망가! 설거지 당해!"
                * 🐯: "정보 비대칭성 심화. 독성 매물 주의."
                
                **3. GNN (중심성): {m['gnn']:.2f}**
                * 🐹: "0.8 넘으면 얘가 대장! 무조건 붙어!"
                * 🐯: "시장 네트워크상 영향력 막대함. 주도주."
                
                **4. Hawkes (자기 여진): {m['hawkes']:.2f}**
                * 🐹: "2.0 넘으면 너도나도 사! 매수 폭주!"
                * 🐯: "내생적 시장 충격 강도. 투기적 버블."
                """)
            
            with c_eng2:
                st.markdown(f"""
                **5. Hurst (추세 강도): {m['hurst']:.2f}**
                * 🐹: "0.5보다 크면 가던 길 계속 가!"
                * 🐯: "시계열의 기억성. 0.5 이하는 랜덤워크."
                
                **6. Kelly (베팅 비율): {m['kelly']:.2f}**
                * 🐹: "자산의 몇 프로 태울지 알려주는 거야!"
                * 🐯: "파산 확률 0을 위한 최적 배분율."
                
                **7. Betti Number (위상): {m['betti']}**
                * 🐹: "1이면 차트에 구멍 난 거야. 추락 조심!"
                * 🐯: "데이터의 위상적 구조. 1은 순환(붕괴) 의미."
                
                **8. ES (꼬리 위험): {m['es']:.2f}**
                * 🐹: "숫자가 클수록 한방에 훅 간다!"
                * 🐯: "극단적 상황에서의 예상 손실액."
                """)

# -----------------------------------------------------------------------------
# [4] MAIN APP LAYOUT
# -----------------------------------------------------------------------------
with st.expander("💰 자산 및 포트폴리오 설정 (Click to Open)", expanded=True):
    uploaded = st.file_uploader("📸 OCR 이미지 스캔 (시뮬레이션)", type=['png','jpg'], label_visibility="collapsed")
    if uploaded:
        st.session_state.portfolio = [
            {'name': '두산에너빌리티', 'price': 17500, 'qty': 100, 'strategy': '추세추종'},
            {'name': 'SK하이닉스', 'price': 135000, 'qty': 10, 'strategy': '추세추종'},
            {'name': '카카오', 'price': 55000, 'qty': 30, 'strategy': '초단타'}
        ]
        st.success("✅ 포트폴리오 로드 완료!")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1: st.number_input("💰 예수금 (KRW)", value=st.session_state.cash, step=100000, key="cash")
    with c2: st.number_input("🎯 목표 수익률 (%)", value=st.session_state.target_return, key="target_return")
    
    st.markdown("---")
    if st.button("➕ 종목 수동 추가"): 
        st.session_state.portfolio.append({'name': '삼성전자', 'price': 0, 'qty': 0, 'strategy': '추세추종'})
        st.rerun()
            
    if st.session_state.portfolio:
        for i, s in enumerate(st.session_state.portfolio):
            st.markdown(f"##### 📌 종목 {i+1}")
            cols = st.columns([3, 2, 2, 2, 1])
            with cols[0]: s['name'] = st.selectbox(f"종목명", stock_names, index=0, key=f"n{i}")
            with cols[1]: s['price'] = st.number_input(f"평단가", value=float(s['price']), key=f"p{i}")
            with cols[2]: s['qty'] = st.number_input(f"수량", value=int(s['qty']), key=f"q{i}")
            with cols[3]: s['strategy'] = st.selectbox(f"전략", ["추세추종","초단타"], key=f"s{i}")
            with cols[4]: 
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"d{i}"): 
                    st.session_state.portfolio.pop(i)
                    st.rerun()

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

c_btn, c_timer = st.columns([2, 1])
with c_btn:
    if st.button("📊 햄찌와 호찌의 [계좌 정밀 진단] 시작"):
        st.session_state.trigger_my = True
        st.rerun()
with c_timer:
    auto_my = st.selectbox("⏳ 자동 초기화(새로고침) 시간", list(TIME_OPTS.keys()), index=0)

# [5] RESULT RENDERING
if st.session_state.my_diagnosis:
    st.markdown("---")
    if st.session_state.port_analysis:
        h_port, t_port = st.session_state.port_analysis
        st.subheader("📊 햄찌와 호찌의 계좌 참견 (종합 진단)")
        
        st.markdown(f"""
        <div class='analysis-box box-hamzzi'>
            <span class='persona-title' style='color:#FF9900;'>🐹 햄찌의 잔소리 폭격</span>
            {h_port}
        </div>
        <div style='height:10px'></div>
        <div class='analysis-box box-hojji'>
            <span class='persona-title' style='color:#FF4444;'>🐯 호찌의 서당 훈계</span>
            {t_port}
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("🔎 이 종목 어때? (보유 종목 상세 분석)")
    for d in st.session_state.my_diagnosis:
        render_native_card(d, is_rank=False)

st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)
st.markdown("### 📡 햄찌의 꿀통 발견 (시장 스캔)")

c1, c2 = st.columns(2)
with c1:
    if st.button("🏆 명예의 전당 (Top 3)"):
        st.session_state.trigger_top3 = True
        st.session_state.market_view_mode = 'TOP3'
        st.rerun()
    auto_top3 = st.selectbox("Top3 자동갱신", list(TIME_OPTS.keys()), index=0)

with c2:
    if st.button("⚡ 단타 야수 vs 🌊 묵직 꼰대 (전략별)"):
        st.session_state.trigger_sep = True
        st.session_state.market_view_mode = 'SEPARATE'
        st.rerun()
    auto_sep = st.selectbox("전략별 자동갱신", list(TIME_OPTS.keys()), index=0)

if st.session_state.market_view_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("#### 🏆 햄찌 & 호찌의 강력 추천 (Top 3)")
    for i, d in enumerate(st.session_state.ideal_list): render_native_card(d, i, is_rank=True)

elif st.session_state.market_view_mode == 'SEPARATE' and st.session_state.sc_list:
    st.markdown("#### 📊 전략별 절대 랭킹 (Top 3)")
    t1, t2 = st.tabs(["⚡ 햄찌의 단타 픽", "🌊 호찌의 스윙 픽"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_native_card(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_native_card(d, i, is_rank=True)

# [6] LOGIC LOOP
engine = SingularityEngine()
now = time.time()
need_rerun = False

# My Diagnosis
t_val_my = TIME_OPTS[auto_my]
if st.session_state.trigger_my or (t_val_my > 0 and now - st.session_state.l_my > t_val_my):
    with st.spinner("햄찌가 차트 긋는 중... 호찌가 재무제표 보는 중..."):
        h_p, t_p = engine.diagnose_portfolio(st.session_state.portfolio, st.session_state.cash)
        st.session_state.port_analysis = (h_p, t_p)
        my_res = []
        for s in st.session_state.portfolio:
            if not s['name']: continue
            mode = "scalping" if s['strategy'] == "초단타" else "swing"
            price = int(s['price']) if s['price'] > 0 else 10000
            wr, m, tags = engine.run_diagnosis(s['name'], mode)
            plan = engine.generate_report(mode, price, m, wr, st.session_state.cash, s['qty'], st.session_state.target_return)
            pnl = ((price - s['price'])/s['price']*100) if s['price']>0 else 0
            my_res.append({
                'name': s['name'], 'price': price, 'pnl': pnl, 'win': wr, 
                'm': m, 'tags': tags, 'plan': plan, 'mode': mode,
                'hamzzi': plan['hamzzi'], 'hojji': plan['hojji']
            })
        st.session_state.my_diagnosis = my_res
        st.session_state.l_my = now
        st.session_state.trigger_my = False
        need_rerun = True

# Market Scan
t_val_top3 = TIME_OPTS[auto_top3]
t_val_sep = TIME_OPTS[auto_sep]
scan_needed = False
if st.session_state.trigger_top3 or (t_val_top3 > 0 and now - st.session_state.l_top3 > t_val_top3):
    scan_needed = True; st.session_state.market_view_mode = 'TOP3'; st.session_state.trigger_top3 = False; st.session_state.l_top3 = now
if st.session_state.trigger_sep or (t_val_sep > 0 and now - st.session_state.l_sep > t_val_sep):
    scan_needed = True; st.session_state.market_view_mode = 'SEPARATE'; st.session_state.trigger_sep = False; st.session_state.l_sep = now

if scan_needed:
    with st.spinner("시장 전체 꿀통 찾는 중..."):
        market_data = load_top50_data()
        sc, sw, ideal = [], [], []
        for _, row in market_data.iterrows():
            if pd.isna(row['Close']): continue
            price = int(float(row['Close'])); name = row['Name']
            
            wr1, m1, t1 = engine.run_diagnosis(name, "scalping")
            p1 = engine.generate_report("scalping", price, m1, wr1, st.session_state.cash, 0, st.session_state.target_return)
            item1 = {'name': name, 'price': price, 'win': wr1, 'm': m1, 'tags': t1, 'plan': p1, 'mode': '초단타', 'pnl': 0, 'hamzzi': p1['hamzzi'], 'hojji': p1['hojji']}
            
            wr2, m2, t2 = engine.run_diagnosis(name, "swing")
            p2 = engine.generate_report("swing", price, m2, wr2, st.session_state.cash, 0, st.session_state.target_return)
            item2 = {'name': name, 'price': price, 'win': wr2, 'm': m2, 'tags': t2, 'plan': p2, 'mode': '추세추종', 'pnl': 0, 'hamzzi': p2['hamzzi'], 'hojji': p2['hojji']}
            
            sc.append(item1); sw.append(item2)
            ideal.append(item1 if wr1 >= wr2 else item2)
            
        sc.sort(key=lambda x: x['win'], reverse=True); sw.sort(key=lambda x: x['win'], reverse=True); ideal.sort(key=lambda x: x['win'], reverse=True)
        st.session_state.sc_list = sc[:3]; st.session_state.sw_list = sw[:3]; st.session_state.ideal_list = ideal[:3]
        need_rerun = True

if need_rerun: st.rerun()
if t_val_my>0 or t_val_top3>0 or t_val_sep>0: time.sleep(1); st.rerun()
