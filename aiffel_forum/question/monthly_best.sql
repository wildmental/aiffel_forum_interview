select a.month, a.id as best_question, max(a.likes) likes
from (select q.id, q.title,
             strftime('%Y-%m', q.created) as month,
             count(qlu.id) as likes
      from question as q
      left join question_like_users as qlu on q.id =qlu.question_id
      group by q.id) as a
group by a.month
order by 1 desc;