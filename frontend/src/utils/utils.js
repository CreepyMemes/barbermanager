export function isEmail(value) {
  // Simple email heuristic
  return /\S+@\S+\.\S+/.test(value);
}
