import math

class Calibrators:
    def __init__(self):
        self.min_normalized = 1.0
        self.max_normalized = 5.0
        self.moderated_for = 4.0
        self.moderated_rev = 2.0
        self.moderated_non = 3.0
        self.min_comparator = 700
        self.mod_for_comparator = 26000
        self.mid_comparator = 36500
        self.max_rev_comparator = 61300
        self.lower_divisor_exponent = 9.24
        self.upper_divisor_exponent = 9.40
        self.lower_divisor = float(math.exp(self.lower_divisor_exponent))
        self.upper_divisor = float(math.exp(self.upper_divisor_exponent))
        self.pival = math.pi

    def scaler(self, val):
        self.val = val
        if val>=0 and val <= self.min_comparator:
            return self.min_normalized
        
        elif val > self.min_comparator and val <= self.mod_for_comparator:
            return round(float(val / self.lower_divisor), 2)
        
        elif val > self.mod_for_comparator and val <=self.mid_comparator:
            return self.moderated_non
        
        elif val > self.mid_comparator and val < self.max_rev_comparator:
            return round(float(val / self.upper_divisor), 2)
            
        elif val >= self.max_rev_comparator:
            return self.max_normalized
        
    def normalizer(self, crval):
        if crval <= self.min_normalized:
            return int(self.min_normalized)
        
        elif crval == self.moderated_non:
            return int(self.moderated_non)
        
        elif crval == self.max_normalized:
            return int(self.max_normalized)
        
        elif crval > self.moderated_non and crval < self.max_normalized:
            return int(self.moderated_for)
        
        elif crval > self.min_normalized and crval < self.moderated_non:
            return int(self.moderated_rev)
        
    def correctedSteps(self, values):
        self.corrected_values = []
        corrected_values = tuple(self.normalizer(self.scaler(val)) for val in values)
        return corrected_values
                
    def toDegrees(self, radians):
        return int(radians * (180 / self.pival))

    def toRadians(self, degrees):
        return ((degrees * self.pival) / 180)
