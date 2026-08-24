# Sources and provenance

Last verified: **2026-08-24**

## Primary source

| Field | Value |
|---|---|
| Guide | [Dreamina Seedance 2.5 Prompt Writing Guide](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh) |
| Locale | English |
| Document status | The document UI displayed “Last updated: Aug 12” when verified; it did not display a year. |
| Chinese edition | [Seedance 2.5 提示词指南](https://bytedance.larkoffice.com/docx/OsiUdR1OxoDqvnxsK8LczYx7nPd) |
| Linked official release | [BytePlus ModelArk documentation](https://docs.byteplus.com/en/docs/ModelArk/2607689) |

The English guide is the normative content source for this repository. The Chinese edition and
the linked BytePlus release are cross-checking surfaces, not substitutes for recording which
edition was used.

## Applicability

- The guide names **Dreamina Seedance 2.5** and describes both the generation page and API.
- Treat a rule as applicable to BytePlus/API only where the guide explicitly mentions the API
  or the corresponding BytePlus documentation confirms it.
- Do not carry these rules to other Seedance versions, providers, or product surfaces without
  checking their current documentation and available controls.
- “Other parameters depend on the options currently available” is a platform boundary: the
  skill must not invent controls that are absent from the user's surface.

## Evidence levels

### Documented guidance

The source guide documents the prompt formula, reference-material roles and limits, dialogue
syntax, scene-by-scene reference selection, long-video staging, editing and extension patterns,
advanced modes, and the pre-submission checklist. It also documents the last-known parameter
behavior below:

| Task | Last-known behavior in the guide |
|---|---|
| General generation | Configurable parameters are set on the generation page or through the API, not in the prompt. |
| Video editing | Aspect ratio and approximate input duration are locked; processing may differ by about 0.3 seconds. |
| First-frame / first-and-last-frame | Aspect ratio follows the first image; duration can be set. First and last images should share an aspect ratio. |
| Video extension | Aspect ratio follows the input video; extension duration can be set. |

### Tested implementation

The deterministic linter translates mechanically checkable parts of the guide into repository
guardrails. Its error/warning severity, pattern matching, and wording are implementation choices,
not additional claims about model capability. Every advertised lint rule has a failing and a safe
regression case in `scripts/run_tests.py`.

### Working inference

The guide requires consistent `@Image`, `@Video`, and `@Audio` mappings but does not document how
the platform assigns their numbers. Treating numbers as upload order is therefore a working
assumption. The runtime instructions label it as an assumption and require the user to verify the
mapping shown by their interface.

## Maintenance

When the source changes:

1. Record the new verification date and the source document's displayed update label.
2. Identify which statements are documented guidance, tested implementation, or inference.
3. Update the runtime skill and references without silently broadening product applicability.
4. Run `python3 scripts/run_tests.py --guide /path/to/authorized-guide-export.md` when an
   authorized local Markdown export is available, then regenerate `dist/`.
