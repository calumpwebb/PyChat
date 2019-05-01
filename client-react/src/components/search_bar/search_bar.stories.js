import React from 'react';

import { storiesOf } from '@storybook/react';

import SearchBar from './index.js';

import { withKnobs, text } from "@storybook/addon-knobs";

const stories = storiesOf('SearchBar', module);
stories.addDecorator(withKnobs);

stories.add('Basic', () => {
    const placeHolder = text('Place Holder', 'Where to?');

    return (<SearchBar placeHolder={placeHolder}/>)
});