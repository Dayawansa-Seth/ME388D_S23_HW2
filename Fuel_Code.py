import os
import re
import matplotlib.pyplot as plt

# Lists to store k_eff and fuel_frac values
k_eff_list = []
fuel_frac_list = []
energy_list = []
critical_flux_list = []

# Function to extract k-eff and fuel_frac values from .out files
def extract_values(filename):
    k_eff = None
    fuel_frac = None
    critical_flux = []
    critical_energy = []
    
    with open(filename, 'r') as file:
        lines = file.readlines()
        in_critical_spectra = False
        # Extract k-eff value
        for line in lines:
            if "k-eff =" in line:
                k_eff_match = re.search(r"k-eff =\s*([\d\.]+)", line)
                if k_eff_match:
                    k_eff = float(k_eff_match.group(1))
        
            # Extract fuel_frac value (on line 39, starting at column 27)
            if "uo2" in line:
                fuel_frac_match = re.search(r"uo2\s*1\s*([\d\.]+)", line)  # Extract the number before space
                if fuel_frac_match:
                    fuel_frac = float(fuel_frac_match.group(1))  # Convert the extracted string to float
                     
            #part b information
            if "Group   Upper      Critical" in line:
                in_critical_spectra = True
            
            if in_critical_spectra:
                critical_match = re.search(r"\d+\s*([\d\.E+-]+)\s*([\d\.E+-]+)", line)
                
                if critical_match:
                    critical_flux.append(float(critical_match.group(2)))
                    critical_energy.append(float(critical_match.group(1)))
           
            if "NOTE" in line:
                in_critical_spectra = False

     
    return k_eff, round(fuel_frac,2), critical_flux, critical_energy

# Walk through current folder and subfolders to find .out files
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.out'):
            filepath = os.path.join(root, file)
            k_eff, fuel_frac, critical_flux, critical_energy   = extract_values(filepath)
            
            if k_eff is not None and fuel_frac is not None:
                k_eff_list.append(k_eff)
                fuel_frac_list.append(fuel_frac)
            if critical_flux is not [] and critical_energy is not []:
                energy_list.append(critical_energy)
                critical_flux_list.append(critical_flux)
# Plotting the data
plt.plot(fuel_frac_list, k_eff_list, 'bo-')
plt.xlabel("Fuel Fraction")
plt.ylabel("k-eff")
plt.title("Fuel Fraction vs k-eff")
plt.grid(True)
plt.show()


for i in range(len(critical_flux_list)):
    if i%5 == 0:
        plt.semilogx(energy_list[i], critical_flux_list[i], label=f"{fuel_frac_list[i]} % uo2")

# Add titles and labels
plt.title('Critical Flux Values Over a Variety of Fuel Fractions')
plt.xlabel('Upper Energy (eV)')
plt.ylabel('Critical Flux (per unit-lethargy)')
plt.tight_layout()

# Add legend to differentiate between the sublists
plt.legend()

# Display the plot
plt.show()