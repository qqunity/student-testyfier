create table subject
(
    subject_id bigserial
        primary key,
    name       varchar(100) not null,
    archived   boolean      not null
);

alter table subject
    owner to postgres;

INSERT INTO public.subject (subject_id, name, archived) VALUES (1, 'Проектирование информационных систем', false);
