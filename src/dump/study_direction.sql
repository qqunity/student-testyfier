create table study_direction
(
    study_direction_id bigserial
        primary key,
    name               varchar(64) not null,
    degree             smallint    not null,
    archived           boolean     not null,
    speciality_code    varchar(10) not null
);

alter table study_direction
    owner to postgres;

INSERT INTO public.study_direction (study_direction_id, name, degree, archived, speciality_code) VALUES (1, 'Программная инженерия', 1, false, '09.04.04');
