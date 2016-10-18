select distinct p.title, p.body, p.tags, p.creationdate,
dupes.title, dupes.body
from posts p
inner join posttags pt on pt.postid = p.id
inner join tags t on pt.tagid = t.id
left JOIN PostLinks links ON (p.Id = links.RelatedPostId AND LinkTypeId = 3)
left JOIN Posts dupes ON (dupes.Id = links.PostId and dupes.PostTypeId = 1)
where t.tagname in ('sql') and
  p.creationdate >= '2016-06-01 00:00:00' and
  p.creationdate <= '2016-09-30 00:00:00'
