# A04: 덱 4 (Basic Statistics) → `02-descriptive-statistics.tex` 채우기 설계

system-architect, 2026-09-24, cycle 1/2. 설계 전용 문서다. LaTeX 본문은 T15(sonnet-writer), 그림은 T14(developer)가 만든다.
입력: `notes_text/4_BasicStats/slides.md`(23 슬라이드) + `media/`, `chapters/02-descriptive-statistics.tex`(568줄),
PLAN.md Q2, Q4, AC-W1..W12, architecture.md §1 덱 4 행, §6 U5, "CDF 경계" 문단.

## 0. 제약 요약

- Q2: 기존 절 본문은 한 줄도 바꾸지 않는다. 새 내용은 기존 `\section` **사이**에 새 `\section` 으로만 넣는다
  (기존 절 안에 subsection을 덧붙이는 방식도 쓰지 않는다. 경계가 모호해지기 때문).
- AC-W11: `\subsection{부호와 방향}`(`sec:skew-sign`)부터 다음 `\subsection{판단 기준}` 사이에는 diff hunk가 없다.
  이 설계의 모든 삽입점은 그 구간 밖이다(아래 §2 표의 "삽입 위치" 열).
- `sec:cdf` 는 `04-distributions.tex` 54행의 라벨이다. 재사용 금지. CDF 정의는 새 라벨 `sec:cdf-def` / `def:cdf` 에 둔다
  (architecture.md "CDF 경계": 정의는 02에만, 04 `sec:cdf` 는 비교 도구만).
- 절 번호 이동: 새 절이 `sec:center` 앞에 들어가므로 기존 "2.3.2 부호와 방향"의 번호가 뒤로 밀린다.
  AC-W11은 제목 텍스트 기준이라 그대로 성립한다. 본문 어디에도 번호를 손으로 쓴 곳이 없다(`\Cref` 만 씀).
- 재계산 도구: 이 에이전트에는 셸이 없어 `uv run python -c` 를 돌리지 못했다. §4의 값은 정확한 분수(손 계산으로 확정)와
  붓꽃(Iris) 값(슬라이드 값 + 손 계산)으로 나뉜다. 붓꽃 값은 T14가 스크립트에서 다시 계산해 확정한다(§4.3의 한 줄).

## 1. 장 뼈대 (최종 순서)

`[새]` = 이번에 추가, `[기존]` = 한 줄도 안 바뀜.

1. `[새]` 장 In brief: `\label{ch:descriptive}`(2행) 바로 뒤, 기존 도입 문단(4행) 앞.
2. `[기존]` 도입 문단 + `keyidea` (4~15행).
3. `[새]` `\section{배경}` `sec:desc-background`: 15행 `\end{keyidea}` 뒤, 17행 `% ===` 앞.
4. `[새]` `\section{확률변수}` `sec:random-variable` (슬라이드 4~5).
5. `[새]` `\section{확률질량함수와 확률밀도함수}` `sec:pmf-pdf` (슬라이드 6~8, 15의 기댓값).
6. `[새]` `\section{누적분포함수}` `sec:cdf-def` (슬라이드 9~11, 18의 중앙값 CDF 정의).
7. `[기존]` `sec:center` (평균과 중앙값).
8. `[기존]` `sec:spread` (표준편차와 IQR, `subsec:fence`).
9. `[새]` `\section{최빈값과 범위}` `sec:mode-range` (슬라이드 19, 20, 13 저항성 종합표): 155행 `\end{pitfall}` 뒤, 157행 `% ===` 앞.
10. `[기존]` `sec:skewness` (`sec:skew-compute`, **`sec:skew-sign` 불가침**, `sec:skew-rule`).
11. `[기존]` `sec:missing`.
12. `[새]` `\section{어떻게 적용하는가}` `sec:desc-apply`: 553행 `\end{keyidea}` 뒤, 555행 `% ===` 앞.
13. `[새]` `\section{앞으로}` `sec:desc-future`: 12번 바로 뒤.
14. `[기존]` `\section{요약}` (라벨 없음, 장의 마지막으로 남긴다).

AC-W8 순서(background → why/what → apply → future)는 1, 3, 4~11, 12, 13으로 충족한다. "왜 필요한가(Why)"는 채우기
규칙대로 기존 절이 맡고, 새 확률 절 셋은 각자 In brief의 Why와 `\paragraph{고치는 문제.}` 로 원칙 8을 지킨다.

## 2. 절별 설계

### 2.1 장 In brief (새)

- 형식: 이 책의 기존 관례인 `\begin{inbrief}...\end{inbrief}` (lec07 5~21행과 같게). AC-W8 문구는
  `\paragraph{In brief.}` 이지만 책 전체가 `inbrief` 환경을 쓴다. 소유자 질문 O3.
