import tkinter as tk

class TrafficLightFSM:
    def __init__(self, canvas):
        self.canvas = canvas
        self.lights = {
            0: self.canvas.create_oval(50, 50, 150, 150, fill="gray"),  # Red
            1: self.canvas.create_oval(50, 200, 150, 300, fill="gray"), # Yellow
            2: self.canvas.create_oval(50, 350, 150, 450, fill="gray"), # Green
        }
        # para transition
        self.state_matrix = {
            1: (0, 5000),  # Yellow to Red
            0: (2, 5000),  # Red to Green
            2: ("Off", 5000), # Green to Off
        }
        self.color_map = {0: "Red", 1: "Yellow", 2: "Green"}  # i-set si numbers to color/variable name
        self.state = 1  # Initial state is Yellow
        self.remaining_time = 5  # Timer countdown starts at 5 seconds
        self.timer_text = self.canvas.create_text(100, 500, text="", fill="black", font=("Helvetica", 24))
        self.timer_running = True
        self.waiting_for_next_state = False
        self.update_light()

    def switch_state(self):
        if self.state in self.state_matrix:
            next_state, _ = self.state_matrix[self.state]
            self.state = next_state
            self.remaining_time = 5  # Reset timer to 5 seconds
            self.timer_running = self.state != "Off" 
            self.waiting_for_next_state = False
            self.update_light()  
            return True
        return False

    def update_light(self):
        # Reset tanan colors to gray every after transition
        self.canvas.itemconfig(self.lights[0], fill="gray")
        self.canvas.itemconfig(self.lights[1], fill="gray")
        self.canvas.itemconfig(self.lights[2], fill="gray")

        if self.state in self.color_map:
            # Set the active light's color based on the state
            color = self.color_map[self.state].lower()
            self.canvas.itemconfig(self.lights[self.state], fill=color)

    def run(self):
        if self.state == "Off":
            self.show_turn_off_message()
            self.timer_running = False
            self.canvas.itemconfig(self.timer_text, text="")
            self.canvas.after(2000, exit)
            return

        self.canvas.after(1000, self.run)

    def update_timer(self):
        if self.timer_running:
            if self.remaining_time >= 0:
                self.canvas.itemconfig(self.timer_text, text=f"Time: {self.remaining_time} s")
                self.remaining_time -= 1
                self.canvas.after(1000, self.update_timer)
            elif not self.waiting_for_next_state:
                self.waiting_for_next_state = True
                if self.switch_state():  # Switch state and update light immediately
                    if self.state != "Off":
                        self.canvas.itemconfig(self.timer_text, text=f"Time: {self.remaining_time} s")
                        self.canvas.after(1000, self.update_timer)
        else:
            self.canvas.itemconfig(self.timer_text, text="")

    def show_turn_off_message(self):
        self.canvas.create_text(100, 250, text="Traffic light turned off", fill="black", font=("Helvetica", 16))

def main():
    root = tk.Tk()
    root.title("Traffic Light Simulation")

    canvas = tk.Canvas(root, width=200, height=550, bg="white")
    canvas.pack()

    traffic_light = TrafficLightFSM(canvas)
    traffic_light.run()
    traffic_light.update_timer() 

    root.mainloop()

if __name__ == "__main__":
    main()
