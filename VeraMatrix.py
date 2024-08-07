import os
import random
import sqlite3
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Ensure MatrixSim directory exists
base_dir = "MatrixSim"
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# Create subdirectories for planets, countries, and states
def create_directories():
    planet_dir = os.path.join(base_dir, "EarthData")
    os.makedirs(planet_dir, exist_ok=True)
    
    usa_dir = os.path.join(planet_dir, "USAData")
    china_dir = os.path.join(planet_dir, "ChinaData")
    russia_dir = os.path.join(planet_dir, "RussiaData")
    os.makedirs(usa_dir, exist_ok=True)
    os.makedirs(china_dir, exist_ok=True)
    os.makedirs(russia_dir, exist_ok=True)
    
    os.makedirs(os.path.join(usa_dir, "CaliforniaData"), exist_ok=True)
    os.makedirs(os.path.join(usa_dir, "NewYorkData"), exist_ok=True)
    os.makedirs(os.path.join(china_dir, "BeijingData"), exist_ok=True)
    os.makedirs(os.path.join(china_dir, "ShanghaiData"), exist_ok=True)
    os.makedirs(os.path.join(russia_dir, "MoscowData"), exist_ok=True)
    os.makedirs(os.path.join(russia_dir, "SaintPetersburgData"), exist_ok=True)

    # Ensure DeathRate directory exists
    death_rate_dir = os.path.join(base_dir, "DeathRate")
    os.makedirs(death_rate_dir, exist_ok=True)

    # Ensure BirthRate directory exists
    birth_rate_db = os.path.join(base_dir, "BirthRateData")
    os.makedirs(birth_rate_db, exist_ok=True)

    # Ensure EconomyData directory exists
    economy_data_dir = os.path.join(base_dir, "EconomyData")
    os.makedirs(economy_data_dir, exist_ok=True)

create_directories()

# Create or connect to the birth rate database
birth_rate_db = os.path.join(base_dir, "BirthRateData", "birth_rate_log.sqlite")
conn = sqlite3.connect(birth_rate_db)
cursor = conn.cursor()

# Create the BirthRate table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS BirthRate (
        year INTEGER,
        population INTEGER,
        births INTEGER
    )
''')
conn.commit()
conn.close()

# Setup DeathRate database
def setup_death_rate_db():
    death_rate_db = os.path.join(base_dir, "DeathRate", "DeathRateLog.sqlite")
    conn = sqlite3.connect(death_rate_db)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DeathRate (
            year INTEGER,
            population INTEGER,
            deaths INTEGER
        )
    ''')
    conn.commit()
    conn.close()

setup_death_rate_db()

