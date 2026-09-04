/**
 * Module AI Logs (Real-time Audit Trail)
 */

async function loadAILogs() {
    const tbody = document.getElementById('ai-logs-table-body');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;">Đang tải nhật ký AI...</td></tr>';
    
    try {
        const res = await fetch(`${API_BASE}/ai/logs`);
        const logs = await res.json();
        tbody.innerHTML = '';
        
        if (logs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:16px;">Chưa có lượt tương tác AI nào. Hãy sang Tab 2 để thử nghiệm!</td></tr>';
            return;
        }

        logs.forEach(l => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>#${l.id}</strong></td>
                <td><span class="badge badge-info">${l.loai_tac_vu}</span></td>
                <td>${l.model}</td>
                <td><strong>${l.exec_time_ms} ms</strong></td>
                <td><span class="badge ${l.trang_thai === 'ThanhCong' ? 'badge-success' : 'badge-warning'}">${l.trang_thai}</span></td>
                <td>${new Date(l.ngay_thuc_hien).toLocaleTimeString()}</td>
                <td><code style="font-size:0.75rem; color:var(--text-muted);">${l.parsed_json.substring(0, 80)}...</code></td>
            `;
            tbody.appendChild(row);
        });
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:var(--danger)">Lỗi tải nhật ký: ${e.message}</td></tr>`;
    }
}
