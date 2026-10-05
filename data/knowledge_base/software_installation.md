---
article_id: KB006
title: Approved Software Installation Request
category: Software and Applications
subcategory: Software Installation
owner_group: Endpoint Management
priority: P3
version: "1.0"
last_reviewed: 2026-10-05
source_type: synthetic_enterprise_kb
audience: Employees
automation:
  eligible: true
  actions:
    - validate_software_catalogue
    - create_software_request
    - provision_approved_software
escalation_group: Endpoint Management
---

# Approved Software Installation Request

## Problem

An employee requires an approved software application to perform their work.

## Common Examples

- Visual Studio Code
- Google Chrome
- Python
- Git
- Postman
- 7-Zip

## Prerequisites

1. Identify the requested software.
2. Check whether the software exists in the approved software catalogue.
3. Determine whether the employee is eligible to receive the software.
4. Check whether manager approval is required.

## Resolution

1. Identify the requested application.
2. Search the approved software catalogue.
3. Verify employee eligibility.
4. Create a software request.
5. Route the request through the required approval workflow.
6. Provision the application after approval.
7. Validate installation status.

## Automation Eligibility

The following workflow may be automated for approved software:

1. Validate software against the catalogue.
2. Create the ServiceNow service request.
3. Trigger the approved provisioning workflow.
4. Validate provisioning status.
5. Update the service request.

## Escalation

Escalate to **Endpoint Management** when:

- The requested software is not in the approved catalogue.
- Approval is required but unavailable.
- Installation fails.
- The application requires special licensing.
- Security review is required.

## Security Rules

The system must not automatically install:

- Unapproved software.
- Unknown executables.
- Software that bypasses corporate security controls.

## Expected Outcome

The approved application is installed successfully and the ServiceNow request is updated with the final provisioning status.