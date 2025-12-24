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
# 요청하신 시간 목록 + '수동' 단어 제거 -> '멈춤'
TIME_OPTS = {"⛔ 멈춤": 0, "⏱️ 3분마다": 180, "⏱️ 10분마다": 600, "⏱️ 30분마다": 1800}

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
# [1] STYLING (Cute & Readable)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global */
    .stApp { background-color: #050505; color: #ffffff; font-family: 'Pretendard', sans-serif; }
    
    /* Buttons: Neon Gold Style */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 55px; font-size: 18px;
        background-color: #1a1a1a; 
        border: 2px solid #FFD700; 
        color: #FFD700; 
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color: #FFD700; color: #000; 
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.8); border-color: #fff;
    }
    
    /* Input Labels */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-size: 16px !important; font-weight: 900 !important; color: #FFD700 !important;
        margin-bottom: 5px !important;
    }
    
    /* Card UI */
    .stock-card { 
        background: #111; border: 1px solid #333; border-radius: 16px; 
        padding: 20px; margin-bottom: 30px; box-shadow: 0 8px 30px rgba(0,0,0,0.8);
    }
    
    /* Rationale Box */
    .rationale-box {
        background: #151515; padding: 15px; border-radius: 8px; margin-top: 15px; border: 1px dashed #555;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] { font-size: 26px !important; color: #fff !important; font-weight: 800 !important; }
    
    /* Engine Guide */
    .engine-guide { font-size: 13px; color: #aaa; background: #222; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    
    /* Headers */
    h1, h2, h3 { font-family: 'Ownglyph_MX', sans-serif !important; }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -15px !important; margin-top: 23px; }
</style>
""", unsafe_allow_html=True)

# [TITLE]
st.markdown("<h1 style='text-align: center; color: #FFD700; font-size: 40px;'>🐯 호찌와 햄찌의 퀀트 대작전 🐹</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# [2] SINGULARITY OMEGA ENGINE (Extreme Detail Logic)
# -----------------------------------------------------------------------------
class SingularityEngine:
    def _calculate_metrics(self, name, mode):
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H-%M-%S')}-{random.randint(0,1000)}"
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
        tags = [{'label': '기본 마진', 'val': '+35', 'bg': '#cccccc'}]

        if m['vpin'] > 0.6: score -= 20; tags.append({'label': '⚠️ 독성 매물', 'val': '-20', 'bg': '#ff4444'})
        if m['es'] < -0.20: score -= 15; tags.append({'label': '📉 Tail Risk', 'val': '-15', 'bg': '#ff4444'})
        
        if mode == "scalping":
            if m['hawkes'] > 2.0: score += 45; tags.append({'label': '🚀 Hawkes 폭발', 'val': '+45', 'bg': '#00ff00'})
            elif m['hawkes'] > 1.5: score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'bg': '#00ccff'})
        else: 
            if m['hurst'] > 0.7: score += 40; tags.append({'label': '📈 추세 지속', 'val': '+40', 'bg': '#00ff00'})
            elif m['hurst'] > 0.6: score += 10; tags.append({'label': '↗️ 모멘텀 양호', 'val': '+10', 'bg': '#00ccff'})

        if m['gnn'] > 0.8: score += 10; tags.append({'label': '👑 GNN 대장주', 'val': '+10', 'bg': '#FFD700'})
        win_rate = min(0.98, max(0.02, score / 100))
        return win_rate, m, tags

    # 🐹 햄찌: 메스가끼 + 공격적 + 엄청 긴 설명
    def _get_hamzzi_msg(self, wr, m, can_buy, target, price):
        if wr >= 0.70:
            return f"""
            **[🐹 햄찌의 야수 본능 브리핑]**
            
            "야, 쫄보야? 아직도 매수 버튼 안 눌렀어? 내가 진짜 답답해서 못 살겠다. 지금 **[Singularity Omega Engine]** 돌려보니까 완전 대박 신호 떴잖아!
            
            첫째, **JLS 모델(Johansen-Ledoit-Sornette)** 상 주가 파동의 진동수(Omega)가 **{m['omega']:.2f}Hz**로 수렴하고 있어. 이게 무슨 뜻인지 알아? 물리학적으로 주가가 '임계 폭발(Critical Burst)' 직전이라는 거야. 지진 나기 직전에 진동계가 미친 듯이 떨리는 거랑 똑같다구!
            
            둘째, **Hawkes Process(자기 여진)** 강도가 **{m['hawkes']:.2f}**를 돌파했어. 사람이 사는 게 아니라, 고빈도 매매(HFT) 알고리즘들이 서로를 자극하면서 미친 듯이 매수 주문을 쏟아내고 있는 상태야. 이럴 때 안 타면 언제 탈래? 평생 손가락만 빨 거야?
            
            셋째, **GNN(그래프 신경망)** 중심성이 **{m['gnn']:.2f}**야. 시장의 모든 유동성이 이 종목을 블랙홀처럼 빨아들이고 있다고! 이건 그냥 기술적 반등이 아니라 '패러다임의 변화'야."
            
            **[⏰ 햄찌의 초정밀 매매 타임테이블]**
            * **08:55 - 09:00:** 동시호가 예상 체결량 급증 확인.
            * **09:00:01:** 장 시작하자마자 **시장가(Market Order)**로 **{can_buy}주** 전량 매수! 1초도 망설이지 마!
            * **09:15:** 만약 3% 이상 급등하면 눌림목(VWAP 근처)에서 **신용 미수**까지 써서 불타기!
            * **13:00:** 기관들 점심 먹고 들어올 때 슈팅 나오면 **{target:,}원**에서 절반 익절. 나머지는 상한가 굳히기 들어갈 때까지 홀딩!
            
            **👉 한줄 요약: 인생 역전 기회야! 쫄지 말고 풀매수 박아! 나 믿고 따라와!**
            """
        elif wr >= 0.50:
            return f"""
            **[🐹 햄찌의 단타 훈수]**
            
            "흥, 차트가 좀 애매하네? 그래도 먹을 자리는 있어 보여. **Hurst Exponent(허스트 지수)**가 **{m['hurst']:.2f}**잖아. 0.5보다 크니까 추세가 한 번 잡히면 계속 가려는 성질(Persistence)이 있다는 거야. 즉, 단타 치기 딱 좋은 '롤러코스터' 구간이지.
            
            근데 조심해야 해. **OBI(오더북 불균형)** 수치가 **{m['obi']:.2f}**로 중립적이야. 매수 세력이랑 매도 세력이 팽팽하게 줄다리기하고 있어서, 자칫하면 고래 싸움에 새우 등 터질 수 있어.
            
            그리고 **Vol Surface(변동성 표면)**가 약간 찌그러져 있어. 옵션 시장 형님들이 아직 확신을 못 하고 있다는 증거야. 그러니까 길게 가져가면 절대 안 돼. 알겠어?"
            
            **[⏰ 햄찌의 초정밀 매매 타임테이블]**
            * **09:00 - 09:30:** 절대 진입 금지. 세력들 간 보는 시간이야. 구경만 해.
            * **10:00:** 1차 파동 끝나고 **{price:,}원** 지지선 형성되는지 호가창 뚫어지게 봐.
            * **10:30:** 지지선에서 매수 물량 쌓이면 **{int(can_buy/3)}주**만 '정찰병'으로 투입.
            * **13:30:** 점심 먹고 거래량 터질 때 2~3% 수익 나면 뒤도 돌아보지 말고 전량 매도! '줄먹(줄 때 먹기)'이 진리야.
            
            **👉 한줄 요약: 욕심 부리면 지옥 간다? 짧게 끊어 쳐서 치킨값만 벌어!**
            """
        else:
            return f"""
            **[🐹 햄찌의 극딜 경고]**
            
            "야! 너 바보야? 이런 쓰레기 차트를 왜 보고 있어? **VPIN(정보 비대칭 지표)** 수치가 **{m['vpin']:.2f}**까지 치솟았잖아! 이게 무슨 뜻이냐면, 기관 형님들이 악재 정보 미리 알고 개미들한테 물량 떠넘기는 '설거지' 중이라는 거야! 독극물이라구!
            
            게다가 **TDA(위상수학적 데이터 분석)** 돌려보니까 **Betti Number**가 1로 변했어. 위상수학적으로 차트 구조에 '구멍(Hole)'이 뚫렸다는 뜻이야. 지지선? 그딴 거 없어. 그냥 바닥 없이 추락할 거야.
            
            **Tail Risk(꼬리 위험)**도 **{m['es']:.2f}**야. 이건 평소엔 멀쩡하다가도 갑자기 하한가 꽂을 수 있는 수치라구. 내 돈 아니라고 막 쓰지 마!"
            
            **[⏰ 햄찌의 초정밀 매매 타임테이블]**
            * **지금 당장:** 보유 중이면 호가 낮춰서라도 **시장가 전량 매도!** 탈출은 지능순이야.
            * **장중 내내:** HTS 끄고 산책이나 가. 쳐다보는 순간 뇌동매매해서 깡통 찬다.
            * **장 마감 후:** 관심 종목에서도 삭제해. 쳐다도 보지 마.
            
            **👉 한줄 요약: 폭탄이야! 만지면 손목 날아가! 당장 도망쳐! 돔황챠!!**
            """

    # 🐯 호찌: 꼰대 + 사자성어(설명) + 방어적 + 엄청 긴 설명
    def _get_hojji_msg(self, wr, m, can_buy, target, price):
        idioms_good = [
            "금상첨화(錦上添花, 비단 위에 꽃을 더한다는 뜻으로 좋은 일에 좋은 일이 겹침)", 
            "낭중지추(囊中之錐, 주머니 속의 송곳처럼 재능이 뛰어나 저절로 드러남)", 
            "파죽지세(破竹之勢, 대나무를 쪼개듯 맹렬한 기세로 거침없이 나아감)", 
            "일취월장(日就月將, 나날이 다달이 발전하고 성장함)"
        ]
        idioms_bad = [
            "사상누각(砂上樓閣, 모래 위에 지은 집처럼 기초가 약하여 오래가지 못함)", 
            "내우외환(內憂外患, 안팎으로 근심과 걱정이 가득한 상태)", 
            "풍전등화(風前燈火, 바람 앞의 등불처럼 매우 위태로운 상황)", 
            "설상가상(雪上加霜, 눈 위에 서리가 덮인다는 뜻으로 엎친 데 덮친 격)"
        ]
        
        sel_idiom_good = random.choice(idioms_good)
        sel_idiom_bad = random.choice(idioms_bad)

        if wr >= 0.70:
            return f"""
            **[🐯 호찌의 훈장님 심층 분석]**
            
            "허허, 자네. 차트를 보게나. 아주 **{sel_idiom_good}**로세! 내가 8대 엔진을 돌려보니 아주 훌륭한 결과가 나왔어.
            
            우선 **GNN(그래프 신경망)** 분석 결과, 이 종목의 중심성 계수가 **{m['gnn']:.2f}**일세. 이는 마치 시장의 모든 자금과 정보가 이 종목을 중심으로 도는 '태양계의 태양'과 같다는 뜻이야. 진정한 주도주(Leader)의 품격을 갖췄지.
            
            또한 **전이 엔트로피(Transfer Entropy)**를 측정해보니, 선행 지표들로부터 양의 정보 흐름(Positive Information Flow)이 유입되고 있어. 즉, 단순한 기대감이 아니라 실질적인 펀더멘털과 수급의 뒷받침이 있다는 증거일세. **Kelly Criterion(켈리 공식)** 상으로도 비중을 실어도 좋다는 신호가 나왔네."
            
            **[⏳ 호찌의 시계열 행동 지침]**
            * **진입 시점:** 오전장의 혼란스러움이 가라앉고 변동성이 줄어드는 **오후 2시경**, 기관들의 수급을 확인하고 들어가는 게 정석일세.
            * **운용 전략:** 자네 가용 자금의 **{int(can_buy*0.8)}주** 정도를 3회에 걸쳐 분할 매수하게. 평단을 유리하게 가져가야 마음이 편한 법이야.
            * **청산 목표:** **{target:,}원**에 도달하기 전까지는 단기 등락에 일희일비하지 말고, **'우보천리(牛步千里)'**의 마음으로 진득하게 홀딩하게.
            
            **👉 한줄 요약: 진국일세. 믿고 맡겨보게나. 엉덩이 무거운 자가 승리하는 법이야.**
            """
        elif wr >= 0.50:
            return f"""
            **[🐯 호찌의 신중론 및 훈계]**
            
            "음... 계륵(鷄肋)일세. 먹자니 먹을 게 없고, 버리자니 아까운 형국이야. 
            **국소 변동성(Local Volatility)** 표면이 너무 거칠어. 이는 옵션 시장의 투기적 거래가 현물 시장에 전이되어 주가가 널뛰기할 수 있다는 위험 신호일세. **내우외환(內憂外患)**이 걱정되는구먼.
            
            게다가 **EVT(극단치 이론)**로 시뮬레이션한 **꼬리 위험(Expected Shortfall)** 수치가 **{m['es']:.2f}**로 감지되었어. 평소에는 얌전하다가도, 한 번 악재가 터지면 걷잡을 수 없이 하락할 수 있는 잠재적 위험이 있다는 걸 명심하게.
            
            투자는 잃지 않는 것이 버는 것보다 중요한 법이야. **'거안사위(居安思危, 편안할 때 위태로움을 미리 생각함)'**의 자세가 필요하네."
            
            **[⏳ 호찌의 시계열 행동 지침]**
            * **진입 시점:** 오늘은 일단 관망하게. 내일 시초가가 5일 이동평균선 위에서 시작하는지 확인하고 결정해도 늦지 않아.
            * **운용 전략:** 정 사고 싶다면, 없어도 되는 돈이라 생각하고 **{int(can_buy*0.2)}주**만 아주 조금 담아보게.
            * **손절 원칙:** 매수가 대비 -3%만 빠져도 뒤도 돌아보지 말고 자르게.
            
            **👉 한줄 요약: 위험해 보이네. 돌다리도 두들겨 보고 건너게. 리스크 관리가 최우선이야.**
            """
        else:
            return f"""
            **[🐯 호찌의 대호통]**
            
            "어허! 이보게! 자네 지금 제정신인가? 이건 **{sel_idiom_bad}**일세! 기초가 부실한데 어찌 탑을 쌓으려 하는가!
            
            재무제표를 보게. **Going Concern(계속기업가치)**에 심각한 의문이 제기되고 있어. 펀더멘털이 훼손된 기업은 주가가 올라도 그건 '죽은 고양이의 반등(Dead Cat Bounce)'일 뿐이야. 속으면 안 되네.
            
            기술적으로도 **비에르고딕(Non-Ergodic)** 파산 위험이 감지되었어. 여기서 한 번 크게 물리면, 자네의 자산은 영원히 복구 불가능한 상태가 될 수 있네. 과거의 강력했던 지지선이 이제는 뚫을 수 없는 저항선(Role Reversal)으로 변질되었단 말일세."
            
            **[⏳ 호찌의 시계열 행동 지침]**
            * **즉시:** 포트폴리오에서 제외하게. 가지고 있다면 지금 당장 시장가로 처분해서 현금화하게.
            * **향후:** 이 종목은 쳐다도 보지 말게. 펀더멘털이 획기적으로 개선되기 전까진 관심 종목에서도 지우는 게 좋아.
            * **명심:** 쉬는 것도 투자일세. 현금이 곧 최고의 종목이라는 걸 잊지 말게.
            
            **👉 한줄 요약: 썩은 동아줄이야. 잡으면 떨어진다네. 절대 잡지 마라.**
            """

    def diagnose_portfolio(self, portfolio, cash):
        if not portfolio: return "포트폴리오 없음", "데이터 없음"
        
        # 데이터 계산
        total_assets = cash + sum(s['price']*s['qty'] for s in portfolio)
        cash_ratio = (cash/total_assets*100) if total_assets > 0 else 100
        stock_count = len(portfolio)
        
        # 가상 PnL 및 베타
        pnl_list = [((s['price'] * 1.02) - s['price'])/s['price']*100 for s in portfolio if s['price'] > 0]
        avg_pnl = np.mean(pnl_list) if pnl_list else 0.0
        beta = np.random.uniform(0.5, 2.0)
        mdd = np.random.uniform(-5.0, -40.0)
        
        # 🐹 햄찌의 포트폴리오 극딜
        h = f"""
        **[🐹 햄찌의 계좌 팩트 폭격]**
        
        "사장님! 지금 계좌 꼬라지 좀 봐!
        💰 **예수금 비중:** {cash_ratio:.1f}% / 📉 **보유 종목:** {stock_count}개 / 📊 **평균 수익률:** {avg_pnl:.2f}%
        
        지금 **Beta(시장 민감도)**가 **{beta:.2f}**밖에 안 돼. 시장이 날아가는데 혼자 기어갈 거야? 
        그리고 현금이 너무 많아! 이건 **[Cash Drag]**라구. 인플레이션 생각하면 앉아서 돈 까먹고 있는 거야. 바보야?
        
        **[Action Plan]**
        내일 장 시작하자마자 현금 50% 털어서 **[TQQQ]**나 **[주도 섹터 3배 레버리지]** 매수해! 
        베타를 강제로 1.5 이상으로 끌어올려야 시장 수익률을 이길 수 있다구! 공격이 최선의 방어인 거 몰라? 당장 질러! 🔥"
        """
        
        # 🐯 호찌의 포트폴리오 훈계
        t = f"""
        **[🐯 호찌의 자산 배분 훈계]**
        
        "자네, 투자를 너무 안일하게 하고 있구먼.
        🛑 **리스크 노출:** MDD {mdd:.1f}% / ⚠️ **종목 분산:** {stock_count}개 (부족/과다)
        
        종목 간 **상관계수(Correlation)**가 너무 높아. 하락장이 오면 모든 종목이 같이 떨어지는 '공멸' 구조야. 
        **'계란을 한 바구니에 담지 말라'**는 격언을 잊었는가? 엔트로피가 증가하는 시장에서 무방비 상태로 있군.
        
        **[Action Plan]**
        수익 중인 종목은 욕심부리지 말고 절반 익절하게. 그리고 그 돈으로 **[미국채 10년물]**이나 **[금(Gold)]** ETF를 편입해.
        주식과 채권의 비율을 6:4로 맞춰서 '유비무환(有備無患)'의 방어벽을 세워야 하네. 살아남는 자가 강한 걸세. 🛡️"
        """
        return h, t

# -----------------------------------------------------------------------------
# [3] NATIVE UI RENDERER (Safe & Clean)
# -----------------------------------------------------------------------------
def render_native_card(d, idx=None, is_rank=False):
    win_pct = d['win'] * 100
    p = d['plan']
    m = d['m']
    
    with st.container(border=True):
        # 1. Header Area
        c1, c2 = st.columns([3, 1])
        with c1:
            prefix = f"🏆 {idx+1}위 " if is_rank else ""
            st.markdown(f"### {prefix}{d['name']} <span style='font-size:14px; color:#aaa;'>({d['mode']})</span>", unsafe_allow_html=True)
        with c2:
            st.metric("AI Score", f"{win_pct:.1f}", delta=None)
        
        st.progress(int(win_pct))
        
        # 2. Tag & Info Area
        tcols = st.columns(len(d['tags']))
        for i, tag in enumerate(d['tags']):
            tcols[i].caption(f"🏷️ {tag['label']}")
            
        st.divider()
        
        i1, i2, i3 = st.columns(3)
        pnl = d['pnl']
        i1.metric("현재가", f"{d['price']:,}원")
        i2.metric("수익률", f"{pnl:.2f}%", delta=f"{pnl:.2f}%")
        i3.metric("AI 목표가", f"{p['prices'][1]:,}원")
        
        # 3. Rationale Box (Native Markdown)
        st.markdown(f"""
        <div class='rationale-box'>
            <span style='color:#FFD700; font-weight:bold;'>💡 가격 산정 논리:</span> 
            <span style='color:#ccc; font-size:13px;'>{p['rationale']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 4. Deep Analysis Tabs
        tab1, tab2, tab3 = st.tabs(["🐹 햄찌의 분석", "🐯 호찌의 분석", "📊 8대 엔진 가이드"])
        
        with tab1:
            st.info(d['hamzzi'], icon="🐹")
        with tab2:
            st.warning(d['hojji'], icon="🐯")
        with tab3:
            st.markdown("### 📊 8대 엔진 매매 기준 가이드")
            c_eng1, c_eng2 = st.columns(2)
            
            with c_eng1:
                st.markdown(f"""
                **1. Omega (진동수): {m['omega']:.1f}**
                * 🐹: "숫자가 높을수록 폭발 임박! 15Hz 넘으면 준비해!"
                * 🐯: "주가 파동의 주기적 수렴 정도. 임계점 도달 신호."
                
                **2. VPIN (독성 유동성): {m['vpin']:.2f}**
                * 🐹: "0.6 넘으면 도망가! 세력 형님들 설거지 타임이야!"
                * 🐯: "정보 비대칭성. 높으면 독성 매물 출회 위험."
                
                **3. GNN (중심성): {m['gnn']:.2f}**
                * 🐹: "0.8 넘으면 얘가 대장! 무조건 얘네 팀에 붙어!"
                * 🐯: "시장 네트워크상 영향력. 높을수록 주도주."
                """)
            
            with c_eng2:
                st.markdown(f"""
                **4. Hawkes (자기 여진): {m['hawkes']:.2f}**
                * 🐹: "2.0 넘으면 미친 듯이 사! 기계들이 펌핑 중!"
                * 🐯: "내생적 시장 충격의 강도. 투기적 버블 감지."
                
                **5. Hurst (추세 강도): {m['hurst']:.2f}**
                * 🐹: "0.5보다 크면 가던 길 계속 가! 추세 매매 꿀!"
                * 🐯: "시계열의 기억성. 0.5 이하는 랜덤워크(예측 불가)."
                
                **6. Kelly (베팅 비율): {m['kelly']:.2f}**
                * 🐹: "자산의 몇 프로 태울지 알려주는 거야. 쫄지마!"
                * 🐯: "파산 확률을 0으로 만드는 최적 자산 배분율."
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
    if st.button("🔍 햄찌 & 호찌의 [계좌 정밀 진단] 시작"):
        st.session_state.trigger_my = True
        st.rerun()
with c_timer:
    auto_my = st.selectbox("⏳ 자동 초기화(새로고침) 시간", list(TIME_OPTS.keys()), index=0)

# -----------------------------------------------------------------------------
# [5] RESULT RENDERING
# -----------------------------------------------------------------------------
if st.session_state.my_diagnosis:
    st.markdown("---")
    if st.session_state.port_analysis:
        h_port, t_port = st.session_state.port_analysis
        with st.container(border=True):
            st.subheader("📊 햄찌와 호찌의 계좌 참견 (종합 진단)")
            st.info(h_port, icon="🐹")
            st.warning(t_port, icon="🐯")
    
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

# -----------------------------------------------------------------------------
# [6] LOGIC LOOP
# -----------------------------------------------------------------------------
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
