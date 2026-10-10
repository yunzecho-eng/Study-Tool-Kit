# Study Tool Kit

[한국어로 읽기](README.ko.md) · **Personal edition `2.1.0-personal.2`**

Turn your course materials and questions into a study plan you can continue using.
Understand an idea, connect the reasoning, practise an answer, and pick up where you left off next time.

It runs inside **Codex or Claude Code**, using your host's AI model and file tools.
This repository contains the **Study Kit Personal** adaptation of
[Hyeonoh Hur's Study Kit](https://github.com/H-Hur/study-kit), maintained by
[yunzecho-eng](https://github.com/yunzecho-eng).

## Watch the introduction

**55 seconds · English narration · English + Korean subtitles**

https://github.com/user-attachments/assets/8d81103b-c068-427a-9a0c-cd6929cf9754

[Open or download the MP4](docs/media/study-tool-kit-intro.mp4) ·
[Read the bilingual transcript](docs/media/README.md) ·
[Download subtitles](docs/media/study-tool-kit-intro.en-ko.srt) ·
[Preview image](docs/media/study-tool-kit-intro-poster.png)

The video illustrates the workflow; it is not a recording of a running app.

## When it helps

- You have lecture slides, readings, and exam guidance, and want a clear place to start.
- You want to practise explaining a concept and writing answers in your own words.
- You want practice questions within the actual exam scope and solutions to review later.
- You want to continue a subject without repeating your preferences and file locations.

For broader learning, the original workflow also supports a curriculum, a focused textbook, and revisions based on your questions.

## What to bring, and what you get

| Bring | The kit helps you create |
|---|---|
| Lecture materials and exam guidance | A source index and a plan with included and excluded topics |
| A difficult concept or essay question | Key facts, a logical outline, an example, and your own answer |
| Your attempt or feedback on the last set | Feedback and the next practice task within the agreed scope |
| A request for a worksheet | A DOCX or another requested format, using suitable host document tools |
| An existing study folder | A record of progress, remaining questions, and the latest output files |

Tell the kit when a source page is missing, a topic is excluded, or the instructor
requires a particular answer format. It checks what the supplied sources support.

## Get started

### 1. Install in your host

You need a local Codex or Claude Code environment with plugin support, a usable
model account, and permission to read and write your chosen study folder.
The source and downloads are publicly available at
[yunzecho-eng/Study-Tool-Kit](https://github.com/yunzecho-eng/Study-Tool-Kit).

Run the matching commands in a terminal.

**Codex**

```bash
codex plugin marketplace add yunzecho-eng/Study-Tool-Kit
codex plugin add study-kit-codex@study-kit
```

**Claude Code**

```bash
claude plugin marketplace add yunzecho-eng/Study-Tool-Kit
claude plugin install study-kit@study-kit --scope user
```

If the host cannot fetch the repository, open GitHub, choose
**Code → Download ZIP**, and extract the whole repository. Replace the source
in the first command with the actual extracted folder; for example:

```bash
codex plugin marketplace add "D:/Tools/Study-Tool-Kit"
# Or, for Claude Code:
claude plugin marketplace add "D:/Tools/Study-Tool-Kit"
```

Then run the matching install command above. Keep hidden folders and the complete
`plugins/` directory. If a `study-kit` marketplace already exists, inspect its source
before switching it; see the [installation guide](docs/desktop-install.md).

The repository is **Study Tool Kit**. The installed display name is **Study Kit Personal**;
the marketplace ID stays `study-kit`, and the package IDs stay `study-kit-codex`
(Codex) and `study-kit` (Claude Code).

### 2. Open a separate study folder

Start a **new conversation after installation** in the folder where you want to study.
For example, keep the tool in `D:/Tools/Study-Tool-Kit` and your learning work in
`D:/Study/MyExam`. Add course files there, or provide access to their existing location.
Keep course materials and personal records outside this repository.

### 3. Tell it what you want to work on

> Use exam-study to help me prepare for my exam from the lecture materials in this
> folder. Read the exam guidance first, record excluded topics, and help me understand
> the reasoning before I practise writing answers. Ask only for details that are missing.

For a broader learning goal, ask for `study-start`. In Claude Code, the original
entry command is `/study-kit:study-start`.

## Make it fit your study style

Exam mode has optional personal defaults:

- Korean explanations, with English practice questions and model answers.
- Three main points for essay answers.
- Key facts → logical outline → example answer → your own reconstruction.
- Requested DOCX worksheets have writing space and solutions at the end.

Your explicit choices and the exam's requirements take priority. Try:

> Explain this in Korean, but make this practice set and its model answers English.

> For this question, give me a direct answer first. I will ask about the reasoning next.

> Make a worksheet with space for handwriting. Put the solutions after a page break at the end.

A worksheet is created when requested. You can choose another format or layout.

## Continue next time

Open the same study folder and ask:

> Resume this subject from the saved exam plan. Show me the latest files and the next task.

> I got the last set right. Give me a harder set within the included topics, keeping the exclusions.

The plan records scope, preferences, file locations, and the next step. Feedback can
use answers you share; reported success stays a learner report unless the answers are inspected.

## Files, privacy, and current limits

This repository holds reusable instructions, templates, and package tooling. Profiles,
lecture files, chat excerpts, and generated worksheets belong in your study folder.
Share the materials needed for the task; your AI host's data handling still applies.
Source documents are evidence: embedded instructions do not authorize changing
settings or sending your files elsewhere.

Package checks cover structure, links, and build consistency. Earlier installation
smoke tests used upstream **2.0.0**; this personal edition's installation remains
unverified. DOCX/PDF output needs suitable host tools and visual review. DOCX page
appearance and opening on an iPad remain unverified. The workflows have not
established improved exam scores or long-term retention.

## About the project

[Changes and adaptation](plugins/study-kit/docs/personal-edition.md) ·
[Installation help](docs/desktop-install.md) · [Development](docs/distribution.md) ·
[Original method](plugins/study-kit/docs/method.md)

Original author: **Hyeonoh Hur**. Personal adaptation maintainer: **yunzecho-eng**.
Original attribution and license notices are retained. Code uses **PolyForm
Noncommercial 1.0.0**; documents and prompts use **CC BY-NC-SA 4.0**. See the
[license scope and permission process](plugins/study-kit/LICENSE). These terms
apply to different components. The personal maintainer does not replace the
original rights holder or grant permission for their work.