- 네 줄 내용:
  - Why: 데이터를 몇 개의 숫자로 줄이려면, 먼저 "값이 나올 가능성"을 적는 언어(확률변수, PMF, PDF, CDF)가 필요하다.
  - When: 새 데이터를 받아 첫 요약표를 만들 때, 그리고 분포 모형이나 검정으로 넘어가기 전.
  - Where: 주사위, 붓꽃 꽃받침 길이(Sepal Length), 과제 데이터의 `sugars`.
  - How: 확률변수로 값을 정의하고, PMF/PDF와 CDF로 분포를 적은 뒤, 중심(평균, 중앙값, 최빈값)과 퍼짐(범위, 표준편차, IQR)을 저항성(Resistance) 기준으로 고른다.
- `% source: deck 4 slide 1` 주석 (슬라이드 1은 제목뿐).

### 2.2 `sec:desc-background` 배경 (새)

- 출처 문장: `notes_text/4_BasicStats/slides.md` (23 슬라이드). 슬라이드 그림 다수가 교재 그림처럼 보이지만 슬라이드가 문헌을
  밝히지 않으므로 참고문헌 항목을 만들지 않는다(원칙 12).
- 선행 개념 한 줄 요약 + `\Cref`:
  - 속성(Attribute)과 척도: `\Cref{ch:attributes}`, `\Cref{sec:attr-numeric}` (둘 다 존재 확인).
  - 데이터 행렬 $n\times d$ (슬라이드 2): 01의 T12가 만들 `sec:data-matrix` 가 T15 시점에 존재하면 `\Cref`, 없으면
    `\Cref{ch:attributes}` 로 대체. **T15 writer가 grep으로 확인**한다(현재 01에는 없음).
  - 붓꽃 데이터(Iris, 슬라이드 3): 150개 꽃, 꽃받침 길이 4.3~7.9 cm. 한 줄 소개.
- 비유: `\analogy{지도}` 를 이어 쓴다(02 5행과 같은 비유). 확률분포 = 지형 전체, 요약값 = 지도에 찍은 몇 개의 표지.
- `% source: deck 4 slide 1-3`.

### 2.3 `sec:random-variable` 확률변수 (새, 슬라이드 4~5)

- In brief: Why(관측값을 계산 가능한 숫자로 바꾸는 규칙이 필요), When(속성을 수식에 넣기 전), Where(수치형 속성은 그대로,
  조건 판정은 0/1로), How(표본공간의 각 결과에 실수 하나를 대응).
- `\paragraph{고치는 문제.}`: "꽃받침이 길다"는 말은 계산할 수 없다. 규칙을 숫자로 바꿔야 셀 수 있다.
- `def:random-variable`: \term{확률변수}(Random Variable) $X:\mathcal{O}\to\mathbb{R}$, \term{표본공간}(Sample Space) $\mathcal{O}$.
  \term{이산 확률변수}(Discrete Random Variable) vs \term{연속 확률변수}(Continuous Random Variable).
  \term{항등 확률변수}(Identity Random Variable) $X(v)=v$: 수치형 속성은 기본적으로 이것이다(슬라이드 4).
- `ex:iris-long-sepal`: $A(v)=0$ ($v<7$), $1$ ($v\ge 7$). 값이 $\{0,1\}$ 뿐이므로 이산이다.
- 연속 예고: 삼각형 밀도(슬라이드 5)는 `sec:pmf-pdf` 의 `ex:triangle-pdf` 로 넘긴다(한 개념 = 한 자리).
- 주의 한 줄(pitfall 아님, 본문 문장): 슬라이드 5는 표본공간을 $[4.3, 7.9]$ 로 적고 슬라이드 4는 $\mathcal{O}=\mathbb{R}$ 로 적는다.
  $[4.3,7.9]$ 는 관측된 범위이고, 정의상 표본공간은 가능한 모든 결과다. §5 C2.
- `% source: deck 4 slide 4-5`.

### 2.4 `sec:pmf-pdf` 확률질량함수와 확률밀도함수 (새, 슬라이드 6~8, 15)

- In brief: Why(값마다 "얼마나 자주"를 적는 함수), When(이산이면 PMF, 연속이면 PDF), Where(주사위, 붓꽃 0/1, 연속 측정값),
  How(PMF는 더하고 PDF는 적분한다).
- `\paragraph{고치는 문제.}`: 연속값에서는 한 점의 확률이 0이므로 "그 값이 나올 확률"이라는 질문이 성립하지 않는다.
  그래서 이산과 연속이 다른 함수를 쓴다.
- `def:pmf`: \term{확률질량함수}(Probability Mass Function, PMF) $f(x)=P(X=x)$, $f(x)\ge 0$, $\sum_x f(x)=1$.
- `ex:iris-long-sepal` 이어서(같은 예제의 후반, 또는 `ex:iris-bernoulli` 새 라벨): 13/150과 137/150 계산을 한 줄씩(원칙 10).
  이것이 \term{베르누이 분포}(Bernoulli Distribution)라는 말은 `\Cref{sec:binomial}` 로 한 줄 예고만.