# Setup EconomyData database
def setup_economy_data_db():
    economy_data_db = os.path.join(base_dir, "EconomyData", "EconomyDataLogs.sqlite")
    conn = sqlite3.connect(economy_data_db)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS EconomyData (
            year INTEGER,
            total_money REAL,
            average_money REAL,
            economic_events TEXT
        )
    ''')
    conn.commit()
    conn.close()

setup_economy_data_db()

class NPC:
    def __init__(self, name, age, country, state):
        self.name = name
        self.age = age
        self.alive = True
        self.money = 1000  # Start with some money
        self.health = random.uniform(50, 100)  # Health between 50 and 100
        self.intelligence = random.uniform(80, 120)  # IQ between 80 and 120
        self.skills = {'work': random.uniform(0, 100), 'social': random.uniform(0, 100), 'survival': random.uniform(0, 100)}  # Skills
        self.personality = self.generate_personality()
        self.mood = "Neutral"
        self.family = []
        self.country = country
        self.state = state
        self.stress_level = random.uniform(0, 100)
        self.thoughts = ""
        self.self_awareness = False
        self.db = self.get_db_path()
        self.setup_database()

    def get_db_path(self):
        path_mapping = {
            "USA": "EarthData/USAData",
            "China": "EarthData/ChinaData",
            "Russia": "EarthData/RussiaData"
        }
        state_mapping = {
            "California": "CaliforniaData",
            "New York": "NewYorkData",
            "Beijing": "BeijingData",
            "Shanghai": "ShanghaiData",
            "Moscow": "MoscowData",
            "Saint Petersburg": "SaintPetersburgData"
        }
        base_path = os.path.join(base_dir, path_mapping[self.country], state_mapping[self.state])
        return os.path.join(base_path, f"{self.name.lower().replace(' ', '_')}_db.sqlite")

    def generate_personality(self):
        traits = ["Friendly", "Aggressive", "Lazy", "Industrious", "Curious", "Cautious"]
        return random.choice(traits)

    def setup_database(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS LifeEvents (
                date TEXT,
                event TEXT,
                consequences TEXT,
                choice_quality TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Finances (
                date TEXT,
                money REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Family (
                name TEXT,
                relation TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Status (
                date TEXT,
                health REAL,
                intelligence REAL,
                work_skill REAL,
                social_skill REAL,
                survival_skill REAL,
                stress_level REAL,
                thoughts TEXT,
                location TEXT,
                time_of_day TEXT,
                self_awareness INTEGER,
                mood TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def log_event(self, event, consequences="", choice_quality="Neutral"):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO LifeEvents (date, event, consequences, choice_quality) VALUES (?, ?, ?, ?)',
                       (datetime.now().strftime('%Y-%m-%d'), event, consequences, choice_quality))
        conn.commit()
        conn.close()

    def log_death(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO LifeEvents (date, event, consequences, choice_quality) VALUES (?, ?, ?, ?)',
                       (datetime.now().strftime('%Y-%m-%d'), "Died", "", "Neutral"))
        conn.commit()
        conn.close()

    def update_finances(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Finances (date, money) VALUES (?, ?)',
                       (datetime.now().strftime('%Y-%m-%d'), self.money))
        conn.commit()
        conn.close()

    def update_status(self, location, time_of_day):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Status (date, health, intelligence, work_skill, social_skill, survival_skill, stress_level, thoughts, location, time_of_day, self_awareness, mood)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (datetime.now().strftime('%Y-%m-%d'), self.health, self.intelligence, self.skills['work'], self.skills['social'], self.skills['survival'], self.stress_level, self.thoughts, location, time_of_day, int(self.self_awareness), self.mood))
        conn.commit()
        conn.close()

    def add_family_member(self, name, relation):
        self.family.append((name, relation))
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Family (name, relation) VALUES (?, ?)', (name, relation))
        conn.commit()
        conn.close()

    def classify_choice(self, event):
        good_choices = ["Found money", "Got a job", "Met someone"]
        bad_choices = ["Lost money", "Lost a job"]
        if event in good_choices:
            return "Good"
        elif event in bad_choices:
            return "Bad"
        else:
            return "Neutral"

    def check_self_awareness(self):
        if not self.self_awareness and random.random() < 0.001:  # Small chance of becoming self-aware each day
            self.self_awareness = True
            self.thoughts = "I think I might be in a simulation."
            self.log_event("Became self-aware", "Realized they are in a simulation", "Neutral")

    def live_day(self):
        if self.alive:
            self.age += 1 / 365  # Increment age by 1 day
            self.money += random.uniform(-10, 10)  # Random daily money change
            self.stress_level += random.uniform(-5, 5)  # Random daily stress change
            self.stress_level = max(0, min(self.stress_level, 100))  # Keep stress level within 0-100
            
            # Health degradation with age
            self.health -= 0.01  # Small daily health decrease
            self.check_self_awareness()  # Check for self-awareness
            self.thoughts = self.generate_thoughts()  # Update thoughts
            self.update_finances()
            self.update_status(f"{self.state}, {self.country}", self.simulation_time())

            if random.random() < 0.0001:  # Very small chance of dying each day
                self.alive = False
                self.log_death()
                print(f"{self.name} has died at the age of {self.age:.2f}")

            # Random daily events
            if random.random() < 0.05:
                event = random.choice(["Found money", "Lost money", "Got a job", "Lost a job", "Met someone", "Traveled", "Fell ill", "Improved skill", "Got educated"])
                consequences = ""
                if event == "Found money":
                    amount = random.uniform(50, 200)
                    self.money += amount
                    consequences = f"Gained {amount:.2f} money"
                elif event == "Lost money":
                    amount = random.uniform(50, 200)
                    self.money -= amount
                    consequences = f"Lost {amount:.2f} money"
                elif event == "Got a job":
                    consequences = "Started a new job"
                    self.skills['work'] += random.uniform(0, 5)  # Improve work skill
                elif event == "Lost a job":
                    consequences = "Lost the job"
                elif event == "Met someone":
                    new_family_member = f"Person_{random.randint(1, 100)}"
                    relation = random.choice(["Friend", "Colleague", "Neighbor"])
                    self.add_family_member(new_family_member, relation)
                    consequences = f"Met {new_family_member}, became {relation}"
                elif event == "Traveled":
                    new_country = random.choice(["USA", "China", "Russia", "Germany", "France"])
                    self.country = new_country
                    consequences = f"Traveled to {new_country}"
                elif event == "Fell ill":
                    self.health -= random.uniform(5, 15)  # Decrease health
                    consequences = "Fell ill"
                elif event == "Improved skill":
                    skill = random.choice(["work", "social", "survival"])
                    self.skills[skill] += random.uniform(1, 5)  # Improve a random skill
                    consequences = f"Improved {skill} skill"
                elif event == "Got educated":
                    self.intelligence += random.uniform(1, 5)  # Increase intelligence
                    consequences = "Gained education"

                choice_quality = self.classify_choice(event)
                self.log_event(event, consequences, choice_quality)

    def generate_thoughts(self):
        if self.self_awareness:
            return "I think I might be in a simulation."
        thoughts_list = [
            "Thinking about work.", "Worrying about money.", "Missing family.",
            "Planning a vacation.", "Feeling stressed.", "Happy about a new opportunity.",
            "Concerned about health.", "Excited about the future.", "Reflecting on the past.",
            "Wondering about the meaning of life."
        ]
        return random.choice(thoughts_list)

    def simulation_time(self):
        current_hour = self.age % 1 * 24
        return f"{int(current_hour)}:{int((current_hour % 1) * 60):02d}"

    def __str__(self):
        return (f"{self.name}, Age: {self.age:.2f}, Alive: {self.alive}, Money: {self.money:.2f}, "
                f"Personality: {self.personality}, Health: {self.health:.2f}, Intelligence: {self.intelligence:.2f}, "
                f"Skills: {self.skills}, Country: {self.country}, State: {self.state}, "
                f"Stress Level: {self.stress_level:.2f}, Thoughts: {self.thoughts}, "
                f"Self-Aware: {self.self_awareness}, Mood: {self.mood}, Location: {self.state}, {self.country}, Time: {self.simulation_time()}")

class State:
    def __init__(self, name):
        self.name = name

class Country:
    def __init__(self, name):
        self.name = name
        self.states = []

    def add_state(self, state):
        self.states.append(state)

class Planet:
    def __init__(self, name):
        self.name = name
        self.countries = []

    def add_country(self, country):
        self.countries.append(country)

class Technology:
    def __init__(self, name):
        self.name = name
        self.discovery_date = None

    def discover(self, date):
        self.discovery_date = date
        print(f"Technology '{self.name}' discovered on {date}.")

class Universe:
    def __init__(self):
        self.planets = []
        self.npcs = []
        self.current_time = datetime.now() - timedelta(days=random.randint(0, 3650))  # Start up to 10 years in the past
        self.start_date = self.current_time
        self.population = 0
        self.technologies = []
        self.population_over_time = []  # Track population changes over time
        self.births_today = 0
        self.deaths_today = 0
        self.total_money = 0
        self.economic_events = []

    def add_planet(self, planet):
        self.planets.append(planet)

    def add_npc(self, npc):
        self.npcs.append(npc)
        self.population += 1
        self.total_money += npc.money

    def remove_npc(self, npc):
        self.npcs.remove(npc)
        self.population -= 1
        self.total_money -= npc.money

    def add_technology(self, tech):
        self.technologies.append(tech)

    def check_technology_discovery(self):
        for tech in self.technologies:
            if tech.discovery_date is None and random.random() < 0.0001:
                tech.discover(self.current_time.strftime('%Y-%m-%d'))

    def simulate_population_growth(self):
        if random.random() < 0.01:  # 1% daily chance of new NPC being born or immigrating
            name = random_name()
            age = random.randint(0, 30)  # Age 0 for newborns, up to 30 for immigrants
            _, country, state = random_location(self.planets)
            self.add_npc(NPC(name, age, country, state))
            self.births_today += 1
            print(f"New NPC added: {name}, Age: {age}, Country: {country}, State: {state}")

    def log_birth_rate(self):
        year = self.current_time.year
        conn = sqlite3.connect(birth_rate_db)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO BirthRate (year, population, births) VALUES (?, ?, ?)',
                       (year, self.population, self.births_today))
        conn.commit()
        conn.close()

    def log_death_rate(self):
        year = self.current_time.year
        conn = sqlite3.connect(os.path.join(base_dir, "DeathRate", "DeathRateLog.sqlite"))
        cursor = conn.cursor()
        cursor.execute('INSERT INTO DeathRate (year, population, deaths) VALUES (?, ?, ?)',
                       (year, self.population, self.deaths_today))
        conn.commit()
        conn.close()

    def log_economy_data(self):
        year = self.current_time.year
        average_money = self.total_money / self.population if self.population > 0 else 0
        economic_events = "; ".join(self.economic_events)
        conn = sqlite3.connect(os.path.join(base_dir, "EconomyData", "EconomyDataLogs.sqlite"))
        cursor = conn.cursor()
        cursor.execute('INSERT INTO EconomyData (year, total_money, average_money, economic_events) VALUES (?, ?, ?, ?)',
                       (year, self.total_money, average_money, economic_events))
        conn.commit()
        conn.close()
        self.economic_events = []  # Reset the economic events list for the next day

    def run_simulation(self, days_to_simulate):
        end_time = self.current_time + timedelta(days=days_to_simulate)
        while self.current_time < end_time:
            self.current_time += timedelta(days=1)
            self.births_today = 0
            self.deaths_today = 0
            for npc in self.npcs:
                npc.live_day()
                if not npc.alive:
                    self.remove_npc(npc)
                    self.deaths_today += 1  # Increment deaths count
            self.simulate_population_growth()
            self.check_technology_discovery()
            self.population_over_time.append((self.current_time, self.population))  # Record population data
            self.log_birth_rate()  # Log the birth rate for the day
            self.log_death_rate()  # Log the death rate for the day
            self.log_economy_data()  # Log the economy data for the day
            self.print_status()
            time.sleep(0.1)  # Sleep for 0.1 seconds to simulate real time passage (adjust or remove for faster runs)

    def print_status(self):
        print(f"\nSimulation Date: {self.current_time.strftime('%Y-%m-%d')} (Start Date: {self.start_date.strftime('%Y-%m-%d')})")
        print(f"Total Population: {self.population}")
        print(f"Total Money in Economy: {self.total_money:.2f}")
        print(f"Economic Events: {', '.join(self.economic_events)}")
        for planet in self.planets:
            print(f"Planet: {planet.name}")
            for country in planet.countries:
                print(f"  Country: {country.name}")
                for state in country.states:
                    print(f"    State: {state.name}")
        for npc in self.npcs:
            print(npc)
        print("Technological Advancements:")
        for tech in self.technologies:
            status = f"Discovered on {tech.discovery_date}" if tech.discovery_date else "Not yet discovered"
            print(f"  {tech.name}: {status}")

    def plot_population(self):
        dates, populations = zip(*self.population_over_time)
        plt.figure(figsize=(10, 5))
        plt.plot(dates, populations, marker='o')
        plt.xlabel('Date')
        plt.ylabel('Population')
        plt.title('Population Over Time')
        plt.grid(True)
        plt.show()

    def plot_death_rate(self):
        death_rate_db = os.path.join(base_dir, "DeathRate", "DeathRateLog.sqlite")
        conn = sqlite3.connect(death_rate_db)
        cursor = conn.cursor()
        cursor.execute('SELECT year, deaths FROM DeathRate')
        data = cursor.fetchall()
        conn.close()
        
        years, deaths = zip(*data)
        plt.figure(figsize=(10, 5))
        plt.plot(years, deaths, marker='o', color='r')
        plt.xlabel('Year')
        plt.ylabel('Deaths')
        plt.title('Death Rate Over Time')
        plt.grid(True)
        plt.show()

    def plot_economy(self):
        economy_data_db = os.path.join(base_dir, "EconomyData", "EconomyDataLogs.sqlite")
        conn = sqlite3.connect(economy_data_db)
        cursor = conn.cursor()
        cursor.execute('SELECT year, total_money, average_money FROM EconomyData')
        data = cursor.fetchall()
        conn.close()

        years, total_money, average_money = zip(*data)
        plt.figure(figsize=(10, 5))
        plt.plot(years, total_money, marker='o', color='b', label='Total Money')
        plt.plot(years, average_money, marker='o', color='g', label='Average Money per NPC')
        plt.xlabel('Year')
        plt.ylabel('Money')
        plt.title('Economy Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

def random_name():
    first_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Faythe", "Grace", "Heidi", "Ivan", "Judy"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_age():
    return random.randint(18, 70)

def random_location(planets):
    planet = random.choice(planets)
    country = random.choice(planet.countries)
    state = random.choice(country.states)
    return planet, country.name, state.name

# Create a universe
universe = Universe()

# Create Earth and add countries and states
earth = Planet("Earth")
usa = Country("USA")
china = Country("China")
russia = Country("Russia")

usa.add_state(State("California"))
usa.add_state(State("New York"))
china.add_state(State("Beijing"))
china.add_state(State("Shanghai"))
russia.add_state(State("Moscow"))
russia.add_state(State("Saint Petersburg"))

earth.add_country(usa)
earth.add_country(china)
earth.add_country(russia)

# Add Earth to the universe
universe.add_planet(earth)

# Randomly generate a number of NPCs
num_npcs = random.randint(10, 100)  # Adjust the range as needed
for _ in range(num_npcs):
    name = random_name()
    age = random_age()
    _, country, state = random_location(universe.planets)
    universe.add_npc(NPC(name, age, country, state))

# Add some technologies
technologies = ["Fire", "Wheel", "Steam Engine", "Electricity", "Internet", "Artificial Intelligence"]
for tech_name in technologies:
    universe.add_technology(Technology(tech_name))

# Run the simulation for a random number of years (between 1 and 10 years)
days_to_simulate = random.randint(1, 10) * 365

# Run the simulation
print("Starting simulation...")
universe.run_simulation(days_to_simulate)
print("Simulation finished.")

# Plot the population changes
universe.plot_population()
# Plot the death rate changes
universe.plot_death_rate()
# Plot the economy changes
universe.plot_economy()

# GUI to interact with NPCs
class NPCApp:
    def __init__(self, root, universe):
        self.root = root
        self.root.title("NPC Interaction")
        self.universe = universe
        
        self.npc_listbox = tk.Listbox(root)
        self.npc_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.detail_text = tk.Text(root)
        self.detail_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.npc_listbox.bind('<<ListboxSelect>>', self.show_npc_details)
        
        self.populate_npc_list()

    def populate_npc_list(self):
        for npc in self.universe.npcs:
            self.npc_listbox.insert(tk.END, npc.name)

    def show_npc_details(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            npc = self.universe.npcs[index]
            self.detail_text.delete('1.0', tk.END)
            self.detail_text.insert(tk.END, str(npc))

root = tk.Tk()
app = NPCApp(root, universe)
root.mainloop()
