""" Relate content via tags """

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

def add_related_via_tags_method(sender):
    contents.Article.related_via_tags = related_via_tags
    contents.Draft.related_via_tags = related_via_tags

def register():
    signals.initialized.connect(add_related_via_tags_method)
