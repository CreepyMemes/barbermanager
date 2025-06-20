function CustomInput({value,type,onChange}) {

    return (
        <input type={type} value={value} onChange={onChange}></input>
    );
}


export default CustomInput;