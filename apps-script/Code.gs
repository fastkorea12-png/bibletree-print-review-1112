// 바이블트리 11–12월 인쇄 검수 기록 — 구글 시트 웹 앱
// 시트 1행: id, at, name, book, spread, st, text, token
// 배포: 확장 프로그램 > Apps Script에 붙여 넣고, 배포 > 새 배포 > 웹 앱
//       (실행 계정: 나, 액세스 권한: 모든 사용자)

const BOOKS = ['low', 'high', 'teen', 'young'];
const STATES = ['ok', 'fix', 'memo'];

function sheet_() {
  return SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
}

// 수식으로 읽히지 않게(= + - @ 로 시작하는 글)
function plain_(s, max) {
  s = String(s == null ? '' : s).slice(0, max);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function notes_() {
  const sh = sheet_();
  const n = sh.getLastRow() - 1;
  if (n < 1) return [];
  return sh.getRange(2, 1, n, 7).getValues().map(function (r) {
    return { id: String(r[0]), at: Number(r[1]), name: String(r[2]), book: String(r[3]), spread: Number(r[4]), st: String(r[5]), text: String(r[6]) };
  });
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

function doGet() {
  return json_({ ok: true, notes: notes_() });
}

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const d = JSON.parse(e.postData.contents);
    const sh = sheet_();
    const token = String(d.token || '').slice(0, 64);
    if (!token) return json_({ ok: false, error: 'token' });
    if (d.action === 'add') {
      const name = String(d.name || '').trim();
      const spread = Number(d.spread);
      if (!name || BOOKS.indexOf(d.book) < 0 || STATES.indexOf(d.st) < 0 || !(spread >= 0 && spread <= 64 && spread % 1 === 0)) {
        return json_({ ok: false, error: 'invalid' });
      }
      const id = Utilities.getUuid().slice(0, 8) + Date.now().toString(36);
      sh.appendRow([id, Date.now(), plain_(name, 40), d.book, spread, d.st, plain_(d.text, 2000), token]);
      return json_({ ok: true, id: id, notes: notes_() });
    }
    if (d.action === 'delete') {
      const n = sh.getLastRow() - 1;
      if (n >= 1) {
        const rows = sh.getRange(2, 1, n, 8).getValues();
        for (let i = rows.length - 1; i >= 0; i--) {
          if (String(rows[i][0]) === String(d.id) && String(rows[i][7]) === token) { sh.deleteRow(i + 2); break; }
        }
      }
      return json_({ ok: true, notes: notes_() });
    }
    return json_({ ok: false, error: 'action' });
  } finally {
    lock.releaseLock();
  }
}
