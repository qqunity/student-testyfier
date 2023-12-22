create table teacher_subject
(
    teacher_subject_id bigserial
        primary key,
    teacher_id         bigint not null
        references "user"
            on delete cascade,
    subject_id         bigint not null
        references subject
            on delete cascade,
    started_at         timestamp with time zone default now(),
    ended_at           timestamp with time zone
);

alter table teacher_subject
    owner to postgres;

INSERT INTO public.teacher_subject (teacher_subject_id, teacher_id, subject_id, started_at, ended_at) VALUES (1, 1, 1, '2023-12-17 13:26:52.183775 +00:00', null);
