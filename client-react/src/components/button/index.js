import React, { Component } from 'react';
import styled from 'styled-components'
import PropTypes from 'prop-types';

const StyledDiv = styled.div`
    background: red;
`;

export default class Button extends Component {
    render () {
        return (
            <StyledDiv className={this.props.className}>
                I'm a button!
            </StyledDiv>
        )
    }
}

Button.defaultProps = {

};

Button.propTypes = {
    className: PropTypes.object
};