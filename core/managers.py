from .query import Connect


class QuerySet:
    def __init__(self, columns, rows, model):
        self.model = model
        objects = []
        for obj in rows:
            objects.append(self.model(**dict(zip(columns, obj))))
        self.objects = objects

    def __repr__(self):
        return f"<QuerySet {self.objects}>"
    
    def __iter__(self):
        for obj in self.objects:
            yield obj
    
    def __getitem__(self, ind):
        return self.objects[ind]
    
    def count(self) -> int:
        return len(self.objects)

    def exists(self) -> bool:
        return bool(self.objects)   

    def delete(self) -> None:
        if self.exists():
            table = self.model.__name__
            ids = [f" id = {i.id} " for i in self.objects]
            self.model.objects.execute(f"delete from {table} where {' or '.join(ids)};")

class Manager:
    def execute(self, command):
        with Connect() as connection:
            rows = connection.run(command)
        try:
            return QuerySet(rows.keys(), rows, self.model)
        except:
            pass

    def all(self) -> QuerySet:
        table = self.model.__name__
        return self.execute(f"select * from {table};")

    def filter(self, **kwargs) -> QuerySet:
        table = self.model.__name__
        params = []
        for k, v in kwargs.items():
            if k.endswith("__icontains") and type(v) == str:
                params.append(f"{k.split('__')[0]} ilike '%{v.lower()}%'")
            elif k.endswith("__contains") and type(v) == str:
                params.append(f"{k.split('__')[0]} like '%{v}%'")
            elif k.endswith("__gt") and type(v) == int:
                params.append(f"{k.split('__')[0]} > {v}")
            elif k.endswith("__gte") and type(v) == int:
                params.append(f"{k.split('__')[0]} >= {v}")
            elif k.endswith("__lt") and type(v) == int:
                params.append(f"{k.split('__')[0]} < {v}")
            elif k.endswith("__lte") and type(v) == int:
                params.append(f"{k.split('__')[0]} <= {v}")
            else:
                params.append(f"{k} = {repr(v)}")
        return self.execute(f"select * from {table} where {' and '.join(params)};")

    def get(self, **kwargs) -> QuerySet:
        return self.filter(**kwargs)[0]
    
    def create(self, **kwargs) -> None:
        table = self.model.__name__
        columns = str(tuple(kwargs.keys())).replace("'", '')
        return self.execute(f"insert into {table} {columns} values {tuple(kwargs.values())};")
