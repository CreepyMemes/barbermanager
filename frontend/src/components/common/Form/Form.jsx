import { useForm } from '@hooks/useForm';
import FormProvider from '@providers/FormProvider';

function Form({ className, initialFields, onSubmit, children }) {
  function InnerForm() {
    const { handleSubmit } = useForm();

    return (
      <form className={className} onSubmit={handleSubmit} autoComplete="on">
        {children}
      </form>
    );
  }

  return (
    <FormProvider initialFields={initialFields} onSubmit={onSubmit}>
      <InnerForm />
    </FormProvider>
  );
}

export default Form;
