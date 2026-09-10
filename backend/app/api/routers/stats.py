from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone

from backend.app.db.database import get_db
from backend.app.db.models import (
    PhieuSuaChua, KhachHang, ThietBi, LinhKien, HoaDon, NhatKyAI, NguoiDung
)
from backend.app.core.security import get_current_user

router = APIRouter(prefix="/stats", tags=["Hệ thống & Thống kê Dashboard"])

@router.get("/overview")
def get_dashboard_overview(db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    """Tổng hợp số liệu thống kê thời gian thực cho Dashboard."""
    # 1. Số liệu tổng quan
    total_repairs = db.query(PhieuSuaChua).count()
    active_repairs = db.query(PhieuSuaChua).filter(
        PhieuSuaChua.trang_thai.in_(["TiepNhan", "PhanCongKTV", "DangKiemTra", "BaoGia_ChoDuyet", "DangSuaChua"])
    ).count()
    completed_repairs = db.query(PhieuSuaChua).filter(
        PhieuSuaChua.trang_thai.in_(["DaSuaXong", "DaThanhToan", "HoanTat_TraMay"])
    ).count()
    total_customers = db.query(KhachHang).count()
    total_parts = db.query(LinhKien).count()
    low_stock_parts = db.query(LinhKien).filter(LinhKien.so_luong_ton <= 5).count()
    total_ai_logs = db.query(NhatKyAI).count()
    
    # 2. Doanh thu
    invoices = db.query(HoaDon).all()
    total_revenue = sum(inv.tong_tien for inv in invoices)
    
    # 3. Phân bổ theo 8 trạng thái phiếu
    statuses = [
        "TiepNhan", "PhanCongKTV", "DangKiemTra", "BaoGia_ChoDuyet",
        "DangSuaChua", "DaSuaXong", "DaThanhToan", "HoanTat_TraMay"
    ]
    status_counts = {}
    for s in statuses:
        status_counts[s] = db.query(PhieuSuaChua).filter(PhieuSuaChua.trang_thai == s).count()

    # 4. Top 5 model thiết bị sửa nhiều nhất
    top_devices = db.query(
        ThietBi.model_may, func.count(PhieuSuaChua.id).label("count")
    ).join(PhieuSuaChua, PhieuSuaChua.thiet_bi_id == ThietBi.id).group_by(ThietBi.model_may).order_by(func.count(PhieuSuaChua.id).desc()).limit(5).all()
    
    top_models = [{"model": row[0], "count": row[1]} for row in top_devices]

    # 5. Top 5 linh kiện tồn kho thấp
    critical_parts = db.query(LinhKien).filter(LinhKien.so_luong_ton <= 5).order_by(LinhKien.so_luong_ton.asc()).limit(5).all()
    low_stock_list = [{"id": p.id, "ten": p.ten_linh_kien, "ton_kho": p.so_luong_ton} for p in critical_parts]

    return {
        "status": "Healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_repairs": total_repairs,
            "active_repairs": active_repairs,
            "completed_repairs": completed_repairs,
            "total_customers": total_customers,
            "total_parts": total_parts,
            "low_stock_parts": low_stock_parts,
            "total_revenue": total_revenue,
            "total_ai_logs": total_ai_logs
        },
        "status_distribution": status_counts,
        "top_models": top_models,
        "low_stock_items": low_stock_list
    }
