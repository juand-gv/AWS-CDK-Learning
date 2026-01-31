# Employee Directory – CDK App

This is a **config-driven AWS CDK application** written in Python, used as a serious learning lab for building production-grade infrastructure patterns.

The goal of this app is not only to deploy resources, but to model **how real teams structure, validate, and evolve infrastructure** using CDK.

Currently following [AWS Cloud Technical Essentials](https://www.coursera.org/learn/aws-cloud-technical-essentials?specialization=aws-cloud-solutions-architect). 
Although they are using AWS console and I'm using CDK. 

---

## 🎯 Goals

- Practice **industrial-grade AWS CDK patterns**
- Separate **configuration from code**
- Use **strong validation** (YAML → Pydantic)
- Keep stacks **thin and declarative**
- Enable **safe cross-stack integration** via SSM
- Be easily extensible to multi-app / multi-environment setups

This app is intentionally opinionated and optimized for long-term maintainability rather than speed.

---

## 🧱 Architecture Overview

The application follows a consistent pattern across all stacks:

```
YAML (config)
↓
Pydantic models (validation)
↓
Reusable Constructs
↓
Thin CDK Stacks (orchestration only)
```


All **cross-stack communication** is done through **SSM Parameter Store**, avoiding tight coupling between stacks.

---

## 📂 Project Structure

```
apps/employee_directory
├── app.py # CDK app entrypoint
├── config/ # Infrastructure configuration (YAML)
│ ├── iam.yaml
│ ├── lambdas.yaml
│ ├── compute_flask.yaml
│ ├── s3.yaml
│ ├── ssm_paths.py # SSM path conventions
│ └── config_loader.py # YAML loaders + validation
│
├── employee_directory/
│ ├── constructs/ # Reusable infrastructure constructs
│ ├── models/ # Pydantic config models
│ ├── stacks/ # Thin CDK stacks
│ └── src/ # Runtime code (Lambda, Glue jobs, etc)
```

Key rule:
> **Config lives outside the Python package.  
> Code never depends on environment-specific values.**

---

## 🧩 Stacks

### IAM Stack (`IamStack`)
- Creates IAM roles using a config-driven approach
- Publishes critical role identifiers to SSM:
  - `role_arn`
  - `role_name`
- Designed to support **least-privilege evolution** over time

---

### S3 Stack (`S3Stack`)
- Creates S3 buckets based on declarative YAML config
- Publishes bucket identifiers to SSM:
  - `bucket_name`
  - `bucket_arn`
- Buckets are consumed by other stacks via SSM, not direct references

---

### Compute Stack (`ComputeStack`)
- Provisions EC2 instances running a Flask application
- Imports dependencies from SSM:
  - IAM role ARN
  - S3 bucket name
- Uses a reusable `ConfigurableEc2FlaskInstance` construct
- Publishes runtime identifiers to SSM:
  - `instance_id`
  - `security_group_id`

---

### Lambda Stack (`LambdaStack`)
- Deploys Lambda functions from YAML configuration
- Example Lambda:
  - **EC2 Kill Switch**
  - Scheduled via EventBridge
  - Shuts down running EC2 instances to avoid unnecessary costs
- Publishes Lambda identifiers to SSM:
  - `function_name`
  - `function_arn`

---

## 🔐 SSM-First Design

All shared infrastructure data is published to SSM using a stable naming convention:

```
/employee-directory/<account>/<service>/<resource>/<attribute>
```

Examples:

```
/employee-directory/123456789012/iam/ec2_role_arn
/employee-directory/123456789012/s3/buckets/photos/bucket_name
/employee-directory/123456789012/compute/ec2/web/instance_id
```

This allows:
- Loose coupling between stacks
- Easy future integrations
- Safe multi-stack and multi-account evolution

---

## 🧪 Environment Philosophy

This project is a **lab**, but designed with production in mind:

- Resources can be destroyed freely
- Naming is explicit and deterministic
- No hidden cross-stack references
- CI/CD-friendly (account and region injected externally)

The same structure can later be reused for real production environments with minimal changes.

---

## 🚀 Deployment

From `apps/employee_directory`:

```bash
cdk synth
cdk deploy IamStack
cdk deploy S3Stack
cdk deploy LambdaStack
cdk deploy ComputeStack
```

Stacks are intentionally deployable independently, as long as their SSM dependencies exist.

## 📌 Notes

* Lambda log groups may need manual cleanup when stacks are destroyed
* EC2 instances are identified by instance_id (ARN is not exposed by CDK)
* This app is intentionally verbose to prioritize clarity and learning

## 🧠 Why this exists

This app is used as:

* A personal reference for real consulting work
* A sandbox to test CDK design decisions
* A foundation for future multi-app CDK repositories
* It favors correctness and clarity over shortcuts.