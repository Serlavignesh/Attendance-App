from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import json
import os
from datetime import datetime

STUDENTS_FILE = "students_data.json"
ATTENDANCE_FILE = "attendance_data.json"

def load_students():
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, "r") as f:
            return json.load(f)
    return {"Pre-Primary": [], "1": [], "2": [], "3": [], "4": [], "5": []}

def save_students(data):
    with open(STUDENTS_FILE, "w") as f:
        json.dump(data, f)

def load_attendance():
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "r") as f:
            return json.load(f)
    return {"Pre-Primary": {}, "1": {}, "2": {}, "3": {}, "4": {}, "5": {}}

def save_attendance(data):
    with open(ATTENDANCE_FILE, "w") as f:
        json.dump(data, f)

# -------------------------------------------------------------
# 1. CLASS SELECTION SCREEN (App Startup)
# -------------------------------------------------------------
class ClassSelectScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        layout.add_widget(Label(text="Student Attendance System", font_size=24, size_hint=(1, None), height=50))
        layout.add_widget(Label(text="Select Class to Open:", font_size=18, size_hint=(1, None), height=30))
        
        self.spinner = Spinner(
            text='Pre-Primary',
            values=('Pre-Primary', '1', '2', '3', '4', '5'),
            size_hint=(1, None),
            height=50
        )
        layout.add_widget(self.spinner)
        
        proceed_btn = Button(text="Open Class Dashboard", size_hint=(1, None), height=60)
        proceed_btn.bind(on_press=self.go_to_dashboard)
        layout.add_widget(proceed_btn)
        
        self.add_widget(layout)

    def go_to_dashboard(self, instance):
        selected_class = self.spinner.text
        dashboard = self.manager.get_screen('dashboard')
        dashboard.set_class(selected_class)
        self.manager.current = 'dashboard'

# -------------------------------------------------------------
# 2. CLASS DASHBOARD SCREEN (Options 1 to 6)
# -------------------------------------------------------------
class ClassDashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_class = 'Pre-Primary'
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.title_label = Label(text="", font_size=20, size_hint=(1, None), height=40)
        layout.add_widget(self.title_label)
        
        # 6 Options buttons
        btn1 = Button(text="1. Add Student", size_hint=(1, None), height=45)
        btn1.bind(on_press=lambda x: self.navigate('add_student'))
        layout.add_widget(btn1)
        
        btn2 = Button(text="2. Delete a Student", size_hint=(1, None), height=45)
        btn2.bind(on_press=lambda x: self.navigate('delete_student'))
        layout.add_widget(btn2)
        
        btn3 = Button(text="3. Add Multiple Students", size_hint=(1, None), height=45)
        btn3.bind(on_press=lambda x: self.navigate('add_multi_students'))
        layout.add_widget(btn3)
        
        btn4 = Button(text="4. Delete Multiple Students", size_hint=(1, None), height=45)
        btn4.bind(on_press=lambda x: self.navigate('delete_multi_students'))
        layout.add_widget(btn4)
        
        btn5 = Button(text="5. Take Attendance of Students", size_hint=(1, None), height=45)
        btn5.bind(on_press=lambda x: self.navigate('take_attendance'))
        layout.add_widget(btn5)
        
        btn6 = Button(text="6. Show Attendance (Monthly)", size_hint=(1, None), height=45)
        btn6.bind(on_press=lambda x: self.navigate('show_attendance'))
        layout.add_widget(btn6)
        
        # Switch Class Button
        switch_class_btn = Button(text="🔄 Change Class (Switch Home)", size_hint=(1, None), height=50, background_color=(0.2, 0.5, 0.8, 1))
        switch_class_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'select_class'))
        layout.add_widget(switch_class_btn)
        
        self.add_widget(layout)

    def set_class(self, class_name):
        self.current_class = class_name
        self.title_label.text = f"Managing Class: {class_name}"

    def navigate(self, screen_name):
        screen = self.manager.get_screen(screen_name)
        if hasattr(screen, 'set_class'):
            screen.set_class(self.current_class)
        self.manager.current = screen_name

# -------------------------------------------------------------
# HELPER: Reusable Navigation Buttons for Sub-screens
# -------------------------------------------------------------
def add_common_nav_buttons(layout, screen_manager):
    back_btn = Button(text="Back to Dashboard", size_hint=(1, None), height=45)
    back_btn.bind(on_press=lambda x: setattr(screen_manager, 'current', 'dashboard'))
    layout.add_widget(back_btn)
    
    home_btn = Button(text="🔄 Change Class (Switch Home)", size_hint=(1, None), height=45, background_color=(0.2, 0.5, 0.8, 1))
    home_btn.bind(on_press=lambda x: setattr(screen_manager, 'current', 'select_class'))
    layout.add_widget(home_btn)

