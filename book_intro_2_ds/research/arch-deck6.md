# A06: architecture.md §4.3 addendum (deck 6 → `chapters/04-distributions.tex`)

작성: system-architect, 2026-09-24, cycle 1/2. 설계 문서다. LaTeX, PLAN.md는 고치지 않았다.
architecture.md §4.3 항목 1–10을 **대체하지 않고 보강**한다. 둘이 어긋나면 이 문서의 해당 행이
더 구체적인 값이며, 어긋남은 §6과 §7에 적었다.

## 0. 입력과 전제

- 원천: `notes_text/6_DataDistribution/slides.md`(슬라이드 30장) + `media/`. 이번에 직접 본 그림:
  image4(아기/성인 키), image5(정규 곡선 눈금), image8(왜도 세 모양), image15/16(웃는 시간 표와
  히스토그램), image17–19(균등분포 PDF, 평균, 분산), image21(지수분포 평균 유도), image26(지수분포
  $\mu=20$), image52/53(이항 평균, 분산).
- 대상: `chapters/04-distributions.tex`(58줄 초안). 현재 라벨: `ch:distributions`, `sec:normal`,
  `def:normal`, `sec:exponential`, `sec:uniform`, `sec:binomial`, `sec:cdf`. `요약` 절은 라벨 없음.
  **모든 기존 라벨은 유지한다**(다른 장이 가리킨다, §5.2).
