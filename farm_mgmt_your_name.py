# ============== TE WAIHORA FARM MANAGEMENT SYSTEM ==============
# Student Name: 
# Student ID : 
# ================================================================
 
from datetime import datetime,timedelta     # datetime module is required for working with dates

import farm_data    # Makes the variables and function in farm_data.py available in this code


# Global variable values that can be referred to throughout your code.  
current_date = datetime(2024,8,26)
# Do not change these values:
pasture_growth_rate = 65    #kg DM/ha/day
stock_growth_rate = 0.7     #kg per day
stock_consumption_rate = 14 #kg DM/animal/day
earliest_birth_date = "1/06/2022"
weight_range = (250,700)

# Collection variables from farm_data.py are available in this code (renamed here to remove the 'farm_data.' prefix).
mobs = farm_data.mobs
paddocks = farm_data.paddocks
stock = farm_data.stock

# Functions from farm_data.py are available in this code (renamed here to remove the 'farm_data.' prefix).
next_id = farm_data.next_id
display_formatted_row = farm_data.display_formatted_row
pasture_levels = farm_data.pasture_levels


def list_all_stock():
    """
    Lists stock details (except birth date).
    This is an example of how to produce basic output."""
    format_str = "{: <5} {: <7} {: <5} {: <5}"            # Use the same format_str for column headers and rows to ensure consistent spacing. 
    display_formatted_row(["ID","Mob","Age","Weight"],format_str)     # Use the display_formatted_row() function to display the column headers with consistent spacing
    for animal in stock:
        id = animal[0]
        mob = animal[1]
        age = animal[3]
        weight = animal[4]
        display_formatted_row([id,mob,age,weight],format_str)     # Use the display_formatted_row() function to display each row with consistent spacing
    input("\nPress Enter to continue.")

def list_stock_by_mob():
    """
    Lists stock details (including birth date), grouped by mob name.
    """
    for mob, animals in mobs.items():
        mob_name = mob
        print(f'\n{mob_name}:')  # Display the mob name as a heading
        format_str = "{: <5} {: <7} {: <5} {: <5} {: <12}"  # Use the same format_str for column headers and rows to ensure consistent spacing.
        display_formatted_row(["ID", "Mob", "Age", "Weight", "Birth Date"], format_str)  # Use the display_formatted_row() function to display the column headers with consistent spacing
        for animal in stock:
            if animal[1] == mob_name and animal[0] in animals:
                id = animal[0]
                age = animal[3]
                weight = animal[4]
                birth_date = animal[2].strftime("%d %B %Y")  # Convert birth date to human readable format
                display_formatted_row([id, mob_name, age, weight, birth_date], format_str)  # Use the display_formatted_row() function to display each row with consistent spacing
    input("\nPress Enter to continue.")

def list_paddock_details():
    """
    List the paddock names and all details."""

    format_str = "{: <10} {: <10} {: <10} {: <10} {: <10} {: <10}"  # Use the same format_str for column headers and rows to ensure consistent spacing.
    display_formatted_row(["Name", "Area (ha)", "Mob", "Stock", "Total DM", "DM/ha"], format_str)  # Use the display_formatted_row() function to display the column headers with consistent spacing
    sorted_paddocks = sorted(paddocks.items(), key=lambda x: x[0])  # Sort the paddocks dictionary by name in alphabetical order
    for paddock_name, paddock_details in sorted_paddocks:
        area = paddock_details['area']
        stock_num = paddock_details['stock num']
        mob = paddock_details['mob']
        total_dm = paddock_details['total dm']
        dm_per_ha = paddock_details['dm/ha']
        display_formatted_row([paddock_name, area, mob, stock_num, total_dm, dm_per_ha], format_str)  # Use the display_formatted_row() function to display each row with consistent spacing
    input("\nPress Enter to continue.")

def move_mobs_between_paddocks(mob, paddock):
    """
    Change which paddock each mob is in. """

    if mob not in mobs:
        print("Invalid mob name.")
        return
    if paddock not in paddocks:
        print("Invalid paddock name.")
        return
    if mobs == paddocks[paddock]['mob']:
        print("The mob is already in the specified paddock.")
        return
    if paddocks[paddock]['stock num'] > 0:
        print("Destination paddock is not empty.")
        return
    
    # Get Paddock Name of the mob
    for paddock_name, paddock_details in paddocks.items():
        if paddock_details['mob'] == mob:
            current_paddock = paddock_name
            break
    
    # Move the mob to the new paddock
    paddocks[paddock]['mob'] = mob
    paddocks[paddock]['stock num'] = len(mobs[mob])

    # Remove the mob from the current paddock
    paddocks[current_paddock]['mob'] = None
    paddocks[current_paddock]['stock num'] = 0
    
    print("Mob successfully moved to the new paddock.")
    input("\nPress Enter to continue.")

