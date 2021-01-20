CREATE DATABASE store;
use store;

CREATE TABLE stock
(
    item_id   INTEGER(20),
    item_name VARCHAR(80),
    provider  VARCHAR(40),
    stock     INTEGER(5)
);

INSERT INTO stock
    (ITEM_ID, ITEM_NAME, PROVIDER, STOCK)
VALUES (1,'Geaca usoara Julianna Ultra', 'Trespass',10 ),
       (2,'Hanorac cu fermoar si buzunare Fluence', 'Geographical Norway',8 ),
       (3,'Rochie mini cu imprimeu zebra', 'Missguided',50 ),
       (4,'Geaca cu gluga Valerie', 'Trespass',30 ),
       (5,'Hanorac cu model logo dry', 'Puma',30 ),
       (6,'Blugi skinny', 'Espirit',30 ),
       (7,'Rochie de satin cu umeri intariti Pady', 'Pandy',30 ),
       (8,'Haina din blana sintetica cu aspect pufos Chilly', 'Mango',30 ),
       (9,'Jacheta parka relaxed fit cu finisaj rezistent la apa si gluga Adventure', 'ONeil',30 ),
       (10,'Jacheta biker din piele cu aplicatii cu strasuri', 'Karl Lagerfeld',30 );


CREATE TABLE price
(
    item_id   INTEGER(10),
    price     INTEGER(5)
);

INSERT INTO price
    (ITEM_ID, price)
VALUES (1, 470),
       (2, 380),
       (3, 220),
       (4,  976),
       (5, 1099),
       (6, 870),
       (7, 110),
       (8, 510),
       (9, 630),
       (10, 4300);


CREATE TABLE users
(
    user_id     INTEGER(10),
    username    VARCHAR(20),
    password_hash    VARCHAR(50),
    scope    VARCHAR(10)
);

CREATE TABLE orders (
    order_id INTEGER(10),
    item_id INTEGER(10),
    user_id INTEGER(10),
    quantity INTEGER(5),
    order_timestamp INTEGER(10)
);

INSERT INTO orders
    (ORDER_ID, ITEM_ID, USER_ID, QUANTITY, ORDER_TIMESTAMP)
VALUES (1, 3, 1, 1, 1611058522),
       (2, 4, 1, 2, 1610972122),
       (3, 5, 2, 1, 1610885722),
       (4, 9, 1, 1, 1610799322),
       (5, 1, 2, 2, 1610712922),
       (6, 7, 1, 1, 1610626522),
       (7, 2, 1, 2, 1610540122),
       (8, 2, 1, 2, 1610453722),
       (9, 8, 1, 3, 1610367322),
       (10, 9, 1, 1, 1610280922);

INSERT INTO users
(USER_ID, USERNAME, PASSWORD_HASH, SCOPE)
VALUES (1, 'john',  '21232f297a57a5a743894a0e4a801fc3', 'admin'),
       (2, 'admin', '21232f297a57a5a743894a0e4a801fc3', 'admin');

CREATE TABLE messages
(
    date DATETIME,
    name   VARCHAR(40),
    email VARCHAR(40),
    phone_number  VARCHAR(40),
    message     VARCHAR(100)
);