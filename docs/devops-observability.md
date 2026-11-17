# DevOps and Observability — implementation guide

## Environments

- Production: existing Render Blueprint in `render.yaml`, connected to `main` and using `fixflow-db`.
- Development: import `render.development.yaml` as a second Render Blueprint. It creates `fixflow-web-dev` from branch `development` and a separate database `fixflow-db-dev`.
- Never point the two services at the same database.

Both Render plans must be checked in the Render dashboard before creation. Free-plan availability, sleeping behavior, database expiry and limits can change.

## CI/CD

- GitHub Actions runs CI and Compose E2E checks on `main` and `development`.
- The Development deployment workflow waits until both test workflows pass for the same commit, then triggers the Render Development deploy hook.
- Configure a Render deploy hook for the Development service and save it as GitHub Environment secret `development / RENDER_DEV_DEPLOY_HOOK_URL`.
- Production promotion is a manual `workflow_dispatch` workflow. It deploys a selected full commit SHA through the Render API only after verifying both CI workflows succeeded for that commit.
- Configure GitHub Environment `production` with `RENDER_API_KEY` and `RENDER_PROD_SERVICE_ID`.
- In Settings → Environments → production, add required reviewers if approval before the job is desired. The workflow itself is manual; environment protection adds a second approval gate.
- To promote a tested development commit, open Actions → Promote Development to Production → Run workflow. Select the `development` branch and supply the full SHA from the development commit if needed. Verify that commit has passed CI before promoting it.

## Observability

Run the local monitoring stack using the instructions in `observability/README.md`. It includes OpenTelemetry Collector, Prometheus, Grafana, Alertmanager and the AI on-call responder. The dashboard is provisioned automatically.

## Required account setup

Repository code cannot create external Render resources or access private account settings. The account owner must:
1. Import the second Blueprint from `render.development.yaml`.
2. Create the Render Development deploy hook.
3. Add the GitHub Environment secrets described above.
4. Optionally set GitHub production required reviewers.
5. Add `OPENAI_API_KEY` to the local `.env` to enable real model-based incident analysis. Add `SLACK_WEBHOOK_URL` only if Slack delivery is wanted.

No credentials should be committed to Git.
