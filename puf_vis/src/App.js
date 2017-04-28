import React, { Component} from 'react';
import symbol from './symbol.svg';
import './App.css';

const data = require('../data/example');

let indent = 0;
const startTaskHeight = 5;
const height = 5;
const endHeight = 1;
const blockWidth = 12;

// const onMouseOver = function(fullLine){
//
// };

const taskStyle = function (blockHeight) {
    return {
        background: '#07a3c6',
        width: blockWidth + 'em',
        height: blockHeight + 'em',
        margin: '0 auto',
        borderStyle: 'solid',
        borderColor: "#01819e",
        position: 'relative',
        left: indent * 50
    }
};

const movementStyle = function () {
    return {
        background: '#57e021',
        width: blockWidth + 'em',
        height: height + 'em',
        margin: '0 auto',
        borderStyle: 'solid',
        borderColor: "#30a501",
        position: 'relative',
        left: indent * 50
    }
};

const pyStyle = function () {
    return {
        background: '#505050',
        width: blockWidth + 'em',
        height: height + 'em',
        margin: '0 auto',
        borderStyle: 'solid',
        borderColor: "#000",
        position: 'relative',
        left: indent * 50,
        color: '#FFFFFF'
    }
};


const logicStyle = function () {
    return {
        background: '#bc0adb',
        width: blockWidth + 'em',
        height: height + 'em',
        margin: '0 auto',
        borderStyle: 'solid',
        borderColor: "#7201a3",
        position: 'relative',
        left: indent * 50
    }
};

const controlStyle = function (blockHeight) {
    return {
        background: "#f4bb1d",
        width: blockWidth + 'em',
        height: blockHeight + 'em',
        margin: '0 auto',
        borderStyle: 'solid',
        borderColor: "#edae02",
        position: 'relative',
        left: indent * 50
    }
};

const blockHeading = function () {
    return {
        fontWeight: '700',
        position: 'relative',
        margin: '0'
    }
};

const functionHeading = function () {
    return {
        fontWeight: '700',
        position: 'relative',
        top: '20',
        margin: '0'
    }
};

const pythonHeading = function () {
    return {
        fontWeight: '700',
        position: 'relative',
        top: '20',
        margin: '0'
    }
};


const controlHeading = function () {
    return {
        fontWeight: '700',
        position: 'relative',
        top: '15',
        margin: '0'
    }
};

const blockInfo = function() {
    return {
        textAlign: 'left',
        margin: '2'
    }
};

const rowHead = function() {
    return {
        margin: '2',
        fontWeight: '600'
    }
};


class TaskBlock extends Component{

    render(){
        const element = (
            <div style={taskStyle(startTaskHeight)}>
                <p style={blockHeading()}>{this.props.primary}</p>
                <table>
                    <tr>
                        <td style={rowHead()}>Parameters</td>
                        <td style={blockInfo()}>{this.props.secondary}</td>
                    </tr>
                </table>
            </div>

        );
        indent++;
        return element

    }
}

class CallBlock extends Component{

    render(){
        const element = (
            <div style={taskStyle(startTaskHeight)}>
                <p style={blockHeading()}>Run:</p>
                <table>
                    <tr>
                        <td style={blockInfo()}>{this.props.primary}</td>
                    </tr>
                    <tr>
                        <td style={rowHead()}>With</td>
                        <td style={blockInfo()}>{this.props.secondary}</td>
                    </tr>
                </table>
            </div>

        );
        return element

    }
}

class ControlBlock extends Component {
    render(){
        const element = (
            <div style={controlStyle(startTaskHeight)}>
                <p style={controlHeading(height)}>{this.props.primary}</p>
                <p>{this.props.secondary}</p>
            </div>

        );
        indent++;
        return element

    }
}

class EndTaskBlock extends TaskBlock {
    render(){
        indent--;
        return <div style={taskStyle(endHeight)}></div>
    }
}

class EndControlBlock extends ControlBlock {
    render(){
        indent--;
        return ( <div style={controlStyle(endHeight)}></div>)
    }
}

class MovementBlock extends Component {
    render(){
        return (
            <div style={movementStyle()}>
                <p style={blockHeading()}>{this.props.tertiary}:</p>
                <table>
                    <tr style={blockInfo()}>
                        <td style={rowHead()}>Direction: </td>
                        <td>{this.props.primary}</td>
                    </tr>
                    <tr style={blockInfo()}>
                        <td style={rowHead()}>Duration: </td>
                        <td>{this.props.secondary}</td>
                    </tr>
                </table>
            </div>
        )

    }
}

class PythonBlock extends Component {
    render(){
        return (
            <div style={pyStyle()}>
                <p style={pythonHeading()}>Python</p>
            </div>
        )

    }
}

class LogicBlock extends Component {
    render(){
        return (
            <div style={logicStyle()}>
                <p style={blockHeading()}>{this.props.tertiary}</p>
                <table>
                    <tr style={blockInfo()}>
                        <td style={rowHead()}>Set: </td>
                        <td>{this.props.primary}</td>
                    </tr>
                    <tr style={blockInfo()}>
                        <td style={rowHead()}>To: </td>
                        <td>{this.props.secondary}</td>
                    </tr>
                </table>
            </div>
        )

    }
}


class App extends Component {

  render() {
    let blocks = [];
    let openClauses = [];
    let lastIndent = -1;
    for(let i = 0; i < data.length; i++) {
        let block = data[i];
        console.log(block);
        let type = block.type.toLowerCase();
        console.log(lastIndent);
        while(block.indent < lastIndent){
            let toAdd = openClauses.pop();
            if(toAdd === 'task'){
                blocks.push(<EndTaskBlock/>)
            } else if (toAdd === 'control'){
                blocks.push(<EndControlBlock/>)
            } else {
                console.error("could not close block of type: " + toAdd);
            }
            lastIndent--;
        }
        lastIndent = block.indent;
        switch (type) {
            case "task":
                openClauses.push('task');
                blocks.push(<TaskBlock primary={block.primary} secondary={block.secondary}/>);
                break;
            case "movement":
                blocks.push(<MovementBlock primary={block.primary} secondary={block.secondary} tertiary={block.tertiary}/>);
                break;
            case "logic":
                blocks.push(<LogicBlock primary={block.primary} secondary={block.secondary} tertiary={block.tertiary}/>);
                break;
            case "python":
                blocks.push(<PythonBlock primary={block.primary} secondary={block.secondary}/>);
                break;
            case "control":
                openClauses.push('control');
                blocks.push(<ControlBlock primary={block.primary} secondary={block.secondary}/>);
                break;
            case "run":
                blocks.push(<CallBlock primary={block.primary} secondary={block.secondary}/>);
                break;
            default:
                console.error("invalid block type: " + type);
                break;
        }
    }
    while(openClauses.length > 0){
        let toAdd = openClauses.pop();
        if(toAdd === 'task'){
            blocks.push(<EndTaskBlock/>)
        } else if (toAdd === 'control'){
            blocks.push(<EndControlBlock/>)
        } else {
            console.error("could not close block of type: " + toAdd);
        }
    }
    return (
      <div className="App">
        <div className="App-header">
          <img src={symbol} className="App-logo" alt="logo" />
          <h2>VisTool</h2>
            <h5>v0.1.0</h5>
        </div>
          {blocks}

      </div>


    );
  }
}

export default App;
