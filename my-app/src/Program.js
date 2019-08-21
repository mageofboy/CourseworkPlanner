import React, { Component } from 'react';
import './Program.css';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";


const coursedata = require('./scrape_data/coursedata.json');


class Programs extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        list: coursedata
      };
    }

    render() {
        return (
            <div>
                <List items={this.state.list} />
            </div>
            );
        }
    }
  
  class List extends React.Component {
      constructor(props) {
          super(props);
          this.state = {
              filtered: []
          };
          this.handleChange = this.handleChange.bind(this);
      }
      
      componentDidMount() {
      this.setState({
        filtered: this.props.items
      });
    }
  
    componentWillReceiveProps(nextProps) {
      this.setState({
        filtered: nextProps.items
      });
    }
      
      handleChange(e) {
          // Variable to hold the original version of the list
      let currentList = [];
          // Variable to hold the filtered list before putting into state
      let newList = [];
          
          // If the search bar isn't empty
      if (e.target.value !== "") {
              // Assign the original list to currentList
        currentList = this.props.items;
              
              // Use .filter() to determine which items should be displayed
              // based on the search terms
        newList = currentList.filter(item => {
                  // change current item to lowercase
          const lc = item["Name"].toLowerCase();
                  // change search term to lowercase
          const filter = e.target.value.toLowerCase();
                  // check to see if the current list item includes the search term
                  // If it does, it will be added to newList. Using lowercase eliminates
                  // issues with capitalization in search terms and search content
          return lc.includes(filter);
        });
      } else {
              // If the search bar is empty, set newList to original task list
        newList = this.props.items;
      }
          // Set the filtered state based on what our rules added to newList
      this.setState({
        filtered: newList
      });
    }
      
      render() {
          return (
            <div>
                <div className="search">
                    <input type="text" className="input" onChange={this.handleChange} placeholder="Search..." />
                    <ul>
                        {this.state.filtered.map(item => (
                            <li key={item["Name"]} >
                                {/*
                                <a href={item["Homepage URL"]} target="_blank" rel="noopener noreferrer">
                                {item["Name"]}
                                </a>
                                */}

                                <Link to={{
                                  pathname:"requirement",
                                  state: {"data":item}
                                  }}>
                                  {item["Name"]}
                                </Link>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
          )
      }
  }
export default Programs;