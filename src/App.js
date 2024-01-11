import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import  { Redirect } from 'react-router-dom'
import Home from './components/Home';

function App() {
  return (
    <Router>
      <div className="App">
        <div className="content">
            <Switch>
              <Route exact path="/"><Redirect to='/extras-about_m'  /></Route>
              <Route exact path="/:id"><Home /></Route>
            </Switch>
        </div>
      </div>
    </Router>
  );
}

export default App;
