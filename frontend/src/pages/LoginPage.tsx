import { useEffect, useState } from 'react';
import {Container, FormControl, FormGroup, Input, Button, InputLabel} from "@mui/material";

import { useThemeContext } from '../components';

const LoginPage = () => {

    const {access, refresh, login, logout} = useThemeContext()

    useEffect(()=>{
        if(access){
            window.location.href = '/';
        }
    }, [access])

    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    const [authError, setAuthError] = useState(false)

    const dispatch = async () => {
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