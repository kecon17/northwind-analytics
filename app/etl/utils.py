"""
Utility functions and data mappings for the ETL process.
"""

def map_country_to_region(country: str) -> str:
    """Maps a country to a business region."""
    
    mapping = {
        # North America
        'USA': 'North America',
        'Canada': 'North America',
        'Mexico': 'North America',
        # South America
        'Brazil': 'South America',
        'Argentina': 'South America',
        'Venezuela': 'South America',
        # Europe
        'UK': 'Europe',
        'Germany': 'Europe',
        'France': 'Europe',
        'Spain': 'Europe',
        'Italy': 'Europe',
        'Sweden': 'Europe',
        'Switzerland': 'Europe',
        'Belgium': 'Europe',
        'Austria': 'Europe',
        'Portugal': 'Europe',
        'Poland': 'Europe',
        'Ireland': 'Europe',
        'Finland': 'Europe',
        'Norway': 'Europe',
        'Denmark': 'Europe',
    }
    return mapping.get(country, 'Other')

def map_country_to_iso3(country: str) -> str:
    """Maps a country name to its ISO 3166-1 alpha-3 code."""
    mapping = {
        'Argentina': 'ARG',
        'Austria': 'AUT',
        'Belgium': 'BEL',
        'Brazil': 'BRA',
        'Canada': 'CAN',
        'Denmark': 'DNK',
        'Finland': 'FIN',
        'France': 'FRA',
        'Germany': 'DEU',
        'Ireland': 'IRL',
        'Italy': 'ITA',
        'Mexico': 'MEX',
        'Norway': 'NOR',
        'Poland': 'POL',
        'Portugal': 'PRT',
        'Spain': 'ESP',
        'Sweden': 'SWE',
        'Switzerland': 'CHE',
        'UK': 'GBR',
        'USA': 'USA',
        'Venezuela': 'VEN',
    }
    return mapping.get(country) # Returns None if not found, which is fine