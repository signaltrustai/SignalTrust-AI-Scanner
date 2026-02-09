# Launch Checklist

Comprehensive pre-launch checklist for SignalTrust AI.

## Technical Readiness
- [ ] Agents running and healthy (crypto, stock, whale, news, coordinator, supervisor) — confirm against current production roster.
- [ ] Core API endpoints responding with 200s (auth, scan, analysis, notifications).
- [ ] Web app loads without console errors; critical flows exercised (login, scan, dashboard).
- [ ] Render deployment uses correct environment variables and secrets; latest image deployed.

## Security Checks
- [ ] Secrets stored in env/Render secrets; no secrets in repo or logs.
- [ ] HTTPS enforced; CORS configured appropriately.
- [ ] Admin routes and payment bypass protections verified; least-privilege roles intact.
- [ ] Basic OWASP checks pass (auth/session, input validation, rate limiting where expected).

## Payment Flow Tests
- [ ] Card payment happy path (auth, capture) succeeds.
- [ ] Payment failure path shows proper errors; no charges occur.
- [ ] PayPal/alt methods (if enabled) succeed and fail gracefully.
- [ ] Subscription limits and upgrade/downgrade flows enforced; webhooks processed.

## Colab Notebook Verification
- [ ] Colab notebook opens and executes all cells without errors.
- [ ] API keys/secrets pulled from env; no hardcoded credentials.
- [ ] Example outputs match expected format (charts, tables, signals).

## Marketing Assets
- [ ] Logos, brand colors, and templates finalized and accessible.
- [ ] Landing page hero, feature graphics, and screenshots updated.
- [ ] One-pager / deck links verified.

## Social Media Scheduling
- [ ] Launch posts drafted (Twitter/X, LinkedIn, Discord, others).
- [ ] Scheduling set in chosen tool; tracking links (UTM) applied.
- [ ] Community/Discord announcement copy approved.

## Email Sequences
- [ ] Pre-launch warmup, launch day, and post-launch drip sequences loaded.
- [ ] Links and CTAs tested; unsubscribe flow verified.
- [ ] Segmentation rules (prospects, customers, trials) configured.

## Final Go/No-Go
- [ ] Monitoring and alerting active (agents, API latency/errors, payments).
- [ ] Rollback plan documented; backups verified.
- [ ] Stakeholder approvals recorded; owner named for launch window.
- [ ] Green light given in launch channel.
