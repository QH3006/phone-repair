/**
 * Module AI Sandbox (Interactive AI Demos: Fault Summary, Message Generation, Service Explanation)
 */

let currentFaultAIResult = null;
let currentSelectedTicketId = 1;

function fillFaultSample() {
    const val = document.getElementById('select-sample-fault').value;
    currentSelectedTicketId = parseInt(val);
    if (val === '1') {
        document.getElementById('ai-fault-model').value = 'iPhone 13 Pro Max';
        document.getElementById('ai-fault-desc').value = 'Máy sập nguồn khi cắm sạc, pin tụt nhanh và máy nóng ran.';
        document.getElementById('ai-fault-notes').value = 'Máy ngấm ẩm, chập đường VDD_MAIN do tụ C2301 rỉ sét. IC sạc USB U3300 nóng bất thường. Pin phù nhẹ 78% dung lượng.';
    } else if (val === '2') {
        document.getElementById('ai-fault-model').value = 'Galaxy S22 Ultra';
        document.getElementById('ai-fault-desc').value = 'Màn hình bị sọc xanh dọc thân máy sau khi va chạm góc bàn.';
        document.getElementById('ai-fault-notes').value = 'Tấm nền Dynamic AMOLED bị nứt cổ cáp hiển thị, cảm ứng góc phải liệt cục bộ. Cần thay nguyên cụm màn hình mới.';
    } else if (val === '3') {
        document.getElementById('ai-fault-model').value = 'Redmi Note 12';
        document.getElementById('ai-fault-desc').value = 'Chân cắm sạc lỏng lẻo, phải bẻ gập dây sạc mới nhận dòng.';
        document.getElementById('ai-fault-notes').value = 'Chân socket cáp sạc Type-C bị gãy chân tiếp xúc số 3 và 5, mạch đường VBUS bị oxy hóa.';
    }
}

async function runSummarizeFault() {
    const resultBox = document.getElementById('ai-fault-result');
    const statusBadge = document.getElementById('ai-fault-status');
    const hitlBox = document.getElementById('hitl-fault-actions');

    resultBox.innerHTML = '<p class="placeholder-text">🤖 Đang gửi request tới AI Orchestrator Service...</p>';
    statusBadge.innerText = 'Đang Xử Lý';
    statusBadge.className = 'badge badge-warning';

    const payload = {
        phieu_id: currentSelectedTicketId,
        model_may: document.getElementById('ai-fault-model').value,
        mo_ta_loi_khach: document.getElementById('ai-fault-desc').value,
        ghi_chu_ky_thuat: document.getElementById('ai-fault-notes').value
    };

    try {
        const res = await fetch(`${API_BASE}/ai/summarize-fault`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        currentFaultAIResult = data.data;

        statusBadge.innerText = `Hoàn Tất (${data.status})`;
        statusBadge.className = data.status === 'ThanhCong' ? 'badge badge-success' : 'badge badge-warning';

        const d = data.data || {};
        const riskColors = {
            'Cao': 'badge-danger',
            'TrungBinh': 'badge-warning',
            'Thap': 'badge-success'
        };
        const riskBadge = `<span class="badge ${riskColors[d.risk_level] || 'badge-info'}">Rủi ro: ${d.risk_level || 'N/A'}</span>`;
        const comps = Array.isArray(d.faulty_components) ? d.faulty_components.map(c => `<span class="badge badge-primary" style="margin:2px 4px 2px 0;">${c}</span>`).join('') : (d.faulty_components || 'N/A');

        resultBox.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
                <div>
                    <span class="badge ${data.is_fallback ? 'badge-warning' : 'badge-primary'}">
                        ${data.is_fallback ? '🛡️ Fallback Rule Engine' : '⚡ Gemini AI Cloud'}
                    </span>
                    <small style="color:var(--text-muted); margin-left:8px;">Độ trễ: ${data.execution_time_ms}ms</small>
                </div>
                <div>${riskBadge}</div>
            </div>

            <div class="ai-summary-card">
                <div class="ai-summary-row">
                    <div class="ai-summary-label">🔍 Hiện Tượng Phần Cứng</div>
                    <div class="ai-summary-value"><strong>${d.hardware_issue || 'N/A'}</strong></div>
                </div>
                <div class="ai-summary-row">
                    <div class="ai-summary-label">⚠️ Linh Kiện Nghi Vấn Hỏng</div>
                    <div class="ai-summary-value">${comps}</div>
                </div>
                <div class="ai-summary-row">
                    <div class="ai-summary-label">🔧 Đề Xuất Xử Lý</div>
                    <div class="ai-summary-value" style="color:var(--primary); font-weight:600;">${d.recommended_action || 'N/A'}</div>
                </div>
            </div>

            <details open style="margin-top: 8px;">
                <summary style="cursor:pointer; font-size:0.8rem; color:var(--text-muted); font-weight:600; margin-bottom:6px;">
                    📋 Khối JSON Chuẩn Hóa (Pydantic Schema)
                </summary>
                <pre class="json-view">${JSON.stringify(d, null, 2)}</pre>
            </details>
        `;

        if (hitlBox) hitlBox.style.display = 'block';

    } catch (e) {
        statusBadge.innerText = 'Thất Bại';
        statusBadge.className = 'badge badge-danger';
        resultBox.innerHTML = `<p style="color:var(--danger)">Lỗi: ${e.message}</p>`;
    }
}

async function approveFaultSummary() {
    if (!currentFaultAIResult) return;

    try {
        const res = await fetch(`${API_BASE}/ai/approve-data`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                phieu_id: currentSelectedTicketId,
                ai_tom_tat_loi: JSON.stringify(currentFaultAIResult),
                trang_thai_moi: 'DangSuaChua'
            })
        });
        const data = await res.json();
        alert(data.message || 'Đã duyệt và lưu vào CSDL!');
        loadRepairs();
    } catch (e) {
        alert('Lỗi phê duyệt: ' + e.message);
    }
}

async function runGenerateMessage() {
    const resultBox = document.getElementById('ai-msg-result');
    const badge = document.getElementById('ai-msg-badge');
    const meta = document.getElementById('msg-meta');

    resultBox.innerHTML = '<p class="placeholder-text">🤖 Đang soạn thảo tin nhắn chăm sóc khách hàng...</p>';
    badge.innerText = 'Đang Tạo';
    badge.className = 'badge badge-warning';

    const payload = {
        ten_khach: document.getElementById('ai-msg-name').value,
        model_may: document.getElementById('ai-msg-model').value,
        trang_thai: document.getElementById('ai-msg-status').value,
        chi_phi: parseFloat(document.getElementById('ai-msg-cost').value) || 0,
        kenh_gui: document.getElementById('ai-msg-channel').value,
        ngay_hen: document.getElementById('ai-msg-time').value
    };

    try {
        const res = await fetch(`${API_BASE}/ai/generate-progress-message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        const msg = data.data.message;

        badge.innerText = data.status;
        badge.className = 'badge badge-success';

        resultBox.innerHTML = `
            <div style="background: rgba(56, 189, 248, 0.08); border-left: 3px solid var(--primary); padding: 14px; border-radius: var(--radius-sm); color: var(--text-main); line-height: 1.6;">
                ${msg}
            </div>
        `;

        if (meta) {
            meta.style.display = 'flex';
            document.getElementById('char-count').innerText = `Độ dài: ${msg.length} ký tự (Chuẩn SMS: ${msg.length <= 160 ? 'Đạt' : 'Vượt quá 160 ký tự'})`;
        }
    } catch (e) {
        badge.innerText = 'Lỗi';
        badge.className = 'badge badge-danger';
        resultBox.innerHTML = `<p style="color:var(--danger)">Lỗi: ${e.message}</p>`;
    }
}

function copyMessage() {
    const text = document.getElementById('ai-msg-result').innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert('Đã sao chép nội dung tin nhắn!');
    });
}

