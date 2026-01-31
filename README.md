# AWS CDK Learning (Python)

This repository is a **personal learning lab for AWS CDK using Python**.

The main goal is to **design, build, and deploy AWS infrastructure in a progressive, modular, and config-driven way**, applying Infrastructure as Code (IaC) best practices and real-world architectural patterns.

At the moment, the repository contains **a single CDK application**, but it is intentionally structured to host **multiple independent CDK apps** over time.

---

## 🎯 Repository Goals

- Learn AWS CDK through hands-on, real infrastructure
- Organize experiments in a long-living, versioned repository
- Apply **config-driven infrastructure patterns**
- Build reusable and composable CDK constructs
- Validate infrastructure configuration using typed models
- Integrate CI/CD pipelines with GitHub Actions
- Follow security best practices and least-privilege principles

---

## 🧱 High-Level Repository Structure

```
AWS-CDK-Learning/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── deploy.yml
│       └── _cdk.yml
├── apps/
│   └── employee_directory/
│       ├── app.py
│       ├── cdk.json
│       ├── pyproject.toml
│       ├── README.md
│       ├── config/
│       ├── employee_directory/
│       │   ├── stacks/
│       │   ├── constructs/
│       │   ├── models/
│       │   └── src/
│       └── cdk.out/
└── README.md
```

---

## 📁 Folder Overview

### `.github/workflows/`

Contains **CI/CD pipelines** implemented with GitHub Actions, including:

- CDK validation and synthesis
- Infrastructure diff checks
- Controlled deployments

Each workflow will be documented individually as the repository evolves.

---

### `apps/`

Root folder for **all CDK applications** in the repository.

Each subfolder inside `apps/` represents a **fully independent CDK app**, with its own:

- CDK entrypoint (`app.py`)
- Configuration (`cdk.json`, YAML files)
- Dependencies
- Stacks and constructs
- Documentation

All applications are designed to be **config-driven**, meaning infrastructure behavior is primarily defined via external configuration rather than hardcoded logic.

---

### `apps/employee_directory/`

Current CDK application used as a **base learning and experimentation project**.

Base project based on the first modules of [AWS Cloud Solutions Architect Professional from Coursera](https://www.coursera.org/professional-certificates/aws-cloud-solutions-architect)

This app explores a typical AWS architecture including:

- IAM
- EC2 (Flask application)
- AWS Lambda
- Amazon S3
- Decoupled CDK stacks
- Reusable constructs
- External YAML-based configuration validated with typed models

It serves as a **reference implementation** for patterns that can later be reused in other apps.

Detailed documentation for this app lives in its own `README.md`.

---

### `config/`

Holds **YAML-based configuration files** that define infrastructure behavior, such as:

- Resource parameters
- Stack-specific settings
- Feature toggles

This enables a **config-driven CDK approach**, reducing hardcoded values and making infrastructure changes easier and safer.

---

### `employee_directory/` (Python package)

Contains the actual Python source code for the CDK app, organized by responsibility:

- `stacks/` – CDK stack definitions
- `constructs/` – Reusable CDK constructs
- `models/` – Typed configuration models
- `src/` – Runtime source code (e.g. Lambda handlers)

---

### `cdk.out/`

Generated artifacts produced by CDK (`cdk synth`, `cdk deploy`).

This folder contains synthesized templates and asset metadata and is **not part of the logical design** of the repository.

---

## 🚧 Current Status

- Functional CI/CD pipeline
- One working CDK application
- Incremental documentation per app and component

---

## 📌 Notes

- This repository is **not intended to be a generic CDK template**
- It reflects real experimentation and learning over time
- Structure prioritizes clarity, scalability, and maintainability
- Documentation will continue to evolve alongside the code

---

*This repository evolves together with my AWS CDK learning journey.*
