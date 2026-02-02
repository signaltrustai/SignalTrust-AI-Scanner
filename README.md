# SignalTrust-AI-Scanner

## Lunch App

A simple command-line application for managing lunch options and getting meal recommendations.

### Features

- 🍽️ View a full menu of lunch options
- 🎲 Get random lunch recommendations
- 🥗 Filter by category (Salad, Sandwich, Burger, Pizza, Asian)
- 📊 Filter by calories and price constraints
- 💰 See prices and nutritional information

### Installation

No external dependencies required! Just Python 3.6 or higher.

```bash
# Clone the repository
git clone https://github.com/signaltrustai/SignalTrust-AI-Scanner.git
cd SignalTrust-AI-Scanner

# Make the script executable (optional)
chmod +x lunch_app.py
```

### Usage

**Display the full menu:**
```bash
python lunch_app.py --menu
```

**Get a random recommendation:**
```bash
python lunch_app.py --recommend
```

**Get a recommendation with calorie constraint:**
```bash
python lunch_app.py --recommend --max-calories 400
```

**Get a recommendation with price constraint:**
```bash
python lunch_app.py --recommend --max-price 10.00
```

**Get a recommendation with both constraints:**
```bash
python lunch_app.py --recommend --max-calories 400 --max-price 10.00
```

**View items by category:**
```bash
python lunch_app.py --category Salad
```

### Testing

Run the test suite to verify functionality:

```bash
python -m unittest test_lunch_app.py
```

Or run with verbose output:

```bash
python -m unittest test_lunch_app.py -v
```

### Examples

```bash
# Show me everything!
$ python lunch_app.py --menu

# I'm on a diet, what should I eat?
$ python lunch_app.py --recommend --max-calories 400

# I only have $10, give me a suggestion
$ python lunch_app.py --recommend --max-price 10.00

# Show me all the salads
$ python lunch_app.py --category Salad
```

### Development

This is part of the SignalTrust-AI-Scanner project. Future enhancements may include:
- AI-powered recommendations based on preferences
- Nutritional analysis and health scoring
- Integration with restaurant APIs
- User preference learning

### License

MIT License

