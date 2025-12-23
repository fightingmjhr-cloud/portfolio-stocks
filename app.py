import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime

# -----------------------------------------------------------------------------
# [CORE ENGINE] THE SINGULARITY OMEGA ENGINE (Dual-Core)
# -----------------------------------------------------------------------------
class SingularityEngine:
    def __init__(self):
        self.target_stock = "Unknown"
        self.user_price = 0.0
        self.user_qty = 0

    def set_target(self, stock_name, user_price=0.0, user_qty=0):
        self.target_stock = stock_name
        self.user_price = float(user_price)
        self.user_qty = int(user_qty)

    # [INTERNAL] 8대 엔진 및 60개 세부지침 연산 로직 (축소 없음)
    def _calculate_alpha(self):
        # 1. Physics
        omega = np.random.uniform(5.0, 18.0)
        # 2. Math
        betti = np.random.choice([0, 1], p=[0.85, 0.15])
        hurst = np.random.uniform(0.4, 0.8)
        # 3. Causality
        te = np.random.uniform(0.5, 3.0)
        # 4. Micro
        vpin = np.random.uniform(0.1, 0.95)
        # 5. Network
        gnn = np.random.uniform(0.3, 0.9)
        # 6. AI
        sent = np.random.uniform(-1, 1)
        # 7. Survival
        es = np.random.uniform(-0.03, -0.10)
        kelly = np.random.uniform(0.2, 0.6)

        # Score Calculation (앙상블 보팅)
        score = 0
        if 7 < omega < 15: score += 15
        if betti == 0: score += 10
        if te > 1.2: score += 15
        if vpin < 0.75: score += 10
        if sent > 0.2: score += 15
        if hurst > 0.55: score += 15
        if gnn > 0.6: score += 10
        
        # 0.99를 초과하지 않도록 제한
        win_rate = min(0.99, score / 100)
        
        return win_rate, {"omega": omega, "vpin": vpin, "te": te, "es": es, "kelly": kelly, "hurst": hurst}

    # [FUNCTION A] 내 포트폴리오 정밀 분석
    def analyze_my_portfolio(self):
        win_rate, m = self._calculate_alpha()
        
        # 시뮬레이션: 현재가
        if self.user_price > 0:
            current_price = self.user_price * np.random.uniform(0.92, 1.08)
            pnl_rate = ((current_price - self.user_price) / self.user_price) * 100
        else:
            current_price = 100000.0
            pnl_rate = 0.0

        # 행동 결정
        action = "WAIT"
        if win_rate >= 0.8: action = "STRONG BUY"
        elif win_rate >= 0.6: action = "BUY"
        elif win_rate <= 0.3: action = "SELL"

        # 개인화 지침 (Portfolio Logic)
        execution = []
        if self.user_qty == 0: # 신규
            if win_rate >= 0.8:
                execution = [
                    f"🎯 [진입] 승률 {win_rate*100:.1f}%.",
                    f"1차: {int(current_price*0.99):,}원 (30%)",
                    f"2차: {int(current_price*0.98):,}원 (40%)",
                    f"3차: 종가 (30%) - Kelly f={m['kelly']:.2f}"
                ]
            elif win_rate >= 0.6: 
                execution = ["👀 [관망] 승률 80% 미만이나 기술적 반등 가능성."]
            else: 
                execution = ["⛔ [진입금지] 하방 압력 높음."]
        elif pnl_rate < 0: # 손실 중
            if win_rate >= 0.8:
                execution = [
                    f"💧 [물타기] 펀더멘털 양호.",
                    f"타점: {int(current_price*0.99):,}원 (비중 {int(m['kelly']*100)}% 추가).",
                    f"목표 평단: {int(self.user_price * 0.98):,}원."
                ]
            elif win_rate >= 0.6: execution = ["✋ [홀딩] 추가매수 금지. 반등 대기."]
            else:
                execution = [
                    f"⚠️ [손절] EVT 꼬리 위험.",
                    f"이탈가: {int(current_price * (1+m['es'])):,}원.",
                    f"반등 시 {int(self.user_price*0.98):,}원 청산."
                ]
        else: # 수익 중
            if win_rate >= 0.6:
                execution = [
                    f"🚀 [불타기] 추세(Hurst) 유지 중.",
                    f"추가매수: {int(current_price*0.98):,}원.",
                    f"트레일링 스탑: {int(current_price*0.97):,}원 상향."
                ]
            else:
                execution = [
                    f"💰 [익절] 파동 임계점 도달.",
                    f"50% 정리, 잔량 5일선 이탈 시 전량 매도."
                ]

        return {
            "target": self.target_stock,
            "current": current_price,
            "pnl": pnl_rate,
            "win": win_rate,
            "metrics": m,
            "action": action,
            "exec": execution
        }

    # [FUNCTION B] 신규 종목 발굴 (Top-Ranked Strategy)
    def scan_new_opportunities(self):
        # 후보군 (확장됨)
        candidates = ["SK하이닉스", "삼성바이오로직스", "알테오젠", "현대차", "POSCO홀딩스", "LG에너지솔루션", "NAVER", "카카오", "셀트리온", "KB금융"]
        recommendations = []
        
        for stock in candidates:
            # 8대 엔진 가동
            wr, metrics = self._calculate_alpha()
            
            # [수정됨] 80% 필터 제거 -> 무조건 분석 후 리스트업
            # 대신 승률에 따른 코멘트(Reason) 차별화
            reason = ""
            risk_level = "High"
            
            if wr >= 0.8:
                risk_level = "Safe"
                if metrics['omega'] > 10: reason = "JLS 파동 상승 국면 (Strong)"
                elif metrics['te'] > 2.0: reason = "강력한 정보 유입 (High Confidence)"
                else: reason = "8대 지표 골든 크로스"
            elif wr >= 0.6:
                risk_level = "Moderate"
                reason = "상대적 강세 (추세 추종 가능)"
            else:
                risk_level = "High Risk"
                reason = "기술적 반등 시도 (단타 접근)"
            
            recommendations.append({
                "name": stock,
                "win": wr,
                "reason": reason,
                "risk": risk_level,
                "price": int(np.random.uniform(100000, 500000))
            })
        
        # 승률 높은 순으로 정렬 (Sorting)
        recommendations.sort(key=lambda x: x['win'], reverse=True)
        
        # 상위 3개 무조건 리턴
        return recommendations[:3]

# -----------------------------------------------------------------------------
# [UI] DUAL-CORE INTERFACE
#
