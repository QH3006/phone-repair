/**
 * Module Tracking & Print (Public Customer Lookup, Receipts, Invoices & CSV Export)
 * Đáp ứng các yêu cầu FR-03, FR-07, FR-09 & UC_KH_Track.
 */

const REPAIR_STAGES = [
    { key: 'TiepNhan', label: '1. Tiếp Nhận', icon: '📥' },
    { key: 'PhanCongKTV', label: '2. Phân Công', icon: '👨‍🔧' },
    { key: 'DangKiemTra', label: '3. Kiểm Tra', icon: '🔍' },
    { key: 'BaoGia_ChoDuyet', label: '4. Báo Giá', icon: '💬' },
    { key: 'DangSuaChua', label: '5. Sửa Chữa', icon: '⚙️' },
    { key: 'DaSuaXong', label: '6. Đã Sửa', icon: '✅' },
    { key: 'DaThanhToan', label: '7. Thanh Toán', icon: '💳' },
    { key: 'HoanTat_TraMay', label: '8. Hoàn Tất', icon: '🎉' }
];

function openPublicTrackingModal() {
    const modal = document.getElementById('modal-public-tracking');
    if (modal) {
        modal.style.display = 'flex';
        modal.classList.add('active');
        const input = document.getElementById('public-tracking-input');
        if (input) {
            input.focus();
            if (!input.value) input.value = 'PSC-20260814-001';
            doPublicTrackingSearch();
        }
    }
}

function closePublicTrackingModal() {
    const modal = document.getElementById('modal-public-tracking');
    if (modal) {
        modal.style.display = 'none';
        modal.classList.remove('active');
    }
}

async function doPublicTrackingSearch() {
    const input = document.getElementById('public-tracking-input');
    const container = document.getElementById('public-tracking-results');
    if (!input || !container) return;

    const query = input.value.trim();
    if (!query) {
        alert('Vui lòng nhập Mã phiếu, Số điện thoại hoặc Số IMEI để tra cứu!');
        return;
    }

    container.innerHTML = '<div style="text-align:center; padding:25px; color:var(--primary);"><div class="spinner"></div> Đang kiểm tra tiến độ trên hệ thống...</div>';

    try {
        const res = await fetch(`/api/repairs/lookup?q=${encodeURIComponent(query)}`);
        if (!res.ok) throw new Error(`Lỗi tra cứu: HTTP ${res.status}`);

        const list = await res.json();
        if (!list || list.length === 0) {
            container.innerHTML = `
                <div style="text-align:center; padding:30px; background:rgba(239, 68, 68, 0.05); border:1px solid rgba(239, 68, 68, 0.2); border-radius:var(--radius-sm); color:var(--danger);">
                    ⚠️ Không tìm thấy hồ sơ sửa chữa nào khớp với <strong>"${query}"</strong>.<br>
                    <small style="color:var(--text-muted); margin-top:5px; display:inline-block;">Vui lòng kiểm tra lại mã phiếu hoặc liên hệ hotline 1900.6868 để được hỗ trợ.</small>
                </div>
            `;
            return;
        }

        let html = '';
        list.forEach(r => {
            const currentStageIndex = REPAIR_STAGES.findIndex(s => s.key === r.trang_thai);
            const activeIdx = currentStageIndex >= 0 ? currentStageIndex : 0;

            // Render Timeline 8 bước
            let stepsHtml = '';
            REPAIR_STAGES.forEach((stage, idx) => {
                const isPassed = idx < activeIdx;
                const isCurrent = idx === activeIdx;
                const color = isCurrent ? 'var(--primary)' : (isPassed ? 'var(--success)' : 'var(--text-muted)');
                const bg = isCurrent ? 'rgba(56, 189, 248, 0.15)' : (isPassed ? 'rgba(34, 197, 94, 0.15)' : 'var(--bg-hover)');
                const border = isCurrent ? '2px solid var(--primary)' : (isPassed ? '2px solid var(--success)' : '1px solid var(--border)');

                stepsHtml += `
                    <div style="flex:1; min-width:85px; text-align:center; position:relative;">
                        <div style="width:36px; height:36px; line-height:34px; margin:0 auto 6px; border-radius:50%; background:${bg}; border:${border}; font-size:1rem;">
                            ${stage.icon}
                        </div>
                        <div style="font-size:0.75rem; font-weight:${isCurrent ? '700' : '500'}; color:${color};">
                            ${stage.label}
                        </div>
                    </div>
                `;
            });

            const khTen = r.khach_hang ? r.khach_hang.ho_ten : 'Khách hàng';
            const may = r.thiet_bi ? `${r.thiet_bi.hang_san_xuat} ${r.thiet_bi.model_may}` : 'Thiết bị';
            const imeiMasked = r.thiet_bi && r.thiet_bi.so_imei ? r.thiet_bi.so_imei.slice(0, 4) + '******' + r.thiet_bi.so_imei.slice(-4) : 'N/A';
            const costFormatted = Number(r.chi_phi_uoc_tinh || 0).toLocaleString('vi-VN') + ' đ';

            html += `
                <div style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-md); padding:18px; margin-bottom:18px; box-shadow:var(--shadow-sm);">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:14px; border-bottom:1px solid var(--border); padding-bottom:10px;">
                        <div>
                            <h4 style="margin:0 0 4px; color:var(--text-main); font-size:1.05rem;">
                                🔖 Phiếu: <span style="color:var(--primary); font-family:monospace;">${r.ma_phieu}</span>
                            </h4>
                            <div style="font-size:0.85rem; color:var(--text-muted);">
                                Khách hàng: <strong>${khTen}</strong> | Thiết bị: <strong>${may}</strong> (IMEI: ${imeiMasked})
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <span class="badge badge-primary">${REPAIR_STAGES[activeIdx]?.label || r.trang_thai}</span>
                            <div style="font-size:0.88rem; font-weight:700; color:var(--success); margin-top:4px;">${costFormatted}</div>
                        </div>
                    </div>

                    <!-- Visual Timeline -->
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin:16px 0 18px; overflow-x:auto; padding-bottom:8px;">
                        ${stepsHtml}
                    </div>

                    <div style="background:var(--bg-hover); padding:12px; border-radius:var(--radius-sm); font-size:0.88rem; margin-bottom:12px;">
                        <div><strong>Mô tả lỗi khách báo:</strong> ${r.mo_ta_loi_ban_dau || 'Chưa cập nhật'}</div>
                        ${r.ai_tom_tat_loi ? `<div style="margin-top:6px; color:var(--primary)"><strong>Chẩn đoán kỹ thuật:</strong> ${r.ai_tom_tat_loi}</div>` : ''}
                    </div>

                    <div style="display:flex; justify-content:flex-end; gap:10px;">
                        <button class="btn btn-outline btn-sm" onclick="printRepairReceipt(${r.id})">
                            🖨️ In Phiếu Tiếp Nhận
                        </button>
                    </div>
                </div>
            `;
        });

        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = `<div style="color:var(--danger); padding:20px; text-align:center;">Lỗi truy vấn: ${e.message}</div>`;
    }
}

