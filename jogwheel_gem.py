
from machine import Pin,ADC
import time,math,random,os

# Constants for ADC thresholds and states
ADC_THRESHOLD_IDLE = 3
ADC_THRESHOLD_ACTIVE = 0
ADC_THRESHOLD_HALF = 2 # Used for shuttle detection
ADC_MAX_STATE = 4

# Jog wheel specific states mapped from combinations of two ADC values
# These are arbitrary values (1-4) used in the original logic, representing phases of rotation
JOG_PHASE_1 = 1 # [4,0] or [0,4] depending on direction
JOG_PHASE_2 = 2 # [0,0]
JOG_PHASE_3 = 3 # [0,4] or [4,0] depending on direction
JOG_PHASE_4 = 4 # [4,4]

# Jog wheel direction
JOG_DIRECTION_CW = 'O' # Clockwise
JOG_DIRECTION_CCW = 'V' # Counter-clockwise

class JogWheel:
    def __init__(self, yellow_pin, green_pin, orange_pin):
        self.yellow_adc = ADC(Pin(yellow_pin))
        self.green_adc = ADC(Pin(green_pin))
        self.orange_adc = ADC(Pin(orange_pin))

        self.yellow_adc.atten(ADC.ATTN_11DB)
        self.green_adc.atten(ADC.ATTN_11DB)
        self.orange_adc.atten(ADC.ATTN_11DB)

        self.idle_state_values = [ADC_THRESHOLD_IDLE, ADC_THRESHOLD_IDLE, ADC_THRESHOLD_ACTIVE]
        self.previous_adc_values = [0, 0, 0]

        self.current_jog_direction = ''
        self.jog_delta_counter = 0
        self.current_jog_phase = 0
        self.previous_jog_phase = 0

    def clear_screen(self):
        print("\x1B\x5B2J", end="")
        print("\x1B\x5BH", end="")

    def read_adc_values(self):
        return [int(self.yellow_adc.read()/1000),
              int(self.green_adc.read()/1000),
              int(self.orange_adc.read()/1000)]

    def wait_for_idle(self):
        while not(self.read_adc_values()[0] == ADC_THRESHOLD_IDLE and self.read_adc_values()[1] == ADC_THRESHOLD_IDLE):
            pass

    def process_input(self):
        current_adc_values = self.read_adc_values();
        if current_adc_values == self.idle_state_values:
            self.current_jog_direction = ''
        elif self.previous_adc_values != current_adc_values:
            if current_adc_values[2] > 0:
                self._handle_jog_input(current_adc_values)
            else:
                self._handle_shuttle_input(current_adc_values)
        self.previous_adc_values = current_adc_values

    def _handle_jog_input(self, current_adc_values):
        two_axis_values = [current_adc_values[0], current_adc_values[1]]
        if self.current_jog_direction == '':
            if two_axis_values == [ADC_THRESHOLD_ACTIVE, ADC_MAX_STATE] : self.current_jog_direction = JOG_DIRECTION_CCW
            if two_axis_values == [ADC_MAX_STATE, ADC_THRESHOLD_ACTIVE] : self.current_jog_direction = JOG_DIRECTION_CW
            self.jog_delta_counter = 0
            self.current_jog_phase = 0
            self.previous_jog_phase = 0
        if self.current_jog_direction == JOG_DIRECTION_CW:
            if two_axis_values == [ADC_MAX_STATE, ADC_THRESHOLD_ACTIVE]: self.current_jog_phase = JOG_PHASE_1
            if two_axis_values == [ADC_THRESHOLD_ACTIVE, ADC_MAX_STATE]: self.current_jog_phase = JOG_PHASE_3
        else: # JOG_DIRECTION_CCW
            if two_axis_values == [ADC_MAX_STATE, ADC_THRESHOLD_ACTIVE]: self.current_jog_phase = JOG_PHASE_3
            if two_axis_values == [ADC_THRESHOLD_ACTIVE, ADC_MAX_STATE]: self.current_jog_phase = JOG_PHASE_1
        if two_axis_values == [ADC_THRESHOLD_ACTIVE, ADC_THRESHOLD_ACTIVE]: self.current_jog_phase = JOG_PHASE_2
        if two_axis_values == [ADC_MAX_STATE, ADC_MAX_STATE]: self.current_jog_phase = JOG_PHASE_4
        if self.previous_jog_phase + 1 == self.current_jog_phase and self.current_jog_phase == JOG_PHASE_3: self.jog_delta_counter += 1 ; print(self.current_jog_direction, self.jog_delta_counter)
        if self.previous_jog_phase - 1 == self.current_jog_phase and self.current_jog_phase == JOG_PHASE_1: self.jog_delta_counter -= 1 ; print(self.current_jog_direction, self.jog_delta_counter)
        self.previous_jog_phase = self.current_jog_phase

    def _handle_shuttle_input(self, current_adc_values):
        left_adc = current_adc_values[0]
        right_adc = current_adc_values[1]
        if right_adc > ADC_THRESHOLD_HALF and left_adc < ADC_THRESHOLD_HALF:
            print("JL")
            self.wait_for_idle()
        if left_adc > ADC_THRESHOLD_HALF and right_adc < ADC_THRESHOLD_HALF:
            print("JR")
            self.wait_for_idle()


# Main execution
def main():
    jogwheel = JogWheel(32, 33, 25)
    jogwheel.clear_screen()
    while True:
        jogwheel.process_input()

if __name__ == '__main__':
    main()


    
