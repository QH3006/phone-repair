/**
 * Module RAG Knowledge Service (Retrieval-Augmented Generation Pipeline)
 * Hệ thống tra cứu tri thức chuyên sâu và phản hồi ngữ cảnh thực tế của PhoneCare.
 */

let lastRetrievedChunks = [];
let currentRAGDocs = [];

// Khởi tạo và nạp dữ liệu ban đầu cho phân hệ RAG
async function initRAGDemo() {
    await loadRAGDocuments();
    await loadRAGChunks();
}

// Nạp danh sách và thông số các file tài liệu tri thức (Yêu cầu 1)
async function loadRAGDocuments() {
    const listContainer = document.getElementById('rag-docs-list');
    const statFiles = document.getElementById('rag-stat-files');
    const statSize = document.getElementById('rag-stat-size');
    const statWords = document.getElementById('rag-stat-words');

    if (!listContainer) return;
    listContainer.innerHTML = '<p class="placeholder-text">⏳ Đang đọc kho tài liệu tri thức...</p>';

    try {
        const res = await fetch(`${API_BASE}/ai/rag/documents`);
        const data = await res.json();
        currentRAGDocs = data.documents || [];

        if (statFiles) statFiles.innerText = `${data.total_files} files TXT (UTF-8)`;
        if (statSize) statSize.innerText = `${data.total_size_kb} KB`;
        if (statWords) statWords.innerText = `${data.total_words.toLocaleString()} từ`;

        let html = '<div class="rag-docs-grid">';
        currentRAGDocs.forEach(doc => {
            html += `
                <div class="rag-doc-card">
                    <div class="rag-doc-header">
                        <span class="rag-doc-icon">📄</span>
                        <div class="rag-doc-title">
                            <strong>${doc.file_name}</strong>
                            <small>${doc.size_formatted} • ${doc.char_count} ký tự • ${doc.word_count} từ</small>
                        </div>
                        <span class="badge badge-success">TXT (UTF-8)</span>
                    </div>
                    <div class="rag-doc-snippet">
                        "${escapeHtml(doc.snippet)}"
                    </div>
                </div>
            `;
        });
        html += '</div>';
        listContainer.innerHTML = html;

    } catch (e) {
        listContainer.innerHTML = `<p style="color:var(--danger)">Lỗi nạp tài liệu: ${e.message}</p>`;
    }
}

// Cập nhật cấu hình và hiển thị danh sách chunks kèm metadata (Yêu cầu 2)
async function loadRAGChunks() {
    const chunkSize = parseInt(document.getElementById('rag-chunk-size').value) || 300;
    const chunkOverlap = parseInt(document.getElementById('rag-chunk-overlap').value) || 50;
    const fileType = 'TXT';

    document.getElementById('lbl-chunk-size').innerText = `${chunkSize} ký tự`;
    document.getElementById('lbl-chunk-overlap').innerText = `${chunkOverlap} ký tự`;

    const sampleContainer = document.getElementById('rag-sample-chunks');
    const statChunks = document.getElementById('rag-stat-chunks');

    if (!sampleContainer) return;
    sampleContainer.innerHTML = '<p class="placeholder-text">⏳ Đang cắt phân đoạn văn bản và tính toán metadata...</p>';

    try {
        const res = await fetch(`${API_BASE}/ai/rag/chunks?chunk_size=${chunkSize}&chunk_overlap=${chunkOverlap}&file_type_filter=${fileType}`);
        const data = await res.json();

        if (statChunks) statChunks.innerText = `${data.total_chunks} chunks`;

        let html = `
            <div class="alert alert-info" style="margin-bottom:12px; font-size:0.85rem;">
                📌 <strong>Thống kê Chunking:</strong> Cắt từ <strong>${data.total_documents_processed}</strong> tài liệu 
                thành tổng cộng <strong>${data.total_chunks}</strong> Chunks (Kích thước: ${chunkSize} ký tự, Gối đầu: ${chunkOverlap} ký tự). Dưới đây là 6 Chunks mẫu:
            </div>
            <div class="rag-chunks-grid">
        `;

        data.sample_chunks.forEach(c => {
            html += `
                <div class="rag-chunk-card">
                    <div class="rag-chunk-meta">
                        <span class="badge badge-purple">${c.chunk_id}</span>
                        <span class="badge badge-outline">${c.doc_name}</span>
                        <small style="color:var(--text-muted); margin-left:auto;">Pos: ${c.start_char}➔${c.end_char} (${c.word_count} từ)</small>
                    </div>
                    <div class="rag-chunk-body">
                        ${escapeHtml(c.content)}
                    </div>
                </div>
            `;
        });
        html += '</div>';
        sampleContainer.innerHTML = html;

    } catch (e) {
        sampleContainer.innerHTML = `<p style="color:var(--danger)">Lỗi phân tách chunk: ${e.message}</p>`;
    }
}

