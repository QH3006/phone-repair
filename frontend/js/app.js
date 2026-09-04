/**
 * PhoneCare AI - Master Application Entry Point
 * Phase KT2: Comprehensive Modular Architecture
 */

// Global API Base
const API_BASE = '/api';

// Application Bootstrap
document.addEventListener('DOMContentLoaded', () => {
    // 1. Khởi tạo giao diện, Theme & Phiên đăng nhập
    initTheme();
    initAuth();
    initNavigation();
    initAISubtabs();

    // 2. Tải dữ liệu ban đầu
    if (typeof loadDashboardData === 'function') loadDashboardData();
    if (typeof loadRepairsData === 'function') loadRepairsData();

    // 3. Đóng modal khi click ra ngoài backdrop hoặc bấm phím Escape
    window.addEventListener('click', (e) => {
        if (e.target && e.target.classList && e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
            document.body.style.overflow = '';
        }
    });

    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal').forEach(m => m.style.display = 'none');
            document.body.style.overflow = '';
        }
    });
});
