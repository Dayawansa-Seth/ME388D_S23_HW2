import os
import re
import matplotlib.pyplot as plt

# Lists to store k_eff and enr values
k_eff_list = []
enr_list = []
energy_list = []
critical_flux_list = []

# Function to extract k-eff and enr values from .out files
def extract_values(filename):
    k_eff = None
    enr = None
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
        
            # Extract enr value (on line 39, starting at column 27)
            if "uo2" in line:
                enr_match = re.search(r"92235\s*([\d\.]+)", line)  # Extract the number before space
                if enr_match:
                    enr = float(enr_match.group(1))  # Convert the extracted string to float
            
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
    
    return k_eff, enr, critical_flux, critical_energy

# Walk through current folder and subfolders to find .out files
for root, dirs, files in os.walk('.'): 
    for file in files:
        if file.endswith('.out'):
            filepath = os.path.join(root, file)
            k_eff, enr, critical_flux, critical_energy   = extract_values(filepath)
            
            if k_eff is not None and enr is not None:
                k_eff_list.append(k_eff)
                enr_list.append(enr)
            if critical_flux is not [] and critical_energy is not []:
                energy_list.append(critical_energy)
                critical_flux_list.append(critical_flux)
# Plotting the data
plt.plot(enr_list, k_eff_list, 'bo-')
plt.xlabel("U-235 Enrichment")
plt.ylabel("k-eff")
plt.title("U-235 Enrichment vs k-eff")
plt.grid(True)
plt.show()


for i in range(len(critical_flux_list)):
    if i%10 == 0:
        plt.semilogx(energy_list[i], critical_flux_list[i], label=f"{enr_list[i]} %")

# Add titles and labels
plt.title('Critical Flux Values Over a Variety of U-235 Enrichments')
plt.xlabel('Upper Energy (eV)')
plt.ylabel('Critical Flux (per unit-lethargy)')
plt.tight_layout()

# Add legend to differentiate between the sublists
plt.legend()

# Display the plot
plt.show()