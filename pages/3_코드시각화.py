"""코드 시각화 — 배운 개념을 numpy로 직접 구현하고 인터랙티브하게 확인.

로드맵 3단계에 맞춘 데모 3개:
  1. 선형대수 : 행렬이 벡터/도형을 어떻게 변환하는가
  2. 확률통계 : 정규분포 샘플링과 대수의 법칙
  3. 최적화   : 경사하강법이 최솟값을 찾아가는 궤적
새 데모는 함수 하나 만들고 아래 DEMOS에 등록하면 된다.
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="코드 시각화", page_icon="📊", layout="wide")
st.title("📊 코드로 배우는 수학")
st.caption(
    "슬라이더를 움직이며 개념이 몸에 박히게. 각 데모의 핵심 코드도 함께 표시됩니다."
)


# ---------------------------------------------------------------- 1. 선형변환
def demo_linear_transform():
    st.subheader("① 선형대수 — 2×2 행렬의 선형변환")
    st.write("행렬 $A$가 단위 정사각형과 벡터들을 어떻게 변형하는지 확인하세요.")

    c = st.columns(4)
    a = c[0].slider("a", -2.0, 2.0, 1.0, 0.1)
    b = c[1].slider("b", -2.0, 2.0, 0.5, 0.1)
    cc = c[2].slider("c", -2.0, 2.0, 0.0, 0.1)
    d = c[3].slider("d", -2.0, 2.0, 1.0, 0.1)

    A = np.array([[a, b], [cc, d]])
    square = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]).T
    transformed = A @ square

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=square[0],
            y=square[1],
            fill="toself",
            name="원본",
            line=dict(color="#888"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=transformed[0],
            y=transformed[1],
            fill="toself",
            name="변환 후",
            line=dict(color="#e45756"),
        )
    )
    fig.update_layout(
        xaxis=dict(scaleanchor="y", range=[-3, 3]),
        yaxis=dict(range=[-3, 3]),
        height=420,
        legend=dict(orientation="h"),
    )
    st.plotly_chart(fig, use_container_width=True)

    det = np.linalg.det(A)
    st.metric("행렬식 det(A) = 넓이 배율", f"{det:.2f}")
    st.caption("det가 음수면 뒤집힘(반사), 0이면 한 직선/점으로 붕괴(정보 손실).")
    st.code(
        "A = np.array([[a, b], [c, d]])\ntransformed = A @ points  # 열벡터들에 변환 적용",
        language="python",
    )


# ---------------------------------------------------------------- 2. 정규분포
def demo_normal():
    st.subheader("② 확률통계 — 정규분포 샘플링 & 대수의 법칙")
    c = st.columns(3)
    mu = c[0].slider("평균 μ", -5.0, 5.0, 0.0, 0.1)
    sigma = c[1].slider("표준편차 σ", 0.1, 3.0, 1.0, 0.1)
    n = c[2].select_slider("표본 수 n", [10, 100, 1000, 10000, 100000], value=1000)

    rng = np.random.default_rng(0)
    samples = rng.normal(mu, sigma, n)

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=samples,
            nbinsx=60,
            histnorm="probability density",
            name="표본",
            marker_color="#4c78a8",
        )
    )
    xs = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 200)
    pdf = np.exp(-((xs - mu) ** 2) / (2 * sigma**2)) / np.sqrt(2 * np.pi * sigma**2)
    fig.add_trace(go.Scatter(x=xs, y=pdf, name="이론 PDF", line=dict(color="#e45756")))
    fig.update_layout(height=420, legend=dict(orientation="h"))
    st.plotly_chart(fig, use_container_width=True)

    c2 = st.columns(2)
    c2[0].metric("표본 평균", f"{samples.mean():.3f}", delta=f"목표 {mu}")
    c2[1].metric("표본 표준편차", f"{samples.std():.3f}", delta=f"목표 {sigma}")
    st.caption("n을 키울수록 표본 통계량이 이론값에 수렴 → 대수의 법칙.")
    st.code(
        "samples = rng.normal(mu, sigma, n)\nsamples.mean(), samples.std()",
        language="python",
    )


# ------------------------------------------------------------- 3. 경사하강법
def demo_gradient_descent():
    st.subheader("③ 최적화 — 경사하강법 궤적")
    st.write(r"함수 $f(x)=x^2$ 의 최솟값(0)을 경사하강법이 찾아가는 과정.")
    c = st.columns(3)
    x0 = c[0].slider("시작점 x₀", -9.0, 9.0, 8.0, 0.5)
    lr = c[1].slider("학습률 η", 0.01, 1.05, 0.1, 0.01)
    steps = c[2].slider("반복 횟수", 1, 40, 15)

    xs_path = [x0]
    x = x0
    for _ in range(steps):
        grad = 2 * x  # f'(x) = 2x
        x = x - lr * grad
        xs_path.append(x)
    xs_path = np.array(xs_path)

    grid = np.linspace(-10, 10, 200)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=grid, y=grid**2, name="f(x)=x²", line=dict(color="#888"))
    )
    fig.add_trace(
        go.Scatter(
            x=xs_path,
            y=xs_path**2,
            mode="lines+markers",
            name="궤적",
            line=dict(color="#e45756"),
        )
    )
    fig.update_layout(height=420, legend=dict(orientation="h"))
    st.plotly_chart(fig, use_container_width=True)

    c2 = st.columns(2)
    c2[0].metric("최종 x", f"{xs_path[-1]:.4f}")
    c2[1].metric("최종 f(x)", f"{xs_path[-1] ** 2:.4f}")
    if lr >= 1.0:
        st.warning("학습률이 너무 크면 발산합니다 — η를 1.0 이상으로 올려보세요!")
    st.code(
        "for _ in range(steps):\n    grad = 2 * x     # f'(x)\n    x = x - lr * grad",
        language="python",
    )


# ------------------------------------------------------------------- 4. PCA
def demo_pca():
    st.subheader("④ 선형대수 — PCA (주성분 분석) 밑바닥 구현")
    st.write("공분산 행렬의 **고유벡터**가 데이터가 가장 퍼진 방향(주성분)이다.")
    c = st.columns(3)
    corr = c[0].slider("상관 정도", -0.95, 0.95, 0.8, 0.05)
    spread = c[1].slider("퍼짐(scale)", 0.5, 4.0, 2.0, 0.1)
    n = c[2].select_slider("표본 수", [100, 300, 1000], value=300)

    rng = np.random.default_rng(1)
    cov = np.array([[spread**2, corr * spread], [corr * spread, 1.0]])
    X = rng.multivariate_normal([0, 0], cov, n)

    # --- PCA from scratch ---
    Xc = X - X.mean(axis=0)  # 1) 중심화
    C = np.cov(Xc, rowvar=False)  # 2) 공분산 행렬
    eigvals, eigvecs = np.linalg.eigh(C)  # 3) 고유분해
    order = np.argsort(eigvals)[::-1]  # 큰 고유값 순
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=X[:, 0],
            y=X[:, 1],
            mode="markers",
            name="데이터",
            marker=dict(color="#4c78a8", size=5, opacity=0.5),
        )
    )
    colors = ["#e45756", "#f58518"]
    for i in range(2):
        vec = eigvecs[:, i] * np.sqrt(eigvals[i]) * 2
        fig.add_trace(
            go.Scatter(
                x=[X.mean(0)[0] - vec[0], X.mean(0)[0] + vec[0]],
                y=[X.mean(0)[1] - vec[1], X.mean(0)[1] + vec[1]],
                mode="lines",
                name=f"주성분 {i+1}",
                line=dict(color=colors[i], width=4),
            )
        )
    fig.update_layout(
        xaxis=dict(scaleanchor="y"), height=430, legend=dict(orientation="h")
    )
    st.plotly_chart(fig, use_container_width=True)

    ratio = eigvals / eigvals.sum()
    st.metric("주성분 1의 설명 분산 비율", f"{ratio[0]*100:.1f}%")
    st.caption("상관을 키울수록 첫 주성분 하나로 데이터를 거의 설명 → 차원 축소 가능.")
    st.code(
        "Xc = X - X.mean(axis=0)\n"
        "C = np.cov(Xc, rowvar=False)\n"
        "eigvals, eigvecs = np.linalg.eigh(C)   # 고유벡터 = 주성분",
        language="python",
    )


# --------------------------------------------------- 5. 로지스틱 회귀
def demo_logistic_regression():
    st.subheader("⑤ 머신러닝 — 로지스틱 회귀 밑바닥 학습")
    st.write("시그모이드 + 경사하강법으로 두 클래스를 가르는 **결정 경계**를 학습한다.")
    c = st.columns(3)
    lr = c[0].slider("학습률 η", 0.01, 2.0, 0.5, 0.01)
    epochs = c[1].slider("에폭", 1, 300, 100)
    gap = c[2].slider("클래스 간격", 0.5, 4.0, 2.0, 0.1)

    rng = np.random.default_rng(2)
    n = 100
    X0 = rng.normal([-gap, -gap], 1.0, (n, 2))
    X1 = rng.normal([gap, gap], 1.0, (n, 2))
    X = np.vstack([X0, X1])
    y = np.hstack([np.zeros(n), np.ones(n)])
    Xb = np.hstack([np.ones((2 * n, 1)), X])  # 편향 항 추가

    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    # --- 경사하강법 학습 ---
    w = np.zeros(3)
    losses = []
    for _ in range(epochs):
        p = sigmoid(Xb @ w)
        grad = Xb.T @ (p - y) / len(y)
        w -= lr * grad
        eps = 1e-9
        losses.append(-np.mean(y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps)))

    col_a, col_b = st.columns([3, 2])
    with col_a:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=X0[:, 0],
                y=X0[:, 1],
                mode="markers",
                name="클래스 0",
                marker=dict(color="#4c78a8", size=6),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=X1[:, 0],
                y=X1[:, 1],
                mode="markers",
                name="클래스 1",
                marker=dict(color="#e45756", size=6),
            )
        )
        # 결정 경계: w0 + w1*x + w2*y = 0
        xs = np.array([X[:, 0].min(), X[:, 0].max()])
        if abs(w[2]) > 1e-6:
            ys = -(w[0] + w[1] * xs) / w[2]
            fig.add_trace(
                go.Scatter(
                    x=xs,
                    y=ys,
                    mode="lines",
                    name="결정 경계",
                    line=dict(color="#333", width=3),
                )
            )
        fig.update_layout(height=400, legend=dict(orientation="h"), title="결정 경계")
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(y=losses, mode="lines", line=dict(color="#e45756")))
        fig2.update_layout(
            height=400, title="손실(교차엔트로피) 감소", xaxis_title="epoch"
        )
        st.plotly_chart(fig2, use_container_width=True)

    acc = ((sigmoid(Xb @ w) > 0.5) == y).mean()
    st.metric("학습 정확도", f"{acc*100:.1f}%")
    st.code(
        "p = sigmoid(Xb @ w)\n"
        "grad = Xb.T @ (p - y) / len(y)\n"
        "w -= lr * grad     # 경사하강법 갱신",
        language="python",
    )


DEMOS = {
    "① 선형변환 (선형대수)": demo_linear_transform,
    "② 정규분포 (확률통계)": demo_normal,
    "③ 경사하강법 (최적화)": demo_gradient_descent,
    "④ PCA (선형대수)": demo_pca,
    "⑤ 로지스틱 회귀 (머신러닝)": demo_logistic_regression,
}

pick = st.sidebar.radio("데모 선택", list(DEMOS.keys()))
DEMOS[pick]()
