#!/usr/bin/env python3
from serial import PARITY_ODD
from pprint import pprint
import minimalmodbus

plc = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # port name, slave address (in decimal)
plc.serial.baudrate = 38400
plc.serial.parity   = PARITY_ODD

status = {}

#Read and store inputs in status
CPUInputs = plc.read_bits(0x0,8)
status['master_power_switch']=bool(CPUInputs[0])
status['phase_error_bypass_button']=bool(CPUInputs[1])
status['overhead_on_button']=bool(CPUInputs[2])
status['overhead_off_button']=not bool(CPUInputs[3])
status['barn_west_on_button']=bool(CPUInputs[4])
status['barn_west_off_button']=not bool(CPUInputs[5])
status['barn_east_on_button']=bool(CPUInputs[6])
status['barn_east_off_button']=not bool(CPUInputs[7])
ACInputs = plc.read_bits(0x20,6)
status['phase_A_precontactor']=bool(ACInputs[0])
status['phase_B_precontactor']=bool(ACInputs[1])
status['phase_C_precontactor']=bool(ACInputs[2])
status['phase_A_postcontactor']=bool(ACInputs[3])
status['phase_B_postcontactor']=bool(ACInputs[4])
status['phase_C_postcontactor']=bool(ACInputs[5])

#Read and store coils in status
CPUCoils = plc.read_bits(0x2000,4,functioncode=1)
status['ac_power_indicator']=bool(CPUCoils[0])
status['overhead_power_indicator']=bool(CPUCoils[1])
status['barn_west_power_indicator']=bool(CPUCoils[2])
status['barn_east_power_indicator']=bool(CPUCoils[3])
AuxCoils = plc.read_bits(0x2040,5,functioncode=1)
status['ac_contactor']=bool(AuxCoils[0])
status['overhead_contactor']=bool(AuxCoils[1])
status['barn_main_contactor']=bool(AuxCoils[2])
status['barn_west_contactor']=bool(AuxCoils[3])
status['barn_east_contactor']=bool(AuxCoils[4])
InternalCoils = plc.read_bits(0x4000,6,functioncode=1)
status['overhead_power_state']=bool(InternalCoils[0])
status['barn_west_power_state']=bool(InternalCoils[1])
status['barn_east_power_state']=bool(InternalCoils[2])
status['phase_error_bypass_state']=bool(InternalCoils[3])
status['ac_supply_ready_state']=bool(InternalCoils[4])
status['emergency_power_off_state']=bool(InternalCoils[5])

#Read and store timers in status
Timers = plc.read_bits(0xB000,3)
status['dc_supply_ready']=bool(Timers[0])
status['no_load']=bool(Timers[1])
status['phase_error_bypass_timeout']=bool(Timers[2])

#Read and store clock in status for testing
Clock = plc.read_bits(0xF006,1)
status['1sec_clock']=bool(Clock[0])

pprint(status)
