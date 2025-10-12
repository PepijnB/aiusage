# AI Usage Summary 💳

A smart command-line tool for tracking AI credit consumption across billing cycles. Designed for AI-powered development tools like Cursor, GitHub Copilot, and other subscription-based AI services.

## 🎯 Why This Matters

Managing AI credits effectively can save you money and frustration:

- **Avoid overages**: Get warned before you hit pay-as-you-go pricing
- **Optimize usage**: Know when you have credits to spare for big projects
- **Track trends**: See if you're conserving or burning through credits
- **Plan ahead**: Project your usage through the end of the billing cycle

## ✨ Features

- 📊 **Real-time Usage Analysis**: Compares your credit usage against time elapsed in billing cycle
- 🎨 **Color-Coded Feedback**: Green for conserving, red for warning, instant visual feedback
- 🔮 **Smart Projections**: Predicts remaining credits at renewal based on current usage rate
- 📅 **Flexible Billing Cycles**: Works with any renewal day of the month
- ⚡ **Zero Dependencies**: Pure Python with no external packages required
- 🧮 **Accurate Calculations**: Handles month boundaries and varying cycle lengths

## 📸 Example Output

When you're conserving credits (good):
```
💳 Credit Usage Analysis
==================================================
Current Date: 2025-10-12
Billing Cycle: Day 18 of 31
Renewal Day: 24th of the month

🎯 Analysis:
  Credits Used: 25.0%
  Difference: -8.1%
  Status: CONSERVING WELL

🔮 Projection (at current rate):
  Expected usage by renewal: 43.1%
  Expected surplus: 56.9%

✅ Great! You're conserving credits - using 8.1% slower than time
   You'll have ~56.9% credits remaining at renewal.
```

When you're using too fast (warning):
```
💳 Credit Usage Analysis
==================================================
Current Date: 2025-10-12
Billing Cycle: Day 18 of 31
Renewal Day: 24th of the month

🎯 Analysis:
  Credits Used: 75.0%
  Difference: +16.9%
  Status: USING TOO FAST

🔮 Projection (at current rate):
  Expected usage by renewal: 129.2%
  Expected surplus: -29.2%

⚠️  WARNING: You're using credits 16.9% faster than time!
   💥 You'll exceed 100% usage by 29.2% before renewal!
```

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/ai-usage-summary.git
cd ai-usage-summary
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Run the script** (no dependencies needed):
```bash
python ai_usage.py <current_usage_percentage>
```

## 📖 Usage

### Basic Usage

If your billing renewal is on the 24th (default):
```bash
python ai_usage.py 45
```

### Custom Renewal Day

If your renewal is on a different day:
```bash
python ai_usage.py 15 45  # Renewal on 15th, 45% used
```

### Finding Your Current Usage

**For Cursor:**
1. Open Cursor Settings
2. Navigate to your subscription/usage page
3. Look for "Usage this billing period" or similar
4. Use the percentage shown

**For GitHub Copilot:**
- Check your GitHub billing page for usage metrics

## 🔧 How It Works

The tool performs three key calculations:

1. **Time Progress**: Calculates how far through your billing cycle you are
   - Example: Day 18 of 31 = 58.1% through cycle

2. **Usage Ratio**: Compares credit usage to time progress
   - Ratio > 1.0 = Using too fast ⚠️
   - Ratio < 1.0 = Conserving well ✅
   - Ratio = 1.0 = On track 📊

3. **Projection**: Estimates final usage based on current rate
   - Daily rate = Current % ÷ Days elapsed
   - Projected = Daily rate × Total cycle days

## 📋 Requirements

- Python 3.10+ (uses modern type hints)
- No external dependencies
- Works on macOS, Linux, and Windows

## 💡 Use Cases

### Scenario 1: Pre-Project Planning
You're at 30% usage with 40% of your cycle remaining. You have credits to spare—perfect time to tackle that AI-intensive refactoring project!

### Scenario 2: Usage Warning
You're at 80% usage with 50% of your cycle remaining. Time to be more selective with AI requests or risk hitting overages.

### Scenario 3: End-of-Cycle Push
You're at 60% usage with only 5 days left. Use those remaining credits before they reset!

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - feel free to use this tool in your own projects!

## 🙏 Acknowledgments

Built for developers who want to maximize their AI tool subscriptions without breaking the bank.

---

**Pro Tip**: Set up a shell alias for quick checks:
```bash
alias aicheck='python /path/to/ai_usage.py'
# Then just run: aicheck 45
``` 