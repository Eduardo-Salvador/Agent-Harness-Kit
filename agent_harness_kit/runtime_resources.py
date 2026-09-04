"""Read and materialize hash-verified runtime resources."""

from __future__ import annotations

import os
import uuid
import zipfile
from pathlib import Path, PurePosixPath


TEMPLATE_PACK = Path("resources/templates.zip")


class RuntimeResourceError(RuntimeError):
    """Raised when a packaged resource cannot be resolved safely."""


def _safe_member(raw: str) -> str:
    candidate = PurePosixPath(raw)
    if (
        not raw
        or candidate.is_absolute()
        or candidate.as_posix() != raw
        or ".." in candidate.parts
        or len(candidate.parts) != 1
        or not raw.casefold().endswith(".md")
    ):
        raise RuntimeResourceError(f"unsafe template member: {raw!r}")
    return raw


def _template_key(name: str) -> str:
    value = name.strip().replace("_", "-")
    if not value or "/" in value or "\\" in value:
        raise RuntimeResourceError(f"unsafe template name: {name!r}")
    candidate = PurePosixPath(value)
    if candidate.suffix and candidate.suffix.casefold() != ".md":
        raise RuntimeResourceError(f"unsafe template name: {name!r}")
    return candidate.stem.casefold()


def _pack_path(kit_root: Path) -> Path:
    path = kit_root.expanduser().resolve() / TEMPLATE_PACK
    if not path.is_file():
        raise RuntimeResourceError(f"template pack is missing: {path}")
    return path


def _template_members(kit_root: Path) -> dict[str, str]:
    try:
        with zipfile.ZipFile(_pack_path(kit_root)) as archive:
            members: dict[str, str] = {}
            for raw in archive.namelist():
                member = _safe_member(raw)
                key = Path(member).stem.replace("_", "-").casefold()
                if key in members:
                    raise RuntimeResourceError(f"duplicate template identity: {key}")
                members[key] = member
            return members
    except (OSError, zipfile.BadZipFile) as exc:
        raise RuntimeResourceError(f"template pack is unreadable: {exc}") from exc


def template_names(kit_root: Path) -> list[str]:
    return sorted(key.upper() for key in _template_members(kit_root))


def template_bytes(kit_root: Path, name: str) -> bytes:
    key = _template_key(name)
    member = _template_members(kit_root).get(key)
    if member is None:
        raise RuntimeResourceError(f"unknown template: {name}")
    try:
        with zipfile.ZipFile(_pack_path(kit_root)) as archive:
            return archive.read(member)
    except (OSError, KeyError, zipfile.BadZipFile) as exc:
        raise RuntimeResourceError(f"template pack is unreadable: {exc}") from exc


def scaffold_template(
    kit_root: Path,
    name: str,
    output: Path,
    *,
    host_root: Path,
    force: bool = False,
) -> Path:
    """Atomically materialize one template inside the host project."""
    host = host_root.expanduser().resolve()
    requested = output.expanduser()
    if not requested.is_absolute():
        requested = host / requested
    if requested.is_symlink():
        raise RuntimeResourceError(f"template output must not be a symlink: {requested}")
    target = requested.resolve()
    try:
        target.relative_to(host)
    except ValueError as exc:
        raise RuntimeResourceError(f"template output escapes host project: {target}") from exc
    if target.exists() and not force:
        raise FileExistsError(f"template output already exists: {target}")
    if target.exists() and (target.is_symlink() or not target.is_file()):
        raise RuntimeResourceError(f"template output must be a regular file: {target}")

    data = template_bytes(kit_root, name)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.parent / f".{target.name}.{uuid.uuid4().hex[:8]}.tmp"
    try:
        temporary.write_bytes(data)
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
    return target
