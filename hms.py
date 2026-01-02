import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

class Hospital:
    def __init__(self):
        # Connect to SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect('hospital.db')
        self.cursor = self.conn.cursor()

        # Drop the old patients table if it exists
        self.cursor.execute('DROP TABLE IF EXISTS patients')

        # Create patients table with the correct schema
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                dob DATE NOT NULL,
                gender TEXT NOT NULL,  
                problem TEXT NOT NULL,
                mobile_no TEXT NOT NULL
            )
        ''')

        # Drop the old staff table if it exists
        self.cursor.execute('DROP TABLE IF EXISTS staff')

        # Create staff table with the correct schema
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                specialization TEXT NOT NULL,
                languages_spoken TEXT,
                mobile_no TEXT NOT NULL,
                email TEXT,
                schedule TEXT
            )
        ''')

        # Recreate appointments table with correct schema
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                details TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
            )
        ''')

    # Method to execute INSERT, UPDATE, DELETE queries
    def execute_query(self, query, parameters=()):
        self.cursor.execute(query, parameters)
        self.conn.commit()

    # Method to fetch records from the database
    def fetch_query(self, query, parameters=()):
        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()

    # Method to add a new patient
    def add_patient(self, name, dob, gender, problem, mobile_no):
        self.execute_query('''
            INSERT INTO patients (name, dob, gender, problem, mobile_no) 
            VALUES (?, ?, ?, ?, ?)
        ''', (name, dob, gender, problem, mobile_no))

    # Method to add a new staff member
    def add_staff(self, name, age, gender, specialization, languages_spoken, mobile_no, email, schedule):
        self.execute_query('''
            INSERT INTO staff (name, age, gender, specialization, languages_spoken, mobile_no, email, schedule) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, gender, specialization, languages_spoken, mobile_no, email, schedule))

    # Method to add a new appointment
    def add_appointment(self, patient_id, date, time, details):
        self.execute_query('''
            INSERT INTO appointments (patient_id, date, time, details) 
            VALUES (?, ?, ?, ?)
        ''', (patient_id, date, time, details))

    # Close the database connection
    def close(self):
        self.conn.close()

    
