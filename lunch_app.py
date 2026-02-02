#!/usr/bin/env python3
"""
Lunch App - A simple application for managing lunch options and recommendations.
Part of the SignalTrust-AI-Scanner project.
"""

import random
import argparse
from datetime import datetime
from typing import List, Dict


class LunchApp:
    """Main lunch application class for managing lunch options."""
    
    def __init__(self):
        """Initialize the lunch app with default menu items."""
        self.menu_items = [
            {"name": "Caesar Salad", "category": "Salad", "calories": 350, "price": 8.99},
            {"name": "Grilled Chicken Sandwich", "category": "Sandwich", "calories": 450, "price": 10.99},
            {"name": "Veggie Burger", "category": "Burger", "calories": 380, "price": 9.99},
            {"name": "Margherita Pizza", "category": "Pizza", "calories": 550, "price": 12.99},
            {"name": "Sushi Roll Combo", "category": "Asian", "calories": 420, "price": 14.99},
            {"name": "Greek Salad", "category": "Salad", "calories": 300, "price": 7.99},
            {"name": "Turkey Club", "category": "Sandwich", "calories": 480, "price": 11.99},
            {"name": "Pad Thai", "category": "Asian", "calories": 520, "price": 13.99},
        ]
        
    def get_all_items(self) -> List[Dict]:
        """Return all menu items."""
        return self.menu_items
    
    def get_recommendation(self, max_calories: int = None, max_price: float = None) -> Dict:
        """
        Get a random lunch recommendation based on constraints.
        
        Args:
            max_calories: Maximum calorie limit (optional)
            max_price: Maximum price limit (optional)
            
        Returns:
            A recommended menu item
        """
        filtered_items = self.menu_items
        
        if max_calories:
            filtered_items = [item for item in filtered_items if item["calories"] <= max_calories]
        
        if max_price:
            filtered_items = [item for item in filtered_items if item["price"] <= max_price]
        
        if not filtered_items:
            return None
        
        return random.choice(filtered_items)
    
    def get_items_by_category(self, category: str) -> List[Dict]:
        """
        Get all items in a specific category.
        
        Args:
            category: The category to filter by
            
        Returns:
            List of menu items in the category
        """
        return [item for item in self.menu_items if item["category"].lower() == category.lower()]
    
    def display_menu(self):
        """Display the full menu."""
        print("\n" + "="*60)
        print("LUNCH MENU".center(60))
        print("="*60)
        
        categories = {}
        for item in self.menu_items:
            cat = item["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
        
        for category, items in sorted(categories.items()):
            print(f"\n{category}:")
            print("-" * 60)
            for item in items:
                print(f"  {item['name']:<30} ${item['price']:>6.2f}  {item['calories']} cal")
        
        print("="*60 + "\n")


def main():
    """Main CLI interface for the lunch app."""
    parser = argparse.ArgumentParser(description="Lunch App - Get lunch recommendations and view menu")
    parser.add_argument("--menu", action="store_true", help="Display the full menu")
    parser.add_argument("--recommend", action="store_true", help="Get a random recommendation")
    parser.add_argument("--max-calories", type=int, help="Maximum calories for recommendation")
    parser.add_argument("--max-price", type=float, help="Maximum price for recommendation")
    parser.add_argument("--category", type=str, help="Filter by category")
    
    args = parser.parse_args()
    
    app = LunchApp()
    
    # If no arguments provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # Display menu
    if args.menu:
        app.display_menu()
    
    # Get recommendation
    if args.recommend:
        recommendation = app.get_recommendation(
            max_calories=args.max_calories,
            max_price=args.max_price
        )
        
        if recommendation:
            print("\n🍽️  LUNCH RECOMMENDATION 🍽️")
            print(f"\nToday's recommendation: {recommendation['name']}")
            print(f"Category: {recommendation['category']}")
            print(f"Calories: {recommendation['calories']}")
            print(f"Price: ${recommendation['price']:.2f}")
            print(f"\nEnjoy your meal! 🍴\n")
        else:
            print("\n❌ No items match your criteria. Try adjusting your filters.\n")
    
    # Filter by category
    if args.category:
        items = app.get_items_by_category(args.category)
        if items:
            print(f"\n{args.category} items:")
            for item in items:
                print(f"  - {item['name']} (${item['price']:.2f}, {item['calories']} cal)")
            print()
        else:
            print(f"\n❌ No items found in category: {args.category}\n")


if __name__ == "__main__":
    main()
