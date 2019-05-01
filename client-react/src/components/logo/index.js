import React, { Component } from 'react';
import styled from 'styled-components'
import PropTypes from 'prop-types';

const StyledDiv = styled.div`
    font-weight: bold;
    font-family: monospace;
    white-space: pre;
    margin-top: 10%;
    position: relative;
    user-select: none;
`;

export default class Logo extends Component {
    render () {
        return (
            <StyledDiv className={this.props.className}>{
                `
$$$$$$$\\             $$$$$$\\  $$\\                  $$\\
$$  __$$\\           $$  __$$\\ $$ |                 $$ |
$$ |  $$ |$$\\   $$\\ $$ /  \\__|$$$$$$$\\   $$$$$$\\ $$$$$$\\
$$$$$$$  |$$ |  $$ |$$ |      $$  __$$\\  \\____$$\\\\_$$  _|
$$  ____/ $$ |  $$ |$$ |      $$ |  $$ | $$$$$$$ | $$ |
$$ |      $$ |  $$ |$$ |  $$\\ $$ |  $$ |$$  __$$ | $$ |$$\\
$$ |      \\$$$$$$$ |\\$$$$$$  |$$ |  $$ |\\$$$$$$$ | \\$$$$  |
\\__|       \\____$$ | \\______/ \\__|  \\__| \\_______|  \\____/
          $$\\   $$ |
          \\$$$$$$  |
           \\______/
                `
            }

            </StyledDiv>
        )
    }
}

Logo.defaultProps = {

};

Logo.propTypes = {
    className: PropTypes.object
};