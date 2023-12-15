--  Найти CASE-средства конкретной категории (Quad Hotel Inc.) с набором заданных тегов (заложить.zqu, палка.eos) и отсортировать их по оценкам:
select R7.case_tool_id, R7.name, R7.description, R6.comprehensive_rating
from "CASE_tool" R7
         join "Category" R9 on R9.category_id = R7.category_id and R9.name = 'Quad Hotel Inc.'
         join "CASE_tools_to_tags" R10 on R7.case_tool_id = R10.case_tool_id
         join "Tag" R11 on R11.tag_id = R10.tag_id and R11.name in ('заложить.zqu', 'палка.eos')
         join "Rating" R6 on R6.case_tool_id = R7.case_tool_id
order by R6.comprehensive_rating desc;
-- Найти все CASE-средства с заданным названием дополнительной информации (бок), которые были опубликованы начиная с заданной даты (2022-05-02):
select *
from "CASE_tool" R7
         join "Additional_info" R14
              on R7.case_tool_id = R14.case_tool_id and R14.name = 'бок' and R7.created_at > '2022-05-02';
-- Определить топ 10 самых популярный CASE-средств:
select *
from "CASE_tool" R7
         join "Rating" R6 on R7.case_tool_id = R6.case_tool_id
order by R6.comprehensive_rating desc
limit 10;
-- Составить график развития CASE-средств за некоторый промежуток (за последние 3 года). Т.е. необходимо выбрать топ 3 CASE-средства в каждый момент времени с заданным интервалом (1 год):
(select *
 from "CASE_tool" R7
          join "Rating" R6
               on R7.case_tool_id = R6.case_tool_id and R7.created_at > '2020-01-01' and
                  R7.created_at < '2021-01-01'
 order by R6.comprehensive_rating desc
 limit 3)
union
(select *
 from "CASE_tool" R7
          join "Rating" R6
               on R7.case_tool_id = R6.case_tool_id and R7.created_at > '2021-01-01' and
                  R7.created_at < '2022-01-01'
 order by R6.comprehensive_rating desc
 limit 3)
union
(select *
 from "CASE_tool" R7
          join "Rating" R6
               on R7.case_tool_id = R6.case_tool_id and R7.created_at > '2022-01-01' and
                  R7.created_at < '2023-01-01'
 order by R6.comprehensive_rating desc
 limit 3);
-- Найти самого активного пользователя за некоторый промежуток времени (с 2022-03-01  по 2022-06-01) по количеству комментариев и оценок:
with R_sub_1 as (select user_id, count(*) as rating_activity
                 from "User" R1
                          join "Rating" R6 on R1.user_id = R6.author_id and R6.created_at > '2022-03-01' and
                                              R6.created_at < '2022-06-01'
                 group by user_id)
select R_sub_1.rating_activity,
       R_sub_2.comment_activity,
       R_sub_1.user_id,
       R_sub_1.rating_activity + R_sub_2.comment_activity as total_activity
from (select user_id, count(*) as comment_activity
      from "User" R1
               join "Comment" R5
                    on R1.user_id = R5.author_id and R5.created_at > '2022-03-01' and R5.created_at < '2022-06-01'
      group by user_id) R_sub_2
         join R_sub_1 on R_sub_1.user_id = R_sub_2.user_id
order by total_activity desc
limit 1;
-- Выбрать все активные (не архивные) подкатегории конкретной категории (идентификатор 1):
select R9_1.category_id, R9_1.name
from "Category" R9
         join "Category" R9_1 on R9.category_id = 1 and R9.category_id = R9_1.parent_id and not R9_1.archived;
-- Найти аккаунты пользователей, которые были активны более года назад:
with R_sub as (select user_id
               from "User" R1
                        join "CASE_tool" R7 on R1.user_id = R7.author_id and R7.created_at > '2021-04-01'
               union
               select user_id
               from "User" R1
                        join "Comment" R5 on R1.user_id = R5.author_id and R5.created_at > '2021-04-01'
               union
               select user_id
               from "User" R1
                        join "Rating" R6 on R1.user_id = R6.author_id and R6.created_at > '2021-04-01')
select user_id
from "User" R1
where user_id not in (select * from R_sub);
-- Найти CASE-средства, по которым нет комментариев за последние 5 лет:
with R_sub as (select R7.case_tool_id
               from "CASE_tool" R7
                        join "Comment" R5 on R7.case_tool_id = R5.case_tool_id and R5.created_at > '2017-04-01')
select case_tool_id
from "CASE_tool" R7
where case_tool_id not in (select * from R_sub);