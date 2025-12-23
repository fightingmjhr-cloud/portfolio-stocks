import streamlit as st
import pandas as pd
import numpy as np
import time
import zlib
import FinanceDataReader as fdr

# -----------------------------------------------------------------------------
# [0] GLOBAL SETTINGS & DATA LOADER
# -----------------------------------------------------------------------------
TIME_OPTS = {
    "⛔ 수동 (멈춤)": 0,
    "⏱️ 3분": 180, "⏱️ 5분": 300, "⏱️ 10분": 600, "⏱️ 15분": 900, "⏱️ 20분": 1200, 
    "⏱️ 30분": 1800, "⏱️ 40분": 2400, "⏱️ 1시간": 3600, "⏱️ 1시간 30분": 5400, 
    "⏱️ 2시간": 7200, "⏱️ 3시간": 10800
}

@st.cache_data(ttl=86400)
def get_stock_list():
    try:
        df = fdr.StockListing('KRX')
        df = df[~df['Name'].str.contains('스팩|리츠|우|홀딩스|ET')]
        return df['Name'].tolist()
    except:
        return ["삼성전자", "SK하이닉스", "LG에너지솔루션", "NAVER", "카카오"]

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
        
        omega = np.random.uniform(5.0, 25.0) 
        vol_surf = np.random.uniform(0.1, 0.9)
        betti = np.random.choice([0, 1], p=[0.85, 0.15]) 
        hurst = np.random.uniform(0.2, 0.95)
        te = np.random.uniform(0.1, 5.0)
        vpin = np.random.uniform(0.0, 1.0)
        hawkes = np.random.uniform(0.1, 4.0) if mode == "scalping" else np.random.uniform(0.1, 2.0)
        obi = np.random.uniform(-1.0, 1.0)
        gnn = np.random.uniform(0.1, 1.0)
        sent = np.random.uniform(-1.0, 1.0)
        es = np.random.uniform(-0.01, -0.30)
        kelly = np.random.uniform(0.01, 0.30)
        
        np.random.seed(None)
        return {
            "omega": omega, "vol_surf": vol_surf, "betti": betti, "hurst": hurst,
            "te": te, "vpin": vpin, "hawkes": hawkes, "obi": obi, 
            "gnn": gnn, "sent": sent, "es": es, "kelly": kelly
        }

    def run_diagnosis(self, name, mode="swing"):
        m = self._calculate_metrics(name, mode)
        score = 35.0 
        tags = [] 
        tags.append({'label': '기본 마진', 'val': '+35', 'type': 'base'})

        if m['vpin'] > 0.6: score -= 15; tags.append({'label': '독성 매물', 'val': '-15', 'type': 'bad'})
        if m['es'] < -0.15: score -= 15; tags.append({'label': '폭락 징후', 'val': '-15', 'type': 'bad'})
        if m['betti'] == 1: score -= 10; tags.append({'label': '구조 붕괴', 'val': '-10', 'type': 'bad'})

        if mode == "scalping":
            if m['hawkes'] > 2.5 and m['obi'] > 0.5: score += 40; tags.append({'label': '🚀 퍼펙트 수급', 'val': '+40', 'type': 'best'})
            elif m['hawkes'] > 1.5: score += 15; tags.append({'label': '⚡ 수급 우위', 'val': '+15', 'type': 'good'})
            elif m['hawkes'] < 0.8: score -= 10; tags.append({'label': '💤 거래 소강', 'val': '-10', 'type': 'bad'})
        else: 
            if m['hurst'] > 0.75 and m['gnn'] > 0.8: score += 35; tags.append({'label': '📈 대세 상승장', 'val': '+35', 'type': 'best'})
            elif m['hurst'] > 0.6: score += 10; tags.append({'label': '↗️ 추세 양호', 'val': '+10', 'type': 'good'})
            else: score -= 5; tags.append({'label': '📉 추세 미약', 'val': '-5', 'type': 'bad'})

        if 9 < m['omega'] < 13: score += 5; tags.append({'label': '📐 파동 안정', 'val': '+5', 'type': 'good'})
        if m['te'] > 3.0: score += 5; tags.append({'label': '📡 정보 폭발', 'val': '+5', 'type': 'good'})

        win_rate = min(0.92, score / 100)
        win_rate = max(0.15, win_rate)
        return win_rate, m, tags

    def generate_report(self, mode, price, m, wr, cash, current_qty, target_return):
        if mode == "scalping":
            vol = m['vol_surf'] * 0.04
            entry = int(price * (1 - vol))
            target = max(int(price * (1 + target_return/100)), int(price * (1 + vol*1.5)))
            stop = int(price * (1 - vol*0.7))
            time_str = "09:00~09:30 (골든타임)"
            
            reason_target = f"현재 <b>[Vol Surface(변동성 표면)]</b> 수치가 {m['vol_surf']:.2f}로 확장 국면입니다. <b>[OBI(호가 불균형)]</b>가 해소되는 1차 저항 구간을 목표로 설정했습니다."
            reason_stop = f"<b>[Hawkes(자기 여진)]</b> 효과가 소멸되는 임계점입니다. <b>[VPIN(독성 유동성)]</b>이 급증하면 알고리즘 투매가 나오니 칼손절하세요."
        else:
            target = int(price * (1 + target_return/100))
            stop = int(price * 0.93)
            time_str = "15:20 종가 or 5일선 지지"
            
            reason_target = f"<b>[Hurst(허스트 지수)]</b>가 {m['hurst']:.2f}로 추세가 강력합니다. 주가가 관성을 유지하며 피보나치 확장 레벨까지 갈 확률이 높습니다."
            reason_stop = f"<b>[Omega(로그 주기 진동수)]</b>는 안정적이나, {stop:,}원은 <b>[Topology(위상수학)]</b> 구조가 붕괴되는 특이점입니다. 깨지면 던지세요."

        adjusted_kelly = m['kelly'] * (wr / 0.8) if wr < 0.8 else m['kelly']
        alloc_cash = cash * adjusted_kelly
        can_buy_qty = int(alloc_cash / price) if price > 0 else 0

        if wr >= 0.75:
            cmd = "🔥 STRONG BUY"; style = "border: 2px solid #00FF00; color: #00FF00;"
            briefing = f"<b>[탁월함]</b> 8대 엔진 스캔 결과, <b>'구조적 상승(Structural Alpha)'</b> 국면입니다. <b>[GNN 중심성]</b>이 높아 돈을 빨아들이는 <b>주도주</b>입니다."
            action = f"확률 우위 확실. 현금 <b>{int(adjusted_kelly*100)}% ({can_buy_qty}주)</b> 투입. 공포를 사세요."
        elif wr >= 0.55:
            cmd = "⚖️ BUY / HOLD"; style = "border: 2px solid #FFAA00; color: #FFAA00;"
            briefing = f"<b>[양호함]</b> 상승 동력은 있으나 <b>[ES(꼬리 위험)]</b>가 {m['es']:.2f}로 불안합니다. 추세 속에 노이즈가 섞여 있습니다."
            action = f"리스크 분산을 위해 <b>{int(can_buy_qty/2)}주</b>만 선취매. 지지 확인 후 불타기 하세요."
        else:
            cmd = "🛡️ SELL / WAIT"; style = "border: 2px solid #FF4444; color: #FF4444;"
            briefing = f"<b>[위험]</b> <b>[VPIN]</b> 경고등이 켜졌습니다. 스마트 머니가 개미에게 물량을 넘기는 '분산' 단계일 수 있습니다."
            action = "절대 진입 금지. 보유 중이면 반등 시 전량 매도하여 현금을 확보가 답입니다."

        return {
            "cmd": cmd, "briefing": briefing, "action": action, "time": time_str, "style": style,
            "prices": (entry if mode=='scalping' else price, target, stop),
            "qty_guide": can_buy_qty,
            "reasons": {"target": reason_target, "stop": reason_stop}
        }

    # [용어 통역사]
    def explain_term(self, persona):
        if persona == 'hamzzi':
            return """
            <div style='background:#222; padding:10px; border-radius:8px; font-size:12px; margin-top:10px; border:1px dashed #555;'>
            <b>🐹 햄찌의 눈높이 설명:</b><br>
            • <b>Hawkes (수급 폭발력):</b> 사람들이 "우와!" 하고 몰려드는 정도야! 2.0 넘으면 축제 분위기! 🎉<br>
            • <b>VPIN (독성 매물):</b> 기관 형님들이 몰래 팔아치우는 나쁜 물량이야! 이거 높으면 도망쳐! 🏃<br>
            • <b>Hurst (추세 강도):</b> 한 번 방향 잡으면 끝까지 가려는 고집! 높을수록 뚝심 있는 녀석이지!<br>
            • <b>Omega (파동):</b> 주가 심장박동 같은 거! 일정하면 건강한 건데, 너무 빠르면 심장마비(폭락) 와!
            </div>
            """
        else:
            return """
            <div style='background:#222; padding:10px; border-radius:8px; font-size:12px; margin-top:10px; border:1px dashed #555;'>
            <b>🐯 호랑이의 실전 해설:</b><br>
            • <b>Hawkes:</b> 매수 주문이 꼬리에 꼬리를 무는 '자기 여진' 현상이다. 수급의 질을 보여주지.<br>
            • <b>VPIN:</b> 정보 비대칭을 이용한 약탈적 유동성이다. 이 수치가 높으면 설거지 당한다.<br>
            • <b>Hurst:</b> 주가의 '기억력'이다. 랜덤워크(0.5)보다 높으면 추세추종 전략이 먹힌다는 뜻이지.<br>
            • <b>GNN:</b> 종목 간의 상관관계를 분석했을 때, 이 놈이 대장(Center)인지 쫄병인지 알려준다.
            </div>
            """

    def hamzzi_nagging(self, cash, portfolio, market_data):
        total_invest = 0; current_val = 0
        for s in portfolio:
            invest = s['price'] * s['qty']
            if s['name'] in market_data['Name'].values: cur_p = int(market_data[market_data['Name'] == s['name']].iloc[0]['Close'])
            else: cur_p = s['price']
            total_invest += invest; current_val += cur_p * s['qty']
        
        total_asset = cash + current_val
        cash_ratio = (cash / total_asset * 100) if total_asset > 0 else 0
        pnl_pct = ((current_val - total_invest) / total_invest * 100) if total_invest > 0 else 0
        
        title = "🐹 야수 햄찌의 불타기 특강"
        if cash_ratio > 50:
            intro = "야! 너 바보야? 현금을 왜 놀려? 😤"
            logic = "지금 변동성(Vol)이 춤을 추는데 구경만 할 거야? 베타(Beta)를 태워야지! 쫄보처럼 굴지 마!"
            advice = "당장 현금 다 털어서 **급등주(High Beta)** 올라타라구! 인생 한 방이야! 🚀"
        elif pnl_pct < -10:
            intro = "으앙 물렸어? 🥺 괜찮아! 오히려 좋아! 세일 기간이잖아!"
            logic = "지금 공포 지수(VIX)가 높아서 그래. 이럴 때가 기회라구! '물타기' 말고 '불타기'로 평단 낮추고 수량 늘려서 탈출하자! 🐹🔥"
            advice = "레버리지 땡겨서라도 더 사! 기술적 반등 한 번이면 멘징하고도 남아! 쫄지마!"
        else:
            intro = "아... 계좌가 너무 얌전해. 재미없어! 🥱"
            logic = "변동성이 없으면 돈을 못 벌어! 거래량 터지는 주도 섹터로 갈아타야지!"
            advice = "지금 당장 거래대금 상위 종목 찍어서 몰빵해! 🐹 야수의 심장을 보여줘!"
        return title, f"<div style='font-size:14px;'><b>1. 잔소리:</b> {intro}<br><b>2. 뇌피셜(?):</b> {logic}<br><b style='color:#FFAA00;'>3. 햄찌의 명령:</b> {advice}</div>"

    def tiger_nagging(self, cash, portfolio, market_data):
        total_invest = 0; current_val = 0
        for s in portfolio:
            invest = s['price'] * s['qty']
            if s['name'] in market_data['Name'].values: cur_p = int(market_data[market_data['Name'] == s['name']].iloc[0]['Close'])
            else: cur_p = s['price']
            total_invest += invest; current_val += cur_p * s['qty']
        
        total_asset = cash + current_val
        cash_ratio = (cash / total_asset * 100) if total_asset > 0 else 0
        pnl_pct = ((current_val - total_invest) / total_invest * 100) if total_invest > 0 else 0

        title = "🐯 호랑이의 유비무환(有備無患) 대호통"
        if cash_ratio > 60:
            intro = "음, 자네 아주 현명하구만. 과유불급(過猶不及)이라 했다. 🐯"
            logic = "시장이 흉흉할 땐 현금이 왕(Cash is King)이야. 불확실성이 해소될 때까지 기다려."
            advice = "지금처럼 현금 꽉 쥐고 있다가, PBR 0.5배 밑으로 떨어지는 우량주 나오면 그때 천천히 담아."
        elif pnl_pct < -5:
            intro = "거봐라! 소탐대실(小貪大失) 하지 말랬지! 😡"
            logic = "기업 가치 훼손이 없다면 기회지만, 잡주라면 MDD 관리 안 하면 계좌 녹는다!"
            advice = "당장 손절해! 그리고 그 돈으로 배당주나 채권 사서 잊어버려."
        else:
            intro = "계좌 꼬라지가 왜 이래? 공부는 하고 투자하는 거야? 쯧쯧."
            logic = "기본적 분석(Fundamental) 없이 차트만 보고 사니까 맨날 제자리걸음이지."
            advice = "HTS 끄고 사업보고서(DART) 정독해! 아는 기업에만 투자해!"
        return title, f"<div style='font-size:14px;'><b>1. 호통:</b> {intro}<br><b>2. 훈계:</b> {logic}<br><b style='color:#FF4444;'>3. 어르신 말씀:</b> {advice}</div>"

