import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random

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
# [1] CORE ENGINE: LOGIC & TEXT GENERATION
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
        if m['betti'] == 1: score -= 10; tags.append({'label': '구조 붕괴', 'val': '-10', 'type': 'bad'})
        
        if mode == "scalping":
            if m['hawkes'] > 2.5: score += 40; tags.append({'label': '🚀 퍼펙트 수급', 'val': '+40', 'type': 'best'})
            elif m['hawkes'] > 1.5: score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'type': 'good'})
        else: 
            if m['hurst'] > 0.75: score += 35; tags.append({'label': '📈 대세 상승장', 'val': '+35', 'type': 'best'})
            elif m['hurst'] > 0.6: score += 10; tags.append({'label': '↗️ 추세 양호', 'val': '+10', 'type': 'good'})

        win_rate = min(0.92, max(0.15, score / 100))
        return win_rate, m, tags

    # [TEXT GENERATOR ENGINE - INFINITE VARIETY]
    def _generate_text(self, persona, wr, m):
        # 🐹 HAMZZI (Aggressive, Cute, Quant)
        if persona == 'hamzzi':
            intros = ["사장님!!", "대박 사건!", "와우!", "히익!", "저기요...", "빨리 와봐!"]
            
            if wr >= 0.75:
                logic_1 = [
                    f"<b>[Hawkes {m['hawkes']:.2f}]</b> 수치 봤어? 이건 그냥 불기둥 예약이야! 🔥",
                    f"<b>[GNN 중심성]</b>이 폭발했어! 시장 돈이 다 여기로 쏠린다구! 💰",
                    f"<b>[Hurst {m['hurst']:.2f}]</b> 추세 강도가 미쳤어! 관성의 법칙 알지? 🚀"
                ]
                logic_2 = [
                    "지금 안 사면 오늘 밤 이불킥 각이야!",
                    "이런 기회는 1년에 몇 번 안 와! 야수의 심장을 꺼내!",
                    "풀레버리지 땡겨서 인생 역전 가보자구!"
                ]
                act = [
                    "시장가로 긁어! ⚡ 고민은 배송을 늦출 뿐!",
                    "영혼까지 끌어모아 풀매수! 💎 목표가까지 숨 참아!",
                    "지금 당장 탑승! 문 닫히기 전에 들어가! 🏃‍♂️💨"
                ]
            elif wr >= 0.55:
                logic_1 = [
                    f"음~ <b>[Vol Surface]</b>가 꿈틀대는데? 변동성 먹기 딱 좋은 날이야! 🌊",
                    f"<b>[OBI]</b> 호가창 보니까 매수세가 살아있어! 단타 치기 좋은 놀이터네!",
                    f"나쁘지 않아! <b>[Omega 파동]</b>도 안정적이고... 한번 들어가볼까? 🐹"
                ]
                logic_2 = [
                    "근데 몰빵은 좀 무섭고, 발만 담가보자!",
                    "오르면 불타기(Pyramiding) 하고 내리면 튀는 거야!",
                    "딱 기계적으로 대응하면 쏠쏠할 것 같아!"
                ]
                act = [
                    "정찰병 진입! 🪖 간 보다가 슈팅 나오면 불타기!",
                    "일단 30%만 사보자. 🍰 상황 봐서 더 담아!",
                    "트레일링 스탑(Trailing Stop) 걸고 진입! 🛡️"
                ]
            else:
                logic_1 = [
                    f"으악! <b>[VPIN {m['vpin']:.2f}]</b> 경고등 켜졌어! 기관 형들이 폭탄 던진다! 💣",
                    f"<b>[ES(꼬리위험)]</b> 수치가 최악이야... 이거 건드리면 계좌 녹아! 🫠",
                    f"차트가 무너졌어... <b>[Betti Number]</b> 위상 구조가 깨졌다구! 📉"
                ]
                logic_2 = [
                    "지금 들어가면 한강 물 온도 체크하러 가야 돼...",
                    "이건 용기가 아니라 만용이야! 절대 안 돼!",
                    "돔황챠!!! 🏃‍♂️💨 뒤도 돌아보지 마!"
                ]
                act = [
                    "관심 종목 삭제! ❌ 쳐다도 보지 마!",
                    "보유 중이면 당장 시장가 매도! 📉 탈출이 지능순이야!",
                    "현금 꽉 쥐고 숨어있어! 🫣 소나기는 피해야지!"
                ]
            
            return f"{random.choice(intros)} {random.choice(logic_1)} {random.choice(logic_2)}", random.choice(act)

        # 🐯 HOJJI (Conservative, Fundamental, Old-school)
        else: 
            intros = ["허허,", "음...", "에잉 쯧쯧,", "자네,", "어허!"]
            
            if wr >= 0.75:
                logic_1 = [
                    f"<b>[내재가치]</b> 대비 저평가 구간이군. <b>[GNN]</b>상 주도주 지위도 확고해. 🏯",
                    f"수급과 펀더멘털이 '금상첨화(錦上添花)'로구나. <b>[안전마진]</b>이 충분해.",
                    f"<b>[Hurst]</b> 지수가 견고해. 추세가 쉽게 꺾이지 않을 기세야. 🌊"
                ]
                logic_2 = [
                    "이런 종목은 진득하게 묻어두면 효자 노릇을 할 게야.",
                    "물 들어올 때 노 저어야지. 과감한 결단이 필요할 때일세.",
                    "오랜만에 제대로 된 물건을 보았구먼."
                ]
                act = [
                    "비중을 실어보게. 단, 분할 매수는 잊지 말고. ⚖️",
                    "목표가까지 '우보천리(牛步千里)'의 마음으로 동행하게. 🐂",
                    "지금 진입해서 연말까지 묻어두게. 📅"
                ]
            elif wr >= 0.55:
                logic_1 = [
                    f"계륵(鷄肋)일세. 좋아 보이나 <b>[변동성(Vol)]</b>이 너무 심해. 🌊",
                    f"상승 여력은 있으나 <b>[꼬리 위험(ES)]</b>이 도사리고 있어. 살얼음판이야. ❄️",
                    f"기술적 반등 구간이나, <b>[펀더멘털]</b> 확신이 부족해. 🤔"
                ]
                logic_2 = [
                    "돌다리도 두들겨 보고 건너라 했네. 신중하게 접근하게.",
                    "욕심 부리다 체할 수 있어. '과유불급'을 명심하게.",
                    "방망이를 짧게 잡고 대응하는 게 상책이야."
                ]
                act = [
                    "전체 시드의 10%만 재미로 담아보게. 🧪",
                    "철저히 분할 매수로 접근하고, 아니면 바로 자르게. ✂️",
                    "관망하다가 지지선 확인 후 들어가는 게 '만수무강'의 길일세. 🐢"
                ]
            else:
                logic_1 = [
                    f"사상누각(砂上樓閣)이야! <b>[독성 매물(VPIN)]</b>이 쏟아지는데 어찌 버티겠나! 🏚️",
                    f"기초 체력이 부실해. <b>[Going Concern]</b> 이슈가 불거질 수 있어. ⚠️",
                    f"떨어지는 칼날일세. <b>[Role Reversal]</b> 저항이 너무 강해. ⚔️"
                ]
                logic_2 = [
                    "지금 들어가는 건 불나방이나 다름없어. 타 죽고 싶은가?",
                    "수업료 내기 싫으면 HTS 끄고 산책이나 다녀오게.",
                    "돈을 허공에 뿌릴 셈인가? 정신 차리게!"
                ]
                act = [
                    "쳐다도 보지 말게. 현금이 곧 종목이야. 🛡️",
                    "당장 매도하고 우량주로 갈아타게. 🔄",
                    "절대 매수 금지. 내 말 명심하게. ⛔"
                ]

            return f"{random.choice(intros)} {random.choice(logic_1)} {random.choice(logic_2)}", random.choice(act)

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        if mode == "scalping":
            vol = m['vol_surf'] * 0.04
            entry = int(price * (1 - vol)); target = int(price * (1 + vol*1.5)); stop = int(price * (1 - vol*0.7))
        else:
            entry = price; target = int(price * (1 + target_return/100)); stop = int(price * 0.93)

        h_an, h_act = self._generate_text('hamzzi', wr, m)
        t_an, t_act = self._generate_text('hojji', wr, m)

        # Why Text (Logical Rationale)
        h_why = f"<b>[Vol Surface]</b>가 {m['vol_surf']:.2f}로 변동성이 살아있고, <b>[Hawkes]</b> 모멘텀이 {m['hawkes']:.2f}로 수급이 붙어주니까 단기 슈팅 가능성 매우 높음!"
        t_why = f"<b>[GNN]</b> 중심성이 {m['gnn']:.2f}이나, <b>[VPIN]</b> {m['vpin']:.2f}를 고려할 때 리스크 대비 기대수익률(Risk-Reward Ratio)을 철저히 계산해야 함."

        return {
            "prices": (entry, target, stop),
            "hamzzi": {"brief": h_an, "act": h_act, "why": h_why, "style": "border: 2px solid #FFAA00; color: #FFAA00;"},
            "hojji": {"brief": t_an, "act": t_act, "why": t_why, "style": "border: 2px solid #FF4444; color: #FF4444;"}
        }

    # [PORTFOLIO DEEP DIAGNOSIS & REBALANCING]
    def diagnose_portfolio(self, portfolio, cash):
        asset_val = sum([s['price'] * s['qty'] for s in portfolio])
        total_val = asset_val + cash
        cash_ratio = (cash / total_val * 100) if total_val > 0 else 100
        
        # Metrics Simulation
        beta = np.random.uniform(0.5, 2.0)
        sharpe = np.random.uniform(0.5, 3.0)
        mdd = np.random.uniform(-5.0, -35.0)
        corr = np.random.uniform(0.1, 0.9) # Correlation
        
        # HAMZZI (Rebalancing for Aggression)
        h_rebal = ""
        if cash_ratio > 50:
            h_rebal = "👉 <b>[리밸런싱]</b>: 현금 30%를 당장 <b>[TQQQ]</b>나 <b>[코스닥 레버리지]</b>에 태워! 현금은 쓰레기야!"
        elif beta < 1.0:
            h_rebal = "👉 <b>[리밸런싱]</b>: 변동성 없는 노잼 주식(Beta < 0.5) 다 팔고, <b>[주도 섹터]</b> 대장주로 교체 매매 고고!"
        else:
            h_rebal = "👉 <b>[유지]</b>: 아주 좋아! 이대로 <b>[불타기]</b> 하면서 수익 극대화하자!"

        h_msg = f"""
        <div style='margin-bottom:8px;'>사장님! 포트폴리오 <b>[Beta]</b>가 {beta:.2f}야! { "🔥 야수 인정!" if beta > 1.2 else "🐢 너무 굼벵이야!" }</div>
        <div style='margin-bottom:8px;'><b>[Sharpe Ratio]</b>는 {sharpe:.2f}로 가성비 { "찢었다!" if sharpe > 1.5 else "나쁘지 않아." }</div>
        <div style='background:#332200; padding:8px; border-radius:5px; margin-top:5px;'>{h_rebal}</div>
        """

        # HOJJI (Rebalancing for Safety)
        t_rebal = ""
        if cash_ratio < 20:
            t_rebal = "👉 <b>[리밸런싱]</b>: 위험해! 수익 난 종목 50% 차익 실현해서 <b>[현금]</b>을 최소 30%까지 확보하게."
        elif mdd < -20:
            t_rebal = "👉 <b>[리밸런싱]</b>: <b>[MDD]</b>가 너무 깊어. 잡주들은 손절하고 <b>[배당주]</b>나 <b>[국채]</b>를 편입해서 변동성을 줄여."
        elif corr > 0.7:
            t_rebal = "👉 <b>[리밸런싱]</b>: 종목들이 다 같이 움직여(상관계수 High). 섹터가 겹치니 일부는 정리해서 <b>[분산 투자]</b> 하게."
        else:
            t_rebal = "👉 <b>[유지]</b>: 자산 배분이 적절하군. 이대로 <b>[바이 앤 홀드]</b> 전략을 유지하게."

        t_msg = f"""
        <div style='margin-bottom:8px;'>자네 계좌의 <b>[MDD]</b>가 {mdd:.1f}%일세. { "잠은 오나?" if mdd < -20 else "관리는 잘 했구먼." }</div>
        <div style='margin-bottom:8px;'>종목 간 <b>[상관계수]</b>가 {corr:.2f}로 { "위험 분산이 안 됐어." if corr > 0.7 else "적절히 분산됐군." }</div>
        <div style='background:#330000; padding:8px; border-radius:5px; margin-top:5px;'>{t_rebal}</div>
        """

        return h_msg, t_msg

    def explain_terms(self):
        return {
            "hamzzi": """
            <div style='font-size:13px; line-height:1.6; color:#eee;'>
            <b>🐹 햄찌의 족집게 과외:</b><br>
            • <b>Hawkes (호크스):</b> 인기 폭발 지수! 높으면 사람들이 "와!" 하고 몰려드는 거야! 🎉<br>
            • <b>Vol Surface (볼 서페이스):</b> 파도 높이! 높으면 서핑 꿀잼(수익)이지만 물 먹을 수도 있어! 🌊<br>
            • <b>Hurst (허스트):</b> 황소 고집! 한 번 가던 방향으로 계속 가려는 성질이야! 💪<br>
            • <b>Beta (베타):</b> 시장 형님이 1만큼 움직일 때 내껀 얼마나 춤추느냐! 높으면 화끈하지! 🔥
            </div>
            """,
            "hojji": """
            <div style='font-size:13px; line-height:1.6; color:#eee;'>
            <b>🐯 호찌의 훈장님 해설:</b><br>
            • <b>VPIN (독성 유동성):</b> 정보 우위를 가진 기관의 기습적 매도 물량일세. 조심하게.<br>
            • <b>GNN (그래프 신경망):</b> 이 종목이 시장 생태계에서 얼마나 중요한 '대장'인지 보여주지.<br>
            • <b>Sharpe Ratio:</b> 위험 한 단위당 얼마나 알짜배기 수익을 냈느냐는 '가성비' 지표야.<br>
            • <b>MDD (최대낙폭):</b> 고점에서 얼마나 처박혔느냐... 자네 멘탈이 버틸 수 있는 한계선이지.
            </div>
            """
        }

    def hamzzi_nagging(self):
        t = random.choice(["🐹 햄찌의 잔소리", "🐹 햄찌의 긴급 타전", "🐹 햄찌의 꿀팁"])
        m = random.choice([
            "차트가 말을 거는데 왜 대답을 안 해? 📞 당장 매수 버튼 눌러!",
            "인생은 타이밍이야! 지금이 바로 그 타이밍이라구! ⏰",
            "쫄지마! 쫄면 지는 거야! 야수의 심장으로 풀매수! 🔥"
        ])
        return t, m

    def hojji_nagging(self):
        t = random.choice(["🐯 호찌의 호통", "🐯 호찌의 훈계", "🐯 호찌의 명언"])
        m = random.choice([
            "공부 안 하고 사는 건 투기야! 재무제표는 읽어봤나? 📚",
            "급할수록 돌아가라 했어. 현금도 소중한 종목임을 잊지 말게. 🛡️",
            "일희일비하지 마. 주식은 머리가 아니라 엉덩이로 버티는 걸세. 🧘‍♂️"
        ])
        return t, m

