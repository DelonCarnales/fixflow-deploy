import test from 'node:test';
import assert from 'node:assert/strict';
import {chooseApiBase} from './apiBase.js';

test('local split-port development calls the API on port 8000', () => {
  assert.equal(chooseApiBase('localhost', '5173', 'http:'), 'http://127.0.0.1:8000');
  assert.equal(chooseApiBase('127.0.0.1', '5173', 'http:'), 'http://127.0.0.1:8000');
});

test('the page served by FastAPI uses the same origin', () => {
  assert.equal(chooseApiBase('localhost', '8000', 'http:'), '');
  assert.equal(chooseApiBase('127.0.0.1', '8000', 'http:'), '');
});

test('a public host name (Docker, Render, AWS) uses the same origin', () => {
  assert.equal(chooseApiBase('fixflow.onrender.com', '', 'https:'), '');
  assert.equal(chooseApiBase('ec2-1-2-3-4.compute.amazonaws.com', '80', 'http:'), '');
});

test('Codespaces behaviour is unchanged', () => {
  assert.equal(chooseApiBase('demo-8000.app.github.dev', '', 'https:'), '');
  assert.equal(chooseApiBase('demo-5173.app.github.dev', '', 'https:'), 'https://demo-8000.app.github.dev');
});
