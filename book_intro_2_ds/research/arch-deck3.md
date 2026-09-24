# §4.1 addendum: 덱 3 → `01-data-attributes.tex` 채우기 (A03)

작성: system-architect, 2026-09-24, cycle 1/2. 설계 문서다. `architecture.md` §4.1 의 보충이며
그 파일은 건드리지 않는다(다른 architect가 병렬로 쓰고 있음). LaTeX 본문은 T12(sonnet-writer),
그림 생성기는 T11(developer) 몫이다.

출처: `notes_text/3_DataAndMatrix/slides.md` 와 `media/image1~21`(모두 열어 확인함).

## 0. 전제와 대체 사항

1. **Q2 적용:** 기존 절 본문(1~220행)은 한 줄도 바꾸지 않는다. 추가만 한다(AC-W12 삭제 0).
   기존 절 안에는 주석 `% source: deck 3 slide K` 줄만 더한다(AC-W9).
2. **§4.1 항목 5의 "3차원 산점도 TikZ"는 대체된다.** 슬라이드 11의 산점도는 실제 데이터
   5행(급여, 나이, 근속연수)의 값을 축 눈금 위에 찍은 **데이터 그림**이다. PLAN §1 Figures
   결정("데이터 그림은 Python 생성기, TikZ는 흐름도만")과 AC-W10에 따라 PNG로 만든다.
   같은 이유로 슬라이드 10, 13, 15의 그림도 PNG다(5절). TikZ는 도식 두 개(이미지 → 행렬,
   네트워크 → 인접 행렬)만.
3. **§4.1 항목 4의 "플래그"는 오류가 아니라 모호성이다.** 이미지를 열어 확인한 결과 두
   슬라이드는 같은 규칙("식별자는 속성이 아니다")을 따른다. 다른 것은 "열"이라는 말이 가리키는
   대상이다(7절 M1). T12 AC의 pitfall은 그대로 두되, 문구는 "슬라이드 값은 X, 다시 계산하면
   Y" 형이 아니라 "두 슬라이드가 세는 대상이 다르다" 형으로 쓴다(Q4 형식은 오류용).
4. **산술 검증 방법:** 이 에이전트에는 셸 도구가 없어 `uv run python -c` 를 돌리지 못했다.
   4절의 값은 손으로 계산했고, 각 값을 T11 생성기가 출력(print)해 확인하도록 5.3절에 넣었다.
   T11 검토(reviewer)에서 출력과 4절이 다르면 출력이 이긴다. **T12는 R4, R12, R14, R17, R18,
   4.2절 값을 T11 출력으로 확인된 뒤에만 인용한다.**
5. 금지 사항 재확인: 모형 학습, `fit`, 노트북 실행 없음. 붓꽃은 `load_iris()` 로 값만 읽는다
   (lec07과 같은 방식).

## 1. 장 배치 (기존 절 기준 삽입 위치)

행 번호는 현재 `chapters/01-data-attributes.tex`(220행) 기준. `[기존]` = 손대지 않음.

| 순서 | 내용 | 라벨 | 위치 |
| :-- | :-- | :-- | :-- |
| 0 | `\chapter`, `\label{ch:attributes}` | [기존] | 1~2행 |
| 1 | **장 머리 In brief** (`\paragraph{In brief.}` + description, Why/When/Where/How) | 없음 | 2행 뒤, 4행 도입 문단 앞 |
| 2 | 도입 문단 + `keyidea` (장의 "왜" 역할) | [기존] | 4~13행 |
| 3 | **배경** | `sec:attr-background` | 13행 뒤, `sec:attr-flow` 앞 |
| 4 | 두 번의 질문 | `sec:attr-flow` [기존] | |
| 5 | 수치형 | `sec:attr-numeric` [기존] | |
| 6 | 범주형 | `sec:attr-categorical` [기존] | |
| 7 | 유형이 통계를 결정한다 (+ `ex:hw1-types`, aside) | `sec:attr-stats` [기존] | 147~220행 |
| 8 | **이산형과 연속형** (+ 슬라이드 4 판정 연습) | `sec:attr-discrete` | 220행 뒤(파일 끝에 이어 붙임) |
| 9 | **데이터 행렬** | `sec:data-matrix` | 8 뒤 |
| 10 | **차원** | `sec:dimension` | 9 뒤 |
| 11 | **벡터** | `sec:vector` | 10 뒤 |
| 12 | **무엇이든 행렬로** (개관, In brief 생략) | `sec:everything-matrix` | 11 뒤 |
| 13 | **어떻게 적용하는가** | `sec:attr-apply` | 12 뒤 |
| 14 | **앞으로** | `sec:attr-future` | 파일 끝 |

