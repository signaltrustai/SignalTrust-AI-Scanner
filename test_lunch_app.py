#!/usr/bin/env python3
"""
Tests for the Lunch App
"""

import unittest
from lunch_app import LunchApp


class TestLunchApp(unittest.TestCase):
    """Test cases for the LunchApp class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = LunchApp()
    
    def test_initialization(self):
        """Test that the app initializes with menu items."""
        self.assertIsNotNone(self.app.menu_items)
        self.assertGreater(len(self.app.menu_items), 0)
    
    def test_get_all_items(self):
        """Test getting all menu items."""
        items = self.app.get_all_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), len(self.app.menu_items))
    
    def test_get_recommendation_no_constraints(self):
        """Test getting a recommendation without constraints."""
        recommendation = self.app.get_recommendation()
        self.assertIsNotNone(recommendation)
        self.assertIn("name", recommendation)
        self.assertIn("category", recommendation)
        self.assertIn("calories", recommendation)
        self.assertIn("price", recommendation)
    
    def test_get_recommendation_with_calorie_constraint(self):
        """Test getting a recommendation with calorie constraint."""
        recommendation = self.app.get_recommendation(max_calories=400)
        self.assertIsNotNone(recommendation)
        self.assertLessEqual(recommendation["calories"], 400)
    
    def test_get_recommendation_with_price_constraint(self):
        """Test getting a recommendation with price constraint."""
        recommendation = self.app.get_recommendation(max_price=10.0)
        self.assertIsNotNone(recommendation)
        self.assertLessEqual(recommendation["price"], 10.0)
    
    def test_get_recommendation_with_both_constraints(self):
        """Test getting a recommendation with both constraints."""
        recommendation = self.app.get_recommendation(max_calories=400, max_price=10.0)
        if recommendation:  # May be None if no items match
            self.assertLessEqual(recommendation["calories"], 400)
            self.assertLessEqual(recommendation["price"], 10.0)
    
    def test_get_recommendation_impossible_constraints(self):
        """Test getting a recommendation with impossible constraints."""
        recommendation = self.app.get_recommendation(max_calories=1, max_price=0.01)
        self.assertIsNone(recommendation)
    
    def test_get_items_by_category(self):
        """Test filtering items by category."""
        salads = self.app.get_items_by_category("Salad")
        self.assertIsInstance(salads, list)
        for item in salads:
            self.assertEqual(item["category"], "Salad")
    
    def test_get_items_by_category_case_insensitive(self):
        """Test that category filtering is case-insensitive."""
        salads_lower = self.app.get_items_by_category("salad")
        salads_upper = self.app.get_items_by_category("SALAD")
        self.assertEqual(len(salads_lower), len(salads_upper))
    
    def test_get_items_by_nonexistent_category(self):
        """Test filtering by a non-existent category."""
        items = self.app.get_items_by_category("NonExistent")
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)
    
    def test_menu_item_structure(self):
        """Test that all menu items have required fields."""
        required_fields = ["name", "category", "calories", "price"]
        for item in self.app.menu_items:
            for field in required_fields:
                self.assertIn(field, item)
            self.assertIsInstance(item["name"], str)
            self.assertIsInstance(item["category"], str)
            self.assertIsInstance(item["calories"], int)
            self.assertIsInstance(item["price"], float)


if __name__ == "__main__":
    unittest.main()
