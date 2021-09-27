import { useEffect, useState } from 'react';
import {Container, FormControl, FormGroup, Input, Button, InputLabel} from "@mui/material";

import { useLoginContext } from '../components';

const LoginPage = () => {

    const {access, refresh, login, logout} = useLoginContext()

    useEffect(()=>{
        /**
         * Send the user to / if they're logged in
         */
        if(access){
            window.location.href = '/';
        }
    }, [access])

    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    const [authError, setAuthError] = useState(false)

    const dispatch = async () => {
        /** 
         * Every field has a state, and typing a string into the field will set the state to that string.
         * Upon clicking the login button, the credentials will be sent to the server. 
         * If authenticated, the user will be routed to the homepage, otherwise the authError state will set to true
         */
        setAuthError(false)
        await login(username, password)
            .catch(error => {
                setAuthError(true)
                console.log(error.response.data)
            })

    }


    return (
        <Container maxWidth="xs">
            <FormGroup>
                <FormControl><InputLabel htmlFor="username">Username: </InputLabel><Input error={authError} required id="username" placeholder='meerkat' onChange={e => setUsername(e.target.value)}/></FormControl>
                <FormControl><InputLabel htmlFor="password">Password: </InputLabel><Input error={authError} required id="password" type="password" placeholder='********' onChange={e => setPassword(e.target.value)}/></FormControl>
                <br/><br/>
                <Button variant="contained" color="primary" onClick={dispatch}>Log in</Button>
                <br/><br/><br/><br/>
                <Button variant="contained" color="primary" onClick={()=> {window.location.href = '/signup'}}>Or would you like to sign up</Button>
            </FormGroup>
        </Container>
    )

}

export { LoginPage };