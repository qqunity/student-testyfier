create table test
(
    test_id     bigserial
        primary key,
    reviewer_id bigint
                             references "user"
                                 on delete set null,
    name        varchar(100) not null,
    type        test_type    not null,
    description text,
    duration    interval     not null,
    archived    boolean      not null
);

alter table test
    owner to postgres;

INSERT INTO public.test (test_id, reviewer_id, name, type, description, duration, archived) VALUES (1, 1, 'Тест эмоционального интеллекта Холла', 'PSYCHOLOGICAL', null, '0 years 0 mons 0 days 1 hours 30 mins 0.0 secs', false);
INSERT INTO public.test (test_id, reviewer_id, name, type, description, duration, archived) VALUES (2, 1, 'Диагностика ведущей перцептивной модальности', 'PSYCHOLOGICAL', null, '0 years 0 mons 0 days 1 hours 30 mins 0.0 secs', false);
INSERT INTO public.test (test_id, reviewer_id, name, type, description, duration, archived) VALUES (3, 1, 'Пятифакторный опросник личности, 5PFQ', 'PSYCHOLOGICAL', null, '0 years 0 mons 0 days 1 hours 30 mins 0.0 secs', false);
INSERT INTO public.test (test_id, reviewer_id, name, type, description, duration, archived) VALUES (4, 1, 'Схемный опросник Янга, YSQ S3R', 'PSYCHOLOGICAL', null, '0 years 0 mons 0 days 1 hours 30 mins 0.0 secs', false);
INSERT INTO public.test (test_id, reviewer_id, name, type, description, duration, archived) VALUES (5, 1, 'Метод портретных выборов', 'PSYCHOLOGICAL', null, '0 years 0 mons 0 days 1 hours 30 mins 0.0 secs', false);
