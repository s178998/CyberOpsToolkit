# -------------------- Permissions / Groups --------------------
user_groups = {
    "Dr_Smith_1001": ["Dean"],
    "Dr_Williams_1003": ["CIO"],
    "Dr_Brown_1004": ["Department_Head"],
    "TA_Miller_1007": ["TA"]
}

groups_permissions = {
    "Dean": ["create_user", "view_logs", "change_roles"],
    "CIO": ["manage_it_assets", "view_system_settings"],
    "Department_Head": ["view_users", "update_user"],
    "TA": []
}

def can_user_perform(username, permission: str | list):
    """
    Checks if a user has the requested permission(s) based on their groups.
    """
    groups = user_groups.get(username, [])
    user_perms = set()
    for group_name in groups:
        perms = groups_permissions.get(group_name, [])
        user_perms.update(perms)

    if isinstance(permission, list):
        return all(p in user_perms for p in permission)
    return permission in user_perms
