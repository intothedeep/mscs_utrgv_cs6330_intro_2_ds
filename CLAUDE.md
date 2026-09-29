# CS 6330 Intro to Data Science: repo rules

저장소 고유 사실과 소유자 규칙. 공유 하네스(`.claude/`)는 이식 가능해야 하므로
이 저장소에만 해당하는 규칙은 여기에 둔다 (`.claude/rules/core.md` 권한 순서 3번).

## 소유자 규칙

### 강의 노트 장 파일 이름 (2026-09-23, 저자 결정)

강의 노트 장(`book.md` 원칙 12)은 `chapters/lecNN-slug.tex`(NN = 덱 번호)로 하고,
읽는 순서는 파일 정렬이 아니라 `parts/*.tex`의 `\input` 순서가 정한다.
기존 `NN-slug.tex` 파일은 개명하지 않는다. 과제 장도 같은 방식으로
`chapters/hwNN-slug.tex`를 쓴다.

### 강의 덱은 저자 입력이다 (2026-09-28, 저자 결정)

`book.md` 원칙 13의 "저자가 말한 것"에 강의 덱(`notes/Lecture*.pdf`) 내용이 포함된다.
덱에 있는 내용은 장으로 옮겨도 된다. 덱에 없는 배경, 해석, 결론은 `\todo{}`로 두고 저자에게 묻는다.
