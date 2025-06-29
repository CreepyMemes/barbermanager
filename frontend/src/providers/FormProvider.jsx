import { useState, useCallback } from 'react';
import FormContext from '@contexts/FormContext';

function FormProvider({ initialFields, onSubmit, children }) {
  const [fields, setFields] = useState(initialFields);
  const [error, setError] = useState('');

  /**
   * Handles input changes by updating field state.
   */
  const handleChange = useCallback((event) => {
    const { name, value } = event.target;
    setFields((prev) => ({ ...prev, [name]: value }));
  }, []);

  /**
   * Handles form submission, catches errors for display.
   */
  const handleSubmit = useCallback(
    async (event) => {
      event.preventDefault();
      try {
        setError(null);
        await onSubmit({ ...fields }); // Copy to avoid stale closure
      } catch (error) {
        setError(error?.response?.data?.detail || error?.message || 'Something went wrong');
      }
    },
    [fields, onSubmit],
  );

  return (
    <FormContext.Provider
      value={{
        fields,
        handleChange,
        error,
        setError,
        handleSubmit,
      }}
    >
      {children}
    </FormContext.Provider>
  );
}

export default FormProvider;
