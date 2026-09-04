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

        resultBox.innerHTML = `
            <div style="margin-bottom: 8px;">
                <span class="badge ${data.is_fallback ? 'badge-warning' : 'badge-primary'}">
                    ${data.is_fallback ? '🛡️ Fallback Rule Engine' : '⚡ Gemini AI Cloud'}
                </span>
                <small style="color:var(--text-muted); margin-left:8px;">Độ trễ: ${data.execution_time_ms}ms</small>
            </div>
            <pre class="json-view">${JSON.stringify(data.data, null, 2)}</pre>
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
        const exp = data.data.explanation;

        resultBox.innerHTML = `
            <div style="background: rgba(192, 132, 252, 0.08); border-left: 3px solid var(--purple); padding: 16px; border-radius: var(--radius-sm);">
                <h5 style="color:var(--purple); margin-bottom:8px;">💡 Giải thích minh bạch dành cho khách hàng:</h5>
                <p style="font-size:0.92rem; color:var(--text-main); line-height:1.7;">${exp}</p>
            </div>
        `;
    } catch (e) {
        resultBox.innerHTML = `<p style="color:var(--danger)">Lỗi: ${e.message}</p>`;
    }
}
