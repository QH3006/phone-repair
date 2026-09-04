/**
 * Module Navigation (Tab switching & Dynamic page loading)
 */

function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const tabRoles = (item.getAttribute('data-roles') || '').split(',');
            const currentRole = (typeof getCurrentUserRole === 'function') ? getCurrentUserRole() : 'QuanLy';
            if (tabRoles.length > 0 && !tabRoles.includes(currentRole)) {
                alert(`⚠️ Quyền bị từ chối! Vai trò '${currentRole}' không được phép truy cập phân hệ này theo ma trận phân quyền RBAC.`);
                return;
            }

            navItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');

            const tabId = item.getAttribute('data-tab');
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('active');
            });
            const activePane = document.getElementById(tabId);
            if (activePane) activePane.classList.add('active');

            // Cập nhật tiêu đề trang
            const headingMap = {
                'tab-dashboard': '📊 Dashboard Thống Kê & Báo Cáo Thời Gian Thực',
                'tab-repairs': '📱 Quản Lý Phiếu Tiếp Nhận & Sửa Chữa',
                'tab-customers': '👥 Quản Lý Khách Hàng & Thiết Bị Tiếp Nhận',
                'tab-inventory': '📦 Quản Lý Kho Linh Kiện & Dịch Vụ Sửa Chữa',
                'tab-billing': '🧾 Quản Lý Hóa Đơn Thu Tiền & Bảo Hành Điện Tử',
                'tab-users': '🛡️ Quản Lý Nhân Sự & Phân Quyền Vai Trò RBAC',
                'tab-ai-sandbox': '✨ Phân Hệ Trợ Lý AI Thông Minh',
                'tab-ai-logs': '📝 Nhật Ký Tương Tác AI Thời Gian Thực (Audit Logs)',
                'tab-architecture': '🏛️ Kiến Trúc Hệ Thống & Ma Trận Phân Quyền'
            };
            const headingEl = document.getElementById('page-heading');
            if (headingEl) {
                headingEl.innerText = headingMap[tabId] || 'Hệ Thống Quản Lý Sửa Chữa Điện Thoại';
            }

            // Tự động load dữ liệu cho tab tương ứng
            if (tabId === 'tab-dashboard') loadDashboardData();
            if (tabId === 'tab-repairs') loadRepairsData();
            if (tabId === 'tab-customers') loadCustomersData();
            if (tabId === 'tab-inventory') loadInventoryData();
            if (tabId === 'tab-billing') loadBillingData();
            if (tabId === 'tab-users') loadUsersData();
            if (tabId === 'tab-ai-logs') loadAILogs();
        });
    });
}

function initAISubtabs() {
    const aiTabs = document.querySelectorAll('.ai-tab-btn');
    aiTabs.forEach(btn => {
        btn.addEventListener('click', () => {
            aiTabs.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const subtabId = btn.getAttribute('data-subtab');
            document.querySelectorAll('.ai-subpane').forEach(pane => pane.classList.remove('active'));
            const targetPane = document.getElementById(subtabId);
            if (targetPane) targetPane.classList.add('active');
        });
    });
}
