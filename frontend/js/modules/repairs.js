/**
 * Module Repairs Management (Core CRUD & Repair Lifecycle)
 */

let allRepairsData = [];

// 8 Trạng thái chuẩn hóa trong vòng đời sửa chữa
const REPAIR_STATUS_BADGES = {
    'TiepNhan': '<span class="badge badge-info">1. Tiếp Nhận</span>',
    'PhanCongKTV': '<span class="badge badge-purple">2. Phân Công KTV</span>',
    'DangKiemTra': '<span class="badge badge-warning">3. Đang Kiểm Tra</span>',
    'BaoGia_ChoDuyet': '<span class="badge badge-warning">4. Báo Giá Chờ Duyệt</span>',
    'DangSuaChua': '<span class="badge badge-warning">5. Đang Sửa Chữa</span>',
    'DaSuaXong': '<span class="badge badge-primary">6. Đã Sửa Xong</span>',
    'DaThanhToan': '<span class="badge badge-success">7. Đã Thanh Toán</span>',
    'HoanTat_TraMay': '<span class="badge badge-success">8. Hoàn Tất Bàn Giao</span>'
};

async function loadRepairsData() {
    const tbody = document.getElementById('repairs-tbody');
    if (!tbody) return;
    
    try {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

        const res = await fetch('/api/repairs', { headers });
        if (res.ok) {
            allRepairsData = await res.json();
            renderRepairsTable(allRepairsData);
        } else {
            tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; color:var(--danger)">Lỗi tải dữ liệu (${res.status})</td></tr>`;
        }
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; color:var(--danger)">Lỗi kết nối CSDL: ${e.message}</td></tr>`;
    }
}

