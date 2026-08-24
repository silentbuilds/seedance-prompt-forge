#!/usr/bin/env python3
"""Test the linter: it must pass clean prompts and catch broken ones.

    python3 scripts/run_tests.py
    python3 scripts/run_tests.py --guide path/to/official-guide.md

Without --guide, runs the committed fixtures only. With it, additionally re-runs every
filled example from the official prompt guide and fails if any produces an ERROR - a linter
that rejects the source material is worse than no linter.
"""
import argparse, hashlib, pathlib, re, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_ROOT = ROOT / "skills" / "seedance-prompt-forge"
LINT = SKILL_ROOT / "scripts" / "lint_prompt.py"
PLACEHOLDER = re.compile(r"<[a-z][^<>\n]{2,}>")


def lint(path, task="generic"):
    r = subprocess.run([sys.executable, str(LINT), str(path), "--task", task],
                       capture_output=True, text=True)
    return r.returncode, r.stdout


def lint_text(text, task="generic"):
    r = subprocess.run([sys.executable, str(LINT), "-", "--task", task], input=text,
                       capture_output=True, text=True)
    return r.returncode, r.stdout


def check_linter_regressions():
    """Every reproduced false-pass gets a matching safe case to prevent overcorrection."""
    cases = [
        ("an unbound cited reference is rejected",
         "@Image 1 appears in the scene.\n@Image 2 defines the scene.",
         "generic", "[ERROR] unbound-reference:", True),
        ("a bound cited reference remains valid", "@Image 1 defines the actor.",
         "generic", "[ERROR] unbound-reference:", False),
        ("collective reference binding is rejected",
         "@Images 1 through 4 define four characters respectively.",
         "generic", "[ERROR] collective-binding:", True),
        ("individual reference binding remains valid",
         "@Image 1 defines Character A.\n@Image 2 defines Character B.",
         "generic", "[ERROR] collective-binding:", False),
        ("lowercase one-word placeholder is rejected", "<subject> walks into frame.",
         "generic", "[ERROR] unfilled-placeholder:", True),
        ("capitalized subject label remains valid", "<Conservator> walks into frame.",
         "generic", "[ERROR] unfilled-placeholder:", False),
        ("two bound image references expose a numbering gap",
         "@Image 1 defines the actor.\n@Image 3 defines the prop.",
         "generic", "[ERROR] numbering-gap:", True),
        ("consecutive bound image references remain valid",
         "@Image 1 defines the actor.\n@Image 2 defines the prop.",
         "generic", "[ERROR] numbering-gap:", False),
        ("reversed timeline blocks are rejected",
         "5-10 seconds: finish.\n0-5 seconds: begin.",
         "generic", "[ERROR] timeline-order:", True),
        ("chronological timeline blocks remain valid",
         "0-5 seconds: begin.\n5-10 seconds: finish.",
         "generic", "[ERROR] timeline-order:", False),
        ("a reversed time range is rejected", "10-5 seconds: action.",
         "generic", "[ERROR] bad-range:", True),
        ("a forward time range remains valid", "5-10 seconds: action.",
         "generic", "[ERROR] bad-range:", False),
        ("overlapping timeline ranges are rejected",
         "0-5 seconds: begin.\n4-9 seconds: continue.",
         "generic", "[ERROR] overlapping-range:", True),
        ("consecutive timeline ranges remain valid",
         "0-5 seconds: begin.\n5-9 seconds: continue.",
         "generic", "[ERROR] overlapping-range:", False),
        ("per-second frequency demands are rejected", "Complete three actions in one second.",
         "generic", "[ERROR] frequency-demand:", True),
        ("paced action wording remains valid", "Complete three actions across three seconds.",
         "generic", "[ERROR] frequency-demand:", False),
        ("locked aspect ratios are rejected", "Extend @Video 1 in 16:9.",
         "extend", "[ERROR] locked-ratio:", True),
        ("locked-ratio tasks without a ratio remain valid", "Extend @Video 1.",
         "extend", "[ERROR] locked-ratio:", False),
        ("locked edit durations are rejected", "Edit @Video 1. Duration: 10 seconds.",
         "edit", "[ERROR] locked-duration:", True),
        ("edit prompts without a duration remain valid", "Edit @Video 1.",
         "edit", "[ERROR] locked-duration:", False),
        ("resolution is still reported for a locked-ratio task",
         "Resolution 4K.",
         "extend", "[WARN] param-in-prompt:", True),
        ("duration is still reported for a locked-ratio task",
         "Duration: 10 seconds.",
         "extend", "[WARN] param-in-prompt:", True),
        ("parameter-free locked-ratio prompts remain valid",
         "Extend @Video 1 after its final frame.",
         "extend", "[WARN] param-in-prompt:", False),
        ("scene references without exclusions are reported",
         "@Image 1 defines the gallery background.",
         "generic", "[WARN] missing-exclusion:", True),
        ("scene references with exclusions remain valid",
         "@Image 1 defines only the gallery layout. Do not use the people.",
         "generic", "[WARN] missing-exclusion:", False),
        ("replacement edits require timeline inheritance",
         "Edit @Video 1, the sole editing master. Replace exactly one lamp.",
         "edit", "[WARN] no-timeline-inheritance:", True),
        ("replacement edits require an explicit target count",
         "Edit @Video 1, the sole editing master. Replace the lamp.\n"
         "[Timeline Inheritance]\nInherit all motion.",
         "edit", "[WARN] no-count-lock:", True),
        ("complete replacement edit structure remains valid",
         "Edit @Video 1, the sole editing master. Replace exactly one lamp.\n"
         "[Timeline Inheritance]\nInherit all motion.",
         "edit", "[WARN] no-timeline-inheritance:", False),
        ("complete replacement edit count remains valid",
         "Edit @Video 1, the sole editing master. Replace exactly one lamp.\n"
         "[Timeline Inheritance]\nInherit all motion.",
         "edit", "[WARN] no-count-lock:", False),
        ("unbalanced dialogue markers are rejected", "The actor says: {Hello.",
         "generic", "[ERROR] unbalanced-dialogue:", True),
        ("balanced dialogue markers remain valid",
         "Dialogue language: English. The actor says: {Hello.}",
         "generic", "[ERROR] unbalanced-dialogue:", False),
        ("unbalanced subtitle markers are rejected", "【Chapter One",
         "generic", "[ERROR] unbalanced-subtitle:", True),
        ("balanced subtitle markers remain valid", "【Chapter One】",
         "generic", "[ERROR] unbalanced-subtitle:", False),
        ("non-Chinese dialogue without a language is reported", "The actor says: {Hello.}",
         "generic", "[WARN] unmarked-dialogue-language:", True),
        ("non-Chinese dialogue with a language remains valid",
         "Dialogue language: English. The actor says: {Hello.}",
         "generic", "[WARN] unmarked-dialogue-language:", False),
    ]
    checks = []
    for label, prompt, task, marker, expected in cases:
        _, out = lint_text(prompt, task)
        checks.append((label, (marker in out) is expected))
    return checks


