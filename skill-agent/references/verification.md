# Verification: the evidence ladder

Not all evidence is equal. Match the strength of evidence to the stakes of the claim.

## The ladder (weakest → strongest)

1. **No check** — "it should work." Worth nothing. Never report this as done.
2. **Exit code / success status** — the tool said ok. Establishes the call ran, not that the effect happened.
3. **Output inspection** — you read the tool's actual output and it shows the expected result.
4. **State check** — you independently read the resulting state (file contents, a database record, the live page).
5. **Independent corroboration** — a second, different check confirms the first (e.g. tests pass *and* the staging deploy behaves correctly).

Rule of thumb: reversible work needs level 3. Irreversible work needs level 4. High-stakes irreversible work (money, data loss, public actions) needs level 5.

## Practices

- **Read after write.** After editing a file, read the edited region back. Edits can land in the wrong place, match the wrong occurrence, or silently fail.
- **Reproduce before fixing.** For bugs: write the failing test first, watch it fail, then fix. A fix without a reproduction is a guess.
- **Distinguish listing from proving.** `ls` showing a file proves existence, not correctness. A `200 OK` proves reachability, not correct behavior.
- **Quote, don't paraphrase, critical values.** When a claim hinges on an exact value — an ID, a hash, an amount — copy it from the source.

## Anti-patterns

- Reporting "done" from a queued / accepted / running status. *Started* is not *finished*.
- Treating the absence of an error as proof of correctness.
- Verifying with the same method that produced the claim (e.g. asking the tool that wrote the file whether the file is correct).
- Citing a search-result snippet as proof of a live, changing fact (price, availability, account state). Snippets are leads, not evidence.
