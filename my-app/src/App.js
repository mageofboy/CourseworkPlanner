import React, { Component } from 'react';
import './App.css';
import Programs from './Program.js'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Requirement from './Requirement.js'

class App extends Component {
  render() {
    return (
      <Router>
      <div className="App">
        <Route exact path="/" component={Programs}/>
        <Route path="/requirement" component={Requirement} />
      </div>
      </Router>
    );
  }
}
export default App;
