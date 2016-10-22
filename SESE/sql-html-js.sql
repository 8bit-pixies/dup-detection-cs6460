select distinct p.id, p.title, p.body, p.tags, p.creationdate,
dupes.id as did, dupes.title as dtitle, dupes.body as dbody, dupes.creationdate as dcreationdate
from posts p
inner join posttags pt on pt.postid = p.id
inner join tags t on pt.tagid = t.id
left JOIN PostLinks links ON (p.Id = links.RelatedPostId AND LinkTypeId = 3)
left JOIN Posts dupes ON (dupes.Id = links.PostId and dupes.PostTypeId = 1)
where t.tagname in ('html', 'javascript') and
  p.creationdate > '2016-01-01 00:00:00'


/*query next*/

select distinct p.id, p.title, p.body, p.tags, p.creationdate,
dupes.id as did, dupes.title as dtitle, dupes.body as dbody, dupes.creationdate as dcreationdate
from posts p
inner join posttags pt on pt.postid = p.id
inner join tags t on pt.tagid = t.id
left JOIN PostLinks links ON (p.Id = links.RelatedPostId AND LinkTypeId = 3)
left JOIN Posts dupes ON (dupes.Id = links.PostId and dupes.PostTypeId = 1)
where t.tagname in ('html', 'javascript') and
  p.creationdate <  '2016-01-01 00:00:00' and
  p.creationdate >= '2015-10-08 22:35:36'
