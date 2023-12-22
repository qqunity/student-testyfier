create table study_direction_subject
(
    study_direction_subject_id bigserial
        primary key,
    study_direction_id         bigint not null
        references study_direction
            on delete cascade,
    subject_id                 bigint not null
        references subject
            on delete cascade
);

alter table study_direction_subject
    owner to postgres;

INSERT INTO public.study_direction_subject (study_direction_subject_id, study_direction_id, subject_id) VALUES (1, 1, 1);
