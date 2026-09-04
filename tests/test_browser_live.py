import httpx
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

def get_test_client():
    """Trả về httpx.Client (nếu live server 8000 đang mở) hoặc FastAPI TestClient in-memory."""
    try:
        live_client = httpx.Client(base_url="http://127.0.0.1:8000", timeout=2.0)
        res = live_client.get("/static/css/base.css")
        if res.status_code == 200:
            return live_client, True
    except Exception:
        pass
    return TestClient(app), False

def test_browser_static_assets_and_tabs():
    client, is_live = get_test_client()
    mode = "Live Server (http://127.0.0.1:8000)" if is_live else "FastAPI In-Memory TestClient"
    print(f"\n[INFO] Running browser & API checks via: {mode}")

    static_files = [
        '/static/css/base.css',
        '/static/css/layout.css',
        '/static/css/components.css',
        '/static/css/modals.css',
        '/static/css/rbac.css',
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
        '/static/js/modules/tracking-print.js',
        '/static/js/app.js'
    ]

    for path in static_files:
        res = client.get(path)
        assert res.status_code == 200, f'Loi tai file {path}'

    # Kiểm tra cổng tra cứu khách hàng chuyên biệt (/tracking và /tra-cuu)
    res_track = client.get('/tracking')
    assert res_track.status_code == 200
    assert 'PhoneCare AI' in res_track.text

    res_vn = client.get('/tra-cuu')
    assert res_vn.status_code == 200

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

    admin_hdr = {'Authorization': f'Bearer {tokens["QuanLy"]}'}

    stats = client.get('/api/stats/overview', headers=admin_hdr).json()
    assert 'summary' in stats
    assert stats['summary']['total_repairs'] >= 0

    repairs = client.get('/api/repairs', headers=admin_hdr).json()
    assert isinstance(repairs, list)

    customers = client.get('/api/customers', headers=admin_hdr).json()
    devices = client.get('/api/devices', headers=admin_hdr).json()
    assert isinstance(customers, list)
    assert isinstance(devices, list)

    parts = client.get('/api/parts', headers=admin_hdr).json()
    services = client.get('/api/services', headers=admin_hdr).json()
    assert isinstance(parts, list)
    assert isinstance(services, list)

    invoices = client.get('/api/invoices', headers=admin_hdr).json()
    warranties = client.get('/api/warranties', headers=admin_hdr).json()
    assert isinstance(invoices, list)
    assert isinstance(warranties, list)

    ai_logs = client.get('/api/ai/logs', headers=admin_hdr).json()
    assert isinstance(ai_logs, list)

if __name__ == '__main__':
    test_browser_static_assets_and_tabs()
    print('KET QUA: TOAN BO GIAO DIEN TRINH DUYET VA API HOAT DONG 100% OK!')
