# CREATE DATABASE knights;
# use knights;
#
# CREATE TABLE favorite_colors
# (
#     name  VARCHAR(20),
#     color VARCHAR(10)
# );
#
# INSERT INTO favorite_colors
#     (name, color)
# VALUES ('Lancelot', 'blue'),
#        ('Galahad', 'yellow');
#

CREATE DATABASE store;
use store;

CREATE TABLE stock
(
    item_id   INTEGER(20),
    item_name VARCHAR(20),
    provider  VARCHAR(20),
    stock     INTEGER(5)
);

INSERT INTO stock
    (ITEM_ID, ITEM_NAME, PROVIDER, STOCK)
VALUES (1,'ciorapi', 'provider1',10 ),
       (2,'chiloti', 'provider1',8 ),
       (3,'pantaloni', 'provider2',50 ),
       (4,'tricouri', 'provider2',30 );


CREATE TABLE price
(
    item_id   INTEGER(20),
    price     INTEGER(5)
);

INSERT INTO price
(ITEM_ID, PRICE)
VALUES (1, 10 ),
       (2,20 ),
       (3,100 ),
       (4,150 );

CREATE TABLE users
(
    user_id     INTEGER(5),
    username    VARCHAR(20),
    password_hash    VARCHAR(50)
);

INSERT INTO users
(user_id, username, password_hash)
VALUES (1, 'cristina', '0c74ac34d6652b2da30488d4f38496d8')
