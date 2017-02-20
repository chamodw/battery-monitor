import time
import sys
import threading
import serial

performed_tilts = 0
detected_tilts = 0

bt = serial.Serial(
    port='/dev/tty.usbserial-AL00C894',
    baudrate=2400,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS,
    timeout=50
)

ard = serial.Serial(
    port='/dev/tty.wchusbserial1410',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
stop_flag = False;
def read_bluetooth():
    global bt_str
    global stop_flag
    global bt
    global bt_available
    global detected_tilts
    while(1):
        if(stop_flag):
            break
        bt_str = bt.readline()[0:2]
        if len(bt_str) > 0:
            detected_tilts+=1;
            bt_available = True


bt_str = ""
bt_available = False
start = time.time();
last_bt_transmission = time.time()


battery_id = raw_input("Enter the battery ID: ");

time.sleep(3);
ard.write('A'); #Signal start
thread1 = threading.Thread(target=read_bluetooth)
thread1.start()
log = open('logs/ID:' + battery_id  + "-" + time.strftime("%b%d-%H:%M:%S", time.localtime())+ '.txt', 'w');
while(1):
    ard_str = ard.readline()[0:2]
    performed_tilts+=1;
    if (bt_available):
        bt_line = '\t' + bt_str + '  ' + time.strftime("%b-%d %H:%M:%S", time.localtime());
        log.write(bt_line);
        log.write("\n");
        last_bt_transmission = time.time();
        bt_available = False
        bt_str = ""

    ard_line =   ard_str + '  ' + time.strftime("%b-%d %H:%M:%S", time.localtime());
    log.write(ard_line);
    log.write("\n");

    #print   str(detected_tilts), '\\', str(performed_tilts), "Elapsed time:",
    if stop_flag == False:
        sys.stdout.write("\r%d\\%d    Elapsed time: %s"% (detected_tilts, performed_tilts,time.strftime("%H:%M:%S", time.gmtime(time.time()-start)))),
        sys.stdout.flush();
    if (time.time() - last_bt_transmission) > 100:
        ard.write('S')
        ard.flush();
        ard.close();
        stop_flag = True;
        log.close()
        bt.close()
        ard.close()
        exit()
        break