- `def:pdf`: \term{확률밀도함수}(Probability Density Function, PDF) $P(X\in[a,b])=\int_a^b f(x)\,dx$, $\int f=1$, $P(X=v)=0$.
- `ex:triangle-pdf`: $f(x)=x$ ($0\le x\le1$), $2-x$ ($1<x\le2$), 0 그 밖. 넓이 $1/2+1/2=1$ 확인,
  $P(0.5\le X\le 1.5)=0.75$ 계산(원칙 4의 작은 예). `\Cref{fig:triangle-pdf-cdf}`.
- 하위 `\subsection{기댓값}` `subsec:expectation` (슬라이드 15): $E[X]=\sum x f(x)$, $\int x f(x)\,dx$.
  주사위 3.5, 삼각형 1. 마무리 한 줄: 표본에서 이것을 추정한 것이 `\Cref{def:center}` 의 평균이다(슬라이드 16의 $\hat\mu$).
  슬라이드 15는 A04 범위(4~11, 19, 20) 밖이지만 02에 없는 내용이라 슬라이드 지도가 "부분"이 된다. 넣을지 O5.
- 짧은 pitfall `pit:pdf-not-prob`(선택): PDF 값 자체는 확률이 아니다(1을 넘을 수 있다). 숫자 예는 폭 0.5의 균등 밀도 2.
- `% source: deck 4 slide 6-8, 15`.

### 2.5 `sec:cdf-def` 누적분포함수 (새, 슬라이드 9~11, 18)

이 절이 04 `sec:cdf`, lec07 `sec:dist-check-cdf`, lec11 `def:ecdf` 가 가리킬 **유일한 CDF 정의 자리**다.

- In brief: Why(이산과 연속을 한 함수로 다루고, "이하일 확률"을 바로 읽기 위해), When(분포 비교, 분위수, 중앙값을 구할 때),
  Where(주사위, 붓꽃 정규 근사, 이후 KS 검정), How(PMF는 누적합, PDF는 누적적분).
- `\paragraph{고치는 문제.}`: PMF와 PDF는 이산/연속에서 다른 물건이라 같은 축에 겹쳐 비교할 수 없다. CDF는 둘 다 $[0,1]$ 값을 준다.
- `def:cdf`: \term{누적분포함수}(Cumulative Distribution Function, CDF) $F(x)=P(X\le x)$, $F:\mathbb{R}\to[0,1]$.
  이산: $\sum_{u\le x} f(u)$. 연속: $\int_{-\infty}^{x} f(u)\,du$. 성질 세 줄: 감소하지 않는다, $F(-\infty)=0$, $F(\infty)=1$.
- `ex:dice-cdf` (슬라이드 10): `tab:dice-cdf` 표 한 개. 열 = $k$, $P(X=k)$, $F(k)=P(X\le k)$. 행 1~6 + "$a<1$ → 0", "$a>6$ → 1".
  비정수 한 줄: $F(3.5)=F(3)=3/6$ (계단이 정수 사이에서 평평함). `\Cref{fig:dice-pmf-cdf}`.
- `ex:cdf-fifteenths` (슬라이드 11): $P(X=x)=x/15$, $x\in\{1,\dots,5\}$. 계산 줄(원칙 10, `align*`):
  $1+2+3+4+5=15$ (합이 1인지 확인), $F(3)=1/15+2/15+3/15=6/15=0.4$, $P(X>3)=1-F(3)=0.6$,
  교차 확인 $P(4)+P(5)=4/15+5/15=9/15=0.6$.
- `pit:cdf-strict` (필수): 이산에서는 $>$ 와 $\ge$ 가 다르다. $P(X\ge 3)=1-F(2)=1-3/15=12/15=0.8\ne 0.6$.
- `pit:cdf-slide-kx` (Q4 형식, §5 E1): 슬라이드 식 $P(X>k)=1-P(X\le x)$ 는 좌우 변수가 다르다. 올바른 식은 $P(X>x)=1-F(x)$.
  문구(AC-W7 grep과 글자 그대로 맞춤): "슬라이드 값은 $P(X>k)=1-P(X\le x)$, 다시 계산하면 $P(X>x)=1-F(x)$, 즉 $P(X>3)=0.6$".
  숫자 결과 0.6은 맞다.
