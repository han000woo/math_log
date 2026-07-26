# 📐 수학 학습 로그 (Streamlit)

매일 공부한 챕터를 마크다운 노트로 남기고, 배운 개념을 코드로 구현해 인터랙티브하게 시각화하는 개인 학습 대시보드. **노트를 git push 하면 배포된 앱에 자동 반영**됩니다.

## 구성
```
math-study-log/
├── streamlit_app.py        # 홈 대시보드 (지표·최근 노트)
├── utils.py                # notes 폴더 파싱
├── pages/
│   ├── 1_학습노트.py        # 마크다운 노트 뷰어 (LaTeX 렌더링)
│   ├── 2_수식라이브러리.py   # 핵심 수식 LaTeX 카드
│   └── 3_코드시각화.py       # 선형변환·정규분포·경사하강법 데모
├── notes/                  # ← 단계별 폴더 안에 매일 노트를 추가!
│   ├── 선형대수/
│   │   └── 2026-07-26_벡터와-내적.md
│   └── 미적분·최적화/
│       └── 2026-07-27_경사하강법-구현.md
├── requirements.txt
└── .gitignore
```

## 로컬 실행
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 매일 하는 일 (핵심 루틴)
1. **단계 폴더** 안에 새 파일 추가 — 파일명은 **`YYYY-MM-DD_주제.md`** 규칙.
   폴더명이 곧 단계(카테고리)가 되고, 앱은 "단계 선택 → 노트 선택" 2단계로 보여준다.
   ```
   notes/선형대수/2026-07-28_행렬곱.md
   ```
   새 단계가 필요하면 폴더를 새로 만들면 된다 (예: `notes/확률통계/`).
2. 파일 맨 위 프론트매터로 태그 지정(선택). 단계는 폴더로 정해지므로 생략 가능:
   ```markdown
   ---
   tags: [행렬곱, 선형변환]
   ---
   ```
3. 본문은 자유롭게. 수식은 `$인라인$` 또는 `$$블록$$` (LaTeX 자동 렌더링).
4. 커밋 & 푸시:
   ```bash
   git add . && git commit -m "day N: 행렬곱" && git push
   ```
   → 배포된 앱이 몇 초 뒤 자동 업데이트.

## 무료 배포 (Streamlit Community Cloud)
1. 이 폴더를 GitHub 리포지토리로 push.
   ```bash
   git init && git add . && git commit -m "init"
   git branch -M main
   git remote add origin https://github.com/<사용자명>/math-study-log.git
   git push -u origin main
   ```
2. https://share.streamlit.io 접속 → GitHub 로그인.
3. **New app** → 리포 선택 → Main file path에 `streamlit_app.py` 입력 → Deploy.
4. `https://<이름>.streamlit.app` 주소가 발급됩니다. 이후엔 push만 하면 끝.

## 확장 아이디어
- `pages/2_수식라이브러리.py` 의 `FORMULAS` 리스트에 dict 추가 → 수식 카드 늘리기.
- `pages/3_코드시각화.py` 의 `DEMOS` 에 함수 등록 → 새 시각화(PCA, 로지스틱 회귀 등) 추가.
- 노트에 그날 구현한 numpy 코드를 함께 붙이면, 이론+구현이 한 곳에 쌓입니다.