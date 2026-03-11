import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from db import get_all_sessions, get_days



def plot_craving_curve(intensity_readings):
    """
    Builds an x axis with minute intervals matching the length of intensity_readings
    Plot x against intensity_readings as a line chart
    Set a title, x and y labels, and call plt.show()
    """

    # Create x axis with minute intervals
    x = list(range(1, len(intensity_readings) + 1))

    # Plot x against intensity_readings as a line chart
    plt.plot(x, intensity_readings, marker='o')

    # Set title and labels
    plt.title('Craving Intensity Over Time')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Craving Intensity')

    # Show the plot
    plt.grid()
    plt.show()



def show_dashboard(user_id):
    """
    Displays dashboard featuring total days and total sessions
    Use rich to create a formatted table with colors and styling
    Color themes include warm colors like orange, brown, red, yellow to feel cozy and inviting
    """

    console = Console()
    sessions = get_all_sessions(user_id)
    days = get_days(user_id)
    table = Table(title="The Hearth Dashboard", style="bold white on red")
    table.add_column("Total Sessions", justify="center", style="bright_white")
    table.add_column("Days showed up", justify="center", style="bold yellow")
    table.add_row(str(len(sessions)), str(days))
    console.print(table)

if __name__ == "__main__":
    show_dashboard(1)