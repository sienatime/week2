"""
Reservation finder

Along with this file, you'll find two files named units.csv and reservations.csv with fields in the following format

units.csv
location_id, unit_size

reservations.csv
location_id, reservation_start_date, reservation_end_date

You will write a simple application that manages a reservation system. It will have two commands, 'available' and 'reserve' with the following behaviors:

available <date> <number of occupants> <length of stay>
This will print all available units that match the criteria. Any unit with capacity equal or greater to the number of occupants will be printed out.

Example:
SeaBnb> available 10/10/2013 2 4
Unit 10 (Size 3) is available
Unit 20 (Size 2) is available

reserve <unit number> <start date> <length of stay>
This creates a record in your reservations that indicates the unit has been reserved. It will print a message indicating its success.

A reservation that ends on any given day may be rebooked for the same evening, ie:
    
    If a reservation ends on 10/10/2013, a different reservation may be made starting on 10/10/2013 as well.

Example:
SeaBnb> reserve 10 10/11/2013 3 
Successfully reserved unit 10 for 3 nights

Reserving a unit must make the unit available for later reservations. Here's a sample session:

SeaBnb> available 10/10/2013 2 4
Unit 10 (Size 3) is available
Unit 20 (Size 2) is available
SeaBnb> reserve 10 10/11/2013 3 
Successfully reserved unit 10 for 3 nights
SeaBnb> available 10/10/2013 2 4
Unit 20 (Size 2) is available
SeaBnb> reserve 10 10/11/2013 3 
Unit 10 is unavailable during those dates
SeaBnb> quit

Notes:
Start first by writing the functions to read in the csv file. These have been stubbed for you. Then write the availability function, then reservation. Test your program at each step (it may be beneficial to write tests in a separate file.) Use the 'reservations' variable as your database. Store all the reservations in there, including the ones from the new ones you will create.

The datetime and timedelta classes will be immensely helpful here, as will the strptime function.
"""

import sys
import datetime

def convert_to_datetime(datestring):
    return datetime.datetime.strptime(datestring, "%m/%d/%Y")

def parse_one_record(line):
    """Take a line from reservations.csv and return a dictionary representing that record. (hint: use the datetime type when parsing the start and end date columns)"""
    return {}

def read_units():
    """Read in the file units.csv and returns a list of all known units."""
    f = open("units.csv")
    lines = f.readlines()
    f.close()

    units = []

    for line in lines:
        tokens = line.split(", ")
        unit_id = int(tokens[0])
        occupancy = int(tokens[1])
        units.append( (unit_id, occupancy) )

    return units

def read_existing_reservations():
    """Reads in the file reservations.csv and returns a list of reservations."""
    f = open("reservations.csv")
    lines = f.readlines()
    f.close()

    rezo_dict = {}

    for line in lines:
        tokens = line.split(", ")

        unit_id = int(tokens[0])
        start_date = convert_to_datetime(tokens[1])
        end_date = convert_to_datetime(tokens[2].strip("\n"))

        # get the list for that unit id if it exists, otherwise return an empty list
        list_of_rezos = rezo_dict.get(unit_id, [])
        list_of_rezos.append( (start_date, end_date) )
        rezo_dict[unit_id] = list_of_rezos

    return rezo_dict

def date_overlap(start_date, end_date, rezo_start, rezo_end):

    if start_date < rezo_start and end_date <= rezo_start:
        return False
    elif start_date >= rezo_end:
        return False

    return True

def check_availablity(unit, reservations, start_date, occupants, stay_length):
    unit_id = int(unit[0])
    occupancy = int(unit[1])
    stay_length = int(stay_length)

    if occupants > occupancy:
        return False
    elif reservations.get(unit_id):
        dates = reservations[unit_id]
        end_date = start_date + datetime.timedelta(days=stay_length)

        for rezo in dates:
            rezo_start = rezo[0]
            rezo_end = rezo[1]

            if date_overlap( start_date, end_date, rezo_start, rezo_end ):
                return False
    
    return True    

def available(units, reservations, start_date, occupants, stay_length):
    # for each unit ID, check:
        # if the room is too small (false)
        # if there is an overlapping reservation for that date (false)
        # if both of those pass, add to list of good units

    available_units = []
    occupants = int(occupants)
    start_date = convert_to_datetime(start_date)
    stay_length = int(stay_length)

    for unit in units:
        if check_availablity(unit, reservations, start_date, occupants, stay_length):
            unit_id = int(unit[0])
            available_units.append(unit_id)

    return available_units

def reserve(units, reservations, unit_id, start_date, stay_length):
    occupants = None
    unit_id = int(unit_id)

    for unit in units:
        if unit[0] == unit_id:
            occupants = unit[1]

    available_units = available(units, reservations, start_date, occupants, stay_length)

    if unit_id in available_units:
        start_date = convert_to_datetime(start_date)
        stay_length = int(stay_length)
        end_date = start_date + datetime.timedelta(days=stay_length)

        list_of_rezos = reservations.get(unit_id, [])
        list_of_rezos.append((start_date, end_date))
        reservations[unit_id] = list_of_rezos
        print "Successfully reserved unit %d for %d nights." % (unit_id, stay_length)
    else:
        print "Unit %d is unavailable for those dates." % unit_id

def main():
    units = read_units()
    reservations = read_existing_reservations()  

    while True:
        command = raw_input("SeaBnb> ")
        cmd = command.split()
        if cmd[0] == "available":
            # look up python variable arguments for explanation of the *
            available_units = available(units, reservations, *cmd[1:])

            if available_units:
                for unit in available_units:
                    print "Unit %d is available." % unit
            else:
                print "No available units."

        elif cmd[0] == "reserve":
            reserve(units, reservations, *cmd[1:])
        elif cmd[0] == "quit":
            sys.exit(0)
        else:
            print "Unknown command"

if __name__ == "__main__":
    main()