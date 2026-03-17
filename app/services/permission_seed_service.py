from sqlalchemy.orm import Session
from app.db.models.auth import Permission
from app.constants.permissions import PERMISSIONS_SEED


def sync_permissions(db: Session) -> None:
    """Đảm bảo DB chứa đầy đủ các permission trong PERMISSIONS_SEED.

    - Nếu chưa có -> tạo mới
    - Nếu đã có -> cập nhật description (nếu khác)
    - Không xóa permission dư, chỉ đồng bộ những gì định nghĩa trong seed
    """
    existing_perms = {p.code: p for p in db.query(Permission).all()}
    for item in PERMISSIONS_SEED:
        code = item["code"]
        desc = item.get("description")
        if code in existing_perms:
            perm = existing_perms[code]
            if perm.description != desc:
                perm.description = desc
        else:
            perm = Permission(code=code, description=desc)
            db.add(perm)
    db.commit()
