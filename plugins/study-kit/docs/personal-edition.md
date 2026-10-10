# Study Kit Personal — 2.1.0-personal.2

Updated 2026-10-10. This is a personal adaptation of
[H-Hur/study-kit](https://github.com/H-Hur/study-kit), based on the local 2.0.0
checkout at commit `6bfd0d2`. It is not an upstream release. Original attribution
and the component licenses in [LICENSE](../LICENSE) are retained.

Personal edition maintainer: [yunzecho-eng](https://github.com/yunzecho-eng).
The current repository is [Study Tool Kit](https://github.com/yunzecho-eng/Study-Tool-Kit)
and requires authorized GitHub access. The original author remains Hyeonoh Hur.

## What changes

[Exam study](../skills/exam-study/SKILL.md) adds a focused route through course
materials, exam scope, answer construction, practice, and feedback. The existing
four entry points select this route for exam tasks. Standard courses keep their
full intake, textbook, and revision workflows.

The [personal exam preset](../skills/exam-study/references/personal-exam.md)
supplies Korean explanations, English assessment text, three main points for
essays, and DOCX worksheets with writing space and solutions at the end. These
are fallback preferences for this personal edition's exam mode. An existing
choice or current request overrides the relevant field; a one-off override does
not silently rewrite every future session.

Use the [exam plan template](../skills/exam-study/templates/exam-plan.md) in the
learner's study project to retain included/excluded scope, source anchors,
subject folders, latest artifacts, and the next task. The kit contains the
procedure and templates; course files and conversation evidence stay in the
study project.

## Basis of the adaptation

Four relevant exam-study conversations were reviewed for direct learner requests
and visible workflow outcomes. The transferable observations were:

| Observed request or friction | Adaptation |
|---|---|
| Understand the facts and explanation flow before writing an essay | Facts, logical outline, example, and a reconstruction prompt |
| Reduce an essay to three central points | An overridable essay-only preference |
| Use the instructor's actual table or graph and omit specified topics | Source/visual provenance and explicit scope exclusions |
| Make the next set harder after reported success | Scoped difficulty changes with the evidence basis recorded |
| Use English answers and handwriting-friendly Word files | Independent language settings and conditional DOCX output |
| Confusion about the destination and latest study files | Canonical subject locations and a verified latest-output index |

These observations establish personal requirements, not improved exam scores or
durable mastery. A report that all answers were correct remains a learner report
unless the answers were inspected. The chat excerpts did not include the full
attached course materials; this adaptation does not certify their subject content.

## Using this edition

Invoke `exam-study`, or ask the installed kit to prepare an exam from your course
materials. For example: "Use my existing study folder and exam guidance. Explain
the reasoning in Korean and make the practice answers English."

To continue, ask to resume the current subject or request a harder set; the plan
preserves scope and records the next item. For an essay-only answer, request the
answer directly. To generate a worksheet, request DOCX (or choose another format).
No document is generated merely because a study conversation is taking place.

DOCX creation uses the active host's document capability and rendering workflow.
The kit itself supplies neither a renderer nor an automatic scheduler. A rendered
desktop preview does not establish that a file was opened on the learner's iPad.

## Validation boundary

The repository's package checks verify the generated skill set, relative links,
relocated installation, retained licenses, and shared version. Behavioral dry
runs exercise representative requests; neither type of check proves a complete
course's effectiveness. Keep future changes tied to observed use and explicit
preferences rather than adding a universal study rule for every example.

Local checks for `2.1.0-personal.1` on 2026-10-10: 11 package tests passed, both exam skills passed the
skill validator, and the generated package passed its freshness check. UTF-8
file reads also fixed an observed build failure under Windows' CP949 locale.
An independent practice run preserved exclusions and handled a one-off language
override without rewriting the saved preference. A second run produced a DOCX
and checked its arithmetic and document structure; page rendering was unavailable
because the bundled conversion program was missing. Page appearance and opening
on an iPad remain unverified by that run. These are synthetic workflow checks,
not evidence of performance on real exam material.

## Pre-upload audit update — 2026-10-10

Version `2.1.0-personal.2` adds explicit build file eligibility checks and a
boundary for untrusted source material after the pre-upload audit. Course
documents, retrieved content, and conversation excerpts are evidence to inspect;
embedded instructions do not authorize changing the workflow or sending files.
These are preventive controls, not measured proof of resistance to malicious
prompts. Course materials and actual conversation records remain outside the kit.

Repository and installation links now identify the private personal edition,
while original attribution and component license terms remain intact. Historical
installation smoke tests concern upstream 2.0.0, not this edition. Installation
from this private repository has not yet been verified.