// Điền câu hỏi mẫu 1-click
function fillRAGSampleQuery(queryText) {
    const input = document.getElementById('rag-query-input');
    if (input) {
        input.value = queryText;
        input.focus();
    }
}

// BƯỚC 1: Truy xuất Top-K Chunks TRƯỚC KHI gọi LLM (Yêu cầu 3)
async function runRAGRetrieveOnly() {
    const query = document.getElementById('rag-query-input').value.trim();
    if (!query) {
        alert('Vui lòng nhập câu hỏi cần tra cứu tri thức!');
        return;
    }

    const topK = parseInt(document.getElementById('rag-top-k').value) || 3;
    const chunkSize = parseInt(document.getElementById('rag-chunk-size').value) || 300;
    const chunkOverlap = parseInt(document.getElementById('rag-chunk-overlap').value) || 50;
    const fileType = 'TXT';

    const retContainer = document.getElementById('rag-retrieval-result');
    const retBadge = document.getElementById('rag-retrieval-badge');
    const btnStep2 = document.getElementById('btn-rag-step2');

    retBadge.innerText = 'Đang So Khớp Ngữ Nghĩa...';
    retBadge.className = 'badge badge-warning';
    retContainer.innerHTML = '<p class="placeholder-text">🔍 Đang tính toán Cosine Similarity trên không gian vector của toàn bộ chunks...</p>';

    try {
        const res = await fetch(`${API_BASE}/ai/rag/retrieve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: query,
                top_k: topK,
                chunk_size: chunkSize,
                chunk_overlap: chunkOverlap,
                file_type_filter: fileType
            })
        });

        const data = await res.json();
        lastRetrievedChunks = data.retrieved_chunks || [];

        retBadge.innerText = `Tìm thấy Top-${lastRetrievedChunks.length} Chunks (${data.execution_time_ms}ms)`;
        retBadge.className = 'badge badge-success';

        if (lastRetrievedChunks.length === 0) {
            retContainer.innerHTML = '<div class="alert alert-warning">Không tìm thấy đoạn thông tin phù hợp trong kho tài liệu.</div>';
            return;
        }

        let html = `
            <div class="alert alert-success" style="margin-bottom:12px; font-size:0.85rem;">
                🎯 <strong>Kết quả Bước 1 (Retrieval):</strong> Đã quét qua <strong>${data.total_chunks_searched}</strong> chunks 
                trong kho tri thức và xếp hạng <strong>Top-${lastRetrievedChunks.length}</strong> chunks có điểm tương đồng Cosine Similarity cao nhất 
                <em>(Lưu ý: Chưa gửi bất kỳ dữ liệu nào đến LLM)</em>.
            </div>
            <div class="rag-topk-list">
        `;

        lastRetrievedChunks.forEach(c => {
            const scoreNum = (c.similarity_score * 100).toFixed(1);
            let scoreBadgeClass = 'badge-success';
            if (c.similarity_score < 0.3) scoreBadgeClass = 'badge-warning';
            if (c.similarity_score < 0.15) scoreBadgeClass = 'badge-info';

            html += `
                <div class="rag-topk-item" id="topk-item-${c.chunk_id}">
                    <div class="rag-topk-header">
                        <span class="rag-rank-badge">#${c.rank}</span>
                        <span class="badge ${scoreBadgeClass}">Độ tương đồng: ${scoreNum}%</span>
                        <strong style="color:var(--text-main); margin-left:6px;">${c.doc_name}</strong>
                        <span class="badge badge-purple" style="margin-left:4px;">${c.chunk_id}</span>
                        <small style="color:var(--text-muted); margin-left:auto;">Vị trí ký tự: [${c.start_char} ➔ ${c.end_char}]</small>
                    </div>
                    <div class="rag-topk-content">
                        ${highlightQueryTerms(c.content, query)}
                    </div>
                </div>
            `;
        });
        html += '</div>';
        retContainer.innerHTML = html;

        // Kích hoạt sáng nút Bước 2
        if (btnStep2) {
            btnStep2.removeAttribute('disabled');
            btnStep2.classList.add('btn-pulse');
        }

    } catch (e) {
        retBadge.innerText = 'Lỗi Truy Xuất';
        retBadge.className = 'badge badge-danger';
        retContainer.innerHTML = `<p style="color:var(--danger)">Lỗi: ${e.message}</p>`;
    }
}

// BƯỚC 2: Ghép Augmented Prompt và gọi LLM sinh câu trả lời có nguồn (Yêu cầu 4)
async function runRAGGenerateOnly() {
    const query = document.getElementById('rag-query-input').value.trim();
    if (!query) {
        alert('Vui lòng nhập câu hỏi!');
        return;
    }

    if (!lastRetrievedChunks || lastRetrievedChunks.length === 0) {
        alert('Vui lòng thực hiện Bước 1 (Truy xuất Top-K Chunks) trước!');
        return;
    }

    const genContainer = document.getElementById('rag-generate-result');
    const genBadge = document.getElementById('rag-generate-badge');
    const promptContainer = document.getElementById('rag-augmented-prompt-view');

    genBadge.innerText = 'LLM Đang Xử Lý & Grounding...';
    genBadge.className = 'badge badge-warning';
    genContainer.innerHTML = '<p class="placeholder-text">🤖 Đang ghép Augmented Prompt và gửi tới LLM Inference Engine...</p>';

    try {
        const res = await fetch(`${API_BASE}/ai/rag/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: query,
                retrieved_chunks: lastRetrievedChunks
            })
        });

        const data = await res.json();
        genBadge.innerText = `Hoàn Tất (${data.status}) • ${data.execution_time_ms}ms`;
        genBadge.className = data.status === 'ThanhCong' ? 'badge badge-success' : 'badge badge-info';

        // Hiển thị Augmented Prompt thực tế
        if (promptContainer) {
            promptContainer.innerHTML = `
                <pre class="json-view" style="max-height:220px; overflow-y:auto; font-size:0.75rem;">${escapeHtml(data.augmented_prompt)}</pre>
            `;
        }

        // Tạo danh sách Citations
        let citationsHtml = '';
        if (data.citations && data.citations.length > 0) {
            citationsHtml = '<div class="rag-citations-box"><strong>📚 Nguồn Trích Dẫn Minh Chứng (Grounding Citations):</strong><ul>';
            data.citations.forEach((cit, idx) => {
                citationsHtml += `
                    <li>
                        <a href="javascript:void(0)" onclick="highlightChunkCard('${cit.chunk_id}')" style="color:var(--primary); font-weight:600;">
                            [Nguồn ${idx + 1}: ${cit.source_file} (Chunk #${cit.chunk_id})]
                        </a>
                        - <em>Độ tương đồng: ${cit.similarity}</em>: "${escapeHtml(cit.snippet)}"
                    </li>
                `;
            });
            citationsHtml += '</ul></div>';
        }

        genContainer.innerHTML = `
            <div class="rag-answer-box">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span class="badge ${data.status === 'ThanhCong' ? 'badge-primary' : 'badge-purple'}">
                        ${data.status === 'ThanhCong' ? '⚡ Gemini AI (Cloud)' : '🛡️ Rule-Based Grounded Engine'}
                    </span>
                    <small style="color:var(--text-muted);">Thời gian sinh: ${data.execution_time_ms}ms</small>
                </div>
                <div class="rag-answer-text">
                    ${formatAnswerMarkdown(data.answer)}
                </div>
                ${citationsHtml}
            </div>
        `;

    } catch (e) {
        genBadge.innerText = 'Lỗi Sinh Lời Giải';
        genBadge.className = 'badge badge-danger';
        genContainer.innerHTML = `<p style="color:var(--danger)">Lỗi: ${e.message}</p>`;
    }
}

