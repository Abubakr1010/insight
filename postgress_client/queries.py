SAVE_OTP = """ 
    INSERT INTO user_otps (email, otp_code, expires_at, used, created_at)
    VALUES ($1,$2,$3,FALSE,$4)
"""


FETCH_STORE = """
    SELECT * FROM stores 
    WHERE shop_domain=$
"""


UPDATE_STORE = """
    UPDATE store
    SET access_store=$1, updated_at=CURRENT_TIMESTAMP,
    WHERE shop_domain=$
"""


INSERT_STORE = """
    INSERT INTO stores(user_id, shop_domain, access_taken)
    VALUES ($1,$2,$3)
"""


GET_OTP_BY_EMAIL = """
    SELECT * FROM user_otps
    WHERE email =$1
    ORDER BY created_at DESC
    LIMIT 1
"""


MARK_OTP_USED = """
    UPDATE user_otps
    SET used = TRUE
    WHERE id = $1
"""


GET_USER_BY_EMAIL = """
    SELECT * FROM users 
    WHERE email =$1
"""


CREATE_USER = """
    INSERT INTO users (email, created_at)
    VALUES ($1, $2)
    RETURNING *
"""