// In Phiếu Tiếp Nhận (Receipt)
async function printRepairReceipt(ticketId) {
    let ticket = allRepairsData.find(x => x.id === ticketId);
    if (!ticket) {
        try {
            const token = localStorage.getItem('token');
            const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
            const res = await fetch(`/api/repairs/${ticketId}`, { headers });
            if (res.ok) ticket = await res.json();
        } catch (e) {}
    }
    if (!ticket) {
        alert('Không tìm thấy thông tin phiếu sửa chữa!');
        return;
    }

    const titleEl = document.getElementById('print-modal-title');
    if (titleEl) titleEl.innerText = `🖨️ Bản In Phiếu Tiếp Nhận (${ticket.ma_phieu})`;

    const contentEl = document.getElementById('printable-receipt-content');
    if (!contentEl) return;

    const kh = ticket.khach_hang || {};
    const tb = ticket.thiet_bi || {};
    const nowStr = new Date().toLocaleString('vi-VN');

    contentEl.innerHTML = `
        <div style="text-align:center; border-bottom:2px dashed #333; padding-bottom:12px; margin-bottom:16px;">
            <h2 style="margin:0 0 4px; font-size:1.4rem; color:#000;">TRUNG TÂM SỬA CHỮA ĐIỆN THOẠI PHONECARE AI</h2>
            <p style="margin:0; font-size:0.85rem; color:#444;">Đ/c: Số 123 Đường Công Nghệ, Quận Cầu Giấy, Hà Nội | Hotline: 1900.6868</p>
            <h3 style="margin:12px 0 4px; font-size:1.2rem; text-transform:uppercase; color:#0284c7;">PHIẾU TIẾP NHẬN SỬA CHỮA THIẾT BỊ</h3>
            <div style="font-family:monospace; font-size:1.1rem; font-weight:bold; letter-spacing:1px;">MÃ PHIẾU: ${ticket.ma_phieu}</div>
            <div style="font-size:0.8rem; color:#666;">Thời gian in: ${nowStr}</div>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-bottom:16px; font-size:0.9rem;">
            <div>
                <h4 style="margin:0 0 6px; border-bottom:1px solid #ddd; padding-bottom:2px;">THÔNG TIN KHÁCH HÀNG:</h4>
                <div>Họ và tên: <strong>${kh.ho_ten || 'Khách vãng lai'}</strong></div>
                <div>Số điện thoại: <strong>${kh.so_dien_thoai || 'N/A'}</strong></div>
                <div>Địa chỉ: ${kh.dia_chi || 'N/A'}</div>
            </div>
            <div>
                <h4 style="margin:0 0 6px; border-bottom:1px solid #ddd; padding-bottom:2px;">THÔNG TIN THIẾT BỊ:</h4>
                <div>Dòng máy: <strong>${tb.hang_san_xuat || ''} ${tb.model_may || ''}</strong></div>
                <div>Số IMEI / Serial: <strong style="font-family:monospace;">${tb.so_imei || 'N/A'}</strong></div>
                <div>Mật khẩu máy: ${tb.mat_khau_man_hinh || 'Không có'}</div>
            </div>
        </div>

        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:12px; margin-bottom:16px; font-size:0.88rem;">
            <div><strong>Tình trạng tiếp nhận / Lỗi khách báo:</strong> ${ticket.mo_ta_loi_ban_dau || 'Kiểm tra tổng thể'}</div>
            ${ticket.ai_tom_tat_loi ? `<div style="margin-top:6px;"><strong>Chẩn đoán sơ bộ:</strong> ${ticket.ai_tom_tat_loi}</div>` : ''}
            <div style="margin-top:6px;"><strong>Chi phí ước tính:</strong> <span style="font-size:1rem; font-weight:bold; color:#059669;">${Number(ticket.chi_phi_uoc_tinh || 0).toLocaleString('vi-VN')} đ</span></div>
        </div>

        <div style="font-size:0.8rem; color:#555; margin-bottom:20px; border-left:3px solid #0284c7; padding-left:8px;">
            * Quý khách vui lòng giữ phiếu này để đối chiếu khi nhận lại máy hoặc tra cứu trực tuyến tại website trung tâm.<br>
            * Trung tâm không chịu trách nhiệm về dữ liệu cá nhân của khách hàng trên thiết bị.
        </div>

        <div style="display:flex; justify-content:space-between; text-align:center; font-size:0.9rem; margin-top:24px;">
            <div style="width:40%;">
                <strong>KHÁCH HÀNG</strong><br>
                <span style="font-size:0.75rem; color:#777;">(Ký và ghi rõ họ tên)</span>
                <div style="height:60px;"></div>
                <div>${kh.ho_ten || ''}</div>
            </div>
            <div style="width:40%;">
                <strong>NGƯỜI TIẾP NHẬN</strong><br>
                <span style="font-size:0.75rem; color:#777;">(Ký và ghi rõ họ tên)</span>
                <div style="height:60px;"></div>
                <div>Lễ tân tiếp nhận</div>
            </div>
        </div>
    `;

    const modal = document.getElementById('modal-print-view');
    if (modal) {
        modal.style.display = 'flex';
        modal.classList.add('active');
    }
}

