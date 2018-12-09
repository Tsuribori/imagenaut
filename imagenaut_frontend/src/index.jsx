/* eslint-disable import/no-extraneous-dependencies */
import { render } from 'react-dom';
import React from 'react';
import Thread from './Thread';

const root = document.getElementById('react_root');

render(
  (
    <Thread />
  ), root,
);
