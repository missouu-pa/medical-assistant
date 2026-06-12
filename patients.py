import customtkinter as ctk
import manager_data
 
class Patients(ctk.CTkFrame):  
    def __init__(self, parent):
        super().__init__(parent)
 
        title_patients = ctk.CTkFrame(self, corner_radius=10, border_width=2, height=40, border_color="black")
        title_patients.pack(padx=10, pady=10, fill="x")
        ctk.CTkLabel(title_patients, text="Patients", font=("Arial", 20)).pack(pady=20)
 
        #=============search bar===================
        self.search_bar = ctk.CTkEntry(self, placeholder_text="search for a patient...", width=350)
        self.search_bar.pack(pady=5)
        self.search_bar.bind("<KeyRelease>", lambda e: self.load_patients())
 
        #==========add patients button=====================
        self.add_patients_button = ctk.CTkButton(self, text="Add patients", command=self.add_patients)
        self.add_patients_button.pack(pady=1)
 
        #==========frame for patients list============
        self.list_frame = ctk.CTkScrollableFrame(self, width=500, height=350)
        self.list_frame.pack(pady=10, fill="x", expand=True)
        
        self.load_patients()
        
    def add_patients(self):
        popup_window = ctk.CTkToplevel(self)
        popup_window.title("Add patient")
        popup_window.geometry("400x500")
        popup_window.grab_set()
 
        ctk.CTkLabel(popup_window, text="Add patients details", font=("Arial", 18, "bold")).pack(pady=10)
 
        first_name = ctk.CTkEntry(popup_window, placeholder_text="Enter patient's name")
        first_name.pack(padx=30, pady=5)
        last_name = ctk.CTkEntry(popup_window, placeholder_text="Enter patient's last name")
        last_name.pack(padx=30, pady=5)
        phone_number = ctk.CTkEntry(popup_window, placeholder_text="Enter patient's number")
        phone_number.pack(padx=30, pady=5)
        phone_number2 = ctk.CTkEntry(popup_window, placeholder_text="second phone number")
        phone_number2.pack(padx=30, pady=5)
        age = ctk.CTkEntry(popup_window, placeholder_text="Enter age")
        age.pack(padx=30, pady=5)
        sex = ctk.CTkEntry(popup_window, placeholder_text="Enter patient's sex")
        sex.pack(padx=30, pady=5)
        details = ctk.CTkEntry(popup_window, placeholder_text="additional details")
        details.pack(padx=30, pady=5)
 
        ctk.CTkButton(popup_window, text="Save", command=lambda: self.save_patient(
            popup_window,
            first_name.get(),
            last_name.get(),
            phone_number.get(),
            phone_number2.get(),
            age.get(),
            sex.get(),
            details.get()
        )).pack(pady=10)
 
    def save_patient(self, popup_window, first_name, last_name, phone_number, phone_number2, age, sex, details):
        if not first_name or not last_name or not phone_number:
            error_msg = ctk.CTkLabel(popup_window, text="Please insert at least Name / Last name / Phone number!")
            error_msg.pack(pady=5)
            error_msg.after(3000, error_msg.destroy)
            return
        manager_data.add_patient(first_name, last_name, phone_number, phone_number2, age, sex, details)
        self.load_patients()
        popup_window.destroy()
    
    def load_patients(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
 
        data = manager_data.load_data()
        words = self.search_bar.get().strip().lower()
 
        for i in data["patients"]:
            full_name = f'{i["first name"]} {i["last name"]}'.lower()
            phone = i["phone number"].lower()
 
           
            if words and words not in full_name and words not in phone:
                continue
 
            name = f'{i["first name"]} {i["last name"]}  |  {i["phone number"]}'
            frame = ctk.CTkFrame(self.list_frame, height=35, border_width=1, border_color="black", corner_radius=10)
            frame.pack(pady=5, padx=5, fill="x")
            frame.pack_propagate(False)
 
            ctk.CTkLabel(frame, text=name).pack(side="left", pady=5, padx=5)
 
            # View details button
            ctk.CTkButton(frame, text="details", width=60, height=24,
                          command=lambda p=i: self.view_details(p)).pack(side="left", padx=5)
 
            # Send to waiting room button
            ctk.CTkButton(frame, text="Waiting Room➕", width=120, height=24,
                          command=lambda w_r=i: self.send_to_waiting_room(w_r)).pack(side="left", padx=5)
 
            # Delete button 
            ctk.CTkButton(frame, text="Delete 🗑", width=80, height=24,
                          fg_color="#e05252", hover_color="#b03a3a",
                          command=lambda p=i: self.confirm_delete(p)).pack(side="left", padx=5)
 
    def view_details(self, p):
        details_win = ctk.CTkToplevel(self)
        details_win.title("Patient details")
        details_win.geometry("500x500")
        details_win.grab_set()
 
        ctk.CTkLabel(details_win, text=f'Name: {p["first name"]}     Last name: {p["last name"]}', font=("Arial", 18)).pack(pady=10)
        ctk.CTkLabel(details_win, text=f'Phone: {p["phone number"]}     Phone 2: {p["phone number2"]}', font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(details_win, text=f'Age: {p["age"]}     Sex: {p["sex"]}', font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(details_win, text=f'Details: {p["details"]}', font=("Arial", 16)).pack(pady=5)
 
        ctk.CTkLabel(details_win, text="Consultation History", font=("Arial", 16, "bold")).pack(pady=(15, 5))
        history_frame = ctk.CTkScrollableFrame(details_win, width=400, height=200)
        history_frame.pack(pady=5, padx=10, fill="x")
 
        if not p["consultation history"]:
            ctk.CTkLabel(history_frame, text="No consultation history!").pack(pady=10)
        else:
            for entry in p["consultation history"]:
                ctk.CTkLabel(history_frame, text=f'Date: {entry["date"]}   ~   Paid: {entry["paid"]} DA',
                             font=("Arial", 14)).pack(pady=5)
 
    def send_to_waiting_room(self, patient):
        sent = manager_data.send_to_waiting_room(patient["id"])
        self.show_toast("Sent to waiting room!" if sent else "Already in waiting room!!")
 
    def confirm_delete(self, patient):
        # Confirmation popup before deleting
        confirm_win = ctk.CTkToplevel(self)
        confirm_win.title("Confirm Delete")
        confirm_win.geometry("320x160")
        confirm_win.grab_set()
 
        name = f'{patient["first name"]} {patient["last name"]}'
        ctk.CTkLabel(confirm_win, text=f'Delete patient "{name}"?', font=("Arial", 15)).pack(pady=20)
 
        btn_frame = ctk.CTkFrame(confirm_win, fg_color="transparent")
        btn_frame.pack(pady=10)
 
        ctk.CTkButton(btn_frame, text="Cancel", width=100,
                      command=confirm_win.destroy).pack(side="left", padx=10)
 
        ctk.CTkButton(btn_frame, text="Delete", width=100,
                      fg_color="#e05252", hover_color="#b03a3a",
                      command=lambda: self.do_delete(patient["id"], confirm_win)).pack(side="left", padx=10)
 
    def do_delete(self, patient_id, confirm_win):
        confirm_win.destroy()
        manager_data.delete_patient(patient_id)
        self.load_patients()
        self.show_toast("Patient deleted 🗑")
 
    def show_toast(self, message):
        #sho a temporarry message
        toast = ctk.CTkLabel(self, text=message, font=("Arial", 13))
        toast.pack(pady=2)
        toast.after(2500, toast.destroy)

