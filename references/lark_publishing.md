# Lark publishing

Only publish to Lark **after** the local research package is already complete.

## Preferred workflow

1. finish the analysis locally
2. upload images once and capture tokens
3. assemble the final Markdown/XML layout offline
4. create or overwrite the doc in as few write operations as practical
5. verify final rendering

Do not treat the Lark doc as the working draft.

## Default rules

- If the user says to use their identity, explicitly pass `--as user`.
- Prefer token-first publishing and final-layout rebuilds over repeated append loops.
- Do **not** use `--caption` for screenshots by default; it can create unwanted white space beneath the image.
- If explanatory text is needed, add it as normal text below the image instead.
- If `docs +media-insert` is used, pass a **relative path** and run the command with `cwd` set to the image directory.

## Relative-path reminder

```bash
# Wrong
lark-cli docs +media-insert --doc "<DOC_ID>" --file "/absolute/path/shot.jpg"

# Better
cd /path/to/images && lark-cli docs +media-insert --doc "<DOC_ID>" --file ./shot.jpg --align center
```

## Publishing fallback

If publishing becomes brittle or noisy, stop live-editing the doc and deliver the local package first. The analysis should remain usable without the doc.

## Report structure

For a polished stakeholder-facing report, use [reference_doc_structure.md](reference_doc_structure.md) after the evidence package is already complete.
