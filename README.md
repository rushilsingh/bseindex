
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/48bf5d4bd08444fa917f278e6cd2193d)](https://app.codacy.com/app/rushilsingh/bseindex?utm_source=github.com&utm_medium=referral&utm_content=rushilsingh/bseindex&utm_campaign=Badge_Grade_Dashboard)

This Cherrpy python web application does the following things:
    - Dowloads the latest published Equity bhavcopy data 
    - Extracts and parses the CSV file, and writes the data into Redis.
    - Lists top 10 stock entries from the Redis DB (based on percentage increase from open to close)
    - Facilitates search by name for all the stocks in the Bhavcopy data.

Hosted at:
<https://bhavcopyapp.herokuapp.com/>
