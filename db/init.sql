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
VALUES (1,'sacou', 'provider1',10 ),
       (2,'parfum', 'provider1',8 ),
       (3,'pantaloni', 'provider2',50 ),
       (4,'tricouri', 'provider2',30 );


CREATE TABLE price
(
    item_id   INTEGER(10),
    price     INTEGER(5)
);

INSERT INTO price
(ITEM_ID, PRICE)
VALUES (1, 100 ),
       (2,200 ),
       (3,100 ),
       (4,150 );

CREATE TABLE users
(
    user_id     INTEGER(10),
    username    VARCHAR(20),
    password_hash    VARCHAR(50)
);

CREATE TABLE orders (
    order_id INTEGER(10),
    item_id INTEGER(10),
    user_id INTEGER(10),
    quantity INTEGER(5),
    oder_timestamp INTEGER(10)
);

INSERT INTO users
    (USER_ID, USERNAME, PASSWORD_HASH)
VALUES (1, 'cristina', '0c74ac34d6652b2da30488d4f38496d8'),
       (2, 'admin', '21232f297a57a5a743894a0e4a801fc3');
