from django.urls import reverse
from django.core.mail import send_mail


def send_client_verify_email(email, uid, token, domain):
    """
    Sends email confirmation link to client after registration.
    """
    link = f'{domain}/verify/{uid}/{token}'

    subject = '[BarberManager] Verify your email to register as a client'
    message = (
        f'Thank you for registering.\n\n'
        f'Please click the link below to verify your account:\n'
        f'{link}\n\n'
        'If you did not register, please ignore this email.'
    )
    send_mail(subject, message, 'barber.manager.verify@gmail.com', [email])


def send_barber_invite_email(email, uid, token, domain):
    """
    Sends barber invitation email with registration link.
    """
    link = f'{domain}/register/{uid}/{token}'

    subject = '[BarberManager] You have been invited to register as a barber'
    message = (
        f'You have been invited to join as a barber.\n\n'
        f'Please click the link below to complete your registration:\n'
        f'{link}\n\n'
        'If you did not expect this invitation, please ignore this email.'
    )
    send_mail(subject, message, 'barber.manager.verify@gmail.com', [email])


def send_password_reset_email(email, uid, token, domain):
    """
    Sends password reset email with reset link.
    """
    link = f'{domain}/reset-password/{uid}/{token}'

    subject = '[BarberManager] You have requested to reset your password'
    message = (
        f'We received a request to reset your password.\n\n'
        f'Please click the link below to set a new password:\n'
        f'{link}\n\n'
        'If you did not request a password reset, please ignore this email.'
    )
    send_mail(subject, message, 'barber.manager.verify@gmail.com', [email])


def send_client_reminder_email(client, barber, appointment_datetime):
    """
    Sends a reminder email to the client 1 hour before their appointment.
    """
    subject = '[BarberManager] Appointment Reminder'
    message = (
        f'Hi {client.name} {client.surname} (username: {client.username}),\n\n'
        f'This is a reminder for your upcoming appointment with the barber {barber.name} {barber.surname} '
        f'on {appointment_datetime.strftime("%Y-%m-%d at %H:%M")}.\n\n'
        'Please arrive on time.\n'
        'Thank you for using BarberManager!'
    )
    send_mail(subject, message, 'barber.manager.verify@gmail.com', [client.email])


def send_barber_reminder_email(barber, client, appointment_datetime):
    """
    Sends a reminder email to the barber 1 hour before an appointment.
    """
    subject = '[BarberManager] Upcoming Appointment Reminder'
    message = (
        f'Dear {barber.name} {barber.surname} (username: {barber.username}),\n\n'
        f'This is a reminder that you have an appointment with the client {client.name} {client.surname} '
        f'on {appointment_datetime.strftime("%Y-%m-%d at %H:%M")}.\n\n'
        'Get ready to provide great service!\n'
        'BarberManager Team'
    )
    send_mail(subject, message, 'barber.manager.verify@gmail.com', [barber.email])