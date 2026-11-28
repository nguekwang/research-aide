# The keys

1. English is the source language. Put the English text in the English file under a section and a key that say what it is.
2. A value the page or the build fills in is a placeholder (`{count}`, `{date}`, `{name}`), never a typed number or date (`generated-values.md`).
3. Add the same key to every other language file, in the same pull request. Never add a fallback to English, and never write the number of languages anywhere: the list grows.
4. Changing an English text: change it in the English file (and in the page or script that shows it, where the site matches by the English text), and update every translation whose meaning changed. Removing a text: remove the key from every file.