// In Hóa Đơn (Invoice)
async function printInvoice(invoiceId) {
    let inv = null;
    try {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const res = await fetch('/api/invoices', { headers });
        if (res.ok) {
            const list = await res.json();
            inv = list.find(x => x.id === invoiceId);
        }
    } catch (e) {}

    if (!inv) {
        alert('Không tìm thấy thông tin hóa đơn!');
        return;
    }

    const titleEl = document.getElementById('print-modal-title');
    if (titleEl) titleEl.innerText = `🖨️ Bản In Hóa Đơn Thanh Toán (${inv.ma_hoa_don})`;

    const contentEl = document.getElementById('printable-receipt-content');
    if (!contentEl) return;

    const nowStr = new Date().toLocaleString('vi-VN');

    contentEl.innerHTML = `
        <div style="text-align:center; border-bottom:2px dashed #333; padding-bottom:12px; margin-bottom:16px;">
            <h2 style="margin:0 0 4px; font-size:1.4rem; color:#000;">TRUNG TÂM SỬA CHỮA ĐIỆN THOẠI PHONECARE AI</h2>
            <p style="margin:0; font-size:0.85rem; color:#444;">Đ/c: Số 123 Đường Công Nghệ, Quận Cầu Giấy, Hà Nội | Hotline: 1900.6868</p>
            <h3 style="margin:12px 0 4px; font-size:1.2rem; text-transform:uppercase; color:#059669;">HÓA ĐƠN THANH TOÁN DỊCH VỤ</h3>
            <div style="font-family:monospace; font-size:1.1rem; font-weight:bold;">SỐ HĐ: ${inv.ma_hoa_don}</div>
            <div style="font-size:0.8rem; color:#666;">Thời gian thanh toán: ${inv.ngay_thanh_toan || nowStr}</div>
        </div>

        <div style="margin-bottom:14px; font-size:0.9rem;">
            <div>Khách hàng: <strong>${inv.ten_khach_hang || 'Khách vãng lai'}</strong> - SĐT: <strong>${inv.so_dien_thoai || 'N/A'}</strong></div>
            <div>Mã phiếu sửa chữa: <strong style="font-family:monospace;">${inv.ma_phieu || 'N/A'}</strong></div>
            <div>Thiết bị: <strong>${inv.model_may || 'N/A'}</strong></div>
            <div>Hình thức thanh toán: <strong>${inv.phuong_thuc}</strong> | Trạng thái: <strong style="color:#059669;">ĐÃ THANH TOÁN</strong></div>
        </div>

        <div style="border-top:1px solid #333; border-bottom:1px solid #333; padding:12px 0; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:1.1rem; font-weight:bold;">TỔNG TIỀN THANH TOÁN:</span>
            <span style="font-size:1.3rem; font-weight:bold; color:#059669;">${Number(inv.tong_tien || 0).toLocaleString('vi-VN')} VNĐ</span>
        </div>

        <div style="font-size:0.82rem; color:#555; margin-bottom:24px;">
            * Linh kiện thay thế được bảo hành điện tử chính hãng theo chính sách tại website.<br>
            * Cảm ơn Quý khách đã tin tưởng sử dụng dịch vụ tại PhoneCare AI!
        </div>

        <div style="display:flex; justify-content:space-between; text-align:center; font-size:0.9rem;">
            <div style="width:40%;">
                <strong>KHÁCH HÀNG</strong><br>
                <div style="height:50px;"></div>
                <div>${inv.ten_khach_hang || ''}</div>
            </div>
            <div style="width:40%;">
                <strong>THU NGÂN</strong><br>
                <div style="height:50px;"></div>
                <div>Bộ phận kế toán</div>
            </div>
        </div>
    `;

    const modal = document.getElementById('modal-print-view');
    if (modal) {
        modal.style.display = 'flex';
        modal.classList.add('active');
    }
}

