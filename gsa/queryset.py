class FakeQuerySet(object):
    """Fake query set used for list_detail view.
    
    Implements just methods required for list_detail.
    """
    def __init__(self, items):
        self.model = None
        self.items = items

    def _clone(self):
        return self

    def __len__(self):
        return len(self.items)

    def __getitem__(self, k):
        return self.items[k]

    def __iter__(self):
        return self.items.__iter__()

    def __nonzero__(self):
        return bool(self.items)

    def __repr__(self):
        return repr(list(self))

    def count(self):
        return len(self.items)

    def exists(self):
        return bool(self.items)

    def first(self):
        if self.items:
            return self.items[0]

    def last(self):
        if self.items:
            return self.items[-1]

    def get(self, **kwargs):
        items = self.filter(**kwargs)
        item_count = items.count()

        if result_count == 0:
            raise self.model.DoesNotExist("%s matching query does not exist." % self.model._meta.object_name)
        elif result_count == 1:
            return items[0]
        else:
            raise self.model.MultipleObjectsReturned(
                "get() returned more than one %s -- it returned %s!" % (self.model._meta.object_name, result_count)
            )

    def all(self):
        return self

    def _get_filters(self, **kwargs):
        # a list of test functions; objects must pass all tests to be included
        # in the filtered list
        filters = []

        for key, val in kwargs.items():
            key_clauses = key.split('__')
            if len(key_clauses) != 1:
                raise NotImplementedError("Complex filters with double-underscore clauses are not implemented yet")

            filters.append(test_exact(self.model, key_clauses[0], val))

        return filters

    def filter(self, **kwargs):
        filters = self._get_filters(**kwargs)

        filtered_results = [
            obj for obj in self.items
            if all([test(obj) for test in filters])
        ]

        return FakeQuerySet(self.model, filtered_results)

