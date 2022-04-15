from itertools import product
from itertools import permutations
from itertools import combinations
import timeit
# Part 1 : Classes and functions you must implement - refer to the jupyter notebook
# You may need to write more classes, which can be done here or in separate files, you choose.

class PlugLead:
    def __init__(self, mapping):
        valid_mapping = self.validate_mapping(mapping)
        if valid_mapping:
            # if mapping inputted is valid then create pluglead
            self.mapping = mapping
        else:
            # if mapping invalid raise value error
            raise ValueError('invalid pluglead: character cannot connect to itself')

    def encode(self, character):
        # if character has a mapping then returns the character that it maps to
        if self.mapping[0] == character:
            return self.mapping[1]
        elif self.mapping[1] == character:
            return self.mapping[0]
        else:
            # if character does not have mapping then returns character
            return character
        
    def validate_mapping(self, mapping):
        # assesses if mapping does not map to itself and is two upper case letters and returns boolean
        if mapping[0] == mapping[1] or not mapping.isupper() or not len(mapping) == 2:
            return False
        else:
            return True
        
    def get_mapping(self):
        # getter method for plugboard
        mapping = self.mapping
        return mapping


class Plugboard:
    def __init__(self):
        self.used_characters = []
        self.plugboard_leads = []
        
    def add(self, lead):
        # assesses if plugboard already has 10 leads
        if len(self.plugboard_leads) < 10:
            # assesses if characters in mapping already have leads in them
            if lead.get_mapping()[0] in self.used_characters or lead.get_mapping()[1] in self.used_characters:
                raise ValueError('invalid plugboard: character can only have one lead')
            else:
                # adds valid lead to plugboard and adds characters to the 'used characters' list
                self.plugboard_leads.append(lead)
                self.used_characters.append(lead.get_mapping()[0])
                self.used_characters.append(lead.get_mapping()[1])
        else:
            raise ValueError('invalid plugboard: only 10 leads')
            
    def encode(self, character):
        # checks each lead in plugboard and returns encoded character
        for lead in self.plugboard_leads:
            if character in lead.get_mapping():
                return lead.encode(character)
        return character   
    
        
class Reflector:
    def __init__(self, mappings):
        self.mappings = mappings
        
    def get_mappings(self):
        return self.mappings
    
    def set_mappings(self, new_mappings):
        # setter function for code five
        # replaces changed pairs in the reflectors mapping
        for x in range (0, len(self.mappings)):
            for maps in new_mappings:
                if maps[0] == self.mappings[x][0]:
                    self.mappings[x] = maps
                elif maps[0] == self.mappings[x][1]:
                    self.mappings[x] = maps[1] + maps[0]
        
    def encode_right_to_left(self, character):
        # calls encode_rotor with '0' which indicates which direction to encode
        return self.encode_rotor(0, character)

    def encode_left_to_right(self, character):
        # calls encode_rotor with '1' which indicates which direction to encode
        return self.encode_rotor(1, character)
    
    def encode_rotor(self, map_value, character):
        # returns the mapped pair value of the character inputted
        rotated_ascii = ord(character)
        for maps in self.mappings:
            if maps[map_value] == chr(rotated_ascii):
                return maps[1-map_value]
        return ValueError('rotor error: character not in rotor')
    
    
class NotchlessRotor(Reflector):
    def __init__(self, mappings):
        self.mappings = mappings
        self.position = "A" # default if not set
        self.ring = "01" # default if not set
        
    def set_position(self, position):
        self.position = position
        
    def set_ring(self, ring):
        self.ring = ring
        
    def encode_rotor(self, map_value, character):
        # calculates the contact point by adding position setting and subtracting ring setting
        rotated_ascii = self.validate_ascii(ord(character) + ord(self.position) - int(self.ring) - 64)   
        for maps in self.mappings:
            if maps[map_value] == chr(rotated_ascii):
                # calculates the pin point by subtracting position setting and adding ring setting
                value = self.validate_ascii(ord(maps[1-map_value]) - ord(self.position) + int(self.ring) + 64)
                # returns encoded character
                return chr(value)
        return ValueError('rotor error: character not in rotor')
        
    def rotate_rotor(self):
        # adds one to position setting to rotate the rotor
        position = self.validate_ascii(ord(self.position) + 1)
        self.position = chr(position)
        
    def validate_ascii(self, value):
        # validates that the ascii value stays between 65 and 90 (upper case characters)
        if value < 65:
            value = value + 26
        elif value > 90:
            value = value - 26
        return value
        
        
