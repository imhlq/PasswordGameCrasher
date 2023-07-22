from ephem import Moon
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
import pickle, os

import tables

console = Console()

class Password:
    Month = "June"
    Sponsor = "Starbucks"
    Specials = "."
    Romans = "XXXV"
    LeapYear = 0
    Captcha = ""
    Wordle = ""
    Country = ""
    Bestmove = ""
    MoonEmoji = ""
    AtomElement = "He"
    Affirmations = ""
    isHatchPaul = False
    isFeedPaul = False
    isRule21Strong = False
    isBoldVowels = True
    isPrimeNeeded = False

    CurrProgress = 0

    def boldVowel(self, strings):
        vowel = ['a', 'e', 'i', 'o', 'u']
        for char in vowel:
            new = strings.replace(char, "<b>" + char + "</b>")
        return new
    
    def makeup(self, bold=False):
        strongs = tables.Rule21Strong if self.isRule21Strong else ""
        eggs = tables.EggPaul if self.isHatchPaul else ""
        # Make up
        password = f"{eggs}{self.Month}{self.Sponsor}{self.Specials}{self.LeapYear}{self.MoonEmoji}{self.Romans}"
        password += f"{self.Captcha}{self.Wordle}{self.Country}{self.AtomElement}{self.Bestmove}{strongs}"
        password += f"{self.Affirmations}"
        if bold: password = self.boldVowel(password)
        return password

    def __str__(self):
        return self.makeup()

class PasswordSolver:
    CurrPwd = None

    def get_moon_phase(self, phase):
        index = round(phase * (len(tables.moon_phases) - 1))
        return tables.moon_phases[index]

    def __init__(self):
        if os.path.exists("progs.pkl"):
            
            cmd = console.input("Load progess(Y/n)?")
            if cmd != 'n':
                with open("progs.pkl", 'rb') as fp:
                    self.CurrPwd = pickle.load(fp)
                return
            
        self.CurrPwd = Password()
        now = datetime.now()

        # Get Moon Phase Emoji
        moon = Moon()
        moon.compute(now)
        phase = moon.moon_phase
        self.CurrPwd.MoonEmoji = self.get_moon_phase(phase)
        self.CurrPwd.LeapYear = self.solveLeapYear()


    def showHelperMsg(self, rule):
        console.print(f"Rule {rule}: {tables.rules_info[rule]}", style="yellow")

    def showPressContinue(self):
        console.input("Press to continue...")
        console.clear()

    def solveLeapYear(self):
        fsum = 25
        self.CurrPwd.LeapYear = 0
        for char in self.CurrPwd.makeup():
            if char.isdigit():
                fsum -= int(char)
        
        # Finds the next leap year, from the starting_year, for which the sum of its digits equals to fsum.
        starting_year = 0
        for year in range(starting_year, starting_year + 10000):
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                if sum(int(digit) for digit in str(year)) == fsum:
                    self.CurrPwd.LeapYear = year
                    return year

        print("Leap year not found!")
        return None

    def solveAtomicNumber(self):
        atom_sum = 200
        self.CurrPwd.AtomElement = ""
        pwd = self.CurrPwd.makeup(bold=False)

        for k, v in tables.periodic_table.items():
            atom_sum -= k * pwd.count(v)
            if pwd.count(v) > 0:
                print("Atomic:", v, pwd.count(v))
        assert atom_sum >= 0
        console.print(f"[red]Sum of Your Atomic Number should be {atom_sum}")
        
        avoid_chars = ["L", "X", 'M', "V", "I"]
        for j in range(atom_sum+1):
            skip_a = False
            i = atom_sum - j
            ci = tables.periodic_table[i]
            cj = tables.periodic_table[j] if j != 0 else ""
            for c in avoid_chars:
                # Break if avoid char appears
                if c.lower() in ci.lower() + cj.lower(): 
                    skip_a = True
                    break

            # when success
            if not skip_a:
                if len(ci) == 2 or len(cj) == 2:
                    self.CurrPwd.AtomElement = ci + cj
                    return True
        console.print("Good elements were not found!")


    def showPassword(self):
        Passwd = self.CurrPwd.makeup()
        PwdPanel = Panel(Passwd)
        console.print(PwdPanel, style="black")
        self.showPressContinue()
        # clipboard.copy(Passwd)
        # console.print("! [gray]Password is copied[/gray]")

    def progress(self):
        current_progress = self.CurrPwd.CurrProgress

        while True:

            if current_progress <= 9:
                # Get Initial Message
                console.print("[blue]Step 1. Initial Password[/blue]")
                console.print("Please select and copy next line:")
                self.showPassword()
                current_progress = 10

            elif current_progress == 10:
                # Get Captcha
                console.print("[blue]Step 2. CAPTCHA[/blue]")
                self.showHelperMsg(10)
                console.print("Please input CAPTCHA here")
                while True:
                    captcha = console.input("CAPTCHA>")
                    if 4 <= len(captcha) <= 6:
                        self.CurrPwd.Captcha = captcha
                        break
                self.CurrPwd.LeapYear = self.solveLeapYear()
                self.showPassword()
                current_progress = 11

            elif current_progress == 11:
                # Get Wordle
                console.print("[blue]Step 3. Wordle[/blue]")
                self.showHelperMsg(11)
                console.print("Please input Wordle here")
                while True:
                    wordle = console.input("Wordle>")
                    if len(captcha) == 5:
                        self.CurrPwd.Wordle = wordle
                        break
                self.showPassword()
                # Rule 12, two letter of periodic table
                current_progress = 14
            
            elif current_progress == 14:
                console.print("[blue]Step 4. Country[/blue]")
                self.showHelperMsg(14)
                console.print("Please input Country name here")
                while True:
                    country = console.input("Country>")
                    if len(country) > 1:
                        self.CurrPwd.Country = country
                        break
                self.showPassword()
                current_progress = 16

            elif current_progress == 16:
                console.print("[blue]Step 5. Chess[/blue]")
                self.showHelperMsg(16)
                console.print("Please input best move here")
                while True:
                    best_move = console.input("Move>")
                    if len(best_move) > 1:
                        self.CurrPwd.Bestmove = best_move
                        break
                self.solveLeapYear()
                self.showPassword()
                current_progress = 17

            elif current_progress == 17:
                console.print("[blue]Step 6. Egg[/blue]")
                self.showHelperMsg(17)
                self.CurrPwd.isHatchPaul = True
                self.solveAtomicNumber()
                console.print("[red]Prepare to fire![/red]")
                self.showPassword()
                current_progress = 20
            
            elif current_progress == 20:
                console.print("[blue]Step 7. Fire[/blue]")
                self.showHelperMsg(20)
                console.print("No worries, here is your password:")
                self.CurrPwd.isRule21Strong = True
                self.CurrPwd.Affirmations = "I am loved"
                self.solveAtomicNumber()
                self.showPassword()
                current_progress = 23
            
            elif current_progress == 23:
                console.print("[blue]Step 8. Feed[/blue]")
                self.showHelperMsg(23)
                self.CurrPwd.isFeedPaul = True
                self.showPassword()
                current_progress = 24

            # finally
            with open("progs.pkl", 'wb') as fp:
                pickle.dump(self.CurrPwd, fp)
            self.CurrPwd.CurrProgress = current_progress



password = "3JanuaryStarbucksVIIVc86mdBurly🌒️Japan🥚0Qd8+🏋️‍♂️🏋️‍♂️🏋️‍♂️I am loved"

solver = PasswordSolver()
solver.progress()