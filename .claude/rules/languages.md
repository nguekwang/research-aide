# Languages of a page

The owner's rules for every site or tool with text in more than one language (the personal site in about 20 languages, Lang Log in English and Japanese, and any later one).

- Every language shows the same thing. A change to page or interface text is not done until every language has it, in the same pull request. A repository's own rule file names where the text of each language lives and the check that fails when one is missing.
- Each language follows its own official documents (the owner's rule, 2026-11-05). Digits, dates, punctuation, brackets, list separators and other notation follow the conventions of that language's current official documents (government, legislature, national standards), not one style shared by all languages and not only what CLDR or common websites do. Record each choice and its source in the repository's rule file.
- Never convert notation in whole strings at build time (for example all digits): identifiers such as "i18n" and codes must keep their own characters.
- Data quoted from a source (names, titles, citations, codes) is not translated or re-punctuated; only the site's own text is.
