create table test_feedback
(
    test_feedback_id bigserial
        primary key,
    test_id          bigint not null
        references test
            on delete cascade,
    user_id          bigint not null
        references "user"
            on delete cascade,
    comment          text   not null,
    score            smallint,
    created_at       timestamp with time zone default now()
);

alter table test_feedback
    owner to postgres;

