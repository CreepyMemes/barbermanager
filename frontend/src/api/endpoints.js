/**
 * API endpoint definitions used throughout the application.
 * Dynamic routes are defined using arrow functions with parameters.
 */
export const ENDPOINTS = {
  // Auth Routes
  auth: {
    me: '/auth/me/',
    login: '/auth/login/',
    logout: '/auth/logout/',
    refresh: '/auth/refresh-token/',
    resetPassword: '/auth/reset-password/',
    registerClient: '/auth/register/',
    registerBarber: (uidb64, token) => `/auth/register/${uidb64}/${token}/`,
    emailFromToken: (uidb64, token) => `/auth/email/${uidb64}/${token}/`,
    resetPasswordConfirm: (uidb64, token) => `/auth/reset-password/${uidb64}/${token}/`,
    verifyEmail: (uidb64, token) => `/auth/verify/${uidb64}/${token}/`,
  },

  // Admin Routes
  admin: {
    profile: '/admin/profile/',
    barbers: '/admin/barbers/',
    clients: '/admin/clients/',
    appointments: '/admin/appointments/',
    inviteBarber: '/admin/barbers/invite/',
    barber: (barberId) => `/admin/barbers/${barberId}/`,
    barberAvailabilities: (barberId) => `/admin/barbers/${barberId}/availabilities/`,
    barberAvailability: (barberId, availabilityId) => `/admin/barbers/${barberId}/availabilities/${availabilityId}/`,
  },

  // Barber Routes
  barber: {
    profile: '/barber/profile/',
    availabilities: '/barber/availabilities/',
    appointments: '/barber/appointments/',
    reviews: '/barber/reviews/',
    services: '/barber/services/',
    service: (serviceId) => `/barber/services/${serviceId}/`,
  },

  // Client Routes
  client: {
    profile: '/client/profile/',
    appointments: '/client/appointments/',
    reviews: '/client/reviews/',
    review: (reviewId) => `/client/reviews/${reviewId}/`,
    createReview: (appointmentId) => `/client/reviews/appointments/${appointmentId}/`,
    createAppointment: (barberId) => `/client/appointments/barbers/${barberId}/`,
    appointment: (appointmentId) => `/client/appointments/${appointmentId}/`,
  },

  // Public Routes
  public: {
    barbers: '/public/barbers/',
    barberAvailabilities: (barberId) => `/public/barbers/${barberId}/availabilities/`,
    barberProfile: (barberId) => `/public/barbers/${barberId}/profile/`,
    barberServices: (barberId) => `/public/barbers/${barberId}/services/`,
    clientProfile: (clientId) => `/public/clients/${clientId}/profile/`,
  },

  // Image Routes
  image: {
    profile: '/image/profile/',
  },
};
