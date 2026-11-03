# Deployment options and cost safety

The application image is built from the root Dockerfile. Local development and the CI integration suite use Docker Compose.

## Render

1. Import this repository into Render and select the Blueprint from render.yaml.
2. Review the plan and database limits in the Render dashboard before creating resources. Free database offerings can have storage, uptime and expiry limits; do not upgrade without approval.
3. Confirm DATABASE_URL is linked to the created database and wait for /health to pass.

Render Blueprints deploy a Dockerfile-backed web service and a separate managed database. They do not deploy this repository's Docker Compose file as one Compose stack.

## Railway

Create a project from this repository, deploy the root Dockerfile, add a PostgreSQL service, and set DATABASE_URL to Railway's reference variable for that database. Review current usage-based pricing and configure spending limits before deployment. Railway is not automatically free.

## Vercel

Vercel is used for the static frontend, not as a Docker Compose host. Set the Vercel project root to frontend. Before deploying, replace YOUR-RENDER-SERVICE in frontend/vercel.json with the real origin of a separately deployed backend. The rewrite rules proxy API requests to that backend. Review CORS and custom-domain settings before exposing real data.

## AWS CloudFormation

No AWS stack is launched by this repository or CI. A CloudFormation template that provisions compute, networking, public IP addresses, storage or a database can create charges even when an account has promotional credits. Free Tier eligibility depends on account age, region, resource type and current offer. Therefore AWS deployment remains a manual, account-owner-approved step: keep the account on its Free plan, inspect the cost estimate and billing controls, and do not launch any resource unless the console explicitly confirms it is covered by the remaining free allowance. Do not add AWS credentials to GitHub Actions until this review is complete.

## CI/CD

GitHub Actions runs frontend, backend, Docker build, Compose integration and Playwright E2E tests. Provider redeploy hooks require account-specific secrets and an explicit billing review; no cloud credentials or paid resources are created automatically.


## GitHub Actions deployment secrets

The optional deploy workflow is gated on successful completion of both CI workflows for the same commit on main. Configure only the providers you intend to use:

- RENDER_DEPLOY_HOOK_URL: Render production deploy hook URL.
- RAILWAY_TOKEN and RAILWAY_SERVICE_ID; optionally RAILWAY_ENVIRONMENT (defaults to production).
- VERCEL_TOKEN, VERCEL_ORG_ID and VERCEL_PROJECT_ID for the frontend project.

Before enabling Railway or Render, review each provider's current billing model and set usage limits. Vercel's rewrite destination in frontend/vercel.json must point to the actual backend host. Missing secrets cause that provider step to be skipped; AWS is deliberately excluded from automatic deployment until a Free-plan-compatible design is verified by the account owner.
