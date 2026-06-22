#!/usr/bin/env python3
"""
Goal State Manager — 状态文件管理脚本

用法:
  python goal_state.py init --workspace /path/to/workspace --goal "用户目标描述" --type software
  python goal_state.py update-stage --workspace /path/to/workspace --stage 1 --status in_progress
  python goal_state.py checkpoint --workspace /path/to/workspace --stage 2 --passed 5 --total 6 --retries 1
  python goal_state.py retrospective --workspace /path/to/workspace --round 1 --scores "func=4,bug=3,ux=3,code=4,perf=2,sec=4" --improvements "3"
  python goal_state.py evolution --workspace /path/to/workspace --round 2 --backtrack-to 4
  python goal_state.py read --workspace /path/to/workspace
  python goal_state.py recover --workspace /path/to/workspace
  python goal_state.py escalate --workspace /path/to/workspace --reason "原因" --stage 3
  python goal_state.py deliver --workspace /path/to/workspace --artifact "file.py"
  python goal_state.py log --workspace /path/to/workspace --message "执行日志条目"
  python goal_state.py user-change --workspace /path/to/workspace --change "用户变更内容" --scope minor|medium|major
  python goal_state.py evolution-history --workspace /path/to/workspace

不依赖外部库，纯 Python 标准库。
"""

import sys
import os
import re
from datetime import datetime

STATE_FILENAME = ".goal-state.md"
LOG_FILENAME = "goal-execution-log.md"


def now():
    return datetime.now().isoformat(sep=" ", timespec="seconds")


def get_state_path(workspace):
    return os.path.join(os.path.expanduser(workspace), STATE_FILENAME)


def get_log_path(workspace):
    return os.path.join(os.path.expanduser(workspace), LOG_FILENAME)


