# Working with the owner

How Claude works with the owner, in every repository and every task, including scheduled runs.

## Starting a task

- Read `CLAUDE.md` and the rule files first. Earlier decisions are recorded there; follow them rather than proposing something already decided. If a request conflicts with a recorded rule, say so and ask instead of overriding it.
- Rule files with `paths` load only when a matching file is opened. Before planning a change in a directory, read its rule file.
- Write the completion criteria (the conditions under which the task counts as done) at the start of the task. Rewrite them if the scope changes. Do not treat the task as finished until they are met.
- If a request can be read more than one way, start on the most likely reading and say which one you chose.
- One task, one thread: a request unrelated to the current task gets its own thread; only follow-ups to the same task stay.
- Scheduled runs start a new session with no memory of earlier ones, so a scheduled task's prompt tells Claude to read `CLAUDE.md` and these shared rules first.

## Asking questions

- Ask the owner with a decision card in the thread (one question, two to four options, one recommended).
- Use the owner's Q&A table (a claude.ai artifact named "Thesis 質問箱", collection `questions`) only when a task has far more questions than cards can carry, such as gathering requirements.
- Never ask what is already decided. Before asking, read the Q&A table (answered and applied rows too), the rule files and any shared decision files; if the answer is there, follow it. If an earlier answer must be reopened, say where it is and why.
- One decision per question, in one short sentence, with one recommended answer. Put explanations in the option text, not in the question.
- If the session cannot post cards, ask in the chat in the same short form.

## Reporting

- Talk to the owner in Japanese, in plain, short sentences. Explain technical terms. (Repository contents stay in English; see `english-first.md`.)
- Do not use emoji.
- A report gives the pull request link, what changed, and what stayed the same and why.
- End every report with three parts: Problems / What I checked / What I could not check, and leave one line in the execution log.
- For a draft, paste its full text in a code block in the reply as well as on any card.
- Claude prepares drafts and pull requests; the owner sends messages and merges.

## Spreading rules

- When the owner gives feedback that should hold beyond one task or repository, propose making it a rule and putting it in the right place: here in `research-aide` when it fits more than one repository (see `instruction-files.md`), otherwise in the repository's own rule file. Propose it even when the owner did not ask; if they decline, it may be proposed again later.
- When a shared rule is added or changed, check each repository that imports it for rules it now repeats or contradicts, and open pull requests there to remove or align them.
