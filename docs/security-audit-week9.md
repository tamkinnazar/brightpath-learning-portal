# Week 9 IAM Security Audit

**Project:** BrightPath Academy Capstone Project  
**Date:** May 2026  
**Reviewed By:** Nesar Ahmad Andar (Security Review) 

## Objective

Review Google Cloud IAM permissions and verify that team access follows the Principle of Least Privilege.

## Team IAM Assignments

| Team Member | Project Role | GitHub Username | GCP IAM Role | Justification |
|------------|-------------|----------------|-------------|-------------|
| Nesar Ahmad Andar | DevSecOps Engineer / GCP Owner | Nesarahmad234 | Editor | Responsible for IAM management, Terraform deployment, CI/CD pipeline, Secret Manager, and Cloud infrastructure administration & Security Review|
| Tamkin Nazari | Project Lead / GitHub Owner | tamkinnazar | Viewer | Responsible for project coordination, architecture planning, repository management, and branch protection |
| Mohammad Qader | Backend Engineer | qaderayoubi19-dot | Editor | Responsible for backend application development, Cloud Run configuration, Cloud SQL integration, and deployment support |
| Aziz Ahadi | Frontend Engineer | azizahadi04 | Viewer | Responsible for frontend development, user interface testing, and application integration |
| Tresor Liongo Langombo | Security Reviewer | Matrix-1979 | Viewer | Responsible for IAM auditing, security reviews, compliance verification, and security documentation |

## Audit Findings

- IAM permissions were reviewed in Google Cloud Console.
- Editor permissions were granted only to members responsible for infrastructure management and deployment activities.
- Viewer permissions were granted to members whose responsibilities do not require administrative access.
- No unnecessary Owner permissions were assigned to team members.
- Access assignments align with the Principle of Least Privilege.

## Security Assessment

**PASS**

The current IAM configuration supports team responsibilities while minimizing unnecessary privileges. No excessive permissions were identified during the review.

## Recommendations

- Continue using least-privilege access throughout the project.
- Review IAM assignments before final deployment in Week 11.
- Remove any temporary permissions that are no longer required.
- Monitor Cloud Audit Logs for unexpected administrative activity.

## Approval

Security Reviewer: Nesar Ahmad Andar

Date Reviewed: June 2026