`sec:attr-discrete` 를 척도 절들 사이가 아니라 `sec:attr-stats` 뒤에 두는 이유: 기존 네 절은
"척도 → 허용 연산"의 한 흐름이다. 이산/연속은 **다른 축**이므로 그 흐름을 끊지 않고 뒤에서
"두 번째 축"으로 연다. 행렬 절들 앞에 두는 이유: 행렬의 열 = 속성이고, 속성의 두 축(척도,
이산/연속)을 다 본 뒤 열로 쌓는 순서가 자연스럽다.

장 제목과 그 안의 기존 줄표는 그대로 둔다(Q6). 제목이 새 절(행렬, 차원)을 포괄하지 못하는
문제는 8절 D3-Q2.

## 2. 절별 설계 (T12 라벨 목록)

### 2.1 장 머리 In brief (슬라이드 1)

- Why: 값에 허용된 연산(척도)과 데이터가 놓이는 모양(행렬, 공간)을 알아야 이후 모든 요약과
  그림이 합법이 된다.
- When: 데이터를 받자마자, 어떤 통계도 계산하기 전에.
- Where: 표로 된 모든 데이터. 이미지, 텍스트, 네트워크도 행렬로 바꾼 뒤 같은 틀에 들어온다.
- How: 열마다 척도와 이산/연속을 가르고, 식별자를 뺀 나머지를 $n \times d$ 행렬로 본다.

### 2.2 `sec:attr-background` (개관 절, In brief 생략)

- 출처: 덱 3 "Data and Matrix"(슬라이드 1~20). 책의 첫 본문 장이므로 선행 개념은 없다.
  대신 이 장이 쓰는 기초 용어 세 개를 한 줄씩 깐다(원칙 9a): 표(Table), 행(Row)/열(Column),
  좌표평면(Coordinate Plane, "점 하나 = 값 두 개").
- 이 장 뒤에 오는 곳: 요약값(`\Cref{ch:descriptive}`), 그림(`\Cref{ch:visualization}`).
- 두 부분으로 된 장임을 밝힌다: 앞(기존 네 절) = 열 하나의 성질, 뒤(새 절) = 열을 모은 행렬.

### 2.3 `sec:attr-discrete` 이산형(Discrete)과 연속형(Continuous) (슬라이드 2, 4)

- In brief 필요(개념 절).
- 고치는 문제: 척도만으로는 "값이 셀 수 있게 끊겨 있는가"를 알 수 없다. 이것이 막대그래프 대
  히스토그램, PMF 대 PDF(덱 4) 선택을 가른다.
- 정의(슬라이드 2): 이산 = 값이 떨어져 있음(태어난 연도, 참/거짓), 연속 = 실수값(길이).
- **2×2 표** `tab:attr-discrete-2x2` (T12 AC 고정). 행 = 수치형(Numeric)/범주형(Categorical),
  열 = 이산형/연속형. 각 칸에 척도명과 예:

  | | 이산형 (Discrete) | 연속형 (Continuous) |
  | :-- | :-- | :-- |
  | 수치형 | 태어난 연도(구간), 고객 수(비율) | 길이, 무게(비율), 섭씨온도, 경도(구간) |
  | 범주형 | 참/거짓, 전공(명목), 만족도 1~5(순서) | 없음: 범주형은 늘 이산 |

  빈 칸의 이유를 본문에 한 문장으로("기호의 집합에서 값을 고르므로 사이값이 없다").
- **슬라이드 4 판정 연습** `ex:attr-slide4` (example 환경, 이 절 끝). 다섯 항목에 척도와
  이산/연속 두 축을 함께 답한다. 척도 답은 T12 AC 고정: 명목, 구간, 순서, 비율, 명목.

  | 항목 | 척도 (슬라이드 답, 재확인 맞음) | 이산/연속 (책이 추가) | 근거 한 줄 |
  | :-- | :-- | :-- | :-- |
  | 색(Color) | 명목 | 이산 | 색 이름에 서열 없음 |
  | 경도(Longitude) | 구간 | 연속 | 0°는 그리니치를 고른 약속 |
  | 강사 만족도 1~5 | 순서 | 이산 | 간격이 같다는 보장 없음(`\Cref{def:nominal-ordinal}` 뒤 문단) |
  | 무게(Weight) | 비율 | 연속 | 0 kg = 무게 없음 |
  | 전공(College major) | 명목 | 이산 | 서열 없음 |

  경도 한 줄 주의(선택): 경도는 180°와 −180°가 같은 곳인 원형 값이라 "차이"도 조심해야 한다.
  슬라이드 답을 뒤집지 않는 보충이다. `media/image1.png`(1~5 라디오 버튼)는 만족도 문항의
  모양이므로 다시 그리지 않고 말로만 적는다.

