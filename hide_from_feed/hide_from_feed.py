""" Hide selected categories from the (atom) feed. Categories can be specified in a list format with the
HIDE_CATEGORIES_FROM_FEED config item. If not specified, HIDE_CATEGORIES_FROM_MENU will be used.
Some code from https://github.com/getpelican/pelican-plugins/tree/master/feed_summary
"""
import inspect
import types

from pelican import signals
from pelican import contents
from pelican.writers import Writer


class FeedSummaryWriter(Writer):

    def __init__(self, output_path, settings=None):
        super(FeedSummaryWriter, self).__init__(output_path, settings)
        self._categories_to_hide = []
        self._set_categories_to_hide_from_feed()

    """Read configuration and store in variable self._categories_to_hide"""
    def _set_categories_to_hide_from_feed(self):
        if self.settings['HIDE_CATEGORIES_FROM_FEED']:
            self._categories_to_hide = self.settings['HIDE_CATEGORIES_FROM_FEED']
        if not self._categories_to_hide and self.settings['HIDE_CATEGORIES_FROM_MENU']:
            self._categories_to_hide = self.settings['HIDE_CATEGORIES_FROM_MENU']

    """ Write items to the feed. If category is hidden, do nothing. Otherwise, delegate 
    to superclass"""
    def _add_item_to_the_feed(self, feed, item):
        if str(item.__dict__['category']) in self._categories_to_hide:
            pass
        else:
            super(FeedSummaryWriter, self)._add_item_to_the_feed(feed, item)

def set_hide_categories_from_feed_default(pelican_object):
    # modifying DEFAULT_CONFIG doesn't have any effect at this point in pelican setup
    # everybody who uses DEFAULT_CONFIG is already used/copied it or uses the pelican_object.settings copy.
    pelican_object.settings.setdefault('HIDE_CATEGORIES_FROM_FEED', False)

def add_writer(pelican_object):
    def writer_func(cls):
        return FeedSummaryWriter(cls.output_path, settings=cls.settings)
    setattr(pelican_object, 'get_writer', types.MethodType(writer_func, pelican_object))

def register():
    signals.initialized.connect(set_hide_categories_from_feed_default)
    signals.initialized.connect(add_writer)
