from machine import Pin, Timer, ADC, PWM

pot_output = ADC(Pin(4))                       
pot_output.atten(ADC.ATTN_11DB)
timer_adc = Timer(0)
pwm_supply = PWM(Pin(2))         
pot_input = ADC(Pin(15))         
pot_input.atten(ADC.ATTN_11DB)

SAMPLE_TIME = 50
time_limit = 30 * 1000/SAMPLE_TIME
current_time = 0

MAX_BITS = 2**16 - 1
MAX_PWM_VALUE = 65535
OFFSET_POTENTIOMETER = 7000
MAX_INPUT_ANGLE = 90
MAX_OUTPUT_ANGLE = 270


e_1 = 0
e_2 = 0
u_1 = 0
u_2 = 0

data = str()

def pid_control(r, y):
    global e_1, u_1, e_2, u_2
    
    Kp = 1
    Ki = 0.2
    Kd = 0.1
    
    e = r - y
    
    u = u_1 + Kp*e + Ki *(e+e_1) + Kd*(e-e_1)
    
    #u = 31090*e_1 + 28920*e_2 - 0.5559*u_1 - 0.9048*u_2 
    
    if u < 0:
        u = 0
    elif u > MAX_OUTPUT_ANGLE:
        u = MAX_OUTPUT_ANGLE
    
    #u_2 = u_1
    u_1 = u
    #e_2 = e_1
    e_1 = e
    
    return int(u)

def convert_scale(x, x_max, y_max):
    return y_max*x/x_max

def read_pot(timer):
    global data, time_limit, current_time
    
    output_pot_value = pot_output.read_u16() - OFFSET_POTENTIOMETER
    angle_output = convert_scale(output_pot_value, MAX_BITS, MAX_OUTPUT_ANGLE)
    
    input_pot_value = pot_input.read_u16()
    angle_input = convert_scale(input_pot_value, MAX_BITS, MAX_INPUT_ANGLE)
    
    angle_pid_output = pid_control(angle_input, angle_output)
    pwm_value = int(convert_scale(angle_pid_output, MAX_OUTPUT_ANGLE, MAX_PWM_VALUE))
    
    pwm_supply.duty_u16(MAX_PWM_VALUE - pwm_value)
    
    print(f'Entrada: {round(angle_input, 2)} Saída: {round(angle_output, 2)} : pwm = {pwm_value}')
               
    if current_time < time_limit:
        data += str(current_time/1000 * SAMPLE_TIME) + ',' + str(angle_input) + ',' + str(angle_output) + '\n'
            
    elif current_time == time_limit:
        with open('dados.txt','a') as f:
            f.write(data)
            f.close()
            
    current_time+=1
    
def app_init():     
    timer_adc.init(period=SAMPLE_TIME, mode=Timer.PERIODIC, callback=read_pot)

def app_loop():        
    while True:
        pass

if __name__=='__main__':
              
    app_init()
    app_loop()