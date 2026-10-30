/**
 * PhoneCare AI - Customer Tracking Portal Logic
 */

const STAGES = [
    { key: 'TiepNhan', label: '1. Tiếp Nhận', icon: '📥' },
    { key: 'PhanCongKTV', label: '2. Phân Công', icon: '👨‍🔧' },
    { key: 'DangKiemTra', label: '3. Kiểm Tra', icon: '🔍' },
    { key: 'BaoGia_ChoDuyet', label: '4. Báo Giá', icon: '💬' },
    { key: 'DangSuaChua', label: '5. Sửa Chữa', icon: '⚙️' },
    { key: 'DaSuaXong', label: '6. Đã Sửa', icon: '✅' },
    { key: 'DaThanhToan', label: '7. Thanh Toán', icon: '💳' },
    { key: 'HoanTat_TraMay', label: '8. Hoàn Tất', icon: '🎉' }
];

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('phonecare_theme', next);
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        themeIcon.innerText = next === 'dark' ? '🌙' : '☀️';
    }
}

function quickFill(val) {
    const input = document.getElementById('portal-query-input');
    if (input) {
        input.value = val;
        executeCustomerSearch();
    }
}

async function executeCustomerSearch() {
    const input = document.getElementById('portal-query-input');
    const container = document.getElementById('portal-results');
    if (!input || !container) return;

    const q = input.value.trim();
    if (!q) {
        alert('Vui lòng nhập Mã phiếu, Số điện thoại hoặc IMEI để tra cứu!');
        return;
    }

    container.innerHTML = '<div style="text-align:center; padding:40px; color:var(--primary);"><div class="spinner"></div> Đang kiểm tra hệ thống cơ sở dữ liệu...</div>';

    try {
        const res = await fetch(`/api/repairs/lookup?q=${encodeURIComponent(q)}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const list = await res.json();
        if (!list || list.length === 0) {
            container.innerHTML = `
                <div class="card" style="text-align:center; padding:40px; border-left:4px solid var(--danger);">
                    <div style="font-size:2.5rem; margin-bottom:12px;">⚠️</div>
                    <h3 style="margin:0 0 8px; color:var(--danger)">Không tìm thấy thông tin sửa chữa</h3>
                    <p style="color:var(--text-muted); margin:0;">Không có hồ sơ nào khớp với từ khóa "<strong>${q}</strong>". Quý khách vui lòng kiểm tra lại mã phiếu ghi trên biên nhận hoặc liên hệ tổng đài <strong>1900.6868</strong> để được hỗ trợ trực tiếp.</p>
                </div>
            `;
            return;
        }

        let html = '';
        list.forEach(r => {
            const stageIdx = STAGES.findIndex(s => s.key === r.trang_thai);
            const activeIdx = stageIdx >= 0 ? stageIdx : 0;

            let stepsHtml = '';
            STAGES.forEach((stage, idx) => {
                const isPassed = idx < activeIdx;
                const isCurrent = idx === activeIdx;
                const color = isCurrent ? 'var(--primary)' : (isPassed ? 'var(--success)' : 'var(--text-muted)');
                const bg = isCurrent ? 'rgba(56, 189, 248, 0.15)' : (isPassed ? 'rgba(34, 197, 94, 0.15)' : 'var(--bg-hover)');
                const border = isCurrent ? '2px solid var(--primary)' : (isPassed ? '2px solid var(--success)' : '1px solid var(--border-color)');

                stepsHtml += `
                    <div class="timeline-step">
                        <div class="timeline-circle" style="background:${bg}; border:${border};">
                            ${stage.icon}
                        </div>
                        <div style="font-size:0.75rem; font-weight:${isCurrent ? '800' : '600'}; color:${color};">
                            ${stage.label}
                        </div>
                    </div>
                `;
            });

            const khName = r.khach_hang ? r.khach_hang.ho_ten : 'Khách hàng';
            const devName = r.thiet_bi ? `${r.thiet_bi.hang_san_xuat} ${r.thiet_bi.model_may}` : 'Thiết bị';
            const imeiMask = r.thiet_bi && r.thiet_bi.so_imei ? r.thiet_bi.so_imei.slice(0, 4) + '******' + r.thiet_bi.so_imei.slice(-4) : 'N/A';
            const costStr = Number(r.tong_tien_du_kien || r.chi_phi_uoc_tinh || 0).toLocaleString('vi-VN') + ' VNĐ';
            const errorDesc = r.mo_ta_loi_khach || r.mo_ta_loi_ban_dau || 'Kiểm tra máy tổng quát';

            // Xác định mức độ cam kết thời gian (SLA)
            let slaBadge = '';
            if (errorDesc.includes('lấy ngay') || errorDesc.includes('30 phút') || errorDesc.includes('45 phút')) {
                slaBadge = '<span class="badge" style="background:#fef3c7; color:#b45309; border:1px solid #fde68a; font-size:0.75rem; padding:3px 8px; margin-left:6px;">⚡ Sửa lấy ngay 30-45p</span>';
            } else if (errorDesc.includes('trong ngày') || errorDesc.includes('tiếng')) {
                slaBadge = '<span class="badge" style="background:#e0f2fe; color:#0369a1; border:1px solid #bae6fd; font-size:0.75rem; padding:3px 8px; margin-left:6px;">📅 Hẹn trả trong ngày</span>';
            } else if (errorDesc.includes('chuyên sâu') || errorDesc.includes('24h') || errorDesc.includes('48h')) {
                slaBadge = '<span class="badge" style="background:#f3e8ff; color:#7e22ce; border:1px solid #e9d5ff; font-size:0.75rem; padding:3px 8px; margin-left:6px;">🛠️ Kỹ thuật chuyên sâu</span>';
            }

            html += `
                <div class="card card-ticket-detail" style="margin-bottom:24px; padding:24px; box-shadow:var(--shadow-lg);">
                    <div class="ticket-card-header" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; border-bottom:1px solid var(--border-color); padding-bottom:14px;">
                        <div>
                            <div style="font-size:0.82rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px;">Mã Tiếp Nhận</div>
                            <h2 style="margin:2px 0 0; color:var(--primary); font-family:monospace; font-size:1.5rem;">${r.ma_phieu}</h2>
                        </div>
                        <div class="ticket-price-box" style="text-align:right;">
                            <span class="badge badge-primary" style="font-size:0.9rem; padding:5px 12px;">${STAGES[activeIdx]?.label || r.trang_thai}</span>
                            <div style="margin-top:4px; font-weight:800; font-size:1.2rem; color:var(--success);">${costStr}</div>
                        </div>
                    </div>

                    <!-- Mobile Quick Stepper Progress Bar -->
                    <div class="mobile-progress-badge">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span style="font-size:0.8rem; font-weight:700; color:var(--primary);">Tiến độ: Bước ${activeIdx + 1}/8</span>
                            <span style="font-size:0.82rem; font-weight:800; color:var(--text-main);">${STAGES[activeIdx]?.icon} ${STAGES[activeIdx]?.label}</span>
                        </div>
                        <div style="width:100%; height:6px; background:rgba(148,163,184,0.2); border-radius:9999px; overflow:hidden;">
                            <div style="width:${Math.round(((activeIdx + 1) / 8) * 100)}%; height:100%; background:linear-gradient(90deg, var(--primary), var(--purple)); border-radius:9999px;"></div>
                        </div>
                    </div>

                    <div class="timeline-scroll">
                        ${stepsHtml}
                    </div>

                    <div class="info-grid-box" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:14px; margin:18px 0; background:var(--bg-hover); padding:16px; border-radius:var(--radius-md);">
                        <div>
                            <div style="color:var(--text-muted); font-size:0.82rem;">👤 Khách hàng:</div>
                            <strong style="font-size:1rem;">${khName}</strong>
                        </div>
                        <div>
                            <div style="color:var(--text-muted); font-size:0.82rem;">📱 Thiết bị:</div>
                            <strong style="font-size:1rem;">${devName}</strong>
                            <div style="font-size:0.78rem; color:var(--text-muted); font-family:monospace;">IMEI: ${imeiMask}</div>
                        </div>
                        <div>
                            <div style="color:var(--text-muted); font-size:0.82rem;">⏱️ Giờ tiếp nhận:</div>
                            <strong style="font-size:0.92rem;">${r.ngay_tiep_nhan || 'Hôm nay'}</strong>
                        </div>
                        <div>
                            <div style="color:var(--text-muted); font-size:0.82rem;">⏰ Cam kết hẹn trả:</div>
                            <strong style="font-size:0.95rem; color:var(--primary);">${r.ngay_hen_tra || 'Chờ cập nhật'}</strong>
                            ${slaBadge}
                        </div>
                    </div>

                    <div style="background:rgba(56, 189, 248, 0.08); border-left:4px solid var(--primary); padding:14px; border-radius:var(--radius-sm); margin-bottom:14px;">
                        <div style="font-weight:700; color:var(--primary); margin-bottom:4px; font-size:0.9rem;">📋 Mô tả lỗi khi tiếp nhận & Cam kết:</div>
                        <div style="line-height:1.55; font-size:0.92rem;">${errorDesc}</div>
                    </div>

                    ${r.ai_tom_tat_loi ? `
                        <div style="background:rgba(192, 132, 252, 0.08); border-left:4px solid var(--purple); padding:14px; border-radius:var(--radius-sm); margin-bottom:16px;">
                            <div style="font-weight:700; color:var(--purple); margin-bottom:4px; font-size:0.9rem;">💡 Chẩn đoán kỹ thuật từ chuyên viên:</div>
                            <div style="line-height:1.55; font-size:0.92rem;">${r.ai_tom_tat_loi}</div>
                        </div>
                    ` : ''}

                    <div class="no-print ticket-footer-actions" style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--border-color); padding-top:14px;">
                        <span style="font-size:0.82rem; color:var(--text-muted);">Cần giải đáp thắc mắc? Gọi ngay <a href="tel:19006868" style="color:var(--primary); font-weight:700;">1900.6868</a></span>
                        <button class="btn btn-outline btn-sm" onclick="window.print()">🖨️ In / Lưu PDF Phiếu Này</button>
                    </div>
                </div>
            `;
        });

        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = `<div class="card" style="color:var(--danger); padding:20px; text-align:center;">Lỗi kết nối máy chủ: ${e.message}</div>`;
    }
}

// Tự động load nếu có query string hoặc mặc định
window.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const q = urlParams.get('q') || 'PSC-20260917-001';
    const input = document.getElementById('portal-query-input');
    if (input) {
        input.value = q;
        executeCustomerSearch();
    }
});
