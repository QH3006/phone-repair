/**
 * Module Quản Trị Nhân Sự & Phân Quyền RBAC (Users & RBAC)
 */

let allUsersData = [];

async function loadUsersData() {
    try {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

        const res = await fetch('/api/users', { headers });
        if (res.ok) {
            allUsersData = await res.json();
            renderUsersTable(allUsersData);
        } else if (res.status === 403) {
            const tbody = document.getElementById('users-tbody');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:30px; color:var(--danger);">⚠️ Bạn không có quyền xem danh sách nhân sự (Yêu cầu vai trò: Quản Lý hoặc Lễ Tân).</td></tr>';
            }
        }
    } catch (e) {
        console.error('Lỗi tải dữ liệu người dùng:', e);
    }
}

function renderUsersTable(data) {
    const tbody = document.getElementById('users-tbody');
    if (!tbody) return;

    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:30px; color:var(--text-muted);">Chưa có tài khoản nhân viên nào.</td></tr>';
        return;
    }

    const roleBadge = {
        "QuanLy": '<span class="badge badge-primary">👑 Quản Lý</span>',
        "LeTan": '<span class="badge badge-info">💁 Lễ Tân</span>',
        "KyThuatVien": '<span class="badge badge-warning">🔧 Kỹ Thuật Viên</span>',
        "ThuNgan": '<span class="badge badge-success">💳 Thu Ngân</span>'
    };

    let html = '';
    data.forEach(u => {
        const isLocked = u.trang_thai === 'TamKhoa';
        html += `
            <tr>
                <td><code>${u.ten_dang_nhap}</code></td>
                <td><strong>${u.ho_ten}</strong></td>
                <td>${roleBadge[u.vai_tro] || u.vai_tro}</td>
                <td>${u.so_dien_thoai || '<span style="color:var(--text-muted)">--</span>'}</td>
                <td>
                    <span class="badge ${isLocked ? 'badge-danger' : 'badge-success'}">
                        ${isLocked ? '🔒 Tạm Khóa' : '🟢 Hoạt Động'}
                    </span>
                </td>
                <td style="text-align:center;">
                    <button class="btn btn-outline btn-sm" onclick="openUserModal(${u.id})">✏️ Sửa</button>
                </td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

function openUserModal(id = null) {
    document.getElementById('user-form-id').value = id || '';
    if (id) {
        const u = allUsersData.find(x => x.id === id);
        if (u) {
            document.getElementById('user-modal-title').innerText = '✏️ Chỉnh Sửa Tài Khoản Nhân Viên';
            document.getElementById('user-form-username').value = u.ten_dang_nhap;
            document.getElementById('user-form-username').disabled = true;
            document.getElementById('user-form-password').value = '';
            document.getElementById('user-form-fullname').value = u.ho_ten;
            document.getElementById('user-form-role').value = u.vai_tro;
            document.getElementById('user-form-status').value = u.trang_thai;
            document.getElementById('user-form-phone').value = u.so_dien_thoai || '';
        }
    } else {
        document.getElementById('user-modal-title').innerText = '👥 Thêm Tài Khoản Nhân Viên Mới';
        document.getElementById('user-form-username').value = '';
        document.getElementById('user-form-username').disabled = false;
        document.getElementById('user-form-password').value = '123456';
        document.getElementById('user-form-fullname').value = '';
        document.getElementById('user-form-role').value = 'LeTan';
        document.getElementById('user-form-status').value = 'HoatDong';
        document.getElementById('user-form-phone').value = '';
    }
    document.getElementById('user-modal').style.display = 'flex';
}

function closeUserModal() {
    document.getElementById('user-modal').style.display = 'none';
}

async function submitUserForm(e) {
    e.preventDefault();
    const id = document.getElementById('user-form-id').value;
    const body = {
        ho_ten: document.getElementById('user-form-fullname').value.trim(),
        vai_tro: document.getElementById('user-form-role').value,
        so_dien_thoai: document.getElementById('user-form-phone').value.trim() || null,
        trang_thai: document.getElementById('user-form-status').value
    };

    const pass = document.getElementById('user-form-password').value;
    if (pass) body.mat_khau = pass;

    if (!id) {
        body.ten_dang_nhap = document.getElementById('user-form-username').value.trim();
        if (!pass) body.mat_khau = '123456';
    }

    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const url = id ? `/api/users/${id}` : '/api/users';
    const method = id ? 'PUT' : 'POST';

    try {
        const res = await fetch(url, { method, headers, body: JSON.stringify(body) });
        const json = await res.json();
        if (res.ok) {
            alert(id ? 'Cập nhật nhân viên thành công!' : 'Tạo tài khoản nhân viên thành công!');
            closeUserModal();
            loadUsersData();
        } else {
            alert(`Lỗi: ${json.detail || 'Không thể lưu tài khoản (Yêu cầu quyền Quản Lý)'}`);
        }
    } catch (err) {
        alert('Lỗi kết nối server.');
    }
}
