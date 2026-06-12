import customtkinter as ctk
from views.patients import Patients
from views.waiting_room import WaitingRoomView
from views.consulted import ConsultedPatientsView
import manager_data


#==========appearance settings==========
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        manager_data.clean_up()

        self.title("Medical Assistant")
        self.geometry("900x600")
        #==========side bar==========
        self.sidebar = ctk.CTkFrame(self, width=400)
        self.sidebar.pack(side="left", fill="y", padx= 10, pady=10)
        ctk.CTkLabel(self.sidebar, text ="menu", font =( "Arial", 20)).pack(pady=20)
        ctk.CTkButton(self.sidebar, text="Patients", command=self.show_patients).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Waiting Room", command=self.show_waiting_room).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Consulted patients", command=self.show_consultations,).pack(pady=10)

        #=========main content ==========
        self.content =ctk.CTkFrame(self)
        self.content.pack(side="right", fill= "both", expand= True,padx=10, pady = 10)
        #========current view=========
        self.current_view = None
        self.show_patients()
        
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_patients(self):
        self.clear_content()
        self.current_view = Patients(self.content)
        self.current_view.pack(fill="both", expand=True)

    def show_waiting_room(self):
        self.clear_content()
        self.current_view = WaitingRoomView(self.content)
        self.current_view.pack(fill="both", expand=True)

    def show_consultations(self):
        self.clear_content()
        self.current_view = ConsultedPatientsView(self.content)
        self.current_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
