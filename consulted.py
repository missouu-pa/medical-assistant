import customtkinter as ctk
import manager_data
 
class ConsultedPatientsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        title_consulted = ctk.CTkFrame(self, corner_radius=10, border_width=2, height=40, border_color="black")
        title_consulted.pack(padx=10, pady=10, fill="x")
        ctk.CTkLabel(title_consulted, text="Consulted Patients", font=("Arial", 20)).pack(pady=20)
 
        # Total revenue label (today)
        self.revenue = ctk.CTkLabel(self, text="", font=("Arial", 14, "bold"))
        self.revenue.pack(pady=(0,5))
 
        #==========frame for consulted patients list============
        self.list_frame = ctk.CTkScrollableFrame(self, width=500, height=350)
        self.list_frame.pack(pady=10, fill="x", expand=True)
 
        self.load_consulted()
 
    def load_consulted(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
 
        data = manager_data.load_data()
        patients = {p["id"]: p for p in data["patients"]}
 
        if not data["consulted patients"]:
            ctk.CTkLabel(self.list_frame, text="No patients consulted today!",
                         font=("Arial", 14)).pack(pady=20)
            self.revenue.configure(text="Total revenue today: 0 DA")
            return
 
        total = 0
        for i in data["consulted patients"]:
            patient = patients.get(i["id"])
            if not patient:
                continue
 
            paid = i.get("paid", 0)
            total = total + paid
 
            name = f'{patient["first name"]} {patient["last name"]}  ~  {patient["phone number"]}'
            frame = ctk.CTkFrame(self.list_frame, height=35, border_width=1, border_color="black", corner_radius=10)
            frame.pack(pady=5, padx=5, fill="x")
            frame.pack_propagate(False)
 
            ctk.CTkLabel(frame, text=name).pack(side="left", pady=5, padx=5)
            ctk.CTkLabel(frame, text=f'Paid: {paid} DA',
                         font=("Arial", 13, "bold"), text_color="#2e7d32").pack(side="left", padx=10)
 
            # View details button
            ctk.CTkButton(frame, text="View", width=60, height=24,
                          command=lambda p=patient: self.view_details(p)).pack(side="left", padx=5)
 
        self.revenue.configure(text=f'Total revenue today: {total} DA')
 
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