# CI / CDK Workflows

This directory contains the **GitHub Actions workflows** used to validate and deploy the AWS CDK applications in this repository.

The CI/CD setup is intentionally simple but structured, designed to reflect **real-world CDK workflows** while remaining flexible for experimentation.

---

## 🎯 Goals of the CI

- Validate CDK code on every change
- Catch synthesis and configuration errors early
- Keep deployment logic explicit and predictable
- Support multi-stack, config-driven CDK apps
- Remain compatible with future multi-account setups

This is not meant to be a fully automated “push-to-prod” pipeline, but rather a **controlled and transparent CDK CI/CD flow**.

---

## 🧩 Workflows Overview

### 1️⃣ `ci.yml` — Continuous Integration

**Purpose:**  
Validate that the CDK codebase is healthy and can synthesize correctly.

**When it runs:**
- On pull requests to master

**What it does:**
- Sets up Python
- Installs dependencies
- Runs CDK synth on the app(s)
- Runs CDK diff --all

This workflow does **not deploy anything**.  
Its only responsibility is to fail fast if the infrastructure definition is broken.

Typical checks include:
- YAML config parsing
- Pydantic validation errors
- CDK construct and stack wiring
- Asset bundling errors

---

### 2️⃣ `deploy.yml` — Deployment Workflow

**Purpose:**  
Deploy CDK stacks to AWS in a controlled manner.

**Characteristics:**
- Explicit deployment (not every commit auto-deploys)
- Uses environment variables for account and region
- Designed to be safe for lab environments

**What it does:**
- Authenticates to AWS
- Bootstraps CDK if needed
- Deploys selected stacks using `cdk deploy`

This workflow assumes:
- The target AWS account and region are provided externally
- Stack dependencies are handled by CDK and/or SSM

---

### 3️⃣ `_cdk.yml` — Shared CDK Configuration

**Purpose:**  
Centralize CDK-related defaults shared across workflows.

Typical responsibilities:
- CDK CLI version pinning
- Reusable steps or settings
- Reducing duplication across workflows

This file exists to keep the CI workflows **clean and DRY**.

---

## 🔐 AWS Authentication Model

The workflows are designed to work with **externally provided AWS credentials**, typically via:

- Environment variables
- GitHub Secrets
- CI-provided identity mechanisms (OIDC-ready)

The CDK app itself does **not** hardcode:
- account IDs
- regions
- environment-specific values

This keeps the infrastructure portable and environment-agnostic.

---

## 🧪 CI Philosophy

- CI should **validate**, not guess
- Deployment should be **explicit**, not implicit
- Configuration errors should fail early
- Infrastructure should be reproducible from scratch

This setup prioritizes:
- clarity over cleverness
- predictability over automation magic

---

## 🧠 Notes & Caveats

- Destroying and redeploying stacks may require manual cleanup of some resources
  (e.g. CloudWatch Log Groups for Lambdas with fixed names)
- The workflows assume a lab-style environment
- Production hardening (approvals, promotions, multi-stage pipelines) can be added later

---

## 🚧 Future Improvements

Possible future extensions:
- Environment-based deployments (dev / prod)
- Stack-specific deploy workflows
- CDK diff checks in CI
- Policy validation (IAM least-privilege checks)

The current setup is intentionally minimal to keep iteration fast.
