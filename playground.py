import numpy as np

# 예제 4-b 를 첨가행렬로 확인
Ab = np.array([[1, 0, 3, -1], [0, 1, -4, 2], [0, 0, 0, 0]], dtype=float)

A, b = Ab[:, :3], Ab[:, 3]
print(A)
r_A, r_Ab, n = (np.linalg.matrix_rank(A), np.linalg.matrix_rank(Ab), A.shape[1])
free = n - r_A  # 자유변수 개수
print(f"rank(A)={r_A}, rank(Ab)={r_Ab}, 자유변수={free}")
# rank(A)=2, rank(Ab)=2, 자유변수=1  → 무수히 많은 해 (직선)
