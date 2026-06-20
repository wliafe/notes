from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict, deque
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "95-Maintenance/Legacy/legacy-manifest-v2.json"
TOPIC_MERGE_MANIFEST = ROOT / "95-Maintenance/Legacy/topic-merge-manifest.json"
ASSET_SUFFIXES = {".png", ".gif", ".jpg", ".jpeg", ".webp", ".svg"}
COMMON_FIELDS = {"title", "aliases", "type", "created", "tags"}
TYPE_FIELDS = {
    "note": {"area", "status", "review"},
    "moc": {"area", "status", "review"},
    "project": {"status", "started", "deadline"},
    "paper": {"status", "authors", "year", "venue", "url", "code", "projects", "topics"},
    "experiment": {
        "status",
        "project",
        "dataset",
        "model",
        "git_commit",
        "config",
        "result",
    },
    "idea": {"status", "projects"},
    "reading": {"status", "source", "projects"},
    "meeting": {"project", "date", "participants"},
    "daily": {"date"},
}
VALID_STATUS = {
    "note": {"active", "archived"},
    "moc": {"active", "archived"},
    "project": {"active", "paused", "completed", "archived"},
    "paper": {"unread", "reading", "read", "skipped"},
    "experiment": {"planned", "running", "completed", "failed", "abandoned"},
    "idea": {"seed", "exploring", "validated", "discarded"},
    "reading": {"queued", "reading", "done"},
}
VALID_REVIEW = {"pending", "reviewed"}
REQUIRED_TEMPLATES = {
    "Daily",
    "Project",
    "Paper",
    "Experiment",
    "Idea",
    "Reading",
    "Meeting",
    "Knowledge Note",
    "MOC",
}
REQUIRED_PATHS = {
    "首页.md",
    "00-Inbox/Inbox.md",
    "10-Daily/Daily.md",
    "20-Projects/Projects.md",
    "30-Research/Research.md",
    "30-Research/Papers/Papers.md",
    "30-Research/Ideas/Ideas.md",
    "30-Research/Experiments/Experiments.md",
    "30-Research/Reading/Reading.md",
    "40-Knowledge/Knowledge.md",
    "40-Knowledge/Computer Vision/Computer Vision.md",
    "40-Knowledge/Deep Learning/Deep Learning.md",
    "40-Knowledge/Mathematics/Mathematics.md",
    "40-Knowledge/Computer Science/Computer Science.md",
    "40-Knowledge/Programming/Programming.md",
    "40-Knowledge/Software Engineering/Software Engineering.md",
    "40-Knowledge/Developer Tools/Developer Tools.md",
    "40-Knowledge/Systems/Systems.md",
    "40-Knowledge/Cybersecurity/Cybersecurity.md",
    "40-Knowledge/Mac/Mac.md",
    "95-Maintenance/待复核.md",
    "95-Maintenance/整理规范.md",
    "95-Maintenance/第二轮迁移报告.md",
    "95-Maintenance/主题合并报告.md",
    "95-Maintenance/Legacy/topic-merge-manifest.json",
    "98-Archive/Archive.md",
}
MERGED_PARENT_MOCS = {
    "40-Knowledge/Computer Science/数据结构实现.md":
        "40-Knowledge/Computer Science/Computer Science.md",
    "40-Knowledge/Deep Learning/深度学习.md":
        "40-Knowledge/Deep Learning/Deep Learning.md",
    "40-Knowledge/Developer Tools/pip.md":
        "40-Knowledge/Developer Tools/Developer Tools.md",
    "40-Knowledge/Developer Tools/shell.md":
        "40-Knowledge/Developer Tools/Developer Tools.md",
    "40-Knowledge/Programming/Assembly.md":
        "40-Knowledge/Programming/Programming.md",
    "40-Knowledge/Programming/C.md":
        "40-Knowledge/Programming/Programming.md",
    "40-Knowledge/Programming/Python.md":
        "40-Knowledge/Programming/Programming.md",
    "40-Knowledge/Software Engineering/Backend/Spring.md":
        "40-Knowledge/Software Engineering/Backend/Backend.md",
    "40-Knowledge/Software Engineering/Backend/SpringSecurity.md":
        "40-Knowledge/Software Engineering/Backend/Backend.md",
    "40-Knowledge/Software Engineering/Frontend/Qt for Python.md":
        "40-Knowledge/Software Engineering/Frontend/Frontend.md",
    "40-Knowledge/Systems/ArchLinux.md":
        "40-Knowledge/Systems/Systems.md",
}
FORBIDDEN_TOP_LEVEL = {
    "inbox",
    "archive",
    "assets",
    "templates",
    "maintenance",
    "语言",
    "工具",
    "后端",
    "前端",
    "系统",
    "数据结构",
    "机器学习",
    "安全",
    "爬虫",
    "博客",
}
HEXO_PATTERN = re.compile(r"{%\s*(?:post_link|note|endnote)\b|<!--\s*more\s*-->")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def code_blocks(text: str) -> list[str]:
    return re.findall(r"```[^\n]*\n.*?```", text, re.S)


