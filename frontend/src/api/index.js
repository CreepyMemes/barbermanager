import axiosInstance from './axios/interceptors';
import * as auth from './services/auth';
import * as admin from './services/admin';
import * as barber from './services/barber';
import * as client from './services/client';
import * as pub from './services/public';
import * as image from './services/image';

export const api = {
  instance: axiosInstance,
  auth,
  admin,
  barber,
  client,
  pub,
  image,
};

export default api;
