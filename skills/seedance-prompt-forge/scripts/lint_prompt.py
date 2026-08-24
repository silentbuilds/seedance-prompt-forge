#!/usr/bin/env python3
"""Deterministic checks for a Seedance 2.5 prompt.

Checks only what can be verified mechanically. Judgement calls stay in
references/checklist.md. Exit code 1 if any ERROR is found, 0 otherwise.

Usage:
    python3 lint_prompt.py prompt.txt
    python3 lint_prompt.py prompt.txt --task edit
    cat prompt.txt | python3 lint_prompt.py -
"""

import argparse
import re
import sys

REF = re.compile(r"@(Image|Video|Audio)\s*(\d+)", re.I)
ROLE_VERB = re.compile(
    r"\b(defines?|corresponds? to|references?|is the|are the|is a|is used|provides?|"
    r"shows?|edit|extend|as keyframes)\b", re.I
)
LABEL_ROLE = re.compile(r"^\s*[\w ]{3,40}:\s.*@(Image|Video|Audio)\s*\d+", re.I | re.M)
SCENEY = re.compile(
    r"\b(scene|background|environment|location|room|studio|lab|gallery|street|interior|"
    r"space|layout|setting|workshop|greenhouse|landscape)\b", re.I
)
PLACEHOLDER = re.compile(r"<[a-z][^<>\n]{2,}>")
TIME_RANGE = re.compile(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(?:seconds|secs?|s)\b", re.I)
COLLECTIVE = re.compile(
    r"@(?:Image|Video|Audio)s?\s*\d+\s*(?:through|to|-|–)\s*\d+.{0,60}?"
    r"(respectively|each|define|are)", re.I | re.S
)
RATIO = re.compile(r"\b(16:9|9:16|4:3|3:4|1:1|21:9|aspect ratio|widescreen|vertical format)\b", re.I)
DURATION = re.compile(
    r"\b(\d+\s*(?:-|to)?\s*\d*\s*(?:second|sec|minute)s?\s+(?:long|video|clip|duration)"
    r"|duration\s*(?:of|:)|make it \d+\s*seconds)\b", re.I
)
RESOLUTION = re.compile(r"\b(\d{3,4}p|4K|1080|720|resolution)\b", re.I)
FREQUENCY = re.compile(r"\b(\w+|\d+)\s+(?:actions?|movements?|cuts?|shots?)\s+in\s+one\s+second\b", re.I)

LOCKED = {
    "edit": ["ratio", "duration"],
    "extend": ["ratio"],
    "firstlast": ["ratio"],
    "keyframe": ["ratio"],
}


class Report:
    def __init__(self):
        self.rows = []

    def add(self, level, code, msg):
        self.rows.append((level, code, msg))

    @property
    def errors(self):
        return [r for r in self.rows if r[0] == "ERROR"]

    def render(self):
        if not self.rows:
            return "PASS - no mechanical issues found."
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        out = []
        for level, code, msg in sorted(self.rows, key=lambda r: order[r[0]]):
            out.append(f"[{level}] {code}: {msg}")
        n_err = len(self.errors)
        out.append("")
        out.append(f"{n_err} error(s), {len(self.rows) - n_err} warning(s)/note(s).")
        return "\n".join(out)


def role_lines(text):
    """Lines that assign a role to a reference.

    Accepts all documented orderings:
        '@Image 1 defines ...'          reference first
        '<Character A> corresponds to @Image 1'   reference last
        'Appearance and clothing: @Image 1.'      label form
        'Edit @Video 1 ...' / 'Extend @Video 1 ...'
    """
    found = {}
    for line in text.splitlines():
        if not (ROLE_VERB.search(line) or LABEL_ROLE.search(line)):
            continue
        for kind, num in REF.findall(line):
            found.setdefault((kind.capitalize(), int(num)), []).append(line.strip())
    return found


def check_bindings(text, rep):
    cited = {(k.capitalize(), int(n)) for k, n in REF.findall(text)}
    if not cited:
        return
    roles = role_lines(text)
    # A text with no role lines at all is almost certainly an excerpt, not a whole
    # prompt. Report, but do not fail the run on it.
    level = "ERROR" if roles else "WARN"
    for ref in sorted(cited):
        if ref not in roles:
            rep.add(level, "unbound-reference",
                    f"@{ref[0]} {ref[1]} is used but never given a role "
                    f"(no line like '@{ref[0]} {ref[1]} defines ...')."
                    + ("" if roles else " No role lines found at all - is this a fragment?"))
    for kind in ("Image", "Video", "Audio"):
        nums = sorted(n for k, n in cited if k == kind)
        bound = [n for k, n in roles if k == kind]
        if not nums or len(bound) < 3:
            # too few bound references of this kind to establish an intended sequence
            continue
        if nums[0] != 1:
            rep.add("WARN", "numbering-start",
                    f"@{kind} numbering starts at {nums[0]}, not 1.")
        gaps = [n for n in range(nums[0], nums[-1] + 1) if n not in nums]
        if gaps:
            rep.add("ERROR", "numbering-gap",
                    f"@{kind} numbering skips {gaps} (present: {nums}). "
                    "Gaps make the material order ambiguous.")


def check_exclusions(text, rep):
    roles = role_lines(text)
    for (kind, num), lines in sorted(roles.items()):
        if kind != "Image":
            continue
        blob = " ".join(lines)
        low = blob.lower()
        if "do not" in low or "only" in low:
            continue
        # The guide asks for exclusions where leakage is plausible - chiefly scene and
        # environment references. A narrow subject reference does not need one.
        if SCENEY.search(blob):
            rep.add("WARN", "missing-exclusion",
                    f"@{kind} {num} references a scene or environment but states no exclusion. "
                    "Add 'Do not use the people in the image' or an 'only ...' scope.")


def check_collective(text, rep):
    m = COLLECTIVE.search(text)
    if m:
        rep.add("ERROR", "collective-binding",
                f"Collective reference binding found: {m.group(0)[:70].strip()!r}. "
                "Bind each subject to its material individually.")


def check_placeholders(text, rep):
    # strip fenced code that is explicitly marked as a template
    hits = {m.group(0) for m in PLACEHOLDER.finditer(text)}
    # angle-bracket subject names like <Conservator> are single capitalised words - allowed
    unfilled = {h for h in hits if " " in h and h[1].islower()}
    if unfilled:
        rep.add("ERROR", "unfilled-placeholder",
                f"{len(unfilled)} unfilled placeholder(s): "
                + ", ".join(sorted(unfilled)[:5])
                + ("..." if len(unfilled) > 5 else ""))


def check_timing(text, rep):
    ranges = [(float(a), float(b), m.group(0)) for m in TIME_RANGE.finditer(text)
              for a, b in [m.groups()]]
    for a, b, raw in ranges:
        if b <= a:
            rep.add("ERROR", "bad-range", f"Time range {raw!r} does not move forward.")
    ordered = sorted(ranges, key=lambda r: r[0])
    for (a1, b1, r1), (a2, b2, r2) in zip(ordered, ordered[1:]):
        if a2 < b1:
            rep.add("ERROR", "overlapping-range",
                    f"{r1!r} and {r2!r} overlap. Ranges must be consecutive and non-overlapping.")
        elif a2 > b1:
            rep.add("WARN", "gap-in-timeline",
                    f"Unallocated time between {b1:g}s and {a2:g}s.")
    m = FREQUENCY.search(text)
    if m:
        rep.add("ERROR", "frequency-demand",
                f"{m.group(0)!r} demands a rate, not a budget. Timestamps allocate time to events.")


def check_locked_params(text, task, rep):
    locked = LOCKED.get(task, [])
    if "ratio" in locked:
        m = RATIO.search(text)
        if m:
            rep.add("ERROR", "locked-ratio",
                    f"Aspect ratio {m.group(0)!r} requested, but this task type locks the ratio "
                    "to the input material. It cannot be set on the page, the API, or the prompt.")
    if "duration" in locked:
        m = DURATION.search(text)
        if m:
            rep.add("ERROR", "locked-duration",
                    f"Duration {m.group(0)!r} requested, but video editing locks duration to the "
                    "input (+/- ~0.3s).")


def check_params_in_prompt(text, rep, task):
    if task in LOCKED:
        return  # already covered, with a stronger message
    for label, pat in (("aspect ratio", RATIO), ("duration", DURATION), ("resolution", RESOLUTION)):
        m = pat.search(text)
        if m:
            rep.add("WARN", "param-in-prompt",
                    f"{label.capitalize()} {m.group(0)!r} appears in the prompt. Set generation "
                    "parameters on the generation page or through the API instead.")


def check_edit_structure(text, rep, task):
    if task != "edit":
        return
    low = text.lower()
    if "sole editing master" not in low:
        rep.add("WARN", "no-master",
                "No 'sole editing master' declaration for the source video.")
    if "timeline inheritance" not in low and re.search(r"\breplace\b", low):
        rep.add("WARN", "no-timeline-inheritance",
                "Replacement edit without a [Timeline Inheritance] block. The target may not "
                "follow the original's motion, occlusion, and exits.")
    if not re.search(r"\bexactly (one|two|three|\d+)\b", low) and re.search(r"\breplace\b", low):
        rep.add("WARN", "no-count-lock",
                "Replacement edit without an explicit target count ('exactly one ...'). "
                "Duplicated subjects are the common failure here.")


def check_dialogue(text, rep):
    if text.count("{") != text.count("}"):
        rep.add("ERROR", "unbalanced-dialogue", "Unbalanced {} dialogue markers.")
    if text.count("\u3010") != text.count("\u3011"):
        rep.add("ERROR", "unbalanced-subtitle", "Unbalanced 【】 subtitle markers.")
    for m in re.finditer(r"\{([^}]{1,400})\}", text):
        line = m.group(1)
        if not re.search(r"[\u4e00-\u9fff]", line):
            before = text[max(0, m.start() - 220):m.start()].lower()
            if "language" not in before and not re.search(
                    r"\b(in|speaks?|says?)\s+\w*\s*(english|japanese|korean|french|spanish|"
                    r"german|thai|vietnamese|malay|indonesian|arabic|portuguese|italian|russian|hindi)",
                    before):
                rep.add("WARN", "unmarked-dialogue-language",
                        f"Non-Chinese dialogue {line[:40]!r} has no language stated before it.")


def main():
    ap = argparse.ArgumentParser(description="Lint a Seedance 2.5 prompt.")
    ap.add_argument("path", help="prompt file, or - for stdin")
    ap.add_argument("--task", default="generic",
                    choices=["generic", "edit", "extend", "firstlast", "keyframe",
                             "longvideo", "oneclick", "transition"],
                    help="task type; enables locked-parameter and structure checks")
    args = ap.parse_args()

    text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()

    rep = Report()
    check_bindings(text, rep)
    check_exclusions(text, rep)
    check_collective(text, rep)
    check_placeholders(text, rep)
    check_timing(text, rep)
    check_locked_params(text, args.task, rep)
    check_params_in_prompt(text, rep, args.task)
    check_edit_structure(text, rep, args.task)
    check_dialogue(text, rep)

    print(rep.render())
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