def headings(text: str) -> set[str]:
    return {
        match.group(1).strip().rstrip("#").strip()
        for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", outside_fences(text), re.M)
    }


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    match = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not match:
        return {}, text
    data: dict[str, object] = {}
    current: str | None = None
    for line in match.group(1).splitlines():
        item = re.match(r"^\s*-\s+(.+?)\s*$", line)
        if item and current:
            data.setdefault(current, [])
            assert isinstance(data[current], list)
            data[current].append(item.group(1).strip().strip("\"'"))
            continue
        field = re.match(r"^([A-Za-z_]+):\s*(.*?)\s*$", line)
        if not field:
            continue
        current, value = field.groups()
        if value == "[]":
            data[current] = []
            current = None
        elif value:
            data[current] = value.strip().strip("\"'")
            current = None
        else:
            data[current] = []
    return data, text[match.end() :]


def outside_fences(text: str) -> str:
    output: list[str] = []
    fence: str | None = None
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is None:
            output.append(line)
    return "".join(output)


def is_date(value: object) -> bool:
    try:
        date.fromisoformat(str(value))
    except ValueError:
        return False
    return True


def metadata_links(meta: dict[str, object]) -> list[str]:
    values: list[str] = []
    for value in meta.values():
        if isinstance(value, list):
            values.extend(str(item) for item in value)
        else:
            values.append(str(value))
    return re.findall(r"\[\[([^\]]+)\]\]", "\n".join(values))


def body_links(body: str) -> list[tuple[bool, str]]:
    return [
        (bool(match.group(1)), match.group(2))
        for match in re.finditer(r"(!?)\[\[([^\]]+)\]\]", outside_fences(body))
    ]


def resolve_note(
    raw: str,
    paths: dict[str, Path],
    titles: dict[str, list[Path]],
) -> Path | None:
    target = raw.split("|", 1)[0].split("#", 1)[0].split("^", 1)[0].strip()
    normalized = target.removesuffix(".md").lstrip("/")
    if normalized in paths:
        return paths[normalized]
    matches = sorted(set(titles.get(normalized, [])))
    return matches[0] if len(matches) == 1 else None


def validate_note_shape(path: Path, meta: dict[str, object], errors: list[str]) -> None:
    missing_common = COMMON_FIELDS - set(meta)
    if missing_common:
        errors.append(f"{rel(path)} 缺少公共属性：{', '.join(sorted(missing_common))}")
        return
    note_type = str(meta["type"])
    if note_type not in TYPE_FIELDS:
        errors.append(f"{rel(path)} type 非法：{note_type}")
        return
    missing_type = TYPE_FIELDS[note_type] - set(meta)
    if missing_type:
        errors.append(f"{rel(path)} 缺少 {note_type} 属性：{', '.join(sorted(missing_type))}")
    if not is_date(meta["created"]):
        errors.append(f"{rel(path)} created 不是 YYYY-MM-DD：{meta['created']}")
    status = meta.get("status")
    if note_type in VALID_STATUS and status not in VALID_STATUS[note_type]:
        errors.append(f"{rel(path)} status 非法：{status}")
    if note_type in {"note", "moc"} and meta.get("review") not in VALID_REVIEW:
        errors.append(f"{rel(path)} review 非法：{meta.get('review')}")
    if note_type == "project" and not is_date(meta.get("started")):
        errors.append(f"{rel(path)} started 不是有效日期：{meta.get('started')}")
    if note_type in {"daily", "meeting"} and not is_date(meta.get("date")):
        errors.append(f"{rel(path)} date 不是有效日期：{meta.get('date')}")


