import curses
import paho.mqtt.client as mqtt
import json

broker_address = "192.168.1.10"
luc_topic = "cmnd/room_2svitlight/POWER" 
luc_update_topic = "luc_update_topic"  
toggle_topic = "stat/room_2svitlight/POWER"  

south_blinds_send = "cmnd/blinds_2south/shutterposition1"
south_blinds_status = "stat/blinds_2south/SHUTTER1"
west_blinds_send = "cmnd/blinds_2west/shutterposition1"
west_blinds_status = "stat/blinds_2west/SHUTTER1"
balcony_blinds_send = "cmnd/blinds_2balcony/ShutterPosition1"  
balcony_blinds_status = "stat/blinds_2balcony/SHUTTER1"  
temperature_topic = "tele/livingroom_2/SENSOR"

c = mqtt.Client()
c.username_pw_set(username="", password="")
c.connect(broker_address, port=1883)

temperature = "N/A"
humidity = "N/A"
def send_toggle_packet():
    c.publish(luc_topic, payload="TOGGLE")
    add_message_to_window("TOGGLE -> stat/room_2svitlight/POWER", "green")

def send_blinds_position(topic, percentage):
    c.publish(topic, payload=str(percentage))
    add_message_to_window(f"{percentage}% ->  {topic}", "green")

def mqtt_on_connect(c, userdata, flags, rc):
    add_message_to_window(f"Connected to 192.168.1.10 with result code: {str(rc)}", "green")

#def mqtt_on_message(c, userdata, msg):
#    global toggle_state, south_blinds_position, west_blinds_position, balcony_blinds_position, messages
#    message = msg.payload.decode().strip()

#    if msg.topic == south_blinds_status:
#        south_blinds_position = int(message)
#    elif msg.topic == west_blinds_status:
#        west_blinds_position = int(message)
#    elif msg.topic == balcony_blinds_status:
#        balcony_blinds_position = int(message)  
#    elif msg.topic == toggle_topic:
#        toggle_state = message.lower() == "on"

#    add_message_to_window(f"{message} <- {msg.topic}", "purple")

def mqtt_on_message(c, userdata, msg):
    global toggle_state, south_blinds_position, west_blinds_position, balcony_blinds_position, messages, temperature, humidity
    message = msg.payload.decode().strip()

    if msg.topic == south_blinds_status:
        south_blinds_position = int(message)
    elif msg.topic == west_blinds_status:
        west_blinds_position = int(message)
    elif msg.topic == balcony_blinds_status:
        balcony_blinds_position = int(message)  
    elif msg.topic == toggle_topic:
        toggle_state = message.lower() == "on"
    elif msg.topic == temperature_topic:
        try:
            data = json.loads(message)
            if "SI7021" in data:
                temperature= f"{data['SI7021']['Temperature']}°C "
                humidity= f"{data['SI7021']['Humidity']}%"
                message=temperature + humidity
        except:
            temp_hum= "Error"

    add_message_to_window(f"{message} <- {msg.topic}", "purple")
c.on_connect = mqtt_on_connect
c.on_message = mqtt_on_message

def add_message_to_window(message, color):
    global messages
    messages.append((message, color))
    if len(messages) > max_messages:
        messages.pop(0)

def create_vertical_progress_bar(window, y, x, percentage, height, label=""):
    """Create a graphical vertical progress bar on the window."""
    window.addstr(y - 2, x, label, curses.color_pair(1))

    filled_length = int(height * (percentage / 100))
    for i in range(filled_length):
        window.addstr(y + height - i - 1, x, " ", curses.color_pair(1))
    for i in range(filled_length, height):
        window.addstr(y + height - i - 1, x, "#", curses.color_pair(1))

    window.addstr(y + height + 1, x - 1, f"{percentage}%", curses.color_pair(2))

def display_messages(msg_window):
    msg_window.clear()
    msg_window.border(0)
    for i, (message, color) in enumerate(messages):
        color_pair = curses.color_pair(7) if color == "blue" else \
                     curses.color_pair(3) if color == "green" else \
                     curses.color_pair(2) if color == "purple" else \
                     curses.color_pair(4)
        msg_window.addstr(i + 1, 1, message, color_pair)
    msg_window.refresh()


