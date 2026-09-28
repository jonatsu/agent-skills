<!-- Internal README template — team codebases, services, internal tools. Focus
on onboarding a new teammate and operational knowledge. Replace placeholders;
drop unused sections. Do not invent contact details or URLs. -->

# {{SERVICE_NAME}}

{{ONE_SENTENCE_DESCRIPTION}}

**Team**: {{TEAM_OR_CHANNEL}} **On-call**: {{ROTATION_OR_CONTACT}}

## Overview

{{WHAT_IT_DOES_AND_WHERE_IT_FITS}}

### Dependencies

- **Upstream**: {{SERVICES_THIS_DEPENDS_ON}}
- **Downstream**: {{SERVICES_THAT_DEPEND_ON_THIS}}

## Local development

### Prerequisites

- {{REQUIRED_TOOL_AND_VERSION}}
- {{ACCESS_OR_VPN}}

### Environment variables

| Variable | Description | Where to get it |
| -- | -- | -- |
| `{{VAR}}` | {{DESCRIPTION}} | {{SOURCE}} |

### Running locally

```sh
{{RUN_AND_TEST_COMMANDS}}
```

## Architecture

{{SYSTEM_DESIGN_OR_DIAGRAM_LINK}}

### Key files

| Path | Purpose |
| -- | -- |
| `{{PATH}}` | {{WHAT_IT_DOES}} |

## Deployment

{{HOW_TO_DEPLOY_OR_LINK}}

## Runbooks

### {{COMMON_TASK}}

{{STEPS}}

## Troubleshooting

### {{COMMON_PROBLEM}}

**Symptom**: {{SYMPTOM}} **Cause**: {{CAUSE}} **Fix**: {{FIX}}

## Related docs

- {{DESIGN_DOC_LINK}}
- {{DASHBOARD_LINK}}
