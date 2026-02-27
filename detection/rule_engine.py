def detect_suspicious(log):
    if log.action == "assign_admin_role":
        return True
    if log.ip.startswith("203."):
        return True
    return False
