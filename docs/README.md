<div align="center">
  <img src="../frontend/assets/images/logo.png" height="100px" alt="BarberManager Logo"/>
  <h3>BarberManager – Management Software for Barber Shops</h3>
</div>

# Description

**BarberManager** is a comprehensive SaaS platform designed to streamline, digitalize, and optimize everyday operations in barber shops. With tools for booking, staff, client, and schedule management, BarberManager ensures efficient workflows for admins, barbers, and clients alike.

This application includes secure registration, appointment booking and reminders, reviews, detailed management dashboards, and user profile features, all built on a Django RESTful API.

## Core Features

### User & Account Management
- **Role-based accounts:**  
  - **Admins:** Created manually via shell for full shop management.
  - **Clients:** Self-register via the web; must verify email.
  - **Barbers:** Can sign up only after an admin invitation; registration is completed through a secure email link.
- All users can:
  - Log in with username or email (JWT authentication).
  - Recover/reset passwords via email-secured links.
  - Edit or permanently delete their profile and associated data.
  - Upload or delete their profile pictures.

### Registration & Authentication Flow
- Admins: Created via CLI, making them inaccessible via public endpoints.
- Clients:  
  - Register via `/auth/register/`: must provide full personal details, a unique username, and valid email.
  - Email confirmation required for activation (`/auth/verify/{uidb64}/{token}/`).
- Barbers:
  - Admins invite via `/admin/barbers/invite/` (email only).
  - Complete registration via magical invite link (`/auth/register/{uidb64}/{token}/`) by setting username, password, and personal details.
- Robust JWT token-based authentication (login, logout, refresh, me endpoints).

### Booking & Scheduling
- **Clients:**
  - Book appointments by browsing active barbers, viewing their services and real-time availabilities.
  - Only one active appointment at a time.
  - Receive automatic email reminders.
  - Cancel bookings if appointment is still pending.
  - View past appointment history.
- **Barbers:**
  - Manage their service offerings (add, edit, remove).
  - Access their schedule of ongoing and upcoming appointments.
  - Receive client reviews and ratings.

### Reviews & Ratings
- Clients can leave one review per completed appointment for a barber, editable or removable after posting.
- Barbers can easily access, monitor, and respond to their client feedback.

### Staff & Resource Administration
- **Admin Dashboard:**
  - Full CRUD for barber and client management (`/admin/barbers/`, `/admin/clients/`).
  - Manage barber availabilities: add, edit, or remove availability slots for each staff member.
  - Invite new barbers via email; remove barbers by user ID.
  - Monitor all salon appointments and aggregate activity statistics for informed business decisions.

### Public-Facing Information
- Anyone can:
  - Browse a directory of barbers, their public profiles, offered services, and availability slots.
  - View public client profiles as appropriate.

## Technical Highlights
- **RESTful API-first design**: All operations exposed for secure, flexible integrations (`/api/`).
- **Robust authentication:** JWT-based user session management.
- **Email-driven flows:** For sensitive operations (registrations, invitations, password recovery).
- **Granular permissioning:** Role-secured endpoints for admins, barbers, and clients.
- **Modern user experience:** Email notifications, mobile-ready, profile images, and detailed dashboards.
- **OpenAPI-compliant schema:** Complete, self-documented API.
