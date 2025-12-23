import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr
import random
import textwrap

# -----------------------------------------------------------------------------
# [0] GLOBAL SETTINGS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

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
    except: return ["삼성전자", "SK하이닉스", "LG에너지솔루션", "NAVER", "카카오"]

@st.cache_data(ttl=3600)
def load_top50_data():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df.sort_values(by='Marcap', ascending=False).head(50)
    except: return pd.DataFrame()

# -----------------------------------------------------------------------------
# [1] CORE ENGINE CLASS
# -----------------------------------------------------------------------------
class SingularityEngine:
    def __init__(self):
        pass

    def _calculate_metrics(self, name, mode):
        # 데이터 일관성: 종목명+시간(시) 기준 시드 고정
        unique_key = f"{name}-{mode}-{time.strftime('%Y%m%d-%H')}"
        seed_val = zlib.crc32(unique_key.encode())
        np.random.seed(seed_val)
        
        m = {
            "omega": np.random.uniform(5.0, 25.0), "vol_surf": np.random.uniform(0.1, 0.9),
            "betti": np.random.choice([0, 1], p=[0.85, 0.15]), "hurst": np.random.uniform(0.2, 0.99),
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

        if m['vpin'] > 0.6: score -= 15; tags.append({'label': '독성 매물(VPIN)', 'val': '-15', 'type': 'bad'})
        if m['es'] < -0.15: score -= 15; tags.append({'label': 'Tail Risk(ES)', 'val': '-15', 'type': 'bad'})
        if m['betti'] == 1: score -= 10; tags.append({'label': '위상 붕괴(Betti)', 'val': '-10', 'type': 'bad'})
        
        if mode == "scalping":
            if m['hawkes'] > 2.5: score += 40; tags.append({'label': '🚀 Hawkes 폭발', 'val': '+40', 'type': 'best'})
            elif m['hawkes'] > 1.5: score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'type': 'good'})
        else: 
            if m['hurst'] > 0.75: score += 35; tags.append({'label': '📈 Hurst 추세장', 'val': '+35', 'type': 'best'})
            elif m['hurst'] > 0.6: score += 10; tags.append({'label': '↗️ 추세 양호', 'val': '+10', 'type': 'good'})

        win_rate = min(0.92, max(0.15, score / 100))
        return win_rate, m, tags

    # [PERSONA REPORT GENERATOR]
    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        volatility = m['vol_surf'] * 0.05
        if mode == "scalping":
            target = int(price * (1 + max(volatility, 0.02)))
            stop = int(price * (1 - volatility * 0.5))
        else:
            target = int(price * (1 + (target_return/100)))
            stop = int(price * 0.93)

        can_buy = int((cash * m['kelly']) / price) if price > 0 else 0

        # --- 1. 🐹 HAMZZI (Aggressive) ---
        h_res = {}
        h_res['style'] = "border: 2px solid #FFAA00; color: #FFAA00;"
        
        if wr >= 0.70:
            h_res['title'] = "🐹 햄찌: \"인생은 한방! 지금이 기회야!\" 🔥"
            h_res['brief'] = random.choice([
                f"사장님! <b>[Hawkes {m['hawkes']:.2f}]</b> 수치 봤어?! 수급이 미친 듯이 들어온다구! 🚀",
                f"대박! <b>[GNN 중심성]</b> 폭발! 돈이 다 여기로 몰린다구! 💰"
            ])
            h_res['action'] = f"쫄지마! <b>{can_buy}주</b> 시장가 매수! <b>{target:,}원</b> 뚫으면 불타기!"
            h_res['why'] = f"변동성(Vol: {m['vol_surf']:.2f})이 살아있어. 베타(Beta)를 먹으려면 지금 위험을 감수해야 해!"
        elif wr >= 0.50:
            h_res['title'] = "🐹 햄찌: \"간 좀 볼까? 단타 치기 딱 좋아!\" ⚡"
            h_res['brief'] = f"음~ <b>[Hurst {m['hurst']:.2f}]</b> 추세가 살아있네! 단타 놀이터로 딱이야. 🎢"
            h_res['action'] = f"일단 <b>{int(can_buy/2)}주</b>만 정찰병 보내고, <b>{price:,}원</b> 지지하면 나머지 태워!"
            h_res['why'] = "모멘텀은 좋은데 <b>[OBI]</b> 눈치 싸움 중이야. 짧게 먹고 나오자!"
        else:
            h_res['title'] = "🐹 햄찌: \"으악! 돔황챠!! 폭탄이야!\" 💣"
            h_res['brief'] = f"으악! <b>[VPIN {m['vpin']:.2f}]</b> 경고등 켜졌어! 폭탄 돌리기 중이야! 💣"
            h_res['action'] = "절대 매수 금지! ❌ 탈출은 지능순이야! 현금 쥐고 숨어!"
            h_res['why'] = "독성 매물이 쏟아지고 있어. 지금 들어가면 계좌 녹는다."

        # --- 2. 🐯 HOJJI (Conservative) ---
        t_res = {}
        t_res['style'] = "border: 2px solid #FF4444; color: #FF4444;"
        
        if wr >= 0.70:
            t_res['title'] = "🐯 호찌: \"허허, 진국일세. 기회를 잡게.\" 🍵"
            t_res['brief'] = f"허허, <b>[내재가치]</b> 대비 저평가로군. 수급과 펀더멘털이 '금상첨화'야. 🍵"
            t_res['action'] = f"안전마진이 확보됐네. <b>{int(can_buy*0.8)}주</b> 정도 비중을 실어서 진득하게 동행하게."
            t_res['why'] = f"<b>[Omega 파동]</b>이 {m['omega']:.1f}로 안정적이야. 발 뻗고 잘 수 있는 자리일세."
        elif wr >= 0.50:
            t_res['title'] = "🐯 호찌: \"계륵일세. 돌다리도 두들겨 보게.\" 🐅"
            t_res['brief'] = f"계륵일세. 🐅 <b>[변동성 {m['vol_surf']:.2f}]</b>이 너무 심해. '내우외환'이 걱정되는군."
            t_res['action'] = f"욕심 버리고 <b>{int(can_buy*0.2)}주</b>만 분할로 담게. '유비무환'의 자세가 필요해."
            t_res['why'] = "상승 여력은 있으나 <b>[꼬리 위험(ES)]</b>이 도사리고 있어. 돌다리도 두들겨 보게."
        else:
            t_res['title'] = "🐯 호찌: \"어허! 사상누각이야!\" 🏚️"
            t_res['brief'] = f"에잉 쯧쯧! 😡 <b>[독성 매물]</b>이 넘쳐나는구먼! 사상누각이야!"
            t_res['action'] = "쳐다도 보지 말게. 현금이 곧 최고의 종목이야. 🛡️"
            t_res['why'] = "스마트 머니는 이미 떠났어. 떨어지는 칼날을 맨손으로 잡으려 하지 말게."

        return {
            "prices": (price, target, stop),
            "hamzzi": h_res,
            "hojji": t_res
        }

    def diagnose_portfolio(self, portfolio, cash, target_return):
        asset_val = sum([s['price'] * s['qty'] for s in portfolio])
        total_val = asset_val + cash
        cash_ratio = (cash / total_val * 100) if total_val > 0 else 100
        stock_count = len(portfolio)
        
        # Simulating Portfolio Metrics
        beta = np.random.uniform(0.5, 2.0)
        sharpe = np.random.uniform(0.5, 3.0)
        mdd = np.random.uniform(-5.0, -35.0)
        corr = np.random.uniform(0.1, 0.9)
        
        # 🐹 HAMZZI (Aggressive View)
        h_msg = ""
        if cash_ratio > 60:
            h_msg += f"사장님! 현금 <b>{cash_ratio:.1f}%</b> 실화야? 😱 <b>[Cash Drag]</b> 때문에 수익률 갉아먹고 있어!<br>"
        if beta < 0.8:
            h_msg += f"포트폴리오가 너무 얌전해(Beta {beta:.2f})... 🐢 재미없어! <b>[레버리지]</b> 좀 섞어서 화끈하게 가보자구!"
        else:
            h_msg += f"오! <b>[Beta {beta:.2f}]</b> 아주 훌륭해! 🐹 이대로 <b>[불타기]</b> 하면서 수익 극대화하자! 🚀"

        # 🐯 HOJJI (Conservative View)
        t_msg = ""
        if cash_ratio < 15:
            t_msg += f"자네 현금이 <b>{cash_ratio:.1f}%</b>뿐인가? 😡 하락장 오면 <b>[MDD {mdd:.1f}%]</b> 맞고 깡통 찰 텐가? '유비무환'을 잊지 말게!<br>"
        if mdd < -20:
            t_msg += f"리스크 관리가 엉망이야. 변동성 큰 잡주는 정리하고 <b>[배당주]</b>나 <b>[채권]</b> 비중을 늘려 방어벽을 세우게."
        else:
            t_msg += f"음, <b>[Sharpe Ratio]</b> {sharpe:.2f}로 관리는 되고 있군. 허나 방심은 금물이야. <b>[펀더멘털]</b>을 수시로 체크하게."

        return h_msg, t_msg

    def explain_terms(self):
        return {
            "hamzzi": """
            <div style='font-size:13px; line-height:1.6; color:#eee;'>
            <b>🐹 햄찌의 족집게 과외:</b><br>
            • <b>Hawkes (호크스):</b> 인기 폭발 지수! 2.0 넘으면 사람들 우르르 몰려오는 거야! 🎉<br>
            • <b>Vol Surface (볼 서페이스):</b> 파도 높이! 높으면 서핑 꿀잼(수익)이지만 물 먹을 수도 있어! 🌊<br>
            • <b>Hurst (허스트):</b> 황소 고집! 한 번 가던 방향으로 계속 가려는 성질이야! 💪<br>
            • <b>Beta (베타):</b> 시장 형님이 1만큼 움직일 때 내껀 얼마나 춤추느냐! 높으면 화끈하지! 🔥
            </div>
            """,
            "hojji": """
            <div style='font-size:13px; line-height:1.6; color:#eee;'>
            <b>🐯 호찌의 훈장님 해설:</b><br>
            • <b>VPIN (독성 유동성):</b> 기관들이 정보 우위를 이용해 개미에게 물량을 넘기는 수치일세.<br>
            • <b>GNN (그래프 신경망):</b> 이 종목이 시장 생태계에서 얼마나 중요한 '대장'인지 보여주지.<br>
            • <b>Sharpe Ratio:</b> 위험 한 단위당 얼마나 알짜배기 수익을 냈느냐는 '가성비' 지표야.<br>
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
# [2] IMAGE OCR (Mock for Demo)
# -----------------------------------------------------------------------------
def parse_image_portfolio(uploaded_file):
    with st.spinner("🔄 [Singularity Omega] OCR 이미지 정밀 분석 중..."):
        time.sleep(1.5)
    st.toast("✅ 이미지 스캔 완료! 데이터를 불러왔습니다.", icon="📸")
    return [
        {'name': '두산에너빌리티', 'price': 17500, 'qty': 100, 'strategy': '추세추종'},
        {'name': 'SK하이닉스', 'price': 135000, 'qty': 10, 'strategy': '추세추종'},
        {'name': '카카오', 'price': 55000, 'qty': 30, 'strategy': '초단타'}
    ]

# -----------------------------------------------------------------------------
# [3] UI STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    .app-title { text-align: center; font-size: 36px; font-weight: 900; color: #fff; padding: 30px 0; text-shadow: 0 0 20px rgba(0,201,255,0.8); }
    
    /* Inputs Labels (Visible) */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        font-size: 13px !important; font-weight: bold !important; color: #bbb !important;
        display: block !important; margin-bottom: 2px !important;
    }
    
    /* Card Styles */
    .stock-card { background: #111; border-radius: 16px; padding: 0; margin-bottom: 30px; border: 1px solid #333; box-shadow: 0 4px 20px rgba(0,0,0,0.5); overflow: hidden; }
    .card-header { padding: 15px 20px; background: #1e1e1e; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center; }
    .stock-name { font-size: 24px; font-weight: bold; color: #fff; }
    .stock-score { font-size: 14px; font-weight: bold; background: #333; padding: 5px 12px; border-radius: 20px; color: #fff; border: 1px solid #555; }
    
    .tag-container { padding: 15px 20px 5px 20px; display: flex; flex-wrap: wrap; gap: 8px; }
    .tag { font-size: 12px; font-weight: bold; padding: 4px 10px; border-radius: 6px; color: #000; display: inline-block; }
    
    .info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: #333; margin: 15px 20px; border: 1px solid #333; }
    .info-item { background: #121212; padding: 10px; text-align: center; }
    .info-label { font-size: 11px; color: #888; display: block; margin-bottom: 3px; }
    .info-val { font-size: 15px; font-weight: bold; color: #fff; }
    
    .persona-box { padding: 20px; font-size: 14px; line-height: 1.6; color: #eee; }
    .persona-title { font-weight: bold; margin-bottom: 12px; font-size: 16px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; }
    
    .port-dash { background: #1a1a1a; padding: 20px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #444; }
    
    .timeline { display: flex; justify-content: space-between; background: #000; padding: 15px 25px; border-top: 1px solid #333; }
    .t-item { text-align: center; } .t-val { font-weight: bold; font-size: 15px; margin-top: 4px; display: block; }
    
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
    
    h_port, t_port = engine.diagnose_portfolio(st.session_state.portfolio, st.session_state.cash, st.session_state.target_return)
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

# [UI: PORTFOLIO SETTINGS & IMAGE UPLOAD]
with st.expander("💰 내 자산 및 포트폴리오 설정", expanded=True):
    # Image Uploader
    st.markdown("#### 📸 포트폴리오 이미지 스캔 (OCR)")
    uploaded_file = st.file_uploader("계좌 캡처 이미지를 업로드하세요", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    if uploaded_file is not None:
        scanned_portfolio = parse_image_portfolio(uploaded_file)
        if scanned_portfolio:
            st.session_state.portfolio = scanned_portfolio
            st.success(f"이미지 인식 성공! {len(scanned_portfolio)}개 종목을 불러왔습니다.")

    st.markdown("---")
    
    # Manual Input Section
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.caption("**예수금 (KRW)**")
        st.session_state.cash = st.number_input("cash_input", value=st.session_state.cash, step=100000, label_visibility="collapsed")
    with c2: 
        st.caption("**목표 수익률 (%)**")
        st.session_state.target_return = st.number_input("target_input", value=st.session_state.target_return, step=1.0, label_visibility="collapsed")
    with c3:
        st.caption("**종목 추가**")
        if st.button("➕ 종목 추가", use_container_width=True):
            st.session_state.portfolio.append({'name': '삼성전자', 'price': 0, 'qty': 0, 'strategy': '추세추종'})
            st.rerun()
    
    st.markdown("---")
    
    # Portfolio Inputs with explicit labels
    if st.session_state.portfolio:
        for i, s in enumerate(st.session_state.portfolio):
            c1, c2, c3, c4, c5 = st.columns([3, 2, 1.5, 2, 0.5])
            with c1: 
                st.caption(f"**종목명 {i+1}**")
                try: idx = stock_names.index(s['name'])
                except: idx = 0
                s['name'] = st.selectbox(f"name_{i}", stock_names, index=idx, label_visibility="collapsed")
            with c2: 
                st.caption("**평단가**")
                s['price'] = st.number_input(f"price_{i}", value=float(s['price']), label_visibility="collapsed")
            with c3: 
                st.caption("**수량**")
                s['qty'] = st.number_input(f"qty_{i}", value=int(s['qty']), label_visibility="collapsed")
            with c4: 
                st.caption("**전략**")
                s['strategy'] = st.selectbox(f"strat_{i}", ["추세추종", "초단타"], index=0 if s['strategy']=="추세추종" else 1, label_visibility="collapsed")
            with c5: 
                st.caption("**삭제**")
                if st.button("🗑️", key=f"del_{i}"): 
                    st.session_state.portfolio.pop(i)
                    st.rerun()
    else:
        st.info("보유 종목이 없습니다. 이미지를 업로드하거나 '➕ 종목 추가' 버튼을 눌러주세요.")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    
    # ACTIONS
    col_btn, col_timer = st.columns([2, 1])
    with col_btn:
        if st.button("📝 내 종목 및 포트폴리오 정밀 진단", use_container_width=True):
            st.session_state.trigger_my = True
            st.rerun()
    with col_timer:
        auto_my = st.selectbox("자동진단", list(TIME_OPTS.keys()), index=0, label_visibility="collapsed")

    # ADVISORS
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

# [DISPLAY MY DIAGNOSIS RESULT]
def render_full_card(d, idx=None, is_rank=False):
    engine = SingularityEngine()
    p = d['plan']
    
    win_pct = d['win'] * 100
    color = "#00FF00" if d['win'] >= 0.7 else "#FFAA00" if d['win'] >= 0.5 else "#FF4444"
    rank_html = f"<div class='rank-ribbon'>{idx+1}위</div>" if is_rank else ""
    
    tag_html = ""
    for t in d['tags']:
        t_color = "#00FF00" if t['type'] == 'best' else "#00C9FF" if t['type'] == 'good' else "#FF4444"
        tag_html += f"<span class='tag' style='color:{t_color}; border:1px solid {t_color};'>{t['label']} {t['val']}</span>"

    # [CRITICAL FIX] Use textwrap.dedent to prevent HTML code exposure
    st.markdown(textwrap.dedent(f"""
    <div class='stock-card'>
        {rank_html}
        <div class='card-header' style='padding-left:{50 if is_rank else 0}px'>
            <div>
                <span class='stock-name'>{d['name']}</span>
                <span style='color:#ccc; font-size:14px; margin-left:10px;'>{d.get('mode','')}</span>
            </div>
            <div class='stock-score' style='color:{color}; border-color:{color};'>AI Score {win_pct:.1f}</div>
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

if st.session_state.my_diagnosis:
    st.markdown("---")
    
    # 1. Portfolio Health
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
                    <div style='font-size:13px; color:#ddd; line-height:1.5;'>{pa['hojji']}</div>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

    st.subheader("👤 보유 종목 상세 분석")
    for d in st.session_state.my_diagnosis:
        render_full_card(d)

# [MARKET SCAN SECTION]
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

# [DISPLAY MARKET RESULT]
if st.session_state.market_view_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("<h5>🏆 금일의 Singularity Ideal Pick (Top 3)</h5>", unsafe_allow_html=True)
    for i, d in enumerate(st.session_state.ideal_list):
        render_full_card(d, i, is_rank=True)

elif st.session_state.market_view_mode == 'SEPARATE' and st.session_state.sc_list:
    st.markdown("<h5>📊 전략별 절대 랭킹 (Top 3)</h5>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["⚡ 초단타", "🌊 추세추종"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_full_card(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_full_card(d, i, is_rank=True)

# -----------------------------------------------------------------------------
# [5] AUTO-REFRESH LOGIC CONTROLLER
# -----------------------------------------------------------------------------
now = time.time()
need_rerun = False

# Logic: If trigger is set OR (timer is on AND time passed)
t_val_my = TIME_OPTS[auto_my]
if st.session_state.trigger_my or (t_val_my > 0 and now - st.session_state.l_my > t_val_my):
    run_my_diagnosis()
    need_rerun = True

t_val_top3 = TIME_OPTS[auto_top3]
if st.session_state.trigger_top3 or (t_val_top3 > 0 and now - st.session_state.l_top3 > t_val_top3):
    run_market_scan('TOP3')
    need_rerun = True

t_val_sep = TIME_OPTS[auto_sep]
if st.session_state.trigger_sep or (t_val_sep > 0 and now - st.session_state.l_sep > t_val_sep):
    run_market_scan('SEPARATE')
    need_rerun = True

if need_rerun: st.rerun()

if t_val_my > 0 or t_val_top3 > 0 or t_val_sep > 0:
    time.sleep(1)
    st.rerun()
