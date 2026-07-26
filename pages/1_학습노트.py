"""학습 노트 뷰어 — notes/ 폴더의 마크다운을 렌더링.

Streamlit은 마크다운 안의 $...$ / $$...$$ 를 LaTeX로 렌더링한다.
"""

import streamlit as st

from utils import load_notes

st.set_page_config(page_title="학습 노트", page_icon="📚", layout="wide")
st.title("📚 학습 노트")

notes = load_notes()
if not notes:
    st.info("`notes/` 폴더에 마크다운 파일을 추가하세요.")
    st.stop()

# --- 사이드바: 검색 ---
query = st.sidebar.text_input("검색 (제목/본문)")

# 검색어로 먼저 걸러낸 뒤, 단계(폴더)별로 그룹핑
matched = [
    n
    for n in notes
    if query.lower() in n.title.lower() or query.lower() in n.body.lower()
]
if not matched:
    st.warning("검색 조건에 맞는 노트가 없습니다.")
    st.stop()

# --- 1단계: 단계(폴더) 선택 → 2단계: 노트 선택 (계단식 드릴다운) ---
stages = sorted({n.stage for n in matched})
counts = {s: sum(n.stage == s for n in matched) for s in stages}

col_l, col_r = st.columns([1, 2])
sel_stage = col_l.selectbox(
    "📁 단계 선택",
    stages,
    format_func=lambda s: f"{s}  ({counts[s]})",
    key="stage_select",
)

in_stage = [n for n in matched if n.stage == sel_stage]
labels = [f"{n.day.isoformat()} · {n.title}" for n in in_stage]
sel_label = col_r.selectbox(
    "📄 노트 선택",
    labels,
    key=f"note_select::{sel_stage}",  # 단계별 독립 상태 → 폴더 바꾸면 첫 노트로 리셋
)
note = in_stage[labels.index(sel_label)]

st.caption(
    f"전체 {len(notes)}개 · 검색 일치 {len(matched)}개 · '{sel_stage}' {counts[sel_stage]}개"
)

st.divider()
st.subheader(note.title)
st.caption(
    f"📅 {note.day.isoformat()}　|　🏷️ {note.stage}　|　"
    + " ".join("#" + t for t in note.tags)
)
st.markdown(note.body)  # 마크다운 + LaTeX 렌더링

with st.expander("📄 원본(raw)"):
    st.code(note.body, language="markdown")