def validate_naming(path: Path, meta: dict[str, object], errors: list[str]) -> None:
    note_type = str(meta.get("type"))
    relative = rel(path)
    stem = path.stem
    if note_type == "daily":
        match = re.fullmatch(r"10-Daily/(\d{4})/(\d{2})/(\d{4}-\d{2}-\d{2})\.md", relative)
        if not match or match.group(3) != str(meta.get("date")):
            errors.append(f"{relative} 不符合 Daily 年/月/日期规则")
    elif note_type == "paper" and not re.fullmatch(r".+-\d{4}-.+", stem):
        errors.append(f"{relative} 不符合 第一作者-年份-短标题 命名规则")
    elif note_type == "experiment":
        if not relative.startswith("30-Research/Experiments/") or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}-.+", stem
        ):
            errors.append(f"{relative} 不符合实验位置或命名规则")
    elif note_type == "meeting" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}-.+", stem):
        errors.append(f"{relative} 不符合会议命名规则")
    elif note_type == "project":
        parts = path.relative_to(ROOT).parts
        if len(parts) != 3 or parts[0] != "20-Projects" or path.parent.name != stem:
            errors.append(f"{relative} 不符合项目目录与项目页同名规则")


def validate_templates(errors: list[str]) -> None:
    template_dir = ROOT / "90-Templates"
    actual = {path.stem for path in template_dir.glob("*.md")}
    missing = REQUIRED_TEMPLATES - actual
    if missing:
        errors.append("缺少模板：" + ", ".join(sorted(missing)))
    for name in REQUIRED_TEMPLATES & actual:
        meta, _ = parse_frontmatter((template_dir / f"{name}.md").read_text())
        note_type = str(meta.get("type"))
        if not COMMON_FIELDS <= set(meta):
            errors.append(f"90-Templates/{name}.md 缺少公共属性")
        if note_type not in TYPE_FIELDS:
            errors.append(f"90-Templates/{name}.md type 非法：{note_type}")
        elif not TYPE_FIELDS[note_type] <= set(meta):
            missing_fields = TYPE_FIELDS[note_type] - set(meta)
            errors.append(
                f"90-Templates/{name}.md 缺少类型属性：{', '.join(sorted(missing_fields))}"
            )
        if name in {"Knowledge Note", "MOC"} and meta.get("review") != "reviewed":
            errors.append(f"90-Templates/{name}.md 必须默认使用 review: reviewed")


def validate_obsidian(errors: list[str]) -> None:
    expected = {
        ".obsidian/app.json": {"attachmentFolderPath": "99-Assets"},
        ".obsidian/templates.json": {"folder": "90-Templates"},
        ".obsidian/daily-notes.json": {
            "folder": "10-Daily",
            "format": "YYYY/MM/YYYY-MM-DD",
            "template": "90-Templates/Daily",
        },
    }
    for name, values in expected.items():
        path = ROOT / name
        if not path.exists():
            errors.append(f"缺少配置：{name}")
            continue
        data = json.loads(path.read_text())
        for key, expected_value in values.items():
            if data.get(key) != expected_value:
                errors.append(f"{name} 的 {key} 配置错误：{data.get(key)!r}")
    types_path = ROOT / ".obsidian/types.json"
    if not types_path.exists():
        errors.append("缺少 .obsidian/types.json")
    else:
        types = json.loads(types_path.read_text()).get("types", {})
        for key in {
            "type",
            "created",
            "area",
            "status",
            "review",
            "project",
            "projects",
            "date",
            "authors",
            "participants",
        }:
            if key not in types:
                errors.append(f".obsidian/types.json 缺少属性类型：{key}")


