# Security Policy

CineScout AI is an early-stage hackathon project. Please do not include API keys, service-account credentials, access tokens or other secrets in issues, pull requests or example files.

## Reporting a vulnerability

If you identify a security issue, please avoid publishing exploit details in a public issue while the problem is still unaddressed. Contact the repository owner through the GitHub profile associated with this repository and provide enough information to reproduce and assess the issue safely.

## Credential handling

Local credentials belong in environment variables or an untracked `.env` file. Production credentials will use managed Google Cloud identity and secret-management services rather than committed files.