class NotchRotor(NotchlessRotor):
    def __init__(self, mappings, notch):
        self.mappings = mappings
        self.notch = notch
        self.position = "A" # default if not set
        self.ring = "01" # default if not set
    
    def is_on_notch(self):
        # assesses if the rotor is currently on its notch and returns boolean
        if self.position == self.notch:
            return True
        else:
            return False
               
        
class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard
        
    def encode(self,text):
        ciphertext = ""
        # loops for every character in provided text
        for character in text:
            # turns rotors at the start of every key press
            self.advance_rotors()
            # values passed from plugboard through rotors and reflector and back again
            temp = self.plugboard.encode(character)
            for n in range(len(self.rotors) - 1, -1, -1):
                temp = self.rotors[n].encode_right_to_left(temp)
            temp = self.reflector.encode_right_to_left(temp)
            for n in range(0, len(self.rotors)):
                temp = self.rotors[n].encode_left_to_right(temp)
            temp = self.plugboard.encode(temp)
            # adds encoded letter to ciphertext string
            ciphertext += temp
        # returns final ciphertext
        return ciphertext
        
    def advance_rotors(self):
        first_notch = False
        second_notch = False
        # assesses if the first rotor is a NotchRotor (if it is not it will not turn the next rotor)
        if isinstance(self.rotors[len(self.rotors)-1], NotchRotor):
            first_notch = self.rotors[len(self.rotors)-1].is_on_notch()
        self.rotors[len(self.rotors)-1].rotate_rotor() # rotates first rotor regardless
        # assesses if the second rotor is a NotchRotor (if it is not it will not turn the next rotor)
        if isinstance(self.rotors[len(self.rotors)-2], NotchRotor):
            second_notch = self.rotors[len(self.rotors)-2].is_on_notch()
        if first_notch:
            self.rotors[len(self.rotors)-2].rotate_rotor() # second rotor turns if first is on its notch
        if second_notch:
            self.rotors[len(self.rotors)-2].rotate_rotor() # double step: second rotor turns with third rotor
            self.rotors[len(self.rotors)-3].rotate_rotor() # third rotor turns if second is on its notch
        # even if there is a fourth rotor and third rotor is on its notch it will not turn
            

