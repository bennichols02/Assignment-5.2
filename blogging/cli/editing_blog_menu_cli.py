from blogging.controller import Controller
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException

class EditingBlogMenuCLI():

    def __init__(self, controller):
        self.controller = controller

    def editing_blog_menu(self):
        while True:
            self.print_editing_blog_menu()
            try:
                response = int(input('\nChoose your option: '))
            except ValueError:
                print('Please enter an integer number.')
                input('Type ENTER to continue.')
                continue
            if response == 1:
                self.create_post()
                input('Type ENTER to continue.')
            elif response == 2:
                self.retrieve_posts()
                input('Type ENTER to continue.')
            elif response == 3:
                self.update_post()
                input('Type ENTER to continue.')
            elif response == 4:
                self.delete_post()
                input('Type ENTER to continue.')
            elif response == 5:
                self.list_full_blog_contents()
                input('Type ENTER to continue.')
            elif response == 6:
                self.end_editing_blog()
                print('\nEDITING BLOG FINISHED.')
                break
            else:
                print('\nWRONG CHOICE. Please pick a choice between 1 and 6.')
                input('Type ENTER to continue.')
        return

    def print_editing_blog_menu(self):
        print('\n\nBLOGGING SYSTEM - EDITING BLOG MENU\n\n')
        print('1 - Add post to blog')
        print('2 - Retrieve posts from blog by text')
        print('3 - Change post from blog')
        print('4 - Remove post from blog')
        print('5 - List full blog contents')
        print('6 - Finish editing blog')

    def create_post(self):
        print('ADD POST TO BLOG:')
        try:
            print("Add post title: ")
            title = input()
            print("Add post text: ")
            text = input()
            self.controller.create_post(title, text)
            print('\nPOST ADDED TO THE SYSTEM.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except NoCurrentBlogException:
            print('\nERROR ADDING NEW POST.') 
            print('Cannot add a post without a valid current blog.')

    def retrieve_posts(self):
        print('RETRIEVE POSTS FROM BLOG BY TEXT:')
        try:
            search_string = input('Search for: ')
            found_posts = self.controller.retrieve_posts(search_string)
            if found_posts:
                print('\nPosts found for %s:\n' % search_string)
                for post in found_posts:
                    self.print_post_data(post)
            else:
                print('\nNo posts found for: %s\n' % search_string)
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except NoCurrentBlogException:
            print('\nERROR RETRIEVING POSTS.') 
            print('Cannot retrieve posts without a valid current blog.')

    # helper method to print post data
    def print_post_data(self, post):
        print('Post #%d, created - %s, changed - %s' % (post.code, post.creation_time, post.update_time))
        print('\nTitle: %s\n' % post.title)
        print('%s\n' % post.text)

    def update_post(self):
        print('CHANGE POST FROM BLOG:')
        try:
            code = int(input('Post number: '))
            post = self.controller.search_post(code)
            if post:
                self.print_post_data(post)
                confirm = input('Are you sure you want to change post #%s (y/n)? ' % post.code)
                if confirm.lower() == 'y':
                    print('Type new title for post: ')
                    new_title = input()
                    print('Type new text for post: ')
                    new_text = input()
                    self.controller.update_post(code, new_title, new_text)
            else:
                print('\nERROR CHANGING POST FROM BLOG.')
                print('There is no post registered with this number.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except NoCurrentBlogException:
            print('\nERROR REMOVING POST.') 
            print('Cannot remove a post without a valid current blog.')

    def delete_post(self):
        print('REMOVE POST FROM BLOG:')
        try:
            code = int(input('Post number: '))
            post = self.controller.search_post(code)
            if post:
                self.print_post_data(post)
                confirm = input('Are you sure you want to remove post #%s (y/n)? ' % post.code)
                if confirm.lower() == 'y':
                    self.controller.delete_post(code)
            else:
                print('\nERROR REMOVING POST FROM BLOG.')
                print('There is no post registered with this number.')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except NoCurrentBlogException:
            print('\nERROR REMOVING POST.') 
            print('Cannot remove a post without a valid current blog.')

    def list_full_blog_contents(self):
        print('LIST FULL BLOG CONTENTS:\n')
        try:
            posts = self.controller.list_posts()
            if posts:
                for post in posts:
                    self.print_post_data(post)
            else:
                print('\nBlog is empty.\n')
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
        except NoCurrentBlogException:
            print('\nERROR LISTING BLOG CONTENTS.') 
            print('Cannot list the blog contents without a valid current blog.')

    def end_editing_blog(self):
        try:
            self.controller.unset_current_blog()
        except IllegalAccessException:
            print('\nMUST LOGIN FIRST.')