- 중앙값 연결 (슬라이드 18): `definition` 환경을 쓰지 않는다(중앙값의 정의 자리는 `def:center` 하나).
  `\paragraph{중앙값을 CDF로 읽기.}` 성질 서술로 쓰고 `\Cref{def:center}` 를 가리킨다. 중앙값 $m$ 의 CDF 성질 $P(X\le m)\ge 1/2$, $P(X\ge m)\ge 1/2$. 주사위에서는 $3\le m\le 4$ 전부가
  조건을 만족하고, 관례로 3.5를 쓴다. 정규분포 CDF에서 $F(\mu)=0.5$ 이므로 중앙값 = 평균(슬라이드 9 그림의 $(5.84, 0.5)$).
  마무리로 `\Cref{sec:center}` 를 가리킨다. 이 문단은 `sec:center` 본문을 고치지 않고 앞에서 다리를 놓는다.
- 붓꽃 그림 두 개(슬라이드 9): 이항 CDF($p=0.087$, $m=10$)와 정규 CDF($\mu=5.84$, $\sigma^2=0.681$). `\Cref{fig:iris-cdfs}`.
  이항과 정규의 자세한 설명은 `\Cref{sec:binomial}`, `\Cref{sec:normal}` 로 넘긴다.
- 분산 관례 pitfall `pit:variance-n` (§5 C1): $\sigma^2=0.681$ 은 $n$ 으로 나눈 값이다. 문구
  "슬라이드 값은 0.681($n$ 으로 나눔), $n-1$ 로 다시 계산하면 0.686". `\Cref{def:spread}` 와 `\Cref{pit:bias}` 를 가리킨다
  (둘 다 존재 확인). 오류가 아니라 관례 차이임을 문장으로 밝힌다.
- 앞으로 가는 링크 한 줄: 두 CDF의 최대 격차 비교는 `\Cref{sec:cdf}`, 경험적 CDF는 `\Cref{def:ecdf}`.
- `% source: deck 4 slide 9-11, 18`.

### 2.6 `sec:mode-range` 최빈값과 범위 (새, 슬라이드 19, 20, 13 종합)

- 위치 근거: 중심(`sec:center`)과 퍼짐(`sec:spread`)을 모두 본 뒤에 "저항성 성적표"로 두 절을 이어 준다. 기존 두 절 안에
  subsection을 덧붙이는 대안은 O1.
- In brief: Why(평균, 중앙값 말고 범주형에도 쓰는 중심, 가장 단순한 퍼짐), When(범주형이면 최빈값, 빠른 1차 점검이면 범위),
  Where(최빈값은 명목 척도, `\Cref{tab:attr-ops}`), How(가장 많이 나온 값을 세고, 최댓값에서 최솟값을 뺀다).
- `def:mode`: \term{최빈값}(Mode). 확률변수: PMF/PDF가 최대인 값. 표본: $\operatorname{mode}(X)=\arg\max_x \hat f(x)$.
  `\operatorname` 대신 preamble에 `\DeclareMathOperator` 가 있는지 writer 확인(latex.md §5).
- `def:range`: \term{범위}(Range) $r=\max X-\min X$.
- `ex:mode-range`: 붓꽃 꽃받침 길이. 최빈값 5.0 cm (10송이), 범위 $7.9-4.3=3.6$ cm (T14 확정, §4.3).
- `ex:resistance` 데이터를 재사용한 비교(원칙 5, 같은 예 유지): $\{1,2,3,4,5\}\to\{1,2,3,4,100\}$ 에서 범위 $4\to 99$.
  최빈값은 이 데이터에서 정의되지 않으므로(모든 값이 한 번씩) 별도 예 $\{1,2,2,3,5\}\to\{1,2,2,3,100\}$: 최빈값 2 그대로, 범위 $4\to 99$.
- `tab:robustness` 저항성 성적표 (슬라이드 13, 16, 18, 19, 20, 21 종합): 행 = 평균, 중앙값, 최빈값, 범위, 표준편차, IQR.
  열 = 통계량(영문 병기), 극단값 하나에 흔들리는가, 근거(`\Cref`). 평균/표준편차/범위 = 흔들림, 중앙값/IQR/최빈값 = 안 흔들림.
- `pit:mode-unstable` (§5 C3): 최빈값은 극단값에는 강하지만 **극단값이 아닌 값 하나**에 뒤집힌다.
  $\{1,2,2,3,3,3\}$ 은 최빈값 3, 3 하나를 2로 바꾼 $\{1,2,2,2,3,3\}$ 은 최빈값 2. 연속 측정값에서는 모든 값이 한 번씩이면
  최빈값이 정의되지 않고, 붓꽃처럼 소수 한 자리로 반올림돼야 의미가 생긴다.
- `% source: deck 4 slide 13, 19-20` (슬라이드 13은 `sec:center` 에도 주석으로 추가, §3).

### 2.7 `sec:desc-apply` 어떻게 적용하는가 (새)

- 과제와 연결: HW1 요약표(`\Cref{ch:hw1}`, `\Cref{sec:hw1-q2}` 등, writer가 해당 절 내용 확인 후 고름),
  HW2 추정량(`\Cref{sec:hw2-estimators}`), HW2 분포 비교 방법(`\Cref{sec:hw2-compare-how}`).
