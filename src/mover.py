import logging
from graph_client import get_user_by_upn, get_user_groups, add_to_group, remove_from_group, update_user

logger = logging.getLogger(__name__)

def handle_mover(token, row, dept_group_map):
    upn = row["upn"]
    new_dept = row["department"]
    new_title = row["title"]
    old_dept = row.get("old_department", "")

    user = get_user_by_upn(token, upn)
    if not user:
        raise ValueError(f"User not found: {upn}")

    user_id = user["id"]
    current_groups = get_user_groups(token, user_id)
    old_dept_groups = set(dept_group_map.get(old_dept, []))
    new_dept_groups = set(dept_group_map.get(new_dept, []))

    for grp in (old_dept_groups - new_dept_groups):
        remove_from_group(token, user_id, grp)
    for grp in (new_dept_groups - current_groups):
        add_to_group(token, user_id, grp)

    update_user(token, user_id, {"department": new_dept, "jobTitle": new_title})
    logger.info(f"[MOVER] {upn} move complete")