def validate_review_queue(
    metadata: dict[Path, dict[str, object]],
    paths: dict[str, Path],
    titles: dict[str, list[Path]],
    errors: list[str],
) -> int:
    queue_path = ROOT / "95-Maintenance/待复核.md"
    if not queue_path.exists():
        return 0

    _, body = parse_frontmatter(queue_path.read_text())
    task_items = re.findall(r"^- \[([ xX])\] \[\[([^\]]+)\]\]\s*$", body, re.M)
    completed_items = [raw for marker, raw in task_items if marker.lower() == "x"]
    if completed_items:
        errors.append(
            "待复核清单不应保留已完成项："
            + ", ".join(f"[[{raw}]]" for raw in completed_items)
        )
    raw_items = [raw for marker, raw in task_items if marker == " "]
    queued: list[Path] = []
    for raw in raw_items:
        resolved = resolve_note(raw, paths, titles)
        if resolved is None:
            errors.append(f"待复核清单项无法解析：[[{raw}]]")
        else:
            queued.append(resolved)

    duplicates = sorted(path for path, count in Counter(queued).items() if count > 1)
    if duplicates:
        errors.append("待复核清单存在重复项：" + ", ".join(rel(path) for path in duplicates))

    pending = {
        path
        for path, meta in metadata.items()
        if meta.get("review") == "pending"
    }
    queued_set = set(queued)
    missing = sorted(pending - queued_set)
    stale = sorted(queued_set - pending)
    if missing:
        errors.append(
            "review: pending 但未加入待复核清单："
            + ", ".join(rel(path) for path in missing)
        )
    if stale:
        errors.append(
            "待复核清单项未设置 review: pending："
            + ", ".join(rel(path) for path in stale)
        )
    return len(pending)


def load_topic_merge_manifest(errors: list[str]) -> dict[str, object]:
    if not TOPIC_MERGE_MANIFEST.exists():
        errors.append("缺少主题合并清单")
        return {}
    try:
        manifest = json.loads(TOPIC_MERGE_MANIFEST.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"主题合并清单不是有效 JSON：{exc}")
        return {}
    if manifest.get("group_count") != 11:
        errors.append(f"主题合并组数异常：{manifest.get('group_count')}")
    if manifest.get("deleted_child_count") != 70:
        errors.append(f"主题合并子笔记数异常：{manifest.get('deleted_child_count')}")
    if manifest.get("code_block_count") != 406:
        errors.append(f"主题合并代码块数异常：{manifest.get('code_block_count')}")
    return manifest


def validate_topic_merge(
    manifest: dict[str, object],
    graph: dict[Path, set[Path]],
    bodies: dict[Path, str],
    errors: list[str],
) -> set[str]:
    deleted_paths: set[str] = set()
    groups = manifest.get("groups", [])
    if not isinstance(groups, list):
        errors.append("主题合并清单 groups 类型错误")
        return deleted_paths

    for group in groups:
        if not isinstance(group, dict):
            errors.append("主题合并清单包含非法组")
            continue
        parent_string = str(group.get("parent", ""))
        parent = ROOT / parent_string
        expected_moc_string = MERGED_PARENT_MOCS.get(parent_string)
        if expected_moc_string is None:
            errors.append(f"主题合并清单包含未知父文档：{parent_string}")
        elif parent not in graph.get(ROOT / expected_moc_string, set()):
            errors.append(f"领域 MOC 未链接合并文档：{parent_string}")
        if not parent.exists():
            errors.append(f"主题合并父文档不存在：{parent_string}")
            continue

        parent_body = bodies.get(parent, parse_frontmatter(parent.read_text())[1])
        parent_headings = headings(parent_body)
        children = group.get("children", [])
        if not isinstance(children, list):
            errors.append(f"主题合并组 children 类型错误：{parent_string}")
            continue
        for child in children:
            if not isinstance(child, dict):
                errors.append(f"主题合并组包含非法子项：{parent_string}")
                continue
            child_path = str(child.get("path", ""))
            child_title = str(child.get("title", ""))
            anchor = str(child.get("anchor", ""))
            deleted_paths.add(child_path.removesuffix(".md"))
            if (ROOT / child_path).exists():
                errors.append(f"已合并子笔记仍存在：{child_path}")
            if anchor not in parent_headings:
                errors.append(f"{parent_string} 缺少章节标题：{anchor}")
            toc_link = f"[[#{anchor}|{child_title}]]"
            if toc_link not in parent_body:
                errors.append(f"{parent_string} 章节目录缺少：{toc_link}")
    return deleted_paths


