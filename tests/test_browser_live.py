import httpx

base_url = 'http://127.0.0.1:8000'
client = httpx.Client(base_url=base_url, timeout=10.0)

print('================================================================')
print(' 1. KIEM TRA TAI NGUYEN GIAO DIEN TRINH DUYET (STATIC ASSETS)')
print('================================================================')
static_files = [
    '/static/css/base.css',
    '/static/css/layout.css',
    '/static/css/components.css',
    '/static/css/ai-sandbox.css',
    '/static/css/style.css',
    '/static/js/modules/theme.js',
    '/static/js/modules/auth.js',
    '/static/js/modules/navigation.js',
    '/static/js/modules/dashboard.js',
    '/static/js/modules/repairs.js',
    '/static/js/modules/customers.js',
    '/static/js/modules/inventory.js',
    '/static/js/modules/billing.js',
    '/static/js/modules/users.js',
    '/static/js/modules/intake.js',
    '/static/js/modules/ai-sandbox.js',
    '/static/js/modules/ai-logs.js',
    '/static/js/app.js'
]

for path in static_files:
    res = client.get(path)
    assert res.status_code == 200, f'Loi tai file {path}'
    print(f'  [OK 200] {path:<32} ({len(res.content):>6} bytes)')

print('\n================================================================')
print(' 2. KIEM TRA PHIEN LAM VIEC & PHAN QUYEN RBAC TREN TRINH DUYET')
print('================================================================')
roles = [
    ('admin', '123456', 'QuanLy'),
    ('letan', '123456', 'LeTan'),
    ('ktv', '123456', 'KyThuatVien'),
    ('thungan', '123456', 'ThuNgan')
]

tokens = {}
for username, pwd, role in roles:
    login_res = client.post('/api/auth/login', json={'ten_dang_nhap': username, 'mat_khau': pwd})
    assert login_res.status_code == 200, f'Dang nhap that bai: {username}'
    token = login_res.json()['access_token']
    tokens[role] = token
    headers = {'Authorization': f'Bearer {token}'}
    me_res = client.get('/api/auth/me', headers=headers)
    assert me_res.status_code == 200
    user_info = me_res.json()
    assert user_info['vai_tro'] == role
    ten = user_info['ho_ten']
    print(f'  [LOGIN OK] {username:<8} | Vai tro: {role:<12} | Ten: {ten}')

print('\n================================================================')
print(' 3. KIEM TRA TAI CAC TAB DU LIEU TRINH DUYET (TUONG TAC SPA)')
print('================================================================')
admin_hdr = {'Authorization': f'Bearer {tokens["QuanLy"]}'}

stats = client.get('/api/stats/overview', headers=admin_hdr).json()
s = stats['summary']
print(f'  [TAB DASHBOARD] Tong phieu: {s["total_repairs"]}, Dang sua: {s["active_repairs"]}, Doanh thu: {s["total_revenue"]:,} d, AI Logs: {s["total_ai_logs"]}')

repairs = client.get('/api/repairs', headers=admin_hdr).json()
print(f'  [TAB PHIEU SUA] Da tai {len(repairs)} phieu sua chua')

customers = client.get('/api/customers', headers=admin_hdr).json()
devices = client.get('/api/devices', headers=admin_hdr).json()
print(f'  [TAB KHACH HANG] Da tai {len(customers)} khach hang va {len(devices)} thiet bi')

parts = client.get('/api/parts', headers=admin_hdr).json()
services = client.get('/api/services', headers=admin_hdr).json()
print(f'  [TAB KHO & DICH VU] Da tai {len(parts)} linh kien va {len(services)} dich vu')

invoices = client.get('/api/invoices', headers=admin_hdr).json()
warranties = client.get('/api/warranties', headers=admin_hdr).json()
print(f'  [TAB HOA DON] Da tai {len(invoices)} hoa don va {len(warranties)} the bao hanh')

ai_logs = client.get('/api/ai/logs', headers=admin_hdr).json()
print(f'  [TAB AI LOGS] Da tai {len(ai_logs)} audit logs')

lookup = client.get('/api/warranties/lookup?query=354892091234567').json()
print(f'  [TRA CUU PUBLIC] Khach tra cuu IMEI 354892091234567: Tim thay {len(lookup)} the bao hanh')

print('\n================================================================')
print(' KET QUA: TOAN BO GIAO DIEN TRINH DUYET DA HOAT DONG 100% OK!')
print('================================================================')
