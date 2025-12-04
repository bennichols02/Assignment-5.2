from blogging.controller import Controller
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.cli.editing_blog_menu_cli import EditingBlogMenuCLI

class MainMenuCLI():

    def __init__(self, controller):
        self.controller = controller
        self.editing_blog_menu_cli = EditingBlogMenuCLI(self.controller)


    def main_menu(self):
        while True:
            self.print_main_menu()
            try:
                response = int(input('\nChoose your option: '))
            except ValueError:
                print('Please enter an integer number.')
                input('Type ENTER to continue.')
                continue
            if response == 1:
                self.create_blog()
                input('Type ENTER to continue.')
            elif response == 2:
                self.search_blog()
                input('Type ENTER to continue.')
            elif response == 3:
                self.retrieve_blogs_by_name()
                input('Type ENTER to continue.')
            elif response == 4:
                self.update_blog()
                input('Type ENTER to continue.')
            elif response == 5:
                self.delete_blog()
                input('Type ENTER to continue.')
            elif response == 6:
                self.list_all_blogs()
                input('Type ENTER to continue.')
            elif response == 7:
                self.start_editing_blog()
                input('Type ENTER to continue.')
            elif response == 8:
                if self.logout():
                    print('\nLOGGED OUT.')
                    input('Type ENTER to continue.')
                    break
            else:
                print('\nWRONG CHOICE. Please pick a choice between 1 and 8.')
                input('Type ENTER to continue.')
        return

    def print_main_menu(self):
        print('\n\nBLOGGING SYSTEM - MAIN MENU\n\n')
        print('1 - Add new blog')
        print('2 - Search blog by ID')
        print('3 - Retrieve blogs by name')
        print('4 - Change blog data')
        print('5 - Remove blog')
        print('6 - List all blogs')
        print('7 - Edit blog')
        print('8 - Log out')

    def create_blog(self):
        print('ADD NEW BLOG:')
        try:
            id = int(input('Enter the Blog ID: '))
            name = input('Blog name: ')
            url = input('Blog URL: ')
            email = input('Blog Email: ')
            self.controller.create_blog(id, name, url, email)
            print('\nBLOG ADDED TO THE SYSTEM.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except IllegalOperationException:
            print('\nERROR ADDING NEW BLOG.') 
            print('There is a blog already registered with ID %d.' % id)

    def search_blog(self):
        print('SEARCH BLOG:')
        try:
            id = int(input('Enter the Blog ID: '))
            blog = self.controller.search_blog(id)
            if blog:
                self.print_blog_data(blog)
            else:
                print('\nThere is no blog registered with this ID.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')

    # helper method to print blog data
    def print_blog_data(self, blog):
        print('\nBLOG:')
        print('ID: %d' % blog.id)
        print('Name: %s' % blog.name)
        print('URL: %s' % blog.url)
        print('Email: %s' % blog.email)
        print()

    def retrieve_blogs_by_name(self):
        print('RETRIEVE BLOGS BY NAME:')
        try:
            search_string = input('Search for: ')
            found_blogs = self.controller.retrieve_blogs(search_string)
            if found_blogs:
                print('\nBlogs found with name %s:\n' % search_string)
                for blog in found_blogs:
                    print(blog)
            else:
                print('\nNo blogs found with name: %s\n' % search_string)
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')


    def update_blog(self):
        print('CHANGE BLOG DATA:')
        try:
            original_id = int(input('Enter the Blog ID: '))
            blog = self.controller.search_blog(original_id)
            if blog:
                self.print_blog_data(blog)
                print('Type the new data value or enter for each field that should keep the old data: ')
                id = input('Blog ID: ')
                name = input('Blog name: ')
                url = input('Blog URL: ')
                email = input('Blog Email: ')

                # update only fields that were not empty
                id = int(id) if id !='' else blog.id
                name = name if name !='' else blog.name
                url = url if url !='' else blog.url
                email = email if email !='' else blog.email

                confirm = input('\nAre you sure you want to change blog data %s (y/n)? ' % blog.name)
                if confirm.lower() == 'y':
                    self.controller.update_blog(original_id, id, name, url, email)
                    print('\nBLOG DATA CHANGED.')
            else:
                print('\nERROR CHANGING BLOG DATA.')
                print('There is no blog registered with this ID.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except IllegalOperationException:
            print('\nERROR CHANGING BLOG DATA.')
            if self.controller.current_blog:
                if self.controller.current_blog.id == id:
                    print('Cannot change the current blog data. Finish blog editing first.')
            else:
                print('Cannot change blog data to a new ID that is already registered in the system.')


    def delete_blog(self):
        print('REMOVE BLOG:')
        try:
            id = int(input('Enter the Blog ID: '))
            blog = self.controller.search_blog(id)
            if blog:
                self.print_blog_data(blog)
                confirm = input('\nAre you sure you want to remove blog %s (y/n)? ' % blog.name)
                if confirm.lower() == 'y':
                    self.controller.delete_blog(id)
                    print('\nBLOG REMOVED FROM THE SYSTEM.')
            else:
                print('\nERROR REMOVING BLOG.')
                print('There is no blog registered with this ID.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except IllegalOperationException:
            print('\nERROR REMOVING BLOG.')
            if self.controller.current_blog:
                if self.controller.current_blog.id == id:
                    print('Cannot remove the current blog. Finish blog editing first.')
            else:
                print('Cannot remove a blog that is not registered in the system.')

    def list_all_blogs(self):
        print('LIST ALL BLOGS:\n')
        try:
            blogs = self.controller.list_blogs()
            if blogs:
                for blog in blogs:
                    print(blog)
            else:
                print('\nNo blogs registered in the system.\n')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')

    def start_editing_blog(self):
        print('START EDITING BLOG:')
        try:
            id = int(input('Enter the Blog ID: '))
            self.controller.set_current_blog(id)
            current_blog = self.controller.get_current_blog()
            self.print_blog_data(current_blog)
            self.editing_blog_menu_cli.editing_blog_menu()
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except IllegalOperationException:
            print('\nERROR STARTING EDITING BLOG.') 
            print('There is no blog registered with ID %d.' % id)

    def logout(self):
        try:
            self.controller.logout()
        except InvalidLogoutException:
            print('\nUSER WAS ALREADY LOGGED OUT.')
            return False
        return True

