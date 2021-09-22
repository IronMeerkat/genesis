import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import { PrivateRoute, ContextProvider, Header } from './components';
import "./App.css";
import { LoginPage, HomePage, SignupPage } from "./pages";
import { Stack} from "@mui/material";


const App = () => {

   
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