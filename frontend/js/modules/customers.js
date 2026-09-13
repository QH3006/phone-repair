/**
 * Module Khách Hàng & Thiết Bị (Customers & Devices)
 */

let allCustomersData = [];
let allDevicesData = [];

async function loadCustomersData() {
    try {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

        // 1. Tải Khách hàng
        const resCust = await fetch('/api/customers', { headers });
        if (resCust.ok) {
            allCustomersData = await resCust.json();
            renderCustomersTable(allCustomersData);
            populateCustomerSelect(allCustomersData);
        }

        // 2. Tải Thiết bị
        const resDev = await fetch('/api/devices', { headers });
        if (resDev.ok) {
            allDevicesData = await resDev.json();
            renderDevicesTable(allDevicesData);
        }
    } catch (e) {
        console.error('Lỗi tải dữ liệu khách hàng & thiết bị:', e);
    }
}

function renderCustomersTable(data) {
    const tbody = document.getElementById('customers-tbody');
    if (!tbody) return;

    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:30px; color:var(--text-muted);">Không tìm thấy khách hàng nào.</td></tr>';
        return;
    }

    let html = '';
    data.forEach(c => {
        html += `
            <tr>
                <td><strong>${c.ho_ten}</strong></td>
                <td><code>${c.so_dien_thoai}</code></td>
                <td>${c.dia_chi || '<span style="color:var(--text-muted)">Chưa cập nhật</span>'}</td>
                <td style="text-align:center;"><span class="badge badge-info">${c.so_thiet_bi || 0} máy</span></td>
                <td style="text-align:center;">
                    <button class="btn btn-outline btn-sm" onclick="editCustomer(${c.id})">✏️ Sửa</button>
                </td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

function renderDevicesTable(data) {
    const tbody = document.getElementById('devices-tbody');
    if (!tbody) return;

    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding:30px; color:var(--text-muted);">Chưa có thiết bị nào.</td></tr>';
        return;
    }

    let html = '';
    data.forEach(d => {
        html += `
            <tr>
                <td><strong>${d.hang_san_xuat} ${d.model_may}</strong></td>
                <td><code>${d.so_imei}</code></td>
                <td>${d.ten_khach_hang} (${d.so_dien_thoai_khach})</td>
                <td>${formatDevicePassword(d.mat_khau_may)}</td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

function formatDevicePassword(pass) {
    if (!pass || pass.trim() === '' || pass.toLowerCase() === 'none' || pass.toLowerCase() === 'null') {
        return '<span style="color:var(--text-muted); font-size:0.8rem;">🔓 Không khóa</span>';
    }
    const p = pass.trim();
    const isPattern = /vẽ|hình|pattern|chữ|[1-9]-[1-9]/i.test(p);
    if (isPattern) {
        return `<span class="badge badge-purple" style="display:inline-flex; align-items:center; gap:4px; font-weight:600;" title="Mật khẩu vẽ mẫu hình (Pattern Lock)"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="5" cy="5" r="2"/><circle cx="12" cy="5" r="2"/><circle cx="19" cy="5" r="2"/><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="12" cy="19" r="2"/><circle cx="19" cy="19" r="2"/><path d="M5 5h14L5 19h14"/></svg> ${p}</span>`;
    }
    return `<span class="badge badge-warning" style="display:inline-flex; align-items:center; gap:4px; font-weight:600;" title="Mã PIN / Mật khẩu số">🔢 ${p}</span>`;
}

function populateCustomerSelect(customers) {
    const select = document.getElementById('dev-form-customer-select');
    if (!select) return;
    select.innerHTML = customers.map(c => `<option value="${c.id}">${c.ho_ten} - ${c.so_dien_thoai}</option>`).join('');
}

function filterCustomersLive() {
    const q = (document.getElementById('customer-search-input')?.value || '').toLowerCase().trim();
    if (!q) {
        renderCustomersTable(allCustomersData);
        return;
    }
    const filtered = allCustomersData.filter(c => 
        (c.ho_ten && c.ho_ten.toLowerCase().includes(q)) || 
        (c.so_dien_thoai && c.so_dien_thoai.includes(q)) ||
        (c.dia_chi && c.dia_chi.toLowerCase().includes(q))
    );
    renderCustomersTable(filtered);
}

// Modal Handlers
function editCustomer(id) {
    openCustomerModal(id);
}

function openCustomerModal(id = null) {
    const modal = document.getElementById('customer-modal');
    if (!modal) return;

    document.getElementById('cust-form-id').value = id || '';
    if (id) {
        const c = allCustomersData.find(x => x.id === id);
        if (c) {
            document.getElementById('customer-modal-title').innerText = '✏️ Chỉnh Sửa Thông Tin Khách Hàng';
            document.getElementById('cust-form-name').value = c.ho_ten;
            document.getElementById('cust-form-phone').value = c.so_dien_thoai;
            document.getElementById('cust-form-address').value = c.dia_chi || '';
        }
    } else {
        document.getElementById('customer-modal-title').innerText = '➕ Thêm Khách Hàng Mới';
        document.getElementById('cust-form-name').value = '';
        document.getElementById('cust-form-phone').value = '';
        document.getElementById('cust-form-address').value = '';
    }
    modal.classList.add('active');
    modal.style.display = 'flex';
}

function closeCustomerModal() {
    const modal = document.getElementById('customer-modal');
    if (modal) {
        modal.classList.remove('active');
        modal.style.display = 'none';
    }
}

async function submitCustomerForm(e) {
    e.preventDefault();
    const id = document.getElementById('cust-form-id').value;
    const body = {
        ho_ten: document.getElementById('cust-form-name').value.trim(),
        so_dien_thoai: document.getElementById('cust-form-phone').value.trim(),
        dia_chi: document.getElementById('cust-form-address').value.trim() || null
    };

    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const url = id ? `/api/customers/${id}` : '/api/customers';
    const method = id ? 'PUT' : 'POST';

    try {
        const res = await fetch(url, { method, headers, body: JSON.stringify(body) });
        const json = await res.json();
        if (res.ok) {
            alert(id ? 'Cập nhật khách hàng thành công!' : 'Thêm khách hàng mới thành công!');
            closeCustomerModal();
            loadCustomersData();
        } else {
            alert(`Lỗi: ${json.detail || 'Không thể lưu khách hàng'}`);
        }
    } catch (err) {
        alert('Lỗi kết nối server.');
    }
}

function openDeviceModal() {
    const modal = document.getElementById('device-modal');
    if (!modal) return;
    document.getElementById('dev-form-model').value = '';
    document.getElementById('dev-form-imei').value = '';
    document.getElementById('dev-form-pass').value = '';
    modal.classList.add('active');
    modal.style.display = 'flex';
}

function closeDeviceModal() {
    const modal = document.getElementById('device-modal');
    if (modal) {
        modal.classList.remove('active');
        modal.style.display = 'none';
    }
}

function setDevicePassPattern(patternText) {
    const input = document.getElementById('dev-form-pass');
    if (input) input.value = patternText;
}

async function submitDeviceForm(e) {
    e.preventDefault();
    const body = {
        khach_hang_id: parseInt(document.getElementById('dev-form-customer-select').value),
        hang_san_xuat: document.getElementById('dev-form-brand').value,
        model_may: document.getElementById('dev-form-model').value.trim(),
        so_imei: document.getElementById('dev-form-imei').value.trim(),
        mat_khau_may: document.getElementById('dev-form-pass').value.trim() || null
    };

    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const res = await fetch('/api/devices', { method: 'POST', headers, body: JSON.stringify(body) });
        const json = await res.json();
        if (res.ok) {
            alert('Đăng ký thiết bị mới thành công!');
            closeDeviceModal();
            loadCustomersData();
        } else {
            alert(`Lỗi: ${json.detail || 'Không thể đăng ký thiết bị'}`);
        }
    } catch (err) {
        alert('Lỗi kết nối server.');
    }
}
