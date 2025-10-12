"""
Command-line interface for AI credit usage analysis.
"""

import sys
from datetime import datetime

from aicheck.core import calculate_progress, ordinal_suffix


# ANSI color codes
class Colors:
    GREEN = '\033[92m'  # Light green
    RED = '\033[91m'  # Light red
    YELLOW = '\033[93m'  # Yellow
    RESET = '\033[0m'  # Reset to default
    BOLD = '\033[1m'


def main():
    """Main entry point for the CLI."""
    if len(sys.argv) < 2:
        print('Usage: aicheck <target_day> <percentage>')
        print('   or: aicheck <percentage>')
        print('Example: aicheck 15 25')
        print('Example: aicheck 25')
        sys.exit(1)

    target_day = 1
    percentage = None

    # Parse arguments - flexible order
    if len(sys.argv) == 2:
        # Single argument: treat as percentage, use default target_day
        try:
            percentage = float(sys.argv[1])
        except ValueError:
            print(f"Error: '{sys.argv[1]}' is not a valid percentage")
            sys.exit(1)
    elif len(sys.argv) >= 3:
        # Two arguments: determine which is which
        # If first arg is <= 31 and second is a larger number, assume day then percentage
        # Otherwise, assume percentage then day (old format)
        try:
            arg1 = float(sys.argv[1])
            arg2 = float(sys.argv[2])

            # Smart detection: if first arg is 1-31 and second is larger, it's likely day then percentage
            if 1 <= arg1 <= 31 and arg2 > 31:
                target_day = int(arg1)
                percentage = arg2
            # If first arg is > 31, it's definitely percentage first
            elif arg1 > 31:
                percentage = arg1
                target_day = int(arg2)
            # If both are <= 31, prefer day first (new format)
            else:
                target_day = int(arg1)
                percentage = arg2

        except ValueError as e:
            print(f'Error: Invalid arguments - {e}')
            sys.exit(1)

    if percentage is None:
        print('Error: Could not determine percentage')
        sys.exit(1)

    result = calculate_progress(percentage, target_day=target_day)

    print('\n💳 Credit Usage Analysis')
    print(f'{"=" * 50}')
    print(f'Current Date: {datetime.now().strftime("%Y-%m-%d")}')
    print(f'Billing Cycle: Day {result["days_since_renewal"]} of {result["days_in_billing_cycle"]}')
    print(f'Renewal Day: {ordinal_suffix(result["target_day"])} of the month')
    print('\n🎯 Analysis:')
    print(f'  Credits Used: {result["current_percentage"]:.1f}%')

    # Color-code the difference based on good/bad
    diff_color = Colors.GREEN if result['ratio'] < 1 else Colors.RED if result['ratio'] > 1 else Colors.YELLOW
    print(f'  Difference: {diff_color}{result["difference_percentage"]:+.1f}%{Colors.RESET}')

    # Color-code the status
    status_color = Colors.GREEN if result['ratio'] < 1 else Colors.RED if result['ratio'] > 1 else Colors.YELLOW
    print(f'  Status: {status_color}{result["status"].upper()}{Colors.RESET}')

    print('\n🔮 Projection (at current rate):')
    print(f'  Expected usage by renewal: {result["projected_usage"]:.1f}%')

    # Color-code the remaining credits
    remaining_color = Colors.GREEN if result['projected_remaining'] > 0 else Colors.RED
    print(f'  Expected surplus: {remaining_color}{result["projected_remaining"]:.1f}%{Colors.RESET}')

    if result['ratio'] > 1:
        print(
            f"\n{Colors.RED}⚠️  WARNING: You're using credits {result['difference_percentage']:.1f}% "
            f'faster than time!{Colors.RESET}'
        )
        if result['projected_remaining'] < 0:
            print(
                f"   {Colors.RED}💥 You'll exceed 100% usage by {abs(result['projected_remaining']):.1f}% "
                f'before renewal!{Colors.RESET}'
            )
        else:
            print(
                f'   {Colors.RED}At this rate, you may run out before renewal day {result["target_day"]}{Colors.RESET}'
            )
    elif result['ratio'] < 1:
        print(
            f"\n{Colors.GREEN}✅ Great! You're conserving credits - using {abs(result['difference_percentage']):.1f}% "
            f'slower than time{Colors.RESET}'
        )
        print(
            f"   {Colors.GREEN}You'll have ~{result['projected_remaining']:.1f}% "
            f'credits remaining at renewal.{Colors.RESET}'
        )
    else:
        print(f"\n{Colors.YELLOW}✓ Perfect! You're using credits at exactly the expected rate.{Colors.RESET}")
        print(f"   {Colors.YELLOW}You'll use exactly 100% by day {result['target_day']}.{Colors.RESET}")

    print()


if __name__ == '__main__':
    main()
