import numpy as np

class EmissionsCalculator:
    """
    Emissions calculator that accepts DataFrame arrays, Series, or scalar values.
    All conversion logic removed - inputs are used directly.
    """
    
    # Table C-1: Default CO2 Emission Factors (kg CO2/MMBtu)
    table_c1_co2_emission_factors = {
        "Coal": {
            "Anthracite": 103.69,
            "Bituminous Coal": 93.28,
            "Sub-bituminous Coal": 97.17,
            "Lignite": 97.72,
            "Mixed (Commercial sector)": 95.52,
            "Mixed (Electric Power sector)": 95.52
        },
        "Natural Gas": 53.06,
        "Petroleum Products": {
            "Asphalt and Road Oil": 75.04,
            "Aviation Gasoline": 70.22,
            "Butane": 64.77,
            "Butane-Butylene Mixtures": 64.77,
            "Crude Oil": 73.96,
            "Distillate Fuel Oil No. 1": 73.25,
            "Distillate Fuel Oil No. 2": 73.96,
            "Distillate Fuel Oil No. 4": 75.04,
            "Ethane": 59.60,
            "Ethane-Ethylene Mixtures": 59.60,
            "Isobutane": 64.77,
            "Isobutane-Isobutylene Mixtures": 64.77,
            "Kerosene": 72.22,
            "Liquefied Petroleum Gases (LPG)": 63.07,
            "Lubricants": 74.54,
            "Motor Gasoline": 70.22,
            "Natural Gasoline": 66.83,
            "Naphtha (<401 deg F)": 68.44,
            "Other Oil (>401 deg F)": 75.04,
            "Pentanes Plus": 70.02,
            "Petrochemical Feedstocks": 68.44,
            "Petroleum Coke": 102.41,
            "Propane": 62.87,
            "Propane-Propylene Mixtures": 62.87,
            "Residual Fuel Oil No. 5": 72.93,
            "Residual Fuel Oil No. 6": 75.10,
            "Special Naphtha": 68.44,
            "Still Gas": 66.72,
            "Unfinished Oils": 73.96,
            "Waste Oil": 73.96
        }
    }

    # Table C-2: Default CH4 and N2O Emission Factors (kg/MMBtu)
    table_c2_emission_factors = {
        "Coal and Coke": {
            "CH4": 1.1e-2,
            "N2O": 1.6e-3
        },
        "Natural Gas": {
            "CH4": 1.0e-3,
            "N2O": 1.0e-4
        },
        "Petroleum Products": {
            "CH4": 3.0e-3,
            "N2O": 6.0e-4
        },
        "Fuel Gas": {
            "CH4": 3.0e-3,
            "N2O": 6.0e-4
        },
        "Other Fuels—Solid": {
            "CH4": 3.2e-2,
            "N2O": 4.2e-3
        },
        "Blast Furnace Gas": {
            "CH4": 2.2e-5,
            "N2O": 1.0e-4
        },
        "Coke Oven Gas": {
            "CH4": 4.8e-4,
            "N2O": 1.0e-4
        },
        "Biomass Fuels—Solid": {
            "CH4": 3.2e-2,
            "N2O": 4.2e-3
        },
        "Wood and Wood Residuals": {
            "CH4": 7.2e-3,
            "N2O": 3.6e-3
        },
        "Biomass Fuels—Gaseous": {
            "CH4": 3.2e-3,
            "N2O": 6.3e-4
        },
        "Biomass Fuels—Liquid": {
            "CH4": 1.1e-3,
            "N2O": 1.1e-4
        }
    }


    # --- Subpart AA Tables ---
    biomass_emission_factors = {
        "North American Softwood": {"CO2": 94.4, "CH4": 0.0019, "N2O": 0.00042},
        "North American Hardwood": {"CO2": 93.7, "CH4": 0.0019, "N2O": 0.00042},
        "Bagasse": {"CO2": 95.5, "CH4": 0.0019, "N2O": 0.00042},
        "Bamboo": {"CO2": 93.7, "CH4": 0.0019, "N2O": 0.00042},
        "Straw": {"CO2": 95.1, "CH4": 0.0019, "N2O": 0.00042}
    }

    fossil_emission_factors = {
        "Residual Oil": {"CH4": 0.0027, "N2O": 0.0000},
        "Distillate Oil": {"CH4": 0.0027, "N2O": 0.0000},
        "Natural Gas": {"CH4": 0.0027, "N2O": 0.0000},
        "Biogas": {"CH4": 0.0027, "N2O": 0.0000},
        "Petroleum Coke": {"CH4": 0.0027, "N2O": None},
        "Other Fuels": {"CH4": None, "N2O": None}
    }

    gwp_table_a1 = {
        "SF6": 23900,
        "CF4": 7390,
        "C2F6": 12200,
        "C3F8": 8900,
        "NF3": 17200,
        "HFC-134a": 1430,
        "HFC-23": 12400,
        "HFC-125": 3500,
        "HFC-143a": 4470,
        "HFC-152a": 124,
        "HFC-32": 675,
        "HFC-227ea": 3220,
        "HFC-236fa": 9810,
        "HFC-365mfc": 794
    }

    @staticmethod
    def get_gwp(self, gas_name):
        """Lookup GWP from Table A-1."""
        return self.gwp_table_a1.get(gas_name)

    # ------------------------------------------------------- Subpart AA Equations ----------------------------------------------------------------------
    @staticmethod
    def calculate_biogenic_emissions_spent_liquor(dataframe, solids_short_tons, hhv_mmbtu_per_kg, ef_kg_per_mmbtu):
        """Eq. AA-1: CO₂(bio), CH₄, or N₂O = 0.90718 * Solids * HHV * EF"""
        solids = np.array(dataframe[solids_short_tons])
        hhv = np.array(dataframe[hhv_mmbtu_per_kg])
        ef = np.array(dataframe[ef_kg_per_mmbtu])
        return 0.90718 * solids * hhv * ef * 1e-3

    @staticmethod
    def calculate_biogenic_co2_carbon_content(dataframe, solids_short_tons, carbon_content_fraction):
        """Eq. AA-2: CO₂(bio) = 0.90718 * Solids * CC * (44/12)"""
        solids = np.array(dataframe[solids_short_tons])
        carbon_content = np.array(dataframe[carbon_content_fraction])
        return 0.90718 * solids * carbon_content * (44 / 12)

    @staticmethod
    def calculate_co2_makeup_chemicals(dataframe, m_caco3_tons, m_naco3_tons):
        """Eq. AA-3: CO₂ = (44/100)*M(CaCO₃) + (44/105.99)*M(Na₂CO₃)"""
        caco3 = np.array(dataframe[m_caco3_tons])
        naco3 = np.array(dataframe[m_naco3_tons])
        return (44/100) * caco3 + (44/105.99) * naco3

    @staticmethod
    def get_biomass_emission_factor(self, furnish_type, gas):
        """Get biomass emission factor from lookup table."""
        return self.biomass_emission_factors.get(furnish_type, {}).get(gas)

    @staticmethod  
    def get_fossil_emission_factor(self, fuel_type, gas):
        """Get fossil fuel emission factor from lookup table."""
        return self.fossil_emission_factors.get(fuel_type, {}).get(gas)
    
    @staticmethod
    def get_co2_emission_factor(fuel_type, fuel_subtype=None):
        """Get CO2 emission factor from Table C-1."""
        if fuel_type in EmissionsCalculator.table_c1_co2_emission_factors:
            ef_data = EmissionsCalculator.table_c1_co2_emission_factors[fuel_type]
            if isinstance(ef_data, dict):
                if fuel_subtype and fuel_subtype in ef_data:
                    return ef_data[fuel_subtype]
                else:
                    # Return first available if no subtype specified
                    return list(ef_data.values())[0] if ef_data else 0
            else:
                return ef_data
        return 0
    
    @staticmethod
    def get_ch4_n2o_emission_factor(fuel_type, gas_type):
        """Get CH4 or N2O emission factor from Table C-2."""
        return EmissionsCalculator.table_c2_emission_factors.get(fuel_type, {}).get(gas_type, 0)
    
    # -------------------------------------------------------- Subpart DD: Threshold Calculations --------------------------

    @staticmethod
    def calculate_threshold_emissions_dd1(dataframe, nc_eps_lbs, ghg_weight_fraction, gwp, ef=0.1):
        """Equation DD-1: Threshold emissions for electric power systems."""
        nc = np.array(dataframe[nc_eps_lbs])
        wf = np.array(dataframe[ghg_weight_fraction])
        gwp_arr = np.array(dataframe[gwp])
        return np.sum(nc * wf * gwp_arr * ef * 0.000453592)

    @staticmethod
    def calculate_threshold_emissions_dd2(dataframe, nc_other_lbs, ghg_weight_fraction, gwp, ef=0.1):
        """Equation DD-2: Threshold emissions for non-electric power systems."""
        nc = np.array(dataframe[nc_other_lbs])
        wf = np.array(dataframe[ghg_weight_fraction])
        gwp_arr = np.array(dataframe[gwp])
        return np.sum(nc * wf * gwp_arr * ef * 0.000453592)

    @staticmethod
    def calculate_weighted_gwp_dd3(dataframe, ghg_weight_fraction, gwp):
        """Equation DD-3: Weighted average GWP of insulating gas."""
        wf = np.array(dataframe[ghg_weight_fraction])
        gwp_arr = np.array(dataframe[gwp])
        return np.sum(wf * gwp_arr)

    @staticmethod
    def calculate_emissions_dd4(dataframe, ghg_weight_fraction, inventory_decrease, acquisitions, disbursements, net_nameplate_increase):
        """Equation DD-4: Mass-balance emissions calculation."""
        wf = np.array(dataframe[ghg_weight_fraction])
        inv_dec = np.array(dataframe[inventory_decrease])
        acq = np.array(dataframe[acquisitions])
        disb = np.array(dataframe[disbursements])
        nameplate = np.array(dataframe[net_nameplate_increase])
        return wf * (inv_dec + acq - disb - nameplate)

    @staticmethod
    def calculate_nameplate_capacity_dd5(dataframe, p_initial, p_final, p_full, m_recovered):
        """Equation DD-5: Adjusted nameplate capacity for retiring equipment."""
        p_init = np.array(dataframe[p_initial])
        p_fin = np.array(dataframe[p_final])
        p_f = np.array(dataframe[p_full])
        m_rec = np.array(dataframe[m_recovered])
        return m_rec * (p_f - p_init) / (p_f - p_fin)
    
    # ----------------------------------------------------- Subpart NN: Suppliers of Natural Gas and NGLs ---------------------------

    @staticmethod
    def calculate_co2_nn1(dataframe, fuel_volume, hhv, ef_kg_per_mmbtu):
        """Equation NN-1: CO₂ emissions using HHV and EF (kg/MMBtu)."""
        vol = np.array(dataframe[fuel_volume])
        heating_value = np.array(dataframe[hhv])
        ef = np.array(dataframe[ef_kg_per_mmbtu])
        return np.sum(vol * heating_value * ef * 1e-3)

    @staticmethod
    def calculate_co2_nn2(dataframe, fuel_volume, ef_mt_per_unit):
        """Equation NN-2: CO₂ emissions using direct EF (MT/unit)."""
        vol = np.array(dataframe[fuel_volume])
        ef = np.array(dataframe[ef_mt_per_unit])
        return np.sum(vol * ef)

    @staticmethod
    def calculate_co2_nn3(dataframe, fuel_volume, ef_mt_per_mscf):
        """Equation NN-3: CO₂ emissions for gas redelivered to transmission pipelines."""
        vol = np.array(dataframe[fuel_volume])
        ef = np.array(dataframe[ef_mt_per_mscf])
        return np.sum(vol * ef)

    @staticmethod
    def calculate_co2_nn4(dataframe, fuel_volume, ef_mt_per_mscf):
        """Equation NN-4: CO₂ emissions for gas delivered to large end-users."""
        vol = np.array(dataframe[fuel_volume])
        ef = np.array(dataframe[ef_mt_per_mscf])
        return np.sum(vol * ef)

    @staticmethod
    def calculate_co2_nn5a(dataframe, fuel_added, fuel_removed, ef_mt_per_mscf):
        """Equation NN-5a: Net change in on-system storage."""
        added = np.array(dataframe[fuel_added])
        removed = np.array(dataframe[fuel_removed])
        ef = np.array(dataframe[ef_mt_per_mscf])
        return (added - removed) * ef

    @staticmethod
    def calculate_co2_nn5b(dataframe, fuel_volume, ef_mt_per_mscf):
        """Equation NN-5b: Gas bypassing city gate."""
        vol = np.array(dataframe[fuel_volume])
        ef = np.array(dataframe[ef_mt_per_mscf])
        return vol * ef

    @staticmethod
    def calculate_co2_nn6(dataframe, co2i, co2j, co2k, co2l, co2n):
        """Equation NN-6: CO₂ emissions to small end-users."""
        i = np.array(dataframe[co2i])
        j = np.array(dataframe[co2j])
        k = np.array(dataframe[co2k])
        l = np.array(dataframe[co2l])
        n = np.array(dataframe[co2n])
        return np.maximum(0, i - j - k - l - n)

    @staticmethod
    def calculate_co2_nn7(dataframe, fuel_volume, ef_mt_per_bbl):
        """Equation NN-7: NGLs received from other fractionators."""
        vol = np.array(dataframe[fuel_volume])
        ef = np.array(dataframe[ef_mt_per_bbl])
        return np.sum(vol * ef)

    @staticmethod
    def calculate_co2_nn8(dataframe, co2i, co2m):
        """Equation NN-8: Net emissions from NGLs supplied minus received."""
        i = np.array(dataframe[co2i])
        m = np.array(dataframe[co2m])
        return np.maximum(0, i - m)

    # ------------------------------------------------ Subpart OO: Suppliers of Industrial GHGs ------------------------------------

    @staticmethod
    def calculate_production_oo1(dataframe, production_period_masses):
        """Equation OO-1: Total annual production."""
        masses = np.array(dataframe[production_period_masses])
        return np.sum(masses)

    @staticmethod
    def calculate_production_oo2(dataframe, output_mass, used_mass):
        """Equation OO-2: Production over a period."""
        output = np.array(dataframe[output_mass])
        used = np.array(dataframe[used_mass])
        return output - used

    @staticmethod
    def calculate_transformation_oo3(dataframe, feed_mass, transformation_fraction):
        """Equation OO-3: Mass transformed annually."""
        feed = np.array(dataframe[feed_mass])
        fraction = np.array(dataframe[transformation_fraction])
        return feed * fraction

    @staticmethod
    def calculate_destruction_oo4(dataframe, feed_mass, destruction_efficiency):
        """Equation OO-4: Mass destroyed annually."""
        feed = np.array(dataframe[feed_mass])
        efficiency = np.array(dataframe[destruction_efficiency])
        return feed * efficiency

    # ---------------------------------------------------- Subpart RR: Geologic Sequestration of CO₂ ---------------------------------
    @staticmethod
    def calculate_co2_received_mass_flow(dataframe, q_mass, s_mass, c_co2):
        """Equation RR-1: CO₂ received via mass flow meter."""
        q = np.array(dataframe[q_mass])
        s = np.array(dataframe[s_mass])
        c = np.array(dataframe[c_co2])
        return np.sum((q - s) * c)

    @staticmethod
    def calculate_co2_received_volumetric_flow(dataframe, q_vol, s_vol, c_co2, density=0.0018682):
        """Equation RR-2: CO₂ received via volumetric flow meter."""
        q = np.array(dataframe[q_vol])
        s = np.array(dataframe[s_vol])
        c = np.array(dataframe[c_co2])
        return np.sum((q - s) * c * density)

    @staticmethod
    def calculate_total_co2_received(dataframe, co2_received_list):
        """Equation RR-3: Sum of CO₂ received from multiple meters."""
        received = np.array(dataframe[co2_received_list])
        return np.sum(received)

    @staticmethod
    def calculate_co2_injected_mass_flow(dataframe, q_mass, c_co2):
        """Equation RR-4: CO₂ injected via mass flow meter."""
        q = np.array(dataframe[q_mass])
        c = np.array(dataframe[c_co2])
        return np.sum(q * c)

    @staticmethod
    def calculate_co2_injected_volumetric_flow(dataframe, q_vol, c_co2, density=0.0018682):
        """Equation RR-5: CO₂ injected via volumetric flow meter."""
        q = np.array(dataframe[q_vol])
        c = np.array(dataframe[c_co2])
        return np.sum(q * c * density)

    @staticmethod
    def calculate_total_co2_injected(dataframe, co2_injected_list):
        """Equation RR-6: Total CO₂ injected across all wells."""
        injected = np.array(dataframe[co2_injected_list])
        return np.sum(injected)

    @staticmethod
    def calculate_co2_produced_mass_flow(dataframe, q_mass, c_co2):
        """Equation RR-7: CO₂ produced via mass flow meter."""
        q = np.array(dataframe[q_mass])
        c = np.array(dataframe[c_co2])
        return np.sum(q * c)

    @staticmethod
    def calculate_co2_produced_volumetric_flow(dataframe, q_vol, c_co2, density=0.0018682):
        """Equation RR-8: CO₂ produced via volumetric flow meter."""
        q = np.array(dataframe[q_vol])
        c = np.array(dataframe[c_co2])
        return np.sum(q * c * density)

    @staticmethod
    def calculate_total_co2_produced(dataframe, co2_produced_list, entrained_fraction):
        """Equation RR-9: Total CO₂ produced including entrained CO₂."""
        produced = np.array(dataframe[co2_produced_list])
        fraction = np.array(dataframe[entrained_fraction])
        return np.sum(produced) * (1 + fraction)

    @staticmethod
    def calculate_surface_leakage(dataframe, leakage_list):
        """Equation RR-10: Total CO₂ emitted by surface leakage."""
        leakage = np.array(dataframe[leakage_list])
        return np.sum(leakage)

    @staticmethod
    def calculate_sequestered_co2_rr11(dataframe, co2_injected, co2_produced, co2_surface_leakage, co2_fi, co2_fp):
        """Equation RR-11: CO₂ sequestered with production."""
        injected = np.array(dataframe[co2_injected])
        produced = np.array(dataframe[co2_produced])
        leakage = np.array(dataframe[co2_surface_leakage])
        fi = np.array(dataframe[co2_fi])
        fp = np.array(dataframe[co2_fp])
        return injected - produced - leakage - fi - fp

    @staticmethod
    def calculate_sequestered_co2_rr12(dataframe, co2_injected, co2_surface_leakage, co2_fi):
        """Equation RR-12: CO₂ sequestered without production."""
        injected = np.array(dataframe[co2_injected])
        leakage = np.array(dataframe[co2_surface_leakage])
        fi = np.array(dataframe[co2_fi])
        return injected - leakage - fi
    
    @staticmethod
    def calculate_total_ghg_co2e(dataframe, co2_tons, ch4_tons, n2o_tons):
        """Total GHG emissions in CO₂-equivalent (CO₂e) metric tons."""
        co2 = np.array(dataframe[co2_tons])
        ch4 = np.array(dataframe[ch4_tons])
        n2o = np.array(dataframe[n2o_tons])
        return co2 + 25 * ch4 + 298 * n2o
    
    # ------------------------------------------ Subpart C Equations ---------------------------------------------------

    @staticmethod
    def calculate_co2_natural_gas_therms(dataframe, gas_therms):
        """Eq. C-1a: CO₂ = 0.1 * 1e-3 * Gas * EF"""
        gas = np.array(dataframe[gas_therms])
        ef = EmissionsCalculator.table_c1_co2_emission_factors["Natural Gas"]
        return 0.1 * 1e-3 * gas * ef

    @staticmethod
    def calculate_co2_natural_gas_mmbtu(dataframe, gas_mmbtu):
        """Eq. C-1b: CO₂ = 1e-3 * Gas * EF"""
        gas = np.array(dataframe[gas_mmbtu])
        ef = EmissionsCalculator.table_c1_co2_emission_factors["Natural Gas"]
        return 1e-3 * gas * ef

    @staticmethod
    def calculate_co2_tier2(dataframe, fuel_mass_or_volume, hhv_mmbtu_per_unit, fuel_type="Natural Gas"):
        """Eq. C-2a: CO₂ = 1e-3 * Fuel * HHV * EF"""
        fuel = np.array(dataframe[fuel_mass_or_volume])
        hhv = np.array(dataframe[hhv_mmbtu_per_unit])
        
        # Get emission factor from Table C-1
        if fuel_type in EmissionsCalculator.table_c1_co2_emission_factors:
            ef_data = EmissionsCalculator.table_c1_co2_emission_factors[fuel_type]
            if isinstance(ef_data, dict):
                # For fuels with subcategories, use a default or first available
                ef = list(ef_data.values())[0] if ef_data else 0
            else:
                ef = ef_data
        else:
            ef = 0
            
        return 1e-3 * fuel * hhv * ef

    @staticmethod
    def calculate_co2_tier2_steam(dataframe, steam_lb, b_ratio, fuel_type="Natural Gas"):
        """Eq. C-2c: CO₂ = 1e-3 * Steam * B * EF"""
        steam = np.array(dataframe[steam_lb])
        ratio = np.array(dataframe[b_ratio])
        
        # Get emission factor from Table C-1
        if fuel_type in EmissionsCalculator.table_c1_co2_emission_factors:
            ef_data = EmissionsCalculator.table_c1_co2_emission_factors[fuel_type]
            if isinstance(ef_data, dict):
                # For fuels with subcategories, use a default or first available
                ef = list(ef_data.values())[0] if ef_data else 0
            else:
                ef = ef_data
        else:
            ef = 0
            
        return 1e-3 * steam * ratio * ef

    @staticmethod
    def calculate_co2_solid_tier3(dataframe, fuel_mass_lb, cc_kgc_per_lb):
        """Eq. C-3: CO₂ = 1e-3 * Fuel * CC * (44/12)"""
        fuel = np.array(dataframe[fuel_mass_lb])
        cc = np.array(dataframe[cc_kgc_per_lb])
        return 1e-3 * fuel * cc * (44/12)

    @staticmethod
    def calculate_co2_liquid_tier3(dataframe, fuel_gal, cc_kgc_per_gal):
        """Eq. C-4: CO₂ = 1e-3 * Fuel * CC * (44/12)"""
        fuel = np.array(dataframe[fuel_gal])
        cc = np.array(dataframe[cc_kgc_per_gal])
        return 1e-3 * fuel * cc * (44/12)

    @staticmethod
    def calculate_co2_gas_tier3(dataframe, fuel_scf, cc_kgc_per_kg, mw_kg_per_kmol, mvc_scf_per_kmol):
        """Eq. C-5: CO₂ = 1e-3 * Fuel * (CC / MW) * (44/12) * (1/MVC)"""
        fuel = np.array(dataframe[fuel_scf])
        cc = np.array(dataframe[cc_kgc_per_kg])
        mw = np.array(dataframe[mw_kg_per_kmol])
        mvc = np.array(dataframe[mvc_scf_per_kmol])
        return 1e-3 * fuel * (cc / mw) * (44/12) * (1/mvc)

    @staticmethod
    def calculate_co2_cems(dataframe, co2_conc_dry_frac, stack_gas_flow_scfh, molar_volume_scf_per_kmol):
        """Eq. C-6: Hourly CO₂ emission rate (metric tons/hr)."""
        conc = np.array(dataframe[co2_conc_dry_frac])
        flow = np.array(dataframe[stack_gas_flow_scfh])
        volume = np.array(dataframe[molar_volume_scf_per_kmol])
        return conc * flow / volume * (44/12) * 1e-3

    @staticmethod
    def calculate_co2_moisture_corrected(dataframe, co2_mass_dry, moisture_percent):
        """Eq. C-7: CO₂* = CO₂ / (1 - %H₂O/100)"""
        co2 = np.array(dataframe[co2_mass_dry])
        moisture = np.array(dataframe[moisture_percent])
        return co2 / (1 - moisture / 100)

    @staticmethod
    def calculate_ch4_n2o_therms(dataframe, gas_therms, fuel_type="Natural Gas", gas_type="CH4"):
        """Eq. C-8a: CH₄ or N₂O = 0.1 * 1e-3 * Fuel * EF"""
        gas = np.array(dataframe[gas_therms])
        ef = EmissionsCalculator.table_c2_emission_factors.get(fuel_type, {}).get(gas_type, 0)
        return 0.1 * 1e-3 * gas * ef

    @staticmethod
    def calculate_ch4_n2o_mmbtu(dataframe, fuel_mmbtu, fuel_type="Natural Gas", gas_type="CH4"):
        """Eq. C-8b: CH₄ or N₂O = 1e-3 * Fuel * EF"""
        fuel = np.array(dataframe[fuel_mmbtu])
        ef = EmissionsCalculator.table_c2_emission_factors.get(fuel_type, {}).get(gas_type, 0)
        return 1e-3 * fuel * ef

    @staticmethod
    def calculate_ch4_n2o_tier2(dataframe, fuel_mass_or_vol, hhv_mmbtu_per_unit, fuel_type="Natural Gas", gas_type="CH4"):
        """Eq. C-9a: CH₄ or N₂O = 1e-3 * Fuel * HHV * EF"""
        fuel = np.array(dataframe[fuel_mass_or_vol])
        hhv = np.array(dataframe[hhv_mmbtu_per_unit])
        ef = EmissionsCalculator.table_c2_emission_factors.get(fuel_type, {}).get(gas_type, 0)
        return 1e-3 * fuel * hhv * ef

    @staticmethod
    def calculate_ch4_n2o_steam(dataframe, steam_lb, b_ratio, fuel_type="Natural Gas", gas_type="CH4"):
        """Eq. C-9b: CH₄ or N₂O = 1e-3 * Steam * B * EF"""
        steam = np.array(dataframe[steam_lb])
        ratio = np.array(dataframe[b_ratio])
        ef = EmissionsCalculator.table_c2_emission_factors.get(fuel_type, {}).get(gas_type, 0)
        return 1e-3 * steam * ratio * ef
    
    @staticmethod
    def calculate_ch4_n2o_tier4(dataframe, annual_heat_input_mmbtu, fuel_type="Natural Gas", gas_type="CH4"):
        """Eq. C-10: CH₄ or N₂O = 1e-3 * (HI)A * EF"""
        heat_input = np.array(dataframe[annual_heat_input_mmbtu])
        ef = EmissionsCalculator.table_c2_emission_factors.get(fuel_type, {}).get(gas_type, 0)
        return 1e-3 * heat_input * ef
    
    @staticmethod
    def calculate_biogenic_co2(dataframe, fuel_mass_or_volume, hhv_mmbtu_per_unit, biomass_type="Wood and Wood Residuals"):
        """Eq. C-11: CO₂(bio) = 1e-3 * Fuel * HHV * EF"""
        fuel = np.array(dataframe[fuel_mass_or_volume])
        hhv = np.array(dataframe[hhv_mmbtu_per_unit])
        
        # Use biomass emission factors for biogenic CO2
        ef = EmissionsCalculator.biomass_emission_factors.get(biomass_type, {}).get("CO2", 0)
        return 1e-3 * fuel * hhv * ef

    @staticmethod
    def calculate_biogenic_co2_cems(dataframe, co2_conc_percent, stack_gas_flow_scfh, bio_fraction, f_factor_scf_per_mmbtu):
        """Eq. C-12: Hourly biogenic CO₂ mass emission rate (metric tons/hr)."""
        conc = np.array(dataframe[co2_conc_percent])
        flow = np.array(dataframe[stack_gas_flow_scfh])
        bio = np.array(dataframe[bio_fraction])
        f_factor = np.array(dataframe[f_factor_scf_per_mmbtu])
        return 5.18e-7 * conc * flow * bio / f_factor

    @staticmethod
    def calculate_total_co2_biomass_fraction(dataframe, total_co2_mass, biomass_fraction):
        """Eq. C-13: CO₂_total = CO₂_total_mass * Biomass_fraction"""
        total_co2 = np.array(dataframe[total_co2_mass])
        bio_fraction = np.array(dataframe[biomass_fraction])
        return total_co2 * bio_fraction

    @staticmethod
    def calculate_biogenic_co2_moisture_corrected(dataframe, co2_mass_dry, moisture_percent):
        """Eq. C-14: CO₂*(bio) = CO₂ / (1 - %H₂O/100)"""
        co2 = np.array(dataframe[co2_mass_dry])
        moisture = np.array(dataframe[moisture_percent])
        return co2 / (1 - moisture / 100)

    @staticmethod
    def calculate_biogenic_co2_annual(dataframe, co2_hourly_mass_rates, operating_hours):
        """Eq. C-15: CO₂_annual(bio) = Σ(CO₂_hourly × time)"""
        rates = np.array(dataframe[co2_hourly_mass_rates])
        hours = np.array(dataframe[operating_hours])
        return np.sum(rates * hours)

    @staticmethod
    def calculate_biogenic_co2_o2_based(dataframe, o2_percent, flow_scfh, bio_fraction, f_factor_scf_per_mmbtu):
        """Eq. C-15a: Biogenic CO₂ from O₂-based monitoring (metric tons/hr)."""
        o2 = np.array(dataframe[o2_percent])
        flow = np.array(dataframe[flow_scfh])
        bio = np.array(dataframe[bio_fraction])
        f_factor = np.array(dataframe[f_factor_scf_per_mmbtu])
        return 5.18e-7 * (20.9 - o2) * flow * bio / f_factor

    # -------------------------------------------- Appendix F: Part 75 Core Emissions Calculations -------------------------------

    @staticmethod
    def calculate_heat_input_rate(dataframe, flow_rate_acfh, o2_percent, f_factor=8710):
        """Equation F-1: Heat input rate (mmBtu/hr) using O₂-based F-factor."""
        flow = np.array(dataframe[flow_rate_acfh])
        o2 = np.array(dataframe[o2_percent])
        return (flow * f_factor * (20.9 / (20.9 - o2))) / 1e6

    @staticmethod
    def calculate_so2_mass_emissions(dataframe, so2_ppm, flow_rate_acfh):
        """Equation F-2: SO₂ mass emissions (lb/hr)."""
        so2 = np.array(dataframe[so2_ppm])
        flow = np.array(dataframe[flow_rate_acfh])
        return so2 * flow * 1.660e-7

    @staticmethod
    def calculate_so2_total_quarter(dataframe, hourly_emissions_lbhr, operating_time_hr):
        """Eq. F-3: Quarterly total SO₂ mass emissions (tons)."""
        emissions = np.array(dataframe[hourly_emissions_lbhr])
        time = np.array(dataframe[operating_time_hr])
        return np.sum(emissions * time) / 2000

    @staticmethod
    def calculate_so2_total_annual(dataframe, quarterly_emissions_tons):
        """Eq. F-4: Annual total SO₂ mass emissions (tons)."""
        quarterly = np.array(dataframe[quarterly_emissions_tons])
        return np.sum(quarterly)

    @staticmethod
    def calculate_nox_rate_o2_dry(dataframe, nox_ppm, o2_percent, f_factor):
        """Eq. F-5: NOₓ emission rate (lb/mmBtu) using dry O₂ basis."""
        K = 1.194e-7
        nox = np.array(dataframe[nox_ppm])
        o2 = np.array(dataframe[o2_percent])
        f_fact = np.array(dataframe[f_factor])
        return K * nox * f_fact * (20.9 / (20.9 - o2))

    @staticmethod
    def calculate_nox_rate_co2(dataframe, nox_ppm, co2_percent, fc_factor):
        """Eq. F-6: NOₓ emission rate (lb/mmBtu) using CO₂ basis."""
        K = 1.194e-7
        nox = np.array(dataframe[nox_ppm])
        co2 = np.array(dataframe[co2_percent])
        fc_fact = np.array(dataframe[fc_factor])
        return K * nox * fc_fact / co2

    @staticmethod
    def calculate_f_factor(dataframe, h, c, s, n, o, gcv):
        """Eq. F-7a: Site-specific dry-basis F-factor (dscf/mmBtu)."""
        hydrogen = np.array(dataframe[h])
        carbon = np.array(dataframe[c])
        sulfur = np.array(dataframe[s])
        nitrogen = np.array(dataframe[n])
        oxygen = np.array(dataframe[o])
        calorific = np.array(dataframe[gcv])
        return (8.749 * hydrogen + 26.64 * carbon + 2.85 * sulfur + 0.0 * nitrogen + 0.0 * oxygen) / calorific

    @staticmethod
    def calculate_fc_factor(dataframe, c, gcv):
        """Eq. F-7b: Site-specific carbon-basis Fc-factor (scf CO₂/mmBtu)."""
        carbon = np.array(dataframe[c])
        calorific = np.array(dataframe[gcv])
        return (1.000 * 1.83 * carbon) / calorific

    @staticmethod
    def calculate_co2_mass_emissions_wet(dataframe, co2_percent, flow_rate_scfh):
        """Eq. F-11: CO₂ mass emission rate (tons/hr), wet basis."""
        K = 5.7e-7
        co2 = np.array(dataframe[co2_percent])
        flow = np.array(dataframe[flow_rate_scfh])
        return co2 * flow * K

    @staticmethod
    def calculate_co2_total_quarter(dataframe, hourly_tonsh, operating_time_hr):
        """Eq. F-12: Quarterly total CO₂ mass emissions (tons)."""
        hourly = np.array(dataframe[hourly_tonsh])
        time = np.array(dataframe[operating_time_hr])
        return np.sum(hourly * time)

    @staticmethod
    def calculate_co2_total_annual(dataframe, quarterly_tons):
        """Eq. F-13: Annual total CO₂ mass emissions (tons)."""
        quarterly = np.array(dataframe[quarterly_tons])
        return np.sum(quarterly)

    @staticmethod
    def calculate_co2_from_o2_dry(dataframe, o2_percent, f_factor, fc_factor):
        """Eq. F-14a: CO₂ from dry O₂ readings (% CO₂ dry)."""
        o2 = np.array(dataframe[o2_percent])
        f_fact = np.array(dataframe[f_factor])
        fc_fact = np.array(dataframe[fc_factor])
        return (fc_fact / f_fact) * (20.9 - o2)

    @staticmethod
    def calculate_co2_from_o2_wet(dataframe, o2_percent, h2o_percent, f_factor, fc_factor):
        """Eq. F-14b: CO₂ from wet O₂ readings (% CO₂ wet)."""
        o2 = np.array(dataframe[o2_percent])
        h2o = np.array(dataframe[h2o_percent])
        f_fact = np.array(dataframe[f_factor])
        fc_fact = np.array(dataframe[fc_factor])
        return (fc_fact / f_fact) * ((20.9 - o2) * ((100 - h2o) / 100))

    @staticmethod
    def calculate_heat_input_co2_wet(dataframe, flow_rate_scfh, fc_factor, co2_percent):
        """Eq. F-15: Heat input using wet CO₂ (% CO₂ wet)."""
        flow = np.array(dataframe[flow_rate_scfh])
        fc_fact = np.array(dataframe[fc_factor])
        co2 = np.array(dataframe[co2_percent])
        return (flow * co2) / (fc_fact * 100)

    @staticmethod
    def calculate_heat_input_co2_dry(dataframe, flow_rate_scfh, fc_factor, co2_percent, h2o_percent):
        """Eq. F-16: Heat input using dry CO₂ (% CO₂ dry)."""
        flow = np.array(dataframe[flow_rate_scfh])
        fc_fact = np.array(dataframe[fc_factor])
        co2 = np.array(dataframe[co2_percent])
        h2o = np.array(dataframe[h2o_percent])
        return (flow * co2 * (100 - h2o)) / (fc_fact * 100)

    @staticmethod
    def calculate_heat_input_o2_wet(dataframe, flow_rate_scfh, f_factor, o2_percent, h2o_percent):
        """Eq. F-17: Heat input using wet O₂ (% O₂ wet)."""
        flow = np.array(dataframe[flow_rate_scfh])
        f_fact = np.array(dataframe[f_factor])
        o2 = np.array(dataframe[o2_percent])
        h2o = np.array(dataframe[h2o_percent])
        return (flow * (20.9 / (20.9 - o2)) * (100 - h2o)) / (f_fact * 100)

    @staticmethod
    def calculate_heat_input_o2_dry(dataframe, flow_rate_scfh, f_factor, o2_percent, h2o_percent):
        """Eq. F-18: Heat input using dry O₂ (% O₂ dry)."""
        flow = np.array(dataframe[flow_rate_scfh])
        f_fact = np.array(dataframe[f_factor])
        o2 = np.array(dataframe[o2_percent])
        h2o = np.array(dataframe[h2o_percent])
        return (flow * (20.9 / (20.9 - o2)) * (100 - h2o)) / (f_fact * 100)

    @staticmethod
    def calculate_heat_input_oil(dataframe, mass_rate_lbhr, gcv_btu_per_lb):
        """Eq. F-19: Heat input from oil (mmBtu/hr)."""
        mass = np.array(dataframe[mass_rate_lbhr])
        gcv = np.array(dataframe[gcv_btu_per_lb])
        return (mass * gcv) / 1e6

    @staticmethod
    def calculate_heat_input_gas(dataframe, flow_100scfh, gcv_btu_per_100scf):
        """Eq. F-20: Heat input from gaseous fuel (mmBtu/hr)."""
        flow = np.array(dataframe[flow_100scfh])
        gcv = np.array(dataframe[gcv_btu_per_100scf])
        return (flow * gcv) / 1e6

    @staticmethod
    def calculate_heat_input_coal(dataframe, mass_tons, gcv_btu_per_lb):
        """Eq. F-21: Daily heat input from coal (mmBtu/day)."""
        mass = np.array(dataframe[mass_tons])
        gcv = np.array(dataframe[gcv_btu_per_lb])
        return mass * gcv / 500

    @staticmethod
    def convert_flow_to_stp(dataframe, flow_actual_acfh, t_stack_f, p_stack_inhg, barometric_inhg):
        """Eq. F-22: Convert volumetric flow to STP (scfh)."""
        T_std, P_std = 528.0, 29.92
        flow = np.array(dataframe[flow_actual_acfh])
        temp = np.array(dataframe[t_stack_f])
        p_stack = np.array(dataframe[p_stack_inhg])
        p_baro = np.array(dataframe[barometric_inhg])
        T_stack = 460 + temp
        P_stack = p_stack + p_baro
        return flow * (T_std / T_stack) * (P_stack / P_std)

    @staticmethod
    def calculate_so2_mass_default(dataframe, default_rate_lb_per_mmbtu, heat_input_mmbtuh):
        """Eq. F-23: SO₂ mass emissions using default rate (lb/hr)."""
        rate = np.array(dataframe[default_rate_lb_per_mmbtu])
        heat_input = np.array(dataframe[heat_input_mmbtuh])
        return rate * heat_input

    @staticmethod
    def calculate_nox_mass_lb(dataframe, emission_rate_lb_per_mmbtu, heat_input_mmbtuh, time_hr):
        """Eq. F-24: NOₓ mass (lb) per hour."""
        rate = np.array(dataframe[emission_rate_lb_per_mmbtu])
        heat_input = np.array(dataframe[heat_input_mmbtuh])
        time = np.array(dataframe[time_hr])
        return rate * heat_input * time

    @staticmethod
    def calculate_nox_mass_rate_lbhr(dataframe, emission_rate_lb_per_mmbtu, heat_input_mmbtuh):
        """Eq. F-24a: NOₓ mass emission rate (lb/hr)."""
        rate = np.array(dataframe[emission_rate_lb_per_mmbtu])
        heat_input = np.array(dataframe[heat_input_mmbtuh])
        return rate * heat_input

    @staticmethod
    def calculate_nox_mass_rate_wet(dataframe, nox_ppm, flow_scfh):
        """Eq. F-26a: NOₓ mass emission rate (lb/hr), wet basis."""
        K = 1.194e-7
        nox = np.array(dataframe[nox_ppm])
        flow = np.array(dataframe[flow_scfh])
        return K * nox * flow

    @staticmethod
    def calculate_nox_mass_rate_dry(dataframe, nox_ppm, flow_scfh, h2o_percent):
        """Eq. F-26b: NOₓ mass emission rate (lb/hr), dry basis with wet flow."""
        K = 1.194e-7
        nox = np.array(dataframe[nox_ppm])
        flow = np.array(dataframe[flow_scfh])
        h2o = np.array(dataframe[h2o_percent])
        return K * nox * flow * ((100 - h2o) / 100)

    @staticmethod
    def calculate_nox_mass_total(dataframe, hourly_lb, hours, convert_to_tons=True):
        """Eq. F-27: Cumulative NOₓ mass (tons or lb)."""
        hourly = np.array(dataframe[hourly_lb])
        hrs = np.array(dataframe[hours])
        total_lb = np.sum(hourly * hrs)
        return total_lb / 2000 if convert_to_tons else total_lb

    @staticmethod
    def calculate_nox_mass_apportioned(dataframe, nox_rate_common_lbhr, heat_input_unit, heat_input_common, time_unit_hr, time_common_hr):
        """Eq. F-28: Apportioned NOₓ mass rate for a unit (lb/hr)."""
        nox_rate = np.array(dataframe[nox_rate_common_lbhr])
        heat_unit = np.array(dataframe[heat_input_unit])
        heat_common = np.array(dataframe[heat_input_common])
        time_unit = np.array(dataframe[time_unit_hr])
        time_common = np.array(dataframe[time_common_hr])
        return (nox_rate * heat_unit * time_unit) / (heat_common * time_common)

    @staticmethod
    def calculate_moisture_from_o2(dataframe, o2_dry_percent, o2_wet_percent):
        """Eq. F-31: Stack gas moisture (% H₂O)."""
        o2_dry = np.array(dataframe[o2_dry_percent])
        o2_wet = np.array(dataframe[o2_wet_percent])
        return (100 * (o2_dry - o2_wet)) / o2_dry

    @staticmethod
    def correct_to_wet_basis(dataframe, dry_concentration, moisture_percent):
        """Moisture correction: Converts dry-basis concentration to wet-basis."""
        dry_conc = np.array(dataframe[dry_concentration])
        moisture = np.array(dataframe[moisture_percent])
        return dry_conc * (1 - moisture / 100)

    @staticmethod
    def calculate_hourly_average(dataframe, data_points):
        """Computes hourly average from valid data points."""
        data = np.array(dataframe[data_points])
        return np.mean(data)

    @staticmethod
    def convert_gas_volume_to_mass(dataframe, volume_scf, gas_density_lb_per_scf):
        """Converts gas volume to mass."""
        volume = np.array(dataframe[volume_scf])
        density = np.array(dataframe[gas_density_lb_per_scf])
        return volume * density

    @staticmethod
    def convert_liquid_volume_to_mass(dataframe, volume_gal, liquid_density_lb_per_gal):
        """Converts liquid volume to mass."""
        volume = np.array(dataframe[volume_gal])
        density = np.array(dataframe[liquid_density_lb_per_gal])
        return volume * density

    @staticmethod
    def flag_calibration_drift(dataframe, calibration_error_ppm, span_value_ppm, threshold=0.025):
        """QA/QC flag for calibration drift."""
        error = np.array(dataframe[calibration_error_ppm])
        span = np.array(dataframe[span_value_ppm])
        return abs(error) > (span * threshold)

    @staticmethod
    def substitute_missing_so2_data(dataframe, max_potential_so2_ppm, flow_rate_acfh):
        """Missing data substitution for SO₂ using maximum potential concentration."""
        max_so2 = np.array(dataframe[max_potential_so2_ppm])
        flow = np.array(dataframe[flow_rate_acfh])
        return max_so2 * flow * 1.660e-7

    @staticmethod
    def substitute_missing_nox_data(dataframe, max_potential_nox_ppm, o2_percent):
        """Missing data substitution for NOₓ using maximum potential concentration."""
        max_nox = np.array(dataframe[max_potential_nox_ppm])
        o2 = np.array(dataframe[o2_percent])
        return max_nox * (20.9 / (20.9 - o2)) * 1.194e-7

    @staticmethod
    def calculate_stack_gas_density(dataframe, temperature_f, pressure_inhg, molecular_weight=29.0):
        """Calculates stack gas density using ideal gas law approximation."""
        temp = np.array(dataframe[temperature_f])
        pressure = np.array(dataframe[pressure_inhg])
        temp_r = temp + 459.67
        pressure_psia = pressure * 0.4912
        R = 10.73  # ft³·psi/(lb·mol·°R)
        return (pressure_psia * molecular_weight) / (R * temp_r)

    @staticmethod
    def convert_sulfur_content_to_so2(dataframe, fuel_mass_lb, sulfur_percent):
        """Converts sulfur content in fuel to SO₂ emissions."""
        fuel_mass = np.array(dataframe[fuel_mass_lb])
        sulfur = np.array(dataframe[sulfur_percent])
        sulfur_mass = fuel_mass * sulfur / 100
        return sulfur_mass * (64 / 32)

    @staticmethod
    def validate_span_range(dataframe, measured_value, span_value, tolerance=0.025):
        """Validates if measured value is within acceptable span range."""
        measured = np.array(dataframe[measured_value])
        span = np.array(dataframe[span_value])
        return abs(measured) <= span * (1 + tolerance)

    @staticmethod
    def validate_fuel_flowmeter_accuracy(dataframe, measured_flow, expected_flow, tolerance=0.02):
        """Validates fuel flowmeter accuracy."""
        measured = np.array(dataframe[measured_flow])
        expected = np.array(dataframe[expected_flow])
        return abs(measured - expected) <= expected * tolerance

    @staticmethod
    def validate_calibration_gas_traceability(dataframe, gas_certified, gas_expired):
        """QA check for calibration gas validity."""
        certified = np.array(dataframe[gas_certified])
        expired = np.array(dataframe[gas_expired])
        return certified & ~expired

    @staticmethod
    def estimate_co2_from_o2(dataframe, o2_percent, fuel_type="natural_gas"):
        """Estimates CO₂ concentration from O₂ using stoichiometric ratios."""
        o2 = np.array(dataframe[o2_percent])
        if fuel_type == "natural_gas":
            return 20.9 - o2
        elif fuel_type == "coal":
            return (20.9 - o2) * 1.1
        else:
            return (20.9 - o2) * 1.05
        
    @staticmethod
    def substitute_missing_flow_data(dataframe, max_potential_flow_acfh):
        """Substitutes missing flow data using maximum potential flow."""
        max_flow = np.array(dataframe[max_potential_flow_acfh])
        return max_flow