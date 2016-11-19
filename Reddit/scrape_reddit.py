"""
r = praw.Reddit('omscs_tester')
submission = r.get_submission(submission_id=sub_id[3])
submission.replace_more_comments(limit=None, threshold=0)
all_comments = submission.comments

all_comments[0].body
all_comments[0].score

# dir(submission)

submission.title
submission.selftext
submission.created_utc
#just force tags to be all the same (i.e. OMSCS)

"""
import praw
import pandas as pd

r = praw.Reddit('omscs_tester')
submission = r.get_subreddit('OMSCS').get_hot(limit=250)

# get the title...
sub_id = [x.id for x in submission]

def get_information(post_id):
    submission = r.get_submission(submission_id=post_id)
    return {'title': submission.title, 
            'body': submission.selftext, 
            'id': submission.created_utc, 
            'tag': 'OMSCS'}
            
post_information = [get_information(x) for x in sub_id]
                    
post_df = pd.DataFrame.from_dict(post_information)

# fix up fields...
def collapse_spaces(x1):
    import re 
    x = re.sub(r'[^\x00-\x7F]+','', x1)
    x = re.sub(r'\s+', ' ', x)
    return x.strip()

post_df['title'] = post_df['title'].apply(collapse_spaces)
post_df['body'] = post_df['body'].apply(collapse_spaces)

post_df.to_csv("reddit.csv", index=False)

