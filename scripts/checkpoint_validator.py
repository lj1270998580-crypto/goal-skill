#!/usr/bin/env python3
"""
Checkpoint Validator — 检查点自动化验证脚本

用法:
  python checkpoint_validator.py --workspace /path/to/workspace --stage 4 --type software --goal-dir /path/to/goal-skill
  
根据目标类型，自动运行对应的检查清单验证。
不依赖外部库，纯 Python 标准库。
"""

import sys
import os
import re
from pathlib import Path


def find_checklist(goal_dir, goal_type):
    """从 goal-skill 的 references 目录读取对应类型的检查清单。"""
    checklist_path = os.path.join(goal_dir, "references", "quality-checklist.md")
    if not os.path.exists(checklist_path):
        return None
    
    with open(checklist_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 根据目标类型找到对应的检查清单部分
    type_map = {
        "software": "## Software Development Checklist",
        "content": "## Content Creation Checklist",
        "data": "## Data Analysis Checklist",
        "document": "## Document Generation Checklist",
        "presentation": "## Presentation Checklist",
        "webapp": "## Webapp / Frontend Checklist"
    }
    
    marker = type_map.get(goal_type, type_map.get("general", "## General Verification Checklist"))
    
    # 提取从 marker 到下一个 ## 之间的内容
    pattern = re.compile(re.escape(marker) + r'(.*?)(?=\n## |\Z)', re.DOTALL)
    match = pattern.search(content)
    if match:
        return match.group(1).strip()
    return None


def parse_checklist(checklist_text):
    """解析检查清单为可验证的条目列表。"""
    items = []
    for line in checklist_text.splitlines():
        line = line.strip()
        # 匹配 - [ ] 或 - [x] 格式的检查项
        match = re.match(r'-\s*\[\s*([xX])?\s*\]\s*(.+)', line)
        if match:
            items.append({
                "text": match.group(2).strip(),
                "auto_verifiable": _is_auto_verifiable(match.group(2).strip()),
                "done": bool(match.group(1))
            })
    return items


def _is_auto_verifiable(text):
    """判断一个检查项是否可以自动验证。"""
    auto_keywords = [
        "runs", "compiles", "builds", "passes", "exists", "file", "format",
        "can run", "no fatal", "no errors", "test", "dependency"
    ]
    text_lower = text.lower()
    return any(kw in text_lower for kw in auto_keywords)


def verify_item(item, workspace):
    """尝试自动验证一个检查项。"""
    text = item["text"].lower()
    
    # 文件存在性检查
    if "file" in text and "exist" in text:
        # 尝试在工作目录查找相关文件
        return {"result": "manual", "reason": "需要指定具体文件名"}
    
    # 代码可运行检查
    if any(kw in text for kw in ["runs", "compiles", "builds", "no fatal error"]):
        # 尝试检测常见构建文件
        for build_file in ["package.json", "requirements.txt", "Makefile", "Cargo.toml", "pom.xml"]:
            if os.path.exists(os.path.join(workspace, build_file)):
                return {"result": "auto_detected", "evidence": f"发现构建文件: {build_file}"}
        return {"result": "manual", "reason": "无法自动检测，需要手动运行测试"}
    
    # 测试通过检查
    if "test" in text and "pass" in text:
        test_files = list(Path(workspace).rglob("*test*")) + list(Path(workspace).rglob("*spec*"))
        if test_files:
            return {"result": "auto_detected", "evidence": f"发现测试文件: {len(test_files)} 个"}
        return {"result": "manual", "reason": "未发现测试文件，需要手动确认"}
    
    # 格式检查
    if "format" in text or "formatting" in text:
        return {"result": "manual", "reason": "格式检查需要手动评审"}
    
    # 默认：需要人工判断
    return {"result": "manual", "reason": "该检查项需要人工判断"}


def run_validation(workspace, stage, goal_type, goal_dir):
    """运行验证流程。"""
    print(f"🔍 Checkpoint Validator — Stage {stage}, Type: {goal_type}")
    print(f"   Workspace: {workspace}")
    print(f"   Goal-skill dir: {goal_dir}")
    print()
    
    # 1. 通用检查
    print("=" * 60)
    print("📋 General Verification Checklist (Always)")
    print("=" * 60)
    
    general_items = [
        "Completeness: The result covers the user's entire goal.",
        "No Omissions: No critical content or functionality is missing.",
        "No Obvious Errors: No visible errors or defects.",
        "Format Match: The output format matches the requested format.",
        "Quality Standard: The quality meets the minimum deliverable standard."
    ]
    
    for item in general_items:
        result = verify_item({"text": item}, workspace)
        symbol = "🤖" if result["result"] == "auto_detected" else "👤"
        print(f"  {symbol} {item}")
        print(f"     → {result['result']}: {result.get('evidence', result.get('reason', ''))}")
    
    print()
    
    # 2. 领域检查
    checklist = find_checklist(goal_dir, goal_type)
    if checklist:
        print("=" * 60)
        print(f"📋 Domain-Specific Checklist ({goal_type})")
        print("=" * 60)
        items = parse_checklist(checklist)
        for item in items:
            result = verify_item(item, workspace)
            symbol = "🤖" if result["result"] == "auto_detected" else "👤"
            print(f"  {symbol} {item['text']}")
            print(f"     → {result['result']}: {result.get('evidence', result.get('reason', ''))}")
    else:
        print(f"⚠️  No checklist found for type: {goal_type}")
    
    print()
    print("=" * 60)
    print("📊 Summary: Items marked 🤖 were auto-detected.")
    print("             Items marked 👤 require manual verification.")
    print("=" * 60)
    
    return 0


def parse_args(argv):
    args = {}
    i = 1
    while i < len(argv):
        if argv[i].startswith("--") and i + 1 < len(argv):
            args[argv[i]] = argv[i + 1]
            i += 2
        else:
            i += 1
    return args


def main():
    if len(sys.argv) < 2:
        print("Usage: python checkpoint_validator.py [options]")
        print("Options:")
        print("  --workspace <path>   Target workspace directory")
        print("  --stage <n>           Stage number (1-6)")
        print("  --type <type>         Goal type (software/content/data/document/presentation/webapp)")
        print("  --goal-dir <path>     Path to goal-skill directory")
        return 1
    
    args = parse_args(sys.argv)
    workspace = args.get("--workspace", os.getcwd())
    stage = args.get("--stage", "5")
    goal_type = args.get("--type", "general")
    goal_dir = args.get("--goal-dir", os.getcwd())
    
    return run_validation(workspace, stage, goal_type, goal_dir)


if __name__ == "__main__":
    sys.exit(main())