function closePrintModal() {
    const modal = document.getElementById('modal-print-view');
    if (modal) {
        modal.style.display = 'none';
        modal.classList.remove('active');
    }
}

function executePrintDocument() {
    const printableContent = document.getElementById('printable-receipt-content');
    if (!printableContent) return;

    const printWin = window.open('', '_blank', 'width=800,height=600');
    if (!printWin) {
        alert('Vui lòng cho phép popup trình duyệt để mở hộp thoại in!');
        return;
    }

    printWin.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>In Chứng Từ - PhoneCare AI</title>
            <style>
                body { font-family: 'Plus Jakarta Sans', Arial, sans-serif; padding: 20px; color: #111; }
                @media print {
                    @page { margin: 10mm; }
                    body { padding: 0; }
                }
            </style>
        </head>
        <body>
            ${printableContent.innerHTML}
            <script>
                window.onload = function() {
                    window.print();
                    setTimeout(function() { window.close(); }, 500);
                };
            <\/script>
        </body>
        </html>
    `);
    printWin.document.close();
}

// Xuất CSV danh sách phiếu sửa chữa (FR-09)
function exportRepairsToCSV() {
    if (!allRepairsData || allRepairsData.length === 0) {
        alert('Không có dữ liệu phiếu sửa chữa để xuất!');
        return;
    }

    let csvContent = "\uFEFF"; // Byte Order Mark (BOM) để Microsoft Excel hiển thị đúng tiếng Việt
    csvContent += "Mã Phiếu,Khách Hàng,Số Điện Thoại,Model Máy,Số IMEI,Trạng Thái,Chi Phí Ước Tính,Ngày Tiếp Nhận\n";

    allRepairsData.forEach(r => {
        const kh = r.khach_hang ? `"${r.khach_hang.ho_ten.replace(/"/g, '""')}"` : '""';
        const sdt = r.khach_hang ? `"${r.khach_hang.so_dien_thoai}"` : '""';
        const model = r.thiet_bi ? `"${r.thiet_bi.hang_san_xuat} ${r.thiet_bi.model_may}"` : '""';
        const imei = r.thiet_bi ? `"${r.thiet_bi.so_imei}"` : '""';
        const cost = r.chi_phi_uoc_tinh || 0;
        const date = r.ngay_tiep_nhan || '';

        csvContent += `"${r.ma_phieu}",${kh},${sdt},${model},${imei},"${r.trang_thai}",${cost},"${date}"\n`;
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    const dateStr = new Date().toISOString().slice(0, 10);
    link.setAttribute('href', url);
    link.setAttribute('download', `danh_sach_phieu_sua_chua_${dateStr}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
