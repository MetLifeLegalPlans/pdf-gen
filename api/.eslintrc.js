"use strict";

module.exports = {
  parser: 'babel-eslint',
  extends: ['airbnb-base', 'prettier'],
  plugins: ['prettier'],
  rules: {
    // for loops should not be restricted
    'no-restricted-syntax': ['off']
  },
  settings: {
    'import/resolver': {
      node: {
        paths: './src'
      }
    }
  }
};