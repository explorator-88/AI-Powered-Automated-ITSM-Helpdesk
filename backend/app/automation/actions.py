from datetime import datetime, timezone


def password_reset(username: str = "employee") -> dict:
    """
    Mock password-reset action.
    In production, this would call an approved identity-management API.
    """

    return {
        "action": "password_reset",
        "status": "success",
        "username": username,
        "message": "Password reset workflow completed successfully.",
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }


def account_unlock(username: str = "employee") -> dict:
    """
    Mock account-unlock action.
    In production, this would call an approved identity-management API.
    """

    return {
        "action": "account_unlock",
        "status": "success",
        "username": username,
        "message": "Account unlock workflow completed successfully.",
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }


def vpn_status_check() -> dict:
    """
    Mock VPN health check.
    """

    return {
        "action": "vpn_status_check",
        "status": "success",
        "vpn_status": "available",
        "message": "VPN service is currently available.",
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }


def clear_outlook_cache() -> dict:
    """
    Mock Outlook cache-clearing action.
    """

    return {
        "action": "clear_outlook_cache",
        "status": "success",
        "message": "Outlook cache clearing completed successfully.",
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }


def restart_outlook() -> dict:
    """
    Mock Outlook restart action.
    """

    return {
        "action": "restart_outlook",
        "status": "success",
        "message": "Outlook restart completed successfully.",
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }


# Only actions in this registry can be executed by the automation system.
ACTION_REGISTRY = {
    "password_reset": password_reset,
    "account_unlock": account_unlock,
    "vpn_status_check": vpn_status_check,
    "clear_outlook_cache": clear_outlook_cache,
    "restart_outlook": restart_outlook,
}


def execute_action(action_name: str, **kwargs) -> dict:
    """
    Execute only an approved automation action.
    """

    action = ACTION_REGISTRY.get(action_name)

    if action is None:
        return {
            "action": action_name,
            "status": "blocked",
            "message": "Automation action is not approved.",
        }

    return action(**kwargs)