"""수학 학습 로그 — 홈 대시보드.
 
실행:  streamlit run streamlit_app.py
"""
import pandas as pd
import streamlit as st
 
from utils import load_notes, study_streak
 
st.set_page_config(page_title="MATH LOG", page_icon="M", layout="wide")
 
st.title("수학 일지")
st.caption("매일 공부한 챕터를 노트로 남기고, 코드로 구현한 개념을 시각화하는 공간")
 
notes = load_notes()
 
# --- 상단 지표 ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("총 노트 수", f"{len(notes)}개")
col2.metric("연속 학습", f"{study_streak(notes)}일 🔥")
col3.metric("다룬 주제", f"{len({n.title for n in notes})}개")
stages = {n.stage for n in notes}
col4.metric("학습 단계", f"{len(stages)}개 영역")
 
st.divider()
 
if not notes:
    st.info(
        "아직 노트가 없어요. `notes/` 폴더에 "
        "`2026-07-26_선형대수-벡터.md` 처럼 파일을 추가하고 git push 하면 여기에 나타납니다."
    )
    st.stop()
 
# --- 단계별 진행 현황 ---
left, right = st.columns([1, 1])
 
with left:
    st.subheader("단계별 노트 분포")
    df = pd.DataFrame({"단계": [n.stage for n in notes]})
    counts = df["단계"].value_counts()
    st.bar_chart(counts)
 
with right:
    st.subheader("학습 잔디 (최근 활동일)")
    day_counts = (
        pd.Series([n.day for n in notes]).value_counts().sort_index()
    )
    day_counts.index = pd.to_datetime(day_counts.index)
    st.bar_chart(day_counts)
 
st.divider()
 
# --- 최근 노트 미리보기 ---
st.subheader("🗂️ 최근 노트")
for n in notes[:5]:
    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**{n.title}**")
        c1.caption(f"{n.day.isoformat()} · {n.stage} · {' '.join('#' + t for t in n.tags)}")
        preview = n.body.strip().split("\n\n")[0][:160]
        c1.write(preview + ("…" if len(n.body) > 160 else ""))
        c2.caption(f"{n.word_count} 단어")
 
st.info("👈 왼쪽 사이드바에서 **학습 노트 · 수식 라이브러리 · 코드 시각화** 페이지로 이동하세요.")
 