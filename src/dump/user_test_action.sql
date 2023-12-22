create table user_test_action
(
    user_test_action_id bigserial
        primary key,
    test_id             bigint   not null
        references test
            on delete cascade,
    user_id             bigint   not null
        references "user"
            on delete cascade,
    action              smallint not null,
    created_at          timestamp with time zone default now()
);

alter table user_test_action
    owner to postgres;

INSERT INTO public.user_test_action (user_test_action_id, test_id, user_id, action, created_at) VALUES (1, 1, 1, 0, '2023-12-17 13:26:52.243789 +00:00');
INSERT INTO public.user_test_action (user_test_action_id, test_id, user_id, action, created_at) VALUES (2, 2, 1, 0, '2023-12-17 13:27:03.905658 +00:00');
INSERT INTO public.user_test_action (user_test_action_id, test_id, user_id, action, created_at) VALUES (3, 3, 1, 0, '2023-12-17 13:27:12.522927 +00:00');
INSERT INTO public.user_test_action (user_test_action_id, test_id, user_id, action, created_at) VALUES (4, 4, 1, 0, '2023-12-17 13:27:24.558054 +00:00');
INSERT INTO public.user_test_action (user_test_action_id, test_id, user_id, action, created_at) VALUES (5, 5, 1, 0, '2023-12-17 13:27:33.784113 +00:00');