# method which returns a Rotor object
# @param - name - name of the Rotor e.g. I or Gamma
def rotor_from_name(name):
    notch = ""
    if name == "I":
        mappings = ["AE", "BK", "CM", "DF", "EL", "FG", "GD", "HQ", "IV", "JZ", "KN", "LT", "MO", "NW", "OY", "PH", "QX", "RU", "SS", "TP", "UA", "VI", "WB", "XR", "YC", "ZJ"]
        notch = "Q"
    elif name == "II":
        mappings = ["AA", "BJ", "CD", "DK", "ES", "FI", "GR", "HU", "IX", "JB", "KL", "LH", "MW", "NT", "OM", "PC", "QQ", "RG", "SZ", "TN", "UP", "VY", "WF", "XV", "YO", "ZE"]
        notch = "E"
    elif name == "III":
        mappings = ["AB", "BD", "CF", "DH", "EJ", "FL", "GC", "HP", "IR", "JT", "KX", "LV", "MZ", "NN", "OY", "PE", "QI", "RW", "SG", "TA", "UK", "VM", "WU", "XS", "YQ", "ZO"]
        notch = "V"
    elif name == "IV":
        mappings = ["AE", "BS", "CO", "DV", "EP", "FZ", "GJ", "HA", "IY", "JQ", "KU", "LI", "MR", "NH", "OX", "PL", "QN", "RF", "ST", "TG", "UK", "VD", "WC", "XM", "YW", "ZB"]
        notch = "J"
    elif name == "V":
        mappings = ["AV", "BZ", "CB", "DR", "EG", "FI", "GT", "HY", "IU", "JP", "KS", "LD", "MN", "NH", "OL", "PX", "QA", "RW", "SM", "TJ", "UQ", "VO", "WF", "XE", "YC", "ZK"]
        notch = "Z"
    elif name == "Beta":
        mappings = ["AL", "BE", "CY", "DJ", "EV", "FC", "GN", "HI", "IX", "JW", "KP", "LB", "MQ", "NM", "OD", "PR", "QT", "RA", "SK", "TZ", "UG", "VF", "WU", "XH", "YO", "ZS"]
    elif name == "Gamma":
        mappings = ["AF", "BS", "CO", "DK", "EA", "FN", "GU", "HE", "IR", "JH", "KM", "LB", "MT", "NI", "OY", "PC", "QW", "RL", "SQ", "TP", "UZ", "VX", "WV", "XG", "YJ", "ZD"]
    else:
        raise ValueError('invalid rotor: that is not a valid rotor name')
    # creates object of different class depending on if it has a notch or not
    if notch == "":
        rotor = NotchlessRotor(mappings)
    else:
        rotor = NotchRotor(mappings, notch)
    return rotor

# method which returns a Reflector object
# @param - name - name of the Reflector e.g. A
def reflector_from_name(name):
    if name == "A":
        mappings = ["AE", "BJ", "CM", "DZ", "EA", "FL", "GY", "HX", "IV", "JB", "KW", "LF", "MC", "NR", "OQ", "PU", "QO", "RN", "ST", "TS", "UP", "VI", "WK", "XH", "YG", "ZD"]
    elif name == "B":
        mappings = ["AY", "BR", "CU", "DH", "EQ", "FS", "GL", "HD", "IP", "JX", "KN", "LG", "MO", "NK", "OM", "PI", "QE", "RB", "SF", "TZ", "UC", "VW", "WV", "XJ", "YA", "ZT"]
    elif name == "C":
        mappings = ["AF", "BV", "CP", "DJ", "EI", "FA", "GO", "HY", "IE", "JD", "KR", "LZ", "MX", "NW", "OG", "PC", "QT", "RK", "SU", "TQ", "US", "VB", "WN", "XM", "YH", "ZL"]
    else:
        raise ValueError('invalid reflector: that is not a valid reflector name')
    reflector = Reflector(mappings)
    return reflector

# method with returns an fully set up enigma machine object
# @param - rotors - string of the rotors used in this enigma machine e.g. "I II III"
# @param - reflector - string of the reflector used in this enigma machine e.g. "B"
# @param - ring_settings - string of the ring settings for the rotors, numbered from 01-26 e.g. "01 02 03"
# @param - initial_positions - string of the starting positions of the rotors, from A-Z e.g. "A A Z"
# @param - plugboard_pairs - list of the plugboard pairs to be used, default is an empty list
def create_enigma_machine(rotors,reflector,ring_settings,initial_positions,plugboard_pairs=[]):
    # make reflector object
    reflector_object = reflector_from_name(reflector)
    # make array of rotor objects
    rotors = rotors.split()
    rotor_objects = []
    for rotor in rotors:
        rotor_objects.append(rotor_from_name(rotor))
    # apply ring settings and initial positions to array of rotor objects
    ring_settings = ring_settings.split()
    initial_positions = initial_positions.split()
    x = 0
    try:
        for rotor in rotor_objects:
            rotor.set_ring(ring_settings[x])
            rotor.set_position(initial_positions[x])
            x += 1
    except:
        raise ValueError('partial ring or position values provided for rotors')
    # create plugboard
    plugboard = Plugboard()
    for pair in plugboard_pairs:
        plugboard.add(PlugLead(pair))
    # create and return enigma machine
    enigma = EnigmaMachine(rotor_objects, reflector_object, plugboard)
    return enigma
        
