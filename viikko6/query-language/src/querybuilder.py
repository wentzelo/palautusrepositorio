from matchers import All, And, PlaysIn, HasAtLeast, HasFewerThan

class QueryBuilder:
    def __init__(self):
        self._matchers = []

    def plays_in(self, team):
        self._matchers.append(PlaysIn(team))
        return self

    def has_at_least(self, value, attr):
        self._matchers.append(HasAtLeast(value, attr))
        return self

    def has_fewer_than(self, value, attr):
        self._matchers.append(HasFewerThan(value, attr))
        return self

    def build(self):
        if len(self._matchers) == 0:
            return All()
        
        if len(self._matchers) == 1:
            return self._matchers[0]
        
        return And(*self._matchers)