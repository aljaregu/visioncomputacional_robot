import cv2
import serial
import numpy as np
import tkinter as tk
from tkinter import ttk

arduino = serial.Serial('COM14', 9600, timeout=0.1)
cap = cv2.VideoCapture(0)

color_ranges = {
    "Verde": (np.array([40, 50, 50]), np.array([80, 255, 255])),
    "Azul": (np.array([90, 50, 50]), np.array([130, 255, 255])),
    "Rojo": (np.array([0, 50, 50]), np.array([10, 255, 255]))
}

selected_color = "Verde"

def on_color_change(event):
    global selected_color
    selected_color = color_combobox.get()

def calculate_speed(cX, frame_width):
    center_x = frame_width // 2
    distance_from_center = abs(cX - center_x)

    # Inverse of distance (the closer, the higher the value)
    inverse_distance = 1 / (distance_from_center + 1e-9)  # Add a small value to avoid division by zero
    
    # Scale the inverse distance to control the speed (you may need to adjust these values)
    max_speed = 255  # Maximum PWM value for full speed
    min_speed = 100  # Minimum PWM value for slow speed
    
    # Calculate the speed based on the inverse distance
    speed = int(np.interp(inverse_distance, [0, 1], [min_speed, max_speed]))
    
    return speed

def detect_color(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color, upper_color = color_ranges[selected_color]
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        max_contour = max(contours, key=cv2.contourArea)

        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cX, cY), 5, (0, 255, 0), -1)

            # Calculate the speed based on the inverse distance
            speed = calculate_speed(cX, frame.shape[1])

            # Control the robot's movement and speed
            if cX < 220:
                arduino.write(f'L{speed}\n'.encode())  # Girar a la izquierda
            elif cX > 420:
                arduino.write(f'R{speed}\n'.encode())  # Girar a la derecha
            else:
                arduino.write(f'F{speed}\n'.encode())  # Avanzar
        else:
            arduino.write(b'S\n')  # Detenerse

def main():
    root = tk.Tk()
    root.title("Color Following Robot")

    global color_combobox
    color_combobox = ttk.Combobox(root, values=list(color_ranges.keys()))
    color_combobox.set(selected_color)
    color_combobox.bind("<<ComboboxSelected>>", on_color_change)
    color_combobox.pack(pady=10)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detect_color(frame)

        cv2.imshow("Color Following", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        root.update()  # Actualizar la interfaz gráfica

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
