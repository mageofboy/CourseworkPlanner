import React, { Component } from 'react';
import './App.css';

const coursedata = require('./scrape_data/coursedata.json');

const courses = (data) => {
  let courselst = []
  data.forEach(function(each){
    courselst.push(<li><a href={each["Homepage URL"]}>{each["Name"]}</a></li>)
  })
  return courselst
}
class App extends Component {
  render() {
    return (
      <div className="App">
        <ul>
          {courses(coursedata)}
        </ul>
      </div>
    );
  }
}
export default App;
