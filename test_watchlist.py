import unittest

#from app import app, db, Movie, User, forge, initdb
from watchlist import app, db
from watchlist.models import User, Movie
from watchlist.commands import forge, initdb

class WatchlistTestCase(unittest.TestCase):
    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )

        #create database
        db.create_all()
        #create one user, one movie
        user = User(name='Test', username='test')
        user.set_password('123')
        movie = Movie(title='Test Movie Title', year='2019')
        #add multiple class
        db.session.add_all([user, movie])
        db.session.commit()

        #works like browser
        self.client = app.test_client()
        #works like cmd
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #test if app exist
    def test_app_exist(self):
        self.assertIsNotNone(app)

    #check if it is in testing mode
    def test_app_is_testing(self):
        #will not output too much error message in testing mode
        self.assertTrue(app.config['TESTING'])

    def test_404_page(self):
        #same as use "get" in browser
        response = self.client.get('/nothing')
        data = response.get_data(as_text=True)
        self.assertIn('Page Not Found - 404', data)
        self.assertIn('Go Back', data)
        self.assertEqual(response.status_code, 404)

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Test\'s Watchlist', data)
        self.assertIn('Test Movie Title', data)
        self.assertEqual(response.status_code, 200)

    #helper function to login..
    def login(self):
        self.client.post('/login', data=dict(username='test', password='123'), follow_redirects=True)

    def test_create_item(self):
        self.login()
        #test create movie
        response = self.client.post('/', data=dict(
            title= 'New Movie',
            year='2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item Created.', data)
        self.assertIn('New Movie', data)


        #case when title is empty
        response = self.client.post('/', data=dict(
            title='',
            year='2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item Created.', data)
        self.assertIn('Invalid Input.', data)

        #case when year is empty
        response = self.client.post('/', data=dict(
            title='New Movie',
            year=''
        ),follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item Created.', data)
        self.assertIn('Invalid Input.', data)



    #test updating the movies
    def test_update_item(self):
        self.login()
        #test update the page
        response = self.client.get('/movie/edit/1')
        data = response.get_data(as_text=True)
        self.assertIn('Edit Item', data)
        self.assertIn('Test Movie Title', data)
        self.assertIn('2019', data)

        #test update movie
        response = self.client.post('/movie/edit/1', data=dict(
            title='New Movie Edited',
            year='2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item Updated.', data)
        self.assertIn('New Movie Edited', data)

        #case when title is empty
        response = self.client.post('/movie/edit/1', data=dict(
            title='',
            year='2019'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item Updated.', data)
        self.assertIn('Invalid Input.', data)

        #case when the year is empty
        response = self.client.post('/movie/edit/1', data=dict(
            title='New Movie Edited Again',
            year=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item Updated.', data)
        self.assertNotIn('New Movie Edited Again', data)
        self.assertIn('Invalid Input.', data)


    #for delete movie operation
    def test_delete_item(self):
        self.login()
        response = self.client.post('/movie/delete/1', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item deleted.', data)
        self.assertNotIn('Test Movie Title', data)



    #test login protection
    def test_login_protect(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)


    #test login
    def test_login(self):
        response = self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Login Success.', data)
        self.assertIn('Logout', data)
        self.assertIn('Settings', data)
        self.assertIn('Delete', data)
        self.assertIn('Edit', data)
        self.assertIn('<form method="post">', data)

        #case: wrong password
        response = self.client.post('/login', data=dict(
            username='test',
            password='456'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login Success.', data)
        self.assertIn('Invalid username or password.', data)

        #case: wrong username
        response = self.client.post('/login', data=dict(
            username='wrong',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid username or password.', data)

        #case: empty username
        response = self.client.post('/login', data=dict(
            username='',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login success.', data)
        self.assertIn('Invalid Input.', data)

        #case: empty password
        response = self.client.post('/login', data=dict(
            username='test',
            password=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login Success.', data)
        self.assertIn('Invalid Input.', data)

    #test logout
    def test_logout(self):
        self.login()
        response = self.client.get('/logout', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Goodbye.',data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Edit', data)
        self.assertNotIn('<form method="post">', data)


    #test settings
    def test_settings(self):
        self.login()

        #test the settings page
        response = self.client.get('/settings')
        data = response.get_data(as_text=True)
        self.assertIn('Settings', data)
        self.assertIn('Your Name', data)

        #case: update settings
        response = self.client.post('/settings', data=dict(
            name='bill bill'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Settings Updated.', data)
        self.assertIn('bill bill', data)

        #case: name is empty
        response = self.client.post('/settings', data=dict(
            name=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Settings Updated.', data)
        self.assertIn('Invalid Input.', data)


    #test the commands
    def test_forge_command(self):
        result = self.runner.invoke(forge)
        self.assertIn('Done.', result.output)
        self.assertNotEqual(Movie.query.count(), 0)

    def test_initdb_command(self):
        result = self.runner.invoke(initdb)
        self.assertIn('Initialized database.', result.output)

    def test_admin_command(self):
        db.drop_all()
        db.create_all()
        result = self.runner.invoke(args=['admin', '--username', 'bill2', '--password', '123'])
        self.assertIn('Creating user...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'bill2')
        self.assertTrue(User.query.first().validate_password('123'))

    def test_admin_command_update(self):
        result = self.runner.invoke(args=['admin', '--username', 'bill3', '--password', '456'])
        self.assertIn('Updating user...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'bill3')
        self.assertTrue(User.query.first().validate_password('456'))

if __name__ == '__main__':
    unittest.main()











