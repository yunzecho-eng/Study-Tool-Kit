---
name: study-publish
description: Revise and publish the textbook, and send it to the learner
---

Read the [runtime notes](../../docs/codex-runtime.md) once per task before following this procedure.


For an exam worksheet or answer document, including a continuation recorded as
active exam mode in `docs/exam-plan.md`, follow the document workflow in
[exam-study](../exam-study/SKILL.md). Apply the selected format and artifact
language, verify the rendered file, and update the subject's latest-file index.
That route does not require `docs/textbook.html` or two PDF editions. An explicit
request to publish the standard textbook uses the steps below instead.

1. **Open `docs/textbook-revisions.md` first.** Fold in every waiting item. If a large item
   must be split, tell the learner and settle the scope of this edition.
2. Amend `docs/textbook.html` under the conventions of the [`textbook-authoring`](../textbook-authoring/SKILL.md) skill and
   raise the edition label.
3. Check conventions, style, and figures with the [`textbook-auditor`](../textbook-auditor/SKILL.md) agent. Fold the findings
   into this edition or return them to the pending list.
4. Build both editions, exercise and answer, with the [`textbook-publish`](../textbook-publish/SKILL.md) skill, and verify the
   page counts.
5. Return the files in the current conversation by default. Send them externally only
   when the learner has authorized that delivery and a suitable tool is available.
   Otherwise state that they have not been sent. Do not expose target identifiers or tokens.
6. Change the status of each reflected item to `reflected (edition N)`, move it to the
   reflection history, and record the publication in `docs/worklog.md`.
