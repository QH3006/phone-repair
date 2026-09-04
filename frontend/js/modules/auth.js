/**
 * Module Authentication & RBAC (Login 4 Roles, JWT Token Storage, Session Sync & Dynamic Role Permissions)
 */

const ROLE_METADATA = {
    'admin': {
        username: 'admin',
        name: 'Nguyễn Hoàng Long',
        roleKey: 'QuanLy',
        roleLabel: 'Quản Lý (Admin)',
        avatar: 'HL',
        badgeClass: 'role-badge-admin',
        bannerClass: 'role-admin',
        allowedTabs: ['tab-dashboard', 'tab-repairs', 'tab-customers', 'tab-inventory', 'tab-billing', 'tab-users', 'tab-ai-sandbox', 'tab-ai-logs', 'tab-architecture'],
        scopeDesc: '🛡️ <strong>Toàn quyền hệ thống (Super Admin):</strong> Quản lý tài khoản nhân sự, phân quyền RBAC, sửa danh mục kho & bảng giá, xem doanh thu, cấu hình hệ thống & tra cứu Audit Logs.',
        color: 'linear-gradient(135deg, #6366f1, #a855f7)'
    },
    'letan': {
        username: 'letan',
        name: 'Trần Mai Phương',
        roleKey: 'LeTan',
        roleLabel: 'Lễ Tân (Receptionist)',
        avatar: 'MP',
        badgeClass: 'role-badge-letan',
        bannerClass: 'role-letan',
        allowedTabs: ['tab-dashboard', 'tab-repairs', 'tab-customers', 'tab-inventory', 'tab-billing', 'tab-ai-sandbox'],
        scopeDesc: '💁 <strong>Quyền Lễ Tân / Tiếp Nhận:</strong> Tiếp nhận máy mới, tạo hồ sơ khách & thiết bị, phân công KTV, tra cứu bảo hành, kích hoạt AI sinh SMS gửi khách. <span style=\"color:#f87171; font-weight:600;\">(Đã ẩn: Kỹ thuật tháo máy, Lập hóa đơn, Quản trị nhân sự & Kiến trúc)</span>',
        color: 'linear-gradient(135deg, #ec4899, #f43f5e)'
    },
    'ktv': {
        username: 'ktv',
        name: 'Lê Quốc Cường',
        roleKey: 'KyThuatVien',
        roleLabel: 'Kỹ Thuật Viên (Technician)',
        avatar: 'QC',
        badgeClass: 'role-badge-ktv',
        bannerClass: 'role-ktv',
        allowedTabs: ['tab-dashboard', 'tab-repairs', 'tab-inventory', 'tab-ai-sandbox'],
        scopeDesc: '🔧 <strong>Quyền Kỹ Thuật Viên:</strong> Khám máy đo đạc, cập nhật tiến độ phần cứng, xuất kho linh kiện vào phiếu sửa, dùng AI tóm tắt lỗi kỹ thuật. <span style=\"color:#f87171; font-weight:600;\">(Đã ẩn: Tiếp nhận máy, Hóa đơn thu tiền, Khách hàng, Quản trị nhân sự & Kiến trúc)</span>',
        color: 'linear-gradient(135deg, #0284c7, #06b6d4)'
    },
    'thungan': {
        username: 'thungan',
        name: 'Phạm Thanh Hà',
        roleKey: 'ThuNgan',
        roleLabel: 'Thu Ngân (Cashier)',
        avatar: 'TH',
        badgeClass: 'role-badge-thungan',
        bannerClass: 'role-thungan',
        allowedTabs: ['tab-dashboard', 'tab-repairs', 'tab-billing'],
        scopeDesc: '💳 <strong>Quyền Thu Ngân & Kế Toán:</strong> Xem phiếu đã sửa xong, lập hóa đơn thanh toán tiền mặt/chuyển khoản QR, in hóa đơn & cấp thẻ bảo hành điện tử. <span style=\"color:#f87171; font-weight:600;\">(Đã ẩn hoàn toàn: Tiếp nhận, Khách hàng, Kho linh kiện, Nhân sự, AI & Kiến trúc hệ thống)</span>',
        color: 'linear-gradient(135deg, #059669, #10b981)'
    }
};

function getCurrentUserRole() {
    const saved = localStorage.getItem('phonecare_user');
    if (saved) {
        try {
            const u = JSON.parse(saved);
            return u.vai_tro || 'QuanLy';
        } catch (e) {}
    }
    return 'QuanLy';
}