async function runExplainService() {
    const resultBox = document.getElementById('ai-exp-result');
    resultBox.innerHTML = '<p class="placeholder-text">🤖 Đang chuyển hóa thuật ngữ chuyên ngành sang ngôn ngữ đời thường...</p>';

    const payload = {
        ten_dich_vu: document.getElementById('ai-exp-service').value,
        ten_linh_kien: document.getElementById('ai-exp-part').value,
        loi_thuc_te: document.getElementById('ai-exp-fault').value
    };

    try {
        const res = await fetch(`${API_BASE}/ai/explain-service`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        const exp = (data.data && (data.data.explanation || data.data.message)) || data.raw_response || "Không có nội dung phản hồi.";
        const isAI = data.status === 'ThanhCong';

        resultBox.innerHTML = `
            <div style="background: rgba(192, 132, 252, 0.08); border-left: 3px solid var(--purple); padding: 16px; border-radius: var(--radius-sm);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <h5 style="color:var(--purple); margin:0;">💡 Giải thích minh bạch dành cho khách hàng:</h5>
                    <span class="badge ${isAI ? 'badge-success' : 'badge-warning'}">${isAI ? 'Gemini AI Cloud' : 'Phòng thủ Fallback'} (${data.execution_time_ms || 0}ms)</span>
                </div>
                <p id="ai-exp-text" style="font-size:0.95rem; color:var(--text-main); line-height:1.7; margin-bottom:12px;">${exp}</p>
                <button class="btn btn-outline btn-sm" onclick="copyExplanation()">📋 Sao chép lời tư vấn</button>
            </div>
        `;
    } catch (e) {
        resultBox.innerHTML = `<p style="color:var(--danger)">Lỗi: ${e.message}</p>`;
    }
}

function copyExplanation() {
    const textEl = document.getElementById('ai-exp-text');
    if (textEl) {
        navigator.clipboard.writeText(textEl.innerText).then(() => {
            alert('Đã sao chép lời tư vấn cho khách hàng!');
        });
    }
}