- 결정 Q2(뼈대는 앞뒤에만 추가, 기존 절 본문은 그대로), Q4(오류는 `pitfall` 상자, "슬라이드 값은
  X, 다시 계산하면 Y"), 절 순서 유지(§4.3 머리말), 라벨 접두사 `dist`(PLAN §1 pm 결과).
- 그림 규칙: 한 그림은 처음 쓰는 장에서 한 번만 라벨을 단다. `06_01_normal_fit.png`는 lec07의
  `fig:normal-fit`이므로 04는 `\Cref{fig:normal-fit}`만 쓰고 `\includegraphics`하지 않는다.

## 1. 슬라이드 대응표 (1–30)

"위치"는 T09 후 04 안의 절/라벨. `% source: deck 6 slide K` 주석을 그 자리에 둔다(AC-W9).

| 슬라이드 | 내용 | 04 안의 위치 | 비고 |
| :-- | :-- | :-- | :-- |
| 1 | 제목 "Data and Distributions" | 없음 (내용 없음) | 제목만 |
| 2 | 분포 = 측정값의 확률이 퍼진 모양, 가장 높은 곳 = 가장 흔한 값 | `sec:dist-background` 안 `\paragraph{왜 분포인가.}` | 장 In brief의 Why 재료 |
| 3 | 흔한 분포 목록: 연속(정규, 균등, 지수, 멱법칙), 이산(베르누이, 이항) | `sec:dist-background` | 표 `tab:dist-map`(분포, 연속/이산, 이 장의 절 `\Cref`)로 둔다. 읽는 순서가 슬라이드 순서와 다르다는 것도 여기서 한 줄로 밝힌다 |
| 4 | 정규 = 가우스 = 종 곡선, 자연에 흔함 | `sec:normal` 첫 문단 | |
| 5 | 세로축 = 상대적 가능성 | `sec:normal` | 밀도는 확률이 아니라 "넓이가 확률"임을 여기서 푼다(원칙 9a) |
| 6 | 아기/성인 키 두 곡선, 중심 = 평균, 폭 = 표준편차, 아기 곡선이 더 높은 이유 | `sec:normal` | 넓이 1 원리로 설명(§6 E5) |
| 7 | ±2 SD 안에 95% | `sec:normal` + `pitfall`(Q4) | `fig:dist-sigma-bands`. 슬라이드 그림(image5) 자체는 1.96σ = 95%로 맞게 그려져 있다 |
| 8 | 이동과 척도 변환 | `sec:normal` | $Z=(X-\mu)/\sigma$ 한 줄 + `\Cref{sec:normalization}` |
| 9 | "Bending": 양/대칭/음의 왜도 세 모양 | `sec:normal` 끝 한 문단 | 정규가 아닌 모양의 예고. `\Cref{sec:skewness}`, `\Cref{sec:skew-sign}`만 건다. 02의 2.3.2는 건드리지 않는다(AC-W11) |
| 10 | 정규 PDF | `sec:normal`의 기존 `def:normal` | 이미 있음. 주석만 추가 |
| 11 | 이산 균등: 주사위 $1/6$, 합 = 1 | `sec:uniform` | `fig:dist-uniform` 왼쪽 패널 |
| 12 | 연속 균등 $[0,5]$ 예제 | `sec:uniform` `example` | `fig:dist-uniform` 오른쪽 패널. 표기 오류 §6 E6 |
| 13 | 생후 8주 아기의 웃는 시간 55개, 히스토그램, 난수 생성 | `sec:uniform` `example` | 슬라이드를 출처로 인용. 값은 §3 R8 |
| 14 | 일반 평균 $(\alpha+\beta)/2$, 분산 $(\beta-\alpha)^2/12$ | `sec:uniform` | 기호는 $[a,b]$로 쓴다(lec07의 기호 충돌 함정, §5.1) |
| 15 | 지수분포 = 사건 사이 시간, "$0<\lambda\le1$", 평균 | `sec:exponential` + `pitfall`(Q4) | §6 E2 |
| 16 | 노트북 수명 예제 | `sec:exponential` `example` | R1 |
| 17 | 커피숍 예제 | `sec:exponential` `example` + `pitfall`(Q4) | R2, R3, §6 E1 |
| 18 | 첫 방문자 1분 단위 확률 | `subsec:geometric`(신설, `sec:exponential` 안) | 표 `tab:dist-geometric`, 근사이지 오류 아님 |
| 19 | 멱법칙 = 파레토, 80/20 | `sec:powerlaw`(신설, `sec:exponential` 뒤) | |
| 20 | $\alpha>1$, $x_{\min}$, 도시 인구 | `sec:powerlaw` | 식은 `sec:hw2-estimators`와 같은 꼴 |
| 21 | 여집합 CDF 예(단어 빈도), Newman 강의 노트 | `sec:powerlaw` | 출처는 "슬라이드가 인용한 자료"로만, bib 없음 |
| 22 | 멱법칙 대 지수, Clauset 강의 노트 | `sec:powerlaw` | `fig:dist-powerlaw` |
| 23 | 베르누이 정의 | `sec:binomial` | |
| 24 | 호감도 예제, 평균 0.6, 분산 0.24 | `sec:binomial` `example` | R11, R12 |
| 25 | 베르누이 일반 평균/표준편차, PMF | `sec:binomial` | $p$, $p(1-p)$ |
| 26 | 이항 = 독립 시행 $n$번의 성공 수 | `sec:binomial` | `fig:dist-bernoulli-binomial` |
| 27 | 5번 중 특정 순서 하나 | `sec:binomial` `example` | R13 |
| 28 | 순서 무관 → 조합 | `sec:binomial` `example` | R14 |
| 29 | 이항 평균 $np$, 분산 $np(1-p)$ | `sec:binomial` | image52/53 확인 |
| 30 | "Kahoot Time" | 없음 (내용 없음) | 수업 퀴즈 |

`sec:cdf`에 대응하는 슬라이드는 없다(덱 6은 CDF를 지수분포 예제의 계산 도구로만 쓴다, 슬라이드
16–17). `sec:cdf`는 기존 TODO(그림 `06_03_cdf.png`, KS 통계량 $D$)를 채우는 절이며 주석은
`% source: deck 6 slide 16-17 (CDF as tool); figure from hw1 data`로 둔다.

## 2. 뼈대와 절별 작업

### 2.1 최종 절 순서 (T09 후)

```
\chapter + \label{ch:distributions}          기존, 그대로 (제목 줄표는 Q6/X01 소관)
keyidea                                      기존, 그대로
\paragraph{In brief.} (장 머리, 4줄)          신설  ← 기존 7행 뒤
\section 배경   \label{sec:dist-background}   신설  (슬라이드 2–3, 선행 개념, 왜 분포인가)
\section 정규분포 \label{sec:normal}            기존 + 본문 추가
\section 지수분포 \label{sec:exponential}       기존 + 본문 추가
   \subsection 기하분포 \label{subsec:geometric}  신설
\section 멱법칙 \label{sec:powerlaw}           신설
\section 균등분포 \label{sec:uniform}           기존 + 본문 추가
\section 베르누이와 이항분포 \label{sec:binomial} 기존 + 본문 추가
\section 누적분포함수로 비교하기 \label{sec:cdf}  기존 + 본문 추가
\section 요약                                 기존, TODO 자리를 요약 표로 채움 (라벨 tab:dist-summary)
\section 어떻게 적용 \label{sec:dist-apply}     신설  ← 파일 끝
\section 앞으로 \label{sec:dist-future}         신설  ← 파일 끝
```

- AC-W8 "새 개념 절은 In brief로 연다": 초안 절 넷(`sec:exponential`, `sec:uniform`, `sec:binomial`,
  `sec:cdf`)과 신설 `sec:powerlaw`는 각각 `inbrief` 환경(04:13, lec07:189와 같은 환경) 네 줄로 연다.
  `sec:normal`은 기존 `inbrief`의 TODO를 채운다. `subsec:geometric`은 선택. 장 머리만
  `\paragraph{In brief.}`(AC-W8 첫 문장).
- 별도의 "왜" 절은 만들지 않는다. Q2가 추가 부품을 넷(In brief, 배경, 어떻게 적용, 앞으로)으로
  정했고 AC-W8은 채우기에서 "why/what은 기존 절"이라고 한다. §4.3 항목 1의 "왜"는
  `sec:dist-background` 안의 `\paragraph{왜 분포인가.}`로 둔다.
- `어떻게 적용`과 `앞으로`는 `요약` **뒤**에 둔다. 그래야 AC-W8의 "apply, future가 마지막" 순서가
  기존 `요약` 위치를 옮기지 않고 성립한다(§7 Q-D).
- `sec:dist-*` 접두사는 lec07의 `sec:dist-check-hist`, `sec:dist-check-cdf`와 겹치지 않는다(검색
  확인). `sec:powerlaw`, `subsec:geometric`은 PLAN T09가 이름을 정했으므로 그대로 쓴다.

### 2.2 절별: 본문 추가인가, 그대로인가

| 절 | 기존 줄 | 작업 |
| :-- | :-- | :-- |
| 장 머리(1–7행) | 제목, 라벨, keyidea | **그대로.** 7행 뒤에 장 In brief 삽입 |
| `sec:normal` | `inbrief`의 네 TODO, `def:normal`, TODO 주석 2줄, KS `pitfall` | `def:normal`과 KS 함정(Shapiro 문장 포함)은 **한 글자도 바꾸지 않는다**(lec07:220, lec11:701이 "`sec:normal`의 함정"을 가리킨다). `inbrief` 네 줄의 `% TODO`만 채운다(W12가 허용하는 TODO 삭제). 그 밖의 본문(슬라이드 4–9)은 `def:normal` **앞뒤에 추가**. 30–31행 TODO 주석은 그림 참조와 96.0% 문장으로 대체 |
| `sec:exponential` | TODO 주석 1줄뿐 | 본문 전체가 추가(슬라이드 15–17) + `subsec:geometric`. TODO 줄 삭제 |
| `sec:powerlaw` | 없음 | 신설(슬라이드 19–22) |
| `sec:uniform` | TODO 주석 3줄(`serving_size` 함정 포함) | 본문 전체 추가(슬라이드 11–14). `serving_size` 함정(최대격차 0.153 > 0.101)은 **본문 `pitfall`로 살린다**(§4.3 항목 3). 값은 T08이 재확인해 출력 |
| `sec:binomial` | TODO 주석 1줄 | 본문 전체 추가(슬라이드 23–29) |
| `sec:cdf` | TODO 주석 1줄 | 본문 전체 추가. CDF는 **다시 정의하지 않는다**: $F(x)=P(X\le x)$ 한 줄 요약(원칙 9a) + `\Cref{def:ecdf}`. 그림 `fig:dist-cdf`, $D$ 한 문장 + `\Cref{def:ks-statistic}`. PLAN T09의 "points to 02"는 틀렸다(§7 Q-A) |
| `요약` | `% TODO` | TODO를 `tab:dist-summary`로 대체: 분포, 연속/이산, 모수, 평균, 분산, 절 `\Cref`. 한 표만 |

### 2.3 장 In brief 초안 (T09이 다듬는다)

- **Why:** 데이터의 모양을 이름 있는 분포(Distribution) 하나로 요약하면, 모수 몇 개로 확률을 계산할 수 있다.
- **When:** 히스토그램의 모양(대칭, 한쪽 꼬리, 평평함, 두 값)이 보이고, 그 모양을 계산에 쓰고 싶을 때.
- **Where:** 정규, 균등, 지수, 멱법칙(연속), 베르누이, 이항(이산). 검정(`\Cref{ch:hypothesis}`)과 정규화(`\Cref{ch:qq-normalization}`)가 이 가정 위에 선다.
- **How:** 모양으로 후보를 고르고, 모수를 추정하고, CDF를 겹쳐 얼마나 어긋나는지 본다.

### 2.4 `sec:dist-background` 재료

선행 개념(한 줄 요약 + `\Cref`): 평균과 표준편차(`\Cref{sec:center}`, `\Cref{def:spread}`),
히스토그램과 구간(`\Cref{sec:histogram}`), 왜도(`\Cref{sec:skewness}`). 출처: 덱 6
(`notes/6_DataDistribution.pptx`). 확률밀도(Probability Density) 대 확률질량(Probability Mass)
구분을 여기서 한 번 깐다(연속/이산 목록이 슬라이드 3에 있으므로).

### 2.5 `sec:dist-apply`, `sec:dist-future` 재료

- 어떻게 적용: HW1 패스트푸드 변수별 판정(calories 정규 기각 `fig:normal-fit`, sugars 지수
  `fig:dist-exponential`, sodium 베르누이/이항 `fig:dist-bernoulli-binomial`), HW2의 공항/영화
  후보 판정(`\Cref{sec:hw2-estimators}`, `\Cref{fig:hw2-airport-powerlaw}`), Q-Q로 확인
  (`\Cref{sec:qq}`, `\Cref{fig:qq-calories}`).
- 앞으로: 모수 추정과 Q-Q(`\Cref{ch:qq-normalization}`), 이항 위의 정확 검정
  (`\Cref{sec:ht-exact}`, `\Cref{sec:pv-discrete}`), 정규 위의 신뢰구간과 1.96(`\Cref{sec:ci}`),
  두 분포 비교와 KS(`\Cref{sec:cd-ks}`).

## 3. 재계산 표

직접 계산(손 계산, 모델 학습 없음). "확인"은 §4.3 값과 같다는 뜻이다. T08이 스크립트로 한 번 더 출력한다.

| 행 | 슬라이드 | 식 | 슬라이드 값 | 재계산 값 | 판정 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| R1 | 16 | $1-e^{-0.2\cdot3}=1-e^{-0.6}$, $e^{-0.6}=0.548812$ | 0.4512 | 0.4512 | 확인 |
| R2 | 17 | $1/\lambda = 1/10$ 시간 | 6분 | 6분 | 확인 |
| R3 | 17 | $1-e^{-10\cdot5/60}=1-e^{-0.8333}$, $e^{-0.8333}=0.434598$ | 0.0801 | **0.5654** | **오류** (§6 E1) |
| R3b | 17 | $1-e^{-5/60}=1-e^{-0.08333}$ ($\lambda$ 빠뜨림) | | 0.0800 (0.07996) | 슬라이드 0.0801과 넷째 자리 차이. "$\lambda$를 빠뜨린 값과 거의 같다"로 쓴다 |
| R4 | 15 | 모수 범위 | $0<\lambda\le1$ | $\lambda>0$ | **오류** (§6 E2) |
| R5 | 18 | 기하 근사 $0.05$, $0.95\cdot0.05$, $0.95^2\cdot0.05$ | 0.05, 0.0475, (0.045125) | 0.05, 0.0475, 0.045125 | 확인 (산술 맞음). 슬라이드는 셋째 값을 식으로만 둔다 |
| R6 | 18 | 정확 지수 $1-e^{-0.05}$, $e^{-0.05}-e^{-0.10}$, $e^{-0.10}-e^{-0.15}$ | 없음 | 0.04877, 0.04639, 0.04413 | 표 `tab:dist-geometric`의 둘째 열. 근사와 차이 0.0012, 0.0011, 0.0010 |
| R7 | 7 | $P(\lvert Z\rvert<2)$ | 95% | 95.45% | 근사 (§6 E3). 95%는 ±1.96 |
| R7b | 7 | $P(\lvert Z\rvert<1)$ | (그림 06_02 범례 68%) | 68.27% | 그림 범례 수정 대상(§4) |
| R8 | 13 | 웃는 시간 55개 합과 평균 | 없음 | 합 640.9, 평균 11.65, 최솟값 0.7, 최댓값 22.8, 히스토그램 개수 4,5,7,6,7,7,3,6,6,4(합 55; **그림 image16에서 읽은 값, 검증 안 됨**. Q-C가 예이면 T08이 검증) | 합, 평균, 최솟값, 최댓값은 손으로 합산해 확인. 표준편차는 T08이 출력(§7 Q-C) |
| R9 | 12 | $P(1<X<2)=1\cdot\frac15$; $P(4<X<4\frac13)=\frac13\cdot\frac15$; $P(X=4)$ | 1/5, 1/15, 0 | 1/5, 1/15, 0 | 확인 |
| R10 | 14 | $[0,5]$: $(a+b)/2$, $(b-a)/\sqrt{12}$ | 식만 | 평균 2.5, 표준편차 $5/\sqrt{12}=1.4434$ | 슬라이드 14 그림(image18/19)에서 식 확인. 슬라이드는 분산 $(\beta-\alpha)^2/12$로 준다 |
| R11 | 24 | $0.4\cdot0+0.6\cdot1$ | 0.6 | 0.6 | 확인. 분포가 가질 수 없는 값 |
| R12 | 24 | $0.4(0-0.6)^2+0.6(1-0.6)^2=0.144+0.096$ | 0.24 | 0.24 $=p(1-p)$ | 확인 |
| R13 | 27 | $0.5^5$ | 식만 | $1/32=0.03125$ | 확인 |
| R14 | 28 | $\binom52/32=10/32$ | 식만 | 0.3125 | 확인 |
| R15 | 29 | $np$, $np(1-p)$ | 식 | image52/53과 같음 | 확인 |
| R16 | 15 | $E[X]=\int_0^\infty x\lambda e^{-\lambda x}dx=1/\lambda$ | 유도 | 부분적분 유도 맞음(image21) | 확인. 본문은 한 줄에 한 조작으로 옮긴다(원칙 9b) |
| R17 | 18 | 평균 20분 → $\lambda=1/20$ | 0.05 | 0.05/분, $f(0)=0.05$ (image26) | 확인 |
| R18 | 기존 TODO | calories의 ±2σ 안 비율, Shapiro p, `serving_size` 최대격차 | 96.0%, 0.00038, 0.153 대 0.101 | T08 출력으로 재확인 | 스크립트 값이 권위. 다르면 T09는 스크립트 값을 쓴다 |

T09 AC 숫자 목록(0.4512, 6분, 0.5654, 0.0801, 0.0800, 0.05, 0.0475, 0.045125, 0.04877, 0.04639,
0.04413, 1/15, 95.45%, 1.96, 0.24, 0.3125)은 위 표와 모두 맞는다. pm이 추가를 검토할 값: 68.27%(그림
범례와 본문 일치), 2.5와 1.4434(R10), 11.65(R8, Q-C 결정 후).

## 4. 그림 목록

**새 그림: 없음.** 필요한 모양은 모두 기존 `06_0N_*.png`에 있다. 단 기존 그림 하나의 **범례 문구
수정**이 필요하다(T08).

| 파일 | 생성 함수 (`deck6_distributions.py`) | 04 라벨 | 04에서 쓰는 곳 | 상태 |
| :-- | :-- | :-- | :-- | :-- |
| `06_01_normal_fit.png` | `_normal_fit` | 없음. `\Cref{fig:normal-fit}`(lec07이 라벨 소유) | `sec:normal`, `sec:dist-apply` | 재사용, `\includegraphics` 금지 |
| `06_02_normal_sigma_bands.png` | `_normal_sigma_bands` | `fig:dist-sigma-bands` | `sec:normal` 슬라이드 7 | **T08 수정:** 47행 범례 `"+/- 2 sigma = 95%"`, `"+/- 1 sigma = 68%"` → `95.45%`, `68.27%`. 본문 함정(95.45%)과 그림이 어긋나면 AC-W6 위반. 제목의 "68-95 rule"은 규칙 이름이므로 그대로 둘 수 있다 |
| `06_03_cdf.png` | `_cdf` | `fig:dist-cdf` | `sec:cdf` | 재사용 |
| `06_04_exponential_fit.png` | `_exponential_fit` | `fig:dist-exponential` | `sec:exponential`, `sec:dist-apply` | 재사용 |
| `06_05_uniform_reference.png` | `_uniform_reference` | `fig:dist-uniform` | `sec:uniform` 슬라이드 11–12 | 재사용 |
| `06_06_powerlaw_vs_exponential.png` | `_powerlaw_vs_exponential` | `fig:dist-powerlaw` | `sec:powerlaw` 슬라이드 20–22 | 재사용 |
| `06_07_bernoulli_binomial.png` | `_bernoulli_binomial` | `fig:dist-bernoulli-binomial` | `sec:binomial` | 재사용 |

검토했으나 넣지 않은 그림: (1) 폭이 다른 두 정규 곡선(슬라이드 6, 8). 넓이 1 원리는 수식 한 줄과
`fig:dist-sigma-bands`로 충분하다. (2) 기하 근사 대 정확 지수 막대그림(슬라이드 18). §4.3이 두 열 표로
정했다. (3) 웃는 시간 히스토그램(슬라이드 13). 슬라이드 그림을 인용한다. 소유자가 (3)을 원하면
`06_08_smiling_times.png` 하나가 생긴다(§7 Q-C).

표(그림 아님, T09가 만든다): `tab:dist-map`(배경), `tab:dist-geometric`(기하 근사 대 정확),
`tab:dist-summary`(요약).

**T08 할 일 요약:** (a) 06_02 범례 두 문자열 수정 후 재생성, (b) R18 세 값 출력(±2σ 안 비율,
Shapiro p, `serving_size`의 균등/정규 최대격차), (c) R1, R3, R3b, R6, R7, R7b 출력(scipy, 계산만),
(d) Q-C가 "예"이면 55개 값 전사 + 검증 함수(합 640.9, $n=55$, 구간 개수) + 표준편차 출력.
모델 학습 없음. `fit()`은 기존 `stats.norm.fit`(최대우도 닫힌 식)만 쓴다.

## 5. `\Cref` 대상 (검증됨)

2026-09-24 `grep '\label{'`로 존재 확인.

### 5.1 04가 걸 링크 (나가는 방향)

| 대상 | 파일 | 04의 쓰임 |
| :-- | :-- | :-- |
| `sec:center`, `def:spread` | 02 | 배경: 평균, 표준편차 |
| `sec:histogram` | 03 | 배경: 히스토그램 |
| `sec:skewness`, `sec:skew-sign` | 02 | 슬라이드 9. 링크만, 2.3.2 본문 불변 |
| `sec:ci`, `subsec:ci-compare` | 03 | 1.96과 95% |
| `fig:normal-fit` | lec07 | calories 정규 적합 |
| `sec:normalization` | lec07 | 슬라이드 8 이동/척도 |
| `sec:qq`, `fig:qq-calories`, `ch:qq-normalization` | lec07 | 적용, 앞으로 |
| `sec:dist-check-cdf` | lec07 | `sec:cdf`에서 "눈으로 보는 CDF 비교" |
| `sec:qq-background` (98–104행의 기호 충돌 함정) | lec07 | 슬라이드 14의 $\alpha,\beta$ → $[a,b]$. `\Cref{sec:qq-background}` |
| `ch:hypothesis`, `sec:ht-exact` | lec09 | 기하분포 "독립이면 곱한다", 이항 정확 계산 |
| `sec:pv-discrete` | lec10 | 이항 p값 |
| `def:ecdf`, `def:ks-statistic`, `sec:cd-ks` | lec11 | `sec:cdf`는 정의를 반복하지 않고 가리킨다 |
| `sec:hw2-estimators`, `fig:hw2-airport-powerlaw` | hw02 | 멱법칙 모수 추정, 실제 멱법칙 데이터 |

위 라벨은 모두 `\label{`로 존재를 확인했다(`sec:histogram`은 03:115). T09 전에 writer가 한 번 더 grep한다.

### 5.2 04로 들어오는 링크 (지켜야 할 라벨)

| 라벨 | 가리키는 곳 | T09 후 영향 |
| :-- | :-- | :-- |
| `sec:normal` | lec07:51, 220; lec10:56; lec11:701; hw02:51 | lec07:220, lec11:701은 "`sec:normal`의 함정"을 가리킨다. 기존 KS 함정을 그대로 둬야 이 문장이 참이다 |
| `def:normal` | lec07:51, lec10:56 | 유지 |
| `sec:exponential` | lec07:100, hw02:59 | 유지 |
| `sec:binomial` | lec09:58, 360 | lec09:58 "현재는 뼈대만 있는 절"이 거짓이 된다(§7 Q-B) |
| `sec:cdf` | lec07:46; lec11:49, 598; hw02:140, 191 | lec07:46–47 "아직 초안(stub)이므로"가 거짓이 된다(§7 Q-B) |
| `ch:distributions` | lec09:58; hw02:91 | hw02:91 "멱법칙은 `ch:distributions`에 아직 절이 없다"가 거짓이 된다(§7 Q-B) |
| `sec:uniform` | 들어오는 링크 없음 | 유지 |

## 6. 슬라이드 오류

Q4 형식 대상(E1–E3)은 `pitfall` 안에 "슬라이드 값은 X, 다시 계산하면 Y"로 쓴다.

| # | 슬라이드 | 슬라이드 값 X | 다시 계산한 값 Y | 처리 |
| :-- | :-- | :-- | :-- | :-- |
| E1 | 17 | $P(X<5/60)\approx0.0801$ | 0.5654. 0.0801은 $\lambda$를 빠뜨린 $1-e^{-5/60}=0.0800$과 거의 같다. 상식 검산: 평균 6분인데 5분 안에 올 확률이 8%일 수 없다 | `pitfall` (T09 AC에 있음) |
| E2 | 15 | $0<\lambda\le1$ | $\lambda>0$. 슬라이드 17 자신이 $\lambda=10$을 쓴다 | `pitfall` (T09 AC에 있음) |
| E3 | 7 | ±2 SD에 95% | 95.45%. 95%는 ±1.96 SD이고 슬라이드 그림(image5)도 그렇게 표시한다 | `pitfall` (T09 AC에 있음). 06_02 범례도 함께 고친다(§4) |
| E4 | 18 | 1분 단위 확률 0.05, 0.0475, 0.045125 | 정확값 0.04877, 0.04639, 0.04413 | **오류 아님, 근사.** 표 `tab:dist-geometric` + 한 문단. `pitfall` 형식 쓰지 않음 |
| E5 | 6 | "성인 키의 가능성이 더 많다" | 원리: 곡선 아래 넓이가 1이므로 폭(표준편차)이 좁으면 높이가 커진다 | 설명 보강. 수치 오류가 아니므로 `pitfall` 아님 |
| E6 | 12 | "5*X = 1 -> X = 1/5" | 구하는 것은 $X$가 아니라 밀도의 높이 $f(x)=h$: $5h=1$, $h=1/5$ | **신규 발견.** 기호 오류이며 숫자는 맞다. Q4 형식("X, 다시 계산하면 Y")은 두 수가 달라야 하므로 맞지 않는다. `pitfall` 대신 본문 한 문장: "슬라이드는 높이를 $X$로 적었지만 구하는 것은 밀도의 높이 $h$다". AC-W7 목록에 넣지 않는다(§7 Q-E) |

## 7. 소유자/pm 질문

- **Q-A (차단, pm):** PLAN T09 "`sec:cdf` does not redefine CDF (points to 02, see A02)"는 현재
  저장소와 맞지 않는다. 01/02/03에는 CDF 정의가 없고(`grep 누적분포|CDF` 결과 0), A02는 §3.5로 T09보다
  뒤다. **제안:** `sec:cdf`는 $F(x)=P(X\le x)$ 한 줄 요약 + `\Cref{def:ecdf}`(lec11) +
  `\Cref{sec:dist-check-cdf}`(lec07) + `\Cref{sec:cd-ks}`로 가리킨다. pm이 T09 문구를 이렇게 고쳐야
  T09가 시작할 수 있다.
- **Q-B (비차단, 소유자):** T09 후 거짓이 되는 기존 문장 셋: lec07:46–47("`sec:cdf`가 아직
  초안(stub)이므로"), lec09:58("현재는 뼈대만 있는 절이며"), hw02:91("멱법칙은
  `ch:distributions`에 아직 절이 없다"). (a) Q8과 같은 방식의 한 줄 수정 과제를 T10 뒤에 둔다,
  (b) 백로그에 둔다. 권고 (a). 세 파일은 리뷰를 마친 장이라 소유자 승인이 필요하다. PLAN §1의 "No
  shrink-back pass"는 본문 축소를 말한 것이고, 이 셋은 사실이 틀리게 되는 문장이다.
- **Q-C (소유자):** 슬라이드 13의 웃는 시간 55개를 스크립트에 전사해 표준편차(와 선택적으로
  `06_08_smiling_times.png`)를 만들 것인가. 기본안: 전사하지 않고 슬라이드를 출처로 인용,
  본문 숫자는 손 계산한 합 640.9와 평균 11.65, 범위 0.7–22.8만 쓴다. 이 경우 새 그림은 없다.
- **Q-D (pm, 경미):** 라벨 없는 기존 `요약` 절을 `tab:dist-summary`로 채우고, `sec:dist-apply`와
  `sec:dist-future`를 그 뒤(파일 끝)에 둔다. 요약을 그대로 비워 두기를 원하면 알려 달라.
- **Q-E (pm):** 신규 오류 E6(슬라이드 12의 "X = 1/5")은 기호 오류라 Q4 형식에 맞지 않는다. 권고:
  AC-W7 목록에 넣지 않고, T09 지시에 "본문 한 문장으로 바로잡는다"를 더한다.
- **Q-F (pm):** T08 AC가 "if none: print TODO values"로 되어 있다. 이 문서는 새 그림은 없지만 06_02
  수정이 있으므로 T08은 §4의 (a)–(c)를 한다. T08 AC에 "06_02 범례에 95.45%와 68.27%가 보인다"를 더할 것.
- **Q-G (확인만):** architecture.md §4.2 항목 4(그림 거처 = 04)는 PLAN §1의 결정(06_01은 lec07이
  라벨 소유)으로 대체된 것으로 본다. 이 문서는 그 결정을 따른다.

## 결정 기록 (2026-09-24, 메인 세션)

- **Q-A:** T09 지시의 "`sec:cdf`는 02를 가리킨다"를 "`sec:cdf`는 lec11의 `def:ecdf`를 가리킨다"로 읽는다.
- **Q-B:** T09 뒤에 lec07, lec09, hw02의 "04는 초안" 취지 문장 세 줄은 틀린 말이 되므로 한 줄씩 고친다(정확성 우선). 메인 세션 과제로 처리한다.
- **Q-C:** 새 그림이 없으므로 슬라이드 13의 55개 값은 옮겨 적지 않는다.
- **Q-D~G:** 설계 문서의 기본안을 따른다.
