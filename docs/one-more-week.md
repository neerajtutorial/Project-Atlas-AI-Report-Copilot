# What I would do with one more week

1. Replace deterministic routing with a typed LangGraph state machine and explicit transitions for router, retrieval, calculator, critic, writer, and escalation.
2. Move retrieval and SQL access behind separate least-privilege credentials; add statement timeouts, a read-only MySQL account, query allowlisting and audit logs.
3. Add hybrid vector + keyword retrieval, a reranker, source freshness handling and page-aware PDF extraction including tables/charts.
4. Build an entailment-based citation critic that checks each numeric claim against exact supporting spans; reject any uncited number.
5. Add an analyst ticket queue and status workflow in the CI3 portal, plus authenticated user sessions and CSRF-protected feedback.
6. Measure p50/p95 latency, token usage and real per-request cost; add a semantic cache with entitlement-aware cache keys.
7. Run the 25+ question set in CI, manually label expected behavior, report precision/recall for citations, refusals, conflicts and escalation, and publish failures without hiding them.
8. Add threat-model review, secret scanning, dependency pinning, API rate limits and an end-to-end test of the Docker stack.