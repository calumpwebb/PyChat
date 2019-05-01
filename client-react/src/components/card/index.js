import React, { Component } from 'react';
import styled from 'styled-components'
import PropTypes from "prop-types";

const StyledDiv = styled.div`
  width: ${props => props.width * 8};
  height: ${props => props.height * 8};
  background: black;
`;

export default class Card extends Component {
    render () {
        return (
            <StyledDiv height={this.props.height} width={this.props.width}>
                {this.props.children}
            </StyledDiv>
        )
    }
}

Card.defaultProps = {
    height: 'auto',
    width: 'auto'
};

Card.propTypes = {
    height: PropTypes.string,
    width: PropTypes.string
};