function renderRepairsTable(data) {
    const tbody = document.getElementById('repairs-tbody');
    if (!tbody) return;

    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align:center; padding:30px; color:var(--text-muted);">Không tìm thấy phiếu sửa chữa nào.</td></tr>';
        return;
    }

    const currentRole = (typeof getCurrentUserRole === 'function') ? getCurrentUserRole() : 'QuanLy';

    let html = '';
    data.forEach(r => {
        const badge = REPAIR_STATUS_BADGES[r.trang_thai] || `<span class="badge badge-info">${r.trang_thai}</span>`;
        const khName = r.khach_hang ? r.khach_hang.ho_ten : 'N/A';
        const khPhone = r.khach_hang ? r.khach_hang.so_dien_thoai : '';
        const devModel = r.thiet_bi ? `${r.thiet_bi.hang_san_xuat} ${r.thiet_bi.model_may}` : 'N/A';
        const devImei = r.thiet_bi ? r.thiet_bi.so_imei : '';

        // Nút thao tác theo vai trò
        let actionBtnHtml = `<button class="btn btn-outline btn-sm" onclick="viewRepairDetail(${r.id})">🔍 Chi Tiết</button>`;
        if (currentRole === 'ThuNgan') {
            if (r.trang_thai === 'DaSuaXong' && !r.da_thanh_toan) {
                actionBtnHtml = `<button class="btn btn-gradient btn-sm" onclick="quickCreateInvoice(${r.id})">💳 Thu Tiền Ngay</button>`;
            } else {
                actionBtnHtml = `<button class="btn btn-outline btn-sm" onclick="viewRepairDetail(${r.id})">📄 Xem HĐ</button>`;
            }
        } else if (currentRole === 'KyThuatVien') {
            actionBtnHtml = `<button class="btn btn-outline btn-sm" onclick="viewRepairDetail(${r.id})">🔧 Khám & Sửa</button>`;
        } else if (currentRole === 'QuanLy') {
            actionBtnHtml = `<button class="btn btn-outline btn-sm" onclick="viewRepairDetail(${r.id})">🔍 Xem & Sửa</button>`;
        }

        html += `
            <tr>
                <td><strong>${r.ma_phieu}</strong></td>
                <td>
                    <strong>${khName}</strong><br>
                    <small style="color:var(--text-muted)">📞 ${khPhone}</small>
                </td>
                <td>
                    <strong>${devModel}</strong><br>
                    <small style="color:var(--text-muted)">IMEI: ${devImei}</small>
                </td>
                <td><small>${r.mo_ta_loi_khach}</small></td>
                <td><small>${r.ktv_phu_trach || 'Chưa phân công'}</small></td>
                <td>${badge}</td>
                <td><strong style="color:var(--primary);">${Number(r.tong_tien_du_kien || 0).toLocaleString('vi-VN')} đ</strong></td>
                <td style="text-align:center; white-space:nowrap;">
                    ${actionBtnHtml}
                    <button class="btn btn-outline btn-sm" onclick="printRepairReceipt(${r.id})" title="In phiếu tiếp nhận">🖨️ In</button>
                </td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

function filterRepairsLive() {
    const q = (document.getElementById('repair-search-input')?.value || '').toLowerCase().trim();
    const st = document.getElementById('repair-status-filter')?.value || '';

    let filtered = allRepairsData;
    if (st) {
        filtered = filtered.filter(r => r.trang_thai === st);
    }
    if (q) {
        filtered = filtered.filter(r => {
            const kh = r.khach_hang ? `${r.khach_hang.ho_ten} ${r.khach_hang.so_dien_thoai}`.toLowerCase() : '';
            const tb = r.thiet_bi ? `${r.thiet_bi.model_may} ${r.thiet_bi.so_imei}`.toLowerCase() : '';
            const mp = (r.ma_phieu || '').toLowerCase();
            return kh.includes(q) || tb.includes(q) || mp.includes(q);
        });
    }
    renderRepairsTable(filtered);
}

async function viewRepairDetail(phieuId) {
    const modal = document.getElementById('repair-modal');
    const modalBody = document.getElementById('modal-body');
    if (!modal || !modalBody) return;
    
    modalBody.innerHTML = '<p style="text-align:center; padding:20px;">Đang tải chi tiết phiếu...</p>';
    modal.style.display = 'flex';

    try {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

        const res = await fetch(`/api/repairs/${phieuId}`, { headers });
        const r = await res.json();

        const currentRole = (typeof getCurrentUserRole === 'function') ? getCurrentUserRole() : 'QuanLy';
        const canManageItems = (currentRole === 'KyThuatVien' || currentRole === 'QuanLy');
        const canInvoice = (currentRole === 'ThuNgan' || currentRole === 'QuanLy');

        let detailsHtml = '';
        if (r.chi_tiet && r.chi_tiet.length > 0) {
            detailsHtml = r.chi_tiet.map(ct => `
                <tr>
                    <td>${ct.ten_muc}</td>
                    <td><span class="badge ${ct.loai === 'LinhKien' ? 'badge-primary' : 'badge-info'}">${ct.loai}</span></td>
                    <td style="text-align:center;">${ct.so_luong}</td>
                    <td style="text-align:right;">${Number(ct.don_gia).toLocaleString('vi-VN')} đ</td>
                    <td style="text-align:right;"><strong>${Number(ct.thanh_tien).toLocaleString('vi-VN')} đ</strong></td>
                    <td style="text-align:center;">
                        ${canManageItems ? `
                            <button class="btn btn-outline btn-sm" onclick="removeItemFromRepair(${r.id}, ${ct.id})" style="color:var(--danger); padding:2px 6px;">✕</button>
                        ` : `
                            <span style="color:var(--text-muted); font-size:0.75rem;">-</span>
                        `}
                    </td>
                </tr>
            `).join('');
        } else {
            detailsHtml = '<tr><td colspan="6" style="text-align:center; color:var(--text-muted); padding:16px;">Chưa có linh kiện hoặc dịch vụ nào trong phiếu</td></tr>';
        }

        const badge = REPAIR_STATUS_BADGES[r.trang_thai] || `<span class="badge badge-info">${r.trang_thai}</span>`;

        // Lọc các trạng thái được phép chuyển đổi theo vai trò
        const roleStatuses = {
            'QuanLy': ['TiepNhan', 'PhanCongKTV', 'DangKiemTra', 'BaoGia_ChoDuyet', 'DangSuaChua', 'DaSuaXong', 'DaThanhToan', 'HoanTat_TraMay'],
            'LeTan': ['TiepNhan', 'PhanCongKTV', 'BaoGia_ChoDuyet', 'HoanTat_TraMay'],
            'KyThuatVien': ['DangKiemTra', 'DangSuaChua', 'DaSuaXong'],
            'ThuNgan': ['DaThanhToan']
        };
        const allowedStatuses = roleStatuses[currentRole] || roleStatuses['QuanLy'];
        
        const allStatusLabels = {
            'TiepNhan': '1. Tiếp Nhận',
            'PhanCongKTV': '2. Phân Công KTV',
            'DangKiemTra': '3. Đang Kiểm Tra',
            'BaoGia_ChoDuyet': '4. Báo Giá Chờ Duyệt',
            'DangSuaChua': '5. Đang Sửa Chữa',
            'DaSuaXong': '6. Đã Sửa Xong',
            'DaThanhToan': '7. Đã Thanh Toán',
            'HoanTat_TraMay': '8. Hoàn Tất Bàn Giao'
        };

        const statusOptionsHtml = allowedStatuses.map(st => `
            <option value="${st}" ${r.trang_thai === st ? 'selected' : ''}>${allStatusLabels[st]}</option>
        `).join('');

        modalBody.innerHTML = `
            <div style="padding: 20px; max-height: 80vh; overflow-y: auto;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid var(--border-color); padding-bottom:10px;">
                    <div>
                        <h3 style="margin:0; color:var(--primary);">Phiếu Sửa Chữa: ${r.ma_phieu}</h3>
                        <small style="color:var(--text-muted);">Tiếp nhận: ${r.ngay_tiep_nhan || 'N/A'}</small>
                    </div>
                    <div>${badge}</div>
                </div>

                <!-- Thao tác Vòng đời Trạng thái -->
                <div style="background:var(--bg-card); border:1px solid var(--border-color); padding:12px 16px; border-radius:var(--radius-sm); margin-bottom:16px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <label style="font-size:0.85rem; font-weight:600;">🔄 Chuyển Trạng Thái:</label>
                        <select id="modal-status-select" class="form-control" style="width:auto; padding:4px 10px; font-size:0.85rem;">
                            ${statusOptionsHtml}
                        </select>
                        <button class="btn btn-primary btn-sm" onclick="submitStatusUpdate(${r.id})">Cập Nhật</button>
                    </div>

                    <div>
                        ${r.trang_thai === 'DaSuaXong' && !r.da_thanh_toan ? (
                            canInvoice ? `
                                <button class="btn btn-gradient btn-sm" onclick="quickCreateInvoice(${r.id})">💳 Lập Hóa Đơn Thu Tiền</button>
                            ` : `
                                <span class="badge badge-info" style="font-size:0.8rem; padding:6px 10px;">ℹ️ Chờ Thu Ngân lập hóa đơn</span>
                            `
                        ) : ''}
                    </div>
                </div>

                <!-- Thông tin Khách hàng & Thiết bị -->
                <div class="grid-2" style="gap:12px; margin-bottom:16px;">
                    <div style="background:var(--bg-input); padding:12px; border-radius:var(--radius-sm); font-size:0.85rem;">
                        <strong>👤 Khách Hàng:</strong> ${r.khach_hang.ho_ten}<br>
                        <strong>📞 SĐT:</strong> ${r.khach_hang.so_dien_thoai}<br>
                        <strong>📍 Địa chỉ:</strong> ${r.khach_hang.dia_chi || 'N/A'}
                    </div>
                    <div style="background:var(--bg-input); padding:12px; border-radius:var(--radius-sm); font-size:0.85rem;">
                        <strong>📱 Thiết Bị:</strong> ${r.thiet_bi.hang_san_xuat} ${r.thiet_bi.model_may}<br>
                        <strong>🔢 IMEI:</strong> <code>${r.thiet_bi.so_imei}</code><br>
                        <strong>🔐 Mật khẩu máy:</strong> ${r.thiet_bi.mat_khau_may || 'Không có'}
                    </div>
                </div>

                <!-- Tình trạng lỗi -->
                <div style="margin-bottom:16px; font-size:0.85rem;">
                    <strong>Mô tả lỗi khách báo:</strong>
                    <div style="background:var(--bg-input); padding:10px; border-radius:var(--radius-sm); margin-top:4px;">
                        ${r.mo_ta_loi_khach}
                    </div>
                </div>

                ${r.ghi_chu_ky_thuat ? `
                <div style="margin-bottom:16px; font-size:0.85rem;">
                    <strong>Ghi chú kỹ thuật viên:</strong>
                    <div style="background:rgba(245, 158, 11, 0.1); border:1px solid #f59e0b; padding:10px; border-radius:var(--radius-sm); margin-top:4px;">
                        ${r.ghi_chu_ky_thuat}
                    </div>
                </div>
                ` : ''}

                <!-- Bảng Chi Tiết Linh Kiện & Dịch Vụ -->
                <div style="margin-bottom:16px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <h4 style="margin:0; font-size:0.95rem;">📦 Linh Kiện & Dịch Vụ Áp Dụng</h4>
                        ${canManageItems ? `
                            <button class="btn btn-outline btn-sm" onclick="openAddItemModal(${r.id})">➕ Thêm Mục</button>
                        ` : `
                            <span style="color:var(--text-muted); font-size:0.8rem; font-style:italic;">🔒 Chỉ KTV mới có quyền xuất linh kiện</span>
                        `}
                    </div>

                    <table class="data-table" style="font-size:0.85rem;">
                        <thead>
                            <tr>
                                <th>Tên Mục</th>
                                <th>Phân Loại</th>
                                <th style="text-align:center;">SL</th>
                                <th style="text-align:right;">Đơn Giá</th>
                                <th style="text-align:right;">Thành Tiền</th>
                                <th style="text-align:center;">Xóa</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${detailsHtml}
                        </tbody>
                    </table>

                    <div style="text-align:right; margin-top:10px; font-size:1.05rem;">
                        <strong>Tổng tiền: <span style="color:var(--primary);">${Number(r.tong_tien_du_kien || 0).toLocaleString('vi-VN')} VNĐ</span></strong>
                    </div>
                </div>
            </div>
        `;
    } catch (e) {
        modalBody.innerHTML = `<p style="color:var(--danger); padding:20px;">Lỗi: ${e.message}</p>`;
    }
}

function closeModal() {
    document.getElementById('repair-modal').style.display = 'none';
}

async function submitStatusUpdate(phieuId) {
    const status = document.getElementById('modal-status-select')?.value;
    if (!status) return;

    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const res = await fetch(`/api/repairs/${phieuId}/status`, {
            method: 'PATCH',
            headers,
            body: JSON.stringify({ trang_thai: status })
        });
        const json = await res.json();
        if (res.ok) {
            alert('Cập nhật trạng thái thành công!');
            viewRepairDetail(phieuId);
            loadRepairsData();
            loadDashboardData();
        } else {
            alert(`Lỗi: ${json.detail || 'Không thể đổi trạng thái'}`);
        }
    } catch (e) {
        alert('Lỗi kết nối server.');
    }
}

// Add Item Modal
async function openAddItemModal(phieuId) {
    document.getElementById('add-item-repair-id').value = phieuId;
    
    // Tải linh kiện
    const token = localStorage.getItem('token');
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

    const resParts = await fetch('/api/parts', { headers });
    if (resParts.ok) {
        const parts = await resParts.json();
        const selPart = document.getElementById('add-item-part-select');
        selPart.innerHTML = parts.map(p => `<option value="${p.id}">${p.ten_linh_kien} (Tồn: ${p.so_luong_ton}) - ${Number(p.gia_ban).toLocaleString('vi-VN')}đ</option>`).join('');
    }

    // Tải dịch vụ
    const resSrv = await fetch('/api/services', { headers });
    if (resSrv.ok) {
        const srvs = await resSrv.json();
        const selSrv = document.getElementById('add-item-service-select');
        selSrv.innerHTML = srvs.map(s => `<option value="${s.id}">${s.ten_dich_vu} - ${Number(s.gia_cong).toLocaleString('vi-VN')}đ</option>`).join('');
    }

    document.getElementById('add-item-modal').style.display = 'flex';
}

function closeAddItemModal() {
    document.getElementById('add-item-modal').style.display = 'none';
}

function toggleItemTypeSelect() {
    const type = document.getElementById('add-item-type').value;
    if (type === 'linhkien') {
        document.getElementById('group-select-part').style.display = 'block';
        document.getElementById('group-select-service').style.display = 'none';
    } else {
        document.getElementById('group-select-part').style.display = 'none';
        document.getElementById('group-select-service').style.display = 'block';
    }
}

async function submitAddItemToRepair(e) {
    e.preventDefault();
    const phieuId = document.getElementById('add-item-repair-id').value;
    const type = document.getElementById('add-item-type').value;
    const qty = parseInt(document.getElementById('add-item-qty').value) || 1;

    const body = { so_luong: qty };
    if (type === 'linhkien') {
        body.linh_kien_id = parseInt(document.getElementById('add-item-part-select').value);
    } else {
        body.dich_vu_id = parseInt(document.getElementById('add-item-service-select').value);
    }

    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const res = await fetch(`/api/repairs/${phieuId}/items`, {
            method: 'POST',
            headers,
            body: JSON.stringify(body)
        });
        const json = await res.json();
        if (res.ok) {
            alert('Đã thêm mục vào phiếu sửa thành công!');
            closeAddItemModal();
            viewRepairDetail(phieuId);
            loadRepairsData();
        } else {
            alert(`Lỗi: ${json.detail || 'Không thể thêm mục'}`);
        }
    } catch (err) {
        alert('Lỗi kết nối server.');
    }
}

async function removeItemFromRepair(phieuId, itemId) {
    if (!confirm('Bạn có chắc chắn muốn xóa mục này khỏi phiếu sửa chữa?')) return;

    const token = localStorage.getItem('token');
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

    try {
        const res = await fetch(`/api/repairs/${phieuId}/items/${itemId}`, { method: 'DELETE', headers });
        const json = await res.json();
        if (res.ok) {
            viewRepairDetail(phieuId);
            loadRepairsData();
        } else {
            alert(`Lỗi: ${json.detail || 'Không thể xóa mục'}`);
        }
    } catch (e) {
        alert('Lỗi kết nối server.');
    }
}

async function quickCreateInvoice(phieuId) {
    if (!confirm('Xác nhận lập hóa đơn và thanh toán cho phiếu sửa chữa này?')) return;

    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const res = await fetch('/api/invoices', {
            method: 'POST',
            headers,
            body: JSON.stringify({ phieu_sua_chua_id: phieuId, phuong_thuc_tt: 'TienMat' })
        });
        const json = await res.json();
        if (res.ok) {
            alert(`Lập hóa đơn ${json.ma_hoa_don} thành công! Hệ thống đã tự động cấp bảo hành điện tử.`);
            viewRepairDetail(phieuId);
            loadRepairsData();
            loadDashboardData();
        } else {
            alert(`Lỗi: ${json.detail || 'Không thể lập hóa đơn (Yêu cầu quyền Thu Ngân hoặc Quản Lý)'}`);
        }
    } catch (e) {
        alert('Lỗi kết nối server.');
    }
}