# -------------------------------------------------------------
# 3. ADD SINGLE STUDENT
# -------------------------------------------------------------
class AddStudentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_class = ''
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        self.header = Label(text="", font_size=18, size_hint=(1, None), height=40)
        layout.add_widget(self.header)
        
        layout.add_widget(Label(text="Student Name:", size_hint=(1, None), height=30))
        self.name_input = TextInput(multiline=False, size_hint=(1, None), height=50)
        layout.add_widget(self.name_input)
        
        save_btn = Button(text="Save Student", size_hint=(1, None), height=50)
        save_btn.bind(on_press=self.save)
        layout.add_widget(save_btn)
        
        self.status = Label(text="", size_hint=(1, None), height=30)
        layout.add_widget(self.status)
        
        add_common_nav_buttons(layout, self.manager)
        self.add_widget(layout)

    def set_class(self, class_name):
        self.current_class = class_name
        self.header.text = f"Add Student to Class {class_name}"
        self.name_input.text = ""
        self.status.text = ""

    def save(self, instance):
        name = self.name_input.text.strip()
        if not name:
            self.status.text = "Enter a valid name!"
            return
        data = load_students()
        if name not in data[self.current_class]:
            data[self.current_class].append(name)
            save_students(data)
            self.status.text = f"Added '{name}' successfully!"
            self.name_input.text = ""
        else:
            self.status.text = "Student already exists!"

# -------------------------------------------------------------
# 4. DELETE SINGLE STUDENT
# -------------------------------------------------------------
class DeleteStudentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_class = ''
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        self.header = Label(text="", font_size=18, size_hint=(1, None), height=40)
        layout.add_widget(self.header)
        
        layout.add_widget(Label(text="Exact Name to Delete:", size_hint=(1, None), height=30))
        self.name_input = TextInput(multiline=False, size_hint=(1, None), height=50)
        layout.add_widget(self.name_input)
        
        del_btn = Button(text="Delete Student", size_hint=(1, None), height=50)
        del_btn.bind(on_press=self.remove_student)
        layout.add_widget(del_btn)
        
        self.status = Label(text="", size_hint=(1, None), height=30)
        layout.add_widget(self.status)
        
        add_common_nav_buttons(layout, self.manager)
        self.add_widget(layout)

    def set_class(self, class_name):
        self.current_class = class_name
        self.header.text = f"Delete from Class {class_name}"
        self.name_input.text = ""
        self.status.text = ""

    def remove_student(self, instance):
        name = self.name_input.text.strip()
        data = load_students()
        if name in data[self.current_class]:
            data[self.current_class].remove(name)
            save_students(data)
            self.status.text = f"Deleted '{name}' successfully!"
            self.name_input.text = ""
        else:
            self.status.text = "Student not found!"

# -------------------------------------------------------------
# 5. ADD MULTIPLE STUDENTS
# -------------------------------------------------------------
class AddMultipleStudentsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_class = ''
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.header = Label(text="", font_size=18, size_hint=(1, None), height=40)
        layout.add_widget(self.header)
        
        layout.add_widget(Label(text="Enter names (one per line):", size_hint=(1, None), height=30))
        self.text_input = TextInput(hint_text="Alice\nBob\nCharlie", size_hint=(1, 1))
        layout.add_widget(self.text_input)
        
        save_btn = Button(text="Save All Students", size_hint=(1, None), height=50)
        save_btn.bind(on_press=self.save_multiple)
        layout.add_widget(save_btn)
        
        self.status = Label(text="", size_hint=(1, None), height=30)
        layout.add_widget(self.status)
        
        add_common_nav_buttons(layout, self.manager)
        self.add_widget(layout)

    def set_class(self, class_name):
        self.current_class = class_name
        self.header.text = f"Add Multiple Students to Class {class_name}"
        self.text_input.text = ""
        self.status.text = ""

    def save_multiple(self, instance):
        lines = self.text_input.text.strip().split('\n')
        data = load_students()
        added_count = 0
        for name in lines:
            clean_name = name.strip()
            if clean_name and clean_name not in data[self.current_class]:
                data[self.current_class].append(clean_name)
                added_count += 1
        save_students(data)
        self.status.text = f"Successfully added {added_count} new student(s)!"
        self.text_input.text = ""

# -------------------------------------------------------------
# 6. DELETE MULTIPLE STUDENTS
# -------------------------------------------------------------
class DeleteMultipleStudentsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_class = ''
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.header = Label(text="", font_size=18, size_hint=(1, None), height=40)
        layout.add_widget(self.header)
        
        layout.add_widget(Label(text="Enter names to delete (one per line):", size_hint=(1, None), height=30))
        self.text_input = TextInput(hint_text="Alice\nBob", size_hint=(1, 1))
        layout.add_widget(self.text_input)
        
        del_btn = Button(text="Delete Listed Students", size_hint=(1, None), height=50)
        del_btn.bind(on_press=self.delete_multiple)
        layout.add_widget(del_btn)
        
        self.status = Label(text="", size_hint=(1, None), height=30)
        layout.add_widget(self.status)
        
        add_common_nav_buttons(layout, self.manager)
        self.add_widget(layout)

    def set_class(self, class_name):
        self.current_class = class_name
        self.header.text = f"Delete Multiple from Class {class_name}"
        self.text_input.text = ""
        self.status.text = ""

    def delete_multiple(self, instance):
        lines = self.text_input.text.strip().split('\n')
        data = load_students()
        removed_count = 0
        for name in lines:
            clean_name = name.strip()
            if clean_name in data[self.current_class]:
                data[self.current_class].remove(clean_name)
                removed_count += 1
        save_students(data)
        self.status.text = f"Removed {removed_count} student(s)."
        self.text_input.text = ""

