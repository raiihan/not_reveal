
OWNER_ID = 1615680044

ADMINS = [
    OWNER_ID,
    5621290261, 
    5765156518
]

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS
