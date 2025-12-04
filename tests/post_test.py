from unittest import TestCase
from unittest import main
from blogging.post import Post
import datetime

class PostTest(TestCase):
    
    def setUp(self):
        # Create a fixed timestamp for consistent testing
        self.fixed_time = datetime.datetime(2023, 1, 1, 12, 0, 0)
        self.post = Post(1, "Starting my journey", "Once upon a time\nThere was a kid...")
        # Override timestamps for consistent testing
        self.post.creation_time = self.fixed_time
        self.post.update_time = self.fixed_time

    def create_post_with_fixed_time(self, post_code, post_title, post_text):
        """Helper method to create posts with fixed timestamps"""
        post = Post(post_code, post_title, post_text)
        post.creation_time = self.fixed_time
        post.update_time = self.fixed_time
        return post

    def test_eq(self):
        same_post = self.create_post_with_fixed_time(1, "Starting my journey", "Once upon a time\nThere was a kid...")
        different_post_1 = self.create_post_with_fixed_time(2, "Starting my journey", "Once upon a time\nThere was a kid...")
        different_post_2 = self.create_post_with_fixed_time(1, "Finishing my journey", "Once upon a time\nThere was a kid...")
        different_post_3 = self.create_post_with_fixed_time(1, "Starting my journey", "And that was it.\nEnd of story.")
        
        self.assertTrue(self.post == self.post)
        self.assertTrue(self.post == same_post)
        self.assertFalse(self.post == different_post_1)
        self.assertFalse(self.post == different_post_2)
        self.assertFalse(self.post == different_post_3)

    def test_str(self):
        same_post = self.create_post_with_fixed_time(1, "Starting my journey", "Once upon a time\nThere was a kid...")
        different_post_1 = self.create_post_with_fixed_time(2, "Starting my journey", "Once upon a time\nThere was a kid...")
        different_post_2 = self.create_post_with_fixed_time(1, "Finishing my journey", "Once upon a time\nThere was a kid...")
        different_post_3 = self.create_post_with_fixed_time(1, "Starting my journey", "And that was it.\nEnd of story.")
        
        expected_str = "1; 2023-01-01 12:00:00; 2023-01-01 12:00:00\nStarting my journey\n\nOnce upon a time\nThere was a kid..."
        
        self.assertEqual(expected_str, str(self.post))
        self.assertEqual(expected_str, str(same_post))
        
        # Test different posts have different string representations
        self.assertNotEqual(str(different_post_1), str(self.post))
        self.assertNotEqual(str(different_post_2), str(self.post))
        self.assertNotEqual(str(different_post_3), str(self.post))

    def test_repr(self):
        same_post = self.create_post_with_fixed_time(1, "Starting my journey", "Once upon a time\nThere was a kid...")
        different_post_1 = self.create_post_with_fixed_time(2, "Starting my journey", "Once upon a time\nThere was a kid...")
        different_post_2 = self.create_post_with_fixed_time(1, "Finishing my journey", "Once upon a time\nThere was a kid...")
        different_post_3 = self.create_post_with_fixed_time(1, "Starting my journey", "And that was it.\nEnd of story.")
        
        expected_repr = "Post(1, datetime.datetime(2023, 1, 1, 12, 0), datetime.datetime(2023, 1, 1, 12, 0),\n'Starting my journey',\n\n'Once upon a time\\nThere was a kid...'\n)"
        
        self.assertEqual(expected_repr, repr(self.post))
        self.assertEqual(expected_repr, repr(same_post))
        
        # Test different posts have different repr representations
        self.assertNotEqual(repr(different_post_1), repr(self.post))
        self.assertNotEqual(repr(different_post_2), repr(self.post))
        self.assertNotEqual(repr(different_post_3), repr(self.post))

    def test_update_method(self):
        """Test the update method of Post class"""
        post = self.create_post_with_fixed_time(1, "Original Title", "Original Text")
        
        # Update the post
        post.update("New Title", "New Text")
        
        # Check that content was updated
        self.assertEqual(post.title, "New Title")
        self.assertEqual(post.text, "New Text")
        
        # Check that update_time was changed (should be newer than creation_time)
        self.assertGreater(post.update_time, post.creation_time)

    def test_initial_timestamps(self):
        """Test that creation_time and update_time are equal initially"""
        post = Post(1, "Test", "Content")
        # They should be very close (within 1 second)
        time_diff = abs((post.creation_time - post.update_time).total_seconds())
        self.assertLess(time_diff, 1.0)

    def test_post_attributes(self):
        """Test that Post has the correct attributes"""
        post = Post(5, "Test Title", "Test Content")
        
        self.assertEqual(post.code, 5)
        self.assertEqual(post.title, "Test Title")
        self.assertEqual(post.text, "Test Content")
        self.assertIsInstance(post.creation_time, datetime.datetime)
        self.assertIsInstance(post.update_time, datetime.datetime)

if __name__ == '__main__':
    unittest.main()
