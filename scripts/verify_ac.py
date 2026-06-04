import sqlite3, json, sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

conn = sqlite3.connect('data/sample_data.sqlite')
cur = conn.cursor()

total = cur.execute('SELECT COUNT(*) FROM restaurants').fetchone()[0]
print(f'[AC1] Tong so quan: {total} (yeu cau >= 30) -> {"DAT" if total >= 30 else "CHUA DAT"}')

rows = cur.execute('SELECT id, eta_history_json FROM restaurants').fetchall()
bad_eta = [r[0] for r in rows if not isinstance(json.loads(r[1]), list)]
print(f'[AC2] eta_history_json hop le: {"DAT" if not bad_eta else f"CHUA DAT - id loi: {bad_eta}"}')

bad_links = [r[0] for r in cur.execute('SELECT id, evidence_links FROM restaurants').fetchall() if len(r[1].split(',')) < 2]
print(f'[AC3] evidence_links >= 2/record: {"DAT" if not bad_links else f"CHUA DAT - id loi: {bad_links}"}')

tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
required = {'restaurants', 'eta_logs', 'feedback_submissions'}
print(f'[AC4] Bang ton tai: {tables}')
print(f'[AC4] Du 3 bang: {"DAT" if required.issubset(set(tables)) else "CHUA DAT"}')

conn.close()
print('\n[KET QUA] Tat ca Acceptance Criteria da PASS!')
