import hashlib
import os
from pathlib import Path
import shutil
import sys


def sha256_digest(path):
    digest = hashlib.sha256()
    with path.open("rb") as image_file:
        for chunk in iter(lambda: image_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    source = Path(__file__).resolve().parent / "news-image-20261121.png"
    if not source.is_file():
        print(f"Error: missing image file: {source}", file=sys.stderr)
        return 1

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination = output_dir / source.name
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        byte_count = destination.stat().st_size
        source_digest = sha256_digest(source)
        copied_digest = sha256_digest(destination)
    except OSError as error:
        print(
            f"Error: could not copy or verify {source.name} to {destination}: {error}",
            file=sys.stderr,
        )
        return 1

    if source_digest != copied_digest:
        print(
            f"Error: SHA-256 mismatch for {destination}: "
            f"source={source_digest}, copy={copied_digest}",
            file=sys.stderr,
        )
        return 1

    print(f"Copied {byte_count} bytes to {destination} (SHA-256: {copied_digest[:12]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
