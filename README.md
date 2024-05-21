**README File**

**Project Overview**

This project aims to query the Open Exchange (Open Exchange Rates) API for currency rates, transform the data from dollar basis to euro basis, and load it into a PostgreSQL database by date.

**Getting Started**

1. **Clone the repository**: Clone this repository by running the command `git clone https://github.com/athnikas/open-exchange-project.git`.

**Setup Environment**

To set up the environment, follow these steps:

1. **Install dependencies**: Run `pip install -r requirements.txt` to install the required packages.
2. **Spin up PostgreSQL and pgAdmin**: Run `docker-compose up` to start the PostgreSQL and pgAdmin containers.
3. **Find the PostgreSQL IP address**: Use the following command to find the PostgreSQL IP address:
```
docker inspect postgres | grep IPAddress
```
This will output the IP address of the PostgreSQL container. You will need this IP address to access the database from pgAdmin.

5. **Access pgAdmin**: Access pgAdmin at `http://0.0.0.0:8888` with dummy passwords as specified in the `docker-compose.yml` file.
6. **Execute DDLs**: Run the Data Definition Language (DDL) scripts to create the necessary tables in the PostgreSQL database.
7. **Activate virtual environment**: Activate the virtual environment by running `source venv/bin/activate` (or equivalent command for your operating system).
8. **Run the pipeline**: Run `python3 main.py` with the following arguments:
	* `--start_date`: Specify the start date in the format `YYYY-MM-DD`.
	* `--end_date`: Specify the end date in the format `YYYY-MM-DD`.

**Execute.sh and Crontab**

To schedule the pipeline to run automatically, you can add the `execute.sh` script to your system's crontab. Here's how:

1. Make sure you have permission to edit your crontab by running `crontab -e`.
2. Add the following line to schedule the script to run daily at 05:45 AM:
```bash
45 5 * * * /path/to/execute.sh
```
Replace `/path/to/execute.sh` with the actual path to your `execute.sh` script.