# Simple and loosely coupled

The owner's rule (2026-11-22), for every repository and every task: always keep the structure as simple and as loosely coupled as possible.

- Each part (page, script, module, generator, workflow) does one job.
- Parts depend on each other only through what they publish (data files, `data-*` attributes, a shared module's functions, a workflow's inputs), never on how another part works inside.
- Behaviour needed in several places, such as one map on several pages, is written once and shared, not rewritten per page or per file.
- Choose the simpler design. Add a layer, a dependency or an abstraction only when the task needs it.
