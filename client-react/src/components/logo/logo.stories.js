import React from 'react';

import { storiesOf } from '@storybook/react';

import Logo from './index.js';

const stories = storiesOf('Logo', module);

stories.add('Main Logo', () => {
    return (<Logo/>)
});