### 2.4 `sec:data-matrix` 표 데이터(Tabular Data)와 데이터 행렬(Data Matrix) (슬라이드 5~8)

- In brief 필요.
- 고치는 문제: 열 하나씩 보는 것으로는 "객체 하나가 여러 속성을 동시에 가진다"를 다룰 수 없다.
  행과 열을 한 번에 다루는 틀이 행렬이다.
- 수식(슬라이드 6~7, `media/image2.png`, `image3.png` 에서 복원):
  $\mathbf{D} \in \mathbb{R}^{n \times d}$, 행 $\mathbf{x}_i = (x_{i1}, \dots, x_{id})^T \in \mathbb{R}^d$,
  열 $X_j = (x_{1j}, \dots, x_{nj})^T \in \mathbb{R}^n$. 기호 표 하나(원칙 9c):
  $n$ = 행(객체) 수, $d$ = 열(속성) 수, 굵은 소문자 = 행, 대문자 = 열. **$\mathbf{x}_i$ 와 $X_j$
  가 다른 것임을 명시 경고.** 동의어 목록(행: 표본(Sample), 인스턴스(Instance), 레코드(Record),
  객체(Object), 점(Point), 특징 벡터(Feature Vector); 열: 속성(Attribute), 특징(Feature),
  차원(Dimension), 변수(Variable), 필드(Field))은 표 `tab:attr-synonyms` 로.
- 예제 `ex:attr-name-salary-age` (슬라이드 5, 8, `media/image5.png`): 이름/급여/나이 표. 표로
  옮기고 `tab:attr-name-salary-age`. 세는 순서를 한 줄씩(원칙 10): 머리글 행 1줄 제외 → 행 5,
  열 3 → 식별자 열(Name) 제외 → 속성 2 → $\mathbf{D} \in \mathbb{R}^{5 \times 2}$.
- **pitfall `식별자 열은 속성이 아니다`** (T12 AC): 7절 M1 내용. 기존 `ex:hw1-types` 의
  `item`("고유 식별자에 가깝다")을 한 줄로 가리킨다.

### 2.5 `sec:dimension` 차원(Dimension)의 두 뜻 (슬라이드 9~12)

- In brief 필요.
- 고치는 문제: 같은 낱말 "차원"이 프로그래밍과 데이터 과학에서 다른 것을 센다. 섞으면
  "100차원 데이터는 100차원 배열이 필요하다"는 오해가 생긴다.
- 두 뜻을 두 열 표 `tab:attr-dimension-two-meanings` 로: 배열 차원(Array Dimension) = 인덱스
  (축) 수, 공간 차원(Space Dimension) = 속성 수 $d$. **슬라이드 9의 "셀의 수를 센다"는 틀렸다**
  (7절 E1, pitfall).
- 2차원 예(슬라이드 10): 이름/급여/나이 → 점 5개, 그림 `fig:attr-2d-scatter`.
  Jane(52, 90000)과 Dave(53, 90000)가 거의 겹친다는 관찰을 한 줄.
- 3차원 예(슬라이드 11, `media/image9.png`): 급여/나이/근속연수 5×3 표 `tab:attr-3d-data`,
  그림 `fig:attr-3d-scatter`. 한 줄씩: 배열로는 2차원(5×3, 셀 15개), 공간으로는 3차원.
- 슬라이드 12: 특징이 100개여도 $n \times 100$ 의 2차원 배열에 담긴다. `media/image6.png`
  (Feature 1 ... Feature n 표)는 다시 그리지 않고, 머리글 표기 오류만 pitfall(7절 E2).
  "고차원 데이터" 목록의 "행이 많음"은 7절 E3 (pitfall).

### 2.6 `sec:vector` 점 = 행 = 벡터(Vector) (슬라이드 13~15)

