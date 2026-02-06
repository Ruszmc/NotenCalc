import customtkinter as ctk

ctk.set_appearance_mode("dark")   # "light" | "dark"
ctk.set_default_color_theme("blue")


def ask():
    selection = input('Do you want to calculate your Note for the test or overall? \n').lower().strip()
    print('')

    if selection == 'overall':
        overall()
    elif selection == 'test':
        test()
    else:
        ask()

def overall(test_result=None):

    # --- Get the values ---#
    if test_result is not None:
        test = float(test_result)
        print('Your Test result was: ' + str(test_result))
    else:
        test = float(input('How many points did you get in the Test \n'))

    seminar = float(input('How many points did you get in the Seminar \n'))

    # --- check the conversion, if "true" add your total points together---#
    if test > 50:
        return
    ue_test = seminar + test

    grade(ue_test)

def test():
    # --- Get the values ---#
    qst = input('How many questions did the test have? \n')
    poi = input('How many points did you get in the Test? \n')

    # --- convert to floats---#
    poi = float(poi)
    qst = float(qst)

    # --- calculate result ---#
    fac = 50 / qst
    result = poi * fac

    # --- use the right, number ---#
    result = round(result * 4) / 4
    print(result)

    ans = input('Do you also want to calculate your overall score? (y/n)\n').lower()
    if ans == 'y':
        overall(result)
    else:
        print('Thank you for using this Programm! \n')

def snap(x):
    return round(x*4) /4

def grade(points):
    allowed_grades = [1, 1.3, 1.7, 2, 2.3, 2.7, 3, 3.3, 3.7, 4, 5]
    result = 1 + 3 * (100 - points) / 50
    closest = min(allowed_grades, key=lambda x: abs(x - result))

    index = allowed_grades.index(closest)

    better = allowed_grades[index - 1] if index > 0 else None
    worse = allowed_grades[index + 1] if index < len(allowed_grades) - 1 else None

    data = {
        "closest": closest,
        "result": result,
        "missing": None,
        "buffer": None
    }

    if better:
        data['missing']= calc_better(better, points)
    if worse:
        data['buffer']= calc_worse(worse, points)

    return data


def calc_better(better, points):
    better_threshold = 100 - (better - 1) * 50 / 3
    missing = max(0, better_threshold - points)
    return snap(missing)

def calc_worse(worse, points):
    worse_threshold = 100 - (worse - 1) * 50 / 3
    buffer = max(0, points - worse_threshold)
    return snap(buffer)


class GradeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Grade Calculator")
        self.geometry("420x420")

        # Main container
        self.main = ctk.CTkFrame(self, corner_radius=15)
        self.main.pack(padx=20, pady=20, expand=True, fill="both")

        # Title
        self.title_label = ctk.CTkLabel(
            self.main,
            text="Grade Calculator",
            font=("Arial", 22, "bold")
        )
        self.title_label.pack(pady=(20, 10))

        # Seminar input
        self.input_frame = ctk.CTkFrame(self.main)
        self.input_frame.pack(padx=20, pady=10, fill="x")

        self.seminar_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Seminar points (0-50)"
        )
        self.seminar_entry.pack(padx=10, pady=10)

        self.test_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Test points (0-50)"
        )
        self.test_entry.pack(padx=10, pady=10)

        self.calc_button = ctk.CTkButton(
            self.input_frame,
            text="Calculate",
            command=self.calculate
        )
        self.calc_button.pack(pady=15)

        # Result Card
        self.result_frame = ctk.CTkFrame(self.main)
        self.result_frame.pack(padx=20, pady=10, fill="x")

        self.output_label = ctk.CTkLabel(
            self.result_frame,
            text="",
            justify="left",
            font=("Arial", 14)
        )
        self.output_label.pack(pady=15)

    def calculate(self):
        try:
            seminar = float(self.seminar_entry.get())
            test = float(self.test_entry.get())
            points = seminar + test

            data = grade(points)

            data = grade(points)

            text = f"Grade: {data['closest']}\n"
            text += f"Calculated: {data['result']:.3f}\n"

            if data["missing"] is not None:
                text += f"\nPoints to better grade: {data['missing']}"

            if data["buffer"] is not None:
                text += f"\nPoints until worse grade: {data['buffer']}"

            self.output_label.configure(text=text)


        except ValueError:
            self.output_label.configure(
                text="Please enter valid numbers."
            )


if __name__ == "__main__":
    app = GradeApp()
    app.mainloop()
