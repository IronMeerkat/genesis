import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import { PrivateRoute, ContextProvider, Header } from './components';
import "./App.css";
import { LoginPage, HomePage, SignupPage } from "./pages";
import { Stack } from "@mui/material";


const App = () => {

    /**
     * ContextProvider will tell you anywhere in the app if you're logged in
     * Stack is a 1-column grid, and it has 2 components: Header and Router
     */

   
	return (
        <ContextProvider>
            <Stack >
                <Header />
                <Router>
                    <Switch>
                        <Route path="/login"><LoginPage/></Route>
                        <Route path="/signup"><SignupPage/></Route>
                        <PrivateRoute path="/"><HomePage /></PrivateRoute>
                    </Switch>
                </Router>
            </Stack>
        </ContextProvider>
	);
}

export default App;