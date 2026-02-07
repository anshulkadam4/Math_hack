import sqlite3
import csv
from datetime import datetime


def export_to_csv():
    """Export all grievances to CSV file"""
    conn = sqlite3.connect("freshmankit.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM grievances")
    grievances = cursor.fetchall()

    if not grievances:
        print("No grievances to export!")
        return

    # Create CSV file
    filename = f"grievances_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Header
        writer.writerow(
            [
                "Ticket ID",
                "User ID",
                "Username",
                "Category",
                "Description",
                "Timestamp",
                "Status",
            ]
        )

        # Data
        writer.writerows(grievances)

    print(f"✅ Exported {len(grievances)} grievances to {filename}")
    conn.close()


if __name__ == "__main__":
    export_to_csv()