function getCurrentUsername() {
    const saved = localStorage.getItem('phonecare_user');
    if (saved) {
        try {
            const u = JSON.parse(saved);
            return u.ten_dang_nhap || 'admin';
        } catch (e) {}
    }
    return 'admin';
}

function initAuth() {
    const savedUser = localStorage.getItem('phonecare_user');
    if (savedUser) {
        try {
            const user = JSON.parse(savedUser);
            applyUserSession(user);
            return;
        } catch (e) {
            console.error('Lỗi đọc session auth:', e);
        }
    }
    // Mặc định đăng nhập Quản Lý
    quickLoginRole('admin');
}

function openLoginModal() {
    const modal = document.getElementById('login-modal');
    const alertBox = document.getElementById('login-alert-box');
    if (alertBox) alertBox.style.display = 'none';
    if (modal) modal.style.display = 'flex';
}

function closeLoginModal() {
    const modal = document.getElementById('login-modal');
    if (modal) modal.style.display = 'none';
}

function switchRoleLive(username) {
    // 1. Cập nhật ngay trạng thái active của pill button
    document.querySelectorAll('.role-pill').forEach(btn => btn.classList.remove('active'));
    const targetPill = document.getElementById(`pill-role-${username}`);
    if (targetPill) targetPill.classList.add('active');

    // 2. Tự động đăng nhập với tài khoản tương ứng
    quickLoginRole(username);
}

function quickLoginRole(username) {
    const uInput = document.getElementById('login-username');
    const pInput = document.getElementById('login-password');
    if (uInput) uInput.value = username;
    if (pInput) pInput.value = '123456';
    
    // Tự động kích hoạt đăng nhập
    const fakeEvent = { preventDefault: () => {} };
    submitLogin(fakeEvent);
}

async function submitLogin(event) {
    if (event && event.preventDefault) event.preventDefault();
    
    const uInput = document.getElementById('login-username');
    const pInput = document.getElementById('login-password');
    const alertBox = document.getElementById('login-alert-box');
    const btnSubmit = document.getElementById('btn-do-login');

    const username = uInput ? uInput.value.trim() : 'admin';
    const password = pInput ? pInput.value.trim() : '123456';

    if (!username || !password) {
        showLoginAlert('Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!', 'danger');
        return;
    }

    if (btnSubmit) {
        btnSubmit.disabled = true;
        btnSubmit.innerHTML = '<span>⏳ Đang xác thực...</span>';
    }

    try {
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ten_dang_nhap: username, mat_khau: password })
        });
        const data = await res.json();

        if (res.ok && data.access_token) {
            // Lưu session vào localStorage
            localStorage.setItem('phonecare_user', JSON.stringify(data));
            localStorage.setItem('phonecare_jwt', data.access_token);
            localStorage.setItem('token', data.access_token);

            applyUserSession(data);
            showLoginAlert(`✓ Đăng nhập thành công với vai trò ${data.vai_tro || 'Người dùng'}!`, 'success');
            
            setTimeout(() => {
                closeLoginModal();
                // Refresh data cho tab hiện tại
                const activePane = document.querySelector('.tab-pane.active');
                if (activePane) {
                    const tabId = activePane.id;
                    if (tabId === 'tab-dashboard' && typeof loadDashboardData === 'function') loadDashboardData();
                    if (tabId === 'tab-repairs' && typeof loadRepairsData === 'function') loadRepairsData();
                    if (tabId === 'tab-customers' && typeof loadCustomersData === 'function') loadCustomersData();
                    if (tabId === 'tab-inventory' && typeof loadInventoryData === 'function') loadInventoryData();
                    if (tabId === 'tab-billing' && typeof loadBillingData === 'function') loadBillingData();
                    if (tabId === 'tab-users' && typeof loadUsersData === 'function') loadUsersData();
                    if (tabId === 'tab-ai-logs' && typeof loadAILogs === 'function') loadAILogs();
                }
            }, 300);
        } else {
            showLoginAlert(data.detail || 'Đăng nhập không thành công. Kiểm tra lại thông tin.', 'danger');
        }
    } catch (e) {
        showLoginAlert('Lỗi kết nối máy chủ: ' + e.message, 'danger');
    } finally {
        if (btnSubmit) {
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = '<span>🔐 Đăng Nhập</span>';
        }
    }
}

