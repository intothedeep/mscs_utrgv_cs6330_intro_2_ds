# CS 6330 Intro to Data Science: repo rules

저장소 고유 사실과 소유자 규칙. 공유 하네스(`.claude/`)는 이식 가능해야 하므로
이 저장소에만 해당하는 규칙은 여기에 둔다 (`.claude/rules/core.md` 권한 순서 3번).

## 소유자 규칙

### 강의 노트 장 파일 이름 (2026-09-23, 저자 결정)

강의 노트 장(`book.md` 원칙 12)은 `chapters/lecNN-slug.tex`(NN = 덱 번호)로 하고,
읽는 순서는 파일 정렬이 아니라 `parts/*.tex`의 `\input` 순서가 정한다.
기존 `NN-slug.tex` 파일은 개명하지 않는다. 과제 장도 같은 방식으로
`chapters/hwNN-slug.tex`를 쓴다.