- In brief 필요.
- 고치는 문제: 행을 "숫자 목록"으로만 보면 두 객체의 거리, 평균 점 같은 기하 연산을 떠올릴 수
  없다. 행을 원점에서 뻗은 화살표로 보면 물리의 벡터 연산이 그대로 쓰인다.
- 슬라이드 13 표(`media/image11.png`, 5×2: (20, 90000), (30, 85000), (28, 40000), (40, 95000),
  (35, 42000)) → 그림 `fig:attr-vectors`(화살표가 원점에서 점까지).
- 붓꽃(Iris) 예(슬라이드 14, `media/image13.png`): 표 `tab:attr-iris-rows` 에 슬라이드의 10행
  ($\mathbf{x}_1 \sim \mathbf{x}_8$, $\mathbf{x}_{149}$, $\mathbf{x}_{150}$)을 옮긴다. 150×5 표,
  수치 열 4개 → $\mathbf{D} \in \mathbb{R}^{150 \times 4}$, Class 열 $X_5$ 는 명목 범주형
  (`\Cref{sec:attr-categorical}`)이라 수치 행렬에서 뺀다. 출처 문장은 `\Cref{sec:qq-iris-source}`
  를 가리키고 다시 쓰지 않는다(원칙 12 "한 번만").
- 슬라이드 15(`media/image14.png`): 꽃받침 길이 × 꽃받침 너비 150점 + 평균 점 → 그림
  `fig:attr-iris-mean`. 평균 점 = 열마다 평균 낸 벡터 $(\bar X_1, \bar X_2)$ 한 줄 정의.

### 2.7 `sec:everything-matrix` 무엇이든 행렬로 (슬라이드 16~19, 개관, In brief 생략)

- 이미지(슬라이드 16): 이미지 하나 → 영역 $r_1, r_2, \dots$ 마다 RGB 색, 질감(Texture) 특징
  → 영역 = 행, 특징 = 열. TikZ 도식 `fig:attr-image-matrix`. **슬라이드의 고양이 사진 두 장
  (`image15.jpeg`, `image16.jpeg`)은 출처 불명이므로 싣지 않는다.**
- 텍스트(슬라이드 17~18): 단어마다 "전역 단어-단어 동시출현(co-occurrence) 통계"로 만든 벡터.
  "King" 벡터는 값 50개(4절 R14). 앞 5개 값만 인라인으로 보이고 "…(모두 50개)"로 줄인다.
  슬라이드 18의 king − man + woman ≈ queen 은 말로만(계산 재현 불가, 벡터 원본이 슬라이드에
  king 하나뿐). 모형 이름은 슬라이드에 없으므로 붙이지 않는다(원칙 12, 문헌 날조 금지).
  히트맵 그림(`image18~20`)은 싣지 않는다.
- 네트워크(슬라이드 19, `media/image21.jpeg`): 노드 5개 그래프 → 5×5 인접 행렬(Adjacency Matrix).
  TikZ 그림 `fig:attr-network`(그래프 + 행렬을 한 그림에). 값은 4절 R15~R17.

### 2.8 `sec:attr-apply` 어떻게 적용하는가

- HW1 데이터(`\Cref{ch:hw1}`, `\Cref{ex:hw1-types}`)를 행렬로 세 번 센다(원칙 10, 한 줄씩):
  저장 배열 126×8 → 식별자 `item` 제외 속성 7 → 수치 데이터 행렬 $\mathbf{D} \in
  \mathbb{R}^{126 \times 5}$(비율 척도 다섯 열). `item` 을 식별자로 보는 판단은 T11이 출력할
  고유값 수(4절 R18)가 126이면 확정, 아니면 "식별자에 가깝지만 중복이 있다"로 한 줄 조정.
- 거리 한 예(선택, 4.2절): 급여 단위가 나이 단위를 압도한다 → 정규화(`\Cref{sec:normalization}`)
  로 이어진다.

### 2.9 `sec:attr-future` 앞으로

- 고차원(High Dimension): $d$ 가 커질 때 생기는 문제(차원의 저주, Curse of Dimensionality)와
  차원 축소(Dimensionality Reduction). 출처는 덱 1 슬라이드 4의 주제 목록(architecture.md §1 Q3,
  인용만).
