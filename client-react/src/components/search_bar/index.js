import React, { Component } from 'react';
import PropTypes from 'prop-types'

import SearchInput from '../search_input';

export default class SearchBar extends Component {

    render () {
        return (
            <div>
                <SearchInput
                    placeHolder={this.props.placeHolder}
                />
            </div>
        )
    }
}

SearchBar.defaultProps = {
    placeHolder: null
};

SearchBar.propTypes = {
    placeHolder: PropTypes.string
};
