import { useState, useEffect } from 'react';
import axios from "axios";
import {Container} from "@mui/material";
import { useLoginContext } from '../components';

const HomePage = () => {

    /**
     * Generic homepage
     */


    return (
        <Container maxWidth="sm">
            <h1>Hi !</h1>
            <p>You're logged in with React & JWT!!</p>
            <h3>Users from secure api end point:</h3>
            
        </Container>
    );
    
}

export { HomePage };