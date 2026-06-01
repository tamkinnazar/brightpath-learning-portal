BrightPath Learning Portal Architecture



flowchart LR

A[Developer Laptop] --> B[Docker Build & Local Test]

B --> C[GitHub Repository]

C --> D[GitHub Actions CI/CD Pipeline]

D -. OIDC (No Service Account Keys) .-> D2[Workload Identity Federation]

D --> AR[Artifact Registry]

AR --> CR[Cloud Run - Frontend + Backend Containers]

CR --> SM["Secret Manager (Runtime Secrets)"]

CR --> VPC["VPC (Private Network) + Subnets"]

VPC --> SQL["Cloud SQL Database (PostgreSQL/MySQL)"]