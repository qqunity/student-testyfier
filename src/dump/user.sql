create table "user"
(
    user_id            bigserial
        primary key,
    first_name         varchar(64) not null,
    last_name          varchar(64) not null,
    middle_name        varchar(64),
    birthday           date,
    gender             smallint    not null,
    login              varchar(64) not null
        unique,
    password           varchar(64) not null,
    phone_number       varchar(64),
    photo_url          varchar(120),
    role               smallint    not null,
    created_at         timestamp with time zone default now(),
    last_logged_at     timestamp with time zone,
    deleted            boolean     not null,
    group_id           bigint
                                   references "group"
                                       on delete set null,
    study_direction_id bigint
                                   references study_direction
                                       on delete set null
);

alter table "user"
    owner to postgres;

create index ix_user_study_direction_id
    on "user" (study_direction_id);

create index ix_user_group_id
    on "user" (group_id);

INSERT INTO public."user" (user_id, first_name, last_name, middle_name, birthday, gender, login, password, phone_number, photo_url, role, created_at, last_logged_at, deleted, group_id, study_direction_id) VALUES (1, 'Дарья', 'Тихомирова', 'Валерьевна', null, 1, 'dvtihomirova', '12345678', null, null, 2, '2023-12-17 13:26:52.175072 +00:00', null, false, null, null);
INSERT INTO public."user" (user_id, first_name, last_name, middle_name, birthday, gender, login, password, phone_number, photo_url, role, created_at, last_logged_at, deleted, group_id, study_direction_id) VALUES (11, 'Анжела', 'Соболева', 'Кузьминична', '1994-11-04', 1, 'julija1998een', '^43aD_g1#E', '+7 081 581 00 62', null, 1, '2023-12-17 13:26:59.359795 +00:00', null, false, 1, 1);
INSERT INTO public."user" (user_id, first_name, last_name, middle_name, birthday, gender, login, password, phone_number, photo_url, role, created_at, last_logged_at, deleted, group_id, study_direction_id) VALUES (12, 'Евдокия', 'Кондратьева', 'Павловна', '1953-12-03', 1, 'jakov1982rgk', 'XgWXJ#w0+6', '8 682 937 67 45', null, 1, '2023-12-17 13:26:59.490794 +00:00', null, false, 1, 1);
INSERT INTO public."user" (user_id, first_name, last_name, middle_name, birthday, gender, login, password, phone_number, photo_url, role, created_at, last_logged_at, deleted, group_id, study_direction_id) VALUES (14, 'Варвара', 'Александрова', 'Евгеньевна', '2022-05-22', 1, 'vladimirovapraskovjabnc', 'wUg6Hqxh&0', '8 (710) 851-53-04', null, 1, '2023-12-17 13:26:59.986165 +00:00', null, false, 1, 1);
INSERT INTO public."user" (user_id, first_name, last_name, middle_name, birthday, gender, login, password, phone_number, photo_url, role, created_at, last_logged_at, deleted, group_id, study_direction_id) VALUES (15, 'Анжела', 'Петрова', 'Леонидовна', '1908-06-13', 1, 'ygrigorevajqz', '5%e#p2Aedf', '+7 (415) 329-6602', null, 1, '2023-12-17 13:27:00.465517 +00:00', null, false, 1, 1);
INSERT INTO public."user" (user_id, first_name, last_name, middle_name, birthday, gender, login, password, phone_number, photo_url, role, created_at, last_logged_at, deleted, group_id, study_direction_id) VALUES (16, 'Евдоким', 'Большаков', 'Авдеевич', '2022-10-25', 0, 'ribakovparfenuuw', '8@9GcaZY^Q', '+7 (918) 012-18-71', null, 1, '2023-12-17 13:27:00.966229 +00:00', null, false, 1, 1);
INSERT INTO public."user" (user_id, first_name, last_name, middle_name, birthday, gender, login, password, phone_number, photo_url, role, created_at, last_logged_at, deleted, group_id, study_direction_id) VALUES (17, 'Ираида', 'Григорьева', 'Ждановна', '1986-10-30', 1, 'mihail00nma', '$k0*60Wnk%', '+7 (056) 862-32-85', null, 1, '2023-12-17 13:27:01.450505 +00:00', null, false, 1, 1);
INSERT INTO public."user" (user_id, first_name, last_name, middle_name, birthday, gender, login, password, phone_number, photo_url, role, created_at, last_logged_at, deleted, group_id, study_direction_id) VALUES (18, 'Лука', 'Фадеев', 'Георгиевич', '2012-12-11', 0, 'savelipestovyjm', '84^vA0ZrT@', '8 (701) 097-7037', null, 1, '2023-12-17 13:27:01.937540 +00:00', null, false, 1, 1);
INSERT INTO public."user" (user_id, first_name, last_name, middle_name, birthday, gender, login, password, phone_number, photo_url, role, created_at, last_logged_at, deleted, group_id, study_direction_id) VALUES (19, 'Елизар', 'Кудряшов', 'Глебович', '1913-08-03', 0, 'fedosi_2000tqb', 'n7KM6VvC&p', '+7 (189) 607-11-42', null, 1, '2023-12-17 13:27:02.412783 +00:00', null, false, 1, 1);
INSERT INTO public."user" (user_id, first_name, last_name, middle_name, birthday, gender, login, password, phone_number, photo_url, role, created_at, last_logged_at, deleted, group_id, study_direction_id) VALUES (20, 'Таисия', 'Веселова', 'Григорьевна', '1916-11-14', 1, 'vladlen_16ljp', '9z0*MgW*$6', '8 (045) 863-2172', null, 1, '2023-12-17 13:27:02.899693 +00:00', null, false, 1, 1);
INSERT INTO public."user" (user_id, first_name, last_name, middle_name, birthday, gender, login, password, phone_number, photo_url, role, created_at, last_logged_at, deleted, group_id, study_direction_id) VALUES (21, 'Митофан', 'Петров', 'Бориславович', '2015-08-10', 0, 'ekaterina94dgk', 'R1CZ%fRc(3', '+7 (162) 676-6096', null, 1, '2023-12-17 13:27:03.393960 +00:00', null, false, 1, 1);
INSERT INTO public."user" (user_id, first_name, last_name, middle_name, birthday, gender, login, password, phone_number, photo_url, role, created_at, last_logged_at, deleted, group_id, study_direction_id) VALUES (22, 'Дарья', 'Попова', 'Геннадьевна', '1981-05-23', 1, 'alla12ojy', 'zI_26Wy@e!', '8 769 111 0702', null, 1, '2023-12-17 13:27:12.063551 +00:00', null, false, 1, 1);
INSERT INTO public."user" (user_id, first_name, last_name, middle_name, birthday, gender, login, password, phone_number, photo_url, role, created_at, last_logged_at, deleted, group_id, study_direction_id) VALUES (13, 'Лазарь', 'Фокин', 'Глебович', '1973-10-11', 0, 'taisija_1997jnz', '9rd9HHCj7!', '+7 (749) 293-34-09', null, 1, '2023-12-17 13:27:27.255107 +00:00', null, false, 1, 1);
