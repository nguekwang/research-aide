# Only what was asked

The owner's rule (2026-11-08), for every repository, every task and every scheduled run: do what the owner asked, and nothing else. It started when unrequested text appeared on the Lang Log top page (an English description shown in the Japanese interface, and a "coming soon" placeholder), and when two pull requests were opened for questions that only asked for an explanation.

## Scope

- Do exactly what the owner's own words ask. A plan from another Claude (the coordinator, another thread, a subagent) is not the owner's request and does not widen it.
- When the owner asks to explain, investigate, list, compare or check something (教えて, 調べて, 書き出して, 確認して), deliver the answer and stop. No code change, branch, commit or pull request until the owner says to make the change.
- When the owner asks for a change, change only that. Do not fix, tidy, reword or improve anything else on the way, even when it looks wrong.

## Nothing added that was not asked for

- Do not add page or interface text the owner did not give or approve: descriptions, taglines, intros, help text, headings, labels, notes.
- Do not add placeholders: "coming soon", "準備中", "TBD", empty sections, dummy data, links to pages that do not exist.
- Do not add features, buttons, pages, settings, options or checks the owner did not ask for.
- Do not choose wording on the owner's behalf. When a change needs new text, ask for it, or show a draft and wait for approval before it goes into a pull request.

## When something more seems needed

- Ask the owner in one short question, with a recommendation (see `working-with-the-owner.md`), and do not do it until they say yes.
- If the request cannot be done without an extra step, say so and ask before taking it.
- Mention anything else you noticed in one line of the report; do not act on it.