function showLoginAlert(msg, type) {
    const alertBox = document.getElementById('login-alert-box');
    if (!alertBox) return;
    alertBox.style.display = 'block';
    alertBox.innerText = msg;
    if (type === 'success') {
        alertBox.style.background = 'rgba(52, 211, 153, 0.15)';
        alertBox.style.color = '#34d399';
        alertBox.style.border = '1px solid #34d399';
    } else {
        alertBox.style.background = 'rgba(248, 113, 113, 0.15)';
        alertBox.style.color = '#f87171';
        alertBox.style.border = '1px solid #f87171';
    }
}

function applyUserSession(user) {
    const username = user.ten_dang_nhap || 'admin';
    const vaiTro = user.vai_tro || 'QuanLy';
    const meta = ROLE_METADATA[username] || {
        username: username,
        name: user.ho_ten,
        roleKey: vaiTro,
        roleLabel: vaiTro,
        avatar: user.ho_ten ? user.ho_ten.substring(0, 2).toUpperCase() : 'US',
        badgeClass: 'role-badge-admin',
        bannerClass: 'role-admin',
        allowedTabs: ['tab-dashboard', 'tab-repairs', 'tab-billing'],
        scopeDesc: `Vai trò: ${vaiTro}`,
        color: 'var(--primary)'
    };

    // 1. Cập nhật Sidebar Footer User Chip
    const sideName = document.getElementById('current-user-name');
    const sideRole = document.getElementById('current-user-role');
    const sideAvatar = document.getElementById('current-user-avatar');

    if (sideName) sideName.innerText = user.ho_ten || meta.name;
    if (sideRole) sideRole.innerText = `Vai trò: ${meta.roleLabel || vaiTro}`;
    if (sideAvatar) {
        sideAvatar.innerText = meta.avatar;
        sideAvatar.style.background = meta.color;
    }

    // 2. Cập nhật Top Header
    const headName = document.getElementById('header-user-name');
    const headBadge = document.getElementById('header-user-badge');
    const headAvatar = document.getElementById('header-user-avatar');

    if (headName) headName.innerText = user.ho_ten || meta.name;
    if (headBadge) headBadge.innerText = meta.roleKey || user.vai_tro;
    if (headAvatar) {
        headAvatar.innerText = meta.avatar;
        headAvatar.style.background = meta.color;
    }

    // 3. Cập nhật Role Banner phía trên Content
    const banner = document.getElementById('role-banner');
    const bBadge = document.getElementById('role-banner-badge');
    const bUser = document.getElementById('role-banner-user');
    const bUname = document.getElementById('role-banner-username');
    const bDesc = document.getElementById('role-banner-desc');

    if (banner) {
        banner.className = `role-banner ${meta.bannerClass}`;
    }
    if (bBadge) {
        bBadge.className = `role-badge ${meta.badgeClass}`;
        bBadge.innerText = meta.roleLabel;
    }
    if (bUser) bUser.innerText = user.ho_ten || meta.name;
    if (bUname) bUname.innerText = `(user: ${username})`;
    if (bDesc) bDesc.innerHTML = meta.scopeDesc;

    // Cập nhật active pill button
    document.querySelectorAll('.role-pill').forEach(btn => btn.classList.remove('active'));
    const activePill = document.getElementById(`pill-role-${username}`);
    if (activePill) activePill.classList.add('active');

    // 4. Áp dụng Phân quyền RBAC động trên Sidebar & Toàn bộ Giao diện
    applyRolePermissionsToUI(vaiTro, meta.allowedTabs);
}

