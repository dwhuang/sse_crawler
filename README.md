# sse_crawler
A crawler for Shanghai Stock Exchange XBRL data

Data structure (results/data.json):
- (top level): [ **company**, **company**, ... ]
- **company**: { 'id': *stock_id*, 'shortname': *short_company_name*, 'data': **data** }
- **data**: [ **section_data**, **section_data**, ... ]
    - There are 6 sections (see `sections.py`)
- **section_data**: [ **data_field**, **data_field**, ... ]
    - The title for each data_field can be found in `sections.py`
    - Each section has different data fields
    - If data are unavailable for a section, section_data = []
- **data_field**: [ **entry**, **entry**, ... ]
- **entry**: [ *year*, *data_value* ]

Todo:
- CSV output (maybe)
