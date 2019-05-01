import React, { Component } from 'react';
import styled from 'styled-components'
import PropTypes from 'prop-types';

import Logo from '../components/logo';
import Button from '../components/button';


const StyledLogo = styled(Logo)`
    
`;

const StyledButtonLeft = styled(Button)`

`;

export default class LoginPage extends Component {
    render () {
        return (
            <div>
                <StyledLogo/>
                <div>
                    <Button/>

                </div>
            </div>

        )
    }
}

LoginPage.defaultProps = {

};

LoginPage.propTypes = {
    className: PropTypes.object
};