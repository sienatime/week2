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
    return datetime.datetime.strptime(date_as_string, "%m/%d/%Y")

def calculate_end_date(start_date_obj, stay_length):
    return start_date_obj + datetime.timedelta(days=int(stay_length))

def parse_one_record(line):
    """Take a line from reservations.csv and return a dictionary representing that record. (hint: use the datetime type when parsing the start and end date columns)"""
    # number of people, start date, end date
    d = {}
    tokens = line.split(", ")

    d["Unit ID"] = int(tokens[0])
    d["Start Date"] = parse_date(tokens[1])
    d["End Date"] = parse_date(tokens[2].strip("\n"))
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

    dict_list = []

    for i in range(len(lines)):
        dict_list.append( parse_one_record(lines[i]) )

    return dict_list

def available(units, reservations, start_date, occupants, stay_length):
    #check if existing reservation during that time for the units that can take that many people
    #units is a list of tuples (id, occupancy), reservations is a list of dictionaries with keys Unit ID, Start Date, End Date.
    avail_units = []

    for unit in units:
        if int(occupants) <= unit[1]:
            avail_units.append(unit)

    date_start = parse_date(start_date)
    end_date = calculate_end_date(date_start,stay_length)
    
    #if you rule out a unit, you need to then not check it again if there are multiple reservations.
    for i in range(len(avail_units)):
        unit = avail_units[i]
        for rezo in reservations: #rezo is a dictionary with keys Unit ID, Start Date, End Date.
            if unit != "bad unit" and rezo["Unit ID"] == unit[0]:
                if rezo["Start Date"] == date_start:
                    avail_units[i] = "bad unit"
                elif date_start < rezo["Start Date"] and end_date > rezo["Start Date"]:
                    avail_units[i] = "bad unit"
                elif date_start > rezo["Start Date"] and end_date < rezo["End Date"]:
                    avail_units[i] = "bad unit"

    final_units = []

    for unit in avail_units:
        if unit != "bad unit":
            final_units.append(unit)

    return final_units

def reserve(units, reservations, unit_id, start_date, stay_length):
    #Use the 'reservations' variable as your database. Store all the reservations in there, including the ones from the new ones you will create.
    occupants = 1
    for unit in units:
        if unit[0] == int(unit_id):
            occupants = unit[1]

    final_units = available(units, reservations, start_date, occupants, stay_length)

    for unit in final_units:
        if int(unit_id) == unit[0]:
            end_date = calculate_end_date(parse_date(start_date), stay_length)
            str_end_date = end_date.strftime('%m/%d/%Y')
            d = parse_one_record( unit_id + ", " + start_date + ", " + str_end_date)
            reservations.append(d)
            print "Successfully reserved unit %s for %s nights." % (unit_id, stay_length)
            return reservations

    print "Unit %s is unavailable during those dates" % unit_id
    return reservations

def main():
    units = read_units()
    reservations = read_existing_reservations()  

    while True:
        command = raw_input("SeaBnb> ")
        cmd = command.split()
        if cmd[0] == "available":
            # look up python variable arguments for explanation of the *
            final_units = available(units, reservations, *cmd[1:])
            if len(final_units) > 0:
                for unit in final_units:
                    print "Unit %d (Size %d) is available" % (unit[0], unit[1])
            else:
                print "No units matching those parameters available for reservation."
            
        elif cmd[0] == "reserve":
            reservations = reserve(units, reservations, *cmd[1:])
        elif cmd[0] == "quit":
            sys.exit(0)
        else:
            print "Unknown command"

if __name__ == "__main__":
    main()
