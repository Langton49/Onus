from enum import Enum

class FacilityType(str, Enum):
    ENERGY = "ENERGY"
    PULP_PAPER = "PULP_PAPER"
    BIOENERGY = "BIOENERGY"

class RuleType(str, Enum):
    CALCULATION = "CALCULATION"
    REPORTING = "REPORTING"
    THRESHOLD = "THRESHOLD"

class FileExtension(str, Enum):
    CSV = "csv"
    XLSX = "xlsx"

class QualityFlag(str, Enum):
    VALID = "VALID"
    ESTIMATED = "ESTIMATED"
    MISSING = "MISSING"
    OUTLIER = "OUTLIER"
    INVALID = "INVALID"

class ValidationStatus(str, Enum):
    PENDING = "PENDING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"

class EPASubpart(str, Enum):
    A = "A"  # General regulations
    C = "C"  # General Stationary Fuel Combustion Sources and CEMS regulations
    D = "D"  # Electricity Generation
    DD = "DD"  # Aluminum Production
    AA = "AA"  # Pulp and Paper Manufacturing
    W = "W"  # Petroleum and Natural Gas Systems
    RR = "RR"  # Geologic Sequestration of CO2
    NN = "NN"  # Reporters

class Equations(str, Enum):
    # Subpart AA
    AA_1 = "AA-1"
    AA_2 = "AA-2"
    AA_3 = "AA-3"
    
    # Subpart DD
    DD_1 = "DD-1"
    DD_2 = "DD-2"
    DD_3 = "DD-3"
    DD_4 = "DD-4"
    DD_5 = "DD-5"
    
    # Subpart NN
    NN_1 = "NN-1"
    NN_2 = "NN-2"
    NN_3 = "NN-3"
    NN_4 = "NN-4"
    NN_5A = "NN-5a"
    NN_5B = "NN-5b"
    NN_6 = "NN-6"
    NN_7 = "NN-7"
    NN_8 = "NN-8"
    
    # Subpart OO
    OO_1 = "OO-1"
    OO_2 = "OO-2"
    OO_3 = "OO-3"
    OO_4 = "OO-4"
    
    # Subpart RR
    RR_1 = "RR-1"
    RR_2 = "RR-2"
    RR_3 = "RR-3"
    RR_4 = "RR-4"
    RR_5 = "RR-5"
    RR_6 = "RR-6"
    RR_7 = "RR-7"
    RR_8 = "RR-8"
    RR_9 = "RR-9"
    RR_10 = "RR-10"
    RR_11 = "RR-11"
    RR_12 = "RR-12"
    
    # Subpart C
    C_1A = "C-1a"
    C_1B = "C-1b"
    C_2A = "C-2a"
    C_2C = "C-2c"
    C_3 = "C-3"
    C_4 = "C-4"
    C_5 = "C-5"
    C_6 = "C-6"
    C_7 = "C-7"
    C_8A = "C-8a"
    C_8B = "C-8b"
    C_9A = "C-9a"
    C_9B = "C-9b"
    C_10 = "C-10"
    C_11 = "C-11"
    C_12 = "C-12"
    C_13 = "C-13"
    C_14 = "C-14"
    C_15 = "C-15"
    C_15A = "C-15a"
    
    # Appendix F
    F_1 = "F-1"
    F_2 = "F-2"
    F_3 = "F-3"
    F_4 = "F-4"
    F_5 = "F-5"
    F_6 = "F-6"
    F_7A = "F-7a"
    F_7B = "F-7b"
    F_11 = "F-11"
    F_12 = "F-12"
    F_13 = "F-13"
    F_14A = "F-14a"
    F_14B = "F-14b"
    F_15 = "F-15"
    F_16 = "F-16"
    F_17 = "F-17"
    F_18 = "F-18"
    F_19 = "F-19"
    F_20 = "F-20"
    F_21 = "F-21"
    F_22 = "F-22"
    F_23 = "F-23"
    F_24 = "F-24"
    F_24A = "F-24a"
    F_26A = "F-26a"
    F_26B = "F-26b"
    F_27 = "F-27"
    F_28 = "F-28"
    F_31 = "F-31"
