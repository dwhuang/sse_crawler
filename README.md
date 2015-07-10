# sse_crawler
A crawler for Shanghai Stock Exchange XBRL data

JSON structure (results/data.json):
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

The csv files in `results/` are extracted from the JSON file by `gencsv.py`

Related URLs
- http://listxbrl.sse.com.cn/companyInfo/toCompanyInfo.do?stock_id=600020&report_year=2014&report_period_id=5000
- http://www.sse.com.cn/disclosure/listedinfo/regular/
