## Core Models & Business Logic

### Barber Availability

Barber availability is defined as a single record per barber per date, listing all 1-hour time slots during which the barber is available.

Model Example:

```json
{
  "id": 1,
  "date": "2025-06-19",
  "slots": ["10:10", "11:00", "12:00"]
}
```

**Rules & Constraints:**

- Each time slot represents a fixed 1-hour window.
- Availability data is managed exclusively by admins.
- Only one availability entry is allowed per barber per date.

### Client Appointments

Clients can book a single available slot with a barber on a specific date, along with one or more services offered by that barber.

Model Example:

```json
{
  "id": 7,
  "client_id": 5,
  "barber_id": 2,
  "date": "2025-06-19",
  "slot": "13:10",
  "services": [3, 4],
  "status": "ONGOING",
  "reminder_email_sent": false
}
```

**Rules & Constraints:**

- A client can only have **one** appointment with `status = "ONGOING"` at a time.
- The selected `slot` must: Exist in the barber’s availability for the specified date and not be already booked.

### Automated Tasks

Used `Celery` deployed with 3 docker services, `Celery worker`, `Celery beat` and `Redis broker` to run these background tasks:

- Email reminders before 1 hour before appointment is due, sent to barber and client.
- Status updates (ONGOING → COMPLETED) when the appointment is due.
- Powered by Celery Worker, Celery Beat, and Redis broker.

### Reviews

Clients can submit a **single** review per barber, but **only** after completing an appointment. Each review is directly associated with both the barber and the related appointment.

Model Example:

```json
{
  "id": 1,
  "appointment_id": 1,
  "client_full_name": "Steve Johnson",
  "rating": 4,
  "comment": "Clean cut, very professional.",
  "created_at": "2025-06-19",
  "edited_at": null
}
```

**Rules & Constraints:**

- One review per client per barber.
- Reviews are allowed **only** after the associated appointment is completed.

### Statistics

Admin statistics dashboard includes:

- Total revenue
- Total appointments
- Review count
- Average barber rating