def validate_manifest(
    merge_manifest: dict[str, object],
    notes: list[Path],
    errors: list[str],
) -> tuple[int, int, int]:
    if not MANIFEST.exists():
        errors.append("缺少逐项遗留清单")
        return 0, 0, 0
    manifest = json.loads(MANIFEST.read_text())
    if manifest.get("source_note_count") != 135:
        errors.append(f"遗留笔记基线异常：{manifest.get('source_note_count')}")
    if manifest.get("knowledge_note_count") != 129:
        errors.append(f"知识笔记基线异常：{manifest.get('knowledge_note_count')}")
    if manifest.get("asset_count") != 174:
        errors.append(f"附件基线异常：{manifest.get('asset_count')}")
    if manifest.get("code_block_count") != 642:
        errors.append(f"代码块基线异常：{manifest.get('code_block_count')}")

    merged_children = {
        str(child["path"])
        for group in merge_manifest.get("groups", [])
        if isinstance(group, dict)
        for child in group.get("children", [])
        if isinstance(child, dict) and "path" in child
    }
    merged_parents = {
        str(group["parent"])
        for group in merge_manifest.get("groups", [])
        if isinstance(group, dict) and "parent" in group
    }
    for item in manifest["notes"]:
        path = ROOT / item["new_path"]
        if not path.exists() and item["new_path"] not in merged_children:
            errors.append(f"遗留笔记目标不存在：{item['new_path']}")

    for item in manifest["assets"]:
        path = ROOT / item["new_path"]
        if not path.exists():
            errors.append(f"遗留附件目标不存在：{item['new_path']}")
        elif sha256(path.read_bytes()) != item["sha256"]:
            errors.append(f"遗留附件内容变化：{item['new_path']}")

    expected_blocks = Counter(item["sha256"] for item in manifest["code_blocks"])
    actual_blocks = Counter(
        sha256(block.encode())
        for path in notes
        for block in code_blocks(path.read_text())
    )
    missing_blocks = expected_blocks - actual_blocks
    if missing_blocks:
        errors.append(
            "遗留代码块内容缺失："
            f"{sum(missing_blocks.values())} 个，{len(missing_blocks)} 种哈希"
        )
    matched_count = sum((expected_blocks & actual_blocks).values())
    if matched_count != manifest["code_block_count"]:
        errors.append(
            "遗留代码块数量变化："
            f"期望 {manifest['code_block_count']}，匹配 {matched_count}"
        )

    for parent in merged_parents:
        if not (ROOT / parent).exists():
            errors.append(f"主题合并重定向目标不存在：{parent}")
    return manifest["source_note_count"], manifest["asset_count"], matched_count


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    merge_manifest = load_topic_merge_manifest(errors)

    for name in FORBIDDEN_TOP_LEVEL:
        if (ROOT / name).exists():
            errors.append(f"旧顶层目录仍存在：{name}")
    for path in REQUIRED_PATHS:
        if not (ROOT / path).exists():
            errors.append(f"缺少结构入口：{path}")

    notes = sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "90-Templates" not in path.parts
    )
    for path in ROOT.rglob("*.md"):
        same_name_dir = path.with_suffix("")
        if same_name_dir.is_dir():
            errors.append(f"存在同名主题文件与目录：{rel(path)} + {rel(same_name_dir)}/")
    assets = sorted(
        path
        for path in (ROOT / "99-Assets").rglob("*")
        if path.is_file() and path.suffix.lower() in ASSET_SUFFIXES
    )

    metadata: dict[Path, dict[str, object]] = {}
    bodies: dict[Path, str] = {}
    titles: dict[str, list[Path]] = defaultdict(list)
    paths: dict[str, Path] = {}

    for path in notes:
        text = path.read_text()
        meta, body = parse_frontmatter(text)
        metadata[path] = meta
        bodies[path] = body
        validate_note_shape(path, meta, errors)
        validate_naming(path, meta, errors)
        if HEXO_PATTERN.search(text):
            errors.append(f"{rel(path)} 仍包含 Hexo 专用语法")
        if "domain" in meta:
            errors.append(f"{rel(path)} 仍包含旧 domain 属性")
        title = str(meta.get("title") or path.stem)
        titles[title].append(path)
        aliases = meta.get("aliases", [])
        if isinstance(aliases, list):
            for alias in aliases:
                titles[str(alias)].append(path)
        paths[rel(path.with_suffix(""))] = path

    for title, matches in titles.items():
        unique = sorted(set(matches))
        if len(unique) > 1:
            errors.append(f"标题或别名重复：{title} -> {', '.join(rel(path) for path in unique)}")

    references: set[Path] = set()
    graph: dict[Path, set[Path]] = defaultdict(set)
    deleted_paths = {
        str(child["path"]).removesuffix(".md")
        for group in merge_manifest.get("groups", [])
        if isinstance(group, dict)
        for child in group.get("children", [])
        if isinstance(child, dict) and "path" in child
    }
    deleted_titles = {
        str(child["title"])
        for group in merge_manifest.get("groups", [])
        if isinstance(group, dict)
        for child in group.get("children", [])
        if isinstance(child, dict) and "title" in child
    }
    for path, body in bodies.items():
        links = body_links(body)
        links.extend((False, raw) for raw in metadata_links(metadata[path]))
        for embedded, raw in links:
            target = raw.split("|", 1)[0].split("#", 1)[0].split("^", 1)[0].strip().lstrip("/")
            normalized_target = target.removesuffix(".md")
            if normalized_target in deleted_paths or normalized_target in deleted_titles:
                errors.append(f"{rel(path)} 仍指向已删除子笔记：[[{raw}]]")
            asset_path = ROOT / target
            if asset_path.suffix.lower() in ASSET_SUFFIXES:
                if not asset_path.exists():
                    errors.append(f"{rel(path)} 附件不存在：{target}")
                else:
                    references.add(asset_path.resolve())
                continue
            resolved = path if not target and "#" in raw else resolve_note(raw, paths, titles)
            if resolved is None:
                errors.append(f"{rel(path)} 内部链接无法解析：[[{raw}]]")
            else:
                graph[path].add(resolved)
            if embedded and resolved is not None:
                warnings.append(f"{rel(path)} 将 Markdown 笔记作为嵌入：[[{raw}]]")

    orphan_assets = [path for path in assets if path.resolve() not in references]
    if orphan_assets:
        errors.append("存在孤立附件：" + ", ".join(rel(path) for path in orphan_assets))

    homepage = ROOT / "首页.md"
    reachable: set[Path] = set()
    queue: deque[Path] = deque([homepage])
    while queue:
        current = queue.popleft()
        if current in reachable or current not in bodies:
            continue
        reachable.add(current)
        queue.extend(graph[current] - reachable)
    unreachable = [path for path in notes if path not in reachable]
    if unreachable:
        errors.append("存在无法从首页到达的笔记：" + ", ".join(rel(path) for path in unreachable))

    validate_templates(errors)
    validate_obsidian(errors)
    pending_reviews = validate_review_queue(metadata, paths, titles, errors)
    validate_topic_merge(merge_manifest, graph, bodies, errors)
    legacy_notes, legacy_assets, legacy_code_blocks = validate_manifest(
        merge_manifest, notes, errors
    )

    print("科研工作台审计")
    print(f"- 当前非模板笔记：{len(notes)} 篇")
    print(f"- 首页可达笔记：{len(reachable)} 篇")
    print(f"- 遗留笔记映射：{legacy_notes} 篇")
    print(f"- 附件：{len(assets)} 个（遗留基线 {legacy_assets}）")
    print(f"- 遗留代码块：{legacy_code_blocks} / 642 个")
    print(f"- 待复核笔记：{pending_reviews} 篇")
    print(f"- 模板：{len(list((ROOT / '90-Templates').glob('*.md')))} 个")
    if warnings:
        print("\n警告：")
        for warning in sorted(set(warnings)):
            print(f"- {warning}")
    if errors:
        print("\n错误：")
        for error in errors:
            print(f"- {error}")
        return 1
    print("\n结果：通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
