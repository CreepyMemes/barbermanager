/**
 * Helper function that vaildates whether a passed string is a valid email
 */
export function isEmail(value) {
  return /\S+@\S+\.\S+/.test(value);
}
/**
 * Remove dashes/underscores and capitalize next letter in styels
 */
export function camelizeStyle(prefix, value) {
  if (!value) return prefix;

  const upper = value.replace(/[-_]+(.)?/g, (_, chr) => (chr ? chr.toUpperCase() : ''));

  return prefix + upper.charAt(0).toUpperCase() + upper.slice(1);
}
