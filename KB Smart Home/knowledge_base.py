import random

CONSTRAINTS = ["motion", "light", "dark", "hot", "cold", "heater", "person_present", "windows", "music", "vacuum", "dirty"]
ODDS = 10

class KB:
    def __init__(self, nb_rooms):
        self.nb_rooms = nb_rooms
        self.kb = {}
        self.logs = {}
        
        for con in CONSTRAINTS:
            entry = {}
            for i in range(1, nb_rooms + 1):
                random_bool = random.choice([True, False])
                entry["room" + str(i)] = random_bool
            self[con] = entry
        
        self.normalize()
               
    
    def __str__(self):
        return str(self.kb)
    def __iter__(self):
        return iter(self.kb.keys())
    def __getitem__(self, key):
        return self.kb[key]
    def __setitem__(self, key, value):
        self.kb[key] = value
    
    def normalize(self):
        """In order to have logical constraints within the KB, some of them need to be normalized.
        Example: It cannot be hot and cold at the same time..."""
        
        for i in range(1, self.nb_rooms+1):
            key = "room" + str(i)
            
            # Setting dark to False whenever light is True
            if self['light'][key]:
                self['dark'][key] = False
            
            # Setting cold to False whenever hot is True
            if self['hot'][key]:
                self['cold'][key] = False
                
            # Setting hot to False whenever cold is True
            if self['cold'][key]:
                self['hot'][key] = False
    
    def randomize(self):
        """Randomly inverse the status of a constraint with a 10% chance"""
        for key in self:
            for i in range(1, self.nb_rooms + 1):
                room = "room" + str(i)
                if random.randint(1, ODDS) == 1:
                    self[key][room] = not self[key][room]
        self.normalize()
    
    def turn_on(self, room, element):
        """Turns on the element, may have additional dynamic consequences depending on the elements.
        Exemple: turning on the light makes the room not dark."""
        if self[element][room]:
            return
        self.logs[element] = self.logs.get(element, 0) + 1
        print(f"Turning on {element} in {room}.")
        self[element][room] = True
        
        if element == 'light':
            if self['dark'][room]:
                print("\tRoom is not dark anymore.")
            self['dark'][room] = False
        elif element == 'heater':
            if self['cold'][room]:
                print("\tRoom is not cold anymore.")
            self['cold'][room] = False
        elif element == 'windows':
            if self['hot'][room]:
                print("\tRoom is not hot anymore.")
            self['hot'][room] = False
        elif element == 'vacuum':
            if self['dirty'][room]:
                print("\tRoom is now clean.")
            self['dirty'][room] = False
        
            
    def turn_off(self, room, element):
        """Turns on the element"""
        if not self[element][room]:
            return
        self.logs[element] = self.logs.get(element, 0) + 1
        print(f"Turning off {element} in {room}.")
        self[element][room] = False
        
                                         
def agent_reasoning(kb, room):
    """List of rules that the agent will follow."""
    
    #Rule 1: If motion is detected and it's dark, turn on the light
    if kb['motion'][room] and kb['dark'][room]:
        kb.turn_on(room, "light")
    
    # Rule 2: If no motion and light is on, turn it off
    if not kb['motion'][room] and kb['light'][room]:
        kb.turn_off(room, 'light')

    # Rule 3: If cold and someone is present, turn on heater
    if kb['cold'][room] and kb['person_present'][room]:
        kb.turn_on(room, 'heater')
    
    # Rule 4: If hot, turn off heater and open windows
    if kb['hot'][room]:
        kb.turn_off(room, 'heater')
        kb.turn_on(room, 'windows')

    # Rule 5: If motion is detected but no one is in the room, close windows for security reasons.
    if kb['motion'][room] and not kb['person_present'][room]:
        kb.turn_off(room, 'windows')
    
    #Rule 6: If no one is here or motion is detected, turn on music
    if not kb["person_present"][room] or kb["motion"][room]:
        kb.turn_on(room, 'music')
    
    #Rule 7: If a person is present but no motion is detected and it is dark, turn off music and light as they are likely sleeping
    if kb['person_present'][room] and not kb['motion'][room] and kb['dark'][room]:
        kb.turn_off(room, 'light')
        kb.turn_off(room, 'music')
    
    #Rule 8: If room is dirty, clean it
    if kb["dirty"][room]:
        kb.turn_on(room, "vacuum")
    