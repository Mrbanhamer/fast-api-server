"""
Database models — describes the tables used in the MySQL database.
Raw SQL is used via sql_connector.py (no ORM).
"""

# Table: users
# id          INT AUTO_INCREMENT PRIMARY KEY
# first_name  VARCHAR(255)
# last_name   VARCHAR(255)
# email       VARCHAR(255) UNIQUE
# password    VARCHAR(255)   -- SHA-256 hash
# salt        VARCHAR(255)   -- hex-encoded random salt

# Table: tickets  (session management)
# ticket_id   VARCHAR(255) PRIMARY KEY
# user_id     INT  REFERENCES users(id) ON DELETE CASCADE
# created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP

# Table: tasks  (the CRUD resource)
# id          INT AUTO_INCREMENT PRIMARY KEY
# user_id     INT  REFERENCES users(id) ON DELETE CASCADE
# title       VARCHAR(255) NOT NULL
# description TEXT
# completed   BOOLEAN DEFAULT FALSE