# -------------------------------------------------------------
# 7. TAKE ATTENDANCE
# -------------------------------------------------------------
class TakeAttendanceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_class = ''
        self.attendance_states = {}
        
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)

    def set_class(self, class_name):
        self.current_class = class_name
        self.layout.clear_widgets()
        self.attendance_states = {}
        
        self.layout.add_widget(Label(text=f"Take Attendance - Class {class_name}", font_size=18, size_hint=(1, None), height=40))
        
        students = load_students().get(class_name, [])
        if not students:
            self.layout.add_widget(Label(text="No students found in this class yet!\nPlease add students first."))
            add_common_nav_buttons(self.layout, self.manager)
            return

        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        for student in students:
            self.attendance_states[student] = "Present"
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            row.add_widget(Label(text=student, font_size=16))
            
            status_btn = Button(text="Present", background_color=(0.1, 0.6, 0.1, 1))
            status_btn.bind(on_press=lambda btn, s=student: self.toggle_status(btn, s))
            row.add_widget(status_btn)
            
            grid.add_widget(row)

        scroll.add_widget(grid)
        self.layout.add_widget(scroll)

        save_btn = Button(text="Save Attendance for Today", size_hint=(1, None), height=50)
        save_btn.bind(on_press=self.save_today_attendance)
        self.layout.add_widget(save_btn)

        add_common_nav_buttons(self.layout, self.manager)

    def toggle_status(self, button, student):
        if self.attendance_states[student] == "Present":
            self.attendance_states[student] = "Absent"
            button.text = "Absent"
            button.background_color = (0.8, 0.1, 0.1, 1)
        else:
            self.attendance_states[student] = "Present"
            button.text = "Present"
            button.background_color = (0.1, 0.6, 0.1, 1)

    def save_today_attendance(self, instance):
        today_date = datetime.now().strftime("%Y-%m-%d")
        month_key = datetime.now().strftime("%Y-%m")
        
        att_data = load_attendance()
        if self.current_class not in att_data:
            att_data[self.current_class] = {}
        if month_key not in att_data[self.current_class]:
            att_data[self.current_class][month_key] = {}
            
        att_data[self.current_class][month_key][today_date] = self.attendance_states
        save_attendance(att_data)
        
        self.manager.current = 'dashboard'

# -------------------------------------------------------------
# 8. SHOW ATTENDANCE (Monthly Separate Breakdown)
# -------------------------------------------------------------
class ShowAttendanceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_class = ''
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)

    def set_class(self, class_name):
        self.current_class = class_name
        self.layout.clear_widgets()
        
        self.layout.add_widget(Label(text=f"Attendance Records - Class {class_name}", font_size=18, size_hint=(1, None), height=40))
        
        att_data = load_attendance().get(class_name, {})
        if not att_data:
            self.layout.add_widget(Label(text="No attendance records found yet."))
        else:
            scroll = ScrollView(size_hint=(1, 1))
            grid = GridLayout(cols=1, spacing=15, size_hint_y=None)
            grid.bind(minimum_height=grid.setter('height'))

            for month in sorted(att_data.keys(), reverse=True):
                month_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
                month_box.add_widget(Label(text=f"--- Month: {month} ---", font_size=16, bold=True, size_hint_y=None, height=30))
                
                for date, records in sorted(att_data[month].items(), reverse=True):
                    record_text = f"Date: {date}\n" + ", ".join([f"{s}: {stat}" for s, stat in records.items()])
                    lbl = Label(text=record_text, font_size=14, size_hint_y=None, height=65)
                    month_box.add_widget(lbl)
                    
                grid.add_widget(month_box)

            scroll.add_widget(grid)
            self.layout.add_widget(scroll)

        add_common_nav_buttons(self.layout, self.manager)

# -------------------------------------------------------------
# APP ROUTER
# -------------------------------------------------------------
class AttendanceApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ClassSelectScreen(name='select_class'))
        sm.add_widget(ClassDashboardScreen(name='dashboard'))
        sm.add_widget(AddStudentScreen(name='add_student'))
        sm.add_widget(DeleteStudentScreen(name='delete_student'))
        sm.add_widget(AddMultipleStudentsScreen(name='add_multi_students'))
        sm.add_widget(DeleteMultipleStudentsScreen(name='delete_multi_students'))
        sm.add_widget(TakeAttendanceScreen(name='take_attendance'))
        sm.add_widget(ShowAttendanceScreen(name='show_attendance'))
        return sm

if __name__ == '__main__':
    AttendanceApp().run()