def check_spec():
    """Frontmatter must satisfy the Agent Skills spec, or the skill silently fails to load
    in some agents. https://agentskills.io/specification"""
    t = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    fm = t.split("---")[1]
    name = re.search(r"^name:\s*(\S+)", fm, re.M)
    name = name.group(1) if name else ""
    desc = re.search(r"description:\s*>\n(.*?)\n\w[\w-]*:", fm, re.S)
    desc = " ".join(desc.group(1).split()) if desc else ""
    comp = re.search(r"compatibility:\s*>\n(.*?)\n\w[\w-]*:", fm, re.S)
    comp = " ".join(comp.group(1).split()) if comp else ""
    return [
        ("standard distributable path is skills/<skill-name>/SKILL.md",
         SKILL_ROOT.is_dir() and (SKILL_ROOT / "SKILL.md").is_file()),
        ("distributable skill includes its license",
         (SKILL_ROOT / "LICENSE").is_file()
         and (SKILL_ROOT / "LICENSE").read_bytes() == (ROOT / "LICENSE").read_bytes()),
        (f"name matches directory {SKILL_ROOT.name!r}", name == SKILL_ROOT.name),
        ("name is lowercase alphanumeric with single hyphens, 1-64 chars",
         bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name)) and len(name) <= 64),
        (f"description 1-1024 chars (is {len(desc)})", 0 < len(desc) <= 1024),
        (f"compatibility <=500 chars (is {len(comp)})", len(comp) <= 500),
        ("version lives in metadata, not top-level",
         not re.search(r"^version:", fm, re.M)),
        (f"SKILL.md body <=500 lines (is {len(t.splitlines())})",
         len(t.splitlines()) <= 500),
        ("file references one level deep", not re.search(r"references/\w+/", t)),
        ("every referenced file exists", all(
            (SKILL_ROOT / m).exists()
            for m in re.findall(r"`(references/[\w.-]+\.md)`", t))),
    ]


def check_bundle_fresh():
    """dist/ is generated. A stale bundle or zip ships wrong instructions to users."""
    names = ["seedance-prompt-forge.bundle.md", "seedance-prompt-forge.zip"]
    dist_files = [ROOT / "dist" / n for n in names]
    missing = [n for n, p in zip(names, dist_files) if not p.exists()]
    if missing:
        return False, f"dist/ missing {missing} - run scripts/build_bundle.py"
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in dist_files}
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_bundle.py")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return False, f"build_bundle.py failed:\n{r.stderr}"
    after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in dist_files}
    stale = [n for n in names if before[n] != after[n]]
    if stale:
        return False, (f"dist/ is stale ({', '.join(stale)}) - run "
                       "scripts/build_bundle.py and commit the result")
    return True, ""


