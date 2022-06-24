create_booking = """
    insert into Bookings 
    (
        UUID, StatusId, PatientPersonId, DoctorPersonId, Date, Time
    )
    output inserted.id
    values 
    (
        :uuid, :statusId, :internalPatientId, :internalDoctorId, :date, :time
    )
"""

create_booking_event = """
    insert into BookingEvents (BookingId, TypeId)
    values (:booking_id, :type_id)
"""

get_internal_personId_by_uuid = """
    select 
        u.PersonId
    from Users u 
    where u.UUID = :uuid
"""

get_by_id = """
    select
        b.Id,
        b.UUID,
        b.StatusId,
        bs.Name StatusName,
        p.UUID PatientPersonId,
        d.UUID DoctorPersonId,
        b.Date,
        b.Time,
        b.No
    from Bookings b
    join Bookings#Status bs on bs.Id = b.StatusId
    join Users p on p.PersonId = b.PatientPersonId
    join Users d on d.PersonId = b.DoctorPersonId
    where b.Id = :id
"""

get_by_uuid = """
    select
        b.Id,
        b.UUID,
        b.StatusId,
        bs.Name StatusName,
        p.UUID PatientPersonId,
        d.UUID DoctorPersonId,
        b.Date,
        b.Time,
        b.No
    from Bookings b
    join Bookings#Status bs on bs.Id = b.StatusId
    join Users p on p.PersonId = b.PatientPersonId
    join Users d on d.PersonId = b.DoctorPersonId
    where b.uuid = :uuid
"""

update_by_id = """
    update Bookings set
        StatusId = :status_id
    where id = :id
"""


get_by_user_uuid = """
    select
        b.Id,
        b.UUID,
        b.StatusId,
        bs.Name StatusName,
        p.UUID PatientPersonId,
        d.UUID DoctorPersonId,
        b.Date,
        b.Time,
        b.No
    from Bookings b
    join Bookings#Status bs on bs.Id = b.StatusId
    join Users p on p.PersonId = b.PatientPersonId
    join Users d on d.PersonId = b.DoctorPersonId
    where p.UUID = :uuid and b.StatusId <> 30
"""