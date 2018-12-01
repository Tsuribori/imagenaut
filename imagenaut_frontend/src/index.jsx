/* eslint-disable import/no-extraneous-dependencies */
import { render } from 'react-dom';
import Thread from './components/Thread';

const root = document.getElementById('react_root');
console.log('hello');
render(
  (
    <Thread />
  ), root,
);
