import customtkinter as ctk

ctk.set_appearance_mode("dark")   # "light" | "dark"
ctk.set_default_color_theme("green")

ALLOWED_GRADES = [1, 1.3, 1.7, 2, 2.3, 2.7, 3, 3.3, 3.7, 4, 5]


def snap(x: float) -> float:
    return round(x * 4) / 4


def calc_better(better: float, points: float) -> float:
    threshold = 100 - (better - 1) * 50 / 3
    missing = max(0, threshold - points)
    return snap(missing)


def calc_worse(worse: float, points: float) -> float:
    threshold = 100 - (worse - 1) * 50 / 3
    buffer_ = max(0, points - threshold)
    return snap(buffer_)


def grade(points: float) -> dict:
    result = 1 + 3 * (100 - points) / 50
    closest = min(ALLOWED_GRADES, key=lambda x: abs(x - result))

    idx = ALLOWED_GRADES.index(closest)
    better = ALLOWED_GRADES[idx - 1] if idx > 0 else None
    worse = ALLOWED_GRADES[idx + 1] if idx < len(ALLOWED_GRADES) - 1 else None

    data = {"closest": closest, "result": result, "missing": None, "buffer": None}

    if better is not None:
        data["missing"] = calc_better(better, points)
    if worse is not None:
        data["buffer"] = calc_worse(worse, points)

    return data


class GradeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Grade Calculator")
        self.geometry("520x560")
        self.minsize(520, 560)

        # ===== Root grid (pro layout) =====
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # ===== Header =====
        header = ctk.CTkFrame(self, corner_radius=18)
        header.grid(row=0, column=0, padx=20, pady=(20, 12), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            header, text="Grade Calculator", font=("Arial", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=18, pady=(14, 4), sticky="w")

        self.subtitle = ctk.CTkLabel(
            header,
            text="Overall grade (Seminar+Test) or convert a test score to /50.",
            font=("Arial", 13),
            text_color="gray70",
        )
        self.subtitle.grid(row=1, column=0, padx=18, pady=(0, 14), sticky="w")

        # ===== Mode selector =====
        self.mode = ctk.StringVar(value="overall")
        self.mode_selector = ctk.CTkSegmentedButton(
            self,
            values=["overall", "test"],
            variable=self.mode,
            command=self.switch_mode,
        )
        self.mode_selector.grid(row=1, column=0, padx=20, pady=(0, 12), sticky="ew")

        # ===== Content (2 cards) =====
        content = ctk.CTkFrame(self, corner_radius=18)
        content.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        # ----- Input card -----
        self.input_card = ctk.CTkFrame(content, corner_radius=18)
        self.input_card.grid(row=0, column=0, padx=(14, 7), pady=14, sticky="nsew")
        self.input_card.grid_columnconfigure(0, weight=1)

        self.input_title = ctk.CTkLabel(
            self.input_card, text="Inputs", font=("Arial", 16, "bold")
        )
        self.input_title.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")

        # Two separate frames so the button never jumps
        self.overall_frame = ctk.CTkFrame(self.input_card, fg_color="transparent")
        self.overall_frame.grid(row=1, column=0, padx=16, pady=(0, 0), sticky="ew")
        self.overall_frame.grid_columnconfigure(0, weight=1)

        self.test_frame = ctk.CTkFrame(self.input_card, fg_color="transparent")
        self.test_frame.grid(row=1, column=0, padx=16, pady=(0, 0), sticky="ew")
        self.test_frame.grid_columnconfigure(0, weight=1)

        # Overall inputs
        self.seminar_entry = ctk.CTkEntry(
            self.overall_frame, placeholder_text="Seminar points (0–50)"
        )
        self.seminar_entry.grid(row=0, column=0, pady=(0, 10), sticky="ew")

        self.test_entry = ctk.CTkEntry(
            self.overall_frame, placeholder_text="Test points (0–50)"
        )
        self.test_entry.grid(row=1, column=0, pady=(0, 6), sticky="ew")

        self.overall_hint = ctk.CTkLabel(
            self.overall_frame,
            text="Tip: convert your raw test score in the “test” tab first.",
            font=("Arial", 12),
            text_color="gray70",
        )
        self.overall_hint.grid(row=2, column=0, pady=(0, 4), sticky="w")

        # Test conversion inputs
        self.question_entry = ctk.CTkEntry(
            self.test_frame, placeholder_text="Number of questions (e.g. 80)"
        )
        self.question_entry.grid(row=0, column=0, pady=(0, 10), sticky="ew")

        self.points_entry = ctk.CTkEntry(
            self.test_frame, placeholder_text="Points in test (e.g. 56.25)"
        )
        self.points_entry.grid(row=1, column=0, pady=(0, 6), sticky="ew")

        self.test_hint = ctk.CTkLabel(
            self.test_frame,
            text="Result will be converted to /50 in 0.25 steps.",
            font=("Arial", 12),
            text_color="gray70",
        )
        self.test_hint.grid(row=2, column=0, pady=(0, 4), sticky="w")

        # Action row (button + live toggle)
        self.action_row = ctk.CTkFrame(self.input_card, fg_color="transparent")
        self.action_row.grid(row=2, column=0, padx=16, pady=(14, 16), sticky="ew")
        self.action_row.grid_columnconfigure(0, weight=1)

        self.calc_button = ctk.CTkButton(
            self.action_row, text="Calculate", command=self.calculate
        )
        self.calc_button.grid(row=0, column=0, sticky="ew")

        self.live_var = ctk.BooleanVar(value=True)
        self.live_switch = ctk.CTkSwitch(
            self.action_row,
            text="Live update",
            variable=self.live_var,
            onvalue=True,
            offvalue=False,
            command=self._apply_live_bindings,
        )
        self.live_switch.grid(row=1, column=0, pady=(10, 0), sticky="w")

        # ----- Result card -----
        self.result_card = ctk.CTkFrame(content, corner_radius=18)
        self.result_card.grid(row=0, column=1, padx=(7, 14), pady=14, sticky="nsew")
        self.result_card.grid_columnconfigure(0, weight=1)

        self.result_title = ctk.CTkLabel(
            self.result_card, text="Result", font=("Arial", 16, "bold")
        )
        self.result_title.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")

        self.output_label = ctk.CTkLabel(
            self.result_card,
            text="Choose a mode and enter values.",
            justify="left",
            font=("Arial", 14),
            anchor="w",
        )
        self.output_label.grid(row=1, column=0, padx=16, pady=(0, 8), sticky="ew")

        self.output_small = ctk.CTkLabel(
            self.result_card,
            text="",
            justify="left",
            font=("Arial", 12),
            text_color="gray70",
            anchor="w",
        )
        self.output_small.grid(row=2, column=0, padx=16, pady=(0, 16), sticky="ew")

        # Default: overall mode visible
        self.test_frame.grid_remove()

        # Optional: remember last converted test value
        self.last_converted_test = None

        # Live update bindings
        self._apply_live_bindings()

    # ===== UI behavior =====
    def _bind_entries(self, widget_list, bind: bool):
        for w in widget_list:
            if bind:
                w.bind("<KeyRelease>", self._on_key_release)
            else:
                w.unbind("<KeyRelease>")

    def _apply_live_bindings(self):
        live = bool(self.live_var.get())
        self._bind_entries(
            [self.seminar_entry, self.test_entry, self.question_entry, self.points_entry],
            bind=live,
        )
        if live:
            self.calculate()

    def _on_key_release(self, _event):
        if self.live_var.get():
            self.calculate()

    def switch_mode(self, value):
        # Clear output
        self.output_label.configure(text="")
        self.output_small.configure(text="")

        if value == "test":
            self.overall_frame.grid_remove()
            self.test_frame.grid()
        else:
            self.test_frame.grid_remove()
            self.overall_frame.grid()

            # convenience: if user previously converted test, prefill
            if self.last_converted_test is not None and not self.test_entry.get().strip():
                self.test_entry.insert(0, f"{self.last_converted_test}")

        self.calculate()

    # ===== Core actions =====
    def calculate(self):
        try:
            mode = self.mode.get().strip().lower()

            if mode == "overall":
                seminar_s = self.seminar_entry.get().strip()
                test_s = self.test_entry.get().strip()

                if not seminar_s or not test_s:
                    self.output_label.configure(text="Enter Seminar and Test points.")
                    self.output_small.configure(text="")
                    return

                seminar = float(seminar_s)
                test = float(test_s)

                if not (0 <= seminar <= 50) or not (0 <= test <= 50):
                    self.output_label.configure(text="Values must be within 0–50.")
                    self.output_small.configure(text="")
                    return

                points = seminar + test
                data = grade(points)

                text = (
                    f"Grade: {data['closest']}\n"
                    f"Calculated: {data['result']:.3f}\n"
                    f"Total points: {points:.2f} / 100"
                )

                details = []
                if data["missing"] is not None:
                    details.append(f"To better grade: +{data['missing']} points")
                if data["buffer"] is not None:
                    details.append(f"Buffer to worse: {data['buffer']} points")

                self.output_label.configure(text=text)
                self.output_small.configure(text=" • ".join(details))

            else:  # test mode: convert raw test score -> /50
                qst_s = self.question_entry.get().strip()
                poi_s = self.points_entry.get().strip()

                if not qst_s or not poi_s:
                    self.output_label.configure(text="Enter questions and points.")
                    self.output_small.configure(text="")
                    return

                qst = float(qst_s)
                poi = float(poi_s)

                if qst <= 0:
                    self.output_label.configure(text="Questions must be > 0.")
                    self.output_small.configure(text="")
                    return
                if poi < 0:
                    self.output_label.configure(text="Points must be ≥ 0.")
                    self.output_small.configure(text="")
                    return

                converted = snap(poi * (50 / qst))
                self.last_converted_test = converted

                self.output_label.configure(
                    text=f"Converted Test Points: {converted:.2f} / 50"
                )
                self.output_small.configure(text="Tip: switch to “overall” to use this value.")

        except ValueError:
            self.output_label.configure(text="Please enter valid numbers.")
            self.output_small.configure(text="")


if __name__ == "__main__":
    app = GradeApp()
    app.mainloop()