- 다른 장과 연결: 경험적 CDF로 후보 분포 보기 `\Cref{sec:dist-check-cdf}`, 이산화 경계(0/1 확률변수 $A$ 와 같은 발상)
  `\Cref{sec:discretization}`, 최빈값 대체 `\Cref{sec:impute}`, 히스토그램 = 경험적 PDF `\Cref{sec:histogram}`, 분위수 = CDF의 역 `\Cref{sec:quantile}`.
- 짧은 코드 한 블록(선택): `pandas` 의 `.mode()`, `.max()-.min()`, `(x>=7).mean()`. 결과 숫자는 §4.3 값과 같아야 한다.

### 2.8 `sec:desc-future` 앞으로 (새)

- 이항, 정규 등 이름 있는 분포: `\Cref{sec:binomial}`, `\Cref{sec:normal}`, `\Cref{ch:distributions}`.
- 두 CDF 비교와 KS: `\Cref{sec:cdf}`, `\Cref{sec:cd-ks}`.
- 표본 평균이 모평균을 얼마나 잘 맞히는가(슬라이드 16의 불편추정량 Unbiased Estimator)는 검정으로 이어진다: `\Cref{ch:hypothesis}`.

## 3. 슬라이드 지도 (1~23)

| 슬라이드 | 내용 | 자리 | 상태 |
| :-- | :-- | :-- | :-- |
| 1 | 제목 | 장 In brief `% source` | 내용 없음 |
| 2 | 데이터 행렬 $n\times d$ | `sec:desc-background` 한 줄 + `ch:attributes` (또는 `sec:data-matrix`) | 덱 3이 본체 |
| 3 | 붓꽃 데이터 | `sec:desc-background` | 새 |
| 4 | 확률변수 정의, 이산/연속, 항등 확률변수 | `sec:random-variable` `def:random-variable` | 새 |
| 5 | 이산 예 $A(v)$, 연속 밀도 예 | `ex:iris-long-sepal`, `ex:triangle-pdf` | 새 |
| 6 | PMF 정의 | `def:pmf` | 새 |
| 7 | 붓꽃 PMF 13/150 | `ex:iris-long-sepal` 후반 | 새 |
| 8 | PDF 정의, $P(X=v)=0$ | `def:pdf` | 새 |
| 9 | CDF 정의, 이항/정규 CDF 그림 | `def:cdf`, `fig:iris-cdfs`, `pit:variance-n` | 새 |
| 10 | 주사위 CDF | `ex:dice-cdf`, `tab:dice-cdf`, `fig:dice-pmf-cdf` | 새 |
| 11 | $x/15$ 예, $F(3)=0.4$, $P(X>3)=0.6$ | `ex:cdf-fifteenths`, `pit:cdf-slide-kx`, `pit:cdf-strict` | 새 |
| 12 | 절 제목 "Descriptive Statistics" | 없음 | 내용 없음 |
| 13 | 저항성(Robust) 정의 | `sec:center` 기존 44~45행 (주석만 추가) + `tab:robustness` | 기존 + 새 표 |
| 14 | 일변량 분석(Univariate Analysis) 그림 | `sec:desc-background` 한 줄(한 열 = 한 확률변수) | 새(한 줄) |
| 15 | 기댓값 정의, 주사위 3.5, 삼각형 1 | `subsec:expectation` | 새 (O5) |
| 16 | 표본 평균, 불편추정량, 저항성 없음 | `def:center`, `ex:resistance` (주석만), `sec:desc-future` 한 줄 | 기존 |
| 17 | 붓꽃 평균 5.843 점그림 | `ex:mode-range` 에서 평균과 최빈값 비교 한 줄 | 새(한 줄) |
| 18 | 중앙값 CDF 정의, 저항성 있음 | `sec:cdf-def` 중앙값 문단 + `def:center` (주석만) | 기존 + 새 |
| 19 | 최빈값 정의, 저항성 | `def:mode`, `pit:mode-unstable` | 새 |
| 20 | 범위 정의, 저항성 없음 | `def:range`, `ex:mode-range` | 새 |
| 21 | 분산, 표준편차 ($1/n$) | `def:spread` (주석만) + `pit:variance-n` | 기존 + 새 |
| 22 | 평균 0, 표준편차가 다른 정규분포 그림 | `sec:spread` 주석만 + `sec:normal` 앞으로 링크 | 기존 |
| 23 | Kahoot 퀴즈 | 없음 | 내용 없음 |

AC-W9: 기존 절(`sec:center`, `sec:spread`)에는 `% source: deck 4 slide 13, 15-18` 과 `% source: deck 4 slide 21-22`
주석 **한 줄만** 덧붙인다(주석 전용 추가, Q2와 W12 성립). 위치는 각 절의 `\label` 다음 줄. `sec:skew-sign` 구간에는 주석도 넣지 않는다.

