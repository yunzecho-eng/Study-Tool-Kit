---
name: exam-study
description: Prepare and continue exam study from the learner's course materials and exam guidance, with scoped practice, answer construction, and optional writing worksheets. Use for exam preparation, past-question practice, essay rehearsal, or resuming an existing exam plan. General study and textbook work keep their existing workflows.
---

Read the [runtime notes](../../docs/runtime.md) once per task before following this procedure.

# Exam study — understand, construct, and practise an answer

This mode supports the learner preparing their own answers. It reuses the profile,
source index, and planning records without requiring a complete textbook. Keep all
learner records and outputs in the separate study project, never in this kit.

## Establish the current task and settings

Read the current request and any existing `docs/learner-profile.md`, `REFERENCES.md`,
and `docs/exam-plan.md` relevant to the subject. Reuse settled answers; ask only for
missing details that affect this task, such as the exam format or included range.
Consult the relevant background and goal questions in
[learner intake](../learner-intake/SKILL.md) when needed, without restarting its
entry flow or making a new intake a prerequisite for a bounded exam question.
Other workflows may route here; apply their relevant general guidance without
recursively re-entering the routing instructions.

In this personal edition, use the [personal exam preset](references/personal-exam.md)
only to fill unset preferences in this mode. The current request wins over stored
choices; explicit course/profile choices win over preset fallbacks. Briefly state
applied defaults when first entering the mode and keep working. Treat a one-off
request as a local override unless the learner asks to retain it.

Keep explanation language separate from question and model-answer language. An
English worksheet does not imply English explanations in the conversation, and
a Korean explanation request does not silently translate the English assessment.
Respect the exam's stated language requirements; surface a conflict with a learner
request rather than pretending the resulting practice meets those requirements.

## Fix the study location and exam scope

Resolve the subject's canonical study and output folders from the learner's latest
correction, existing project records, and actual filesystem paths. Check that the
paths exist before relying on them; a stated new destination can be created for
the requested output. Do not guess a folder from the subject's name, silently
switch to a similarly named folder, or search unrelated projects for study history.
If two real locations remain ambiguous, clarify the destination before writing;
continue source review or an inline answer meanwhile. A corrected folder does not
authorize moving or deleting earlier files.

Create or update `docs/exam-plan.md` using the
[exam plan template](templates/exam-plan.md). If an equivalent plan already lives
elsewhere in the project, make `docs/exam-plan.md` a short pointer to it and update
the canonical plan, rather than maintaining duplicate content. Mark active exam
mode in the canonical plan (and in a pointer, if used). Preserve each subject's
settings and scope in a named subsection when switching subjects; changing the
current subject does not erase the others. Keep this record small: scope and source
anchors, the current practice objective, subject output index, and continuation.
Integrate existing curriculum sessions by reference when useful; do not rebuild
the course or write a full textbook to satisfy a request for a few practice items.

Determine scope in this order:

1. The learner's current included and excluded ranges, interpreted against the
   supplied exam instructions and instructor announcements.
2. The relevant course materials and their actual pages, slides, tables, or figures.
3. Supplementary references only for an identified gap, clearly distinguished
   from the assessed course content.

An explicit exclusion stays excluded when the learner asks for harder questions.
Record its source or the learner's instruction and any later explicit change.
If the instructor's guidance conflicts with the learner's chosen practice range,
show the difference and label the practice scope; do not silently change either.
If no exam guidance is available, label coverage provisional rather than claiming
that a topic will be tested.

Use [source indexing](../source-index/SKILL.md) to record the materials actually
used and their verification state. Instructor material sets exam coverage; it
does not make a factual inconsistency disappear. Name discrepancies and separate
the course's expected framing from any correction supported by other sources.

## Build an answer the learner can reconstruct

For explanation and essay rehearsal, use this sequence at the scale of the request:

1. **Core facts** — the few definitions, relationships, or observations needed,
   anchored to the source and page or slide where available.
