from google.generativeai.types import FunctionDeclaration

gemini_tool_declarations = {
    "AA-3":
        FunctionDeclaration(
            name="emissions_from_spent_liquor_combustion",
            description="Equation AA-3: Calculate emissions from spent liquor combustion in pulp and paper mills (Subpart AA).",
            parameters={
                "type": "object",
                "properties": {
                    "solids_short_tons": {
                        "type": "string",
                        "description": "Column name containing dry weight of spent liquor solids combusted (short tons)"
                    },
                    "hhv_mmbtu_per_kg": {
                        "type": "string",
                        "description": "Column name containing higher heating value of spent liquor (MMBtu per kg)"
                    },
                    "ef_kg_per_mmbtu": {
                        "type": "string",
                        "description": "Column name containing emission factor (kg per MMBtu)"
                    }
                },
                "required": ["solids_short_tons", "hhv_mmbtu_per_kg", "ef_kg_per_mmbtu"]
            }
        ),
        "AA-4": FunctionDeclaration(
            name="biogenic_co2_from_carbon_content",
            description="Equation AA-4: Calculate biogenic CO₂ emissions from carbon content of spent liquor solids (Subpart AA).",
            parameters={
                "type": "object",
                "properties": {
                    "solids_short_tons": {
                        "type": "string",
                        "description": "Column name containing dry weight of spent liquor solids (short tons)"
                    },
                    "carbon_content_fraction": {
                        "type": "string",
                        "description": "Column name containing carbon content as fraction of dry weight (0-1)"
                    }
                },
                "required": ["solids_short_tons", "carbon_content_fraction"]
            }
        ),
        "AA-5": FunctionDeclaration(
            name="co2_from_makeup_chemicals",
            description="Equation AA-5: Calculate CO₂ emissions from makeup chemicals (CaCO₃ and Na₂CO₃) in pulp production (Subpart AA).",
            parameters={
                "type": "object",
                "properties": {
                    "m_caco3_mt": {
                        "type": "string",
                        "description": "Column name containing mass of calcium carbonate (CaCO₃) consumed (metric tons)"
                    },
                    "m_na2co3_mt": {
                        "type": "string",
                        "description": "Column name containing mass of sodium carbonate (Na₂CO₃) consumed (metric tons)"
                    }
                },
                "required": ["m_caco3_mt", "m_na2co3_mt"]
            }
        ),
        "AA-1": FunctionDeclaration(
            name="get_biomass_emission_factor",
            description="Table AA-1: Retrieve emission factor for biomass fuel types (Subpart AA).",
            parameters={
                "type": "object",
                "properties": {
                    "furnish_type": {
                        "type": "string",
                        "description": "Type of biomass fuel",
                        "enum": ["North American Softwood", "North American Hardwood", "Bagasse", "Bamboo", "Straw"]
                    },
                    "gas": {
                        "type": "string",
                        "description": "GHG type",
                        "enum": ["CO2", "CH4", "N2O"]
                    }
                },
                "required": ["furnish_type", "gas"]
            }
        ),
        "AA-2": FunctionDeclaration(
            name="get_fossil_emission_factor",
            description="Table AA-2: Retrieve emission factor for fossil fuel types (Subpart AA).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_type": {
                        "type": "string",
                        "description": "Type of fossil fuel",
                        "enum": ["Residual Oil", "Distillate Oil", "Natural Gas", "Biogas", "Petroleum Coke", "Other Fuels"]
                    },
                    "gas": {
                        "type": "string",
                        "description": "GHG type",
                        "enum": ["CH4", "N2O"]
                    }
                },
                "required": ["fuel_type", "gas"]
            }
        ),
        "DD-1": FunctionDeclaration(
            name="calculate_threshold_emissions_dd1",
            description="Equation DD-1: Calculate threshold emissions for electric power systems with fluorinated GHGs (Subpart DD).",
            parameters={
                "type": "object",
                "properties": {
                    "nc_eps_lbs": {
                        "type": "string",
                        "description": "Column name containing nameplate capacity of equipment (lbs)"
                    },
                    "ghg_weight_fraction": {
                        "type": "string",
                        "description": "Column name containing weight fraction of fluorinated GHG in gas (0-1)"
                    },
                    "gwp": {
                        "type": "string",
                        "description": "Column name containing global warming potential of each GHG"
                    },
                    "ef": {
                        "type": "string",
                        "description": "Column name containing emission factor (lbs emitted per lbs nameplate, default 0.1)"
                    }
                },
                "required": ["nc_eps_lbs", "ghg_weight_fraction", "gwp"]
            }
        ),
        "DD-2": FunctionDeclaration(
            name="calculate_threshold_emissions_dd2",
            description="Equation DD-2: Calculate threshold emissions for non-electric power systems with fluorinated GHGs (Subpart DD).",
            parameters={
                "type": "object",
                "properties": {
                    "nc_other_lbs": {
                        "type": "string",
                        "description": "Column name containing nameplate capacity of equipment (lbs)"
                    },
                    "ghg_weight_fraction": {
                        "type": "string",
                        "description": "Column name containing weight fraction of fluorinated GHG in gas (0-1)"
                    },
                    "gwp": {
                        "type": "string",
                        "description": "Column name containing global warming potential of each GHG"
                    },
                    "ef": {
                        "type": "string",
                        "description": "Column name containing emission factor (lbs emitted per lbs nameplate, default 0.1)"
                    }
                },
                "required": ["nc_other_lbs", "ghg_weight_fraction", "gwp"]
            }
        ),
        "DD-3": FunctionDeclaration(
            name="calculate_weighted_gwp_dd3",
            description="Equation DD-3: Calculate weighted average GWP of insulating gas mixture (Subpart DD).",
            parameters={
                "type": "object",
                "properties": {
                    "ghg_weight_fraction": {
                        "type": "string",
                        "description": "Column name containing weight fraction of each GHG in mixture (0-1)"
                    },
                    "gwp": {
                        "type": "string",
                        "description": "Column name containing GWP of each GHG"
                    }
                },
                "required": ["ghg_weight_fraction", "gwp"]
            }
        ),
        "DD-4": FunctionDeclaration(
            name="calculate_emissions_dd4",
            description="Equation DD-4: Calculate mass-balance emissions for fluorinated GHGs (Subpart DD).",
            parameters={
                "type": "object",
                "properties": {
                    "ghg_weight_fraction": {
                        "type": "string",
                        "description": "Column name containing weight fraction of fluorinated GHG (0-1)"
                    },
                    "inventory_decrease": {
                        "type": "string",
                        "description": "Column name containing net decrease in stored gas inventory (lbs)"
                    },
                    "acquisitions": {
                        "type": "string",
                        "description": "Column name containing total acquisitions of gas (lbs)"
                    },
                    "disbursements": {
                        "type": "string",
                        "description": "Column name containing total disbursements of gas (lbs)"
                    },
                    "net_nameplate_increase": {
                        "type": "string",
                        "description": "Column name containing net increase in nameplate capacity (lbs)"
                    }
                },
                "required": ["ghg_weight_fraction", "inventory_decrease", "acquisitions", "disbursements", "net_nameplate_increase"]
            }
        ),
        "DD-5": FunctionDeclaration(
            name="calculate_nameplate_capacity_dd5",
            description="Equation DD-5: Calculate adjusted nameplate capacity for retiring equipment (Subpart DD).",
            parameters={
                "type": "object",
                "properties": {
                    "p_initial": {
                        "type": "string",
                        "description": "Column name containing initial pressure (psia)"
                    },
                    "p_final": {
                        "type": "string",
                        "description": "Column name containing final pressure (psia)"
                    },
                    "p_full": {
                        "type": "string",
                        "description": "Column name containing full charge pressure (psia)"
                    },
                    "m_recovered": {
                        "type": "string",
                        "description": "Column name containing mass of gas recovered (lbs)"
                    }
                },
                "required": ["p_initial", "p_final", "p_full", "m_recovered"]
            }
        ),
        "NN-1": FunctionDeclaration(
            name="calculate_co2_nn1",
            description="Equation NN-1: Calculate CO₂ emissions using higher heating value and emission factor for natural gas and NGLs suppliers (Subpart NN).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_volume": {
                        "type": "string",
                        "description": "Column name containing annual volume of fuel supplied (Mscf for NG, bbl for NGLs)"
                    },
                    "hhv": {
                        "type": "string",
                        "description": "Column name containing higher heating value (MMBtu per unit)"
                    },
                    "ef_kg_per_mmbtu": {
                        "type": "string",
                        "description": "Column name containing CO₂ emission factor (kg CO₂ per MMBtu)"
                    }
                },
                "required": ["fuel_volume", "hhv", "ef_kg_per_mmbtu"]
            }
        ),
        "NN-2": FunctionDeclaration(
            name="calculate_co2_nn2",
            description="Equation NN-2: Calculate CO₂ emissions using direct emission factor (Subpart NN).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_volume": {
                        "type": "string",
                        "description": "Column name containing annual volume of fuel supplied (Mscf or bbl)"
                    },
                    "ef_mt_per_unit": {
                        "type": "string",
                        "description": "Column name containing CO₂ emission factor (MT CO₂ per unit)"
                    }
                },
                "required": ["fuel_volume", "ef_mt_per_unit"]
            }
        ),
        "NN-3": FunctionDeclaration(
            name="calculate_co2_nn3",
            description="Equation NN-3: Calculate CO₂ emissions for gas redelivered to transmission pipelines or other LDCs (Subpart NN).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_volume": {
                        "type": "string",
                        "description": "Column name containing volume of natural gas (Mscf)"
                    },
                    "ef_mt_per_mscf": {
                        "type": "string",
                        "description": "CO₂ emission factor (MT per Mscf)"
                    }
                },
                "required": ["fuel_volume", "ef_mt_per_mscf"]
            }
        ),
        "NN-4": FunctionDeclaration(
            name="calculate_co2_nn4",
            description="Equation NN-4: Calculate CO₂ emissions for gas delivered to large end-users (Subpart NN).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_volume": {
                        "type": "string",
                        "description": "Column name containing volume of natural gas (Mscf)"
                    },
                    "ef_mt_per_mscf": {
                        "type": "string",
                        "description": "CO₂ emission factor (MT per Mscf)"
                    }
                },
                "required": ["fuel_volume", "ef_mt_per_mscf"]
            }
        ),
        "NN-5a": FunctionDeclaration(
            name="calculate_co2_nn5a",
            description="Equation NN-5a: Calculate net change in on-system storage (Subpart NN).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_added": {
                        "type": "string",
                        "description": "Column name containing volume added to storage (Mscf)"
                    },
                    "fuel_removed": {
                        "type": "string",
                        "description": "Column name containing volume removed from storage (Mscf)"
                    },
                    "ef_mt_per_mscf": {
                        "type": "string",
                        "description": "CO₂ emission factor (MT per Mscf)"
                    }
                },
                "required": ["fuel_added", "fuel_removed", "ef_mt_per_mscf"]
            }
        ),
        "NN-5b": FunctionDeclaration(
            name="calculate_co2_nn5b",
            description="Equation NN-5b: Calculate emissions for gas bypassing city gate (Subpart NN).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_volume": {
                        "type": "string",
                        "description": "Column name containing volume of gas bypassing city gate (Mscf)"
                    },
                    "ef_mt_per_mscf": {
                        "type": "string",
                        "description": "CO₂ emission factor (MT per Mscf)"
                    }
                },
                "required": ["fuel_volume", "ef_mt_per_mscf"]
            }
        ),
        "NN-6": FunctionDeclaration(
            name="calculate_co2_nn6",
            description="Equation NN-6: Calculate CO₂ emissions to small end-users by difference (Subpart NN).",
            parameters={
                "type": "object",
                "properties": {
                    "co2i": {
                        "type": "string",
                        "description": "Column name containing total CO₂ emissions from gas supplied (metric tons)"
                    },
                    "co2j": {
                        "type": "string",
                        "description": "Column name containing CO₂ emissions from gas redelivered (metric tons)"
                    },
                    "co2k": {
                        "type": "string",
                        "description": "Column name containing CO₂ emissions from gas to large end-users (metric tons)"
                    },
                    "co2l": {
                        "type": "string",
                        "description": "Column name containing CO₂ emissions from storage changes (metric tons)"
                    },
                    "co2n": {
                        "type": "string",
                        "description": "Column name containing CO₂ emissions from gas bypassing city gate (metric tons)"
                    }
                },
                "required": ["co2i", "co2j", "co2k", "co2l", "co2n"]
            }
        ),
        "NN-7": FunctionDeclaration(
            name="calculate_co2_nn7",
            description="Equation NN-7: Calculate emissions from NGLs received from other fractionators (Subpart NN).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_volume": {
                        "type": "string",
                        "description": "Column name containing volume of NGL product received (bbl)"
                    },
                    "ef_mt_per_bbl": {
                        "type": "string",
                        "description": "Column name containing CO₂ emission factor (MT per bbl)"
                    }
                },
                "required": ["fuel_volume", "ef_mt_per_bbl"]
            }
        ),
        "NN-8": FunctionDeclaration(
            name="calculate_co2_nn8",
            description="Equation NN-8: Calculate net emissions from NGLs supplied minus received (Subpart NN).",
            parameters={
                "type": "object",
                "properties": {
                    "co2i": {
                        "type": "string",
                        "description": "Column name containing emissions from NGLs supplied (metric tons)"
                    },
                    "co2m": {
                        "type": "string",
                        "description": "Column name containing emissions from NGLs received from other fractionators (metric tons)"
                    }
                },
                "required": ["co2i", "co2m"]
            }
        ),
        "OO-1": FunctionDeclaration(
            name="calculate_production_oo1",
            description="Equation OO-1: Calculate total annual production of industrial GHGs (Subpart OO).",
            parameters={
                "type": "object",
                "properties": {
                    "production_period_masses": {
                        "type": "string",
                        "description": "Column name containing masses produced over each period (metric tons)"
                    }
                },
                "required": ["production_period_masses"]
            }
        ),
        "OO-2": FunctionDeclaration(
            name="calculate_production_oo2",
            description="Equation OO-2: Calculate production over a period (Subpart OO).",
            parameters={
                "type": "object",
                "properties": {
                    "output_mass": {
                        "type": "string",
                        "description": "Column name containing mass measured coming out of production process (metric tons)"
                    },
                    "used_mass": {
                        "type": "string",
                        "description": "Column name containing mass of used gas added upstream (metric tons)"
                    }
                },
                "required": ["output_mass", "used_mass"]
            }
        ),
        "OO-3": FunctionDeclaration(
            name="calculate_transformation_oo3",
            description="Equation OO-3: Calculate mass of GHG transformed annually (Subpart OO).",
            parameters={
                "type": "object",
                "properties": {
                    "feed_mass": {
                        "type": "string",
                        "description": "Column name containing mass fed into transformation process (metric tons)"
                    },
                    "transformation_fraction": {
                        "type": "string",
                        "description": "Column name containing fraction transformed (0-1)"
                    }
                },
                "required": ["feed_mass", "transformation_fraction"]
            }
        ),
        "OO-4": FunctionDeclaration(
            name="calculate_destruction_oo4",
            description="Equation OO-4: Calculate mass of GHG destroyed annually (Subpart OO).",
            parameters={
                "type": "object",
                "properties": {
                    "feed_mass": {
                        "type": "string",
                        "description": "Column name containing mass fed into destruction device (metric tons)"
                    },
                    "destruction_efficiency": {
                        "type": "string",
                        "description": "Column name containing destruction efficiency (0-1)"
                    }
                },
                "required": ["feed_mass", "destruction_efficiency"]
            }
        ),
        "RR-1": FunctionDeclaration(
            name="calculate_co2_received_mass_flow",
            description="Equation RR-1: Calculate CO₂ received via mass flow meter for geologic sequestration (Subpart RR).",
            parameters={
                "type": "object",
                "properties": {
                    "q_mass": {
                        "type": "string",
                        "description": "Column name containing quarterly mass flow (metric tons)"
                    },
                    "s_mass": {
                        "type": "string",
                        "description": "Column name containing quarterly redelivered mass (metric tons)"
                    },
                    "c_co2": {
                        "type": "string",
                        "description": "Column name containing quarterly CO₂ concentration (weight fraction, 0-1)"
                    }
                },
                "required": ["q_mass", "s_mass", "c_co2"]
            }
        ),
        "RR-2": FunctionDeclaration(
            name="calculate_co2_received_volumetric_flow",
            description="Equation RR-2: Calculate CO₂ received via volumetric flow meter for geologic sequestration (Subpart RR).",
            parameters={
                "type": "object",
                "properties": {
                    "q_vol": {
                        "type": "string",
                        "description": "Column name containing quarterly volumetric flow (standard m³)"
                    },
                    "s_vol": {
                        "type": "string",
                        "description": "Column name containing quarterly redelivered volume (standard m³)"
                    },
                    "c_co2": {
                        "type": "string",
                        "description": "Column name containing quarterly CO₂ concentration (volume fraction, 0-1)"
                    },
                    "density": {
                        "type": "string",
                        "description": "Column name containing CO₂ density at standard conditions (MT/m³, default 0.0018682)"
                    }
                },
                "required": ["q_vol", "s_vol", "c_co2"]
            }
        ),
        "RR-3": FunctionDeclaration(
            name="calculate_total_co2_received",
            description="Equation RR-3: Calculate sum of CO₂ received from multiple meters (Subpart RR).",
            parameters={
                "type": "object",
                "properties": {
                    "co2_received_list": {
                        "type": "string",
                        "description": "Column name containing list of CO₂ received values from different meters (metric tons)"
                    }
                },
                "required": ["co2_received_list"]
            }
        ),
        "RR-4": FunctionDeclaration(
            name="calculate_co2_injected_mass_flow",
            description="Equation RR-4: Calculate CO₂ injected via mass flow meter for geologic sequestration (Subpart RR).",
            parameters={
                "type": "object",
                "properties": {
                    "q_mass": {
                        "type": "string",
                        "description": "Column name containing quarterly mass flow (metric tons)"
                    },
                    "c_co2": {
                        "type": "string",
                        "description": "Column name containing quarterly CO₂ concentration (weight fraction, 0-1)"
                    }
                },
                "required": ["q_mass", "c_co2"]
            }
        ),
        "RR-5": FunctionDeclaration(
            name="calculate_co2_injected_volumetric_flow",
            description="Equation RR-5: Calculate CO₂ injected via volumetric flow meter for geologic sequestration (Subpart RR).",
            parameters={
                "type": "object",
                "properties": {
                    "q_vol": {
                        "type": "string",
                        "description": "Column name containing quarterly volumetric flow (standard m³)"
                    },
                    "c_co2": {
                        "type": "string",
                        "description": "Column name containing quarterly CO₂ concentration (volume fraction, 0-1)"
                    },
                    "density": {
                        "type": "string",
                        "description": "Column name containing CO₂ density at standard conditions (MT/m³, default 0.0018682)"
                    }
                },
                "required": ["q_vol", "c_co2"]
            }
        ),
        "RR-6": FunctionDeclaration(
            name="calculate_total_co2_injected",
            description="Equation RR-6: Calculate total CO₂ injected across all wells (Subpart RR).",
            parameters={
                "type": "object",
                "properties": {
                    "co2_injected_list": {
                        "type": "string",
                        "description": "Column name containing list of CO₂ injected values from all wells (metric tons)"
                    }
                },
                "required": ["co2_injected_list"]
            }
        ),
        "RR-7": FunctionDeclaration(
            name="calculate_co2_produced_mass_flow",
            description="Equation RR-7: Calculate CO₂ produced via mass flow meter from geologic sequestration site (Subpart RR).",
            parameters={
                "type": "object",
                "properties": {
                    "q_mass": {
                        "type": "string",
                        "description": "Column name containing quarterly gas mass flow (metric tons)"
                    },
                    "c_co2": {
                        "type": "string",
                        "description": "Column name containing quarterly CO₂ concentration (weight fraction, 0-1)"
                    }
                },
                "required": ["q_mass", "c_co2"]
            }
        ),
        "RR-8": FunctionDeclaration(
            name="calculate_co2_produced_volumetric_flow",
            description="Equation RR-8: Calculate CO₂ produced via volumetric flow meter from geologic sequestration site (Subpart RR).",
            parameters={
                "type": "object",
                "properties": {
                    "q_vol": {
                        "type": "string",
                        "description": "Column name containing quarterly gas volume (standard m³)"
                    },
                    "c_co2": {
                        "type": "string",
                        "description": "Column name containing quarterly CO₂ concentration (volume fraction, 0-1)"
                    },
                    "density": {
                        "type": "string",
                        "description": "Column name containing CO₂ density at standard conditions (MT/m³, default 0.0018682)"
                    }
                },
                "required": ["q_vol", "c_co2"]
            }
        ),
        "RR-9": FunctionDeclaration(
            name="calculate_total_co2_produced",
            description="Equation RR-9: Calculate total CO₂ produced including entrained CO₂ from geologic sequestration site (Subpart RR).",
            parameters={
                "type": "object",
                "properties": {
                    "co2_produced_list": {
                        "type": "string",
                        "description": "Column name containing list of CO₂ produced values from all wells (metric tons)"
                    },
                    "entrained_fraction": {
                        "type": "string",
                        "description": "Column name containing fraction of entrained CO₂ in produced fluids (0-1)"
                    }
                },
                "required": ["co2_produced_list", "entrained_fraction"]
            }
        ),
        "RR-10": FunctionDeclaration(
            name="calculate_surface_leakage",
            description="Equation RR-10: Calculate total CO₂ emitted by surface leakage at geologic sequestration site (Subpart RR).",
            parameters={
                "type": "object",
                "properties": {
                    "leakage_list": {
                        "type": "string",
                        "description": "Column name containing CO₂ emissions per leakage pathway (metric tons)"
                    }
                },
                "required": ["leakage_list"]
            }
        ),
        "RR-11": FunctionDeclaration(
            name="calculate_sequestered_co2_rr11",
            description="Equation RR-11: Calculate net CO₂ sequestered with production at geologic sequestration site (Subpart RR).",
            parameters={
                "type": "object",
                "properties": {
                    "co2_injected": {
                        "type": "string",
                        "description": "Total CO₂ injected (metric tons)"
                    },
                    "co2_produced": {
                        "type": "string",
                        "description": "Total CO₂ produced (metric tons)"
                    },
                    "co2_surface_leakage": {
                        "type": "string",
                        "description": "Total surface leakage emissions (metric tons)"
                    },
                    "co2_fi": {
                        "type": "string",
                        "description": "CO₂ emissions from fuel combustion at injection facility (metric tons)"
                    },
                    "co2_fp": {
                        "type": "string",
                        "description": "CO₂ emissions from fuel combustion at production facility (metric tons)"
                    }
                },
                "required": ["co2_injected", "co2_produced", "co2_surface_leakage", "co2_fi", "co2_fp"]
            }
        ),
        "RR-12": FunctionDeclaration(
            name="calculate_sequestered_co2_rr12",
            description="Equation RR-12: Calculate net CO₂ sequestered without production at geologic sequestration site (Subpart RR).",
            parameters={
                "type": "object",
                "properties": {
                    "co2_injected": {
                        "type": "string",
                        "description": "Total CO₂ injected (metric tons)"
                    },
                    "co2_surface_leakage": {
                        "type": "string",
                        "description": "Total surface leakage emissions (metric tons)"
                    },
                    "co2_fi": {
                        "type": "string",
                        "description": "CO₂ emissions from fuel combustion at injection facility (metric tons)"
                    }
                },
                "required": ["co2_injected", "co2_surface_leakage", "co2_fi"]
            }
        ),
        
        # ------------------------------------------ Subpart C: Stationary Combustion Equations ------------------------------------------
        
        "C-1a": FunctionDeclaration(
            name="calculate_co2_natural_gas_therms",
            description="Equation C-1a: Calculate CO₂ emissions from natural gas combustion using default EPA emission factor (53.06 kg CO₂/MMBtu) (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "gas_therms": {
                        "type": "string",
                        "description": "Column name containing natural gas consumption (therms)"
                    }
                },
                "required": ["gas_therms"]
            }
        ),
        "C-1b": FunctionDeclaration(
            name="calculate_co2_natural_gas_mmbtu",
            description="Equation C-1b: Calculate CO₂ emissions from natural gas combustion using default EPA emission factor (53.06 kg CO₂/MMBtu) (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "gas_mmbtu": {
                        "type": "string",
                        "description": "Column name containing natural gas consumption (MMBtu)"
                    }
                },
                "required": ["gas_mmbtu"]
            }
        ),
        "C-2a": FunctionDeclaration(
            name="calculate_co2_tier2",
            description="Equation C-2a: Calculate Tier 2 CO₂ emissions using EPA Table C-1 default emission factors (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_mass_or_volume": {
                        "type": "string",
                        "description": "Column name containing fuel consumption (mass or volume units)"
                    },
                    "hhv_mmbtu_per_unit": {
                        "type": "string",
                        "description": "Column name containing higher heating value (MMBtu per unit)"
                    },
                    "fuel_type": {
                        "type": "string",
                        "description": "Fuel type for emission factor lookup",
                        "enum": ["Natural Gas", "Coal", "Petroleum Products"]
                    }
                },
                "required": ["fuel_mass_or_volume", "hhv_mmbtu_per_unit"]
            }
        ),
        "C-2c": FunctionDeclaration(
            name="calculate_co2_tier2_steam",
            description="Equation C-2c: Calculate CO₂ emissions using steam generation data and EPA Table C-1 default emission factors (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "steam_lb": {
                        "type": "string",
                        "description": "Column name containing steam generated (pounds)"
                    },
                    "b_ratio": {
                        "type": "string",
                        "description": "Column name containing boiler efficiency ratio (MMBtu per pound of steam)"
                    },
                    "fuel_type": {
                        "type": "string",
                        "description": "Fuel type for emission factor lookup",
                        "enum": ["Natural Gas", "Coal", "Petroleum Products"],
                    }
                },
                "required": ["steam_lb", "b_ratio"]
            }
        ),
        "C-3": FunctionDeclaration(
            name="calculate_co2_solid_tier3",
            description="Equation C-3: Calculate Tier 3 CO₂ emissions from solid fuels using carbon content (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_mass_lb": {
                        "type": "string",
                        "description": "Column name containing solid fuel mass (pounds)"
                    },
                    "cc_kgc_per_lb": {
                        "type": "string",
                        "description": "Column name containing carbon content (kg C per pound of fuel)"
                    }
                },
                "required": ["fuel_mass_lb", "cc_kgc_per_lb"]
            }
        ),
        "C-4": FunctionDeclaration(
            name="calculate_co2_liquid_tier3",
            description="Equation C-4: Calculate Tier 3 CO₂ emissions from liquid fuels using carbon content (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_gal": {
                        "type": "string",
                        "description": "Column name containing liquid fuel volume (gallons)"
                    },
                    "cc_kgc_per_gal": {
                        "type": "string",
                        "description": "Column name containing carbon content (kg C per gallon of fuel)"
                    }
                },
                "required": ["fuel_gal", "cc_kgc_per_gal"]
            }
        ),
        "C-5": FunctionDeclaration(
            name="calculate_co2_gas_tier3",
            description="Equation C-5: Calculate Tier 3 CO₂ emissions from gaseous fuels using carbon content (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_scf": {
                        "type": "string",
                        "description": "Column name containing gaseous fuel volume (standard cubic feet)"
                    },
                    "cc_kgc_per_kg": {
                        "type": "string",
                        "description": "Column name containing carbon content (kg C per kg of fuel)"
                    },
                    "mw_kg_per_kmol": {
                        "type": "string",
                        "description": "Column name containing molecular weight (kg per kmol)"
                    },
                    "mvc_scf_per_kmol": {
                        "type": "string",
                        "description": "Column name containing molar volume conversion (scf per kmol)"
                    }
                },
                "required": ["fuel_scf", "cc_kgc_per_kg", "mw_kg_per_kmol", "mvc_scf_per_kmol"]
            }
        ),
        "C-6": FunctionDeclaration(
            name="calculate_co2_cems",
            description="Equation C-6: Calculate hourly CO₂ mass emission rate from CEMS data (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "co2_conc_dry_frac": {
                        "type": "string",
                        "description": "Column name containing CO₂ concentration (dry basis fraction)"
                    },
                    "stack_gas_flow_scfh": {
                        "type": "string",
                        "description": "Column name containing stack gas flow rate (scfh)"
                    },
                    "molar_volume_scf_per_kmol": {
                        "type": "string",
                        "description": "Column name containing molar volume conversion (scf per kmol)"
                    }
                },
                "required": ["co2_conc_dry_frac", "stack_gas_flow_scfh", "molar_volume_scf_per_kmol"]
            }
        ),
        "C-7": FunctionDeclaration(
            name="calculate_co2_moisture_corrected",
            description="Equation C-7: Calculate moisture-corrected CO₂ emission rate (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "co2_mass_dry": {
                        "type": "string",
                        "description": "Column name containing CO₂ mass on dry basis (metric tons/hr)"
                    },
                    "moisture_percent": {
                        "type": "string",
                        "description": "Column name containing moisture content (%)"
                    }
                },
                "required": ["co2_mass_dry", "moisture_percent"]
            }
        ),
        "C-8a": FunctionDeclaration(
            name="calculate_ch4_n2o_therms",
            description="Equation C-8a: Calculate CH₄ or N₂O emissions from natural gas using EPA Table C-2 default emission factors (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "gas_therms": {
                        "type": "string",
                        "description": "Column name containing natural gas consumption (therms)"
                    },
                    "fuel_type": {
                        "type": "string",
                        "description": "Fuel type for emission factor lookup",
                        "enum": ["Natural Gas", "Coal and Coke", "Petroleum Products", "Biomass Fuels—Solid", "Biomass Fuels—Liquid", "Biomass Fuels—Gaseous"],
                    },
                    "gas_type": {
                        "type": "string",
                        "description": "Gas type for emission calculation",
                        "enum": ["CH4", "N2O"],
                    }
                },
                "required": ["gas_therms"]
            }
        ),
        "C-8b": FunctionDeclaration(
            name="calculate_ch4_n2o_mmbtu",
            description="Equation C-8b: Calculate CH₄ or N₂O emissions from fuel using EPA Table C-2 default emission factors (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_mmbtu": {
                        "type": "string",
                        "description": "Column name containing fuel consumption (MMBtu)"
                    },
                    "fuel_type": {
                        "type": "string",
                        "description": "Fuel type for emission factor lookup",
                        "enum": ["Natural Gas", "Coal and Coke", "Petroleum Products", "Biomass Fuels—Solid", "Biomass Fuels—Liquid", "Biomass Fuels—Gaseous"],
                    },
                    "gas_type": {
                        "type": "string",
                        "description": "Gas type for emission calculation",
                        "enum": ["CH4", "N2O"],
                    }
                },
                "required": ["fuel_mmbtu"]
            }
        ),
        "C-9a": FunctionDeclaration(
            name="calculate_ch4_n2o_tier2",
            description="Equation C-9a: Calculate CH₄ or N₂O emissions from Tier 2 fuels using EPA Table C-2 default emission factors (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_mass_or_vol": {
                        "type": "string",
                        "description": "Column name containing fuel consumption (mass or volume units)"
                    },
                    "hhv_mmbtu_per_unit": {
                        "type": "string",
                        "description": "Column name containing higher heating value (MMBtu per unit)"
                    },
                    "fuel_type": {
                        "type": "string",
                        "description": "Fuel type for emission factor lookup",
                        "enum": ["Natural Gas", "Coal and Coke", "Petroleum Products", "Biomass Fuels—Solid", "Biomass Fuels—Liquid", "Biomass Fuels—Gaseous"],
                       
                    },
                    "gas_type": {
                        "type": "string",
                        "description": "Gas type for emission calculation",
                        "enum": ["CH4", "N2O"],

                    }
                },
                "required": ["fuel_mass_or_vol", "hhv_mmbtu_per_unit"]
            }
        ),
        "C-9b": FunctionDeclaration(
            name="calculate_ch4_n2o_steam",
            description="Equation C-9b: Calculate CH₄ or N₂O emissions using steam and boiler data with EPA Table C-2 default emission factors (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "steam_lb": {
                        "type": "string",
                        "description": "Column name containing steam generated (pounds)"
                    },
                    "b_ratio": {
                        "type": "string",
                        "description": "Column name containing boiler efficiency ratio (MMBtu per pound of steam)"
                    },
                    "fuel_type": {
                        "type": "string",
                        "description": "Fuel type for emission factor lookup",
                        "enum": ["Natural Gas", "Coal and Coke", "Petroleum Products", "Biomass Fuels—Solid", "Biomass Fuels—Liquid", "Biomass Fuels—Gaseous"],
                       
                    },
                    "gas_type": {
                        "type": "string",
                        "description": "Gas type for emission calculation",
                        "enum": ["CH4", "N2O"],
                       
                    }
                },
                "required": ["steam_lb", "b_ratio"]
            }
        ),
        "C-10": FunctionDeclaration(
            name="calculate_ch4_n2o_tier4",
            description="Equation C-10: Calculate CH₄ or N₂O emissions for Tier 4 using EPA Table C-2 default emission factors (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "annual_heat_input_mmbtu": {
                        "type": "string",
                        "description": "Column name containing annual heat input (MMBtu)"
                    },
                    "fuel_type": {
                        "type": "string",
                        "description": "Fuel type for emission factor lookup",
                        "enum": ["Natural Gas", "Coal and Coke", "Petroleum Products", "Biomass Fuels—Solid", "Biomass Fuels—Liquid", "Biomass Fuels—Gaseous"],
                
                    },
                    "gas_type": {
                        "type": "string",
                        "description": "Gas type for emission calculation",
                        "enum": ["CH4", "N2O"],
                       
                    }
                },
                "required": ["annual_heat_input_mmbtu"]
            }
        ),
        "C-11": FunctionDeclaration(
            name="calculate_biogenic_co2",
            description="Equation C-11: Calculate annual biogenic CO₂ emissions from biomass fuels using default EPA biomass emission factors (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "fuel_mass_or_volume": {
                        "type": "string",
                        "description": "Column name containing biomass fuel consumption (mass or volume units)"
                    },
                    "hhv_mmbtu_per_unit": {
                        "type": "string",
                        "description": "Column name containing higher heating value (MMBtu per unit)"
                    },
                    "biomass_type": {
                        "type": "string",
                        "description": "Biomass fuel type for emission factor lookup",
                        "enum": ["North American Softwood", "North American Hardwood", "Bagasse", "Bamboo", "Straw", "Wood and Wood Residuals"],
            
                    }
                },
                "required": ["fuel_mass_or_volume", "hhv_mmbtu_per_unit"]
            }
        ),
        "C-12": FunctionDeclaration(
            name="calculate_biogenic_co2_cems",
            description="Equation C-12: Calculate hourly biogenic CO₂ mass emission rate using CEMS and F-factors (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "co2_conc_percent": {
                        "type": "string",
                        "description": "Column name containing CO₂ concentration (%)"
                    },
                    "stack_gas_flow_scfh": {
                        "type": "string",
                        "description": "Column name containing stack gas flow rate (scfh)"
                    },
                    "bio_fraction": {
                        "type": "string",
                        "description": "Column name containing biomass fraction (0-1)"
                    },
                    "f_factor_scf_per_mmbtu": {
                        "type": "string",
                        "description": "F-factor (scf per MMBtu)"
                    }
                },
                "required": ["co2_conc_percent", "stack_gas_flow_scfh", "bio_fraction", "f_factor_scf_per_mmbtu"]
            }
        ),
        "C-13": FunctionDeclaration(
            name="calculate_total_co2_biomass_fraction",
            description="Equation C-13: Calculate biomass-derived portion of total CO₂ emissions (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "total_co2_mass": {
                        "type": "string",
                        "description": "Column name containing total CO₂ mass emissions (metric tons)"
                    },
                    "biomass_fraction": {
                        "type": "string",
                        "description": "Column name containing biomass fraction (0-1)"
                    }
                },
                "required": ["total_co2_mass", "biomass_fraction"]
            }
        ),
        "C-14": FunctionDeclaration(
            name="calculate_biogenic_co2_moisture_corrected",
            description="Equation C-14: Calculate moisture-corrected biogenic CO₂ emission rate (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "co2_mass_dry": {
                        "type": "string",
                        "description": "Column name containing biogenic CO₂ mass on dry basis (metric tons/hr)"
                    },
                    "moisture_percent": {
                        "type": "string",
                        "description": "Column name containing moisture content (%)"
                    }
                },
                "required": ["co2_mass_dry", "moisture_percent"]
            }
        ),
        "C-15": FunctionDeclaration(
            name="calculate_biogenic_co2_annual",
            description="Equation C-15: Calculate total annual biogenic CO₂ emissions via CEMS (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "co2_hourly_mass_rates": {
                        "type": "string",
                        "description": "Column name containing hourly biogenic CO₂ emission rates (metric tons/hr)"
                    },
                    "operating_hours": {
                        "type": "string",
                        "description": "Column name containing operating hours for each period"
                    }
                },
                "required": ["co2_hourly_mass_rates", "operating_hours"]
            }
        ),
        "C-15a": FunctionDeclaration(
            name="calculate_biogenic_co2_o2_based",
            description="Equation C-15a: Calculate biogenic CO₂ from O₂-based monitoring systems (Subpart C).",
            parameters={
                "type": "object",
                "properties": {
                    "o2_percent": {
                        "type": "string",
                        "description": "Column name containing O₂ concentration (% dry)"
                    },
                    "flow_scfh": {
                        "type": "string",
                        "description": "Column name containing stack gas flow rate (scfh)"
                    },
                    "bio_fraction": {
                        "type": "string",
                        "description": "Column name containing biomass fraction (0-1)"
                    },
                    "f_factor_scf_per_mmbtu": {
                        "type": "string",
                        "description": "F-factor (scf per MMBtu)"
                    }
                },
                "required": ["o2_percent", "flow_scfh", "bio_fraction", "f_factor_scf_per_mmbtu"]
            }
        ),
        
        # ------------------------------------------ Appendix F: Part 75 Core Emissions Calculations ------------------------------------------
        
        "F-1": FunctionDeclaration(
            name="calculate_heat_input_rate",
            description="Equation F-1: Calculate heat input rate using O₂-based F-factor (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "flow_rate_acfh": {
                        "type": "string",
                        "description": "Column name containing stack gas flow rate (actual cubic feet/hour)"
                    },
                    "o2_percent": {
                        "type": "string",
                        "description": "Column name containing O₂ concentration (% dry)"
                    },
                    "f_factor": {
                        "type": "string",
                        "description": "Column name containing fuel-specific F-factor (default 8710 for natural gas)"
                    }
                },
                "required": ["flow_rate_acfh", "o2_percent"]
            }
        ),
        "F-2": FunctionDeclaration(
            name="calculate_so2_mass_emissions",
            description="Equation F-2: Calculate SO₂ mass emissions (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "so2_ppm": {
                        "type": "string",
                        "description": "Column name containing SO₂ concentration (ppm)"
                    },
                    "flow_rate_acfh": {
                        "type": "string",
                        "description": "Column name containing stack gas flow rate (acfh)"
                    }
                },
                "required": ["so2_ppm", "flow_rate_acfh"]
            }
        ),
        "F-3": FunctionDeclaration(
            name="calculate_so2_total_quarter",
            description="Equation F-3: Calculate quarterly total SO₂ mass emissions (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "hourly_emissions_lbhr": {
                        "type": "string",
                        "description": "Column name containing hourly SO₂ mass emission rate (lb/hr)"
                    },
                    "operating_time_hr": {
                        "type": "string",
                        "description": "Column name containing hourly operating time (hr)"
                    }
                },
                "required": ["hourly_emissions_lbhr", "operating_time_hr"]
            }
        ),
        "F-4": FunctionDeclaration(
            name="calculate_so2_total_annual",
            description="Equation F-4: Calculate annual total SO₂ mass emissions (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "quarterly_emissions_tons": {
                        "type": "string",
                        "description": "Column name containing quarterly SO₂ emissions (tons)"
                    }
                },
                "required": ["quarterly_emissions_tons"]
            }
        ),
        "F-5": FunctionDeclaration(
            name="calculate_nox_rate_o2_dry",
            description="Equation F-5: Calculate NOₓ emission rate using dry O₂ basis (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "nox_ppm": {
                        "type": "string",
                        "description": "Column name containing NOₓ concentration (ppm)"
                    },
                    "o2_percent": {
                        "type": "string",
                        "description": "Column name containing O₂ concentration (% dry)"
                    },
                    "f_factor": {
                        "type": "string",
                        "description": "F-factor (dscf/MMBtu)"
                    }
                },
                "required": ["nox_ppm", "o2_percent", "f_factor"]
            }
        ),
        "F-6": FunctionDeclaration(
            name="calculate_nox_rate_co2",
            description="Equation F-6: Calculate NOₓ emission rate using CO₂ basis (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "nox_ppm": {
                        "type": "string",
                        "description": "Column name containing NOₓ concentration (ppm)"
                    },
                    "co2_percent": {
                        "type": "string",
                        "description": "Column name containing CO₂ concentration (%)"
                    },
                    "fc_factor": {
                        "type": "string",
                        "description": "Fc-factor (scf CO₂/MMBtu)"
                    }
                },
                "required": ["nox_ppm", "co2_percent", "fc_factor"]
            }
        ),
        "F-7a": FunctionDeclaration(
            name="calculate_f_factor",
            description="Equation F-7a: Calculate site-specific dry-basis F-factor (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "h": {
                        "type": "string",
                        "description": "Column name containing hydrogen content (% by weight)"
                    },
                    "c": {
                        "type": "string",
                        "description": "Carbon content (% by weight)"
                    },
                    "s": {
                        "type": "string",
                        "description": "Column name containing sulfur content (% by weight)"
                    },
                    "n": {
                        "type": "string",
                        "description": "Column name containing nitrogen content (% by weight)"
                    },
                    "o": {
                        "type": "string",
                        "description": "Column name containing oxygen content (% by weight)"
                    },
                    "gcv": {
                        "type": "string",
                        "description": "Gross calorific value (Btu/lb)"
                    }
                },
                "required": ["h", "c", "s", "n", "o", "gcv"]
            }
        ),
        "F-7b": FunctionDeclaration(
            name="calculate_fc_factor",
            description="Equation F-7b: Calculate site-specific carbon-basis Fc-factor (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "c": {
                        "type": "string",
                        "description": "Carbon content (% by weight)"
                    },
                    "gcv": {
                        "type": "string",
                        "description": "Gross calorific value (Btu/lb)"
                    }
                },
                "required": ["c", "gcv"]
            }
        ),
        "F-11": FunctionDeclaration(
            name="calculate_co2_mass_emissions_wet",
            description="Equation F-11: Calculate CO₂ mass emission rate on wet basis (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "co2_percent": {
                        "type": "string",
                        "description": "Column name containing CO₂ concentration (%)"
                    },
                    "flow_rate_scfh": {
                        "type": "string",
                        "description": "Column name containing stack gas flow rate (scfh)"
                    }
                },
                "required": ["co2_percent", "flow_rate_scfh"]
            }
        ),
        "F-12": FunctionDeclaration(
            name="calculate_co2_total_quarter",
            description="Equation F-12: Calculate quarterly total CO₂ mass emissions (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "hourly_tonsh": {
                        "type": "string",
                        "description": "Column name containing hourly CO₂ emission rates (tons/hr)"
                    },
                    "operating_time_hr": {
                        "type": "string",
                        "description": "Column name containing operating time for each hour (hr)"
                    }
                },
                "required": ["hourly_tonsh", "operating_time_hr"]
            }
        ),
        "F-13": FunctionDeclaration(
            name="calculate_co2_total_annual",
            description="Equation F-13: Calculate annual total CO₂ mass emissions (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "quarterly_tons": {
                        "type": "string",
                        "description": "Column name containing quarterly CO₂ emissions (tons)"
                    }
                },
                "required": ["quarterly_tons"]
            }
        ),
        "F-14a": FunctionDeclaration(
            name="calculate_co2_from_o2_dry",
            description="Equation F-14a: Calculate CO₂ from dry O₂ readings (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "o2_percent": {
                        "type": "string",
                        "description": "Column name containing O₂ concentration (% dry)"
                    },
                    "f_factor": {
                        "type": "string",
                        "description": "F-factor (dscf/MMBtu)"
                    },
                    "fc_factor": {
                        "type": "string",
                        "description": "Fc-factor (scf CO₂/MMBtu)"
                    }
                },
                "required": ["o2_percent", "f_factor", "fc_factor"]
            }
        ),
        "F-14b": FunctionDeclaration(
            name="calculate_co2_from_o2_wet",
            description="Equation F-14b: Calculate CO₂ from wet O₂ readings (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "o2_percent": {
                        "type": "string",
                        "description": "Column name containing O₂ concentration (% wet)"
                    },
                    "h2o_percent": {
                        "type": "string",
                        "description": "Column name containing H₂O concentration (%)"
                    },
                    "f_factor": {
                        "type": "string",
                        "description": "F-factor (dscf/MMBtu)"
                    },
                    "fc_factor": {
                        "type": "string",
                        "description": "Fc-factor (scf CO₂/MMBtu)"
                    }
                },
                "required": ["o2_percent", "h2o_percent", "f_factor", "fc_factor"]
            }
        ),
        "F-15": FunctionDeclaration(
            name="calculate_heat_input_co2_wet",
            description="Equation F-15: Calculate heat input using wet CO₂ (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "flow_rate_scfh": {
                        "type": "string",
                        "description": "Column name containing stack gas flow rate (scfh)"
                    },
                    "fc_factor": {
                        "type": "string",
                        "description": "Fc-factor (scf CO₂/MMBtu)"
                    },
                    "co2_percent": {
                        "type": "string",
                        "description": "Column name containing CO₂ concentration (% wet)"
                    }
                },
                "required": ["flow_rate_scfh", "fc_factor", "co2_percent"]
            }
        ),
        "F-16": FunctionDeclaration(
            name="calculate_heat_input_co2_dry",
            description="Equation F-16: Calculate heat input using dry CO₂ (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "flow_rate_scfh": {
                        "type": "string",
                        "description": "Column name containing stack gas flow rate (scfh)"
                    },
                    "fc_factor": {
                        "type": "string",
                        "description": "Fc-factor (scf CO₂/MMBtu)"
                    },
                    "co2_percent": {
                        "type": "string",
                        "description": "Column name containing CO₂ concentration (% dry)"
                    },
                    "h2o_percent": {
                        "type": "string",
                        "description": "Column name containing H₂O concentration (%)"
                    }
                },
                "required": ["flow_rate_scfh", "fc_factor", "co2_percent", "h2o_percent"]
            }
        ),
        "F-17": FunctionDeclaration(
            name="calculate_heat_input_o2_wet",
            description="Equation F-17: Calculate heat input using wet O₂ (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "flow_rate_scfh": {
                        "type": "string",
                        "description": "Column name containing stack gas flow rate (scfh)"
                    },
                    "f_factor": {
                        "type": "string",
                        "description": "F-factor (dscf/MMBtu)"
                    },
                    "o2_percent": {
                        "type": "string",
                        "description": "Column name containing O₂ concentration (% wet)"
                    },
                    "h2o_percent": {
                        "type": "string",
                        "description": "Column name containing H₂O concentration (%)"
                    }
                },
                "required": ["flow_rate_scfh", "f_factor", "o2_percent", "h2o_percent"]
            }
        ),
        "F-18": FunctionDeclaration(
            name="calculate_heat_input_o2_dry",
            description="Equation F-18: Calculate heat input using dry O₂ (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "flow_rate_scfh": {
                        "type": "string",
                        "description": "Column name containing stack gas flow rate (scfh)"
                    },
                    "f_factor": {
                        "type": "string",
                        "description": "F-factor (dscf/MMBtu)"
                    },
                    "o2_percent": {
                        "type": "string",
                        "description": "Column name containing O₂ concentration (% dry)"
                    },
                    "h2o_percent": {
                        "type": "string",
                        "description": "Column name containing H₂O concentration (%)"
                    }
                },
                "required": ["flow_rate_scfh", "f_factor", "o2_percent", "h2o_percent"]
            }
        ),
        "F-19": FunctionDeclaration(
            name="calculate_heat_input_oil",
            description="Equation F-19: Calculate heat input from oil (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "mass_rate_lbhr": {
                        "type": "string",
                        "description": "Column name containing oil mass flow rate (lb/hr)"
                    },
                    "gcv_btu_per_lb": {
                        "type": "string",
                        "description": "Column name containing gross calorific value (Btu/lb)"
                    }
                },
                "required": ["mass_rate_lbhr", "gcv_btu_per_lb"]
            }
        ),
        "F-20": FunctionDeclaration(
            name="calculate_heat_input_gas",
            description="Equation F-20: Calculate heat input from gaseous fuel (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "flow_100scfh": {
                        "type": "string",
                        "description": "Column name containing gas flow rate (100 scfh)"
                    },
                    "gcv_btu_per_100scf": {
                        "type": "string",
                        "description": "Column name containing gross calorific value (Btu/100 scf)"
                    }
                },
                "required": ["flow_100scfh", "gcv_btu_per_100scf"]
            }
        ),
        "F-21": FunctionDeclaration(
            name="calculate_heat_input_coal",
            description="Equation F-21: Calculate daily heat input from coal (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "mass_tons": {
                        "type": "string",
                        "description": "Column name containing coal mass (tons)"
                    },
                    "gcv_btu_per_lb": {
                        "type": "string",
                        "description": "Column name containing gross calorific value (Btu/lb)"
                    }
                },
                "required": ["mass_tons", "gcv_btu_per_lb"]
            }
        ),
        "F-22": FunctionDeclaration(
            name="convert_flow_to_stp",
            description="Equation F-22: Convert volumetric flow to standard temperature and pressure (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "flow_actual_acfh": {
                        "type": "string",
                        "description": "Column name containing actual volumetric flow rate (acfh)"
                    },
                    "t_stack_f": {
                        "type": "string",
                        "description": "Column name containing stack temperature (°F)"
                    },
                    "p_stack_inhg": {
                        "type": "string",
                        "description": "Column name containing stack pressure (inHg)"
                    },
                    "barometric_inhg": {
                        "type": "string",
                        "description": "Column name containing barometric pressure (inHg)"
                    }
                },
                "required": ["flow_actual_acfh", "t_stack_f", "p_stack_inhg", "barometric_inhg"]
            }
        ),
        "F-23": FunctionDeclaration(
            name="calculate_so2_mass_default",
            description="Equation F-23: Calculate SO₂ mass emissions using default rate (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "default_rate_lb_per_mmbtu": {
                        "type": "string",
                        "description": "Column name containing default SO₂ emission rate (lb/MMBtu)"
                    },
                    "heat_input_mmbtuh": {
                        "type": "string",
                        "description": "Column name containing heat input rate (MMBtu/hr)"
                    }
                },
                "required": ["default_rate_lb_per_mmbtu", "heat_input_mmbtuh"]
            }
        ),
        "F-24": FunctionDeclaration(
            name="calculate_nox_mass_lb",
            description="Equation F-24: Calculate NOₓ mass per hour (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "emission_rate_lb_per_mmbtu": {
                        "type": "string",
                        "description": "Column name containing NOₓ emission rate (lb/MMBtu)"
                    },
                    "heat_input_mmbtuh": {
                        "type": "string",
                        "description": "Column name containing heat input rate (MMBtu/hr)"
                    },
                    "time_hr": {
                        "type": "string",
                        "description": "Column name containing time period (hr)"
                    }
                },
                "required": ["emission_rate_lb_per_mmbtu", "heat_input_mmbtuh", "time_hr"]
            }
        ),
        "F-24a": FunctionDeclaration(
            name="calculate_nox_mass_rate_lbhr",
            description="Equation F-24a: Calculate NOₓ mass emission rate (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "emission_rate_lb_per_mmbtu": {
                        "type": "string",
                        "description": "Column name containing NOₓ emission rate (lb/MMBtu)"
                    },
                    "heat_input_mmbtuh": {
                        "type": "string",
                        "description": "Column name containing heat input rate (MMBtu/hr)"
                    }
                },
                "required": ["emission_rate_lb_per_mmbtu", "heat_input_mmbtuh"]
            }
        ),
        "F-26a": FunctionDeclaration(
            name="calculate_nox_mass_rate_wet",
            description="Equation F-26a: Calculate NOₓ mass emission rate on wet basis (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "nox_ppm": {
                        "type": "string",
                        "description": "Column name containing NOₓ concentration (ppm)"
                    },
                    "flow_scfh": {
                        "type": "string",
                        "description": "Column name containing stack gas flow rate (scfh)"
                    }
                },
                "required": ["nox_ppm", "flow_scfh"]
            }
        ),
        "F-26b": FunctionDeclaration(
            name="calculate_nox_mass_rate_dry",
            description="Equation F-26b: Calculate NOₓ mass emission rate on dry basis with wet flow (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "nox_ppm": {
                        "type": "string",
                        "description": "Column name containing NOₓ concentration (ppm dry)"
                    },
                    "flow_scfh": {
                        "type": "string",
                        "description": "Column name containing stack gas flow rate (scfh wet)"
                    },
                    "h2o_percent": {
                        "type": "string",
                        "description": "Column name containing H₂O concentration (%)"
                    }
                },
                "required": ["nox_ppm", "flow_scfh", "h2o_percent"]
            }
        ),
        "F-27": FunctionDeclaration(
            name="calculate_nox_mass_total",
            description="Equation F-27: Calculate cumulative NOₓ mass (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "hourly_lb": {
                        "type": "string",
                        "description": "Column name containing hourly NOₓ mass (lb)"
                    },
                    "hours": {
                        "type": "string",
                        "description": "Column name containing operating hours for each period"
                    },
                    "convert_to_tons": {
                        "type": "string",
                        "description": "Convert result to tons (true/false, default true)"
                    }
                },
                "required": ["hourly_lb", "hours"]
            }
        ),
        "F-28": FunctionDeclaration(
            name="calculate_nox_mass_apportioned",
            description="Equation F-28: Calculate apportioned NOₓ mass rate for a unit (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "nox_rate_common_lbhr": {
                        "type": "string",
                        "description": "Column name containing common stack NOₓ rate (lb/hr)"
                    },
                    "heat_input_unit": {
                        "type": "string",
                        "description": "Column name containing unit heat input (MMBtu/hr)"
                    },
                    "heat_input_common": {
                        "type": "string",
                        "description": "Column name containing common stack heat input (MMBtu/hr)"
                    },
                    "time_unit_hr": {
                        "type": "string",
                        "description": "Column name containing unit operating time (hr)"
                    },
                    "time_common_hr": {
                        "type": "string",
                        "description": "Column name containing common stack operating time (hr)"
                    }
                },
                "required": ["nox_rate_common_lbhr", "heat_input_unit", "heat_input_common", "time_unit_hr", "time_common_hr"]
            }
        ),
        "F-31": FunctionDeclaration(
            name="calculate_moisture_from_o2",
            description="Equation F-31: Calculate stack gas moisture from wet and dry O₂ measurements (Appendix F).",
            parameters={
                "type": "object",
                "properties": {
                    "o2_dry_percent": {
                        "type": "string",
                        "description": "Column name containing O₂ concentration on dry basis (%)"
                    },
                    "o2_wet_percent": {
                        "type": "string",
                        "description": "Column name containing O₂ concentration on wet basis (%)"
                    }
                },
                "required": ["o2_dry_percent", "o2_wet_percent"]
            }
        )
}

