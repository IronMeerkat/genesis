import axios from "axios";
import { useState, useEffect, createContext, FC, useContext }  from "react";

type Params = {
    access: string|null;
    refresh: string|null;
    login: (user:string, pass:string) => Promise<any>;
    logout: () => void;
}

axios.defaults.baseURL = 'http://localhost:8000/api'
const defaultHeaders = {
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
      setAccess(access)
      axios.defaults.headers = {...defaultHeaders, 'Authorization': `Bearer ${access}`}
      localStorage.setItem('access', access);
      if(refresh) {
        setRefresh(refresh)
        localStorage.setItem('refresh', refresh);
      }
    }

    const logout = () => {
      setAccess(null)
      setRefresh(null)
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      axios.defaults.headers = defaultHeaders
    }


    const login = async (username: string, password: string, remember: boolean = true) => {
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
      return await axios.post('auth/token/verify/', JSON.stringify({ token: access })).then(resp => {
        console.log(resp)
        return true
      }).catch(err => {
        logout()
        return false
      })
    }

    const refreshFunc = async () => {
      return await axios.post('auth/token/refresh/', JSON.stringify({ refresh: refresh })).then(resp => {
        enter(resp.data.access, resp.data.refresh)
        return resp            
      }).catch(err => {
        logout()
        throw err
      })
    }

    useEffect(() => {
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

const useThemeContext = () =>  useContext(Context);

export {Context, ContextProvider, useThemeContext}

