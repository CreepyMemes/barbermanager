import CustomButton from "@components/CustomButton";
import CustomInput from "@components/CustomInput";

function Login({onLogin}) {

const azioneClick = () => {
        alert("click sul bottone allert");
        //console.log("click sul bottone");
        onLogin();
        
    }

    const onChange = (event) => {
        console.log(event.target.value);
    }




    return (
        <div>
            <h1>Login</h1>
            <CustomInput  type="text" onChange={onChange}></CustomInput>
            <CustomButton onClick={azioneClick} text="cliccami"></CustomButton>
        </div>
    )
}

export default Login;