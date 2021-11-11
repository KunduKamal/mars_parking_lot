
from random import randint
from time import time as now_in_sec

## ================= Define Classes ========================== ##
class ParkingLot:
    # Define attributes
    parking_lot_name = ''
    as_car, as_cy = '', ''
    pc_car, pc_by = '',''

    # bill_data = {"ticket_number": {"oname":value, "tnum":value, "stime":value, 
    # "cph":value, "etime":value, "ploc":value, "tbill":value} }
    bill_data = {}
    int_Ticket = 0
    t_number = 0 
    t_count = 0
    # Define the parkig lot allocation map variable
    ploc_map = [[]]
    p_availability = "empty"
    

    def __init__(self, name, number_of_floor, place_per_floor):
        self.parking_lot_name = name
        # for j in range (rows)  repetedly assign that arry previously genareted infront of it.)
        self.ploc_map = [[0 for i in range(place_per_floor)] for j in range(number_of_floor)]
        

    # Define Methods
    def allocate_area(self, total_s_car, total_s_byc):
        t_area = len(self.ploc_map) * len(self.ploc_map[0])
        # print("row, col", len(self.ploc_map) , "    ", len(self.ploc_map[0])   )
        t_vehicle  = total_s_car + total_s_byc

        # print(f" t_vehicle {t_vehicle}  <=   t_area {t_area}")
        if( t_vehicle <= t_area ):
            self.as_car = total_s_car
            self.as_cy = total_s_byc
        else:
            print("Total nuumber of vehicle is greater than the capacity of the parking lot.")
            print("So, default distribution policy is applied (50/50.")
            self.as_car = t_area / 2
            self.as_cy = t_area / 2


    def set_parking_cost(self, price_car, price_byc):
        self.pc_car = price_car
        self.pc_by  = price_byc


    def collect_bill(self, ticket_number):
        print("Your bill is: ", self.bill_data[ticket_number]['bill'])
        cash_confirm = input("Please enter ok after complete payment.\n")
        self.bill_number[ticket_number]["status"] = cash_confirm


    def gen_bill(self, ticket_number, coupon=0):
        t_info = self.bill_data[ticket_number]
        e_time = now_in_sec()
        t_duration = e_time - t_info['stime']
        bill_cost = int( t_info['cph'] * t_duration * (1 - (coupon%100) / 100) )
        self.bill_data[ticket_number]['etime'] = e_time
        self.bill_data[ticket_number]['tdur']= t_duration
        self.bill_data[ticket_number]['bill'] = bill_cost
  

    def close_ticket(self, ticket_num):
        (r, c) = self.bill_data[ticket_num]['flock']
        self.ploc_map[r][c] = 0     # Set the location free, remove marker
        self.bill_data[ticket_num]['flock'] = [None]


    def gen_ticket(self, vehicle_owner_name,cost_unit ):
        # self.bill_data[]
        # Generate a random number for ticket number
        r_ticket_num = str( randint(1000,9999) )
        self.bill_data[r_ticket_num] = {} 
        self.bill_data[r_ticket_num]['oname'] = vehicle_owner_name
        self.bill_data[r_ticket_num]['tnum']  = r_ticket_num
        self.bill_data[r_ticket_num]['stime']  = int( now_in_sec() )
        self.bill_data[r_ticket_num]['cph'] = cost_unit

        ploc = []
        # Get available location for parking
        for row in range(len(self.ploc_map)):
            for col in range(len(self.ploc_map[row])):
                if self.ploc_map[row][col] == 0:
                    ploc = [row, col]
                    # print(f"[Debug]row {row}, col {col}: ", self.ploc_map[row][col]) ; exit(0)
                    self.ploc_map[row][col] = 1    # Set the marker for allocate space
                    break

        if ploc == []:
            self.p_availability = "full"
        else:
            self.bill_data[r_ticket_num]['floc'] = ploc
                
        # Show the ticket information
        return r_ticket_num


    def update_space_status(self):
        ploc = []
        # Get available location for parking
        for row in range(len(self.ploc_map)):
            for col in range(len(self.ploc_map[row])):
                if self.ploc_map[row][col] == 0:
                    ploc = [row, col]

        if ploc == []:
            self.p_availability = "full"
        else:
            self.p_availability = "empty"


## ----------------------------------------------------------- ##
class Car:
    # Define attributes
    owner = ''
    cur_location = ""
    ticket_status = ''

    def __init__(self, car_owner):
        self.owner = car_owner
        self.cur_location = "Home"
        self.ticket_status = "Blank"

    # Define Methods
    def wait_on_q(self):
        self.cur_location = "on_queue"
        

    def go_in_park(self, p_location):
        self.cur_location = p_location


    def get_out_park(self):
        self.cur_location = 'on_road'


    def pay_bill(self, bill_amount):
        print("Give money", bill_amount)
        return 'ok'

## ----------------------------------------------------------- ##
class BiCycle( Car ):
    # Define attributes
    byc_owner = ""

    def __init__(self, name):
        self.byc_owner = name

    # Define Methods
    pass

## ================= Start Main Program ====================== ##
# Global variable
parkig_q = 'empty'
bill_q = 'empty'
vehicle_type = ''

## ----------------------------------------------------------- ##
# Build parking lot
marsP =  ParkingLot("Mars_parking", 2, 10)
marsP.allocate_area(15, 5)
marsP.set_parking_cost(5, 2)

def parkig_manager(veh_obj, vehicle_type, parkig_q="not_empty", bill_q="empty" ):
    # Check the queue of the parking entrance
    if parkig_q == 'not_empty':
        if vehicle_type == "car":
            veh_obj.ticket_status = marsP.gen_ticket(veh_obj.owner, marsP.pc_car)
            veh_obj.go_in_park( marsP.bill_data[veh_obj.ticket_status]["floc"] )
            pass
        elif vehicle_type == 'bicycle':
            veh_obj.ticket_status = marsP.gen_ticket(veh_obj.owner, marsP.pc_by)
            veh_obj.go_in_park( marsP.bill_data[veh_obj.ticket_status]["floc"] )
            pass
        else:
            print("Unidetifyed vehicle! WARNING for UFO.")
        # Update parking availability status
        marsP.update_space_status()
    elif bill_q == 'not_empty':
        marsP.gen_bill(veh_obj.ticket_status)
        marsP.collect_bill(veh_obj.ticket_status) 
        veh_obj.pay_bill(marsP.bill_data[veh_obj.ticket_status]["bill"])
        marsP.close_ticket(veh_obj.ticket_status)
        veh_obj.get_out_park()
        # Update parking availability status
        marsP.update_space_status()
    else:
        print("Parking manager is free to watch TV.")

# Build Car
carT = Car('Tesla')
carN = Car('Nova')

# Build Bicycle
bicA = BiCycle("Alpha")


## ----------------------------------------------------------- ##
if marsP.p_availability == "empty":
    parkig_manager(carT, 'car', 'not_empty')
    print("Current location of Tesla car", carT.cur_location)
    print("Ticket number of Tesla car", carT.ticket_status)
    print("Entry time of Tesla car", marsP.bill_data[carT.ticket_status]['stime'] )

# print("[Debug]: parking agailabilit", marsP.p_availability)
if marsP.p_availability == "empty":
    parkig_manager(bicA, 'bicycle', 'not_empty')
    print("Current location of Alpha cycle", bicA.cur_location)
    print("Entry time of Alpha cycle", marsP.bill_data[bicA.ticket_status]['stime'] )


parkig_manager(carT, 'car', parkig_q='none', bill_q='not_empty')
print("Current location of Tesla car", carT.cur_location)


print("By by from the Mars!!!")

