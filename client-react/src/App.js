import React, { Component } from 'react';
import styled from 'styled-components'
import LoginPage from './pages/LoginPage';

const AppDiv = styled.div`
    width: 100%;
    height: 100%;
    margin: 0px;
    padding: 0px;
    position: absolute;
    display: flex;
    justify-content: center;
    background: black;
    color: white;
`;

class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <AppDiv>
                <LoginPage/>
            </AppDiv>
        );
    }
}

export default App;