- 이산화(`\Cref{sec:discretization}`): 연속 속성을 이산 속성으로 바꾸는 다리(2×2 표의 열 이동).
- 가설검정(`\Cref{ch:hypothesis}`)은 이 장의 척도 판정을 전제로 한다는 한 줄(선택).

## 3. 슬라이드 → 절 대응 (1~20)

| 슬라이드 | 내용 | 절/라벨 | 비고 |
| :-- | :-- | :-- | :-- |
| 1 | 제목 "Data and Matrix" | 장 머리 In brief | 내용 없음(제목만) |
| 2 | 이산/연속 | `sec:attr-discrete`, `tab:attr-discrete-2x2` | |
| 3 | 구간/비율/명목/순서 | `sec:attr-numeric`, `sec:attr-categorical` [기존] | 주석 줄만 추가 |
| 4 | 판정 연습 5문항 + `image1` | `sec:attr-discrete` 끝 `ex:attr-slide4` | 답 모두 맞음 |
| 5 | Tabular Data | `sec:data-matrix` | |
| 6 | $n \times d$ 데이터 행렬, 행/열 동의어 (`image2`, `image4`) | `sec:data-matrix`, `tab:attr-synonyms` | `image4` 는 기호 ∈ 한 글자 |
| 7 | 대수적 보기 (`image3`) | `sec:data-matrix` 수식 | |
| 8 | 식별자 열, 5 객체 2 특징 (`image5`) | `sec:data-matrix`, `ex:attr-name-salary-age`, pitfall | M1 |
| 9 | 차원의 두 뜻 (`image6`) | `sec:dimension`, `tab:attr-dimension-two-meanings` | E1, E2 |
| 10 | 2차원 데이터 (`image7`, `image8`) | `sec:dimension`, `fig:attr-2d-scatter` | |
| 11 | 3차원 데이터 (`image9`, `image10`) | `sec:dimension`, `tab:attr-3d-data`, `fig:attr-3d-scatter` | M1, C1 |
| 12 | 100차원도 2D 배열, 고차원 (`image6`) | `sec:dimension` | E2, E3 |
| 13 | 벡터 (`image11`, `image12`) | `sec:vector`, `fig:attr-vectors` | C2 |
| 14 | 붓꽃 표 (`image13`) | `sec:vector`, `tab:attr-iris-rows` | |
| 15 | 붓꽃 2D 점 + 평균 점 (`image14`) | `sec:vector`, `fig:attr-iris-mean` | |
| 16 | 이미지 → 행렬 (`image15`, `image16`) | `sec:everything-matrix`, `fig:attr-image-matrix` | 사진 미수록 |
| 17 | 텍스트 → 벡터 (`image17~19`) | `sec:everything-matrix` | R14 |
| 18 | king − man + woman ≈ queen (`image20`) | `sec:everything-matrix` | 말로만 |
| 19 | 네트워크 → 인접 행렬 (`image21`) | `sec:everything-matrix`, `fig:attr-network` | R15~R17 |
| 20 | Kahoot 퀴즈 | 없음 | 내용 없음 |

## 4. 재계산 표

### 4.1 AC-W6 대상 (본문에 반드시 나와야 하는 값)

