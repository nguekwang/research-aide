# Links to the profile site

The owner's rule for every link to the personal site (`https://nguekwang.github.io/...`) from any other project, page or profile (tools, slides, business card, other sites).

- Add a `?ref=<source>` query parameter to every such link, so the personal site can tell where a visit came from. Example: `https://nguekwang.github.io/en/?ref=langlog`.
- `<source>` names where the link sits: lowercase letters and digits, words joined with `-` (such as `langlog`, `card`, `slides-<conference><year>`). Each tool uses one value on all its pages and records it in its own rule file.
- Put `ref` before any `#` fragment: `https://nguekwang.github.io/en/?ref=langlog#projects`. If the link already has a query, add `&ref=<source>`.
- Keep the value in one constant or config entry in the tool's code, not typed into each page.
- Links inside the personal site itself do not get a `ref`.
