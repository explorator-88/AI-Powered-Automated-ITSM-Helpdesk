---
article_id: KB002
title: Password Expired or Password Reset Required
category: Account and Access
subcategory: Password
owner_group: Identity and Access Management
priority: P2
version: "1.0"
last_reviewed: 2026-10-05
source_type: synthetic_enterprise_kb
audience: Employees
automation:
  eligible: true
  actions:
    - password_reset
    - account_unlock
escalation_group: Identity and Access Management
---

# Password Expired or Password Reset Required

## Problem

An employee cannot sign in because their corporate password has expired or the account has become locked after repeated unsuccessful authentication attempts.

## Common Symptoms

- Login reports that the password has expired.
- Authentication repeatedly fails.
- The account is reported as locked.
- Corporate applications reject the user's credentials.

## Prerequisites

1. Confirm the employee identity using the approved identity verification process.
2. Determine whether the account is expired, locked, or simply has an incorrect password.

## Resolution

### Password Expired

1. Start the approved password-reset workflow.
2. Verify employee identity.
3. Allow the employee to create a new password.
4. Confirm that the new password meets corporate password policy.
5. Ask the employee to sign in again.

### Account Locked

1. Verify employee identity.
2. Check account lock status.
3. Unlock the account through the approved identity-management workflow.
4. Ask the employee to authenticate again.

## Automation Eligibility

The following controlled actions may be executed automatically after identity verification:

- Password reset workflow.
- Account unlock workflow.

## Escalation

Escalate to **Identity and Access Management** when:

- Identity verification fails.
- The account remains locked after the approved process.
- The employee reports suspicious authentication activity.
- The identity-management service is unavailable.

## Security Rules

The helpdesk system must never:

- Store plaintext passwords.
- Ask users to provide passwords.
- Disable MFA.
- Bypass identity verification.

## Expected Outcome

The employee can securely authenticate using a valid corporate account.