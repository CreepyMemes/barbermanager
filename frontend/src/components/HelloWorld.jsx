import { useState } from 'react';

function HelloWorld() {

    const [visibile, setVisibile] = useState(true)
    const [testo, setTesto]= useState("testo")
    const [username, setUsername]= useState("")

    const azioneClick = () => {
        //alert("click sul bottone allert");
        //console.log("click sul bottone");
        setVisibile(!visibile);
        if (visibile == true) {
            setTesto("testo");
        }else {
            setTesto("ciao");
        }
    }

    const onChange = (event) => {
        console.log("username: -", username, "-")
        setUsername(event.target.value);
    }


    return (
        <div>

            <button onClick={azioneClick}>{visibile ? "nascondi": "Mostra"} messaggio</button>
            <br></br>
            {visibile && <p>Questo è un messaggio visibile</p>}
            <h1>{testo}</h1>
            <input type="text" value={username} onChange={onChange}></input>
        </div>
    );
}

export default HelloWorld;