def add_new_stock(stock):
    """
    Add a new animal to the stock list."""

    while True:
        new_id = next_id(stock) # Get the next available ID

        # Get the mob name, birth date, age, and weight from the user
        mob = input("Enter the mob name: ")
        if mob not in mobs:
            print("Invalid mob name.")
            continue

        birth_date = input("Enter the birth date (dd/mm/yyyy): ")
        birth_date = datetime.strptime(birth_date, "%d/%m/%Y")
        if birth_date < datetime.strptime(earliest_birth_date, "%d/%m/%Y"):
            print("Invalid birth date. Please enter a date no earlier than", earliest_birth_date)
            continue

        age = current_date.year - birth_date.year
        if current_date < birth_date.replace(year=current_date.year):
            age -= 1
        
        weight = float(input("Enter the weight in kg: "))
        if weight < weight_range[0] or weight > weight_range[1]:
            print("Invalid weight. Please enter a weight between", weight_range[0], "and", weight_range[1])
            continue

        # Add the new stock to the stock list
        stock.append([new_id, mob, birth_date, age, weight])
        # Add the new stock to the mob list
        mobs[mob].append(new_id)
        # Update the stock number in the paddock
        for paddock_name, paddock_details in paddocks.items():
            if paddock_details['mob'] == mob:
                paddock_details['stock num'] += 1
                break
        print("New stock successfully added.")
        response = input("Enter 'Y' to add another stock or any other key to return to the main menu: ")
        if response.upper() != "Y":
            break

    print("New stock successfully added.")
    input("\nPress Enter to continue.")
    
def move_to_next_day(stock, paddocks):
    """
    Increase the current date by one day, making other required changes.
    """
    # Use the function in the line below to return 'total dm' and 'dm/ha' values for each paddock:  
    #     pasture_levels(area,stock,total_dm,pasture_growth_rate,stock_consumption_rate)  
    
    global current_date  # Add this line to define current_date as a global variable
    
    # Increase the current date by one day
    current_date += timedelta(days=1)

    # Update the age of each animal by one day
    for animal in stock:
        animal[3] += 1
    
    # Update pasture levels for each paddock
    for paddock_name, paddock_details in paddocks.items():
        area = paddock_details['area']
        stock_num = paddock_details['stock num']
        updated_pasture_levels = pasture_levels(area, stock_num, paddock_details['total dm'], pasture_growth_rate, stock_consumption_rate)
        paddock_details['total dm'] = updated_pasture_levels['total dm']
        paddock_details['dm/ha'] = updated_pasture_levels['dm/ha']

    print("Day successfully moved to the next day.")
    input("\nPress Enter to continue.")
    


def disp_menu():
    """
    Displays the menu and current date.  No parameters required.
    """
    print("==== WELCOME TE WAIHORA FARM MANAGEMENT SYSTEM ===")
    print("Today is", current_date.strftime("%d/%m/%Y"))
    print(" 1 - List All Stock")
    print(" 2 - List Stock Grouped by Mob")
    print(" 3 - List Paddock Details")
    print(" 4 - Move Mobs Between Paddocks")
    print(" 5 - Add New Stock")
    print(" 6 - Move to Next Day")
    print(" X - eXit (stops the program)")


# ------------ This is the main program ------------------------


# Don't change the menu numbering or function names in this menu.
# Although you can add arguments to the function calls, if you wish.
# Repeat this loop until the user enters an "X" or "x"
response = ""
while response.upper() != "X":
    disp_menu()
    # Display menu for the first time, and ask for response
    response = input("Please enter menu choice: ")    
    if response == "1":
        list_all_stock()
    elif response == "2":
        list_stock_by_mob()
    elif response == "3":
        move_mobs_between_paddocks(paddocks)
    elif response == "4":
        mob = input("Enter the mob: ")
        paddock = input("Enter the paddock: ")
        move_mobs_between_paddocks(mob, paddock)
    elif response == "5":
        add_new_stock(stock)
    elif response == "6":
        move_to_next_day(stock,paddocks)
    elif response.upper() != "X":
        print("\n*** Invalid response, please try again (enter 1-6 or X)")

    print("")

print("\n=== Thank you for using Te Waihora Farm Management System! ===\n")