2. **Logical outline** — show how those facts lead to the answer, including the
   links between claims rather than only a list of terms.
3. **Example answer** — a model in the requested answer language and length,
   labelled as an example rather than an official answer unless verified as such.
4. **Learner reconstruction** — offer a prompt or outline from which the learner
   can write their own answer, then respond to their attempt if they submit one.

For essay answers only, use the configured number of main points; the personal
fallback is three. This is not a limit on facts, calculation steps, multiple-choice
options, or every explanation. An explicit request for two points or a different
format takes precedence. If the learner requests the answer directly, give it;
do not require an attempt or a quiz before showing the requested explanation.

For a practice set, keep example answers in the requested answer section so that
the question pages remain usable for writing. Fix a short self-check criterion
with each item: what a sufficient answer must explain or calculate. Use misses to
identify a missing link or a passage that needs a better explanation, not to build
an instructor-style score or mastery ledger.

## Use tables, graphs, and difficulty honestly

When a question uses a course table or graph, inspect the original visual as well
as any extracted text. Preserve units, labels, legends, and the relevant range.
Label every included visual close to the visual as one of:

- **Original** — reproduced from the identified course source and page/slide.
- **Reconstructed** — redrawn from that source; identify any simplification and
  verify the data and axes against the original.
- **Synthetic practice example** — invented values or an illustrative diagram,
  clearly separated from the professor's actual material.

Do not silently repair missing data or present invented numbers as a source
figure. If the original is unavailable, say what cannot be verified and avoid
questions whose answer depends on unreadable details.

When the learner reports that a set was easy or all answers were correct, increase
difficulty within the included range: ask for a justification, interpretation,
comparison, less guided answer, or a combination of already included ideas. Mark
the basis as **learner-reported** unless an attempt was actually inspected; for an
inspected attempt, name the specific reasoning seen. Neither is proof of durable
mastery. An explicit request for harder practice needs no scoring prerequisite.
Record only the current level, why it changed, and the next practice task.

## Produce a worksheet only when requested

An ordinary study exchange stays in the conversation. For a requested document,
apply the learner's format and device preferences; the personal preset supplies
DOCX for iPad writing only when no format has been chosen. Use the active host's
available document workflow or Documents skill, reading its instructions before
creating or editing a DOCX. This kit does not bundle a document renderer.

- Put the questions first, with writing space sized for the expected answer.
- Put solutions and self-check criteria at the end, after a clear page break,
  unless the learner asks for another arrangement. Preserve question numbering.
- Keep tables, figures, and writing space readable at the requested page size;
  avoid clipped content and answer hints in the exercise pages.
- Render and inspect every page with the host's document workflow. Correct
  overflow, broken figures, awkward page breaks, and missing answer space, then
  verify the revised rendering. Report whether device opening was actually tested;
  desktop rendering alone does not establish iPad compatibility.

If generation or rendering is unavailable, state exactly what was produced and
what remains unverified. Do not claim that a text outline is a DOCX or that an
unrendered document passed visual checks. Return a usable draft when possible.

## Save just enough to continue

After substantive work, update the subject's output index in the exam plan with
the actual file paths, purpose, date/revision, and latest version. Confirm files
exist before returning links. Preserve earlier versions; mark replacements as
superseded rather than silently overwriting a learner's working copy. Use stable
relative links within the project and actual absolute paths in delivery messages
when supported by the host.

Keep a compact continuation block: current subject and included range, last
completed task, next item, unresolved learner question, and latest output links.
Record lasting preference changes in the profile and source changes in
`REFERENCES.md`; do not copy private conversations into the reusable kit. On
resuming, read this state and continue the next item without repeating intake.

Personal edition update — 2026-10-10: this mode captures reported exam-study
preferences and observed friction around answer structure, scope, document
layout, and output locations. Its defaults are personal choices, not measured
claims that these methods improve exam performance.
