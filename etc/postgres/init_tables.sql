CREATE TABLE IF NOT EXISTS Users (
  id int,
  name text,
  age int,
  PRIMARY KEY (id)
);

INSERT INTO Users VALUES(1, 'admin', 10);
INSERT INTO Users VALUES(2, 'vasya', 20);