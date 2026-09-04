/**
 * Module Hóa Đơn & Bảo Hành Điện Tử (Billing & Warranties)
 */

let allInvoicesData = [];
let allWarrantiesData = [];

async function loadBillingData() {
    try {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

        // 1. Tải Hóa đơn
        const resInv = await fetch('/api/invoices', { headers });
        if (resInv.ok) {
            allInvoicesData = await resInv.json();
            renderInvoicesTable(allInvoicesData);
        }

        // 2. Tải Bảo hành
        const resBh = await fetch('/api/warranties', { headers });
        if (resBh.ok) {
            allWarrantiesData = await resBh.json();
            renderWarrantiesTable(allWarrantiesData);
        }
    } catch (e) {
        console.error('Lỗi tải dữ liệu Hóa đơn & Bảo hành:', e);
    }
}

function renderInvoicesTable(data) {
    const tbody = document.getElementById('invoices-tbody');
    if (!tbody) return;

    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:30px; color:var(--text-muted);">Chưa có hóa đơn nào.</td></tr>';
        return;
    }

    let html = '';
    data.forEach(inv => {
        html += `
            <tr>
                <td>
                    <strong>${inv.ma_hoa_don}</strong><br>
                    <small style="color:var(--text-muted)">Phiếu: ${inv.ma_phieu}</small>
                </td>
                <td>
                    <strong>${inv.ten_khach_hang}</strong><br>
                    <small>${inv.model_may}</small>
                </td>
                <td><strong style="color:var(--primary);">${Number(inv.tong_tien).toLocaleString('vi-VN')} đ</strong></td>
                <td><span class="badge badge-info">${inv.phuong_thuc_tt === 'TienMat' ? '💵 Tiền Mặt' : '💳 Chuyển Khoản'}</span></td>
                <td><small>${inv.ngay_thanh_toan}</small></td>
                <td style="text-align:center;">
                    <button class="btn btn-outline btn-sm" onclick="printInvoice(${inv.id})">🖨️ In HĐ</button>
                </td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

function renderWarrantiesTable(data) {
    const tbody = document.getElementById('warranties-tbody');
    if (!tbody) return;

    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:30px; color:var(--text-muted);">Chưa có phiếu bảo hành nào.</td></tr>';
        return;
    }

    let html = '';
    data.forEach(bh => {
        const isConHan = bh.trang_thai === 'ConHan';
        html += `
            <tr>
                <td>
                    <strong>${bh.ma_bao_hanh}</strong><br>
                    <small>IMEI: <code>${bh.so_imei}</code></small>
                </td>
                <td>
                    <strong>${bh.ten_linh_kien}</strong><br>
                    <small>${bh.ten_khach_hang} - ${bh.model_may}</small>
                </td>
                <td>
                    <small>Từ: ${bh.ngay_bat_dau || 'N/A'}</small><br>
                    <small>Đến: <strong>${bh.ngay_het_han || 'N/A'}</strong></small>
                </td>
                <td>
                    <span class="badge ${isConHan ? 'badge-success' : 'badge-danger'}">
                        ${isConHan ? '🟢 Còn Hạn' : '🔴 Hết Hạn'}
                    </span>
                </td>
                <td style="text-align:center;">
                    <button class="btn btn-outline btn-sm" onclick="printWarranty(${bh.id})">📄 Xem Thẻ</button>
                </td>
            </tr>
        `;
    });
    tbody.innerHTML = html;
}

function filterBillingLive() {
    const q = (document.getElementById('billing-search-input')?.value || '').toLowerCase().trim();
    if (!q) {
        renderInvoicesTable(allInvoicesData);
        renderWarrantiesTable(allWarrantiesData);
        return;
    }
    const filteredInv = allInvoicesData.filter(inv =>
        (inv.ma_hoa_don && inv.ma_hoa_don.toLowerCase().includes(q)) ||
        (inv.ma_phieu && inv.ma_phieu.toLowerCase().includes(q)) ||
        (inv.ten_khach_hang && inv.ten_khach_hang.toLowerCase().includes(q)) ||
        (inv.so_dien_thoai && inv.so_dien_thoai.includes(q))
    );
    renderInvoicesTable(filteredInv);

    const filteredBh = allWarrantiesData.filter(bh =>
        (bh.ma_bao_hanh && bh.ma_bao_hanh.toLowerCase().includes(q)) ||
        (bh.so_imei && bh.so_imei.includes(q)) ||
        (bh.ten_khach_hang && bh.ten_khach_hang.toLowerCase().includes(q)) ||
        (bh.so_dien_thoai && bh.so_dien_thoai.includes(q))
    );
    renderWarrantiesTable(filteredBh);
}

// In Hóa Đơn Modal
function printInvoice(id) {
    const inv = allInvoicesData.find(x => x.id === id);
    if (!inv) return;

    document.getElementById('print-modal-title').innerText = `🧾 HÓA ĐƠN BÁN LẺ & DỊCH VỤ (#${inv.ma_hoa_don})`;
    
    let itemsHtml = '';
    (inv.chi_tiet_items || []).forEach((it, idx) => {
        itemsHtml += `
            <tr>
                <td>${idx + 1}</td>
                <td>${it.ten_muc}</td>
                <td style="text-align:center;">${it.so_luong}</td>
                <td style="text-align:right;">${Number(it.don_gia).toLocaleString('vi-VN')} đ</td>
                <td style="text-align:right;">${Number(it.thanh_tien).toLocaleString('vi-VN')} đ</td>
            </tr>
        `;
    });

    const bodyHtml = `
        <div style="text-align: center; border-bottom: 2px dashed var(--border-color); padding-bottom: 15px; margin-bottom: 15px;">
            <h2 style="margin:0; font-size:1.3rem;">⚡ PHONECARE AI SERVICE CENTER</h2>
            <p style="margin:4px 0; font-size:0.85rem;">Địa chỉ: 120 Cầu Giấy, Hà Nội | Hotline: 1900-8888</p>
            <h3 style="margin:10px 0 0 0; color:var(--primary);">HÓA ĐƠN THANH TOÁN</h3>
            <small>Mã HĐ: <strong>${inv.ma_hoa_don}</strong> | Mã Phiếu: <strong>${inv.ma_phieu}</strong></small>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:0.85rem; margin-bottom:15px;">
            <div><strong>Khách hàng:</strong> ${inv.ten_khach_hang}</div>
            <div><strong>Số điện thoại:</strong> ${inv.so_dien_thoai}</div>
            <div><strong>Thiết bị:</strong> ${inv.model_may}</div>
            <div><strong>Thu ngân:</strong> ${inv.thu_ngan_ten}</div>
            <div><strong>Ngày thanh toán:</strong> ${inv.ngay_thanh_toan}</div>
            <div><strong>Hình thức:</strong> ${inv.phuong_thuc_tt === 'TienMat' ? 'Tiền mặt' : 'Chuyển khoản'}</div>
        </div>

        <table style="width:100%; border-collapse:collapse; font-size:0.85rem; margin-bottom:15px;">
            <thead>
                <tr style="border-bottom:1px solid var(--border-color); background:var(--bg-input);">
                    <th style="text-align:left; padding:6px;">STT</th>
                    <th style="text-align:left; padding:6px;">Chi Tiết Dịch Vụ / Linh Kiện</th>
                    <th style="text-align:center; padding:6px;">SL</th>
                    <th style="text-align:right; padding:6px;">Đơn Giá</th>
                    <th style="text-align:right; padding:6px;">Thành Tiền</th>
                </tr>
            </thead>
            <tbody>
                ${itemsHtml || '<tr><td colspan="5" style="text-align:center; padding:10px;">Chi phí sửa chữa tổng hợp</td></tr>'}
            </tbody>
        </table>

        <div style="text-align:right; font-size:1.1rem; border-top:2px solid var(--border-color); padding-top:10px;">
            <strong>TỔNG TIỀN THANH TOÁN: <span style="color:var(--primary);">${Number(inv.tong_tien).toLocaleString('vi-VN')} VNĐ</span></strong>
        </div>

        <div style="text-align:center; margin-top:20px; font-size:0.8rem; color:var(--text-muted);">
            <p>Cảm ơn Quý khách đã tin tưởng dịch vụ tại PhoneCare AI!</p>
            <p>Tra cứu bảo hành online tại: <strong>phonecare.vn/lookup</strong></p>
        </div>
    `;

    document.getElementById('print-modal-body').innerHTML = bodyHtml;
    document.getElementById('print-modal').style.display = 'flex';
}

// In Bảo Hành Modal
function printWarranty(id) {
    const bh = allWarrantiesData.find(x => x.id === id);
    if (!bh) return;

    document.getElementById('print-modal-title').innerText = `🛡️ THẺ BẢO HÀNH ĐIỆN TỬ (#${bh.ma_bao_hanh})`;

    const bodyHtml = `
        <div style="border: 2px solid var(--primary); border-radius: 10px; padding: 20px; background: rgba(59, 130, 246, 0.03);">
            <div style="text-align: center; border-bottom: 2px solid var(--border-color); padding-bottom: 12px; margin-bottom: 15px;">
                <h2 style="margin:0; color:var(--primary);">⚡ PHONECARE AI WARRANTY CARD</h2>
                <h4 style="margin:4px 0 0 0;">THẺ BẢO HÀNH ĐIỆN TỬ</h4>
                <small>Mã Thẻ: <strong>${bh.ma_bao_hanh}</strong></small>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; font-size:0.85rem; margin-bottom:15px;">
                <div><strong>Chủ sở hữu:</strong> ${bh.ten_khach_hang}</div>
                <div><strong>Số điện thoại:</strong> ${bh.so_dien_thoai}</div>
                <div><strong>Dòng máy:</strong> ${bh.model_may}</div>
                <div><strong>Số IMEI:</strong> <code>${bh.so_imei}</code></div>
                <div><strong>Linh kiện bảo hành:</strong> <span style="color:var(--primary); font-weight:700;">${bh.ten_linh_kien}</span></div>
                <div><strong>Mã phiếu sửa gốc:</strong> ${bh.ma_phieu}</div>
                <div><strong>Ngày kích hoạt:</strong> ${bh.ngay_bat_dau}</div>
                <div><strong>Hạn bảo hành đến:</strong> <strong style="color:var(--success); font-size:0.95rem;">${bh.ngay_het_han}</strong></div>
            </div>

            <div style="background:var(--bg-input); padding:10px 14px; border-radius:6px; font-size:0.8rem; margin-bottom:12px;">
                <strong>Điều kiện bảo hành:</strong> ${bh.dieu_kien_bh || 'Bảo hành lỗi kỹ thuật nhà sản xuất. Không bảo hành rơi vỡ, cấn móp, vào nước.'}
            </div>

            <div style="text-align:center; font-size:0.8rem; color:var(--text-muted);">
                Quý khách vui lòng xuất trình Số điện thoại hoặc IMEI khi cần yêu cầu bảo hành.
            </div>
        </div>
    `;

    document.getElementById('print-modal-body').innerHTML = bodyHtml;
    document.getElementById('print-modal').style.display = 'flex';
}

function closePrintModal() {
    document.getElementById('print-modal').style.display = 'none';
}
