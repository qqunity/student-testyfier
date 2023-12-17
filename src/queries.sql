select distinct subject.subject_id
from subject
         join test_subject on subject.subject_id = test_subject.subject_id
         join test on test_subject.test_id = test.test_id
         join question on test.test_id = question.test_id
where question.description like '%Эмпатия%';


select test.test_id, count(answer.answer_id) as answers_cnt
from test
         join question on test.test_id = question.test_id
         join answer on question.question_id = answer.question_id
group by test.test_id
order by answers_cnt desc;


select test.test_id
from (select test.test_id, count(answer.answer_id) as answers_cnt
      from test
               join question on test.test_id = question.test_id
               join answer on question.question_id = answer.question_id
      group by test.test_id) q
         join test on q.test_id = test.test_id
where test.archived
   or answers_cnt = 0;


select "user".user_id, answer.answer
from answer
         join "user" on answer.user_id = "user".user_id
         join question on answer.question_id = question.question_id
         join test on question.test_id = test.test_id
         join test_subject on test.test_id = test_subject.test_id
         join subject on test_subject.subject_id = subject.subject_id
where subject.name = 'Проектирование информационных систем'
  and "user".group_id = 1;


select *
from "user"
where "user".first_name like '%Дар%'
   or "user".last_name like '%Ива%'
   or "user".middle_name like '%Ива%';


select "user".*
from (select subject.subject_id
      from teacher_subject
               join "user" on teacher_subject.teacher_id = "user".user_id
               join subject on teacher_subject.subject_id = subject.subject_id and "user".first_name = 'Дарья' and
                               "user".middle_name = 'Валерьевна') q
         join study_direction_subject on q.subject_id = study_direction_id
         join study_direction on study_direction_subject.study_direction_id = study_direction.study_direction_id
         join "user" on study_direction.study_direction_id = "user".study_direction_id;


