"""Cong (Gate) — kiem tra billing/local-first truoc khi cho qua."""
from than_thong.config import config
from than_thong.notifier import notifier
from than_thong.logger import log


class GateError(Exception):
    pass


class BillingBlock(GateError):
    """Bi chan vi billing risk."""
    pass


class ToolBlock(GateError):
    """Cong cu bi chan vi chinh sach."""
    pass


def kiem_tra_cong_cu(ten_cong_cu: str) -> bool:
    """Kiem tra cong cu co duoc phep chay khong. True = cho qua."""
    blocked = config.blocked_tools
    if ten_cong_cu in blocked:
        msg = "DA CHAN: %s - vi pham chinh sach offline-first/khong-billing" % ten_cong_cu
        log.warning(msg)
        notifier.canh_bao_chan(ten_cong_cu)
        return False
    log.debug("CHO QUA: %s", ten_cong_cu)
    notifier.canh_bao_qua_cong(ten_cong_cu)
    return True


def kiem_tra_billing(nha_cung_cap: str = None) -> bool:
    """Kiem tra co billing risk khong. True = an toan."""
    if config.get("no_billing", True) and nha_cung_cap:
        msg = "DA CHAN: billing risk - provider=%s" % nha_cung_cap
        log.warning(msg)
        return False
    return True


def kiem_tra_uu_tien_local(duong_dan: str = None) -> bool:
    """Kiem tra uu tien local. True = OK."""
    if config.get("local_first", True) and duong_dan:
        if duong_dan.startswith(("http://", "https://", "ftp://")):
            msg = "DA CHAN: duong dan khong local - %s" % duong_dan
            log.warning(msg)
            return False
    return True


# English aliases for backward compatibility
check_tool = kiem_tra_cong_cu
check_billing = kiem_tra_billing
check_local_first = kiem_tra_uu_tien_local
