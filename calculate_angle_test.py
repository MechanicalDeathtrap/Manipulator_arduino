import serial
import math
import time

PORT = "COM7"
BAUD_RATE = 9600

L1 = 75
L2 = 65


def calculate_angles(x, y):
    c = math.sqrt(x ** 2 + y ** 2)
    if c > (L1 + L2):
        raise ValueError("Точка вне досягаемости манипулятора")

    phi1 = math.acos((L1 ** 2 + c ** 2 - L2 ** 2) / (2 * L1 * c))
    phi2 = math.atan2(y, x)
    theta1 = math.degrees(phi1 + phi2)

    theta2 = math.degrees(math.acos((L1 ** 2 + L2 ** 2 - c ** 2) / (2 * L1 * L2)))
    return round(theta1/2.1, 2), round(theta2/2.1, 2)


def process_gcode(file_path):
    commands = []
    last_x, last_y = None, None

    max_x, max_y = 0, 0
    min_x, min_y = float('inf'), float('inf')

    #  максимальные и минимальные координаты
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("G"):
                parts = line.split()
                try:
                    x = float(next((p[1:] for p in parts if p.startswith("X")), 0))
                    y = float(next((p[1:] for p in parts if p.startswith("Y")), 0))
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                except Exception:
                    continue

    # коэффициент для масштабирования
    scale_factor = 99.0 / max(max_x - min_x, max_y - min_y)


    # смещение для центрирования
    offset_x = (99 - (max_x - min_x) * scale_factor) / 2
    offset_y = (99 - (max_y - min_y) * scale_factor) / 2

    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("G"):
                parts = line.split()
                try:
                    g_code = int(parts[0][1:])
                    x = float(next((p[1:] for p in parts if p.startswith("X")), None))
                    y = float(next((p[1:] for p in parts if p.startswith("Y")), None))

                    if x is not None and y is not None:
                        # масштабируем и смещаем рисунок
                        x = x * scale_factor + offset_x
                        y = y * scale_factor + offset_y

                        if last_x is not None and last_y is not None:
                            distance = ((x - last_x) ** 2 + (y - last_y) ** 2) ** 0.5
                            if distance < 5:
                                continue

                        last_x, last_y = x, y
                        theta1, theta2 = calculate_angles(x, y)
                        if g_code == 0:
                            commands.append((160, theta1, theta2))
                        elif g_code == 1:
                            commands.append((190, theta1 + 10, theta2 + 10))
                except Exception as e:
                    print(f"Ошибка обработки строки: {line.strip()} ({e})")

    return commands

def send_to_arduino(commands):
    with serial.Serial(PORT, BAUD_RATE, timeout=1) as ser:
        for command in commands:
            servo1, servo2, servo3 = command
            data = f"{servo1},{servo2},{servo3}\n"
            ser.write(data.encode())
            print(f"Отправлено: {data}")
            # response = wait_for_response(ser)
            # print(f"REsponse:{response}")
            ser.readline()
            time.sleep(1.3)


if __name__ == "__main__":
    gcode_file = "sava.gcode"
    commands = process_gcode(gcode_file)
    send_to_arduino(commands)