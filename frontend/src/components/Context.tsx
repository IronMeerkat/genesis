import axios from "axios";
import { useState, useEffect, createContext, FC, useContext }  from "react";

type Params = {
    /**
     * Basic type for an authentication management context
     * access and refresh are tokens taken from the server
     * login and logout are reducer functions that do as their names sugget
     */
    access: string|null;
    refresh: string|null;
    login: (user:string, pass:string) => Promise<any>;
    logout: () => void;
}

axios.defaults.baseURL = 'http://localhost:8000/api'
const defaultHeaders = {
  /**
   * Headers you always need to send
   * Leave content-type as it is 
   * change the access-control headers as needed
   */
  'Content-Type': 'application/json',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Credentials': 'true'
}


const defaultState = {
    access: null,
    refresh:null,
    login: (async (user:string, pass:string) => {return await pass}),
    logout: () => {console.log('default logout')},
  };

const Context = createContext<Params>(defaultState);

const ContextProvider: FC = ({ children }) => {
    const [access, setAccess] = useState<string|null>(localStorage.getItem('access'))
    const [refresh, setRefresh] = useState<string|null>(localStorage.getItem('refresh'))

    const enter = (access: string, refresh?: string) => {
      /**
       * Places the context into an authenticated state. It gets invoked upon login but also upon returning to a session
       * It works by setting all the token states, the local storages, and setting an Authorization: Bearer token in axios
       */
      setAccess(access)
      axios.defaults.headers = {...defaultHeaders, 'Authorization': `Bearer ${access}`}
      localStorage.setItem('access', access);
      if(refresh) {
        setRefresh(refresh)
        localStorage.setItem('refresh', refresh);
      }
    }

    const logout = () => {
      /**
       * Reducer function for logging out, does the opposite of what const enter does.
       * It simply purges all the 
       */
      setAccess(null)
      setRefresh(null)
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      axios.defaults.headers = defaultHeaders
    }


    const login = async (username: string, password: string, remember: boolean = true) => {
      /**
       * Login reducer function. It sends the username and password to the server and upon authentication it retrieves the tokens.
       */
      return await axios.post('/auth/token/', JSON.stringify({ username, password })).then(resp =>{
        if(remember){
          enter(resp.data.access, resp.data.refresh)
        } else {
          enter(resp.data.access)  
        }
        return resp            
      }).catch(err => {
        logout()
        throw err
      })
    }

    const verify = async () => {
      /**
       * Ensures the bearer token is valid.
       * Do not abuse this function, set strict permissions in the backend to keep it from compromising data.
       */
      return await axios.post('auth/token/verify/', JSON.stringify({ token: access })).then(resp => {
        console.log(resp)
        return true
      }).catch(err => {
        logout()
        return false
      })
    }

    const refreshFunc = async () => {
      /**
       * Validates the refresh token and retrieves a new access token. 
       * Used to return to a logged in session
       */
      return await axios.post('auth/token/refresh/', JSON.stringify({ refresh: refresh })).then(resp => {
        enter(resp.data.access, resp.data.refresh)
        return resp            
      }).catch(err => {
        logout()
        throw err
      })
    }

    useEffect(() => {
      /**
       * Checks all the tokens upon initial load. 
       * This is to let the router know what to display and nothing else.
       * Do not validate anything on the front end, doing so would let anyone with basic knowledge of JS hack the system
       */

      axios.defaults.headers = defaultHeaders

      if(refresh){
        refreshFunc()
      } else if (access) {
        verify()
      }
    }, [])
  
  
    return (
      <Context.Provider
        value={{
          access,
          refresh,
          login,
          logout,
        }}
      >
        {children}
      </Context.Provider>
    );
  };

const useLoginContext = () =>  useContext(Context);

export {Context, ContextProvider, useLoginContext}

