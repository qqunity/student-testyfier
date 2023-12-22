create table "group"
(
    group_id   bigserial
        primary key,
    name       varchar(10) not null,
    archived   boolean     not null,
    created_at timestamp with time zone default now()
);

alter table "group"
    owner to postgres;

INSERT INTO public."group" (group_id, name, archived, created_at) VALUES (1, 'М23-504', false, '2023-12-17 13:26:52.140762 +00:00');
