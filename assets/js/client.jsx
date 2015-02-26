/** @jsx React.DOM */

'use strict';

var React = require('react');
var components = require('./components');

React.render(<components.Hello />, document.getElementById('hello'));
// React.renderToString(<components.Hello />);
