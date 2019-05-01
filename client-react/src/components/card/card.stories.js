import React from 'react';

import { storiesOf } from '@storybook/react';
import { withKnobs, text, boolean, number } from '@storybook/addon-knobs';

import Card from './index.js';

const stories = storiesOf('Card', module);
stories.addDecorator(withKnobs);

stories.add('Basic', () => {
    const height = number('Height', 300);
    const width = number('Width', 300);

    return (<Card height={`${height}px`} width={`${width}px`}/>)
});