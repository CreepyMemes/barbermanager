import { useState, useCallback } from 'react';
import FormContext from '@contexts/FormContext';

export default function FormProvider({ initialFields, onSubmit, children }) {
  const [fields, setFields] = useState(initialFields);
  const [error, setError] = useState('');

  /**
   * Handles input changes by updating field state.
   */
  const handleChange = useCallback((event) => {
    setFields((prev) => ({
      ...prev,
      [event.target.name]: event.target.value,
    }));
  }, []);

  /**
   * Handles form submission, catches errors for display.
   */
  const handleSubmit = useCallback(
    async (event) => {
      event.preventDefault();
      try {
        await onSubmit(fields);
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
