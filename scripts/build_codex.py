#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Required Notice: Copyright (c) 2026 Hyeonoh Hur (https://github.com/H-Hur/study-kit)
"""Build the Codex edition from the maintained Claude Code procedures (stdlib only)."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugins/study-kit"
NAME = "study-kit-codex"
OUTPUT = ROOT / "plugins" / NAME
SOURCE_FOLDERS = ("skills", "agents", "commands", "docs", "templates", "licenses")
SOURCE_SUFFIXES = frozenset({".md", ".html", ".txt"})
LOCAL_FILE_STEMS = frozenset({"credentials", "secrets", "id_rsa", "id_dsa",
                              "id_ecdsa", "id_ed25519"})
LINK = re.compile(r"(\[[^\]\n]*\]\()([^\s)]+)(\))")
EXPECTED_SKILLS = frozenset({
    "learner-intake", "source-index", "curriculum-design", "textbook-authoring",
    "textbook-revision", "textbook-publish", "exam-study",
    "study-start", "study-session", "study-review", "study-publish",
    "source-scout", "drill-designer", "textbook-auditor", "comprehension-auditor",
})


def require_plain_path(path: Path, root: Path) -> None:
    """Reject linked package paths before reading or writing through them."""
    try:
        relative = path.absolute().relative_to(root.absolute())
    except ValueError:
        raise ValueError(f"Package path is outside its root: {path}") from None
    for current in (root, *(root / Path(*relative.parts[:i])
                             for i in range(1, len(relative.parts) + 1))):
        try:
            info = current.lstat()
        except FileNotFoundError:
            continue
        if (stat.S_ISLNK(info.st_mode) or
                getattr(info, "st_file_attributes", 0) &
                getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)):
            raise ValueError(f"Linked package path requires review: {current}")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Package path is outside its root: {path}")


def checked_tree(folder: Path, root: Path):
    """Walk without descending into a symlink or Windows reparse point."""
    require_plain_path(folder, root)
    if not folder.exists():
        return
    for path in sorted(folder.iterdir()):
        require_plain_path(path, root)
        yield path
        if path.is_dir():
            yield from checked_tree(path, root)


def source_files():
    """Fail closed on local files; supported text still needs content review."""
    require_plain_path(SOURCE, ROOT)
    for folder in SOURCE_FOLDERS:
        for path in checked_tree(SOURCE / folder, SOURCE):
            relative = path.relative_to(SOURCE)
            if any(part.startswith(".") for part in relative.parts):
                raise ValueError(f"Hidden/local source path requires review: {relative}")
            if path.is_dir():
                continue
            if (not path.is_file() or path.suffix not in SOURCE_SUFFIXES or
                    path.stem.casefold() in LOCAL_FILE_STEMS):
                raise ValueError(f"Unsupported/local source file requires review: {relative}")
            yield path


def release_version(manifest: dict) -> str:
    version = manifest.get("version")
    if (not isinstance(version, str) or len(version) > 128 or
            not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
                             r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?", version)):
        raise ValueError("Invalid release version; expected a safe semantic version")
    return version


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"Source changed; review the Codex adaptation for: {old!r}")
    return text.replace(old, new, 1)


def destination(path: Path) -> Path:
    relative = path.relative_to(SOURCE)
    if relative.parts[0] in {"agents", "commands"}:
        return Path("skills") / path.stem / "SKILL.md"
    if relative == Path("templates/PROJECT-CLAUDE.md"):
        return Path("templates/PROJECT-AGENTS.md")
    if relative == Path("docs/runtime.md"):
        return Path("docs/codex-runtime.md")
    return relative


def rewrite_links(text: str, source_path: Path, target_path: Path) -> str:
    def rewrite(match: re.Match) -> str:
        url, separator, anchor = match[2].partition("#")
        if not url or ":" in url or url.startswith("/"):
            return match[0]
        linked = (source_path.parent / url).resolve()
        if not linked.is_file() or not linked.is_relative_to(SOURCE):
            return match[0]  # Study-project links in templates are filled on use.
        relative = os.path.relpath(destination(linked), target_path.parent)
        return match[1] + Path(relative).as_posix() + separator + anchor + match[3]

    return LINK.sub(rewrite, text)


def adapt(text: str, source_path: Path) -> str:
    relative = source_path.relative_to(SOURCE).as_posix()
    if relative.startswith(("commands/", "agents/")):
        _, header, body = text.split("---", 2)
        fields = dict(line.split(":", 1) for line in header.strip().splitlines())
        text = (f"---\nname: {source_path.stem}\n"
                f"description:{fields['description']}\n---" + body)
    if relative == "commands/study-start.md":
        text = replace_once(text,
            '1. Read the kit\'s method (`${CLAUDE_PLUGIN_ROOT}/docs/method.md`) to confirm the whole\n'
            '   sequence. Kit files are always addressed through `${CLAUDE_PLUGIN_ROOT}` — a bare\n'
            '   `docs/` here would mean the study project\'s own `docs/`, which is a different folder.',
            '1. Read the kit\'s [method](../../docs/method.md) to confirm the whole sequence.\n'
            '   Resolve this link from this installed skill. Choose a separate study project\n'
            '   before writing any learner artifacts; never write them into the kit or its cache.')
        text = replace_once(text,
            '4. Stand up the project skeleton — take `PROJECT-CLAUDE.md`, `worklog.md`, and\n'
            '   `toolbox-log.md` from `${CLAUDE_PLUGIN_ROOT}/templates/`, fill them in, and create\n'
            '   `docs/notes/` and `docs/reports/` (these two in the study project, not in the kit).',
            '4. Stand up the project skeleton from the bundled\n'
            '   [project instructions](../../templates/PROJECT-AGENTS.md),\n'
            '   [work log](../../templates/worklog.md),\n'
            '   [toolbox log](../../templates/toolbox-log.md), and\n'
            '   [inbox README](../../templates/inbox-README.md). Fill them in as `AGENTS.md`,\n'
            '   `docs/worklog.md`, `docs/toolbox-log.md`, and `docs/inbox/README.md` in the\n'
            '   study project. Copy the [style rules](../textbook-authoring/references/style-rules.md)\n'
            '   to `docs/study-kit-style-rules.md`. Create `docs/notes/` and `docs/reports/` there.')
    elif relative == "commands/study-session.md":
        text += "\nUse a session number supplied by the learner; otherwise determine the next session from the curriculum and work log.\n"
    elif relative == "agents/comprehension-auditor.md":
        text = replace_once(text,
            '1. **Session conversation records**: `~/.claude/projects/<project path with slashes replaced\n'
            '   by hyphens>/*.jsonl` — skim the learner\'s utterances in recent sessions. Filtering the\n'
            '   jsonl down to user messages is enough.',
            '1. **Session conversation records**: use the current conversation or an export\n'
            '   supplied for this study project. Skim the learner\'s utterances in recent sessions.\n'
            '   If those records are unavailable, use the notes and recovered questions below\n'
            '   and state that the conversation evidence is incomplete. Do not infer missing quotes.')
    elif relative == "templates/PROJECT-CLAUDE.md":
        text = replace_once(text,
            '`${CLAUDE_PLUGIN_ROOT}/skills/textbook-authoring/references/style-rules.md`',
            '`docs/study-kit-style-rules.md` (copied from the kit when the project was created)')
        text += ('\n## Study Kit in Codex\n\n'
                 'Use the installed Study Kit skills for study-start, study-session,\n'
                 'study-review, and study-publish. Read the runtime notes linked from\n'
                 'the installed skill before work; do not guess an old cache path.\n'
                 'Keep intake and learner decisions in the main conversation. Delegate\n'
                 'bounded specialist work through available subagent tools with the\n'
                 'role procedure, study directory, inputs, write scope, and expected\n'
                 'report. Collect the result before integrating it. If delegation is\n'
                 'unavailable, execute that procedure directly in manageable batches.\n')
    return text


def link_skill_mentions(text: str, target: Path) -> str:
    """Make bare procedure references executable by reading the installed skill."""
    names = {p.parent.name for p in (SOURCE / "skills").glob("*/SKILL.md")}
    names.update(p.stem for folder in ("agents", "commands")
                 for p in (SOURCE / folder).glob("*.md"))
    pattern = r"(?<!\[)`(" + "|".join(sorted(names)) + r")`(?!\])"

    def link(match: re.Match) -> str:
        dest = Path("skills") / match[1] / "SKILL.md"
        if dest == target:
            return match[0]
        path = Path(os.path.relpath(dest, target.parent)).as_posix()
        return f"[{match[0]}]({path})"

    # Never change code samples or skill discovery frontmatter.
    prefix = ""
    if text.startswith("---\n"):
        _, header, text = text.split("---", 2)
        prefix = f"---{header}---"
    chunks = re.split(r"(^```[^\n]*\n.*?^```[^\n]*$)", text,
                      flags=re.MULTILINE | re.DOTALL)
    return prefix + "".join(chunk if i % 2 else re.sub(pattern, link, chunk)
                            for i, chunk in enumerate(chunks))


def render() -> dict[Path, bytes]:
    require_plain_path(SOURCE, ROOT)
    for path in (SOURCE / ".claude-plugin/plugin.json", SOURCE / "LICENSE",
                 ROOT / "codex/runtime.md", ROOT / "codex/interface.json"):
        require_plain_path(path, ROOT)
    validate_catalogs()
    manifest = json.loads((SOURCE / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    release_version(manifest)
    files = {}
    for path in source_files():
        target = destination(path)
        if target in files:
            raise ValueError(f"Duplicate Codex skill or file: {target}")
        if path == SOURCE / "docs/runtime.md":
            files[target] = (ROOT / "codex/runtime.md").read_bytes()
            continue
        if path.suffix == ".md":
            # Rebase existing links before adding links already written for the target.
            value = rewrite_links(path.read_text(encoding="utf-8"), path, target)
            value = adapt(value, path)
            value = link_skill_mentions(value, target)
            if path.parent == SOURCE / "agents":
                _, header, body = value.split("---", 2)
                note = ('\n\n## Codex role execution\n\n'
                        'This is a specialist procedure, not a registered custom agent.\n'
                        'From the main conversation, follow the runtime notes for bounded\n'
                        'delegation, required inputs, permitted writes, and result collection.\n'
                        'If already assigned this role as a subagent, execute it here and\n'
                        'return the result; do not delegate this same role again. If subagents\n'
                        'are unavailable, perform it directly with the same restrictions.\n')
                value = f"---{header}---{note}{body}"
            files[target] = value.encode()
        else:
            files[target] = path.read_bytes()

    manifest.update(
        name=NAME,
        description=("Study Kit Personal, a personal adaptation of Hyeonoh Hur's Study Kit. "
                     "Build focused study materials and prepare for exams from verified "
                     "course sources, with answer-writing practice and reusable preferences. "
                     f"Includes {len(EXPECTED_SKILLS)} Codex skills."),
        skills="./skills/",
        homepage=manifest.get("homepage", "https://github.com/H-Hur/study-kit"),
        repository=manifest.get("repository", "https://github.com/H-Hur/study-kit"),
        interface=json.loads((ROOT / "codex/interface.json").read_text(encoding="utf-8")),
    )
    files[Path(".codex-plugin/plugin.json")] = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode()
    files[Path("LICENSE")] = (SOURCE / "LICENSE").read_bytes()
    validate(files)
    return files


def validate_catalogs() -> None:
    for catalog_path, plugin_name in (
        (ROOT / ".claude-plugin/marketplace.json", "study-kit"),
        (ROOT / ".agents/plugins/marketplace.json", NAME),
    ):
        require_plain_path(catalog_path, ROOT)
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        if catalog.get("name") != "study-kit":
            raise ValueError(f"Installation instructions require marketplace name study-kit: {catalog_path}")
        entries = [entry for entry in catalog["plugins"] if entry.get("name") == plugin_name]
        if len(entries) != 1:
            raise ValueError(f"Expected one entry for {plugin_name} in {catalog_path}")
        entry = entries[0]
        source = entry["source"]
        if isinstance(source, dict):
            if source.get("source") != "local":
                raise ValueError(f"Expected a bundled local source in {catalog_path}")
            source = source["path"]
        if source != f"./plugins/{plugin_name}":
            raise ValueError(f"Marketplace points at the wrong package: {catalog_path}")
        if plugin_name == NAME:
            if entry.get("policy") != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
                raise ValueError("Review the Codex installation policy before changing it")
            if entry.get("category") != "Productivity":
                raise ValueError("Codex marketplace and interface categories must agree")


def validate(files: dict[Path, bytes]) -> None:
    for required in ("LICENSE", "licenses/PolyForm-Noncommercial-1.0.0.txt",
                     "licenses/CC-BY-NC-SA-4.0.txt"):
        if not files.get(Path(required)):
            raise ValueError(f"Missing bundled license: {required}")
    skills = {p for p in files if p.name == "SKILL.md"}
    expected = {Path("skills") / name / "SKILL.md" for name in EXPECTED_SKILLS}
    if skills != expected:
        missing = sorted(path.as_posix() for path in expected - skills)
        unexpected = sorted(path.as_posix() for path in skills - expected)
        raise ValueError(f"Unexpected skill set; missing={missing}, unexpected={unexpected}; "
                         "review the release metadata")
    for path, data in files.items():
        if path.suffix != ".md":
            continue
        text = data.decode()
        if any(marker in text for marker in
               ("CLAUDE_PLUGIN_ROOT", "~/.claude/", "PROJECT-CLAUDE.md", "/study-kit:")):
            raise ValueError(f"Unconverted Claude dependency in {path}")
        if path.name == "SKILL.md":
            header = text.split("---", 2)[1]
            if f"name: {path.parent.name}\n" not in header or "\ndescription:" not in header:
                raise ValueError(f"Invalid skill frontmatter: {path}")
            if re.search(r"^(tools|argument-hint|model):", header, re.MULTILINE):
                raise ValueError(f"Claude frontmatter in {path}")
            if "(../../docs/codex-runtime.md)" not in text:
                raise ValueError(f"Missing host runtime instructions: {path}")
            if (SOURCE / "agents" / f"{path.parent.name}.md").is_file():
                if "## Codex role execution" not in text:
                    raise ValueError(f"Missing specialist execution contract: {path}")
        # Template links intentionally refer to the future learner project.
        if "templates" in path.parts:
            continue
        for match in LINK.finditer(text):
            link = match[2].split("#")[0]
            if not link or ":" in link or link.startswith("/"):
                continue
            resolved = Path(os.path.normpath(path.parent / link))
            if resolved not in files:
                raise ValueError(f"Broken bundled link: {path} -> {link}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the committed package differs from the sources")
    parser.add_argument("--archive", action="store_true", help="Also write a reproducible ZIP under dist/")
    args = parser.parse_args(argv)
    files = render()
    require_plain_path(OUTPUT, ROOT)
    existing = {p.relative_to(OUTPUT): p for p in checked_tree(OUTPUT, OUTPUT) if p.is_file()}
    stale = sorted(set(existing) - set(files))
    changed = [p for p, data in files.items() if p not in existing or existing[p].read_bytes() != data]
    if args.check:
        if stale or changed:
            print("Codex package is out of date; run python3 scripts/build_codex.py", file=sys.stderr)
            for path in stale + changed:
                print(f"  {path}", file=sys.stderr)
            return 1
    else:
        if stale:
            raise ValueError(f"Unexpected files in generated package; review and remove them before rebuilding: {stale}")
        for path in changed:
            target = OUTPUT / path
            require_plain_path(target, OUTPUT)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(files[path])
    print(f"Codex package {'checked' if args.check else 'built'}: "
          f"{len(files)} files, {len(EXPECTED_SKILLS)} skills")
    if args.archive:
        version = release_version(json.loads(files[Path(".codex-plugin/plugin.json")]))
        archive = ROOT / "dist" / f"{NAME}-{version}.zip"
        require_plain_path(archive, ROOT)
        archive.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
            for path, data in sorted(files.items()):
                entry = zipfile.ZipInfo(f"{NAME}/{path.as_posix()}", (2026, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                bundle.writestr(entry, data)
        print(f"Archive: {archive}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as error:
        print(f"Build failed: {error}", file=sys.stderr)
        raise SystemExit(1)
