import React, { Component } from 'react';
import PropTypes from 'prop-types'

import styled from 'styled-components'

import Card from '../card';

export default class SearchInput extends Component {

    constructor (props) {
        super(props);

        this.onKeyPress = this.onKeyPress.bind(this);

        this.state = {
            inputValue: ''
        };
    }

    componentDidMount () {
        document.addEventListener('keydown', this.onKeyPress, false);
    }

    componentWillUnmount () {
        document.removeEventListener('keydown', this.onKeyPress, false);
    }

    onKeyPress = (event) => {
        if (event.keyCode === 13) {
            return this.focusInput();
        }

        return true;
    };

    focusInput = () => {
        this.StyledInput.focus();
    };

    onInputChange = (event) => {
        this.setState({
            inputValue: event.target.value
        })
    };

    onFocus = (event) => {
        event.target.placeholder = "";
    };

    onBlur = (event) => {
        event.target.placeholder = this.props.placeHolder;
    };

    render () {
        return (
            <Card width={'600px'}>
                <StyledInput
                    value={this.state.inputValue}
                    onChange={this.onInputChange}
                    placeholder={this.props.placeHolder}
                    onBlur={this.onBlur}
                    onFocus={this.onFocus}
                    ref={(input) => { this.StyledInput = input; }}
                />
            </Card>
        )
    }
}

SearchInput.defaultProps = {
    placeHolder: null
};

SearchInput.propTypes = {
    placeHolder: PropTypes.string
};

const StyledInput = styled.input`
    width: calc(100% - 20px);
    height: calc(100% - 20px);
    outline: none;
    border: none;
    margin: 10px;
    font-size: 30px;
    font-family: SF Pro Display;
    font-weight: normal;
    color: #4E4E4E;
    line-height: normal;
    text-align: center;
    
    &::placeholder {
        opacity: 0.5;
    } 
`;
