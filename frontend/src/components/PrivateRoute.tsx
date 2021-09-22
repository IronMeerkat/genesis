import React, { Component, FC, ReactNode, ReactChild, useContext, useEffect, useLayoutEffect } from 'react';
import { Route, Redirect, RouteProps } from 'react-router-dom';
import { Context, useThemeContext } from '.';


type Props = {
    path: string;
    children?: ReactNode;
}

const PrivateRoute: FC<Props> = props => {

    const {access, refresh, login, logout} = useThemeContext()


    useEffect(() => {
        console.log('private route')
    }, [access])


    return(access ? 
            <Route path={props.path}> {props.children} </Route> :
            <Redirect to={{ pathname: '/login'}} />
        )
}

export { PrivateRoute }