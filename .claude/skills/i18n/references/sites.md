# Each site's own facts

Read the site's rule files below before the other steps; they name where the text lives, the languages, who writes which language, notation such as digits, and the check that fails when a language lacks a text. A new site with text in several languages adds its line here.

- Lang Log (`lang-log/lang-log.github.io`): `.claude/rules/interface-text.md` (text in `i18n/<code>.yaml`, languages in `LANGS`, check `python3 tools/build_i18n.py`, who translates) and `.claude/rules/fonts.md`.
- The personal site (`nguekwang/nguekwang.github.io`): `.claude/rules/data.md` (text in `data/i18n/<code>.yaml`, languages in `data/site.yaml`, check `python3 tools/build.py --check`), `.claude/rules/writing-style.md` (wording, machine translation, `protected_terms`) and `.claude/rules/digits.md`.
