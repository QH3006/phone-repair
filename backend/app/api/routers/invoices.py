from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from backend.app.db.database import get_db
from backend.app.db.models import HoaDon, PhieuSuaChua, NguoiDung, BaoHanh, ChiTietSuaChua
from backend.app.core.security import require_roles, get_current_user
from backend.app.schemas.schemas import InvoiceCreate, InvoiceOut

router = APIRouter(prefix="/invoices", tags=["Quản lý Hóa Đơn & Thanh Toán"])

@router.get("", response_model=List[InvoiceOut])
def list_invoices(
    q: Optional[str] = Query(None, description="Tìm theo mã hóa đơn, mã phiếu hoặc tên khách"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Lấy danh sách các hóa đơn thanh toán."""
    query = db.query(HoaDon)
    if q:
        search = f"%{q.strip()}%"
        query = query.join(HoaDon.phieu_sua_chua).join(PhieuSuaChua.khach_hang).filter(
            (HoaDon.ma_hoa_don.ilike(search)) |
            (PhieuSuaChua.ma_phieu.ilike(search)) |
            (PhieuSuaChua.khach_hang.has(ho_ten=search))
        )
    
    invoices = query.order_by(HoaDon.id.desc()).offset(skip).limit(limit).all()
    result = []
    for inv in invoices:
        p = inv.phieu_sua_chua
        items = []
        if p:
            for ct in p.chi_tiet:
                ten_muc = ct.linh_kien.ten_linh_kien if ct.linh_kien else (ct.dich_vu.ten_dich_vu if ct.dich_vu else "N/A")
                items.append({
                    "ten_muc": ten_muc,
                    "so_luong": ct.so_luong,
                    "don_gia": ct.don_gia,
                    "thanh_tien": ct.thanh_tien
                })

        result.append(InvoiceOut(
            id=inv.id,
            ma_hoa_don=inv.ma_hoa_don,
            phieu_sua_chua_id=inv.phieu_sua_chua_id,
            ma_phieu=p.ma_phieu if p else "N/A",
            ten_khach_hang=p.khach_hang.ho_ten if (p and p.khach_hang) else "N/A",
            so_dien_thoai=p.khach_hang.so_dien_thoai if (p and p.khach_hang) else "N/A",
            model_may=p.thiet_bi.model_may if (p and p.thiet_bi) else "N/A",
            thu_ngan_id=inv.thu_ngan_id,
            thu_ngan_ten=inv.thu_ngan.ho_ten if inv.thu_ngan else "Thu ngân",
            tong_tien=inv.tong_tien,
            phuong_thuc_tt=inv.phuong_thuc_tt,
            trang_thai_tt=inv.trang_thai_tt,
            ngay_thanh_toan=inv.ngay_thanh_toan.strftime("%d/%m/%Y %H:%M") if inv.ngay_thanh_toan else None,
            chi_tiet_items=items
        ))
    return result

@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Xem chi tiết một hóa đơn."""
    inv = db.query(HoaDon).filter(HoaDon.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Không tìm thấy hóa đơn.")
    p = inv.phieu_sua_chua
    items = []
    if p:
        for ct in p.chi_tiet:
            ten_muc = ct.linh_kien.ten_linh_kien if ct.linh_kien else (ct.dich_vu.ten_dich_vu if ct.dich_vu else "N/A")
            items.append({
                "ten_muc": ten_muc,
                "so_luong": ct.so_luong,
                "don_gia": ct.don_gia,
                "thanh_tien": ct.thanh_tien
            })

    return InvoiceOut(
        id=inv.id,
        ma_hoa_don=inv.ma_hoa_don,
        phieu_sua_chua_id=inv.phieu_sua_chua_id,
        ma_phieu=p.ma_phieu if p else "N/A",
        ten_khach_hang=p.khach_hang.ho_ten if (p and p.khach_hang) else "N/A",
        so_dien_thoai=p.khach_hang.so_dien_thoai if (p and p.khach_hang) else "N/A",
        model_may=p.thiet_bi.model_may if (p and p.thiet_bi) else "N/A",
        thu_ngan_id=inv.thu_ngan_id,
        thu_ngan_ten=inv.thu_ngan.ho_ten if inv.thu_ngan else "Thu ngân",
        tong_tien=inv.tong_tien,
        phuong_thuc_tt=inv.phuong_thuc_tt,
        trang_thai_tt=inv.trang_thai_tt,
        ngay_thanh_toan=inv.ngay_thanh_toan.strftime("%d/%m/%Y %H:%M") if inv.ngay_thanh_toan else None,
        chi_tiet_items=items
    )

@router.post("", response_model=InvoiceOut, status_code=status.HTTP_201_CREATED)
def create_invoice(
    req: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "ThuNgan"]))
):
    """Lập hóa đơn thanh toán cho phiếu sửa chữa và tự động tạo bảo hành điện tử cho các linh kiện thay thế."""
    p = db.query(PhieuSuaChua).filter(PhieuSuaChua.id == req.phieu_sua_chua_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu sửa chữa.")

    existing_inv = db.query(HoaDon).filter(HoaDon.phieu_sua_chua_id == p.id).first()
    if existing_inv:
        raise HTTPException(status_code=400, detail="Phiếu sửa chữa này đã được lập hóa đơn.")

    # Tính tổng tiền
    total = sum(ct.thanh_tien for ct in p.chi_tiet) if p.chi_tiet else (p.tong_tien_du_kien or 0.0)

    # Sinh mã hóa đơn
    today_str = datetime.utcnow().strftime("%Y%m%d")
    count_today = db.query(HoaDon).filter(HoaDon.ma_hoa_don.like(f"HD-{today_str}-%")).count()
    ma_hoa_don = f"HD-{today_str}-{count_today + 1:03d}"

    inv = HoaDon(
        ma_hoa_don=ma_hoa_don,
        phieu_sua_chua_id=p.id,
        thu_ngan_id=current_user.id,
        tong_tien=total,
        phuong_thuc_tt=req.phuong_thuc_tt,
        trang_thai_tt="DaThanhToan",
        ngay_thanh_toan=datetime.utcnow()
    )
    db.add(inv)

    # Cập nhật trạng thái phiếu sửa chữa
    p.trang_thai = "DaThanhToan"

    # Tự động tạo phiếu bảo hành cho tất cả linh kiện được thay thế
    for ct in p.chi_tiet:
        if ct.linh_kien_id and ct.linh_kien:
            lk = ct.linh_kien
            thoi_han = lk.thoi_han_bao_hanh_thang or 6
            count_bh = db.query(BaoHanh).count()
            ma_bh = f"BH-{today_str}-{count_bh + 1:03d}"
            bh = BaoHanh(
                ma_bao_hanh=ma_bh,
                phieu_sua_chua_id=p.id,
                linh_kien_id=lk.id,
                ngay_bat_dau=datetime.utcnow(),
                ngay_het_han=datetime.utcnow() + timedelta(days=thoi_han * 30),
                dieu_kien_bh=f"Bảo hành chính hãng {thoi_han} tháng cho {lk.ten_linh_kien}. Không bảo hành rơi vỡ, ngâm nước.",
                trang_thai="ConHan"
            )
            db.add(bh)

    db.commit()
    db.refresh(inv)

    items = []
    for ct in p.chi_tiet:
        ten_muc = ct.linh_kien.ten_linh_kien if ct.linh_kien else (ct.dich_vu.ten_dich_vu if ct.dich_vu else "N/A")
        items.append({
            "ten_muc": ten_muc,
            "so_luong": ct.so_luong,
            "don_gia": ct.don_gia,
            "thanh_tien": ct.thanh_tien
        })

    return InvoiceOut(
        id=inv.id,
        ma_hoa_don=inv.ma_hoa_don,
        phieu_sua_chua_id=inv.phieu_sua_chua_id,
        ma_phieu=p.ma_phieu,
        ten_khach_hang=p.khach_hang.ho_ten if p.khach_hang else "N/A",
        so_dien_thoai=p.khach_hang.so_dien_thoai if p.khach_hang else "N/A",
        model_may=p.thiet_bi.model_may if p.thiet_bi else "N/A",
        thu_ngan_id=inv.thu_ngan_id,
        thu_ngan_ten=current_user.ho_ten,
        tong_tien=inv.tong_tien,
        phuong_thuc_tt=inv.phuong_thuc_tt,
        trang_thai_tt=inv.trang_thai_tt,
        ngay_thanh_toan=inv.ngay_thanh_toan.strftime("%d/%m/%Y %H:%M"),
        chi_tiet_items=items
    )
