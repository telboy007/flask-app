#!/usr/bin/env python

import logging
import os
import pytest
import sys
import tempfile
import unittest

sys.path.append('./flask_app')

import flask_app


class FlaskAppTestCase(unittest.TestCase):

    # so capsys can be used within TestClass
    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys


    def setUp(self):
        """ checks database config """
        self.db_fd, flask_app.app.config['DATABASE'] = tempfile.mkstemp()
        flask_app.app.testing = True
        self.app = flask_app.app.test_client()
        with flask_app.app.app_context():
            flask_app.init_db()


    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flask_app.app.config['DATABASE'])


    def test_root_path_redirect(self):
        """ checks for redirect """
        rv = self.app.get('/')
        assert 'Redirecting...' in rv.data


    def test_start_page_text(self):
        """ checks for start text """
        rv = self.app.get('/key=a')
        assert 'In a galaxy far far away...' in rv.data


    def test_add_entry(self):
        rv = self.app.post('/add', 
            data=dict(
                key='aa',
                parent='a',
                pos='a',
                text='test message'
                ), 
            follow_redirects=True)
        out, err = self.capsys.readouterr()
        assert b'In a galaxy far far away...' in rv.data
        assert b"<a href='/key=aa'>test message</a>" in rv.data


    def test_add_empty_entry(self):
        rv = self.app.post('/add', 
            data=dict(
                key='aa',
                parent='a',
                pos='a',
                text=''
                ), 
            follow_redirects=True)
        out, err = self.capsys.readouterr()
        assert b'In a galaxy far far away...' in rv.data
        assert b"<a href='/key=aa'></a>" not in rv.data
        assert b"Empty text field, entry not added." in err


    def test_restart_story(self):
        self.test_add_entry()
        rv = self.app.get('/restart')
        assert b"<a href='/key=aa'>test message</a>" not in rv.data


    def test_400(self):
        """ checks for redirect """
        rv = self.app.post('/add', 
            data=dict(), 
            follow_redirects=True)
        assert 'unexpected' in rv.data


    def test_404(self):
        """ checks for redirect """
        rv = self.app.get('/foo')
        assert 'File Not Found' in rv.data


if __name__ == "__main__":
    unittest.main()