class HospitalGUI:
    def __init__(self, root):
        self.hospital = Hospital()
        self.root = root
        self.root.title("Hospital Management System")

        # Load the hospital image
        self.load_image()

        # Create a login frame
        self.create_login_frame()

        # Photo slideshow variables
        self.photo_index = 0
        self.photo_files = [
            r"C:\Users\chint\Downloads\hospital1.jpg",
            r"C:\Users\chint\Downloads\hospital2.jpg",
            r"C:\Users\chint\Downloads\hospital3.jpg",
            r"C:\Users\chint\Downloads\hospital4.jpg",
            r"C:\Users\chint\Downloads\hospital5.jpg"
        ]
        self.slideshow_running = False
        self.slideshow_label = None  # Placeholder for the slideshow label

    def load_image(self):
        image_path = r"C:\Users\chint\Downloads\hospital.jpg"
        if os.path.exists(image_path):
            self.hospital_image = Image.open(image_path)
            self.update_image()

            self.canvas = tk.Canvas(self.root, width=self.hospital_image.width, height=self.hospital_image.height)
            self.canvas.pack(fill='both', expand=True)

            self.hospital_image_tk = ImageTk.PhotoImage(self.hospital_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.hospital_image_tk)
        else:
            messagebox.showerror("File Error", f"Image file not found: {image_path}")

    def update_image(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        img_width, img_height = self.hospital_image.size
        aspect_ratio = img_width / img_height

        if img_width > screen_width or img_height > screen_height:
            if aspect_ratio > 1:  # Wider than tall
                new_width = screen_width
                new_height = int(screen_width / aspect_ratio)
            else:  # Taller than wide
                new_height = screen_height
                new_width = int(screen_height * aspect_ratio)
        else:
            new_width, new_height = img_width, img_height

        # Resize image
        self.hospital_image = self.hospital_image.resize((new_width, new_height), Image.LANCZOS)

    def create_login_frame(self):
        self.login_frame = ttk.Frame(self.root, relief=tk.SUNKEN, borderwidth=10, padding=20)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Add login sub-heading
        sub_heading_label = ttk.Label(self.login_frame, text="ADMIN LOGIN", font=("Helvetica", 24, "bold"))
        sub_heading_label.grid(row=1, column=0, columnspan=2, pady=10)
        sub_heading_label.configure(background='lightblue', foreground='darkblue')

        ttk.Label(self.login_frame, text="Username", font=("Helvetica", 12)).grid(row=2, column=0, pady=10)
        self.username_entry = ttk.Entry(self.login_frame, font=("Helvetica", 12))
        self.username_entry.grid(row=2, column=1, pady=10)

        ttk.Label(self.login_frame, text="Password", font=("Helvetica", 12)).grid(row=3, column=0, pady=10)
        self.password_entry = ttk.Entry(self.login_frame, show='*', font=("Helvetica", 12))
        self.password_entry.grid(row=3, column=1, pady=10)

        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(self.login_frame, text="Forgot Password?", command=self.forgot_password).grid(row=5, column=0, columnspan=2, pady=10)

        # Configure styles
        style = ttk.Style()
        style.configure('TFrame', background='lightblue')
        style.configure('TButton', background='skyblue', font=("Helvetica", 12))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Basic authentication
        if username == "admin" and password == "password":
            messagebox.showinfo("Login Successful", "Welcome to the Hospital Management System!")
            self.canvas.destroy()  # Close the image
            self.login_frame.destroy()  # Remove the login frame
            self.create_home_frame()  # Create the home frame
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Reset password feature is not implemented yet.")

    def create_home_frame(self):
        self.clear_frame()
        self.home_frame = ttk.Frame(self.root)
        self.home_frame.pack(fill='both', expand=True)

        heading_label = ttk.Label(self.home_frame, text="HOSPITAL MANAGEMENT SYSTEM", font=("Helvetica", 24, "bold"))
        heading_label.pack(pady=10)
        heading_label.configure(background='lightblue', foreground='darkblue')

        # Create a frame for buttons
        button_frame = ttk.Frame(self.home_frame)
        button_frame.pack(pady=10)

        # Home options in a single row
        ttk.Button(button_frame, text="Home", command=self.show_slideshow).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="New Patient", command=self.open_new_patient_frame).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="New Staff", command=self.open_new_staff_frame).pack(side=tk.LEFT, padx=5)

        # Appointments Menu Button
        appointment_button = tk.Menubutton(button_frame, text="Appointments", font=("Helvetica", 14), relief=tk.RAISED)
        appointment_menu = tk.Menu(appointment_button, tearoff=0)

        # Sub-menu options
        appointment_menu.add_command(label="Book Appointment", command=self.create_appointments_frame)
        appointment_menu.add_command(label="View Appointments", command=self.create_view_appointments_frame)
        appointment_menu.add_command(label="Cancel Appointment", command=self.create_cancel_appointments_frame)

        appointment_button.config(menu=appointment_menu)
        appointment_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="View Patient by ID", command=self.create_view_patients_frame).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Discharge Patient", command=self.create_discharge_patient_frame).pack(side=tk.LEFT, padx=5)

        # Contact Us button
        ttk.Button(self.home_frame, text="Contact Us", command=self.create_contact_us_frame).pack(padx=10)

        # Billing button
        ttk.Button(button_frame, text="Billing", command=self.create_billing_frame).pack(side=tk.LEFT,padx=5)
        ttk.Button(button_frame, text="View Staff", command=self.create_view_staff_frame).pack(side=tk.LEFT,padx=10)
        # Start the photo slideshow
        self.slideshow_label = tk.Label(self.home_frame)
        self.slideshow_label.pack(fill='both', expand=True)
        self.photo_index = 0
        self.show_slideshow()

    def show_slideshow(self):
        if self.photo_index >= len(self.photo_files):
            self.photo_index = 0  # Reset index

        img_path = self.photo_files[self.photo_index]
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((1200, 600), Image.LANCZOS)
            self.photo_index += 1
            img_tk = ImageTk.PhotoImage(img)

            self.slideshow_label.configure(image=img_tk)
            self.slideshow_label.image = img_tk  # Keep a reference to avoid garbage collection

            # Call this method again after 3 seconds
            self.slideshow_label.after(3000, self.show_slideshow)  # Change image every 3 seconds

    def clear_frame(self):
        # Destroy all widgets from the root window (i.e., the main container)
        for widget in self.root.winfo_children():
            widget.destroy()
    def create_contact_us_frame(self):
        self.clear_frame()  # Clear the current frame before creating a new one

        # Create the contact us frame
        self.contact_frame = ttk.Frame(self.root, padding=20)  # Attach to root window
        self.contact_frame.pack(fill='both', expand=True)

        # Add a title label for better visualization
        title_label = ttk.Label(self.contact_frame, text="Contact Us", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(10, 20))  # Add some top padding for visual appeal

        # Hospital details to display
        hospital_details = [
            "Hospital Name: City Hospital",
            "Address: 123 Health St, Wellness City, CA 90210",
            "Phone: (123) 456-7890",
            "Email: info@cityhospital.com",
            "Website: www.cityhospital.com"
        ]

        # Create labels for each detail in a loop
        for detail in hospital_details:
            label = ttk.Label(self.contact_frame, text=detail, font=("Helvetica", 14))
            label.pack(pady=5)

        # Create a "Back to Home" button
        back_button = ttk.Button(self.contact_frame, text="Back to Home", command=self.create_home_frame)
        back_button.pack(pady=20)

    def create_view_staff_frame(self):
        self.clear_frame()  # Clear the current frame

        # Create the staff viewing frame
        staff_frame = ttk.Frame(self.root, padding=20)
        staff_frame.pack(fill='both', expand=True)

        # Title label with larger font
        ttk.Label(staff_frame, text="Staff Details", font=("Helvetica", 20, "bold")).pack(pady=10)

        # Create a custom style for the Treeview to increase font size
        style = ttk.Style()
        style.configure("Treeview", font=("Times New Roman", 14))  # Set font for Treeview rows
        style.configure("Treeview.Heading", font=("Times New Roman", 16, "bold"))  # Set font for Treeview headers

        # Create a Treeview widget to display staff records
        tree = ttk.Treeview(staff_frame, columns=("ID", "Name", "Age", "Gender", "Specialization", "Languages", "Mobile No", "Email", "Schedule"), show='headings')

        # Define the headings
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Age", text="Age")
        tree.heading("Gender", text="Gender")
        tree.heading("Specialization", text="Specialization")
        tree.heading("Languages", text="Languages Spoken")
        tree.heading("Mobile No", text="Mobile No")
        tree.heading("Email", text="Email")
        tree.heading("Schedule", text="Schedule")

        # Set column widths and center the text in each column
        tree.column("ID", width=50, anchor="center")  # Center-aligned
        tree.column("Name", width=150, anchor="center")  # Center-aligned
        tree.column("Age", width=50, anchor="center")  # Center-aligned
        tree.column("Gender", width=100, anchor="center")  # Center-aligned
        tree.column("Specialization", width=150, anchor="center")  # Center-aligned
        tree.column("Languages", width=150, anchor="center")  # Center-aligned
        tree.column("Mobile No", width=100, anchor="center")  # Center-aligned
        tree.column("Email", width=150, anchor="center")  # Center-aligned
        tree.column("Schedule", width=200, anchor="center")  # Center-aligned

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(staff_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Fetch staff details from the database
        try:
            staff_details = self.hospital.fetch_query('SELECT * FROM staff')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch staff details: {e}")
            return

        # Insert each staff member into the Treeview
        for staff in staff_details:
            tree.insert('', tk.END, values=staff)

        # Pack the Treeview to expand and fill the frame
        tree.pack(fill='both', expand=True)

        # Back button to return to home
        ttk.Button(staff_frame, text="Back to Home", command=self.create_home_frame).pack(pady=20)

    def create_billing_frame(self):
        self.clear_frame()  # Clear the current frame

        # Create the billing frame
        billing_frame = ttk.Frame(self.root, padding=20)
        billing_frame.pack(fill='both', expand=True)

        # Billing form title
        ttk.Label(billing_frame, text="Billing Information", font=("Helvetica", 20, "bold")).pack(pady=10)

        # Patient ID
        ttk.Label(billing_frame, text="Patient ID:", font=("Helvetica", 12)).pack(pady=5)
        self.patient_id_entry = ttk.Entry(billing_frame, font=("Helvetica", 12))
        self.patient_id_entry.pack(pady=5, fill='x')

        # Services Rendered
        ttk.Label(billing_frame, text="Services Rendered:", font=("Helvetica", 12)).pack(pady=5)
        self.services_entry = ttk.Entry(billing_frame, font=("Helvetica", 12))
        self.services_entry.pack(pady=5, fill='x')

        # Total Amount Due
        ttk.Label(billing_frame, text="Total Amount Due:", font=("Helvetica", 12)).pack(pady=5)
        self.amount_entry = ttk.Entry(billing_frame, font=("Helvetica", 12))
        self.amount_entry.pack(pady=5, fill='x')

        # Submit button
        ttk.Button(billing_frame, text="Submit Billing", command=self.submit_billing).pack(pady=10)

        # Back button
        ttk.Button(billing_frame, text="Back to Home", command=self.create_home_frame).pack(pady=20)

    def submit_billing(self):
        # Retrieve data from entries
        patient_id = self.patient_id_entry.get()
        services = self.services_entry.get()
        amount_due = self.amount_entry.get()

        # Validate inputs
        if not patient_id or not services or not amount_due:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            # Attempt to convert amount_due to a float to ensure it’s a valid number
            amount_due = float(amount_due)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount for Total Amount Due.")
            return

        # Calculate taxes
        cst_rate = 0.02  # 2% CST
        gst_rate = 0.18  # 18% GST

        cst = amount_due * cst_rate
        gst = amount_due * gst_rate
        total_amount = amount_due + cst + gst

        # Display receipt
        self.create_receipt_frame(patient_id, services, amount_due, cst, gst, total_amount)

    def create_receipt_frame(self, patient_id, services, amount_due, cst, gst, total_amount):
        self.clear_frame()  # Clear the current frame

        # Create the receipt frame
        receipt_frame = ttk.Frame(self.root, padding=20)
        receipt_frame.pack(fill='both', expand=True)

        # Receipt title
        ttk.Label(receipt_frame, text="Billing Receipt", font=("Helvetica", 20, "bold")).pack(pady=10)

        # Display billing information
        ttk.Label(receipt_frame, text=f"Patient ID: {patient_id}", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(receipt_frame, text=f"Services Rendered: {services}", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(receipt_frame, text=f"Total Amount Due: ${amount_due:.2f}", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(receipt_frame, text=f"CST (2%): ${cst:.2f}", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(receipt_frame, text=f"GST (18%): ${gst:.2f}", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(receipt_frame, text=f"Total Amount Payable: ${total_amount:.2f}", font=("Helvetica", 12, "bold")).pack(pady=10)

        # Back button to return to home
        ttk.Button(receipt_frame, text="Back to Home", command=self.create_home_frame).pack(pady=20)


    def open_new_patient_frame(self):
        # Clear any existing frames
        self.clear_frame()

        # Create a parent frame for centering the registration form
        self.new_patient_window = ttk.Frame(self.root, padding=20)
        self.new_patient_window.pack(pady=20)  # Add vertical padding to center

        # Configure grid layout to center the form
        for i in range(10):  # For 10 rows
            self.new_patient_window.grid_rowconfigure(i, weight=1)
        for j in range(2):  # For 2 columns
            self.new_patient_window.grid_columnconfigure(j, weight=1)

        # Set a background color for the frame and larger font size for labels, entry fields, and buttons
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')  # Light gray background
        style.configure('TLabel', font=("Helvetica", 14))  # Set font size for labels
        style.configure('TEntry', font=("Helvetica", 14))  # Set font size for entry fields
        style.configure('TButton', font=("Helvetica", 14))  # Set font size for buttons
        self.new_patient_window.configure(style='TFrame')

        # Create form title with larger font
        title_label = ttk.Label(self.new_patient_window, text="New Patient Registration", font=("Helvetica", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Patient ID - Display only
        ttk.Label(self.new_patient_window, text="Patient ID (Auto-generated)").grid(row=1, column=0, sticky='w', pady=5)
        self.patient_id_label = ttk.Label(self.new_patient_window, text="(Will be assigned automatically)", font=("Helvetica", 12, "italic"))
        self.patient_id_label.grid(row=1, column=1, sticky='w', pady=5)

        # Name
        ttk.Label(self.new_patient_window, text="Name").grid(row=2, column=0, sticky='w', pady=5)
        self.patient_name_entry = ttk.Entry(self.new_patient_window)
        self.patient_name_entry.grid(row=2, column=1, pady=5)

        # Date of Birth
        ttk.Label(self.new_patient_window, text="Date of Birth (YYYY-MM-DD)").grid(row=3, column=0, sticky='w', pady=5)
        self.patient_dob_entry = ttk.Entry(self.new_patient_window)
        self.patient_dob_entry.grid(row=3, column=1, pady=5)

        # Gender
        ttk.Label(self.new_patient_window, text="Gender").grid(row=4, column=0, sticky='w', pady=5)
        self.patient_gender_var = tk.StringVar()
        ttk.Radiobutton(self.new_patient_window, text="Male", variable=self.patient_gender_var, value="Male").grid(row=4, column=1, sticky='w')
        ttk.Radiobutton(self.new_patient_window, text="Female", variable=self.patient_gender_var, value="Female").grid(row=5, column=1, sticky='w')
        ttk.Radiobutton(self.new_patient_window, text="Other", variable=self.patient_gender_var, value="Other").grid(row=6, column=1, sticky='w')

        # Problem
        ttk.Label(self.new_patient_window, text="Problem").grid(row=7, column=0, sticky='w', pady=5)
        self.patient_problem_entry = ttk.Entry(self.new_patient_window)
        self.patient_problem_entry.grid(row=7, column=1, pady=5)

        # Mobile No.
        ttk.Label(self.new_patient_window, text="Mobile No.").grid(row=8, column=0, sticky='w', pady=5)
        self.patient_mobile_no_entry = ttk.Entry(self.new_patient_window)
        self.patient_mobile_no_entry.grid(row=8, column=1, pady=5)

        # Register button
        ttk.Button(self.new_patient_window, text="Register", command=self.register_patient).grid(row=9, column=0, pady=(10, 0))

        # Back button
        ttk.Button(self.new_patient_window, text="Back to Home", command=self.return_to_home).grid(row=9, column=1, pady=(10, 0))

    def register_patient(self):
        name = self.patient_name_entry.get()
        dob = self.patient_dob_entry.get()
        gender = self.patient_gender_var.get()
        problem = self.patient_problem_entry.get()
        mobile_no = self.patient_mobile_no_entry.get()

        if name and dob and gender and problem and mobile_no:
            # Insert the new patient into the database
            self.hospital.execute_query(
                'INSERT INTO patients (name, dob, gender, problem, mobile_no) VALUES (?, ?, ?, ?, ?)',
                (name, dob, gender, problem, mobile_no)
            )

            # Fetch the last inserted patient ID
            patient_id = self.hospital.fetch_query('SELECT last_insert_rowid()')[0][0]

            messagebox.showinfo("Success", f"Patient registered successfully! Patient ID: {patient_id}")
            self.return_to_home()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    def return_to_home(self):
        self.clear_frame()
        self.create_home_frame()
    def create_appointments_frame(self):
        self.clear_frame()

        # Create a parent frame for centering the appointment form
        self.appointment_frame = ttk.Frame(self.root, padding=20)
        self.appointment_frame.pack(expand=True)

        # Configure grid layout for better alignment
        for i in range(6):  # 6 rows (fields + buttons)
            self.appointment_frame.grid_rowconfigure(i, weight=1)
        for j in range(2):  # 2 columns (label + entry)
            self.appointment_frame.grid_columnconfigure(j, weight=1)

        # Set a background color for the frame
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')  # Light gray background
        self.appointment_frame.configure(style='TFrame')

        # Create form title
        title_label = ttk.Label(self.appointment_frame, text="Book Appointment", font=("Helvetica", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Patient ID
        ttk.Label(self.appointment_frame, text="Patient ID").grid(row=1, column=0, sticky='e', padx=10, pady=5)
        self.appointment_patient_id_entry = ttk.Entry(self.appointment_frame)
        self.appointment_patient_id_entry.grid(row=1, column=1, pady=5)

        # Appointment Date
        ttk.Label(self.appointment_frame, text="Appointment Date (YYYY-MM-DD)").grid(row=2, column=0, sticky='e', padx=10, pady=5)
        self.appointment_date_entry = ttk.Entry(self.appointment_frame)
        self.appointment_date_entry.grid(row=2, column=1, pady=5)

        # Appointment Time
        ttk.Label(self.appointment_frame, text="Appointment Time (HH:MM)").grid(row=3, column=0, sticky='e', padx=10, pady=5)
        self.appointment_time_entry = ttk.Entry(self.appointment_frame)
        self.appointment_time_entry.grid(row=3, column=1, pady=5)

        # Appointment Details
        ttk.Label(self.appointment_frame, text="Details").grid(row=4, column=0, sticky='e', padx=10, pady=5)
        self.appointment_details_entry = ttk.Entry(self.appointment_frame)
        self.appointment_details_entry.grid(row=4, column=1, pady=5)

        # Buttons for actions
        book_button = ttk.Button(self.appointment_frame, text="Book Appointment", command=self.book_appointment)
        book_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Back button
        back_button = ttk.Button(self.appointment_frame, text="Back", command=self.return_to_home)
        back_button.grid(row=6, column=0, columnspan=2, pady=5)

        # Add padding to make the form visually appealing
        for widget in self.appointment_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)


    def book_appointment(self):
        patient_id = self.appointment_patient_id_entry.get()
        date = self.appointment_date_entry.get()
        time = self.appointment_time_entry.get()
        details = self.appointment_details_entry.get()

        if not (patient_id and date and time and details):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            patient_id = int(patient_id)
        except ValueError:
            messagebox.showerror("Error", "Patient ID must be a valid number.")
            return

        # Check if patient ID exists in the database
        patient_exists = self.hospital.fetch_query('SELECT id FROM patients WHERE id = ?', (patient_id,))
        if not patient_exists:
            messagebox.showerror("Error", "Patient ID does not exist.")
            return

        try:
            self.hospital.execute_query(
                'INSERT INTO appointments (patient_id, date, time, details) VALUES (?, ?, ?, ?)', 
                (patient_id, date, time, details)
            )
            messagebox.showinfo("Success", "Appointment booked successfully!")
            self.return_to_home()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
                
    def create_view_appointments_frame(self):
        self.clear_frame()

        # Create a frame for the view appointments section
        self.view_appointments_frame = ttk.Frame(self.root, padding=20)
        self.view_appointments_frame.pack(fill='both', expand=True)

        # Title label with larger font
        ttk.Label(self.view_appointments_frame, text="View Appointments", font=("Helvetica", 20, "bold")).pack(pady=(10, 20))

        # Create a custom style for the Treeview to increase font size
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 14))  # Set font for Treeview rows
        style.configure("Treeview.Heading", font=("Times New Roman", 16, "bold"))  # Set font for Treeview headers

        # Fetch appointments from the database
        appointments = self.hospital.fetch_query('SELECT * FROM appointments')

        # Create a Treeview widget to display the appointments
        tree = ttk.Treeview(self.view_appointments_frame, columns=("ID", "Patient ID", "Date", "Time", "Details"), show='headings')
        
        # Define the headings
        tree.heading("ID", text="ID")
        tree.heading("Patient ID", text="Patient ID")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Details", text="Details")

        # Set column widths and center the text in each column
        tree.column("ID", width=50, anchor="center")
        tree.column("Patient ID", width=100, anchor="center")
        tree.column("Date", width=100, anchor="center")
        tree.column("Time", width=100, anchor="center")
        tree.column("Details", width=200, anchor="center")

        # Insert each appointment into the Treeview
        for appointment in appointments:
            tree.insert('', tk.END, values=appointment)

        # Pack the Treeview and make it expandable
        tree.pack(fill='both', expand=True, pady=(0, 20))

        # Create a separate frame for the Back button
        button_frame = ttk.Frame(self.view_appointments_frame)
        button_frame.pack(fill='x')  # Make sure it stretches horizontally

        # Add the Back button inside the button frame
        back_button = ttk.Button(button_frame, text="Back", command=self.return_to_home)
        back_button.pack(pady=10)  # Add some padding around the button



    def create_cancel_appointments_frame(self):
        self.clear_frame()
        self.cancel_appointments_frame = ttk.Frame(self.root)
        self.cancel_appointments_frame.pack(fill='both', expand=True)

        ttk.Label(self.cancel_appointments_frame, text="Cancel Appointment", font=("Helvetica", 16, "bold")).pack(pady=10)

        ttk.Label(self.cancel_appointments_frame, text="Appointment ID").pack(pady=5)
        self.cancel_appointment_id_entry = ttk.Entry(self.cancel_appointments_frame)
        self.cancel_appointment_id_entry.pack(pady=5)

        ttk.Button(self.cancel_appointments_frame, text="Cancel Appointment", command=self.cancel_appointment).pack(pady=5)
        ttk.Button(self.cancel_appointments_frame, text="Back", command=self.return_to_home).pack(pady=5)

    def cancel_appointment(self):
        appointment_id = self.cancel_appointment_id_entry.get()

        if not appointment_id:
            messagebox.showerror("Error", "Please enter the appointment ID.")
            return

        try:
            appointment_id = int(appointment_id)
        except ValueError:
            messagebox.showerror("Error", "Appointment ID must be a valid number.")
            return

        try:
            self.hospital.execute_query('DELETE FROM appointments WHERE id = ?', (appointment_id,))
            messagebox.showinfo("Success", "Appointment cancelled successfully!")
            self.return_to_home()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def clear_frame(self):
        # Clear all widgets from the current frame
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_view_patients_frame(self):
        self.clear_frame()
        self.view_patients_frame = ttk.Frame(self.root, padding=20)
        self.view_patients_frame.pack(fill='both', expand=True)

        # Label for the title
        ttk.Label(self.view_patients_frame, text="View Patients by ID", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Input for Patient ID
        ttk.Label(self.view_patients_frame, text="Patient ID").pack(pady=5)
        self.view_patient_id_entry = ttk.Entry(self.view_patients_frame)
        self.view_patient_id_entry.pack(pady=5)

        # Button to view patient
        ttk.Button(self.view_patients_frame, text="View Patient", command=self.view_patient).pack(pady=5)
        ttk.Button(self.view_patients_frame, text="Back", command=self.return_to_home).pack(pady=5)

    def view_patient(self):
        patient_id = self.view_patient_id_entry.get()

        if not patient_id:
            messagebox.showerror("Error", "Please enter the patient ID.")
            return

        try:
            patient_id = int(patient_id)
        except ValueError:
            messagebox.showerror("Error", "Patient ID must be a valid number.")
            return

        patient = self.hospital.fetch_query('SELECT * FROM patients WHERE id = ?', (patient_id,))

        if patient:
            self.display_patient_details(patient[0])
        else:
            messagebox.showerror("Error", "Patient not found.")

    def display_patient_details(self, patient_info):
        # Clear existing widgets in the frame
        for widget in self.view_patients_frame.winfo_children():
            widget.destroy()

        # Create a new frame for displaying patient details
        details_frame = ttk.Frame(self.view_patients_frame, padding=20, relief='solid', borderwidth=1)
        details_frame.pack(fill='both', expand=True, padx=50, pady=50)  # Adding padding around the frame

        # Set the background color for the details frame
        details_frame.configure(style='TFrame')

        # Create a label for the header
        ttk.Label(details_frame, text="Patient Details", font=("Helvetica", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Create labels for patient information with increased font size
        ttk.Label(details_frame, text="Patient ID:", font=("Helvetica", 12)).grid(row=1, column=0, sticky='w', pady=5)
        ttk.Label(details_frame, text=patient_info[0], font=("Helvetica", 12)).grid(row=1, column=1, sticky='w', pady=5)

        ttk.Label(details_frame, text="Name:", font=("Helvetica", 12)).grid(row=2, column=0, sticky='w', pady=5)
        ttk.Label(details_frame, text=patient_info[1], font=("Helvetica", 12)).grid(row=2, column=1, sticky='w', pady=5)

        ttk.Label(details_frame, text="Date of Birth:", font=("Helvetica", 12)).grid(row=3, column=0, sticky='w', pady=5)
        ttk.Label(details_frame, text=patient_info[2], font=("Helvetica", 12)).grid(row=3, column=1, sticky='w', pady=5)

        ttk.Label(details_frame, text="Address:", font=("Helvetica", 12)).grid(row=4, column=0, sticky='w', pady=5)
        ttk.Label(details_frame, text=patient_info[3], font=("Helvetica", 12)).grid(row=4, column=1, sticky='w', pady=5)

        ttk.Label(details_frame, text="Contact:", font=("Helvetica", 12)).grid(row=5, column=0, sticky='w', pady=5)
        ttk.Label(details_frame, text=patient_info[4], font=("Helvetica", 12)).grid(row=5, column=1, sticky='w', pady=5)

        # Back button to return to the previous screen
        ttk.Button(details_frame, text="Back", command=self.create_view_patients_frame).grid(row=6, column=0, columnspan=2, pady=(20, 0))


    def create_discharge_patient_frame(self):
        self.clear_frame()
        self.discharge_patient_frame = ttk.Frame(self.root)
        self.discharge_patient_frame.pack(fill='both', expand=True)

        ttk.Label(self.discharge_patient_frame, text="Discharge Patient", font=("Helvetica", 16, "bold")).pack(pady=10)

        ttk.Label(self.discharge_patient_frame, text="Patient ID").pack(pady=5)
        self.discharge_patient_id_entry = ttk.Entry(self.discharge_patient_frame)
        self.discharge_patient_id_entry.pack(pady=5)

        ttk.Button(self.discharge_patient_frame, text="Discharge", command=self.discharge_patient).pack(pady=5)
        ttk.Button(self.discharge_patient_frame, text="Back", command=self.return_to_home).pack(pady=5)

    def discharge_patient(self):
        patient_id = self.discharge_patient_id_entry.get()

        if not patient_id:
            messagebox.showerror("Error", "Please enter the patient ID.")
            return

        try:
            patient_id = int(patient_id)
        except ValueError:
            messagebox.showerror("Error", "Patient ID must be a valid number.")
            return

        try:
            self.hospital.execute_query('DELETE FROM patients WHERE id = ?', (patient_id,))
            messagebox.showinfo("Success", "Patient discharged successfully!")
            self.return_to_home()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def open_new_staff_frame(self):
        # Clear any existing frames
        self.clear_frame()

        # Create a parent frame for centering the registration form
        self.new_staff_window = ttk.Frame(self.root, padding=20)
        self.new_staff_window.pack(pady=20)  # Add vertical padding to center

        # Configure grid layout to center the form
        for i in range(13):  # For 13 rows
            self.new_staff_window.grid_rowconfigure(i, weight=1)
        for j in range(2):  # For 2 columns
            self.new_staff_window.grid_columnconfigure(j, weight=1)

        # Set a background color for the frame
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')  # Light gray background
        style.configure('TLabel', font=("Helvetica", 14))  # Set font size for labels
        style.configure('TEntry', font=("Helvetica", 14))  # Set font size for entry fields
        style.configure('TButton', font=("Helvetica", 14))  # Set font size for buttons
        self.new_staff_window.configure(style='TFrame')

        # Create form title with larger font
        title_label = ttk.Label(self.new_staff_window, text="New Staff Registration", font=("Helvetica", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Staff ID - Display only
        ttk.Label(self.new_staff_window, text="Staff ID (Auto-generated)").grid(row=1, column=0, sticky='w', pady=5)
        self.staff_id_label = ttk.Label(self.new_staff_window, text="(Will be assigned automatically)", font=("Helvetica", 12, "italic"))
        self.staff_id_label.grid(row=1, column=1, sticky='w', pady=5)

        # Name
        ttk.Label(self.new_staff_window, text="Name").grid(row=2, column=0, sticky='w', pady=5)
        self.staff_name_entry = ttk.Entry(self.new_staff_window)
        self.staff_name_entry.grid(row=2, column=1, pady=5)

        # Age
        ttk.Label(self.new_staff_window, text="Age").grid(row=3, column=0, sticky='w', pady=5)
        self.staff_age_entry = ttk.Entry(self.new_staff_window)
        self.staff_age_entry.grid(row=3, column=1, pady=5)

        # Gender
        ttk.Label(self.new_staff_window, text="Gender").grid(row=4, column=0, sticky='w', pady=5)
        self.staff_gender_var = tk.StringVar()
        ttk.Radiobutton(self.new_staff_window, text="Male", variable=self.staff_gender_var, value="Male").grid(row=4, column=1, sticky='w')
        ttk.Radiobutton(self.new_staff_window, text="Female", variable=self.staff_gender_var, value="Female").grid(row=5, column=1, sticky='w')
        ttk.Radiobutton(self.new_staff_window, text="Other", variable=self.staff_gender_var, value="Other").grid(row=6, column=1, sticky='w')

        # Specialization
        ttk.Label(self.new_staff_window, text="Specialization").grid(row=7, column=0, sticky='w', pady=5)
        self.staff_specialization_entry = ttk.Entry(self.new_staff_window)
        self.staff_specialization_entry.grid(row=7, column=1, pady=5)

        # Languages Spoken
        ttk.Label(self.new_staff_window, text="Languages Spoken").grid(row=8, column=0, sticky='w', pady=5)
        self.staff_languages_entry = ttk.Entry(self.new_staff_window)
        self.staff_languages_entry.grid(row=8, column=1, pady=5)

        # Mobile No.
        ttk.Label(self.new_staff_window, text="Mobile No.").grid(row=9, column=0, sticky='w', pady=5)
        self.staff_mobile_no_entry = ttk.Entry(self.new_staff_window)
        self.staff_mobile_no_entry.grid(row=9, column=1, pady=5)

        # Email
        ttk.Label(self.new_staff_window, text="Email").grid(row=10, column=0, sticky='w', pady=5)
        self.staff_email_entry = ttk.Entry(self.new_staff_window)
        self.staff_email_entry.grid(row=10, column=1, pady=5)

        # Schedule
        ttk.Label(self.new_staff_window, text="Schedule").grid(row=11, column=0, sticky='w', pady=5)
        self.staff_schedule_entry = ttk.Entry(self.new_staff_window)  # Corrected variable
        self.staff_schedule_entry.grid(row=11, column=1, pady=5)

        # Register button
        ttk.Button(self.new_staff_window, text="Register", command=self.register_staff).grid(row=12, column=0, pady=(10, 0))

        # Back button
        ttk.Button(self.new_staff_window, text="Back to Home", command=self.return_to_home).grid(row=12, column=1, pady=(10, 0))

    def register_staff(self):
        name = self.staff_name_entry.get()
        age = self.staff_age_entry.get()
        gender = self.staff_gender_var.get()
        specialization = self.staff_specialization_entry.get()
        languages = self.staff_languages_entry.get()
        mobile_no = self.staff_mobile_no_entry.get()
        email = self.staff_email_entry.get()
        schedule = self.staff_schedule_entry.get() # Assuming you've captured the schedule data

        if name and age and gender and specialization and languages and mobile_no and email and schedule:
            # Insert the new staff member into the database
            self.hospital.execute_query(
                'INSERT INTO staff (name, age, gender, specialization, languages_spoken, mobile_no, email, schedule) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (name, age, gender, specialization, languages, mobile_no, email, schedule)
            )

            # Fetch the last inserted staff ID
            staff_id = self.hospital.fetch_query('SELECT last_insert_rowid()')[0][0]

            messagebox.showinfo("Success", f"Staff registered successfully! Staff ID: {staff_id}")
            self.return_to_home()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()

