---
article_id: KB005
title: Slow Laptop or Poor System Performance
category: Hardware and Performance
subcategory: Laptop Performance
owner_group: End User Computing
priority: P3
version: "1.0"
last_reviewed: 2026-10-05
source_type: synthetic_enterprise_kb
audience: Employees
automation:
  eligible: true
  actions:
    - check_system_resources
    - clear_temp_cache
    - restart_device
escalation_group: End User Computing
---

# Slow Laptop or Poor System Performance

## Problem

An employee reports that their corporate laptop is running slowly, applications are taking longer than expected to respond, or the system becomes temporarily unresponsive.

## Common Symptoms

- Applications open slowly.
- System becomes unresponsive.
- High CPU or memory utilization.
- Insufficient temporary storage.
- Performance degrades after extended uptime.

## Prerequisites

1. Confirm whether the problem affects one application or the entire system.
2. Determine whether the problem is temporary or persistent.
3. Check available system resources.

## Resolution

1. Close unnecessary applications.
2. Check CPU and memory utilization.
3. Check available disk space.
4. Clear approved temporary files or application cache.
5. Restart the affected application.
6. Restart the device if required.
7. Recheck system performance.

## Automation Eligibility

The following actions may be automated:

- Check CPU and memory utilization.
- Clear approved temporary cache.
- Restart the device when explicitly authorized by the workflow.

## Escalation

Escalate to **End User Computing** when:

- Performance remains poor after troubleshooting.
- Hardware diagnostics report an error.
- Disk or memory capacity appears insufficient.
- The device repeatedly becomes unresponsive.

## Do Not

- Delete user documents.
- Modify system security settings.
- Disable endpoint protection.
- Execute arbitrary cleanup commands.

## Expected Outcome

The laptop returns to an acceptable level of performance and the employee can continue normal work.