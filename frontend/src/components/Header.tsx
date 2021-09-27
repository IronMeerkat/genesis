import { useLoginContext } from "."
import axios from "axios";
import {AppBar, Toolbar, IconButton, Typography, Button} from "@mui/material";
import MenuIcon from '@mui/icons-material/Menu';
import { useEffect, useState } from "react";



const Header = () => {

    /**
     * Toolbar that will show up on top of the app, regarless which page is open
     * Default is the Basic App Bar
     * Further documentation https://mui.com/components/app-bar/
     */

    const {access, refresh, login, logout} = useLoginContext()
    const [username, setUsername] = useState<string>()

    const getUsername = async () => {
        await axios.get('/users').then(resp => {
            setUsername(resp.data.username)
        })
    }

    useEffect(()=> {
        if (access){
            getUsername()
        } else {
            setUsername('guest')
        }
    }, [access])


    return (

            
            <AppBar position="sticky"> 
            {/* Keep position=sticky to avoid overlapping components */}
                <Toolbar>
                <IconButton
                    size="large"
                    edge="start"
                    color="inherit"
                    aria-label="menu"
                    sx={{ mr: 2 }}
                >
                    <MenuIcon />
                </IconButton>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    Welcome, {username}
                </Typography>
                {access ? 
                    <Button color="inherit" onClick={logout}>Logout</Button> :
                    <></>}
                </Toolbar>
            </AppBar>

    )



}

export {Header}