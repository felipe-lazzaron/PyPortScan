import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket
import threading

def scan_ports():
    target = entry_target.get()
    start_port = int(entry_start_port.get())
    end_port = int(entry_end_port.get())

    # Criar uma nova thread para o escaneamento
    scan_thread = threading.Thread(target=perform_scan, args=(target, start_port, end_port))
    scan_thread.start()

def perform_scan(target, start_port, end_port):
    for port in range(start_port, end_port+1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        sock.close()

        if result == 0:
            service_name = get_service_name(port)
            # Atualizar a interface gráfica usando uma função callback
            root.after(0, update_result_label, f"Porta {port}: {service_name} - Aberta\n")

def update_result_label(text):
    result_label.config(state=tk.NORMAL)
    result_label.insert(tk.END, text)
    result_label.config(state=tk.DISABLED)

def get_service_name(port):
    well_known_ports = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        # Adicione mais portas conforme necessário
    }

    return well_known_ports.get(port, "Desconhecido")

# Interface gráfica
root = tk.Tk()
root.title("Escaneamento de Portas")

main_frame = ttk.Frame(root, padding="20")
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)

label_target = ttk.Label(main_frame, text="Host:")
label_target.grid(column=0, row=0, sticky=tk.W)
entry_target = ttk.Entry(main_frame, width=30)
entry_target.grid(column=1, row=0)

label_start_port = ttk.Label(main_frame, text="Porta Inicial:")
label_start_port.grid(column=0, row=1, sticky=tk.W)
entry_start_port = ttk.Entry(main_frame, width=10)
entry_start_port.grid(column=1, row=1)

label_end_port = ttk.Label(main_frame, text="Porta Final:")
label_end_port.grid(column=0, row=2, sticky=tk.W)
entry_end_port = ttk.Entry(main_frame, width=10)
entry_end_port.grid(column=1, row=2)

scan_button = ttk.Button(main_frame, text="Escanear", command=scan_ports)
scan_button.grid(column=0, row=3, columnspan=2)

result_label = tk.Text(main_frame, height=10, width=50, state=tk.DISABLED)
result_label.grid(column=0, row=4, columnspan=2)

root.mainloop()
