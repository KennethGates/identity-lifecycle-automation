import logging
from graph_client import get_user_by_upn, update_user, revoke_sign_in_sessions, remove_all_groups

logger = logging.getLogger(__name__)

def handle_leaver(token, row):
    upn = row["upn"]
    user = get_user_by_upn(token, upn)
    if not user:
        logger.warning(f"[LEAVER] User not found: {upn} — skipping")
        return

    user_id = user["id"]
    update_user(token, user_id, {"accountEnabled": False})
    revoke_sign_in_sessions(token, user_id)
    groups_removed = remove_all_groups(token, user_id)
    logger.info(f"[LEAVER] {upn} offboarded — {groups_removed} groups removed")