def parse_state(content):
    """从 Markdown 状态文件解析出状态字典。"""
    state = {
        "goal_info": {},
        "stage_tracker": {},
        "checkpoint_tracker": {},
        "escalation_log": [],
        "user_feedback": [],
        "artifacts": [],
        "evolution": {
            "current_round": 1,
            "max_rounds": 6,
            "history": []
        }
    }
    
    # 解析 Goal Info
    goal_match = re.search(r'\*\*Goal Summary\*\*:\s*(.*)', content)
    if goal_match:
        state["goal_info"]["goal_summary"] = goal_match.group(1).strip()
    
    goal_type_match = re.search(r'\*\*Goal Type\*\*:\s*(.*)', content)
    if goal_type_match:
        state["goal_info"]["goal_type"] = goal_type_match.group(1).strip()
    
    workspace_match = re.search(r'\*\*Workspace\*\*:\s*(.*)', content)
    if workspace_match:
        state["goal_info"]["workspace"] = workspace_match.group(1).strip()
    
    # 解析 Evolution 轮次
    round_match = re.search(r'\*\*Current Round\*\*:\s*(\d+)', content)
    if round_match:
        state["evolution"]["current_round"] = int(round_match.group(1))
    
    max_round_match = re.search(r'\*\*Max Rounds\*\*:\s*(\d+)', content)
    if max_round_match:
        state["evolution"]["max_rounds"] = int(max_round_match.group(1))
    
    # 解析 Stage Tracker
    stage_pattern = re.compile(
        r'\|\s*(\d+\.\s*\w+)\s*\|\s*([^|]+)\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|'
    )
    for m in stage_pattern.finditer(content):
        state["stage_tracker"][m.group(1).strip()] = {
            "status": m.group(2).strip(),
            "started": m.group(3).strip(),
            "completed": m.group(4).strip(),
            "retries": m.group(5).strip(),
            "notes": m.group(6).strip()
        }
    
    # 解析 Checkpoint Tracker
    cp_pattern = re.compile(
        r'-\s*\[\s*([xX])?\s*\]\s*Stage\s+(\d+)\s+Checkpoint\s*\((\d+)/(\d+)\s+passed(?:,\s+(\d+)\s+retries)?\)'
    )
    for m in cp_pattern.finditer(content):
        state["checkpoint_tracker"][m.group(2)] = {
            "passed": m.group(3),
            "total": m.group(4),
            "retries": m.group(5) if m.group(5) else "0",
            "completed": bool(m.group(1))
        }
    
    # 解析 Evolution History
    in_evolution = False
    for line in content.splitlines():
        if line.startswith("## Evolution History"):
            in_evolution = True
            continue
        if in_evolution and line.startswith("##"):
            in_evolution = False
        if in_evolution and line.startswith("|") and not line.startswith("| Round"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 6 and parts[1].isdigit():
                state["evolution"]["history"].append({
                    "round": int(parts[1]),
                    "stage": parts[2],
                    "score": parts[3],
                    "improvements": parts[4],
                    "status": parts[5]
                })
    
    # 解析 Artifacts
    artifact_pattern = re.compile(r'-\s*\[\s*([xX])?\s*\]\s*(.+)')
    in_artifacts = False
    for line in content.splitlines():
        if line.startswith("## Artifacts"):
            in_artifacts = True
            continue
        if in_artifacts and line.startswith("##"):
            in_artifacts = False
        if in_artifacts and artifact_pattern.match(line):
            m = artifact_pattern.match(line)
            state["artifacts"].append({
                "done": bool(m.group(1)),
                "name": m.group(2).strip()
            })
    
    return state


def format_state(state):
    """将状态字典格式化为 Markdown 状态文件。"""
    goal_info = state.get("goal_info", {})
    stage_tracker = state.get("stage_tracker", {})
    checkpoint_tracker = state.get("checkpoint_tracker", {})
    escalation_log = state.get("escalation_log", [])
    user_feedback = state.get("user_feedback", [])
    artifacts = state.get("artifacts", [])
    evolution = state.get("evolution", {"current_round": 1, "max_rounds": 6, "history": []})
    
    lines = [
        "# Goal Execution State",
        "",
        "## Goal Info",
        f"- **Started**: {goal_info.get('started', now())}",
        f"- **Goal Summary**: {goal_info.get('goal_summary', '')}",
        f"- **Goal Type**: {goal_info.get('goal_type', '')}",
        f"- **Workspace**: {goal_info.get('workspace', '')}",
        f"- **Current Round**: {evolution.get('current_round', 1)} / {evolution.get('max_rounds', 6)}",
        f"- **Max Rounds**: {evolution.get('max_rounds', 6)}",
        "",
        "## Stage Tracker",
        "| Stage | Status | Started | Completed | Retries | Notes |",
        "|-------|--------|---------|-----------|---------|-------|",
    ]
    
    for stage_name in ["1. Understand", "2. Plan", "3. Design", "4. Execute", "5. Verify", "6. Deliver"]:
        info = stage_tracker.get(stage_name, {})
        lines.append(
            f"| {stage_name} | {info.get('status', '⬜ Not Started')} | "
            f"{info.get('started', '-')} | {info.get('completed', '-')} | "
            f"{info.get('retries', '0')} | {info.get('notes', '')} |"
        )
    
    lines.extend([
        "",
        "## Checkpoint Tracker"
    ])
    
    for i in range(1, 7):
        cp = checkpoint_tracker.get(str(i), {})
        passed = cp.get("passed", "0")
        total = cp.get("total", "6")
        retries = cp.get("retries", "0")
        completed = "x" if cp.get("completed") else " "
        lines.append(f"- [{completed}] Stage {i} Checkpoint ({passed}/{total} passed, {retries} retries)")
    
    lines.extend([
        "",
        "## Evolution History"
    ])
    if evolution.get("history"):
        lines.append("| Round | Stage | Score | Improvements | Status |")
        lines.append("|-------|-------|-------|-------------|--------|")
        for entry in evolution["history"]:
            lines.append(
                f"| {entry.get('round', '-')} | {entry.get('stage', '-')} | "
                f"{entry.get('score', '-')} | {entry.get('improvements', '-')} | {entry.get('status', '-')} |"
            )
    else:
        lines.append("[Empty — no evolution rounds yet]")
    
    lines.extend([
        "",
        "## Escalation Log"
    ])
    if escalation_log:
        for entry in escalation_log:
            lines.append(f"- **{entry['time']}** — Stage {entry['stage']}: {entry['reason']}")
    else:
        lines.append("[Empty until first escalation]")
    
    lines.extend([
        "",
        "## User Feedback"
    ])
    if user_feedback:
        for entry in user_feedback:
            lines.append(f"- **{entry['time']}** — {entry['type']}: {entry['content']}")
    else:
        lines.append("[Empty until user provides mid-execution feedback]")
    
    lines.extend([
        "",
        "## Artifacts"
    ])
    if artifacts:
        for a in artifacts:
            done = "x" if a.get("done") else " "
            lines.append(f"- [{done}] {a['name']}")
    else:
        lines.append("- [ ] Plan file: `goal-plan.md`")
        lines.append("- [ ] Design file: `goal-design.md` (if applicable)")
        lines.append("- [ ] Execution log: `goal-execution-log.md`")
        lines.append("- [ ] Verification report: `goal-verification-report.md`")
        lines.append("- [ ] Deliverables: [list as created]")
    
    return "\n".join(lines) + "\n"


def cmd_init(args):
    workspace = args.get("--workspace", os.getcwd())
    goal = args.get("--goal", "")
    goal_type = args.get("--type", "general")
    max_rounds = args.get("--max-rounds", "6")
    
    state = {
        "goal_info": {
            "started": now(),
            "goal_summary": goal,
            "goal_type": goal_type,
            "workspace": os.path.abspath(workspace)
        },
        "stage_tracker": {},
        "checkpoint_tracker": {},
        "escalation_log": [],
        "user_feedback": [],
        "artifacts": [],
        "evolution": {
            "current_round": 1,
            "max_rounds": int(max_rounds),
            "history": []
        }
    }
    
    path = get_state_path(workspace)
    with open(path, "w", encoding="utf-8") as f:
        f.write(format_state(state))
    
    print(f"✅ State file created: {path}")
    return 0


def cmd_update_stage(args):
    workspace = args.get("--workspace", os.getcwd())
    stage = args.get("--stage", "")
    status = args.get("--status", "")
    notes = args.get("--notes", "")
    
    path = get_state_path(workspace)
    if not os.path.exists(path):
        print(f"❌ State file not found: {path}", file=sys.stderr)
        return 1
    
    with open(path, "r", encoding="utf-8") as f:
        state = parse_state(f.read())
    
    stage_map = {
        "1": "1. Understand", "2": "2. Plan", "3": "3. Design",
        "4": "4. Execute", "5": "5. Verify", "6": "6. Deliver"
    }
    stage_name = stage_map.get(stage, stage)
    
    if stage_name not in state["stage_tracker"]:
        state["stage_tracker"][stage_name] = {}
    
    current = state["stage_tracker"][stage_name]
    
    if status:
        current["status"] = status
    if status == "🟡 In Progress" and not current.get("started"):
        current["started"] = now()
    if status == "✅ Completed":
        current["completed"] = now()
    if notes:
        current["notes"] = notes
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(format_state(state))
    
    print(f"✅ Stage {stage_name} updated: status={status}")
    return 0


def cmd_checkpoint(args):
    workspace = args.get("--workspace", os.getcwd())
    stage = args.get("--stage", "")
    passed = args.get("--passed", "0")
    total = args.get("--total", "6")
    retries = args.get("--retries", "0")
    
    path = get_state_path(workspace)
    if not os.path.exists(path):
        print(f"❌ State file not found: {path}", file=sys.stderr)
        return 1
    
    with open(path, "r", encoding="utf-8") as f:
        state = parse_state(f.read())
    
    state["checkpoint_tracker"][stage] = {
        "passed": passed,
        "total": total,
        "retries": retries,
        "completed": passed == total
    }
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(format_state(state))
    
    print(f"✅ Checkpoint Stage {stage}: {passed}/{total} passed, {retries} retries")
    return 0


def cmd_retrospective(args):
    """记录反思结果。"""
    workspace = args.get("--workspace", os.getcwd())
    round_num = args.get("--round", "")
    scores = args.get("--scores", "")
    improvements = args.get("--improvements", "0")
    
    path = get_state_path(workspace)
    if not os.path.exists(path):
        print(f"❌ State file not found: {path}", file=sys.stderr)
        return 1
    
    with open(path, "r", encoding="utf-8") as f:
        state = parse_state(f.read())
    
    # Parse scores: "func=4,bug=3,ux=3,code=4,perf=2,sec=4"
    score_map = {}
    if scores:
        for pair in scores.split(","):
            if "=" in pair:
                k, v = pair.strip().split("=", 1)
                score_map[k.strip()] = v.strip()
    
    total_score = sum(int(v) for v in score_map.values() if v.isdigit())
    max_score = len(score_map) * 5 if score_map else 30
    
    state["evolution"]["history"].append({
        "round": int(round_num) if round_num.isdigit() else len(state["evolution"]["history"]) + 1,
        "stage": "Delivered",
        "score": f"{total_score}/{max_score}",
        "improvements": improvements,
        "status": "✅ Completed"
    })
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(format_state(state))
    
    print(f"📊 Retrospective recorded: Round {round_num}, Score {total_score}/{max_score}, {improvements} improvements")
    return 0


def cmd_evolution(args):
    """进入下一轮进化。"""
    workspace = args.get("--workspace", os.getcwd())
    round_num = args.get("--round", "")
    backtrack_to = args.get("--backtrack-to", "")
    
    path = get_state_path(workspace)
    if not os.path.exists(path):
        print(f"❌ State file not found: {path}", file=sys.stderr)
        return 1
    
    with open(path, "r", encoding="utf-8") as f:
        state = parse_state(f.read())
    
    current_round = int(round_num) if round_num.isdigit() else state["evolution"]["current_round"] + 1
    state["evolution"]["current_round"] = current_round
    
    # Reset stages for the new round based on backtrack target
    if backtrack_to:
        reset_stages = []
        if backtrack_to == "1":
            reset_stages = ["1. Understand", "2. Plan", "3. Design", "4. Execute", "5. Verify", "6. Deliver"]
        elif backtrack_to == "2":
            reset_stages = ["2. Plan", "3. Design", "4. Execute", "5. Verify", "6. Deliver"]
        elif backtrack_to == "3":
            reset_stages = ["3. Design", "4. Execute", "5. Verify", "6. Deliver"]
        elif backtrack_to == "4":
            reset_stages = ["4. Execute", "5. Verify", "6. Deliver"]
        elif backtrack_to == "5":
            reset_stages = ["5. Verify", "6. Deliver"]
        
        for stage_name in reset_stages:
            if stage_name in state["stage_tracker"]:
                state["stage_tracker"][stage_name] = {}
        
        # Also reset checkpoint tracker for affected stages
        for i in range(int(backtrack_to), 7):
            if str(i) in state["checkpoint_tracker"]:
                del state["checkpoint_tracker"][str(i)]
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(format_state(state))
    
    print(f"🔄 Evolution: Round {current_round} started")
    if backtrack_to:
        print(f"   Backtrack to Stage {backtrack_to}")
    return 0


def cmd_evolution_history(args):
    """读取进化历史。"""
    workspace = args.get("--workspace", os.getcwd())
    path = get_state_path(workspace)
    
    if not os.path.exists(path):
        print(f"❌ State file not found: {path}", file=sys.stderr)
        return 1
    
    with open(path, "r", encoding="utf-8") as f:
        state = parse_state(f.read())
    
    evolution = state.get("evolution", {})
    print(f"Current Round: {evolution.get('current_round', 1)} / {evolution.get('max_rounds', 6)}")
    print(f"History:")
    for entry in evolution.get("history", []):
        print(f"  Round {entry['round']}: {entry['score']} ({entry['improvements']} improvements) — {entry['status']}")
    return 0


def cmd_read(args):
    workspace = args.get("--workspace", os.getcwd())
    path = get_state_path(workspace)
    
    if not os.path.exists(path):
        print(f"❌ State file not found: {path}", file=sys.stderr)
        return 1
    
    with open(path, "r", encoding="utf-8") as f:
        print(f.read())
    return 0


def cmd_recover(args):
    workspace = args.get("--workspace", os.getcwd())
    path = get_state_path(workspace)
    
    if not os.path.exists(path):
        print(f"❌ State file not found: {path}", file=sys.stderr)
        return 1
    
    with open(path, "r", encoding="utf-8") as f:
        state = parse_state(f.read())
    
    evolution = state.get("evolution", {})
    current_round = evolution.get("current_round", 1)
    max_rounds = evolution.get("max_rounds", 6)
    
    # 找到最后一个未完成的阶段
    current_stage = None
    for stage_name in ["1. Understand", "2. Plan", "3. Design", "4. Execute", "5. Verify", "6. Deliver"]:
        info = state["stage_tracker"].get(stage_name, {})
        if info.get("status") == "🟡 In Progress":
            current_stage = stage_name
            break
        if info.get("status") != "✅ Completed":
            current_stage = stage_name
            break
    
    if current_stage:
        print(f"🔄 Recovery: Round {current_round}/{max_rounds}, resume from {current_stage}")
    else:
        # All stages completed — check if we should enter evolution
        history = evolution.get("history", [])
        if len(history) >= current_round:
            print(f"✅ Round {current_round} completed. Check if evolution needed.")
        else:
            print(f"✅ Round {current_round} stages completed. Ready for retrospective.")
    return 0


def cmd_escalate(args):
    workspace = args.get("--workspace", os.getcwd())
    reason = args.get("--reason", "")
    stage = args.get("--stage", "")
    
    path = get_state_path(workspace)
    if not os.path.exists(path):
        print(f"❌ State file not found: {path}", file=sys.stderr)
        return 1
    
    with open(path, "r", encoding="utf-8") as f:
        state = parse_state(f.read())
    
    state["escalation_log"].append({
        "time": now(),
        "stage": stage,
        "reason": reason
    })
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(format_state(state))
    
    print(f"🛑 Escalation logged at Stage {stage}: {reason}")
    return 0


def cmd_deliver(args):
    workspace = args.get("--workspace", os.getcwd())
    artifact = args.get("--artifact", "")
    
    path = get_state_path(workspace)
    if not os.path.exists(path):
        print(f"❌ State file not found: {path}", file=sys.stderr)
        return 1
    
    with open(path, "r", encoding="utf-8") as f:
        state = parse_state(f.read())
    
    if artifact:
        state["artifacts"].append({"done": True, "name": artifact})
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(format_state(state))
    
    print(f"✅ Deliverable recorded: {artifact}")
    return 0


def cmd_log(args):
    workspace = args.get("--workspace", os.getcwd())
    message = args.get("--message", "")
    
    log_path = get_log_path(workspace)
    entry = f"## [{now()}] — {message}\n\n"
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)
    
    print(f"📝 Log appended: {log_path}")
    return 0