| ID | 슬라이드 | 항목 | 슬라이드 값 | 재계산 | 판정 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| R1 | 8 | 이름/급여/나이 표: 행, 열 | 5행, 3열 | 머리글 1행 제외 5행, 열 3 | 맞음 |
| R2 | 8 | 객체 수, 특징 수 | 5, 2 | 5, $3-1=2$ (Name 제외), $\mathbb{R}^{5\times2}$ | 맞음 |
| R3 | 11 | 급여/나이/근속 배열 크기 | 5×3 | 5×3 (이 표에는 Name 열이 없음) | 맞음 |
| R4 | 11 | 셀 수 | (없음) | $5\times3=15$ | 추가(E1 반례) |
| R5 | 11 | 배열 차원, 공간 차원 | 2, 3 | 2(인덱스 두 개), 3(속성 3개) | 맞음 |
| R6 | 12 | 100차원 데이터 배열 | 2D 배열 | $n\times100$, 배열 차원 2 | 맞음 |
| R7 | 9 | "프로그래밍의 차원 = 셀 수" | 셀 수 | 인덱스(축) 수. 5×3 배열: 셀 15, 차원 2 | **오류 E1** |
| R8 | 9, 12 | `image6` 마지막 열 머리글 | Feature n | Feature d ($n$ 은 행 수, 슬라이드 6) | **오류 E2** |
| R9 | 12 | 고차원 데이터 = 행이 많음 | 포함 | 행이 많음 = 큰 $n$(대용량), 고차원은 큰 $d$ 뿐 (슬라이드 9 정의) | **오류 E3** |
| R10 | 14 | 붓꽃 표 크기 | 150행, $X_1\sim X_5$ | 150×5, 수치 150×4, $X_5$ 명목 | 맞음 |
| R11 | 14 | 슬라이드 10행이 실제 붓꽃에 있는가 | 10행 | T11이 `load_iris()` 행 집합 포함 여부 출력(10/10 기대) | T11 확인 |
| R12 | 15 | 평균 점 $(\bar X_1,\bar X_2)$ | 그림상 약 (5.84, 3.05) | 5.843, 3.057 (`load_iris` 기준 손계산; UCI 원본이면 너비 3.054) | T11 출력으로 확정 |
| R13 | 13 | 벡터 표 크기 | 5×2 | 5×2, 점 5개 = 화살표 5개 | 맞음 |
| R14 | 17 | "King" 벡터 길이 | 값 목록 + 색 칸 0~49 | 값 개수 $10+11+10+11+8=50$ (줄별로 셈), 색 칸 인덱스 0~49 = 50 | 맞음 |
| R15 | 19 | 인접 행렬 크기, 대칭 | 5×5 | 5×5, $A=A^T$ (A-B, A-C, A-D, B-D, B-E, C-D, D-E 7개 간선) | 맞음 |
| R16 | 19 | D의 자기 고리(Self-loop) | $A_{DD}=1$ | 그림의 D 아래 고리와 일치 | 맞음 |
| R17 | 19 | 행렬 원소 합 | (없음) | 행 합 A 3, B 3, C 2, D 5, E 2 → $3+3+2+5+2=15 = 2\times7+1$ (간선 7개는 두 번, 자기 고리는 한 번) | 추가 |
| R18 | (HW1) | HW1 행렬 크기 | (없음) | 저장 126×8, 속성 7(`item` 제외), 수치 $\mathbb{R}^{126\times5}$. `item` 고유값 수는 T11 출력 | 추가, T11 확인 |
| R19 | 4 | 판정 답 | 명목, 구간, 순서, 비율, 명목 | 동일 | 맞음 |

### 4.2 선택 예제 값 (`sec:attr-apply`, AC-W6 대상 아님, 쓰면 이 값으로)

슬라이드 10 데이터(나이, 급여). 손계산, T11이 출력해 확정.

| 쌍 | 원 단위 유클리드 거리 | 범위 정규화 후 (나이 범위 21, 급여 범위 15000) |
| :-- | :-- | :-- |
| Jane–Dave | $\sqrt{1^2+0^2}=1$ | $1/21=0.0476$ |
| Jane–John | $\sqrt{4^2+5000^2}=\sqrt{25{,}000{,}016}\approx5000.0016$ | $\sqrt{(4/21)^2+(5000/15000)^2}=\sqrt{0.03628+0.11111}\approx0.3839$ |

요점: 원 단위에서는 거리가 거의 급여 차이 그 자체다. 정규화(`\Cref{sec:normalization}`) 뒤에야
나이가 거리에 기여한다.

## 5. 그림과 표

### 5.1 데이터 그림 (PNG, T11이 만든다)

생성기 `hw1/00_lecture_charts/deck3_data_matrix.py`, 출력 `hw1/00_lecture_charts/figures/`,
`style.save()` 사용, `main.py` 에 다른 덱과 같은 방식으로 한 줄 연결.

| 파일 | 슬라이드 | 라벨 | 데이터 출처 | 내용 |
| :-- | :-- | :-- | :-- | :-- |
| `03_01_salary_age_2d.png` | 10 | `fig:attr-2d-scatter` | 스크립트 상수(슬라이드 8 `image5` 전사) | x 나이, y 급여, 점 5개 이름 표기. Jane/Dave 겹침은 주석 화살표 |
| `03_02_salary_age_service_3d.png` | 11 | `fig:attr-3d-scatter` | 스크립트 상수(슬라이드 11 `image9` 전사, 이름은 행 라벨로만) | matplotlib 3D 산점도, 축 범위가 모든 점을 포함하도록(C1) |
| `03_03_vectors_origin.png` | 13 | `fig:attr-vectors` | 스크립트 상수(`image11` 전사) | 원점에서 각 점까지 화살표, 화살촉이 점에서 끝남(C2) |
| `03_04_iris_points_mean.png` | 15 | `fig:attr-iris-mean` | `sklearn.datasets.load_iris()` 값만(학습 없음) | 꽃받침 길이 × 너비 150점(겹침 보이게 투명도), 평균 점, 점선 보조선 |