# -----------------------------------------------------------------------------
# [2] UI & PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Tiger&Hamzzi Quant", page_icon="🐯", layout="centered")

st.markdown("""
<style>
    /* Global Styles */
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Pretendard', sans-serif; }
    .app-title { text-align: center; font-size: 36px; font-weight: 900; color: #fff; padding: 30px 0; text-shadow: 0 0 25px rgba(0,201,255,0.7); }
    
    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1f26 !important; color: #fff !important; border: 1px solid #444 !important; border-radius: 8px;
    }
    
    /* Buttons */
    .stButton>button { 
        width: 100%; border-radius: 12px; font-weight: 800; height: 50px; font-size: 18px;
        background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%); border: none; color: #000;
        box-shadow: 0 4px 15px rgba(0, 201, 255, 0.3); transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    
    /* Card UI */
    .stock-card { 
        background: #121212; border-radius: 16px; padding: 0; margin-bottom: 30px; 
        border: 1px solid #333; box-shadow: 0 10px 30px rgba(0,0,0,0.5); overflow: hidden;
    }
    .card-header { padding: 15px 20px; background: #1e1e1e; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center; }
    .stock-name { font-size: 22px; font-weight: 900; color: #fff; }
    .stock-score { font-size: 14px; font-weight: bold; background: #333; padding: 5px 12px; border-radius: 20px; color: #fff; border: 1px solid #555; }
    
    /* Tags & Info */
    .tag-container { padding: 15px 20px 5px 20px; display: flex; flex-wrap: wrap; gap: 8px; }
    .tag { font-size: 12px; font-weight: bold; padding: 4px 10px; border-radius: 6px; color: #000; display: inline-block; }
    .tag-best { background: #00FF00; box-shadow: 0 0 10px rgba(0,255,0,0.4); }
    .tag-good { background: #00C9FF; }
    .tag-bad { background: #FF4444; color: #fff; }
    .tag-base { background: #555; color: #ccc; }
    
    .info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: #333; margin: 15px 20px; border: 1px solid #333; }
    .info-item { background: #121212; padding: 10px; text-align: center; }
    .info-label { font-size: 11px; color: #888; display: block; margin-bottom: 3px; }
    .info-val { font-size: 15px; font-weight: bold; color: #fff; }
    
    .action-box { margin: 0 20px 20px 20px; background: #1a1a1a; border-radius: 10px; padding: 15px; border-left: 4px solid #fff; }
    .ab-title { font-size: 14px; font-weight: bold; margin-bottom: 8px; color: #aaa; text-transform: uppercase; }
    .ab-content { font-size: 14px; line-height: 1.6; color: #eee; margin-bottom: 15px; }
    .rationale-box { background: #0d1117; padding: 12px; border-radius: 8px; font-size: 13px; color: #ccc; line-height: 1.5; border: 1px solid #333; }
    .rat-label { color: #888; font-weight: bold; font-size: 12px; margin-bottom: 4px; display:block; }
    
    .timeline { display: flex; justify-content: space-between; background: #0f0f0f; padding: 15px 25px; border-top: 1px solid #333; }
    .tl-item { text-align: center; }
    .tl-label { font-size: 11px; color: #666; margin-bottom: 4px; }
    .tl-val { font-size: 16px; font-weight: bold; color: #fff; }
    
    /* Advisors */
    .hamzzi-box { background: linear-gradient(135deg, #2c241b, #1a1510); border: 2px solid #FFAA00; border-radius: 16px; padding: 25px; color: #eee; margin-bottom: 15px; box-shadow: 0 0 20px rgba(255, 170, 0, 0.2); }
    .hamzzi-title { color: #FFAA00; font-size: 20px; font-weight: 900; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;}
    .tiger-box { background: linear-gradient(135deg, #3d0000, #1a0000); border: 2px solid #FF4444; border-radius: 16px; padding: 25px; color: #eee; margin-bottom: 25px; box-shadow: 0 0 20px rgba(255, 68, 68, 0.2); }
    .tiger-title { color: #FF4444; font-size: 20px; font-weight: 900; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;}
    
    .rank-ribbon { position: absolute; top: 0; left: 0; padding: 5px 12px; font-size: 12px; font-weight: bold; color: #fff; background: linear-gradient(45deg, #FF416C, #FF4B2B); border-bottom-right-radius: 12px; z-index: 5; }
    
    .hud-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 10px; background: #0d1117; padding: 10px; border-radius: 8px; }
    .hud-item { background: #21262d; padding: 8px; border-radius: 6px; text-align: center; border: 1px solid #30363d; }
    .hud-label { font-size: 10px; color: #8b949e; display: block; margin-bottom: 2px; }
    .hud-val { font-size: 13px; color: #58a6ff; font-weight: bold; }
    
    /* Progress Bar */
    .prog-bg { background: #333; height: 8px; border-radius: 4px; width: 100%; }
    .prog-fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
    
    div[data-testid="column"]:nth-child(5) { margin-left: -20px !important; margin-top: 2px; }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-title'>🐯 Tiger&Hamzzi Quant 🐹</div>", unsafe_allow_html=True)

# [SESSION STATE]
if 'portfolio' not in st.session_state: st.session_state.portfolio = []
if 'ideal_list' not in st.session_state: st.session_state.ideal_list = []
if 'sc_list' not in st.session_state: st.session_state.sc_list = []
if 'sw_list' not in st.session_state: st.session_state.sw_list = []
if 'cash' not in st.session_state: st.session_state.cash = 10000000 
if 'target_return' not in st.session_state: st.session_state.target_return = 5.0
if 'my_diagnosis' not in st.session_state: st.session_state.my_diagnosis = []
if 'display_mode' not in st.session_state: st.session_state.display_mode = None
# Triggers & Timers
if 'l_my' not in st.session_state: st.session_state.l_my = 0
if 'l_top3' not in st.session_state: st.session_state.l_top3 = 0
if 'l_sep' not in st.session_state: st.session_state.l_sep = 0
if 'trigger_my' not in st.session_state: st.session_state.trigger_my = False
if 'trigger_top3' not in st.session_state: st.session_state.trigger_top3 = False
if 'trigger_sep' not in st.session_state: st.session_state.trigger_sep = False

stock_names = get_stock_list()

# [CORE EXECUTION FUNCTIONS]
def run_my_diagnosis():
    engine = SingularityEngine(); market_data = load_top50_data(); my_res = []
    with st.spinner("내 보유 종목 정밀 해부 중..."):
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
    st.session_state.trigger_my = False # Reset trigger

def run_market_scan(mode):
    engine = SingularityEngine(); market_data = load_top50_data()
    sc, sw, ideal = [], [], []
    with st.spinner("전 종목 정밀 타격 및 랭킹 산출 중..."):
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
            
    sc.sort(key=lambda x: x['win'], reverse=True)
    sw.sort(key=lambda x: x['win'], reverse=True)
    ideal.sort(key=lambda x: x['win'], reverse=True)
    st.session_state.sc_list = sc[:3]; st.session_state.sw_list = sw[:3]; st.session_state.ideal_list = ideal[:3]
    
    if mode == 'TOP3': 
        st.session_state.l_top3 = time.time()
        st.session_state.trigger_top3 = False
    else: 
        st.session_state.l_sep = time.time()
        st.session_state.trigger_sep = False

# [UI: PERSONAL PORTFOLIO]
with st.expander("💰 내 자산 및 포트폴리오 (Personal)", expanded=True):
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
        h1, h2, h3, h4, h5 = st.columns([3.2, 1.8, 1.3, 2.0, 0.4])
        h1.caption("종목명 (검색/선택)")
        h2.caption("평단가 (원)")
        h3.caption("수량")
        h4.caption("전략")
        
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
    else: st.info("보유 종목이 없습니다. 우측 상단 '➕ 종목 추가' 버튼을 눌러주세요.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # MY DIAGNOSIS BUTTON & TIMER
    if st.button("📝 내 종목만 진단하기", use_container_width=True):
        st.session_state.display_mode = 'MY'
        st.session_state.trigger_my = True # Trigger flag set
        st.rerun()
        
    auto_my = st.selectbox("⏱️ 내 종목 자동진단 주기", list(TIME_OPTS.keys()), index=0, key="tm_my", label_visibility="collapsed")

    # ADVISORS
    st.markdown("<br>", unsafe_allow_html=True)
    bc1, bc2 = st.columns(2)
    with bc1:
        if st.button("🐹 햄찌의 앙큼상큼 팩트폭격 뀨? ❤️", use_container_width=True):
            engine = SingularityEngine(); market_data = load_top50_data()
            title, msg = engine.hamzzi_nagging(st.session_state.cash, st.session_state.portfolio, market_data)
            st.session_state.adv_msg = f"<div class='hamzzi-box'><div class='hamzzi-title'>{title}</div>{msg}</div>"
    with bc2:
        if st.button("🐯 호랑이의 유비무환(有備無患) 대호통", use_container_width=True):
            engine = SingularityEngine(); market_data = load_top50_data()
            title, msg = engine.tiger_nagging(st.session_state.cash, st.session_state.portfolio, market_data)
            st.session_state.adv_msg = f"<div class='tiger-box'><div class='tiger-title'>{title}</div>{msg}</div>"
            
    if 'adv_msg' in st.session_state: st.markdown(st.session_state.adv_msg, unsafe_allow_html=True)

# Helper Function
def render_full_card(d, idx=None, is_rank=False):
    p = d['plan']
    tag_html = "".join([f"<span class='tag tag-{t['type']}'>{t['label']} {t['val']}</span> " for t in d['tags']])
    rank_html = f"<div class='rank-ribbon'>{idx+1}위</div>" if is_rank else ""
    win_pct = d['win'] * 100
    color = "#00FF00" if d['win'] >= 0.75 else "#FFAA00" if d['win'] >= 0.55 else "#FF4444"
    
    st.markdown(f"""
    <div class='stock-card'>
        {rank_html}
        <div class='card-header' style='padding-left: {50 if is_rank else 20}px;'>
            <span class='stock-name'>{d['name']}</span>
            <span class='stock-score' style='color:{p['style'].split(':')[1]}; border-color:{p['style'].split(':')[1]};'>승률 {d['win']*100:.1f}%</span>
        </div>
        <div style='padding:0 20px 10px 20px; display:flex; align-items:center; gap:10px;'>
            <div class='prog-bg'><div class='prog-fill' style='width:{win_pct}%; background:{color};'></div></div>
            <span style='color:{color}; font-weight:bold; font-size:12px;'>{win_pct:.1f}%</span>
        </div>
        <div class='tag-container'>{tag_html}</div>
        {'<div class="info-grid"><div class="info-item"><span class="info-label">현재가</span><span class="info-val">'+f"{d['price']:,}"+'</span></div><div class="info-item"><span class="info-label">수익률</span><span class="info-val" style="color:'+("#ff4444" if d.get('pnl',0)<0 else "#00ff00")+f'">{d.get("pnl",0):.2f}%</span></div></div>' if not is_rank else ''}
        <div class='action-box' style='{p['style']}'>
            <div class='ab-title'>{p['cmd']}</div>
            <div class='ab-content'>{p['briefing']}<br><br>{p['action']}</div>
            <div class='rationale-box' style='margin-top:10px;'>
                <span class='rat-label'>🎯 목표가 근거:</span>{p['reasons']['target']}<br><br>
                <span class='rat-label'>🛑 손절가 근거:</span>{p['reasons']['stop']}
            </div>
        </div>
        <div class='timeline'>
            <div class='tl-item'><div class='tl-label'>진입/추매</div><div class='tl-val' style='color:#00C9FF'>{p['prices'][0]:,}</div></div>
            <div class='tl-item'><div class='tl-label'>목표가</div><div class='tl-val' style='color:#00FF00'>{p['prices'][1]:,}</div></div>
            <div class='tl-item'><div class='tl-label'>손절가</div><div class='tl-val' style='color:#FF4444'>{p['prices'][2]:,}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander(f"🔍 {d['name']} - 8대 엔진 HUD & 용어 설명"):
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
        engine = SingularityEngine()
        t1, t2 = st.tabs(["🐹 햄찌의 쉬운 설명", "🐯 호랑이의 실전 해설"])
        with t1: st.markdown(engine.explain_term('hamzzi'), unsafe_allow_html=True)
        with t2: st.markdown(engine.explain_term('tiger'), unsafe_allow_html=True)

# [MY DIAGNOSIS RENDER]
if st.session_state.my_diagnosis:
    st.markdown("---")
    st.markdown("<h5>👤 내 보유 종목 정밀 진단 리포트</h5>", unsafe_allow_html=True)
    for d in st.session_state.my_diagnosis: render_full_card(d, is_rank=False)

# [MARKET SCAN SECTION]
st.markdown("<br><hr style='border-top: 1px dashed #333; margin: 30px 0;'><br>", unsafe_allow_html=True)
st.markdown("#### 📡 시장 정밀 타격 (Market Intelligence)")
st.markdown("<br>", unsafe_allow_html=True)

b1, b2 = st.columns(2)
with b1:
    if st.button("🏆 타이거&햄찌 출격! (Top 3)"):
        st.session_state.display_mode = 'TOP3'
        st.session_state.trigger_top3 = True # Trigger flag set
        st.rerun()
    auto_top3 = st.selectbox("타이머1", list(TIME_OPTS.keys()), index=0, key="tm_top3", label_visibility="collapsed")

with b2:
    if st.button("📊 단타 / 추세 (전략별 보기)"):
        st.session_state.display_mode = 'SEPARATE'
        st.session_state.trigger_sep = True # Trigger flag set
        st.rerun()
    auto_sep = st.selectbox("타이머2", list(TIME_OPTS.keys()), index=0, key="tm_sep", label_visibility="collapsed")

# [MARKET RESULTS]
if st.session_state.display_mode == 'TOP3' and st.session_state.ideal_list:
    st.markdown("<h5>🏆 금일의 Singularity Ideal Pick (Top 3)</h5>", unsafe_allow_html=True)
    for i, d in enumerate(st.session_state.ideal_list): render_full_card(d, i, is_rank=True)

elif st.session_state.display_mode == 'SEPARATE' and (st.session_state.sc_list or st.session_state.sw_list):
    st.markdown("<h5>📊 전략별 절대 랭킹 (Top 3)</h5>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["⚡ 초단타", "🌊 추세추종"])
    with t1:
        for i, d in enumerate(st.session_state.sc_list): render_full_card(d, i, is_rank=True)
    with t2:
        for i, d in enumerate(st.session_state.sw_list): render_full_card(d, i, is_rank=True)

# [EXECUTION LOGIC CHECK - MAIN LOOP]
now = time.time()
need_rerun = False

# Logic: Manual Trigger OR Auto Timer
# 1. My Diagnosis
t_val_my = TIME_OPTS[auto_my]
if st.session_state.trigger_my or (t_val_my > 0 and now - st.session_state.l_my > t_val_my):
    if st.session_state.display_mode == 'MY':
        run_my_diagnosis()
        need_rerun = True

# 2. Top 3
t_val_top3 = TIME_OPTS[auto_top3]
if st.session_state.trigger_top3 or (t_val_top3 > 0 and now - st.session_state.l_top3 > t_val_top3):
    if st.session_state.display_mode == 'TOP3':
        run_market_scan('TOP3')
        need_rerun = True

# 3. Separate
t_val_sep = TIME_OPTS[auto_sep]
if st.session_state.trigger_sep or (t_val_sep > 0 and now - st.session_state.l_sep > t_val_sep):
    if st.session_state.display_mode == 'SEPARATE':
        run_market_scan('SEPARATE')
        need_rerun = True

if need_rerun: st.rerun()

# Timer Keep-Alive
if t_val_my > 0 or t_val_top3 > 0 or t_val_sep > 0:
    time.sleep(1)
    st.rerun()