## 4. 재계산 표

### 4.1 정확한 분수 (손 계산 확정)

| 항목 | 슬라이드 | 다시 계산 | 판정 |
| :-- | :-- | :-- | :-- |
| 주사위 $P(X=k)$ | 1/6 | 1/6 = 0.1667 | 일치 |
| 주사위 $F(1..6)$ | 1/6, 2/6, ..., 6/6 | $k/6$ = 0.167, 0.333, 0.5, 0.667, 0.833, 1 | 일치 |
| 주사위 $P(X<1)$, $F(a), a>6$ | 0, 1 | 0, 1 | 일치 |
| 주사위 $F(3.5)$ | 없음 | 3/6 = 0.5 | 새 값 |
| 주사위 $E[X]$ (슬 15) | 3.5 | 21/6 = 3.5 | 일치 |
| $x/15$ 합 | 없음 | 15/15 = 1 | 새 값 |
| $F(3)$ (슬 11) | 6/15 = 0.4 | 6/15 = 0.4 | 일치 |
| $P(X>3)$ | 0.6 | 1 − 0.4 = 0.6 = 9/15 | 일치 |
| $P(X\ge 3)$ | 없음 | 12/15 = 0.8 | 새 값 (`pit:cdf-strict`) |
| 삼각형 PDF 넓이 | 없음 | 1/2 + 1/2 = 1 | 새 값 |
| 삼각형 $P(0.5\le X\le1.5)$ | 없음 | 1 − 2·(0.5²/2) = 0.75 | 새 값 |
| 삼각형 $E[X]$ (슬 15) | 1/3 + 2/3 = 1 | 1 | 일치 |
| 범위 예 $\{1,2,3,4,5\}\to\{..,100\}$ | 없음 | 4 → 99 | 새 값 |
| 최빈값 예 $\{1,2,2,3,5\}\to\{..,100\}$ | 없음 | 2 → 2 | 새 값 |
| 최빈값 뒤집힘 $\{1,2,2,3,3,3\}\to\{1,2,2,2,3,3\}$ | 없음 | 3 → 2 | 새 값 |

### 4.2 붓꽃 값 (슬라이드 + 손 계산, T14 확정 필요)

| 항목 | 슬라이드 | 손 계산 | T14 확정 방법 |
| :-- | :-- | :-- | :-- |
| 꽃받침 길이 $\ge 7$ 개수 | 13 | 13 (7.0×1, 7.1×1, 7.2×3, 7.3×1, 7.4×1, 7.6×1, 7.7×4, 7.9×1) | `(x>=7).sum()` |
| $f(1)=P(A=1)$ | 13/150 = 0.087 | 0.0867 | `13/150` |
| $f(0)=P(A=0)$ | 137/150 = 0.913 | 0.9133 | `137/150` |
| 평균 $\hat\mu$ (슬 9, 17) | 5.84, 5.843 | 5.8433 | `x.mean()` |
| 분산 $1/n$ (슬 9) | 0.681 | 0.6811 | `x.var(ddof=0)` |
| 분산 $1/(n-1)$ | 없음 | 0.6857 | `x.var(ddof=1)` |
| 최빈값 (슬 17 점그림에서 가장 높은 기둥) | 5.0 (10송이, 그림 판독) | 5.0 | `x.mode()`, `(x==5.0).sum()` |
| 최솟값, 최댓값, 범위 | 4.3, 7.9 (슬 5) | 3.6 | `x.max()-x.min()` |
| 이항 $F(0)$, $p=0.087$, $m=10$ | 그림 약 0.40 | $0.913^{10}=0.4025$ | `scipy.stats.binom.cdf(k,10,0.087)` |
| 이항 $F(1)$ | 그림 약 0.79 | 0.7860 | 같음 |
| 이항 $F(2)$ | 그림 약 0.95 | 0.9504 | 같음 |
| 이항 $F(3)$ | 그림 약 1.0 | 0.9922 | 같음 |
| 정규 $F(\mu)$ | 0.5 | 0.5 | 정의상 |

이항 값은 슬라이드처럼 반올림된 $p=0.087$ 을 쓴다($p=13/150$ 을 쓰면 넷째 자리가 달라진다. 스크립트는 슬라이드 값을 쓰고 주석으로 밝힌다).

### 4.3 T14가 돌릴 확인 한 줄

```
uv run python -c "from sklearn.datasets import load_iris; import pandas as pd; from scipy.stats import binom; x=pd.Series(load_iris().data[:,0]); print((x>=7).sum(), round(x.mean(),4), round(x.var(ddof=0),4), round(x.var(ddof=1),4), x.mode().tolist(), (x==5.0).sum(), x.min(), x.max(), round(x.max()-x.min(),2), [round(binom.cdf(k,10,0.087),4) for k in range(4)])"
```

