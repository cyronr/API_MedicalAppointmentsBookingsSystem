get_doctor_specialities = """
    select
        s.Id Id,
        s.Name Name,
        ps.Main Main
    from Persons_Specialities ps
    join Specialties s on s.Id = ps.SpecialityId
    where ps.PersonId = :id
"""

get_by_uuid = """
    select
        p.firstname Firstname,
        p.surname Surname,
        p.city City,
        p.street Street,
        p.zipCode ZipCode,
        p.title Title,
        u.UUID UUID,
        p.Id Id
    from Persons p
    join Users u on u.PersonId = p.Id
    where u.UUID = :uuid
"""

get_all = """
    select
        p.firstname Firstname,
        p.surname Surname,
        p.city City,
        p.street Street,
        p.zipCode ZipCode,
        p.title Title,
        u.UUID UUID,
        p.Id Id
    from Persons p
    join Users u on u.PersonId = p.Id
    where p.TypeId = 20
"""

get_doctor_schedule = """
    select 
        s.Time,
        s.Date,
        s.DateTime
    from Users u
    cross apply doctor_GetScheduleDetails(u.PersonId) s
    where u.UUID = :uuid
"""