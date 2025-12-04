from unittest import TestCase
from unittest import main
from blogging.blog import Blog
from blogging.post import Post
import datetime
from blogging.configuration import Configuration

class BlogTest(TestCase):
	
	def setUp(self):
		Configuration.autosave = False
		self.blog = Blog(1111112000, "Long Journey", "long_journey", "long.journey@gmail.com")

	def test_eq(self):
		same_blog = Blog(1111112000, "Long Journey", "long_journey", "long.journey@gmail.com")
		different_blog_1 = Blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		different_blog_2 = Blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		different_blog_3 = Blog(1111112000, "Long Trip", "long_journey", "long.journey@gmail.com")
		self.assertTrue(self.blog == self.blog)
		self.assertTrue(self.blog == same_blog)
		self.assertFalse(self.blog == different_blog_1)
		self.assertFalse(self.blog == different_blog_2)
		self.assertFalse(self.blog == different_blog_3)

	def test_str(self):
		same_blog = Blog(1111112000, "Long Journey", "long_journey", "long.journey@gmail.com")
		different_blog_1 = Blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		different_blog_2 = Blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		different_blog_3 = Blog(1111112000, "Long Trip", "long_journey", "long.journey@gmail.com")
		self.assertEqual("1111112000; Long Journey; long_journey; long.journey@gmail.com", str(self.blog))
		self.assertEqual("1111112000; Long Journey; long_journey; long.journey@gmail.com", str(same_blog))
		self.assertEqual("1111114444; Short Journey; short_journey; short.journey@gmail.com", str(different_blog_1))
		self.assertEqual("1111115555; Long Journey; long_journey; long.journey@gmail.com", str(different_blog_2))
		self.assertEqual("1111112000; Long Trip; long_journey; long.journey@gmail.com", str(different_blog_3))
		self.assertEqual(str(same_blog), str(self.blog))
		self.assertNotEqual(str(different_blog_1), str(self.blog))
		self.assertNotEqual(str(different_blog_2), str(self.blog))
		self.assertNotEqual(str(different_blog_3), str(self.blog))

	def test_repr(self):
		same_blog = Blog(1111112000, "Long Journey", "long_journey", "long.journey@gmail.com")
		different_blog_1 = Blog(1111114444, "Short Journey", "short_journey", "short.journey@gmail.com")
		different_blog_2 = Blog(1111115555, "Long Journey", "long_journey", "long.journey@gmail.com")
		different_blog_3 = Blog(1111112000, "Long Trip", "long_journey", "long.journey@gmail.com")
		self.assertEqual("Blog(1111112000, 'Long Journey', 'long_journey', 'long.journey@gmail.com')", repr(self.blog))
		self.assertEqual("Blog(1111112000, 'Long Journey', 'long_journey', 'long.journey@gmail.com')", repr(same_blog))
		self.assertEqual("Blog(1111114444, 'Short Journey', 'short_journey', 'short.journey@gmail.com')", repr(different_blog_1))
		self.assertEqual("Blog(1111115555, 'Long Journey', 'long_journey', 'long.journey@gmail.com')", repr(different_blog_2))
		self.assertEqual("Blog(1111112000, 'Long Trip', 'long_journey', 'long.journey@gmail.com')", repr(different_blog_3))
		self.assertEqual(repr(same_blog), repr(self.blog))
		self.assertNotEqual(repr(different_blog_1), repr(self.blog))
		self.assertNotEqual(repr(different_blog_2), repr(self.blog))
		self.assertNotEqual(repr(different_blog_3), repr(self.blog))

	def test_create_post(self):
		# some posts that may be created
		expected_post_1 = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
		expected_post_2 = Post(2, "Continuing my journey", "Along the way...\nThere were challenges.")
		expected_post_3 = Post(3, "Finishing my journey", "And that was it.\nEnd of story.")

		# add one post
		actual_post = self.blog.create_post("Starting my journey", "Once upon a time\nThere was a kid...")
		self.assertIsNotNone(actual_post, "post 1 was created and is valid")

		# implement __eq__(self, other) in Post to compare posts based on their code and text
		self.assertEqual(expected_post_1, actual_post, "post 1 was created and its data are correct")

		# after creating the post, one should be able to search it
		actual_post = self.blog.search_post(1)
		self.assertIsNotNone(actual_post, "post created and retrieved cannot be null")
		self.assertEqual(expected_post_1, actual_post, "post 1 was created, retrieved and its data are correct")

		# add a second post
		actual_post = self.blog.create_post("Continuing my journey", "Along the way...\nThere were challenges.")
		self.assertIsNotNone(actual_post, "post 2 was created and is valid")
		self.assertEqual(expected_post_2, actual_post, "post 2 was created and its data are correct")

		# after creating the post, one should be able to search it
		actual_post = self.blog.search_post(2)
		self.assertIsNotNone(actual_post, "post created and retrieved cannot be null")
		self.assertEqual(expected_post_2, actual_post, "post 2 was created, retrieved and its data are correct")

		# add a third post
		actual_post = self.blog.create_post("Finishing my journey", "And that was it.\nEnd of story.")
		self.assertIsNotNone(actual_post, "post 3 was created and is valid")
		self.assertEqual(expected_post_3, actual_post, "post 3 was created and its data are correct")

		# after creating the post, one should be able to search it
		actual_post = self.blog.search_post(3)
		self.assertIsNotNone(actual_post, "post created and retrieved cannot be null")
		self.assertEqual(expected_post_3, actual_post, "post 3 was created, retrieved and its data are correct")

		# creating new posts should not affect previous posts
		actual_post = self.blog.search_post(2)
		self.assertIsNotNone(actual_post, "post created and retrieved cannot be null regardless of search order")
		self.assertEqual(expected_post_2, actual_post, "post 2 was created, retrieved and its data are correct regardless of search order")
		actual_post = self.blog.search_post(1)
		self.assertIsNotNone(actual_post, "post created and retrieved cannot be null regardless of search order")
		self.assertEqual(expected_post_1, actual_post, "post 1 was created, retrieved and its data are correct regardless of search order")


	def test_retrieve_posts(self):
		# some posts that may be retrieved
		expected_post_1 = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
		expected_post_2 = Post(2, "Second step", "Before one could think,\nA storm stroke.")
		expected_post_3 = Post(3, "Continuing my journey", "Along the way...\nThere were challenges.")
		expected_post_4 = Post(4, "Fourth step", "When less expected,\nAll worked fine.")
		expected_post_5 = Post(5, "Finishing my journey", "And that was it.\nEnd of story.")

		# add some posts
		self.blog.create_post("Starting my journey", "Once upon a time\nThere was a kid...")
		self.blog.create_post("Second step", "Before one could think,\nA storm stroke.")
		self.blog.create_post("Continuing my journey", "Along the way...\nThere were challenges.")
		self.blog.create_post("Fourth step", "When less expected,\nAll worked fine.")
		self.blog.create_post("Finishing my journey", "And that was it.\nEnd of story.")

		# retrieve one post
		retrieved_list = self.blog.retrieve_posts("think")
		self.assertEqual(len(retrieved_list), 1, "retrieved list of posts has size 1")
		actual_post = retrieved_list[0]
		self.assertEqual(actual_post, expected_post_2, "retrieved post in the list is post 2")

		# retrieve three posts
		retrieved_list = self.blog.retrieve_posts("journey")
		self.assertEqual(len(retrieved_list), 3, "retrieved list of posts has size 3")
		self.assertEqual(retrieved_list[0], expected_post_1, "first retrieved post in the list is post 1")
		self.assertEqual(retrieved_list[1], expected_post_3, "second retrieved post in the list is post 3")
		self.assertEqual(retrieved_list[2], expected_post_5, "third retrieved post in the list is post 5")

		# retrieve zero posts
		retrieved_list = self.blog.retrieve_posts("ship")
		self.assertEqual(len(retrieved_list), 0)

	def test_update_post(self):
		# some posts that may be updated
		expected_post_1 = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
		expected_post_2 = Post(2, "Second step", "Before one could think,\nA storm stroke.")
		expected_post_3 = Post(3, "Continuing my journey", "Along the way...\nThere were challenges.")
		expected_post_4 = Post(4, "Fourth step", "When less expected,\nAll worked fine.")
		expected_post_5 = Post(5, "Finishing my journey", "And that was it.\nEnd of story.")

		# try to update a post when there are no posts taken for that blog in the system
		self.assertFalse(self.blog.update_post(3, "Continuing the journey", "Along the way...\nThere were challenges."),
			"cannot update post when there are no posts for that blog in the system")

		# add some posts
		self.blog.create_post("Starting my journey", "Once upon a time\nThere was a kid...")
		self.blog.create_post("Second step", "Before one could think,\nA storm stroke.")
		self.blog.create_post("Continuing my journey", "Along the way...\nThere were challenges.")
		self.blog.create_post("Fourth step", "When less expected,\nAll worked fine.")
		self.blog.create_post("Finishing my journey", "And that was it.\nEnd of story.")

		# update one existing post
		self.assertTrue(self.blog.update_post(3, "Continuing the journey", "Along the way...\nThere were challenges."), 
			"update blog's post")
		actual_post = self.blog.search_post(3)
		self.assertNotEqual(actual_post, expected_post_3, "post has updated data, cannot be equal to the original data")
		expected_post_3a = Post(3, "Continuing the journey", "Along the way...\nThere were challenges.")
		self.assertEqual(actual_post, expected_post_3a, "post was updated, its data has to be updated and correct")
		# notice we have not checked the timestamp. 
		# You should check that manually.
		# some parts of code are not simple to test. How can anyone fix that in general?

		# update another existing post
		self.assertTrue(self.blog.update_post(5, "Finishing my journey", "And that was the way.\nEnd of story."), 
			"update blog's post")
		actual_post = self.blog.search_post(5)
		self.assertNotEqual(actual_post, expected_post_5, "post has updated data, cannot be equal to the original data")
		expected_post_5a = Post(5, "Finishing my journey", "And that was the way.\nEnd of story.")
		self.assertEqual(actual_post, expected_post_5a, "post was updated, its data has to be updated and correct")

	def test_delete_post(self):
		# some posts that may be deleted
		expected_post_1 = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
		expected_post_2 = Post(2, "Second step", "Before one could think,\nA storm stroke.")
		expected_post_3 = Post(3, "Continuing my journey", "Along the way...\nThere were challenges.")
		expected_post_4 = Post(4, "Fourth step", "When less expected,\nAll worked fine.")
		expected_post_5 = Post(5, "Finishing my journey", "And that was it.\nEnd of story.")

		# try to delete a post when there are no posts taken for that blog in the system
		self.assertFalse(self.blog.delete_post(3), "cannot delete post when there are no posts for that blog in the system")

		# add some posts
		actual_post = self.blog.create_post("Starting my journey", "Once upon a time\nThere was a kid...")
		actual_post = self.blog.create_post("Second step", "Before one could think,\nA storm stroke.")
		actual_post = self.blog.create_post("Continuing my journey", "Along the way...\nThere were challenges.")
		actual_post = self.blog.create_post("Fourth step", "When less expected,\nAll worked fine.")
		actual_post = self.blog.create_post("Finishing my journey", "And that was it.\nEnd of story.")

		# delete one existing post
		self.assertTrue(self.blog.delete_post(3), "delete blog's post")
		self.assertIsNone(self.blog.search_post(3))

		# delete the remaining existing posts regardless of deleting order
		self.assertTrue(self.blog.delete_post(1), "delete blog's post")
		self.assertIsNone(self.blog.search_post(1))
		self.assertTrue(self.blog.delete_post(5), "delete blog's post")
		self.assertIsNone(self.blog.search_post(5))
		self.assertTrue(self.blog.delete_post(4), "delete blog's post")
		self.assertIsNone(self.blog.search_post(4))
		self.assertTrue(self.blog.delete_post(2), "delete blog's post")
		self.assertIsNone(self.blog.search_post(2))

	def test_list_posts(self):
		# some posts that may be listed
		expected_post_1 = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
		expected_post_2 = Post(2, "Second step", "Before one could think,\nA storm stroke.")
		expected_post_3 = Post(3, "Continuing my journey", "Along the way...\nThere were challenges.")
		expected_post_4 = Post(4, "Fourth step", "When less expected,\nAll worked fine.")
		expected_post_5 = Post(5, "Finishing my journey", "And that was it.\nEnd of story.")

		# listing posts when the current patient has no posts
		posts_list = self.blog.list_posts()
		self.assertEqual(len(posts_list), 0, "list of posts for patient has size 0")

		# listing posts in a singleton list
		actual_post = self.blog.create_post("Starting my journey", "Once upon a time\nThere was a kid...")
		posts_list = self.blog.list_posts()
		self.assertEqual(len(posts_list), 1, "list of posts for patient has size 1")
		self.assertEqual(posts_list[0], expected_post_1, "first post in the list is post 1")

		# add some more posts
		actual_post = self.blog.create_post("Second step", "Before one could think,\nA storm stroke.")
		actual_post = self.blog.create_post("Continuing my journey", "Along the way...\nThere were challenges.")
		actual_post = self.blog.create_post("Fourth step", "When less expected,\nAll worked fine.")
		actual_post = self.blog.create_post("Finishing my journey", "And that was it.\nEnd of story.")

		# listing posts in a larger list
		posts_list = self.blog.list_posts()
		self.assertEqual(len(posts_list), 5, "list of posts has size 5")
		self.assertEqual(posts_list[0], expected_post_5, "post 5 is the first in the list of posts")
		self.assertEqual(posts_list[1], expected_post_4, "post 4 is the second in the list of posts")
		self.assertEqual(posts_list[2], expected_post_3, "post 3 is the third in the list of posts")
		self.assertEqual(posts_list[3], expected_post_2, "post 2 is the fourth in the list of posts")
		self.assertEqual(posts_list[4], expected_post_1, "post 1 is the fifth in the list of posts")

		# deleting some posts
		self.blog.delete_post(3)
		self.blog.delete_post(1)
		self.blog.delete_post(5)

		# listing posts for a patient with deleted posts
		posts_list = self.blog.list_posts()
		self.assertEqual(len(posts_list), 2, "list of posts has size 2")
		self.assertEqual(posts_list[0], expected_post_4, "post 4 is the first in the list of posts")
		self.assertEqual(posts_list[1], expected_post_2, "post 2 is the second in the list of posts")


if __name__ == '__main__':
	unittest.main()