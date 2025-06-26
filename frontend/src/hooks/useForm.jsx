import { useContext } from 'react';
import FormContext from '@contexts/FormContext';

/**
 * Custom React hook for accessing form state and methods.
 */
export function useForm() {
  const context = useContext(FormContext);
  if (!context) {
    throw new Error('useForm must be used within a FormProvider');
  }
  return context;
}
