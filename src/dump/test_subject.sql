create table test_subject
(
    test_subject_id bigserial
        primary key,
    test_id         bigint not null
        references test
            on delete cascade,
    subject_id      bigint not null
        references subject
            on delete cascade
);

alter table test_subject
    owner to postgres;

INSERT INTO public.test_subject (test_subject_id, test_id, subject_id) VALUES (1, 1, 1);
INSERT INTO public.test_subject (test_subject_id, test_id, subject_id) VALUES (2, 2, 1);
INSERT INTO public.test_subject (test_subject_id, test_id, subject_id) VALUES (3, 3, 1);
INSERT INTO public.test_subject (test_subject_id, test_id, subject_id) VALUES (4, 4, 1);
INSERT INTO public.test_subject (test_subject_id, test_id, subject_id) VALUES (5, 5, 1);