상수는 스크립트 안에 "transcribed from deck 3 slide K, media/imageN" 주석과 함께 둔다. 별도
데이터 파일은 만들지 않는다(YAGNI).

### 5.2 TikZ 도식과 LaTeX 표 (T12가 직접)

- `fig:attr-image-matrix` (슬라이드 16): 이미지 상자 → 영역 $r_1,r_2$ → 행렬(행 = 영역, 열 =
  RGB 색, 질감, …).
- `fig:attr-network` (슬라이드 19): 노드 A~E 그래프(D 자기 고리 포함) → 5×5 인접 행렬.
- 표: `tab:attr-discrete-2x2`, `tab:attr-synonyms`, `tab:attr-name-salary-age`,
  `tab:attr-dimension-two-meanings`, `tab:attr-3d-data`, `tab:attr-iris-rows`.
- 수식: 데이터 행렬 $\mathbf{D}$(`eq:data-matrix`, 참조할 때만 번호).

### 5.3 T11 생성기가 출력(print)할 확인값

R5 셀 수 15, R11 슬라이드 붓꽃 10행 포함 수, R12 평균 점(소수 넷째 자리), R15 대칭 여부, R17
행 합(3, 3, 2, 5, 2)과 원소 합 15, R18 HW1 `df.shape` 와 `item` 고유값 수(`data.load()` 사용), 4.2절 네 거리. 모두
산술과 데이터 읽기뿐이다. 모형 학습, `fit`, 노트북 실행 금지를 T11 프롬프트에 명시한다.

## 6. `\Cref` 대상 (확인함)

2026-09-24 `chapters/*.tex` 에서 `\label` 존재를 grep으로 확인.

| 라벨 | 파일 | 쓰는 곳 |
| :-- | :-- | :-- |
| `ch:attributes`, `sec:attr-flow`, `sec:attr-numeric`, `sec:attr-categorical`, `sec:attr-stats` | 01 | 배경, discrete, vector |
| `def:interval-ratio`, `def:nominal-ordinal`, `tab:attr-ops`, `ex:hw1-types` | 01 | discrete, data-matrix, apply |
| `ch:descriptive`, `sec:center`, `sec:missing` | 02 | 배경 |
| `ch:visualization` | 03 | 배경 |
| `ch:hw1` | 05-hw1-casebook | apply |
| `sec:discretization`, `sec:normalization`, `sec:qq-iris-source`, `tab:qq-iris-bins` | lec07 | vector, apply, future |
| `ch:hypothesis` | lec09 | future (선택) |

새 라벨(이 장에서 만든다): 2절의 `sec:attr-background`, `sec:attr-discrete`, `sec:data-matrix`,
`sec:dimension`, `sec:vector`, `sec:everything-matrix`, `sec:attr-apply`, `sec:attr-future`,
`ex:attr-slide4`, `ex:attr-name-salary-age`, 5절의 `fig:`/`tab:`/`eq:` 라벨. 다른 장에 같은
이름이 없는지 T12가 빌드(AC-W2 multiply defined 0)로 확인한다.

## 7. 슬라이드 오류와 모호성

### 7.1 오류 (Q4 pitfall, "슬라이드 값은 X, 다시 계산하면 Y")

- **E1 (슬라이드 9):** 슬라이드 값은 "프로그래밍의 차원 = 셀의 수", 다시 따지면 "배열의 인덱스
  (축) 수". 5×3 배열은 셀 15개지만 차원은 2다. 슬라이드 11 자신이 이 표를 "2차원 배열"이라 부른다. (8절 D3-Q1b: 오류로 드러낼지 확인.)
- **E2 (슬라이드 9, 12의 `image6`):** 슬라이드 값은 마지막 열 머리글 "Feature n", 슬라이드 6의
  기호로 다시 쓰면 "Feature d"($n$ 은 행 수). 기호 충돌이다.
