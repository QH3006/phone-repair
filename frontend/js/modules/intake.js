/**
 * Module Ticket Intake (Create Customer, Device, Ticket & Photo Upload)
 */

const DEMO_IMAGES = {
    broken_screen: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="280" viewBox="0 0 400 280"><rect width="400" height="280" fill="%230f172a" rx="12"/><rect x="90" y="15" width="220" height="250" rx="16" fill="%231e293b" stroke="%2338bdf8" stroke-width="3"/><rect x="105" y="40" width="190" height="200" rx="8" fill="%230284c7" fill-opacity="0.15"/><circle cx="200" cy="28" r="4" fill="%2394a3b8"/><path d="M 120 50 L 190 130 L 160 170 L 250 230 M 190 130 L 270 100 M 190 130 L 130 210" stroke="%23f87171" stroke-width="3" stroke-linecap="round" fill="none"/><text x="200" y="260" font-family="sans-serif" font-size="11" fill="%23f87171" font-weight="bold" text-anchor="middle">⚠️ MÀN HÌNH NỨT VỠ KÍNH & LIỆT CẢM ỨNG</text></svg>`,
    stripe_screen: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="280" viewBox="0 0 400 280"><rect width="400" height="280" fill="%230f172a" rx="12"/><rect x="90" y="15" width="220" height="250" rx="16" fill="%231e293b" stroke="%23818cf8" stroke-width="3"/><rect x="105" y="40" width="190" height="200" rx="8" fill="%230b0f19"/><line x1="140" y1="40" x2="140" y2="240" stroke="%2334d399" stroke-width="4"/><line x1="195" y1="40" x2="195" y2="240" stroke="%23ec4899" stroke-width="6"/><line x1="260" y1="40" x2="260" y2="240" stroke="%2338bdf8" stroke-width="3"/><text x="200" y="260" font-family="sans-serif" font-size="11" fill="%23fbbf24" font-weight="bold" text-anchor="middle">⚡ SỌC MÀN HÌNH AMOLED & CHẬP NGUỒN</text></svg>`,
    battery_swollen: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="280" viewBox="0 0 400 280"><rect width="400" height="280" fill="%230f172a" rx="12"/><rect x="90" y="15" width="220" height="250" rx="16" fill="%231e293b" stroke="%23fbbf24" stroke-width="3"/><rect x="125" y="60" width="150" height="140" rx="12" fill="%23d97706" fill-opacity="0.25" stroke="%23fbbf24" stroke-dasharray="6,4" stroke-width="2"/><text x="200" y="130" font-family="sans-serif" font-size="32" text-anchor="middle">🔋</text><text x="200" y="165" font-family="sans-serif" font-size="12" fill="%23fbbf24" font-weight="bold" text-anchor="middle">PIN PHỒNG / KÊNH NẮP LƯNG</text><text x="200" y="260" font-family="sans-serif" font-size="11" fill="%23f87171" font-weight="bold" text-anchor="middle">⚠️ HỎNG BO CÁP SẠC & PIN BẢO TRÌ</text></svg>`
};

let currentIntakePhotoBase64 = null;

function openIntakeModal() {
    const modal = document.getElementById('intake-modal');
    if (modal) modal.style.display = 'flex';
    fillSampleIntake('iphone');
}

function closeIntakeModal() {
    const modal = document.getElementById('intake-modal');
    if (modal) modal.style.display = 'none';
}

function fillSampleIntake(type) {
    if (type === 'iphone') {
        document.getElementById('intake-customer-name').value = 'Hoàng Đức Minh';
        document.getElementById('intake-customer-phone').value = '0988123456';
        document.getElementById('intake-customer-address').value = '123 Cầu Giấy, Hà Nội';
        document.getElementById('intake-device-brand').value = 'Apple';
        document.getElementById('intake-device-model').value = 'iPhone 14 Pro Max 256GB Gold';
        document.getElementById('intake-device-imei').value = '354892091234567';
        document.getElementById('intake-device-pass').value = '112233';
        document.getElementById('intake-fault-desc').value = 'Màn hình nứt vỡ góc trên, cảm ứng đơ không phản hồi, máy sạc không vào.';
        document.getElementById('intake-tech-notes').value = 'Viền nhôm xước dăm nhẹ, kính lưng nguyên vẹn.';
        document.getElementById('intake-est-cost').value = 2850000;
        setDemoPhoto('broken_screen');
    } else if (type === 'samsung') {
        document.getElementById('intake-customer-name').value = 'Nguyễn Thùy Linh';
        document.getElementById('intake-customer-phone').value = '0977234567';
        document.getElementById('intake-customer-address').value = '45 Hai Bà Trưng, Hoàn Kiếm, Hà Nội';
        document.getElementById('intake-device-brand').value = 'Samsung';
        document.getElementById('intake-device-model').value = 'Galaxy S24 Ultra 512GB';
        document.getElementById('intake-device-imei').value = '358912093847561';
        document.getElementById('intake-device-pass').value = 'Vẽ hình chữ L';
        document.getElementById('intake-fault-desc').value = 'Màn hình bị sọc xanh dọc, cắm sạc nóng ran không lên nguồn.';
        document.getElementById('intake-tech-notes').value = 'Ngoại quan đẹp 99%, có dán bảo vệ camera.';
        document.getElementById('intake-est-cost').value = 3400000;
        setDemoPhoto('stripe_screen');
    } else if (type === 'xiaomi') {
        document.getElementById('intake-customer-name').value = 'Phan Anh Tuấn';
        document.getElementById('intake-customer-phone').value = '0911345678';
        document.getElementById('intake-customer-address').value = '88 Nguyễn Trãi, Thanh Xuân, Hà Nội';
        document.getElementById('intake-device-brand').value = 'Xiaomi';
        document.getElementById('intake-device-model').value = 'Xiaomi 13T Pro 12GB/512GB';
        document.getElementById('intake-device-imei').value = '864912048591823';
        document.getElementById('intake-device-pass').value = '000000';
        document.getElementById('intake-fault-desc').value = 'Hỏng bo sạc Type-C, pin phù nhẹ làm kênh nhẹ nắp lưng sau.';
        document.getElementById('intake-tech-notes').value = 'Nắp lưng hở mép trái 1mm do pin phù.';
        document.getElementById('intake-est-cost').value = 950000;
        setDemoPhoto('battery_swollen');
    }
}

function handleImageUpload(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            currentIntakePhotoBase64 = e.target.result;
            showPhotoPreview(currentIntakePhotoBase64, 'Ảnh tải lên từ thiết bị');
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function setDemoPhoto(type) {
    const photo = DEMO_IMAGES[type];
    if (photo) {
        currentIntakePhotoBase64 = photo;
        const labels = {
            broken_screen: 'Ảnh demo: Màn hình nứt vỡ kính',
            stripe_screen: 'Ảnh demo: Sọc màn hình AMOLED & Chập nguồn',
            battery_swollen: 'Ảnh demo: Pin phồng & Hỏng bo cáp sạc'
        };
        showPhotoPreview(photo, labels[type] || 'Ảnh hiện trạng tiếp nhận');
    }
}

function showPhotoPreview(src, label) {
    const container = document.getElementById('photo-preview-container');
    const img = document.getElementById('photo-preview-img');
    const lbl = document.getElementById('photo-preview-label');
    const btnClear = document.getElementById('btn-clear-photo');
    if (container && img) {
        img.src = src;
        if (lbl) lbl.innerText = label;
        container.style.display = 'block';
        if (btnClear) btnClear.style.display = 'inline-flex';
    }
}

function clearPhoto() {
    currentIntakePhotoBase64 = null;
    const container = document.getElementById('photo-preview-container');
    const input = document.getElementById('intake-photo-input');
    const btnClear = document.getElementById('btn-clear-photo');
    if (container) container.style.display = 'none';
    if (input) input.value = '';
    if (btnClear) btnClear.style.display = 'none';
}

async function submitIntakeTicket(event) {
    event.preventDefault();
    const btn = document.getElementById('btn-submit-intake');
    btn.disabled = true;
    btn.innerHTML = '<span>⏳ Đang xử lý lưu phiếu...</span>';

    const payload = {
        ho_ten: document.getElementById('intake-customer-name').value,
        so_dien_thoai: document.getElementById('intake-customer-phone').value,
        dia_chi: document.getElementById('intake-customer-address').value,
        hang_san_xuat: document.getElementById('intake-device-brand').value,
        model_may: document.getElementById('intake-device-model').value,
        so_imei: document.getElementById('intake-device-imei').value,
        mat_khau_may: document.getElementById('intake-device-pass').value,
        mo_ta_loi_khach: document.getElementById('intake-fault-desc').value,
        ghi_chu_ky_thuat: document.getElementById('intake-tech-notes').value,
        tong_tien_du_kien: parseFloat(document.getElementById('intake-est-cost').value) || 0.0,
        hinh_anh: currentIntakePhotoBase64
    };

    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const res = await fetch('/api/repairs', {
            method: 'POST',
            headers,
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        
        if (res.ok && data.success) {
            alert(`Lập phiếu tiếp nhận ${data.ma_phieu} thành công!`);
            closeIntakeModal();
            clearPhoto();
            const form = document.getElementById('intake-form');
            if (form) form.reset();
            loadRepairsData();
            loadDashboardData();
        } else {
            alert('Lỗi tạo phiếu: ' + (data.detail || 'Không thể tạo phiếu (Cần quyền Lễ Tân hoặc Quản Lý)'));
        }
    } catch (e) {
        alert('Lỗi kết nối máy chủ: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span>💾 Lưu & Lập Phiếu Tiếp Nhận</span>';
    }
}
