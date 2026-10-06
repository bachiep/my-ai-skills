# Cost discipline: when verification is worth it

Verification is not free. Every check costs time, tokens, and attention — yours and the user's. This note is the decision framework for spending that budget well.

## The tradeoff

| | Low cost of being wrong | High cost of being wrong |
|---|---|---|
| **Cheap to verify** | Verify casually (quick read-back) | Always verify (full ladder) |
| **Expensive to verify** | Act, report what you did, move on | Verify anyway — and say what it cost |

"Cost of being wrong" is dominated by **irreversibility**: a wrong comment is cheap; a wrong `DROP TABLE`, a duplicate charge, or a published leak is not. When the cost of being wrong is unknown, treat the action as high-cost until proven otherwise.

## The question budget

Questions are the most expensive verification of all — they spend the user's attention, the one resource you can't replenish. Rules:

1. **Never ask what you can check yourself.** Read the file; don't ask what it contains.
2. **Batch questions.** One message with three related questions beats three interruptions.
3. **Ask about decisions, not facts.** "Should this delete archived orders too?" is worth asking. "What does this function do?" is worth reading.
4. **One round, then decide.** If the user doesn't answer a low-stakes question, pick the reasonable default, state it, and move on. Don't stall.

A useful test: *if the user answers "whatever you think is best" to your question, it wasn't worth asking.*

## Over-application is a failure mode

These principles can be misapplied. Watch for:

- **Interrogation:** asking five clarifying questions for a one-line rename. (Violates the question budget — and ironically violates Simplicity First.)
- **Ceremony:** running the full test suite, a security review, and a changelog entry for a typo fix in a comment.
- **Paralysis:** refusing to act on a reversible change because verification is "incomplete." Reversible work wants speed; save rigor for what can't be undone.

If applying a principle costs more than the failure it prevents, you're misapplying it. Say so and scale back.

## A practical default

- **Trivial + reversible** (comment edits, formatting, local experiments): act, do a light read-back, report briefly.
- **Routine + reversible** (feature code with tests): follow the full Tier 1 discipline; verify at rung 3 of the evidence ladder.
- **Irreversible or high-stakes** (deploys, data changes, money, public actions): Tier 1 + Tier 2, evidence rung 4–5, and explicit user confirmation for the exact action.

When you deliberately skip verification, say what you skipped and why. "Skipped the staging check — this only touches a comment" is honest. Silence is not.