데이터 적재만 한다(`fit`, 학습 없음). 결과가 §4.2와 다르면 T14는 그림을 만들기 전에 멈추고 보고한다. deck 7의
`check_iris_transcription` 과 같은 sklearn 적재 경로를 쓴다.

## 5. 슬라이드 오류와 관례 차이

| ID | 슬라이드 | 내용 | 책에서 | 형식 |
| :-- | :-- | :-- | :-- | :-- |
| E1 | 11 (image17) | $P(X>k)=1-P(X\le x)$: 좌우 변수 불일치 | `pit:cdf-slide-kx` | Q4: "슬라이드 값은 $P(X>k)=1-P(X\le x)$, 다시 계산하면 $P(X>x)=1-F(x)$, 즉 $P(X>3)=0.6$" |
| C1 | 9, 21 | $\sigma^2=0.681$ 은 $1/n$ 분산. 02 `def:spread` 는 $n-1$ | `pit:variance-n` | "슬라이드 값은 0.681, $n-1$ 로 다시 계산하면 0.686" (오류 아닌 관례 차이라고 명시) |
| C2 | 5 (image3) vs 4 | 표본공간을 $[4.3,7.9]$ 로 적음. 슬라이드 4는 $\mathcal{O}=\mathbb{R}$ | 본문 한 문장 | pitfall 아님 |
| C3 | 19 | "최빈값은 저항성 있음"은 극단값에 대해서만 참. 비극단값 하나에 뒤집히고 연속값에서는 정의가 흔들림 | `pit:mode-unstable` | 보충 pitfall |
| C4 | 7 | 0.087은 0.0867의 반올림 | 본문에 두 값 모두 | 오류 아님 |
| C5 | 5 제목 | "Continuous Random Variable" 아래 그림은 확률변수가 아니라 PDF | 본문에서 PDF로 부름 | 오류 아님, 언급 불필요 |

AC-W7 적용 대상은 E1 하나(수식 오류). C1은 Q4 문구를 빌려 쓰되 "관례 차이"로 표기한다.

## 6. 그림 목록 (T14, `hw1/00_lecture_charts/deck4_basic_stats.py`)

모듈 형태는 deck7_transforms.py와 같게: `from style import ... save`, `__all__ = ["build_all"]`, `build_all() -> list[str]`,
출력 `figures/04_0N_*.png`. 현재 `04_0` 접두 파일과 스크립트는 없음(grep 확인). TikZ 그림은 없다(흐름도 없음).

| 파일 | 라벨 | 내용 | 슬라이드 |
| :-- | :-- | :-- | :-- |
| `04_01_dice_pmf_cdf.png` | `fig:dice-pmf-cdf` | 두 패널: 주사위 PMF 막대(1/6 여섯 개), CDF 계단(열린/닫힌 점, $x<1$ 에서 0, $x>6$ 에서 1) | 10 |
| `04_02_triangle_pdf_cdf.png` | `fig:triangle-pdf-cdf` | 두 패널: 삼각형 PDF (색칠 $[0.5,1.5]$, 넓이 0.75), 그 CDF ($F(1)=0.5$ 표시) | 5, 15 |
| `04_03_iris_cdfs.png` | `fig:iris-cdfs` | 두 패널: 이항 CDF 계단($p=0.087$, $m=10$), 정규 CDF($\mu=5.843$, $\sigma^2=0.681$, $(\mu,0.5)$ 점) + 붓꽃 경험적 CDF 겹침(선택) | 7, 9 |
| `04_04_iris_mode_range.png` | `fig:iris-mode-range` | 붓꽃 꽃받침 길이 빈도 막대(0.1 cm 단위), 최빈값 5.0 강조, 평균 5.843 선, 최소 4.3과 최대 7.9에 범위 화살표 3.6 | 17, 19, 20 |

캡션은 한국어 + 영어 병기(AC-W5). 모든 그림은 본문에서 `\Cref` 한다(AC-W10).

## 7. `\Cref` 대상 확인 결과 (2026-09-24 grep)

존재 확인: `ch:attributes`, `sec:attr-numeric`, `tab:attr-ops`, `ch:descriptive`, `sec:center`, `def:center`, `ex:resistance`,
`sec:spread`, `def:spread`, `pit:bias`, `ch:distributions`, `sec:normal`, `sec:binomial`, `sec:cdf`, `sec:histogram`,
`sec:quantile`, `sec:dist-check-cdf`, `sec:discretization`, `sec:impute`, `def:ecdf`, `sec:cd-ks`, `ch:hypothesis`,
`ch:hw1`, `sec:hw1-q2`, `ch:hw2`, `sec:hw2-estimators`, `sec:hw2-compare-how`, `tab:analogy`(02 5행에서 이미 사용).

없음(쓰지 말 것, 또는 T15 시점에 재확인): `sec:data-matrix`(01 T12 예정).

