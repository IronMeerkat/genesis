import React, {useEffect, useState} from "react";
import {Container, FormControl, FormGroup, Input, Button, InputLabel} from "@mui/material";
import axios from 'axios'
import { useThemeContext } from '../components';


const SignupPage = () => {

    const {access, refresh, login, logout} = useThemeContext()

    useEffect(()=>{
        if(access){
            window.location.href = '/';
        }
    }, [access])


    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [pass2, setPass2] = useState('')

    const [usernameError, setUsernameError] = useState(false)
    const [emailError, setEmailError] = useState(false)
    const [passwordError, setPassError] = useState(false)

    const dispatch = async () => {
        setEmailError(false)
        setUsernameError(false)
        setPassError(false)

        if (password !== pass2){
            setPassError(true)
            return
        }
        const payload = {username: username, email: email, password: password}
        console.log(axios.defaults.headers)
        
        await axios.post('/users/', JSON.stringify(payload)) //TODO create a user via the SimpleJWT package or independently?
            .then(() => {
                console.log(payload)
                login(username, password)
            }).catch(err => {
                switch (err.response.data.type){
                    case '["email"]': setEmailError(true); break;
                    case '["name"]': setUsernameError(true); break;
                    case '["name","email"]': setUsernameError(true); setEmailError(true); break;
                    default: setPassError(true); setEmailError(true); setUsernameError(true);
                }
            })
    }


    return(
        <Container maxWidth="xs">
            <FormGroup>
                <FormControl><InputLabel htmlFor="username">Username: </InputLabel><Input error={usernameError} required id="username" placeholder='meerkat' onChange={e => setUsername(e.target.value)}/></FormControl>
                <FormControl><InputLabel htmlFor="email">Email: </InputLabel><Input error={emailError} required id="email" placeholder='example@domain.com' onChange={e => setEmail(e.target.value)}/></FormControl>
                <FormControl><InputLabel htmlFor="pass">Password: </InputLabel><Input error={passwordError} required id="pass" placeholder='********' onChange={e => setPassword(e.target.value)}/></FormControl>
                <FormControl><InputLabel htmlFor="pass2">Password again: </InputLabel><Input error={passwordError} required id="pass2" placeholder='********' onChange={e => setPass2(e.target.value)}/></FormControl>
                    <br/><br/>
                <Button variant="contained" color="primary" onClick={dispatch}>Sign up</Button>
                    <br/><br/><br/><br/>
                <Button variant="contained" color="primary" onClick={()=> {window.location.href = '/login'}}>Or would you like to log in</Button>

            </FormGroup>
        </Container>
    );

}

export {SignupPage};