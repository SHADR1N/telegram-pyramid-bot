import peewee

db = peewee.SqliteDatabase('database.db', pragmas=(
    ('cache_size', -16000),  
    ('journal_mode', 'wal'), ))


class BaseModel(peewee.Model):
    class Meta:
        database = db

class Users(BaseModel):
    UID = peewee.IntegerField( unique = True, primary_key=True )
    referal = peewee.IntegerField(default = 0)
    balance = peewee.IntegerField(default = 0)
    refovod = peewee.IntegerField(default = '')
    play = peewee.TextField(default = 'await')
    start_money = peewee.IntegerField(default = '')
    role = peewee.TextField(default = 'user')
    phone = peewee.TextField( default = '' )
    
    @classmethod
    def get_row(cls, UID):
        return cls.get(UID == UID)

    @classmethod
    def row_exists(cls, UID):
        query = cls().select().where(cls.UID == UID)
        return query.exists()

    @classmethod
    def creat_row(cls, UID):
        user, created = cls.get_or_create(UID=UID)



class ReferalStairs(BaseModel):
    UID = peewee.IntegerField()
    RID = peewee.IntegerField()
    

    @classmethod
    def get_row(cls, UID):
        return cls.get(UID == UID)

    @classmethod
    def row_exists(cls, UID):
        query = cls().select().where(cls.UID == UID)
        return query.exists()

    @classmethod
    def creat_row(cls, UID, RID):
        user, created = cls.get_or_create(UID=UID, RID = RID)



class comission(BaseModel):
    comout = peewee.TextField()


db.create_tables([ReferalStairs])
db.create_tables([Users])
db.create_tables([comission])