from fastapi import APIRouter
from backend.app.api.routers import auth, users, customers, devices, parts, services, repairs, invoices, warranties, stats, ai, rag

router = APIRouter()

# Nạp toàn bộ các sub-routers module hóa
router.include_router(auth.router)
router.include_router(users.router)
router.include_router(customers.router)
router.include_router(devices.router)
router.include_router(parts.router)
router.include_router(services.router)
router.include_router(repairs.router)
router.include_router(invoices.router)
router.include_router(warranties.router)
router.include_router(stats.router)
router.include_router(ai.router)
router.include_router(rag.router)

# Endpoint kiểm tra sức khỏe hệ thống & tương thích ngược
@router.get("/system/stats", tags=["Hệ thống & Thống kê"])
def get_system_stats_legacy():
    from backend.app.api.routers.stats import get_dashboard_overview
    from backend.app.db.database import SessionLocal
    db = SessionLocal()
    try:
        overview = get_dashboard_overview(db=db)
        return {
            "status": "Healthy",
            "stats": overview.get("summary", {})
        }
    finally:
        db.close()