# -----------------------------------------------------------------------------
# [2] UI & RENDERERS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    .app-title { text-align: center; font-size: 36px; font-weight: 900; color: #fff; padding: 30px 0; text-shadow: 0 0 20px rgba(0,201,255,0.8); }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div { background-color: #1a1f26 !important; color: #fff !important; border: 1px solid #444 !important; border-radius: 8px; }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: 800; height: 50px; background: linear-gradient(135deg, #00C9FF, #92FE9D); border: none; color: #000; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); }
    .stock-card { background: #111; border-radius: 16px; padding: 0; margin-bottom: 30px; border: 1px solid #333; box-shadow: 0 4px 20px rgba(0,0,0,0.5); overflow: hidden; }
    .card-header { padding: 15px 20px; background: #1e1e1e; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center; }
    .stock-name { font-size: 24px; font-weight: bold; color: #fff; }
    .win-rate { font-size: 14px; font-weight: bold; padding: 5px 12px; border-radius: 20px; background: #222; }
    .persona-box { padding: 20px; font-size: 14px; line-height: 1.6; color: #eee; }
    .persona-title { font-weight: bold; margin-bottom: 12px; font-size: 16px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; }
    .port-dash { background: #1a1a1a; padding: 20px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #444; }
    .tag { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 11px; margin-right: 5px; font-weight: bold; color: #000; }
    .tag-base { background: #888; } .tag-best { background: #00FF00; } .tag-good { background: #00C9FF; } .tag-bad { background: #FF4444; color: #fff; }
    .timeline { display: flex; justify-content: space-between; background: #000; padding: 15px 25px; border-top: 1px solid #333; }
    .t-item { text-align: center; } .t-val { font-weight: bold; font-size: 15px; margin-top: 4px; display: block;}
    .rank-ribbon { position: absolute; top: 0; left: 0; padding: 5px 12px; font-size: 12px; font-weight: bold; color: #fff; background: linear-gradient(45deg, #FF416C, #FF4B2B); border-bottom-right-radius: 12px; z-index: 5; }
    .prog-bg { background: #333; height: 8px; border-radius: 4px; width: 100%; }
    .prog-fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
    .hud-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 10px; background: #0d1117; padding: 10px; border-radius: 8px; }
    .hud-item { background: #21262d; padding: 8px; border-radius: 6px; text-align: center; border: 1px solid #30363d; }
    .hud-label { font-size: 10px; color: #8b949e; display: block; margin-bottom: 2px; }
    .hud-val { font-size: 13px; color: #58a6ff; font-weight: bold; }
    .hamzzi-box { background: linear-gradient(135deg, #2c241b, #1a1510); border: 2px solid #FFAA00; border-radius: 16px; padding: 20px; color: #eee; margin-bottom: 15px; }
    .hojji-box { background: linear-gradient(135deg, #3d0000, #1a0000); border: 2px solid #FF4444; border-radius: 16px; padding: 20px; color: #eee; margin-bottom: 15px; }
    div[data-testid="column"]:nth-child(5) { margin-left: -20px !important; margin-top: 2px; }
    header, footer {visibility: hidden;}
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
if 'market_view_mode' not in st.session_state: st.session_state.market_view_mode = None
# Timers & Triggers
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
    
    # Portfolio Deep Diagnosis (Text Generation)
    h_port, t_port = engine.diagnose_portfolio(st.session_state.portfolio, st.session_state.cash)
    st.session_state.port_analysis = {'hamzzi': h_port, 'hojji': t_port}
    
    with st.spinner("내 포트폴리오 정밀 해부 및 리밸런싱 전략 수립 중..."):
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
            # Generate Rich HTML Text Plan
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

# [RENDER CARD FUNCTION - HTML ONLY]
def render_full_card(d, idx=None, is_rank=False):
    engine = SingularityEngine()
    p = d['plan']
    
    tag_html = "".join([f"<span class='tag tag-{t['type']}'>{t['label']} {t['val']}</span> " for t in d['tags']])
    win_pct = d['win'] * 100
    color = "#00FF00" if d['win'] >= 0.75 else "#FFAA00" if d['win'] >= 0.55 else "#FF4444"
    bar_html = f"<div style='background:#333; height:6px; border-radius:3px; margin-top:5px;'><div style='width:{win_pct}%; background:{color}; height:100%; border-radius:3px;'></div></div>"
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

    t1, t2, t3 = st.tabs(["🐹 햄찌의 분석", "🐯 호찌의 분석", "📚 용어 해설"])
    
    with t1:
        h = p['hamzzi']
        st.markdown(f"""
        <div class='persona-box' style='{h['style']}'>
            <div class='persona-title'>🐹 햄찌의 야수 본능 (인생 한방! 🔥)</div>
            <div style='margin-bottom:10px;'>{h['brief']}</div>
            <div style='background:#222; padding:10px; border-radius:8px; margin-bottom:10px;'><b>💡 행동 지침:</b> {h['act']}</div>
            <div style='font-size:13px; color:#aaa; margin-top:10px;'><b>🎯 논리적 근거:</b> {h['why']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with t2:
        t = p['hojji']
        st.markdown(f"""
        <div class='persona-box' style='{t['style']}'>
            <div class='persona-title'>🐯 호찌의 유비무환(有備無患) 정신 🛡️</div>
            <div style='margin-bottom:10px;'>{t['brief']}</div>
            <div style='background:#222; padding:10px; border-radius:8px; margin-bottom:10px;'><b>💡 어르신 말씀:</b> {t['act']}</div>
            <div style='font-size:13px; color:#aaa; margin-top:10px;'><b>🎯 논리적 근거:</b> {t['why']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with t3:
        terms = engine.explain_terms()
        st.markdown(terms['hamzzi'], unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#333; margin:10px 0;'>", unsafe_allow_html=True)
        st.markdown(terms['hojji'], unsafe_allow_html=True)

    st.markdown(f"""
    <div class='stock-card' style='margin-top:-20px; border-top:none; border-radius:0 0 16px 16px;'>
        <div class='timeline'>
            <div class='t-item'><span style='color:#888; font-size:12px;'>진입/추매</span><br><span class='t-val' style='color:#00C9FF'>{p['prices'][0]:,}</span></div>
            <div class='t-item'><span style='color:#888; font-size:12px;'>목표가</span><br><span class='t-val' style='color:#00FF00'>{p['prices'][1]:,}</span></div>
            <div class='t-item'><span style='color:#888; font-size:12px;'>손절가</span><br><span class='t-val' style='color:#FF4444'>{p['prices'][2]:,}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander(f"🔍 {d['name']} - 8대 엔진 HUD (전문가용)"):
        m = d['m']
        st.markdown(f"""
        <div class='hud-grid'>
            <div class='hud-item'><span class='hud-label'>JLS 파동</span><span class='hud-val'>{m['omega']:.1f}</span></div>
            <div class='hud-item'><span class='hud-label'>독성(VPIN)</span><span class='hud-val'>{m['vpin']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>수급(Hawkes)</span><span class='hud-val'>{m['hawkes']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>호가(OBI)</span><span class='hud-val'>{m['obi']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>추세(Hurst)</span><span class='hud-val'>{m['hurst']:.2f}</span></div>
            <div class='hud-item'><span class='hud-label'>켈리비중</span><span class='hud-val'>{m['kelly']:.2f}</span></div>
        </div>
        """, unsafe_allow_html=True)

# [ADVISORS]
st.markdown("<br>", unsafe_allow_html=True)
bc1, bc2 = st.columns(2)
with bc1:
    if st.button("🐹 햄찌의 앙큼상큼 팩트폭격 뀨? ❤️", use_container_width=True):
        engine = SingularityEngine()
        title, msg = engine.hamzzi_nagging()
        st.session_state.adv_msg = f"<div class='hamzzi-box'><div class='hamzzi-title'>{title}</div>{msg}</div>"
with bc2:
    if st.button("🐯 호찌의 유비무환(有備無患) 대호통", use_container_width=True):
        engine = SingularityEngine()
        title, msg = engine.hojji_nagging()
        st.session_state.adv_msg = f"<div class='hojji-box'><div class='tiger-title'>{title}</div>{msg}</div>"
        
if 'adv_msg' in st.session_state: st.markdown(st.session_state.adv_msg, unsafe_allow_html=True)

# [MY DIAGNOSIS & PORTFOLIO HEALTH]
if st.session_state.my_diagnosis:
    st.markdown("---")
    if 'port_analysis' in st.session_state:
        pa = st.session_state.port_analysis
        st.markdown(f"""
        <div class='port-dash'>
            <div style='font-size:18px; font-weight:bold; color:#fff; margin-bottom:15px;'>📊 포트폴리오 종합 진단 (Conflict Engine)</div>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:15px;'>
                <div style='background:#222; padding:15px; border-radius:8px; border:1px solid #FFAA00;'>
                    <div style='color:#FFAA00; font-weight:bold; margin-bottom:5px;'>🐹 햄찌의 야수 본능 (인생 한방! 🔥)</div>
                    <div style='font-size:13px; color:#ddd; line-height:1.5;'>{pa['hamzzi']}</div>
                </div>
                <div style='background:#222; padding:15px; border-radius:8px; border:1px solid #FF4444;'>
                    <div style='color:#FF4444; font-weight:bold; margin-bottom:5px;'>🐯 호찌의 유비무환(有備無患) 정신 🛡️</div>
                    <div style='font-size:13px; color:#ddd; line-height:1.5;'>{pa['hojji']}</div>
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