def connect_mqtt():
    c.connect(broker_address, 1883, 60)
    c.subscribe(luc_update_topic)
    c.subscribe(toggle_topic)
    c.subscribe(south_blinds_status)
    c.subscribe(west_blinds_status)
    c.subscribe(balcony_blinds_status)
    c.subscribe(temperature_topic)


c.on_message = mqtt_on_message

def ui_control(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)

    global toggle_state, south_blinds_position, west_blinds_position, balcony_blinds_position, messages, max_messages
    toggle_state = False
    south_blinds_position = 100
    west_blinds_position = 100
    balcony_blinds_position = 100 
    messages = []

    connect_mqtt()
    c.loop_start()

    msg_window_height = curses.LINES // 2
    msg_window_width = curses.COLS // 2
    msg_window = curses.newwin(msg_window_height, msg_window_width, curses.LINES - msg_window_height, 0)
    msg_window.scrollok(True)
    msg_window.bkgd(curses.color_pair(6))
    msg_window.border(0)
    msg_window.addstr(0, 2, "Messages:", curses.color_pair(4))
    max_messages = msg_window_height - 2

    temp_window = curses.newwin(msg_window_height, curses.COLS - msg_window_width, curses.LINES - msg_window_height, msg_window_width)
    temp_window.border(0)
    temp_window.addstr(0, 2, "Temperature", curses.color_pair(4))

    main_window = curses.newwin(curses.LINES - msg_window_height, curses.COLS, 0, 0)
    main_window.timeout(100)

    while True:
        main_window.clear()
        main_window.border(0)
        main_window.addstr(0, 2, " Nadzoor ", curses.color_pair(4))

        toggle_text = "[ON]" if toggle_state else "[OFF]"
        main_window.addstr(6, 5, "Luc: ", curses.color_pair(4))
        main_window.addstr(6, 10, toggle_text, curses.color_pair(5) if not toggle_state else curses.color_pair(3))

        create_vertical_progress_bar(main_window, 7, 20, south_blinds_position, 10, label="Jug:")  
        create_vertical_progress_bar(main_window, 7, 35, west_blinds_position, 10, label="Zahod:")  
        create_vertical_progress_bar(main_window, 7, 50, balcony_blinds_position, 10, label="Balkon:")  

        display_messages(msg_window)

        temp_window.clear()
        temp_window.border(0)
        temp_window.addstr(0, 2, " Podatki ", curses.color_pair(4))
        temp_window.addstr(2, 5, f"Temperatura v dneuni sobi: {temperature}", curses.color_pair(2))
        temp_window.addstr(3, 5, f"Vlaznost v dnevni sobi: {humidity}", curses.color_pair(2))
        temp_window.refresh()

        msg_window.border(0)
        msg_window.addstr(0, 2, " Log ", curses.color_pair(4))
        msg_window.refresh()

        main_window.refresh()

        key = main_window.getch()
        if key == -1:
            continue
        elif key in [ord('a'), ord('A')]:
            toggle_state = not toggle_state
            send_toggle_packet()
        elif key in [ord('w'), ord('W')]:
            if south_blinds_position < 100:
                south_blinds_position += 5
                send_blinds_position(south_blinds_send, south_blinds_position)
        elif key in [ord('s'), ord('S')]:
            if south_blinds_position > 0:
                south_blinds_position -= 5
                send_blinds_position(south_blinds_send, south_blinds_position)
        elif key in [ord('e'), ord('E')]:
            if west_blinds_position < 100:
                west_blinds_position += 5
                send_blinds_position(west_blinds_send, west_blinds_position)
        elif key in [ord('d'), ord('D')]:
            if west_blinds_position > 0:
                west_blinds_position -= 5
                send_blinds_position(west_blinds_send, west_blinds_position)
        elif key in [ord('r'), ord('R')]:
            if balcony_blinds_position < 100:
                balcony_blinds_position += 5
                send_blinds_position(balcony_blinds_send, balcony_blinds_position)
        elif key in [ord('f'), ord('F')]:
            if balcony_blinds_position > 0:
                balcony_blinds_position -= 5
                send_blinds_position(balcony_blinds_send, balcony_blinds_position)
        elif key in [ord('q'), 27]:
            break
    c.disconnect()

curses.wrapper(ui_control)