def cmd_user_change(args):
    workspace = args.get("--workspace", os.getcwd())
    change = args.get("--change", "")
    scope = args.get("--scope", "minor")
    
    path = get_state_path(workspace)
    if not os.path.exists(path):
        print(f"❌ State file not found: {path}", file=sys.stderr)
        return 1
    
    with open(path, "r", encoding="utf-8") as f:
        state = parse_state(f.read())
    
    state["user_feedback"].append({
        "time": now(),
        "type": scope,
        "content": change
    })
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(format_state(state))
    
    print(f"📝 User change recorded ({scope}): {change}")
    return 0


def parse_args(argv):
    """简单解析 --key value 形式的参数。"""
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
        print("Usage: python goal_state.py <command> [options]")
        print("Commands: init, update-stage, checkpoint, retrospective, evolution, evolution-history,")
        print("          read, recover, escalate, deliver, log, user-change")
        return 1
    
    cmd = sys.argv[1]
    args = parse_args(sys.argv)
    
    commands = {
        "init": cmd_init,
        "update-stage": cmd_update_stage,
        "checkpoint": cmd_checkpoint,
        "retrospective": cmd_retrospective,
        "evolution": cmd_evolution,
        "evolution-history": cmd_evolution_history,
        "read": cmd_read,
        "recover": cmd_recover,
        "escalate": cmd_escalate,
        "deliver": cmd_deliver,
        "log": cmd_log,
        "user-change": cmd_user_change
    }
    
    handler = commands.get(cmd)
    if not handler:
        print(f"❌ Unknown command: {cmd}", file=sys.stderr)
        print(f"Available: {', '.join(commands.keys())}", file=sys.stderr)
        return 1
    
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
