import customtkinter as ctk
import manager_data
 
class WaitingRoomView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
 
        title_wai_room = ctk.CTkFrame(self, corner_radius=10, border_width=2, height=40, border_color="black")
        title_wai_room.pack(padx=10, pady=10, fill="x")
        ctk.CTkLabel(title_wai_room, text="Waiting Room", font=("Arial", 20)).pack(pady=20)
 
        #==========frame for waiting room list============
        self.list_frame = ctk.CTkScrollableFrame(self, width=500, height=350)
        self.list_frame.pack(pady=10, fill="x", expand=True)
 
        self.load_waiting_room()
 
    def load_waiting_room(self): 
        for widget in self.list_frame.winfo_children():
            widget.destroy()
 
        data = manager_data.load_data()
        patients = {p["id"]: p for p in data["patients"]}
 
        if not data["waiting room"]:
            ctk.CTkLabel(self.list_frame, text="No patients in the waiting room today.",
                         font=("Arial", 14)).pack(pady=20)
            return
 
        for i in data["waiting room"]:
            patient = patients.get(i["id"])
            if not patient:
                continue
 
            text = f'{patient["first name"]} {patient["last name"]}  |  {patient["phone number"]}'
            frame = ctk.CTkFrame(self.list_frame, height=35, border_width=1, border_color="black", corner_radius=10)
            frame.pack(pady=5, padx=5, fill="x")
            frame.pack_propagate(False)
 
            ctk.CTkLabel(frame, text=text).pack(side="left", pady=5, padx=5)
 
            # View details button
            ctk.CTkButton(frame, text="details", width=60, height=24,
                          command=lambda p=patient: self.view_details(p)).pack(side="left", padx=5)
 
            # Send to consulted button (green)
            ctk.CTkButton(frame, text=" Consulted ✔", width=110, height=24,
                          fg_color="#2e7d32", hover_color="#1b5e20",
                          command=lambda p=patient: self.ask_payment(p)).pack(side="left", padx=5)
 
    def ask_payment(self, patient):
        #Popup to enter the amount paid before sending to consulted
        pay_win = ctk.CTkToplevel(self)
        pay_win.title("Payment")
        pay_win.geometry("350x200")
        pay_win.grab_set()
 
        name = f'{patient["first name"]} {patient["last name"]}'
        ctk.CTkLabel(pay_win, text=f'Consultation done for {name}', font=("Arial", 14, "bold")).pack(pady=15)
        ctk.CTkLabel(pay_win, text="Amount paid (DA):", font=("Arial", 13)).pack()
 
        amount_entry = ctk.CTkEntry(pay_win, placeholder_text="0", width=150)
        amount_entry.pack(pady=8)
 
        error_label = ctk.CTkLabel(pay_win, text="", text_color="red", font=("Arial", 12))
        error_label.pack()
 
        def confirm():
            raw = amount_entry.get().strip()
            # Allow empty input as 0
            if raw == "":
                amount = 0
            else:
                try:
                    amount = float(raw)
                except ValueError:
                    error_label.configure(text="Please enter a valid number!")
                    return
            manager_data.send_to_consulted(patient["id"], amount)
            pay_win.destroy()
            self.load_waiting_room()
            self.show_toast(f' {name} moved to consulted ✅ Paid: {amount} DA')
 
        ctk.CTkButton(pay_win, text="Confirm", command=confirm).pack(pady=10)
 
    def view_details(self, patient):
        details_win = ctk.CTkToplevel(self)
        details_win.title("Patient details")
        details_win.geometry("500x500")
        details_win.grab_set()
 
        ctk.CTkLabel(details_win, text=f'Name: {patient["first name"]}     Last name: {patient["last name"]}', font=("Arial", 18)).pack(pady=10)
        ctk.CTkLabel(details_win, text=f'Phone: {patient["phone number"]}     Phone 2: {patient["phone number2"]}', font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(details_win, text=f'Age: {patient["age"]}     Sex: {patient["sex"]}', font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(details_win, text=f'Details: {patient["details"]}', font=("Arial", 16)).pack(pady=5)
 
        ctk.CTkLabel(details_win, text="Consultation History", font=("Arial", 16, "bold")).pack(pady=(15, 5))
        history_frame = ctk.CTkScrollableFrame(details_win, width=400, height=200)
        history_frame.pack(pady=5, padx=10, fill="x")
 
        if not patient["consultation history"]:
            ctk.CTkLabel(history_frame, text="No consultation history").pack(pady=10)
        else:
            for entry in patient["consultation history"]:
                ctk.CTkLabel(history_frame, text=f'Date: {entry["date"]}   ~   Paid: {entry["paid"]} DA',
                             font=("Arial", 14)).pack(pady=5)
 
    def show_toast(self, message):
        toast = ctk.CTkLabel(self, text=message, font=("Arial", 13))
        toast.pack(pady=2)
        toast.after(2500, toast.destroy)