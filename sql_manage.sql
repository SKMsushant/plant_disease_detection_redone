create database bioshield;

select * from information_schema.columns where table_schema='public' order by table_name,ordinal_position;

drop table "users" cascade;

select * from users;