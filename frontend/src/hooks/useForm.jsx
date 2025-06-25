import { useContext } from 'react';
import FormContext from '@contexts/FormContext';

/**
 * Custom React hook for using Form by passing state to it
 */
export const useForm = () => useContext(FormContext);
