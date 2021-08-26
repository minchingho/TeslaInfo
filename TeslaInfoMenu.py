
import getpass

from teslapy import Tesla


def show_vehicle_data(vehicle):
    climate_state = vehicle['climate_state']
    drive_state = vehicle['drive_state']
    vehicle_state = vehicle['vehicle_state']
    charge_state = vehicle['charge_state']
    vehicle_config = vehicle['vehicle_config']

    #Climate state
    fmt = 'Outside Temperature: {:17} Inside Temperature: {}'
    print(fmt.format(vehicle.temp_units(climate_state['outside_temp']),
                     vehicle.temp_units(climate_state['inside_temp'])))
    fmt = 'Driver Temperature Setting: {:10} Passenger Temperature Setting: {}'
    print(fmt.format(vehicle.temp_units(climate_state['driver_temp_setting']),
                     vehicle.temp_units(climate_state['passenger_temp_setting'])))
    fmt = 'Is Climate On: {:23} Fan Speed: {}'
    print(fmt.format(str(climate_state['is_climate_on']), climate_state['fan_status']))
    fmt = 'Driver Seat Heater: {:18} Passenger Seat Heater: {}'
    print(fmt.format(str(climate_state['seat_heater_left']), str(climate_state['seat_heater_right'])))
    fmt = 'Is Front Defroster On: {:15} Is Rear Defroster On: {}'
    print(fmt.format(str(climate_state['is_front_defroster_on']),
                     str(climate_state['is_rear_defroster_on'])))
    print('-'*80)
    # Vehicle state
    fmt = 'Vehicle Name: {:24} Odometer: {}'
    print(fmt.format(vehicle_state['vehicle_name'], vehicle.dist_units(vehicle_state['odometer'])))
    fmt = 'Car Version: {:25} Locked: {}'
    print(fmt.format(vehicle_state['car_version'], vehicle_state['locked']))
    door = ['Closed', 'Open']
    fmt = 'Driver/Pass Front Door: {:14} Driver/Pass Rear Door: {}/{}'
    print(fmt.format('%s/%s' % (door[bool(vehicle_state['df'])], door[bool(vehicle_state['pf'])]),
                     door[bool(vehicle_state['dr'])], door[bool(vehicle_state['pr'])]))
    window = {0: 'Closed', 1: 'Venting', 2: 'Open'}
    fmt = 'Drvr/Pass Front Window: {:14} Driver/Pass Rear Window: {}/{}'
    print(fmt.format('%s/%s' % (window.get(vehicle_state.get('fd_window')),
                                window.get(vehicle_state.get('fp_window'))),
                                window.get(vehicle_state.get('rd_window')),
                                window.get(vehicle_state.get('rp_window'))))
    fmt = 'Front Trunk: {:25} Rear Trunk: {}'
    print(fmt.format(door[vehicle_state['ft']], door[vehicle_state['rt']]))
    fmt = 'Remote Start: {:24} Is User Present: {}'
    print(fmt.format(str(vehicle_state['remote_start']), str(vehicle_state['is_user_present'])))
    fmt = 'Speed Limit Mode: {:20} Current Limit: {}'
    limit = vehicle.dist_units(vehicle_state['speed_limit_mode']['current_limit_mph'], True)
    print(fmt.format(str(vehicle_state['speed_limit_mode']['active']), limit))
    fmt = 'Speed Limit Pin Set: {:17} Sentry Mode: {}'
    print(fmt.format(str(vehicle_state['speed_limit_mode']['pin_code_set']),
                     str(vehicle_state['sentry_mode'])))
    fmt = 'Valet Mode: {:26} Valet Pin Set: {}'
    print(fmt.format(str(vehicle_state['valet_mode']), str(not 'valet_pin_needed' in vehicle_state)))
    print('-'*80)
    # Drive state
    speed = 0 if drive_state['speed'] is None else drive_state['speed']
    fmt = 'Power: {:31} Speed: {}'
    print(fmt.format(str(drive_state['power']) + ' kW', vehicle.dist_units(speed, True)))
    fmt = 'Shift State: {:25} Heading: {}'
    print(fmt.format(str(drive_state['shift_state']), drive_state['heading']))
    print('-'*80)
    # Charging state
    fmt = 'Charging State: {:22} Time To Full Charge: {:02.0f}:{:02.0f}'
    print(fmt.format(charge_state['charging_state'],
                     *divmod(charge_state['time_to_full_charge'] * 60, 60)))
    phases = '3 x ' if charge_state['charger_phases'] == 2 else ''
    fmt = 'Charger Voltage: {:21} Charger Actual Current: {}{:d} A'
    print(fmt.format(str(charge_state['charger_voltage']) + ' V',
                     phases, charge_state['charger_actual_current']))
    fmt = 'Charger Power: {:23} Charge Rate: {}'
    print(fmt.format(str(charge_state['charger_power']) + ' kW',
                     vehicle.dist_units(charge_state['charge_rate'], True)))
    fmt = 'Battery Level: {:23} Battery Range: {}'
    print(fmt.format(str(charge_state['battery_level']) + ' %',
                     vehicle.dist_units(charge_state['battery_range'])))
    fmt = 'Charge Energy Added: {:17} Charge Range Added: {}'
    print(fmt.format(str(charge_state['charge_energy_added']) + ' kWh',
                     vehicle.dist_units(charge_state['charge_miles_added_rated'])))
    fmt = 'Charge Limit SOC: {:20} Estimated Battery Range: {}'
    print(fmt.format(str(charge_state['charge_limit_soc']) + ' %',
                     vehicle.dist_units(charge_state['est_battery_range'])))
    fmt = 'Charge Port Door Open: {:15} Charge Port Latch: {}'
    print(fmt.format(str(charge_state['charge_port_door_open']),
                     str(charge_state['charge_port_latch'])))
    print('-'*80)
    # Vehicle config
    fmt = 'Car Type: {:28} Exterior Color: {}'
    print(fmt.format(vehicle_config['car_type'], vehicle_config['exterior_color']))
    fmt = 'Wheel Type: {:26} Spoiler Type: {}'
    print(fmt.format(vehicle_config['wheel_type'], vehicle_config['spoiler_type']))
    fmt = 'Roof Color: {:26} Charge Port Type: {}'
    print(fmt.format(vehicle_config['roof_color'], vehicle_config['charge_port_type']))


