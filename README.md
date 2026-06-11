# BrightPath Learning Portal

![CIS 410](https://img.shields.io/badge/CIS%20410-Capstone%20Project-blue)
![Python](https://img.shields.io/badge/Python-Flask-green)
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple)

## 🏢 Company Profile & Mission

* **Company Name:** BrightPath Academy
* **Industry / Sector:** Education Technology / Online Learning
* **Company Size:** 50-employee startup
* **Headquarters / Region:** Seattle, WA — serving students across the United States
* **Founded Year:** 2025

### 🎯 Mission Statement
To provide students with a secure and modern online learning platform that supports accessible education for everyone.

### 📝 Problem Statement
Many students and teachers need a simple and secure platform to manage online learning, assignments, and course materials in one centralized location. BrightPath Learning Portal mitigates credential exposure and application vulnerabilities by embedding automated security controls straight into the production container ecosystem.

***

## 👥 Team Members, Roles & Accountabilities

Our team operates under a strict role-based structure mirroring real-world corporate DevSecOps teams:

| Name | Project Role | Individual Structural Responsibility |
| :--- | :--- | :--- |
| **Tamkin Nazari** | **Project Lead & Repo Owner** | Owns repository management, established/enforced branch protection rules, handles final feature merging. |
| **Mohammad Qader** | **Backend Engineer** | Developed Flask API logic, managed application route authentication, constructed the Dockerfile base. |
| **Aziz** | **Frontend Engineer** | Designed user-facing UI Flask HTML/CSS templates and integrated them with backend endpoints. |
| **Nesar Ahmad Andar** | **DevSecOps Engineer** | Built the GitHub Actions pipeline, managed the automated Terraform runs, established OIDC authentication. |
| **Tresor Liongo Langombo** | **Security Reviewer** | Executed mandatory pull request security reviews, audited platform IAM, and led compliance testing. |

***

## 🛠️ Technology Stack & Decoupled Architecture

* **Frontend:** Flask templates (HTML5 / CSS3 structured UI layout)
* **Backend:** Python Flask API engine
* **Database:** Cloud SQL (MySQL) — *Completely decoupled from compute layer per capstone requirements.*
* **Container Registry:** GCP Artifact Registry
* **Compute / Hosting:** Google Cloud Run (Serverless Container Platform)
* **Infrastructure as Code (IaC):** Terraform 
* **CI/CD Automation Platform:** GitHub Actions
* **Security Scanning Infrastructure:** Snyk (SAST, SCA, and Container Vulnerability Scanning)
* **Secrets Management Ecosystem:** Google Secret Manager

***

## 🔀 Secure Git & Collaboration Workflow

To fulfill our collaborative security metrics, direct pushes to the `main` branch are **100% blocked** by repository administrative configurations. Every line of production code followed this exact zero-trust path:

```text
[Feature Branch Created] ➔ [Code Pushed] ➔ [PR Opened] ➔ [Snyk Automated Scans Run] ➔ [Security Reviewer Approves] ➔ [Project Lead Merges]