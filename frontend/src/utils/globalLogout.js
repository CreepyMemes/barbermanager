// Global logout handler function
let globalLogout = null;

/**
 * Function that sets the global logout funcion with passed argument
 */
export function setGlobalLogout(fn) {
  globalLogout = fn;
}

/**
 * Function that performs global logout, if it's already set
 */
export function performGlobalLogout() {
  globalLogout && globalLogout();
}
