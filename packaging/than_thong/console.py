"""Console — chay lenh tu terminal, toan bo tieng Viet."""
import sys, json, os
from than_thong.router import route
from than_thong.gate import check_tool
from than_thong.logger import log


HELP_TEXT = """
Than Thong - Cong Kiem Soat May Tinh
=====================================

LENH CO SAN (khong can Python):

  kiem-tra-cong    Kiem tra cong (gate) dang hoat dong
  trang-thai       Trang thai he thong
  thong-tin        Thong tin may tinh chi tiet
  don-dep          Don dep file tam Windows
  kiem-tra-bao-mat Kiem tra bao may tinh
  status           (English) System status
  info             (English) System info
  win-cleanup      (English) Clean temp files
  win-audit        (English) Security audit
  gate-test        (English) Test gate policies

LENH CAN PYTHON:
  full-dashboard   Bang dieu khien day du
  dashboard        Bang dieu khien ops
  inventory        Kiem ke workspace
  domains          Kiem tra domain

CHE DO:
  console / dieu-khien  Mo giao dien dong lenh
  gui                   Mo app system tray (mac dinh)
  help, ?               Tro giup nay
  exit, quit            Thoat
"""


def _out(data: str):
    """Write UTF-8 bytes to stdout via raw file descriptor."""
    try:
        os.write(1, data.encode('utf-8') + b'\n')
    except Exception:
        try:
            sys.stdout.buffer.write(data.encode('utf-8') + b'\n')
            sys.stdout.buffer.flush()
        except Exception:
            try:
                print(data, flush=True)
            except Exception:
                pass


def run_interactive():
    """Vong lap console tuong tac."""
    _out("=== Than Thong - Dieu Khien ===")
    _out("Go 'help' de xem lenh, 'exit' de thoat")
    while True:
        try:
            line = input("than-thong> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line in ("exit", "quit", "thoat"):
            break
        if line in ("help", "?"):
            print(HELP_TEXT)
            continue
        parts = line.split()
        cmd = parts[0]
        args = parts[1:]
        result = route(cmd, *args)
        _out(json.dumps(result, indent=2, ensure_ascii=False))


def run_once(command: str, *args):
    """Chay 1 lenh, in ket qua."""
    result = route(command, *args)
    _out(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("thanh_cong") else 1