# Example usage documentation for Gemini API integration:
"""
USAGE GUIDE FOR GEMINI API INTEGRATION
======================================

These tool declarations are formatted for the Google Gemini API function calling feature.
Each function maps to a method in the GHGEmissionsCalculator class.

Example Function Call Handling:
-------------------------------
def handle_function_call(function_call, calculator):
    function_name = function_call.name
    args = function_call.args
    
    # Get the method from calculator
    method = getattr(calculator, function_name)
    
    # Call with unpacked arguments
    result = method(**args)
    
    # Return result to Gemini
    return {
        'function_response': {
            'name': function_name,
            'response': {'result': result}
        }
    }

Equation Reference:
------------------
- Subpart C: Stationary Combustion (Equations C-1a, C-1b, C-2a, C-2c, C-3, C-4, C-5, C-6, C-7, C-8a, C-8b, C-9a, C-9b, C-10, C-11, C-12, C-13, C-14, C-15, C-15a)
- Subpart W: Oil and Gas Operations (Equations W-1A, W-3A, W-5A, W-10A, W-11A, W-14A)
- Subpart AA: Pulp and Paper (Equations AA-3, AA-4, AA-5; Tables AA-1, AA-2)
- Subpart DD: Fluorinated GHGs (Equations DD-1 through DD-5)
- Subpart NN: Natural Gas Suppliers (Equations NN-1 through NN-8)
- Subpart OO: Industrial GHG Suppliers (Equations OO-1 through OO-4)
- Subpart RR: Geologic Sequestration (Equations RR-1 through RR-12)
- Appendix F: Part 75 Core Emissions Calculations (Equations F-1, F-2, F-3, F-4, F-5, F-6, F-7a, F-7b, F-11, F-12, F-13, F-14a, F-14b, F-15, F-16, F-17, F-18, F-19, F-20, F-21, F-22, F-23, F-24, F-24a, F-26a, F-26b, F-27, F-28, F-31)
- Table A-1: Global Warming Potentials for fluorinated GHGs

Return Value Handling:
---------------------
Most functions return float values (metric tons of emissions).
Some functions return tuples (e.g., pneumatic_device_emissions_batch returns (CH4, CO2)).
Array functions may return numpy arrays for batch operations.

All emissions are calculated according to EPA 40 CFR Part 98 regulations.
"""
