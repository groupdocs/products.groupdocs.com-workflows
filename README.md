# Workflows for products.groupdocs.com

Repository containing GitHub Actions workflows to build & deploy products.groupdocs.com.

## Architecture

This repository uses a **unified workflow architecture** with a reusable workflow pattern:

- **`deploy_product.yml`** - Reusable workflow containing all common deployment logic
- **`deploy_{product}.yml`** - Thin wrapper workflows for each product family that call the reusable workflow

## Product Deployment Workflows

All product workflows follow the same pattern and use the `deploy_product.yml` reusable workflow:

| Workflow | Product Family | Special Features |
|----------|---------------|-----------------|
| `deploy_annotation.yml` | annotation | - |
| `deploy_assembly.yml` | assembly | - |
| `deploy_classification.yml` | classification | - |
| `deploy_comparison.yml` | comparison | Uploads images folder |
| `deploy_conversion.yml` | conversion | - |
| `deploy_editor.yml` | editor | - |
| `deploy_markdown.yml` | markdown | - |
| `deploy_merger.yml` | merger | - |
| `deploy_metadata.yml` | metadata | - |
| `deploy_parser.yml` | parser | - |
| `deploy_redaction.yml` | redaction | - |
| `deploy_search.yml` | search | - |
| `deploy_signature.yml` | signature | - |
| `deploy_total.yml` | total | - |
| `deploy_viewer.yml` | viewer | - |
| `deploy_watermark.yml` | watermark | - |

## Other Workflows

### `deploy_home.yml`

Deploys the home page and handles general content changes.

### `deploy_custom.yml`

Custom deployment workflow for specific branches (currently configured for `license-popup` branch). Used for special deployment scenarios.

### `scan_locales.yml`

Utility workflow to scan content folders and analyze locale information. Can be run manually via workflow_dispatch.

## Supported Locales

All product workflows support the following locales:
- `en` (English - default)
- `de` (German)
- `es` (Spanish)
- `fa` (Farsi)
- `fr` (French)
- `id` (Indonesian)
- `it` (Italian)
- `ja` (Japanese)
- `ko` (Korean)
- `pt` (Portuguese)
- `ru` (Russian)
- `th` (Thai)
- `uk` (Ukrainian)
- `vi` (Vietnamese)
- `zh` (Chinese)

## Environment Configuration

### Staging Environment

- **Base URL:** `https://products-qa.groupdocs.com/`
- **S3 Bucket:** `products-qa.groupdocs.com`
- **Config:** `config-staging.toml`
- **Triggered by:** Push to `main` branch, `staging-complete` dispatch

### Production Environment

- **Base URL:** `https://products.groupdocs.com/`
- **S3 Bucket:** `products.groupdocs.com`
- **Config:** `config-production.toml`
- **Triggered by:** Push to `production` branch, `production-complete` dispatch

## Adding a New Product Workflow

To add a new product workflow:

1. Create `deploy_{product_name}.yml` in `.github/workflows/`
2. Copy the structure from an existing workflow (e.g., `deploy_assembly.yml`)
3. Update:
   - Workflow name
   - Path trigger (`content/{product_name}/**`)
   - `product_family` parameter
   - Set `upload_images: true` if the product has an images folder to upload

Example:
```yaml
name: Deploy NewProduct

on:
  push:
    branches: [ main, production ]
    paths:
       - 'content/newproduct/**'
  # ... other triggers

jobs:
  deploy:
    uses: ./.github/workflows/deploy_product.yml
    with:
      product_family: "newproduct"
      default_deploy_scope: "index_pages_only"
      upload_images: false
      environment: ${{ inputs.environment }}
      deploy_scope: ${{ inputs.deploy_scope }}
    secrets: inherit
```

## Maintenance

- **Updating deployment logic:** Edit `deploy_product.yml` - changes apply to all products
- **Updating a specific product:** Edit the corresponding `deploy_{product}.yml` wrapper
- **Adding new locales:** Update `supported_locales` in `deploy_product.yml`

## Requirements

Common keys
  - `REPO_TOKEN` - Token to access products.groupdocs.com repository

S3/CF Keys
  - `ACCESS_KEY` - AWS access key ID (for S3 deployments)
  - `SECRET_ACCESS` - AWS secret access key (for S3 deployments)
  - `CACHE_INVALIDATION_API_ENDPOINT` - Cache invalidation API endpoint

Ceph Keys
  - `CEPH_ACCESS_KEY_ID` - Ceph access key ID (for Ceph deployments)
  - `CEPH_SECRET_ACCESS_KEY` - Ceph secret access key (for Ceph deployments)
  - `CEPH_QA_ENDPOINT` - Ceph endpoint URL for QA/staging environment
  - `CEPH_PROD_ENDPOINT` - Ceph endpoint URL for production environment
  - `BUNNYNET_ACCESS_KEY` - BunnyNet API access key for cache invalidation
  - `BUNNYNET_PURGE_URL` - BunnyNet cache purge API endpoint