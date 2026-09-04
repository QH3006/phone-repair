/**
 * Module Kho Linh Kiện & Dịch Vụ Sửa Chữa (Inventory & Services)
 */

let allPartsData = [];
let allServicesData = [];

async function loadInventoryData() {
    try {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const lowStock = document.getElementById('inventory-low-stock-checkbox')?.checked || false;

        // 1. Tải Linh Kiện
        const resParts = await fetch(`/api/parts${lowStock ? '?low_stock=true' : ''}`, { headers });
        if (resParts.ok) {
            allPartsData = await resParts.json();
            renderPartsTable(allPartsData);
        }

        // 2. Tải Dịch Vụ
        const resSrv = await fetch('/api/services', { headers });
        if (resSrv.ok) {
            allServicesData = await resSrv.json();
            renderServicesTable(allServicesData);
        }
    } catch (e) {
        console.error('Lỗi tải dữ liệu kho & dịch vụ:', e);
    }
}

function renderPartsTable(data) {
    const tbody = document.getElementById('parts-tbody');
    if (!tbody) return;

    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:30px; color:var(--text-muted);">Không có linh kiện nào.</td></tr>';
        return;
    }

    const currentRole = (typeof getCurrentUserRole === 'function') ? getCurrentUserRole() : 'QuanLy';
    const canEdit = (currentRole === 'QuanLy');

    let html = '';
    data.forEach(p => {
        const isLow = p.so_luong_ton <= 5;
        html += `
            <tr>
                <td>
                    <strong>${p.ten_linh_kien}</strong><br>
                    <small style="color:var(--text-muted)"><code>${p.ma_linh_kien}</code></small>
                </td>
                <td>${p.loai_may || '<span style="color:var(--text-muted)">Dùng chung</span>'}</td>
                <td><strong style="color:var(--primary);">${Number(p.gia_ban).toLocaleString('vi-VN')} đ</strong></td>
                <td style="text-align:center;">
                    <span class="badge ${isLow ? 'badge-danger' : 'badge-success'}">${p.so_luong_ton} cái</span>
                </td>
                <td style="text-align:center;">${p.thoi_han_bao_hanh_thang} tháng</td>
                <td style="text-align:center;">
                    ${canEdit ? `
                        <button class="btn btn-outline btn-sm" onclick="openPartModal(${p.id})">✏️ Sửa</button>
                    ` : `
                        <span style="color:var(--text-muted); font-size:0.8rem;">👁️ Xem</span>
                    `}
                </td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

function renderServicesTable(data) {
    const tbody = document.getElementById('services-tbody');
    if (!tbody) return;

    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding:30px; color:var(--text-muted);">Chưa có dịch vụ kỹ thuật nào.</td></tr>';
        return;
    }

    const currentRole = (typeof getCurrentUserRole === 'function') ? getCurrentUserRole() : 'QuanLy';
    const canEdit = (currentRole === 'QuanLy');

    let html = '';
    data.forEach(s => {
        html += `
            <tr>
                <td>
                    <strong>${s.ten_dich_vu}</strong><br>
                    <small style="color:var(--text-muted)"><code>${s.ma_dich_vu}</code></small>
                </td>
                <td><strong style="color:var(--success);">${Number(s.gia_cong).toLocaleString('vi-VN')} đ</strong></td>
                <td><small>${s.mo_ta || '<span style="color:var(--text-muted)">Theo tiêu chuẩn</span>'}</small></td>
                <td style="text-align:center;">
                    ${canEdit ? `
                        <button class="btn btn-outline btn-sm" onclick="openServiceModal(${s.id})">✏️ Sửa</button>
                    ` : `
                        <span style="color:var(--text-muted); font-size:0.8rem;">👁️ Xem</span>
                    `}
                </td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

function filterInventoryLive() {
    const q = (document.getElementById('inventory-search-input')?.value || '').toLowerCase().trim();
    if (!q) {
        renderPartsTable(allPartsData);
        renderServicesTable(allServicesData);
        return;
    }
    const filteredParts = allPartsData.filter(p => 
        (p.ten_linh_kien && p.ten_linh_kien.toLowerCase().includes(q)) ||
        (p.ma_linh_kien && p.ma_linh_kien.toLowerCase().includes(q)) ||
        (p.loai_may && p.loai_may.toLowerCase().includes(q))
    );
    renderPartsTable(filteredParts);

    const filteredServices = allServicesData.filter(s =>
        (s.ten_dich_vu && s.ten_dich_vu.toLowerCase().includes(q)) ||
        (s.ma_dich_vu && s.ma_dich_vu.toLowerCase().includes(q))
    );
    renderServicesTable(filteredServices);
}

// Modal Handlers
function openPartModal(id = null) {
    document.getElementById('part-form-id').value = id || '';
    if (id) {
        const p = allPartsData.find(x => x.id === id);
        if (p) {
            document.getElementById('part-modal-title').innerText = '✏️ Cập Nhật Linh Kiện';
            document.getElementById('part-form-code').value = p.ma_linh_kien;
            document.getElementById('part-form-model').value = p.loai_may || '';
            document.getElementById('part-form-name').value = p.ten_linh_kien;
            document.getElementById('part-form-cost').value = p.gia_nhap;
            document.getElementById('part-form-price').value = p.gia_ban;
            document.getElementById('part-form-qty').value = p.so_luong_ton;
            document.getElementById('part-form-warranty').value = p.thoi_han_bao_hanh_thang;
        }
    } else {
        document.getElementById('part-modal-title').innerText = '📦 Nhập Linh Kiện Mới';
        document.getElementById('part-form-code').value = '';
        document.getElementById('part-form-model').value = '';
        document.getElementById('part-form-name').value = '';
        document.getElementById('part-form-cost').value = '200000';
        document.getElementById('part-form-price').value = '450000';
        document.getElementById('part-form-qty').value = '10';
        document.getElementById('part-form-warranty').value = '6';
    }
    document.getElementById('part-modal').style.display = 'flex';
}

function closePartModal() {
    document.getElementById('part-modal').style.display = 'none';
}

async function submitPartForm(e) {
    e.preventDefault();
    const id = document.getElementById('part-form-id').value;
    const body = {
        ma_linh_kien: document.getElementById('part-form-code').value.trim(),
        ten_linh_kien: document.getElementById('part-form-name').value.trim(),
        loai_may: document.getElementById('part-form-model').value.trim() || null,
        gia_nhap: parseFloat(document.getElementById('part-form-cost').value),
        gia_ban: parseFloat(document.getElementById('part-form-price').value),
        so_luong_ton: parseInt(document.getElementById('part-form-qty').value),
        thoi_han_bao_hanh_thang: parseInt(document.getElementById('part-form-warranty').value)
    };

    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const url = id ? `/api/parts/${id}` : '/api/parts';
    const method = id ? 'PUT' : 'POST';

    try {
        const res = await fetch(url, { method, headers, body: JSON.stringify(body) });
        const json = await res.json();
        if (res.ok) {
            alert(id ? 'Cập nhật linh kiện thành công!' : 'Thêm linh kiện mới thành công!');
            closePartModal();
            loadInventoryData();
        } else {
            alert(`Lỗi: ${json.detail || 'Không thể lưu linh kiện'}`);
        }
    } catch (err) {
        alert('Lỗi kết nối server.');
    }
}

function openServiceModal(id = null) {
    document.getElementById('service-form-id').value = id || '';
    if (id) {
        const s = allServicesData.find(x => x.id === id);
        if (s) {
            document.getElementById('service-modal-title').innerText = '✏️ Cập Nhật Dịch Vụ';
            document.getElementById('service-form-code').value = s.ma_dich_vu;
            document.getElementById('service-form-name').value = s.ten_dich_vu;
            document.getElementById('service-form-price').value = s.gia_cong;
            document.getElementById('service-form-desc').value = s.mo_ta || '';
        }
    } else {
        document.getElementById('service-modal-title').innerText = '🛠️ Thêm Dịch Vụ Kỹ Thuật';
        document.getElementById('service-form-code').value = '';
        document.getElementById('service-form-name').value = '';
        document.getElementById('service-form-price').value = '150000';
        document.getElementById('service-form-desc').value = '';
    }
    document.getElementById('service-modal').style.display = 'flex';
}

function closeServiceModal() {
    document.getElementById('service-modal').style.display = 'none';
}

async function submitServiceForm(e) {
    e.preventDefault();
    const id = document.getElementById('service-form-id').value;
    const body = {
        ma_dich_vu: document.getElementById('service-form-code').value.trim(),
        ten_dich_vu: document.getElementById('service-form-name').value.trim(),
        gia_cong: parseFloat(document.getElementById('service-form-price').value),
        mo_ta: document.getElementById('service-form-desc').value.trim() || null
    };

    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const url = id ? `/api/services/${id}` : '/api/services';
    const method = id ? 'PUT' : 'POST';

    try {
        const res = await fetch(url, { method, headers, body: JSON.stringify(body) });
        const json = await res.json();
        if (res.ok) {
            alert(id ? 'Cập nhật dịch vụ thành công!' : 'Thêm dịch vụ mới thành công!');
            closeServiceModal();
            loadInventoryData();
        } else {
            alert(`Lỗi: ${json.detail || 'Không thể lưu dịch vụ'}`);
        }
    } catch (err) {
        alert('Lỗi kết nối server.');
    }
}
