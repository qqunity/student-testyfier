create table "group"
(
    group_id   bigserial,
    name       varchar(10) not null,
    archived   boolean     not null,
    created_at timestamp with time zone default now(),
    primary key (group_id)
);

alter table "group"
    owner to postgres;

create table study_direction
(
    study_direction_id bigserial,
    name               varchar(64) not null,
    degree             smallint    not null,
    archived           boolean     not null,
    speciality_code    varchar(10) not null,
    primary key (study_direction_id)
);

alter table study_direction
    owner to postgres;

create table "user"
(
    user_id            bigserial,
    first_name         varchar(64) not null,
    last_name          varchar(64) not null,
    middle_name        varchar(64),
    birthday           timestamp,
    gender             smallint    not null,
    login              varchar(64) not null,
    password           varchar(64) not null,
    phone_number       varchar(64),
    photo_url          varchar(120),
    role               smallint    not null,
    created_at         timestamp with time zone default now(),
    last_logged_at     timestamp with time zone,
    deleted            boolean     not null,
    group_id           bigint,
    study_direction_id bigint,
    primary key (user_id),
    unique (login),
    foreign key (group_id) references "group"
        on delete set null,
    foreign key (study_direction_id) references study_direction
        on delete set null
);

alter table "user"
    owner to postgres;

create index ix_user_study_direction_id
    on "user" (study_direction_id);

create index ix_user_group_id
    on "user" (group_id);

create table subject
(
    subject_id bigserial,
    name       varchar(100) not null,
    archived   boolean      not null,
    primary key (subject_id)
);

alter table subject
    owner to postgres;

create table teacher_subject
(
    teacher_subject_id bigserial,
    teacher_id         bigint not null,
    subject_id         bigint not null,
    started_at         timestamp with time zone default now(),
    ended_at           timestamp with time zone,
    primary key (teacher_subject_id),
    foreign key (teacher_id) references "user"
        on delete cascade,
    foreign key (subject_id) references subject
        on delete cascade
);

alter table teacher_subject
    owner to postgres;

create table study_direction_subject
(
    study_direction_subject_id bigserial,
    study_direction_id         bigint not null,
    subject_id                 bigint not null,
    primary key (study_direction_subject_id),
    foreign key (study_direction_id) references study_direction
        on delete cascade,
    foreign key (subject_id) references subject
        on delete cascade
);

alter table study_direction_subject
    owner to postgres;

create type test_type as enum ('PSYCHOLOGICAL', 'EXAM', 'TEST');

alter type test_type
    owner to postgres;

create table test
(
    test_id     bigserial,
    reviewer_id bigint,
    name        varchar(100) not null,
    type        test_type    not null,
    description text,
    duration    interval     not null,
    archived    boolean      not null,
    primary key (test_id),
    foreign key (reviewer_id) references "user"
        on delete set null
);

alter table test
    owner to postgres;

create table test_subject
(
    test_subject_id bigserial,
    test_id         bigint not null,
    subject_id      bigint not null,
    primary key (test_subject_id),
    foreign key (test_id) references test
        on delete cascade,
    foreign key (subject_id) references subject
        on delete cascade
);

alter table test_subject
    owner to postgres;

create table test_feedback
(
    test_feedback_id bigserial,
    test_id          bigint not null,
    user_id          bigint not null,
    comment          text   not null,
    score            smallint,
    created_at       timestamp with time zone default now(),
    primary key (test_feedback_id),
    foreign key (test_id) references test
        on delete cascade,
    foreign key (user_id) references "user"
        on delete cascade
);

alter table test_feedback
    owner to postgres;

create table user_test_action
(
    user_test_action_id bigserial,
    test_id             bigint   not null,
    user_id             bigint   not null,
    action              smallint not null,
    created_at          timestamp with time zone default now(),
    primary key (user_test_action_id),
    foreign key (test_id) references test
        on delete cascade,
    foreign key (user_id) references "user"
        on delete cascade
);

alter table user_test_action
    owner to postgres;

create type question_type as enum ('SINGLE_ANSWER', 'MULTIPLE_ANSWERS', 'TEXT_ANSWER');

alter type question_type
    owner to postgres;

create table question
(
    question_id    bigserial,
    test_id        bigint        not null,
    description    text          not null,
    type           question_type not null,
    answer_options jsonb,
    required       boolean       not null,
    deleted        boolean       not null,
    primary key (question_id),
    foreign key (test_id) references test
        on delete cascade
);

alter table question
    owner to postgres;

create table user_question_action
(
    user_question_action_id bigserial,
    question_id             bigint   not null,
    user_id                 bigint   not null,
    action                  smallint not null,
    created_at              timestamp with time zone default now(),
    primary key (user_question_action_id),
    foreign key (question_id) references question
        on delete cascade,
    foreign key (user_id) references "user"
        on delete cascade
);

alter table user_question_action
    owner to postgres;

create table answer
(
    answer_id   bigserial,
    question_id bigint not null,
    user_id     bigint not null,
    answer      jsonb  not null,
    created_at  timestamp with time zone default now(),
    primary key (answer_id),
    foreign key (question_id) references question
        on delete cascade,
    foreign key (user_id) references "user"
        on delete cascade
);

alter table answer
    owner to postgres;
