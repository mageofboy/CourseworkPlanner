import React, { Component } from 'react';
import './requirement.css'
const temp = {
            "title": "DOES NOT EXIST",
            "description": "",
            "units": ""
            }
class Requirement extends Component {
    constructor(props) {
        super(props);
        this.data = this.props.location.state.data
        this.name = this.data["Name"]
        this.hasmajor = this.data["Has Major"]
        this.hasminor = this.data["Has Minor"]
        this.majorreq = this.hasmajor ? this.data["Major Requirements"] : [temp]
        this.minorreq = this.hasminor ? this.data["Minor Requirements"] : [temp]
    }
    render() {
        return (
        <div>
            <h1> {this.name}</h1>
            <h2> Major Requirements </h2>
            <ul>
            {this.majorreq.map(item => (
                <li key={item["title"]}>
                    <p>{item["title"]} {this.hasmajor ? "- " : ""} {item["description"]} {this.hasmajor ? " - " : ""} {item["units"]}</p>
                </li>
            ))}
            </ul>
            <h2> Minor Requirements </h2>
            <ul>
            {this.minorreq.map(item => (
                <li key={item["title"]}>
                    <p>{item["title"]} {this.hasminor ? "- " : ""} {item["description"]}  {this.hasminor ? " - " : ""} {item["units"]}</p>
                </li>
            ))}
            </ul>
        </div>
        );
    }
}
export default Requirement;
