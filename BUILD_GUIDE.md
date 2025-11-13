# BUILD_GUIDE.md - Step-by-step implementation (Option D)
Generated: 2025-11-13T034229Z

This guide walks you through implementing the RL Book Ecosystem from the scaffold.

PHASE 0: PREP
1. Unzip repo_scaffold.zip and open it locally.
2. Review README.md and BUILD_GUIDE.md.
3. Create GitHub repo and push scaffold to branch `feature/bootstrap`:
   git init
   git add .
   git commit -m "bootstrap scaffold"
   git branch -M main
   gh repo create <owner>/rl-book-ecosystem --public --source=. --remote=origin
   git push -u origin main

PHASE 1: QUEUE + E2E TESTS
1. Populate data/jobs/inbox/testjob.json and run queue daemon locally:
   python3 scripts/queue/queue_daemon.py
2. Confirm outbox receives processed job.

PHASE 2: INDEX BUILD
1. Run index builder stub:
   python3 src/build_index.py
2. Confirm data/index/meta.json exists

PHASE 3: COMPOSER + DRAFTS
1. Run composer stub:
   python3 scripts/agents/composer.py
2. Confirm drafts/sample_section.md created

PHASE 4: CI & PAGES
1. Push branch to GitHub and ensure Pages workflow runs (pages.yml)
2. Inspect Actions logs and site build artifact

PHASE 5: OPS & BACKUPS
1. Add GDRIVE_SA_JSON secret (see ops/drive-automation.md)
2. Implement scripts/index/backup_index.py and enable index-backup workflow

PHASE 6: ADVANCED (Optional)
- Integrate advanced stubs (reflexive pipelines, CEL, GraphRAG) from advanced-blueprint-v2.zip

VERIFICATION
- Use verification_checklist.md to capture evidence after each phase.