- **E3 (슬라이드 12):** 슬라이드는 "행이 많음"도 고차원 데이터로 든다. 슬라이드 9의 정의(차원 수
  = 특징 수)로 다시 따지면 고차원은 $d$ 가 클 때뿐이고, 행이 많은 것은 큰 $n$(대용량 데이터)이다.
  (8절 D3-Q1: 오류로 드러낼지 확인.)

### 7.2 모호성 (pitfall, 오류 형식 아님)

- **M1 (슬라이드 8 대 11, T12 AC의 pitfall):** 두 슬라이드 모두 5×3이라 말하지만 세는 표가 다르다.
  슬라이드 8의 3열은 Name(식별자) 포함, 속성 2. 슬라이드 11의 5×3은 Name 열을 빼고 근속연수를
  더한 표, 속성 3. 이름은 3D 그림에서 점의 라벨로만 남는다. Name 열까지 배열에 넣으면 5×4.
  규칙 하나로 정리: "식별자는 속성이 아니다. 차원 = 식별자를 뺀 열 수."

### 7.3 그림의 표시 문제 (재생성 그림에서 고치고, pitfall 없음)

- **C1 (슬라이드 11 `image10`):** 급여 축이 76k부터라 Delilah(75000)가 가장 낮은 눈금 아래에, 나이
  축 눈금이 35~50이라 Delilah(32), Dave(53)가 눈금 밖에 있다.
- **C2 (슬라이드 13 `image12`):** 화살촉이 점을 지나쳐 끝난다. 벡터는 원점에서 점까지다.

## 8. 소유자 질문

- **D3-Q1:** 슬라이드 12의 "고차원 = 행이 많음"(E3)을 오류 pitfall로 드러내는가, 아니면 "큰
  데이터의 두 방향"이라는 뜻으로 읽고 용어만 바로잡는가? 권고: pitfall로 드러낸다(Q4와 같은 이유).
- **D3-Q1b:** 슬라이드 9의 "프로그래밍의 차원 = 셀 수"(E1)는 "5×3이라는 크기가 셀 수를 알려 준다"로
  너그럽게 읽을 여지가 있다. 오류 pitfall로 드러내는가, "두 뜻 표"에서 배열 차원 = 축 수로 바로잡기만
  하는가? 권고: pitfall(슬라이드 11이 같은 표를 "2차원 배열"이라 불러 문구끼리 어긋난다).
- **D3-Q3:** M1(슬라이드 8 대 11)은 값 오류가 아니라 세는 대상의 모호성이다. 이 pitfall을 AC-W7의
  "슬라이드 값은 X, 다시 계산하면 Y" 문형에서 면제하는가? 권고: 면제(9절 AC 메모 참조).
- **D3-Q2:** 장 제목("속성 유형"과 부제 "값의 종류를 먼저 가른다")이 새 절(행렬, 차원, 벡터)을 포괄하지
  않는다. 권고: 이번 채우기에서는 바꾸지 않고(AC-W12 삭제 0), Q6 줄표 정리 과제 때 함께 결정.

## 9. pm에게 넘길 설계 단위

- T11은 **실행한다**(데이터 그림 4개, "n/a" 아님). 크기 소. 입력 = 5절, 확인값 = 5.3절.
- T12는 T11 검토 뒤. 새 절 8개 + 장 머리 In brief, 표 6개, TikZ 2개, PNG 4개 참조. 크기 중.
- **AC 메모(T13이 읽을 것):** M1 pitfall은 AC-W7 문형 면제(D3-Q3 확정 시). 값 오류가 아니라
  세는 대상의 모호성이기 때문이다.
- T12 AC 보강 후보(pm 판단): pitfall E2 확정, E1과 E3는 D3-Q1b/D3-Q1 결과에 따라, + M1 한 개,
  "King 벡터 50개", "5×3 배열 셀 15 차원 2", HW1 "126×8 → 7 → 126×5".

## 결정 기록 (2026-09-24, 메인 세션, 소유자 기존 결정에서 도출)

- **D3-Q1, D3-Q1b:** E1, E3 모두 pitfall 상자로 드러낸다 (Q4).
- **D3-Q3:** 오류가 아닌 모호성(슬라이드 8 대 11)은 "슬라이드 값은 X, 다시 계산하면 Y" 문형에서 면제한다. "두 슬라이드가 세는 대상이 다르다"로 쓴다.
- **D3-Q2:** 장 제목은 바꾸지 않는다 (Q2: 기존 본문 불변). 제목의 줄표 정리는 백로그 X01에서 따로 한다.
