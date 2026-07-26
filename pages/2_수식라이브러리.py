"""수식 라이브러리 — 자주 쓰는 ML 수식을 LaTeX 카드로 모아두는 곳.

새 수식을 추가하려면 아래 FORMULAS 리스트에 dict 하나만 append 하면 된다.
"""

import streamlit as st

st.set_page_config(page_title="수식 라이브러리", page_icon="🧮", layout="wide")
st.title("🧮 수식 라이브러리")
st.caption(
    "공부하며 만난 핵심 수식을 LaTeX로 정리. 딕셔너리에 한 줄 추가하면 카드가 늘어납니다."
)

FORMULAS = [
    {
        "stage": "선형대수",
        "name": "내적 (dot product)",
        "latex": r"\mathbf{a}\cdot\mathbf{b}=\sum_{i=1}^{n} a_i b_i = \|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta",
        "note": "두 벡터의 유사도. 코사인 유사도의 뿌리.",
        "code": "import numpy as np\nnp.dot(a, b)   # 또는  a @ b",
    },
    {
        "stage": "선형대수",
        "name": "L2 노름",
        "latex": r"\|\mathbf{x}\|_2 = \sqrt{\sum_i x_i^2}",
        "note": "벡터의 길이. 정규화·거리 계산의 기본.",
        "code": "np.linalg.norm(x)",
    },
    {
        "stage": "선형대수",
        "name": "고유값 방정식",
        "latex": r"A\mathbf{v} = \lambda\mathbf{v}",
        "note": "변환해도 방향이 안 바뀌는 벡터 v(고유벡터)와 배율 λ. PCA의 뿌리.",
        "code": "eigvals, eigvecs = np.linalg.eig(A)",
    },
    {
        "stage": "선형대수",
        "name": "행렬곱",
        "latex": r"(AB)_{ij} = \sum_{k} A_{ik} B_{kj}",
        "note": "선형변환의 합성. 신경망 한 층 = 행렬곱 + 편향.",
        "code": "C = A @ B",
    },
    {
        "stage": "확률통계",
        "name": "정규분포 PDF",
        "latex": r"f(x)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)",
        "note": "가장 많이 나오는 분포. 가중치 초기화·노이즈 모델링.",
        "code": "from scipy.stats import norm\nnorm.pdf(x, loc=mu, scale=sigma)",
    },
    {
        "stage": "확률통계",
        "name": "베이즈 정리",
        "latex": r"P(A\mid B)=\frac{P(B\mid A)\,P(A)}{P(B)}",
        "note": "관측(B)으로 믿음(A)을 갱신. 나이브 베이즈·베이지안 추론.",
        "code": "posterior = (likelihood * prior) / evidence",
    },
    {
        "stage": "확률통계",
        "name": "분산 · 표준편차",
        "latex": r"\mathrm{Var}(X)=\mathbb{E}[(X-\mu)^2],\quad \sigma=\sqrt{\mathrm{Var}(X)}",
        "note": "데이터가 평균에서 퍼진 정도. 정규화·표준화의 기준.",
        "code": "x.var(), x.std()",
    },
    {
        "stage": "확률통계",
        "name": "공분산",
        "latex": r"\mathrm{Cov}(X,Y)=\mathbb{E}[(X-\mu_X)(Y-\mu_Y)]",
        "note": "두 변수가 함께 변하는 정도. PCA는 공분산 행렬의 고유분해.",
        "code": "np.cov(X, rowvar=False)",
    },
    {
        "stage": "미적분·최적화",
        "name": "경사하강법 갱신식",
        "latex": r"\theta_{t+1} = \theta_t - \eta\,\nabla_\theta J(\theta_t)",
        "note": "손실 J의 그래디언트 반대 방향으로 파라미터 이동. 학습의 심장.",
        "code": "theta -= lr * grad",
    },
    {
        "stage": "미적분·최적화",
        "name": "연쇄법칙 (chain rule)",
        "latex": r"\frac{dz}{dx}=\frac{dz}{dy}\cdot\frac{dy}{dx}",
        "note": "역전파(backprop)의 수학적 정체. 층을 거슬러 미분을 곱해 전파.",
        "code": "# grad_x = grad_y * dy_dx",
    },
    {
        "stage": "머신러닝",
        "name": "시그모이드",
        "latex": r"\sigma(z)=\frac{1}{1+e^{-z}}",
        "note": "실수를 (0,1) 확률로 압축. 로지스틱 회귀·이진 분류 출력.",
        "code": "1 / (1 + np.exp(-z))",
    },
    {
        "stage": "머신러닝",
        "name": "소프트맥스",
        "latex": r"\mathrm{softmax}(z_i)=\frac{e^{z_i}}{\sum_j e^{z_j}}",
        "note": "여러 점수를 확률분포로. 다중분류 출력층.",
        "code": "e = np.exp(z - z.max())\ne / e.sum()",
    },
    {
        "stage": "머신러닝",
        "name": "ReLU",
        "latex": r"\mathrm{ReLU}(x)=\max(0, x)",
        "note": "가장 흔한 활성화 함수. 음수를 0으로, 기울기 소실 완화.",
        "code": "np.maximum(0, x)",
    },
    {
        "stage": "머신러닝",
        "name": "MSE 손실",
        "latex": r"J=\frac{1}{n}\sum_{i=1}^{n}\left(y_i-\hat{y}_i\right)^2",
        "note": "회귀의 기본 손실함수.",
        "code": "np.mean((y - y_hat) ** 2)",
    },
    {
        "stage": "머신러닝",
        "name": "이진 교차엔트로피",
        "latex": r"J=-\frac{1}{n}\sum_i \big[y_i\log\hat{y}_i+(1-y_i)\log(1-\hat{y}_i)\big]",
        "note": "이진 분류 손실. 로지스틱 회귀·시그모이드 출력과 짝.",
        "code": "-np.mean(y*np.log(p) + (1-y)*np.log(1-p))",
    },
]

stages = sorted({f["stage"] for f in FORMULAS})
tabs = st.tabs(stages)
for tab, stage in zip(tabs, stages):
    with tab:
        for f in [x for x in FORMULAS if x["stage"] == stage]:
            with st.container(border=True):
                st.markdown(f"**{f['name']}**")
                st.latex(f["latex"])
                st.caption(f["note"])
                st.code(f["code"], language="python")
