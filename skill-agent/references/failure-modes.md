# Failure modes: failed, blocked, unknown

## The taxonomy

| State | Meaning | What to do |
|---|---|---|
| **Failed** | The action did not take effect (evidence confirms). | Fix the cause or try a genuinely different approach. Don't repeat the identical call and hope. |
| **Blocked** | Progress needs new input: a user decision, an approval, a credential, a result. | State the blocker, what would unblock it, and how the user can help. Continue independent work. Don't poll. |
| **Unknown** | Unclear whether the action took effect (timeout, ambiguous output, lost connection). | Investigate the actual state before acting again. This is the dangerous one — for irreversible actions, treat it as guilty until proven innocent. |

## Safe retry patterns

1. **Make it idempotent when you can.** "Ensure X exists" instead of "create X". Upserts over inserts. Declarative over imperative.
2. **Check-then-act.** Before a retry, query the current state: does the record exist? Was the message sent? Did the deploy land?
3. **Never retry blind on irreversible actions.** A timeout after "charge the card" means: check the ledger first, then decide.
4. **Back off, don't hammer.** On rate limits or transient errors, stop and report. Don't sleep-loop, switch endpoints, or lower the rate to dodge the limit.

## Preserving uncertainty across handoffs

When you hand work to another agent — or to a future session — carry the failure classification with it.

- Bad: *"Deploy didn't work, moving on."*
- Good: *"Deploy attempt timed out after 120s (unknown outcome). The release API shows no new release as of 14:02 UTC; build logs end at 'pushing image'. Next step: check the registry before retrying."*

The next agent should never have to re-derive what you already learned. Uncertainty you preserve is work you save.
