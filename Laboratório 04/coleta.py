import sys
import time
import zipfile
import urllib.request
from urllib.error import HTTPError, URLError
from pathlib import Path

URL = "https://download.inep.gov.br/microdados/microdados_enem_2024.zip"
ZIP_NAME = "microdados_enem_2024.zip"
EXTRACT_DIR = Path("microdados_enem_2024")
CHUNK_SIZE = 1024 * 1024
DELETE_ZIP_AFTER_EXTRACT = True

def get_remote_size(url: str) -> int | None:
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=30) as resp:
            cl = resp.headers.get("Content-Length")
            return int(cl) if cl is not None else None
    except Exception:
        return None

def stream_download(url: str, dst: Path, resume: bool = True) -> None:
    dst = Path(dst)
    tmp = dst.with_suffix(".part")
    remote_size = get_remote_size(url)

    already = tmp.stat().st_size if tmp.exists() else 0
    headers = {}
    mode = "wb"
    if resume and remote_size and already > 0 and already < remote_size:
        headers["Range"] = f"bytes={already}-"
        mode = "ab"
        print(f"Retomando download a partir de {already:,} bytes...")
    elif dst.exists():
        if remote_size and dst.stat().st_size == remote_size:
            print("Arquivo já baixado. Pulando download.")
            return
        else:
            dst.unlink(missing_ok=True)
            tmp.unlink(missing_ok=True)

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp, open(tmp, mode) as f:
            status = getattr(resp, "status", None)
            if status == 200 and mode == "ab":
                f.close()
                tmp.unlink(missing_ok=True)
                print("Servidor não aceitou Range. Recomeçando do zero...")
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=60) as resp2, open(tmp, "wb") as f2:
                    _download_loop(resp2, f2, remote_size)
            else:
                _download_loop(resp, f, remote_size, initial_bytes=already)
    except (HTTPError, URLError) as e:
        print(f"Erro de download: {e}")
        raise

    tmp.rename(dst)
    print(f"Download concluído: {dst} ({dst.stat().st_size:,} bytes)")

def _download_loop(resp, file_obj, total_size: int | None, initial_bytes: int = 0):
    downloaded = initial_bytes
    start = time.time()
    while True:
        chunk = resp.read(CHUNK_SIZE)
        if not chunk:
            break
        file_obj.write(chunk)
        downloaded += len(chunk)
        _print_progress(downloaded, total_size, start)

    print()

def _print_progress(downloaded: int, total_size: int | None, start_time: float):
    if total_size:
        pct = downloaded / total_size * 100
        elapsed = max(time.time() - start_time, 1e-6)
        speed = downloaded / elapsed
        sys.stdout.write(
            f"\rBaixado: {downloaded:,}/{total_size:,} bytes ({pct:5.1f}%) | "
            f"Velocidade: {speed/1_048_576:6.2f} MB/s"
        )
        sys.stdout.flush()
    else:
        sys.stdout.write(f"\rBaixado: {downloaded:,} bytes")
        sys.stdout.flush()

def validate_zip(zip_path: Path) -> None:
    print("Validando ZIP...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        bad = zf.testzip()
        if bad is not None:
            raise RuntimeError(f"Arquivo ZIP corrompido. Primeiro arquivo com erro: {bad}")
    print("ZIP válido.")

def unzip(zip_path: Path, extract_to: Path) -> None:
    extract_to.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_to)
    print(f"Extraído para: {extract_to.resolve()}")

def main():
    zip_path = Path(ZIP_NAME)

    print(f"Baixando ENEM 2024 de:\n{URL}\n")
    stream_download(URL, zip_path, resume=True)
    validate_zip(zip_path)
    unzip(zip_path, EXTRACT_DIR)

    if DELETE_ZIP_AFTER_EXTRACT:
        zip_path.unlink(missing_ok=True)
        print("ZIP removido após extração.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\nFalha: {e}")
        sys.exit(2)