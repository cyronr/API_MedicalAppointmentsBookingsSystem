get_all = """
    select 
        u.Id UserId, 
        u.UUID UUID,
        u.Email Email, 
        u.StatusId StatusId,
        u.TypeId TypeId,
        p.Id PersonId,
        p.Firstname Firstname,
        p.Surname Surname,
        p.Phone Phone,
        p.IdentificationNumberTypeId IdentificationNumberTypeId,
        p.IdentificationNumber IdentificationNumber,
        p.City City,
        p.Street Street,
        p.ZipCode ZipCode
    from Users u
    left join Persons p on p.Id = u.PersonId
    where u.StatusId = 10
"""

get_by_id = """
    select 
        u.Id UserId, 
        u.UUID UUID,
        u.Email Email, 
        u.StatusId StatusId,
        u.TypeId TypeId,
        p.Id PersonId,
        p.Firstname Firstname,
        p.Surname Surname,
        p.Phone Phone,
        p.IdentificationNumberTypeId IdentificationNumberTypeId,
        p.IdentificationNumber IdentificationNumber,
        p.City City,
        p.Street Street,
        p.ZipCode ZipCode
    from Users u
    left join Persons p on p.Id = u.PersonId
    where u.id = :user_id and u.StatusId = 10
"""

get_by_email = """
    select 
        u.Id UserId, 
        u.UUID UUID,
        u.Email Email, 
        u.StatusId StatusId,
        u.TypeId TypeId,
        p.Id PersonId,
        p.Firstname Firstname,
        p.Surname Surname,
        p.Phone Phone,
        p.IdentificationNumberTypeId IdentificationNumberTypeId,
        p.IdentificationNumber IdentificationNumber,
        p.City City,
        p.Street Street,
        p.ZipCode ZipCode
    from Users u
    left join Persons p on p.Id = u.PersonId
    where u.email = :email and u.StatusId = 10
"""

get_by_uuid = """
    select 
        u.Id UserId, 
        u.UUID UUID,
        u.Email Email, 
        u.StatusId StatusId,
        u.TypeId TypeId,
        p.Id PersonId,
        p.Firstname Firstname,
        p.Surname Surname,
        p.Phone Phone,
        p.IdentificationNumberTypeId IdentificationNumberTypeId,
        p.IdentificationNumber IdentificationNumber,
        p.City City,
        p.Street Street,
        p.ZipCode ZipCode
    from Users u
    left join Persons p on p.Id = u.PersonId
    where u.uuid = :uuid and u.StatusId = 10
"""

create_user = """
    insert into Users 
    (
        UUID, Email, Password, StatusId, TypeId
    )
    output inserted.id
    values 
    (
        :uuid, :email, :password, :statusId, :typeId
    )
"""

create_user_event = """
    insert into UserEvents (UserId, TypeId)
    values (:user_id, :type_id)
"""

update_user_by_id = """
    update Users set
        StatusId = :statusId,
        PersonId = :personId
    where uuid = :id
"""

create_person = """
    insert into Persons
    (
        Firstname,
        Surname,
        Phone,
        IdentificationNumberTypeId,
        IdentificationNumber,
        City,
        Street,
        ZipCode
    )
    output inserted.id
    values
    (
        :firstname,
        :surname,
        :phone,
        :identificationNumberType,
        :identificationNumber,
        :city,
        :street,
        :zipCode
    )
"""

update_person_by_id = """
    update Persons set
        Firstname = :firstname,
        Surname = :surname,
        Phone = :phone,
        IdentificationNumberTypeId = :identificationNumberType,
        IdentificationNumber = :identificationNumber,
        City = :city,
        Street = :street,
        ZipCode = :zip
    where id = :id
"""