새 라벨 충돌 검사: `sec:desc-*`, `sec:random-variable`, `sec:pmf-pdf`, `sec:cdf-def`, `sec:mode-range`, `def:pmf`, `def:pdf`,
`def:cdf`, `def:mode`, `def:range`, `ex:dice-*`, `ex:iris-long-sepal`, `ex:triangle-pdf`, `ex:cdf-fifteenths`,
`subsec:expectation`, `pit:cdf-strict`, `pit:cdf-slide-kx`, `pit:variance-n`, `pit:pdf-not-prob`, `pit:mode-unstable`,
`tab:robustness`, `tab:dice-cdf`, `fig:iris-cdfs`, `fig:iris-mode-range`, `ex:iris-bernoulli` 모두 `chapters/` 에 없음(grep 0건, 두 번 확인).

## 8. T15 수용 기준에 더할 항목 (pm 참고)

- 새 라벨 전부 존재: `sec:desc-background`, `sec:random-variable`, `sec:pmf-pdf`, `sec:cdf-def`, `def:cdf`, `ex:dice-cdf`,
  `ex:cdf-fifteenths`, `sec:mode-range`, `def:mode`, `def:range`, `tab:robustness`, `sec:desc-apply`, `sec:desc-future`.
- 숫자 존재: 0.4, 0.6, 0.8(`pit:cdf-strict`), 3.5, 0.75, 0.0867, 0.9133, 0.681, 0.686, 5.0, 3.6, 99.
- `git diff -U0` 의 삭제 줄 0개, `sec:skew-sign` 구간 hunk 0개.
- PLAN.md T15 AC의 "04 `sec:cdf` 가 이 장의 CDF 정의로 `\Cref`" 는 04 파일을 고치는 일이라 T15의 출력(02만)과 맞지 않는다. O4.

## 9. 소유자 질문

- **O1** 최빈값과 범위를 새 절 `sec:mode-range`(`sec:spread` 뒤)로 둘지, `sec:center` 와 `sec:spread` 끝에 subsection으로 덧붙일지.
  설계 기본값은 새 절(Q2 "본문 불변"을 가장 엄격하게 지킴).
- **O2** (참고, 기본값으로 진행 가능) `sec:desc-apply`, `sec:desc-future` 는 기존 `\section{요약}` 앞에 둔다. 근거: `\section{요약}` 은
  02, 03, 04에만 있고 lec 장에는 없다(grep). 채우는 장은 기존 요약을 마지막에 남기는 편이 본문 불변 원칙과 맞다. 반대 의견이 있으면 답해 주면 된다.
- **O3** 장 In brief 형식: AC-W8 문구 `\paragraph{In brief.}` 와 책 관례 `inbrief` 환경이 다르다. 기본값은 `inbrief` 환경(lec07과 같음).
- **O4** 04 `sec:cdf` 에 `\Cref{sec:cdf-def}` 한 줄을 넣는 일은 누구의 몫인가: T15(02만 출력)인가, 04 채우기(U2)인가.
  lec11 49행 "누적분포함수(`sec:cdf`)를 이미 안다"도 정의 자리가 02로 옮겨지면 대상이 어긋나지만 본문 불변 규칙으로 그대로 둔다.
- **O5** 슬라이드 15의 기댓값($E[X]$, 주사위 3.5, 삼각형 1)을 `subsec:expectation` 으로 넣을지. A04 범위(4~11, 19, 20) 밖이지만 02에 없는 내용이다.
- **O6** 기존 도입 문단 8~9행 "이 장은 네 가지 요약값을 다룬다"는 새 확률 절이 들어가면 불완전해진다. 본문 불변이라 그대로 두고
  장 In brief와 배경이 범위를 바로잡게 할지(기본값), 한 줄 수정을 허용할지.
- **O7** 재계산을 셸 없이 손으로 했다. 붓꽃 값(§4.2)의 최종 확정을 T14 스크립트 출력에 맡기는 것을 받아들이는지.

## 결정 기록 (2026-09-24, 메인 세션, 소유자 기존 결정에서 도출)

- **최빈값과 범위 배치:** 설계안대로 새 절 `sec:mode-range`로 둔다.
- **In brief 형식:** book.md 원칙 7과 기존 장의 `inbrief` 환경을 따른다.
- **04 `sec:cdf`와의 연결:** 02의 새 `def:cdf`가 04의 `\Cref{sec:cdf}`를 가리킨다. 04 쪽에서 02를 가리키는 줄은 T09(04 채우기)가 넣는다.
- **슬라이드 15 기댓값:** 넣는다 (강의 노트 하나 = 장 하나, 슬라이드 내용 누락 금지).
- **도입 문단 8~9행 수정:** 하지 않는다 (Q2: 기존 본문 불변). 필요한 말은 새 줄로 더한다.
- **손 계산 값:** T14 스크립트가 계산한 값이 이긴다. 다르면 둘 다 보고한다.