// Chạy toàn bộ luồng RAG 2 bước tự động
async function runFullRAGPipeline() {
    await runRAGRetrieveOnly();
    if (lastRetrievedChunks && lastRetrievedChunks.length > 0) {
        setTimeout(async () => {
            await runRAGGenerateOnly();
        }, 400);
    }
}

// BỘ THỰC NGHIỆM A/B: Thay đổi chunk size và top-k để thấy chất lượng thay đổi (Yêu cầu 5)
async function runRAGParameterComparison() {
    const query = document.getElementById('rag-query-input').value.trim() || 
                  "Máy bị dán keo màn hình hoặc rơi nước thì điều kiện bảo hành và bảo quản thế nào?";
    
    document.getElementById('rag-query-input').value = query;

    const modal = document.getElementById('modal-rag-compare');
    const resultBox = document.getElementById('rag-compare-results');
    
    if (modal) modal.classList.add('active');
    resultBox.innerHTML = '<p class="placeholder-text">🧪 Đang chạy đồng thời 3 kịch bản: Chunk nhỏ (80 chars) vs Chuẩn mực (300 chars) vs Chunk lớn (1200 chars)...</p>';

    try {
        const res = await fetch(`${API_BASE}/ai/rag/compare`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        const data = await res.json();
        let html = `
            <div class="alert alert-info" style="margin-bottom:16px;">
                💡 <strong>Câu hỏi thử nghiệm:</strong> "${escapeHtml(data.query)}"<br>
                <small>Tổng thời gian thực nghiệm 3 kịch bản: ${data.total_benchmark_time_ms}ms</small>
            </div>
            <div class="grid-3" style="gap:16px;">
        `;

        data.scenarios.forEach(sc => {
            html += `
                <div class="card" style="border-top:3px solid var(--primary); display:flex; flex-direction:column;">
                    <div class="card-header" style="padding:10px 12px;">
                        <h5 style="margin:0; font-size:0.9rem;">${sc.name}</h5>
                        <span class="badge ${sc.tag_class}">Top-K: ${sc.top_k}</span>
                    </div>
                    <div style="padding:12px; flex:1; display:flex; flex-direction:column; gap:10px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.8rem; background:rgba(255,255,255,0.03); padding:8px; border-radius:4px;">
                            <span>Số Chunks tạo ra: <strong>${sc.total_chunks_created}</strong></span>
                            <span>Độ tương đồng TB: <strong>${(sc.avg_similarity * 100).toFixed(1)}%</strong></span>
                        </div>
                        <div class="alert ${sc.tag_class === 'badge-success' ? 'alert-success' : 'alert-warning'}" style="font-size:0.8rem; padding:8px;">
                            ${sc.evaluation}
                        </div>
                        <div style="font-size:0.8rem; color:var(--text-muted); font-weight:600;">Câu trả lời sinh ra:</div>
                        <div style="font-size:0.82rem; line-height:1.5; background:rgba(0,0,0,0.2); padding:10px; border-radius:4px; max-height:160px; overflow-y:auto; color:var(--text-main);">
                            ${formatAnswerMarkdown(sc.answer)}
                        </div>
                    </div>
                </div>
            `;
        });

        html += '</div>';
        resultBox.innerHTML = html;

    } catch (e) {
        resultBox.innerHTML = `<p style="color:var(--danger)">Lỗi thực nghiệm: ${e.message}</p>`;
    }
}

function closeRAGCompareModal() {
    const modal = document.getElementById('modal-rag-compare');
    if (modal) modal.classList.remove('active');
}

// Highlight thẻ chunk khi nhấp vào citation
function highlightChunkCard(chunkId) {
    const el = document.getElementById(`topk-item-${chunkId}`);
    if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.style.transition = 'all 0.4s ease';
        el.style.boxShadow = '0 0 0 3px var(--primary), 0 0 15px rgba(56, 189, 248, 0.4)';
        setTimeout(() => {
            el.style.boxShadow = '';
        }, 2000);
    }
}

// Highlight từ khóa tìm kiếm trong đoạn trích
function highlightQueryTerms(text, query) {
    if (!query) return escapeHtml(text);
    const words = query.split(/\s+/).filter(w => w.length > 2);
    let escaped = escapeHtml(text);
    words.forEach(w => {
        const regex = new RegExp(`(${escapeRegExp(w)})`, 'gi');
        escaped = escaped.replace(regex, '<mark class="rag-highlight">$1</mark>');
    });
    return escaped;
}

function formatAnswerMarkdown(text) {
    if (!text) return '';
    let formatted = escapeHtml(text);
    formatted = formatted.replace(/\n\n/g, '<br><br>');
    formatted = formatted.replace(/\n/g, '<br>');
    formatted = formatted.replace(/•\s/g, '&bull; ');
    // Highlight citations [Nguồn: ...]
    formatted = formatted.replace(/\[Nguồn:\s*([^\]]+)\]/g, '<span class="badge badge-purple" style="display:inline-block; margin:2px 0;">📌 Nguồn: $1</span>');
    return formatted;
}

function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
