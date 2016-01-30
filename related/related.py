""" Relate content via tags """

import time

from pelican import signals
from pelican import contents


def related_via_tags(cls, articles, categories=[], exclude_categories=[],limit=-1):
    def filter_this(related, categories, excludecategories):
        if related:
            related = filter(lambda article: article.source_path != cls.source_path, related) # Remove self
            if categories:
                related = filter(lambda article: str(article.category) in categories, related)
            if exclude_categories:
                related = filter(lambda article: str(article.category) not in exclude_categories, related)
        return related
    buf = []
    debug = False
    if not hasattr(cls, 'tags'):
        return buf
    related = []
    for art in articles:
        if hasattr(art, 'tags'):
            for t in art.tags:
                if t in cls.tags:
                    related.append(art)
                    break # Only add article one time even if it has more tags in common
    # Filter on categories and excludecategories
    related = filter_this(related, categories, exclude_categories)
    if limit:
        related = related[:limit]
    return related

# age in days
def latest_articles(cls, articles, categories=[], exclude_categories=[], limit=-1, age=3000):
    def exclude_old(articles, age):
        articles = filter(lambda article: article.source_path != cls.source_path, articles) # Remove self
        def filter_by_age(articles, timestampdiff):
            buf = []
            for art in articles:
                artstamp = time.mktime(art.date.timetuple())
                if artstamp > time.time() - timestampdiff:
                    buf.append(art)
            return buf
        timestampdiff = age*24*60*60
        if articles:
            articles = filter_by_age(articles, timestampdiff)
            articles = filter_this(articles, categories, exclude_categories)
        return articles
    
    def filter_this(related, categories, exclude_categories):
        if related:
            related = filter(lambda article: article.source_path != cls.source_path, related) # Remove self
            if categories:
                related = filter(lambda article: str(article.category) in categories, related)
            if exclude_categories:
                related = filter(lambda article: str(article.category) not in exclude_categories, related)
        return related
    def getDate(art):
        return art.date
    articles = exclude_old(articles, age)
    articles = sorted(articles, key=getDate, reverse=True)
    #selection = filter_this(articles, categories, exclude_categories)
    selection = articles
    if limit:
        selection = selection[:limit]
    return selection

def add_related_via_tags_method(sender):
    contents.Article.related_via_tags = related_via_tags
    contents.Draft.related_via_tags = related_via_tags
    contents.Article.latest_articles = latest_articles
    contents.Draft.latest_articles = latest_articles

def register():
    signals.initialized.connect(add_related_via_tags_method)
