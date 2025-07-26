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

/**
 * Removes fields that are: undefined, null, empty string, or string with only whitespace, from a passed payload
 * Trims string fields from spaces
 */
export function cleanPayload(payload) {
  return Object.entries(payload).reduce((acc, [key, value]) => {
    if (value === undefined || value === null || (typeof value === 'string' && value.trim() === '')) {
      return acc;
    }

    acc[key] = typeof value === 'string' ? value.trim() : value;
    return acc;
  }, {});
}

/**
 * Validates that at least one field in the payload has a non-empty value.
 * Returns `undefined` if valid (at least one field is set), or the error message if not.
 * Optionally, pass a custom error message as the second argument.
 */
export function isAnyFieldSet(payload, errorMsg = 'Provide at least one value to update.') {
  const anyHasValue = Object.entries(payload).some(
    ([_, value]) =>
      (typeof value === 'string' && value.trim() !== '') || //
      (typeof value === 'number' && !isNaN(value)),
  );
  return anyHasValue ? undefined : errorMsg;
}
