import src.models as models
from sqlalchemy import create_engine, text


server = 'LAPTOP-TI3DHGEF'
db_name = 'mabs'
driver = 'ODBC Driver 17 for SQL Server'

DB = f'mssql://@{server}/{db_name}?driver={driver}'

engine = create_engine(DB)


def get_all_users():
    conn = engine.connect()
    result = conn.execute(text('select id, email, uuid from users'))
    users = []
    for row in result:
        row_as_dict = dict(row)
        user = models.User(
            id=row_as_dict["id"],
            email=row_as_dict["email"],
            uuid=row_as_dict["uuid"]
        )
        users.append(user)

    return users


def create_user(user: models.UserCreate):
    sql = """
        INSERT INTO users (email, password, uuid)
        OUTPUT inserted.id
        VALUES (:email, :password, newid())
        """
    with engine.begin() as conn:
        user_id = conn.execute(
            text(sql),
            user.dict()
        ).scalar()
        sql = text('select id, email, uuid from users where id = :id')
        result = conn.execute(sql, {"id": user_id})
        a = dict(result.fetchone())

    return models.User(
        id=a["id"],
        email=a["email"],
        uuid=a["uuid"]
    )
