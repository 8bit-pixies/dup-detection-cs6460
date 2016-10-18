SELECT
  p.Id as postid,
  p.Title as posttitle,
  p.tags as posttags,
  dupes.Id as dupid,
  dupes.Title as duptitle,
  dupes.tags as duptags
FROM Posts p
JOIN PostLinks links ON (p.Id = links.RelatedPostId AND LinkTypeId = 3)
JOIN Posts dupes ON (dupes.Id = links.PostId and dupes.PostTypeId = 1)

WHERE p.CreationDate > '2016-01-01 00:00:00'
