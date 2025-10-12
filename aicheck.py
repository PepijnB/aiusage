"""
Calculate credit usage rate compared to time progress through the billing cycle.
Shows if you're using credits faster or slower than expected based on renewal date.
Target day is the 24th of each month (renewal date).
"""

import sys
from datetime import datetime


# ANSI color codes
class Colors:
    GREEN = '\033[92m'  # Light green
    RED = '\033[91m'  # Light red
    YELLOW = '\033[93m'  # Yellow
    RESET = '\033[0m'  # Reset to default
    BOLD = '\033[1m'


def ordinal_suffix(day: int) -> str:
    """
    Return the ordinal suffix for a given day number.

    Args:
        day: The day number (1-31)

    Returns:
        The ordinal suffix string (e.g., "1st", "2nd", "3rd", "24th")
    """
    if 11 <= day <= 13:
        return f'{day}th'

    last_digit = day % 10
    if last_digit == 1:
        return f'{day}st'
    elif last_digit == 2:
        return f'{day}nd'
    elif last_digit == 3:
        return f'{day}rd'
    else:
        return f'{day}th'


def calculate_progress(
    current_percentage: float,
    current_date: datetime | None = None,
    target_day: int = 1,
) -> dict[str, float]:
    """
    Calculate if you're using credits faster or slower than expected.

    Args:
        current_percentage: Your current credit usage percentage (e.g., 25 for 25%)
        current_date: The date to calculate from (defaults to today)
        target_day: The renewal day of the month (defaults to 1)

    Returns:
        Dictionary with progress metrics
    """
    if current_date is None:
        current_date = datetime.now()

    # Convert percentage to decimal
    current_pct = current_percentage / 100

    from datetime import timedelta

    # Get the day of the month (1-31)
    current_day = current_date.day

    # Calculate which billing cycle we're in
    # If current day >= target_day, we're past renewal for this month
    # Otherwise, we're still in the cycle from last month's target_day
    if current_day >= target_day:
        # We're in the period from target_day of this month to target_day of next month
        days_since_renewal = current_day - target_day
        # Calculate when next renewal is
        if current_date.month == 12:
            next_renewal = current_date.replace(year=current_date.year + 1, month=1, day=target_day)
        else:
            next_renewal = current_date.replace(month=current_date.month + 1, day=target_day)
    else:
        # We're in the period from target_day of last month to target_day of this month
        days_since_renewal = current_day + (31 - target_day)  # Approximate, will recalculate properly
        # Calculate last renewal date
        if current_date.month == 1:
            last_renewal = current_date.replace(year=current_date.year - 1, month=12, day=target_day)
        else:
            last_renewal = current_date.replace(month=current_date.month - 1, day=target_day)
        # Calculate next renewal
        next_renewal = current_date.replace(day=target_day)
        # Proper days since renewal
        days_since_renewal = (current_date - last_renewal).days

    # Calculate total days in this billing cycle
    if current_day >= target_day:
        if current_date.month == 1:
            last_renewal = current_date.replace(year=current_date.year - 1, month=12, day=target_day)
        else:
            last_renewal = current_date.replace(month=current_date.month - 1, day=target_day)
    else:
        if current_date.month == 1:
            last_renewal = current_date.replace(year=current_date.year - 1, month=12, day=target_day)
        else:
            last_renewal = current_date.replace(month=current_date.month - 1, day=target_day)

    days_in_billing_cycle = (next_renewal - last_renewal).days

    # Days in the current month (for display purposes)
    if current_date.month == 12:
        next_month = current_date.replace(year=current_date.year + 1, month=1, day=1)
    else:
        next_month = current_date.replace(month=current_date.month + 1, day=1)
    days_in_month = (next_month - timedelta(days=1)).day

    # Calculate time progress (how far through the billing cycle)
    time_progress = days_since_renewal / days_in_billing_cycle

    # Calculate the ratio: actual percentage vs expected percentage
    # Ratio > 1 means using credits faster than time (bad)
    # Ratio < 1 means using credits slower than time (good)
    ratio = current_pct / time_progress if time_progress > 0 else 0

    # Calculate how ahead or behind you are
    expected_pct = time_progress
    difference = current_pct - expected_pct
    difference_pct = difference * 100

    # Project usage at renewal date based on current rate
    # If we're 16 days into a 31-day cycle with 25% used, rate is 25/16 = 1.56% per day
    # At day 31: 1.56 * 31 = 48.4% projected usage
    if days_since_renewal > 0:
        daily_rate = current_percentage / days_since_renewal
        projected_usage = daily_rate * days_in_billing_cycle
        projected_remaining = 100 - projected_usage
    else:
        projected_usage = 0
        projected_remaining = 100

    # Status is inverted: using fewer credits than time = good (conserving)
    return {
        'current_percentage': current_percentage,
        'current_day': current_day,
        'target_day': target_day,
        'days_in_month': days_in_month,
        'days_since_renewal': days_since_renewal,
        'days_in_billing_cycle': days_in_billing_cycle,
        'time_progress': time_progress * 100,
        'expected_percentage': expected_pct * 100,
        'ratio': ratio,
        'difference_percentage': difference_pct,
        'projected_usage': projected_usage,
        'projected_remaining': projected_remaining,
        'status': 'using too fast' if difference > 0 else 'conserving well' if difference < 0 else 'on track',
    }


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print('Usage: python cursor_usage.py <target_day> <percentage>')
        print('   or: python cursor_usage.py <percentage>')
        print('Example: python cursor_usage.py 24 25')
        print('Example: python cursor_usage.py 25')
        sys.exit(1)

    target_day = 24
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
    # print('\n📈 Usage Stats:')
    # print(f'  Credits Used: {result["current_percentage"]:.1f}%')
    # print(f'  Usage if linear per day: {result["expected_percentage"]:.1f}%')
    # print(f"  Time Elapsed: {result['time_progress']:.1f}%")
    print('\n🎯 Analysis:')
    # print(f"  Usage Ratio: {result['ratio']:.2f}")
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
