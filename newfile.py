import os
import csv
from datetime import datetime

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.textinput import TextInput
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.togglebutton import ToggleButton
except ImportError:
    print("Kivy is not installed. Please run: pip install kivy")

class AttendanceApp(App):
    def build(self):
        self.title = "Student Attendance Tracker"
        
        # Use user_data_dir for safe writing on mobile (Android/iOS)
        data_dir = self.user_data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        self.csv_file = os.path.join(data_dir, "attendance_records.csv")
        self.students_file = os.path.join(data_dir, "students_list.txt")
        
        # Load existing students
        self.students = self.load_students()
        self.attendance_data = {}

        # Root Layout
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # --- Header Section ---
        header = Label(
            text=f"Date: {datetime.now().strftime('%Y-%m-%d')} | Attendance Tracker",
            size_hint_y=None,
            height=40,
            font_size=18
        )
        self.main_layout.add_widget(header)

        # --- Add Student Section ---
        add_student_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        self.student_input = TextInput(hint_text="Enter student name", multiline=False)
        add_button = Button(text="Add Student", size_hint_x=0.3)
        add_button.bind(on_press=self.add_student)
        
        add_student_layout.add_widget(self.student_input)
        add_student_layout.add_widget(add_button)
        self.main_layout.add_widget(add_student_layout)

        # --- Student List Scrollable View ---
        scroll_view = ScrollView()
        self.grid_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        
        self.populate_student_list()
        
        scroll_view.add_widget(self.grid_layout)
        self.main_layout.add_widget(scroll_view)

        # --- Action Buttons Section ---
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        save_button = Button(text="Save Attendance", background_color=(0.1, 0.6, 0.1, 1))
        save_button.bind(on_press=self.save_attendance)
        
        buttons_layout.add_widget(save_button)
        self.main_layout.add_widget(buttons_layout)

        return self.main_layout

    def load_students(self):
        """Loads the list of students from a local text file."""
        if os.path.exists(self.students_file):
            with open(self.students_file, 'r') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        return []

    def save_students_to_file(self):
        """Saves the current student list to a local text file."""
        with open(self.students_file, 'w') as f:
            for student in self.students:
                f.write(f"{student}\n")

    def populate_student_list(self):
        """Clears and rebuilds the visual student attendance grid."""
        self.grid_layout.clear_widgets()
        self.attendance_data = {}
        
        for student in self.students:
            name_label = Label(text=student, size_hint_y=None, height=40, halign='left', valign='middle')
            name_label.bind(size=name_label.setter('text_size'))
            
            status_button = ToggleButton(text='Present', state='down', size_hint_y=None, height=40, size_hint_x=0.3)
            status_button.bind(on_press=lambda btn, s=student: self.toggle_status(btn, s))
            
            self.attendance_data[student] = "Present"
            self.grid_layout.add_widget(name_label)
            self.grid_layout.add_widget(status_button)

    def toggle_status(self, button, student):
        """Toggles student status between Present and Absent."""
        if button.state == 'down':
            button.text = "Present"
            self.attendance_data[student] = "Present"
        else:
            button.text = "Absent"
            self.attendance_data[student] = "Absent"

    def add_student(self, instance):
        """Adds a new student to the database."""
        name = self.student_input.text.strip()
        if name and name not in self.students:
            self.students.append(name)
            self.save_students_to_file()
            self.populate_student_list()
            self.student_input.text = ""

    def save_attendance(self, instance):
        """Saves the attendance of the day into a CSV file."""
        date_str = datetime.now().strftime('%Y-%m-%d')
        file_exists = os.path.exists(self.csv_file)

        records = {}
        if file_exists:
            with open(self.csv_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader, None)
                for row in reader:
                    if row:
                        records[row[0]] = row[1:]

        for student, status in self.attendance_data.items():
            if student not in records:
                records[student] = []
            records[student].append(f"{date_str}: {status}")

        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Student Name", "Attendance History"])
            for student, history in records.items():
                writer.writerow([student] + history)
        
        print("Attendance successfully saved!")

if __name__ == '__main__':
    AttendanceApp().run()