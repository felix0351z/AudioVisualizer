import customtkinter as ctk
from program import SingleProgram


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.program = SingleProgram(self.callback)

        self.effects = self.program.get_effects()
        self.effect_names = []

        for effect in self.effects:
            self.effect_names.append(effect.name)
            print(effect.name)

        self.geometry("620x440")
        self.title("AudioVisualizer")

        self.select_frame = ctk.CTkFrame(self)
        self.select_frame.pack(pady=10, padx=100, expand=False)

        self.select_label = ctk.CTkLabel(self.select_frame, text="Change Effect")
        self.select_label.pack(pady=12, padx=10)

        self.combobox_var = ctk.StringVar(value="Shine")
        self.combobox = ctk.CTkComboBox(self.select_frame, values=self.effect_names,
                                        variable=self.combobox_var)
        self.combobox.pack(padx=20, pady=20)

        self.button = ctk.CTkButton(self.select_frame, text="set", command=self.change_effect)
        self.button.pack(padx=20, pady=10)

        self.program.start()

    def change_effect(self):
        selected_effect = self.combobox.get()
        pos = 0
        for effect in self.effects:
            if effect.name == selected_effect:
                break
            else:
                pos += 1
        self.program.set_effect(pos)

    def callback(self, raw):
        pass


app = App()
app.mainloop()
