# 다시 만들기

1. 그림: `python3 -I tools/make_site.py <출력폴더> <임시폴더>` → `<출력폴더>/img/…`와 `data.json`이 생김. `img/`를 저장소로 복사.
2. 페이지: `template.html`의 `/*DATA*/`를 `data.json` 내용으로, `/*SHEET_URL*/`을 Apps Script 웹 앱 주소로 바꾸고, `<!doctype html>` 머리를 붙여 `index.html`로 저장(지금 `index.html`의 머리 부분 참고).
3. commit · push → GitHub Pages가 1분 안에 갱신.
