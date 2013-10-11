"""
Reservation finder

Along with this file, you'll find two files named units.csv and reservations.csv with fields in the following format

location_id, unit_size
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

def parse_date(date_as_string):
    #date_as_string must be formatted like "10/9/2013" (month, day, year)
    # split_tokens = date_as_string.split("/")
    # date = datetime.date(int(split_tokens[2]), int(split_tokens[0]), int(split_tokens[1]))
    return datetime.datetime.strptime(date_as_string, "%m/%d/%Y")

def parse_one_record(line):
    """Take a line from reservations.csv and return a dictionary representing that record. (hint: use the datetime type when parsing the start and end date columns)"""
    # number of people, start date, end date
    d = {}
    tokens = line.split(", ")
    d["Unit ID"] = tokens[0]
    d["Start Date"] = parse_date(tokens[1])
    d["End Date"] = parse_date(tokens[2])
    return d

def read_units():
    """Read in the file units.csv and returns a list of all known units."""
    #units.csv is unit ID, unit capacity
    f = open("units.csv")
    lines = f.readlines()
    f.close()

    unit_ids = []

    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")
        unit_data = lines[i].split(", ")
        unit_ids.append( (int(unit_data[0]), int(unit_data[1])) )
    
    return unit_ids

def read_existing_reservations():
    """Reads in the file reservations.csv and returns a list of reservations."""
    f = open("reservations.csv")
    lines = f.readlines()
    f.close()

    list_of_tuples = []

    for i in range(len(lines)):
        splt = lines[i].split(", ")
        list_of_tuples.append( (int(splt[0]), parse_date(splt[1]), parse_date(splt[2].strip("\n"))) )

    return list_of_tuples

def available(units, reservations, start_date, occupants, stay_length):

    #check if existing reservation during that time for the units that can take that many people

    #units is a list of tuples (id, occupancy), reservations is a list (id, start, end)
    can_hold_occupants = []

    for unit in units:
        if int(occupants) <= unit[1]:
            can_hold_occupants.append(unit)

    date_start = parse_date(start_date)
    end_date = date_start + datetime.timedelta(days=int(stay_length))

    avail_units = []

    print can_hold_occupants

    for unit in can_hold_occupants:
        for rezo in reservations:
            if unit[0] == rezo[0]:
                if date_start < rezo[1] and end_date <= rezo[1]:
                    print "okay"
                    avail_units.append(unit)
                elif date_start >= rezo[1]:
                    print "also okay"
                    avail_units.append(unit)
                else:
                    print "not okay"


    for unit in avail_units:
        print "Unit %d (Size %d) is available" % (unit[0], unit[1])

def reserve(units, reservations, unit_id, start_date, stay_length):
    print "Successfully reserved"

def main():
    units = read_units()
    reservations = read_existing_reservations()  

    while True:
        command = raw_input("SeaBnb> ")
        cmd = command.split()
        if cmd[0] == "available":
            # look up python variable arguments for explanation of the *
            available(units, reservations, *cmd[1:])
        elif cmd[0] == "reserve":
            reserve(units, reservations, *cmd[1:])
        elif cmd[0] == "quit":
            sys.exit(0)
        else:
            print "Unknown command"

if __name__ == "__main__":
    main()