def check_distribution():
    """The documented install path and fallback installer must stay safe and portable."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    checks = [
        ("README previews the skill before installation",
         "gh skill preview silentbuilds/seedance-prompt-forge seedance-prompt-forge" in readme),
        ("README uses the standard GitHub skill installer",
         "gh skill install silentbuilds/seedance-prompt-forge seedance-prompt-forge" in readme),
        ("README uses the current Codex personal skill path",
         "~/.agents/skills/" in readme and "~/.codex/skills/" not in readme),
    ]

    installer = ROOT / "scripts" / "install.sh"
    with tempfile.TemporaryDirectory() as tmp:
        scratch = pathlib.Path(tmp)
        project = scratch / "target-project"
        project.mkdir()

        missing_target = subprocess.run(
            ["bash", str(installer), "--project"], cwd=scratch,
            capture_output=True, text=True)
        checks.append(("--project requires an explicit target path",
                       missing_target.returncode != 0))

        first = subprocess.run(
            ["bash", str(installer), "--project", str(project)], cwd=scratch,
            capture_output=True, text=True)
        installed = project / ".agents" / "skills" / "seedance-prompt-forge"
        checks.append(("explicit project install writes to the requested project",
                       first.returncode == 0 and (installed / "SKILL.md").is_file()))

        if installed.is_dir():
            sentinel = installed / "keep-existing-install.txt"
            sentinel.write_text("preserve me", encoding="utf-8")
            refused = subprocess.run(
                ["bash", str(installer), "--project", str(project)], cwd=scratch,
                capture_output=True, text=True)
            checks.append(("existing installs are preserved unless --force is supplied",
                           refused.returncode != 0 and sentinel.is_file()))

            forced = subprocess.run(
                ["bash", str(installer), "--force", "--project", str(project)], cwd=scratch,
                capture_output=True, text=True)
            backups = list(installed.parent.glob("seedance-prompt-forge.backup-*"))
            checks.append(("--force replaces the install after creating a backup",
                           forced.returncode == 0
                           and (installed / "SKILL.md").is_file()
                           and any((backup / sentinel.name).is_file() for backup in backups)))

    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--guide", help="official prompt guide markdown, for regression testing")
    args = ap.parse_args()
    failures = []

    for label, ok in check_spec():
        print(f"{'ok  ' if ok else 'FAIL'} spec: {label}")
        if not ok:
            failures.append(f"spec violation: {label}")

    for label, ok in check_distribution():
        print(f"{'ok  ' if ok else 'FAIL'} distribution: {label}")
        if not ok:
            failures.append(f"distribution violation: {label}")

    for label, ok in check_linter_regressions():
        print(f"{'ok  ' if ok else 'FAIL'} linter: {label}")
        if not ok:
            failures.append(f"linter regression: {label}")

    ok, msg = check_bundle_fresh()
    print(f"{'ok  ' if ok else 'FAIL'} dist/ is up to date")
    if not ok:
        failures.append(msg)

    rc, out = lint(ROOT / "tests/fixtures/clean-prompt.txt")
    if rc != 0:
        failures.append(f"clean-prompt.txt should pass:\n{out}")
    else:
        print("ok   clean fixture passes")

    rc, out = lint(ROOT / "tests/fixtures/broken-prompt.txt", "edit")
    codes = set(re.findall(r"\[ERROR\] ([\w-]+):", out))
    expected = {"collective-binding", "unfilled-placeholder", "overlapping-range",
                "frequency-demand", "locked-ratio", "locked-duration"}
    if not expected <= codes:
        failures.append(f"broken-prompt.txt missed {sorted(expected - codes)}")
    else:
        print(f"ok   broken fixture caught all {len(expected)} expected errors")

    if args.guide:
        text = pathlib.Path(args.guide).read_text(encoding="utf-8").replace("\\", "")
        blocks = re.findall(r"```text\n(.*?)```", text, re.S)
        filled = [b for b in blocks
                  if not any(" " in m and m[1].islower() for m in PLACEHOLDER.findall(b))]
        errs = 0
        with tempfile.TemporaryDirectory() as d:
            for i, b in enumerate(filled):
                f = pathlib.Path(d) / f"ex{i:02d}.txt"
                f.write_text(b, encoding="utf-8")
                rc, out = lint(f)
                if rc != 0:
                    errs += 1
                    failures.append(f"official example {i} rejected:\n{out}")
        print(f"{'ok  ' if errs == 0 else 'FAIL'} {len(filled)} official examples, "
              f"{errs} rejected (must be 0)")

    if failures:
        print("\n" + "\n\n".join(failures), file=sys.stderr)
        print(f"\n{len(failures)} failure(s)", file=sys.stderr)
        return 1
    print("\nall tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
