get_all = """
    select 
        u.Id, 
        u.Email, 
        u.UUID 
    from Users u
"""

get_by_id = """
    select 
        u.Id, 
        u.Email, 
        u.UUID 
    from Users u
    where u.id = :user_id
"""

create_user = """
    insert into Users 
    (
        Email, Password, StatusId
    )
    output inserted.id
    values 
    (
        :email, :password, :status_id
    )
"""

create_event = """
    insert into UserEvents (UserId, TypeId)
    values (:user_id, :type_id)
"""