# Part 2 : functions to implement to demonstrate code breaking.
# each function should return a list of all the possible answers
# code_one provides an example of how you might declare variables and the return type

def code_one():
    start = timeit.default_timer()
    rotors = "Beta Gamma V"
    possible_reflectors = ["A", "B", "C"] # list of possible reflectors
    ring_settings = "04 02 14"
    initial_positions = "M J M"
    plugboard = ["KI", "XN", "FL"]
    possible_messages = []
    code = "DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ"
    crib = "SECRETS"
    
    # iterates through each possible reflector
    for reflector in possible_reflectors:
        # creates engima machine with current reflector
        enigma = create_enigma_machine(rotors, reflector, ring_settings, initial_positions, plugboard)
        # decodes code
        plaintext = enigma.encode(code)
        # if crib in plaintext returned then add to list of possible messages
        if crib in plaintext:
            possible_messages.append(plaintext)  
    print(possible_messages)
    end = timeit.default_timer()
    print ("Time elapsed:", end - start)
    return possible_messages

def code_two():
    start = timeit.default_timer()
    rotors = "Beta I III"
    reflector = "B"
    ring_settings = "23 02 10"
    # list of possible initial position combinations e.g. AAA, AAB ... ZZZ
    initial_positions = list(map(" ".join, product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', repeat=3)))
    plugboard = ["VH", "PT", "ZG", "BJ", "EY", "FS"]
    possible_messages = []
    code = "CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH"
    crib = "UNIVERSITY"
    
    # iterates through each possible initial position
    for initial_position in initial_positions:
        # creates enigma machine with this position and decodes
        enigma = create_enigma_machine(rotors, reflector, ring_settings, initial_position, plugboard)
        plaintext = enigma.encode(code)
        # if crib in plaintext returned then add to list of possible messages
        if crib in plaintext:
            possible_messages.append(plaintext)  
    print(possible_messages)
    end = timeit.default_timer()
    print ("Time elapsed:", end - start)
    return possible_messages
  

def code_three():
    start = timeit.default_timer()
    # list of accepted rotors
    possible_rotors_list = "Beta, Gamma, II, IV"
    # list of all possible combinations of 3 accepted rotors
    possible_rotors = list(map(" ".join, permutations(possible_rotors_list.split(", "), 3)))
    # list of possible reflectors
    possible_reflectors = ["A", "B", "C"]
    # list of accepted ring settings
    possible_rings_list = "02, 04, 06, 08, 20, 22, 24, 26"
    # list of all possible combinations of 3 accepted ring settings
    possible_ring_settings = list(map(" ".join, product(possible_rings_list.split(", "), repeat=3)))
    initial_position = "E M Y"
    plugboard = ["FH", "TS", "BE", "UQ", "KD", "AL"]
    possible_messages = []
    code = "ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY"
    crib = "THOUSANDS"
    
    # loops for every combination of reflector, rotors and ring settings
    for reflector in possible_reflectors:
        for rotors in possible_rotors:
            for ring_settings in possible_ring_settings:
                # creates enigma machine and decodes
                enigma = create_enigma_machine(rotors, reflector, ring_settings, initial_position, plugboard)
                plaintext = enigma.encode(code)
                # if crib in plaintext returned then add to list of possible messages
                if crib in plaintext:
                    possible_messages.append(plaintext)  
    print(possible_messages)
    end = timeit.default_timer()
    print ("Time elapsed:", end - start)
    return possible_messages
      
    
def code_four():
    start = timeit.default_timer()
    rotors = "V III IV"
    reflector = "A"
    ring_settings = "24 12 10"
    initial_position = "S W U"
    # list of available letters that do not currently have a lead in them
    possible_leads = "D, E, K, L, M, O, T, U, X, Y, Z"
    # list of every combination of two of these letters
    possible_pairs = list(map(" ".join, permutations(possible_leads.split(", "), 2)))
    plugboard = ["WP", "RJ", "VF", "HN", "CG", "BS"]
    possible_messages = []
    code = "SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW"
    crib = "TUTOR"
    
    for pair in possible_pairs:
        # adds pairs to plugboard
        pair1 = "A" + pair[0]
        pair2 = "I" + pair[2]
        plugboard.append(pair1)
        plugboard.append(pair2)
        # creates engima with these plugboard settings and decodes
        enigma = create_enigma_machine(rotors, reflector, ring_settings, initial_position, plugboard)
        plaintext = enigma.encode(code)
        # if crib in plaintext then add to possible message list
        if crib in plaintext:
            possible_messages.append(plaintext)
        # removes added pairs from plugboard
        del plugboard[-2:]
    print(possible_messages)  
    end = timeit.default_timer()
    print ("Time elapsed:", end - start)
    return possible_messages

def code_five():
    start = timeit.default_timer()
    rotors = "V II IV"
    possible_standard_reflectors = ["A", "B", "C"] # list of possible standard reflectors
    ring_settings = "06 18 07"
    initial_position = "A J L"
    plugboard = ["UG", "IE", "PO", "NX", "WT"]
    possible_messages = []
    code = "HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX"
    crib = "INSTAGRAM"
    
    for possible_reflector in possible_standard_reflectors:
        # creates reflector object
        reflector = reflector_from_name(possible_reflector)
        # removes duplicate reversed pairs from the reflector's mapping
        mapping = reflector.get_mappings()
        for x in range(0,13):
            reversed_pair = mapping[x][1] + mapping[x][0]
            mapping.remove(reversed_pair)
        original_mappings = ", ".join(mapping)
        # creates a list of all combinations of 4 pairs of maps e.g. [AY, BR, CU, DH]
        select_pairs = list(map(" ".join, combinations(original_mappings.split(", "), 4)))
        # iterates through all 4 pair combinations
        for pairs in select_pairs:
            pairs = pairs.split()
            # creates list of all possible combinations of pairs that can swap within the four pairs 
            # e.g. [[[AY, BR],[CU, DH]] , [[AY, DH],[BR,CU]] , [[AY, CU],[BR,DH]]]
            swapping_pairs = [[[pairs[0], pairs[1]], [pairs[2], pairs[3]]], [[pairs[0], pairs[3]], [pairs[1], pairs[2]]], [[pairs[0], pairs[2]], [pairs[1], pairs[3]]]]
            # iterates through all possible wire swaps
            for pair in swapping_pairs:
                # performs the wire swaps
                pair1 = pair[0][0]
                pair2 = pair[0][1]
                temp = pair1
                pair1 = pair1[0] + pair2[1]
                pair2 = pair2[0] + temp[1]             
                pair3 = pair[1][0]
                pair4 = pair[1][1]
                temp = pair3
                pair3 = pair3[0] + pair4[1]
                pair4 = pair4[0] + temp[1]
                pairs_list = [pair1, pair2, pair3, pair4]
                # creates enigma
                enigma = create_enigma_machine(rotors, possible_reflector, ring_settings, initial_position, plugboard)
                # edits mapping of reflector with wire swaps
                enigma.reflector.set_mappings(pairs_list)
                plaintext = enigma.encode(code)
                # if crib in plaintext then add to possible messages and save current reflector and wire swaps
                if crib in plaintext:
                    possible_messages.append(plaintext)
                    correct_reflector = possible_reflector
                    swapped_wires = pairs_list
    end = timeit.default_timer()
    print(possible_messages)
    print("original reflector is :", correct_reflector)
    print("swapped wires are :", swapped_wires)
    print ("Time elapsed:", end - start)
    return possible_messages

if __name__ == "__main__":
    # You can use this section to test your code.  However, remember that your code
    # is automarked in the jupyter notebook so make sure you have followed the
    # instructions in the notebook to make sure your code works and passes the
    # example tests.

    # NOTE - if your code does not work in the notebook when we
    # run the autograded tests you will receive a 0 mark for functionality.
    pass