def menu(vehicle):
    lst = ['Refresh', 'Wake up']

    opt = 0
    while True:
        if vehicle['state'] == 'online':
            show_vehicle_data(vehicle.get_vehicle_data())
        else:
            print('Wake up vehicle to user remote telemetry')
        
        print('-'*80)

        for i, option in enumerate(lst, 1):
            print('{:2} {:23}'.format(i, option), end='' if i % 3 else '\n')

        print()
        print('-'*80)
        # Get user choice
        opt = int(input("Choice (0 to quit): "))
        print('-'*80)

        if opt == 0:
            break

        if opt == 1:
            pass
        elif opt == 2:
            print('Please wait...')
            vehicle.sync_wake_up()
            print('-'*80)

def select_factor(factors):
    print('-'*80)
    print('ID Name')
    for i, factor in enumerate(factors):
        print('{:2} {}'.format(i, factor['name']))
    print('-'*80)
    idx = int(input('Select factor: '))
    print('-'*80)
    return factors[idx]

def main():
    email = input('Enter email: ')
    password = getpass.getpass('Password: ')
    with Tesla(email, password) as tesla:
        tesla.factor_selector = select_factor
        tesla.fetch_token()
        vehicles = tesla.vehicle_list()
        print('-'*80)
        fmt = '{:2} {:25} {:25} {:25}'
        print(fmt.format('ID', 'Display name', 'VIN', 'State'))
        for i, vehicle in enumerate(vehicles):
            print(fmt.format(i, vehicle['display_name'], vehicle['vin'],
                             vehicle['state']))
        print('-'*80)
        idx = int(input("Select vehicle: "))
        print('-'*80)
        print('VIN decode:', ', '.join(vehicles[idx].decode_vin().values()))
        print('Option codes:', ', '.join(vehicles[idx].option_code_list()))
        print('-'*80)
        menu(vehicles[idx])

if __name__ == "__main__":
    main()