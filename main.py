__author__ = 'arubtsov'

import praw
import HTMLParser
from urlparse import urlsplit, urlunsplit


class Story(object):
    def __init__(self, title, text, score):
        self.title = title
        self.text = text
        self.score = score

    def __unicode__(self):
        return self.title + "\n\n" + self.text

digest = []
h = HTMLParser.HTMLParser()
result = '<html><head title="Page"></head><body>'
templ = '<h1>{0}</h1>{1}<br>'

r = praw.Reddit(user_agent="bestof2pdf")
best = r.get_subreddit('bestof')
subs = best.get_top_from_month()
for i in subs:
    parsedUrl = urlsplit(i.url)
    url = urlunsplit(parsedUrl[0:3] + ('', ''))
    post = r.get_submission(url)
    comment = post.comments[0].body_html
    # print('{0}\t{1}\n{2}\n\n'.format(i.score, i.title, h.unescape(comment)))
    digest.append(Story(i.title, comment, i.score))

for d in digest:
    result += templ.format(d.title, h.unescape(d.text))

result += "</body></html>"
with open("file.html", "w") as outFile:
    outFile.write(result)


