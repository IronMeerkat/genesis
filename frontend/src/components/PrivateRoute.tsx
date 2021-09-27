import { FC, ReactNode,useEffect } from 'react';
import { Route, Redirect } from 'react-router-dom';
import { useLoginContext } from '.';


type Props = {
    path: string;
    children?: ReactNode;
}

const PrivateRoute: FC<Props> = props => {

    const {access, refresh, login, logout} = useLoginContext()

    /**
     * Simple override of react-router-dom's Route component
     * Check's for the presence of an access token. 
     * If one is present, it acts as a regular Route, otherwise it redirects to /login
     */


    useEffect(() => {
        console.log('private route')
    }, [access])


    return(access ? 
            <Route path={props.path}> {props.children} </Route> :
            <Redirect to={{ pathname: '/login'}} />
        )
}

export { PrivateRoute }