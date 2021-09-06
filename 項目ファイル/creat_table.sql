--1.社員情報
drop table if exists e_profile;
create table e_profile(
id serial not null PRIMARY KEY ,
user_id integer not null ,
last_name_k character varying(30) not null ,
first_name_k character varying(30) not null ,
last_name character varying(15) not null ,
first_name character varying(15) not null ,
gender integer not null ,
birth timestamp(6) with time zone not null ,
nationality character varying(30) not null ,
phone character varying(20) not null ,
postal_code character varying(15) not null ,
address1 character varying(128) not null ,
address2 character varying(128) not null ,
residence_card character varying(20) not null ,
health_insurance character varying(20) not null ,
department_pro_id integer not null ,
emergency_contact_1_name character varying(30) not null ,
emergency_contact_1_relationship character varying(10) not null ,
emergency_contact_1_phone character varying(20) not null ,
emergency_contact_2_name character varying(30) not null ,
emergency_contact_2_relationship character varying(10) not null ,
emergency_contact_2_phone character varying(20) not null ,
emergency_contact_3_name character varying(30) not null ,
emergency_contact_3_relationship character varying(10) not null ,
emergency_contact_3_phone character varying(20) not null ,
delete integer not null ,
create_date timestamp(6) with time zone not null ,
create_id integer not null ,
update_date timestamp(6) with time zone not null ,
update_id integer not null
);

--2.部門
drop table if exists e_department;
create table e_department(
dep_id serial not null PRIMARY KEY ,
department character varying(10) not null ,
establish_date timestamp(6) with time zone not null ,
delete integer not null ,
create_date timestamp(6) with time zone not null ,
create_id integer not null ,
update_date timestamp(6) with time zone not null ,
update_id integer not null
);

--3.資産管理
drop table if exists e_asset;
create table e_asset(
asset_id character varying(100) not null PRIMARY KEY ,
num integer not null ,
product_ass_id integer not null ,
model_name character varying(50) not null ,
storing_date timestamp(6) with time zone not null ,
purchase_date timestamp(6) with time zone not null ,
serial_number character varying(50) not null ,
delete integer not null ,
create_date timestamp(6) with time zone not null ,
create_id integer not null ,
update_date timestamp(6) with time zone not null ,
update_id integer not null
);

--4.品名管理
drop table if exists e_product;
create table e_product(
product_id serial not null PRIMARY KEY ,
product_name character varying(50) not null ,
product_abbreviation character varying(50) not null ,
delete integer not null ,
create_date timestamp(6) with time zone not null ,
create_id integer not null ,
update_date timestamp(6) with time zone not null ,
update_id integer not null
);

--5.資産履歴
drop table if exists e_asset_history;
create table e_asset_history(
asset_history_id serial not null PRIMARY KEY ,
asset_ash_id character varying(100) not null ,
status integer not null ,
user_id integer  ,
repair_reason character varying(200)  ,
delete integer not null ,
create_date timestamp(6) with time zone not null ,
create_id integer not null ,
update_date timestamp(6) with time zone not null ,
update_id integer not null
);

--6.マスター
drop table if exists m_list;
create table m_list(
code_type integer not null ,
id integer not null ,
value character varying(200) not null ,
sort integer not null,
primary key (code_type,id) 
);