function applyRolePermissionsToUI(vaiTro, allowedTabs) {
    if (!allowedTabs) {
        const u = getCurrentUsername();
        allowedTabs = ROLE_METADATA[u] ? ROLE_METADATA[u].allowedTabs : ['tab-dashboard', 'tab-repairs'];
    }

    // A. Quét TẤT CẢ các phần tử có thuộc tính data-roles trong toàn bộ trang
    let hasVisibleAI = false;
    document.querySelectorAll('[data-roles]').forEach(el => {
        const roles = (el.getAttribute('data-roles') || '').split(',').map(r => r.trim());
        const isNav = el.classList.contains('nav-item');

        if (roles.includes(vaiTro)) {
            el.style.display = isNav ? 'flex' : '';
            if (isNav) {
                const tabId = el.getAttribute('data-tab');
                if (tabId === 'tab-ai-sandbox' || tabId === 'tab-ai-logs') {
                    hasVisibleAI = true;
                }
            }
        } else {
            el.style.display = 'none';
        }
    });

    // Ẩn tiêu đề nhóm AI trong sidebar nếu vai trò đó không dùng AI (ví dụ Thu Ngân)
    const aiTitle = document.getElementById('nav-title-ai');
    if (aiTitle) {
        aiTitle.style.display = hasVisibleAI ? 'block' : 'none';
    }

    // B. Nếu tab hiện tại bị cấm đối với vai trò mới, tự động redirect về Tab được phép
    const currentActiveItem = document.querySelector('.nav-item.active');
    const currentTabId = currentActiveItem ? currentActiveItem.getAttribute('data-tab') : '';
    
    if (currentTabId && !allowedTabs.includes(currentTabId)) {
        // Chuyển về Dashboard hoặc tab đầu tiên được phép
        const fallbackTabId = allowedTabs.includes('tab-dashboard') ? 'tab-dashboard' : allowedTabs[0];
        const fallbackNavBtn = document.querySelector(`.nav-item[data-tab="${fallbackTabId}"]`);
        if (fallbackNavBtn) {
            fallbackNavBtn.click();
        }
    }

    // C. Phân quyền các nút thao tác nghiệp vụ trên các trang (Action-level RBAC)
    
    // 1. Nút "Tiếp Nhận Máy Mới" (Tab 2)
    const btnIntake = document.getElementById('btn-intake-new');
    if (btnIntake) {
        if (vaiTro === 'QuanLy' || vaiTro === 'LeTan') {
            btnIntake.style.display = 'inline-flex';
            btnIntake.disabled = false;
        } else {
            btnIntake.style.display = 'none'; // Thu Ngân và KTV không tiếp nhận máy
        }
    }

    // 2. Nút "Nhập Linh Kiện" & "Thêm Dịch Vụ" (Tab 4)
    const btnAddPart = document.querySelector("button[onclick='openPartModal()']");
    const btnAddSrv = document.querySelector("button[onclick='openServiceModal()']");
    if (btnAddPart) {
        btnAddPart.style.display = (vaiTro === 'QuanLy') ? 'inline-flex' : 'none';
    }
    if (btnAddSrv) {
        btnAddSrv.style.display = (vaiTro === 'QuanLy') ? 'inline-flex' : 'none';
    }

    // 3. Nút "Thêm Tài Khoản Nhân Viên" (Tab 6)
    const btnAddUser = document.querySelector("button[onclick='openUserModal()']");
    if (btnAddUser) {
        btnAddUser.style.display = (vaiTro === 'QuanLy') ? 'inline-flex' : 'none';
    }

    // 4. Phân hệ AI Subtabs (Tab 7)
    const subtabFaultBtn = document.querySelector("button[data-subtab='subtab-fault']");
    const subtabMsgBtn = document.querySelector("button[data-subtab='subtab-message']");
    const subtabExplainBtn = document.querySelector("button[data-subtab='subtab-explain']");

    if (subtabFaultBtn) {
        subtabFaultBtn.style.display = (vaiTro === 'KyThuatVien' || vaiTro === 'QuanLy') ? 'flex' : 'none';
    }
    if (subtabMsgBtn) {
        subtabMsgBtn.style.display = (vaiTro === 'LeTan' || vaiTro === 'QuanLy') ? 'flex' : 'none';
    }
    if (subtabExplainBtn) {
        subtabExplainBtn.style.display = (vaiTro !== 'ThuNgan') ? 'flex' : 'none';
    }

    // Đảm bảo subtab AI active hợp lệ
    const activeSubtabBtn = document.querySelector('.ai-tab-btn.active');
    if (activeSubtabBtn && activeSubtabBtn.style.display === 'none') {
        const firstVisibleSubtab = document.querySelector('.ai-tab-btn:not([style*="display: none"])');
        if (firstVisibleSubtab) firstVisibleSubtab.click();
    }
}

function handleLogout() {
    localStorage.removeItem('phonecare_user');
    localStorage.removeItem('phonecare_jwt');
    localStorage.removeItem('token');
    
    showLoginAlert('Đã đăng xuất tài khoản.', 'success');
    setTimeout(() => {
        closeLoginModal();
        quickLoginRole('admin');
    }, 500);
}
