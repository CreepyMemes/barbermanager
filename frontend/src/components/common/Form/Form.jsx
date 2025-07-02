import { useForm } from '@hooks/useForm';
import FormProvider from '@providers/FormProvider';

function Form({ className, initialFields, onSubmit, validate, children }) {
  function InnerForm() {
    const { handleSubmit } = useForm();

    return (
      <form className={className} onSubmit={handleSubmit} autoComplete="on">
        {children}
      </form>
    );
  }

  return (
    <FormProvider initialFields={initialFields} onSubmit={onSubmit} validate={validate}>
      <InnerForm />
    </FormProvider>
  );
}

export default Form;
