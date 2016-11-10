.txtselect distinct p.id, p.title, p.body, p.tags, p.creationdate,
dupes.id as did, dupes.title as dtitle, dupes.body as dbody, dupes.tags, dupes.creationdate as dcreationdate, links.linktypeid as linktype
from posts p
inner join posttags pt on pt.postid = p.id
inner join tags t on pt.tagid = t.id
inner JOIN PostLinks links ON (p.Id = links.RelatedPostId AND (LinkTypeId = 3 or linktypeid=1))
inner JOIN Posts dupes ON (dupes.Id = links.PostId and dupes.PostTypeId = 1
                            and dupes.creationdate >  p.creationdate)
where t.tagname in ('html', 'javascript') and
  p.creationdate > '2016-01-01 00:00:00'
