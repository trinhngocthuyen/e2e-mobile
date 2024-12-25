class MetaUtils:
    @staticmethod
    def all_subclasses(cls):
        return set(cls.__subclasses__()).union(s for c in cls.__subclasses__() for s in MetaUtils.all_subclasses(c))
