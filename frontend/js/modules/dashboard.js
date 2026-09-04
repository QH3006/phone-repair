/**
 * Module Dashboard - Thống kê KPI & Báo cáo tổng quan
 */

async function loadDashboardData() {
    try {
        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        
        const res = await fetch('/api/stats/overview', { headers });
        if (!res.ok) return;
        const data = await res.json();
        
        const s = data.summary || {};
        
        // Update KPI counters
        document.getElementById('kpi-total-repairs').innerText = s.total_repairs ?? 0;
        document.getElementById('kpi-active-repairs').innerText = `Đang xử lý: ${s.active_repairs ?? 0}`;
        document.getElementById('kpi-completed-repairs').innerText = s.completed_repairs ?? 0;
        document.getElementById('kpi-total-revenue').innerText = `${Number(s.total_revenue || 0).toLocaleString('vi-VN')} đ`;
        document.getElementById('kpi-total-customers').innerText = s.total_customers ?? 0;
        document.getElementById('kpi-total-parts').innerText = s.total_parts ?? 0;
        document.getElementById('kpi-low-stock').innerText = `Cảnh báo tồn ít: ${s.low_stock_parts ?? 0}`;
        document.getElementById('kpi-total-ai-logs').innerText = s.total_ai_logs ?? 0;

        // Render 8 lifecycle bars
        const dist = data.status_distribution || {};
        const labels = {
            "TiepNhan": "1. Tiếp Nhận",
            "PhanCongKTV": "2. Phân Công KTV",
            "DangKiemTra": "3. Đang Kiểm Tra",
            "BaoGia_ChoDuyet": "4. Báo Giá Chờ Duyệt",
            "DangSuaChua": "5. Đang Sửa Chữa",
            "DaSuaXong": "6. Đã Sửa Xong",
            "DaThanhToan": "7. Đã Thanh Toán",
            "HoanTat_TraMay": "8. Hoàn Tất Trả Máy"
        };
        const total = Math.max(s.total_repairs || 1, 1);
        let barsHtml = '';
        for (const [st, count] of Object.entries(dist)) {
            const pct = Math.round((count / total) * 100);
            barsHtml += `
                <div style="margin-bottom: 12px;">
                    <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:4px;">
                        <span><strong>${labels[st] || st}</strong></span>
                        <span class="badge badge-info">${count} phiếu (${pct}%)</span>
                    </div>
                    <div style="background:var(--bg-input); height:8px; border-radius:4px; overflow:hidden;">
                        <div style="background:linear-gradient(90deg, #3b82f6, #10b981); width:${Math.max(pct, count > 0 ? 5 : 0)}%; height:100%; border-radius:4px; transition:width 0.5s ease;"></div>
                    </div>
                </div>
            `;
        }
        document.getElementById('lifecycle-bars-container').innerHTML = barsHtml;

        // Render Top Models
        const topModels = data.top_models || [];
        let modelsHtml = '';
        if (topModels.length === 0) {
            modelsHtml = '<li style="color:var(--text-muted); font-size:0.85rem;">Chưa có dữ liệu thống kê thiết bị</li>';
        } else {
            topModels.forEach((item, idx) => {
                modelsHtml += `
                    <li style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid var(--border-color); font-size:0.85rem;">
                        <span><strong>#${idx + 1}. ${item.model}</strong></span>
                        <span class="badge badge-success">${item.count} máy</span>
                    </li>
                `;
            });
        }
        document.getElementById('top-devices-list').innerHTML = modelsHtml;

        // Render Low Stock Alert
        const lowStock = data.low_stock_items || [];
        let lowHtml = '';
        if (lowStock.length === 0) {
            lowHtml = '<p style="color:var(--text-muted); font-size:0.85rem;">✅ Kho linh kiện an toàn, không có mặt hàng thiếu hụt.</p>';
        } else {
            lowStock.forEach(p => {
                lowHtml += `
                    <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(239, 68, 68, 0.1); border:1px solid #ef4444; border-radius:6px; padding:6px 12px; margin-bottom:6px; font-size:0.85rem;">
                        <span>${p.ten}</span>
                        <strong style="color:#ef4444;">Tồn: ${p.ton_kho}</strong>
                    </div>
                `;
            });
        }
        document.getElementById('low-stock-alert-list').innerHTML = lowHtml;

    } catch (e) {
        console.error('Lỗi nạp Dashboard:', e);
    }
}
