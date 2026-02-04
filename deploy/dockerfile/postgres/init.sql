CREATE USER bee_user WITH PASSWORD 'bee_password';
CREATE DATABASE bee_db OWNER bee_user;
GRANT ALL PRIVILEGES ON DATABASE bee_db TO bee_user;
