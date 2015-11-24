""" Noe kode fra https://github.com/getpelican/pelican-plugins/tree/master/feed_summary"""
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
        
    def _set_categories_to_hide_from_feed(self):
        if self.settings['HIDE_CATEGORIES_FROM_FEED']:
            self._categories_to_hide = self.settings['HIDE_CATEGORIES_FROM_FEED']
        if not self._categories_to_hide and self.settings['HIDE_CATEGORIES_FROM_MENU']:
            self._categories_to_hide = self.settings['HIDE_CATEGORIES_FROM_MENU']
        
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
    
    print inspect.getmembers(pelican_object, predicate=inspect.ismethod)
    

def register():
    signals.initialized.connect(set_hide_categories_from_feed_default)
    signals.initialized.connect(add_writer)
