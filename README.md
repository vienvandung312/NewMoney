# New Money

<!-- Need to implement -->
[![Build Status](https://travis-ci.org/your-username/your-repo.svg?branch=main)](https://travis-ci.org/your-username/your-repo) [![Coverage Status](https://coveralls.io/repos/github/your-username/your-repo/badge.svg?branch=main)](https://coveralls.io/github/your-username/your-repo?branch=main)


My web application for managing and analyzing investment portfolios, including stocks, gold, cryptocurrencies, and real estate.

## Features
- **Historical Data Tracking:** View historical price data for stocks, gold, crypto, and real estate.
- **Portfolio Simulation:**  Perform "what-if" analysis by simulating portfolio performance based on past investment decisions.
- **A/B Testing:** Compare different investment strategies and analyze their potential outcomes.
- **Secure User Authentication:**  Protect your financial data with secure login and authorization.
- **Data Visualization:**  Clear and informative charts and graphs to visualize portfolio performance and historical trends.

## Tech Stack
- **Front-end:** React
- **Back-end:** Spring Boot. Consider serverless functions (AWS Lambda, etc.) for specific tasks. 
- **Data layer:** 
    1. **Data Ingestion and Data Lake:**
    - APIs to S3: Use a tool like AWS Lambda or a custom ingestion service to pull data from various APIs and store it in S3 as your data lake. Parquet or ORC are good file formats for this purpose.
    - Iceberg and Trino: Iceberg provides schema evolution and table management on top of your data lake, and Trino allows you to query the data using SQL. This is a solid approach for analytical queries.

    2. **Snapshotting from Iceberg:** You can use Trino to query data from Iceberg and insert it into PostgreSQL tables. This provides a snapshot of the data for your application's operational needs. Consider how frequently you need to update these snapshots (e.g., daily, hourly).
    
    3. **Master Data:** Building your master data in PostgreSQL is a reasonable approach, especially if it's related to core entities like users, accounts, or investment instruments. PostgreSQL's relational capabilities and data integrity features are well-suited for this.

    4. **Time-Series Analysis:** TimescaleDB, an extension for PostgreSQL, is a great choice for time-series analysis. You can move the time-series data from your PostgreSQL snapshots into TimescaleDB for optimized time-series queries.

    5. **Application events/logs:** Storing application logs or user activity data using Cassandra. Cassandra excels at high-write throughput and availability, considering using it

    6. **Searching:** Elasticsearch is ideal for full-text search and other search functionalities within your application. You can index relevant data from PostgreSQL or other sources into Elasticsearch

    7. **Warehouse:** ClickHouse is a powerful columnar database well-suited for analytical queries on large datasets. You can use it as your data warehouse, potentially loading data from your S3 data lake (via Iceberg/Trino) or directly from other sources.

    8. **Change Data Capture:** Debezium is an excellent choice for CDC. It can capture changes from your databases (PostgreSQL, MySQL, Cassandra, etc.) and stream them to Kafka or other message brokers. This allows you to propagate changes to other systems in real-time, update search indexes, or trigger other downstream processes.

- **Version Control:** GitHub
- **CI/CD:** Jenkins
---
## Development Phases 
### Phase 1: Data Acquisition and Storage

<input type="checkbox" disabled> Identify Data Sources: Research reliable sources for historical stock, gold, crypto, and real estate data. Consider APIs

<input type="checkbox" disabled> Data Storage: Design your database schema to efficiently store the historical data. Consider time-series databases if you have very high-frequency data

<input type="checkbox" disabled> Data Ingestion Pipeline: Create a process (scripts, serverless functions) to fetch data from your chosen sources and store it in your database. Automate this process to update data regularly (e.g., daily).

### Phase 2: Back-end Development

<input type="checkbox" disabled> API Implementation: Develop your backend API endpoints to provide the data and perform calculations (portfolio simulation, A/B testing).

<input type="checkbox" disabled>Business Logic: Implement the core logic for calculating portfolio performance based on historical data and user inputs (investment amounts, time periods).

<input type="checkbox" disabled>Authentication and Authorization: Secure your API by implementing user authentication (e.g., JWT) and authorization.


### Phase 3: Front-end Development

<input type="checkbox" disabled>UI Design: Design the user interface for displaying historical data, inputting investment scenarios, and visualizing portfolio performance. Consider using a UI library (e.g., Material UI, Ant Design).

<input type="checkbox" disabled>Component Development: Build reusable React/Vue.js components for different parts of your UI.

<input type="checkbox" disabled>API Integration: Connect your frontend to your backend API to fetch and display data and perform calculations.


### Phase 4: CI/CD and Deployment

<input type="checkbox" disabled>Set up CI/CD Pipeline: Use a tool like AWS CodePipeline, GitHub Actions, or GitLab CI/CD to automate building, testing, and deploying your application.

<input type="checkbox" disabled>Automated Testing: Write unit tests and integration tests to ensure code quality and catch bugs early.

<input type="checkbox" disabled>Deployment to AWS: Deploy your application to AWS using services like Elastic Beanstalk, EC2, or serverless technologies like Lambda and API Gateway.

<input type="checkbox" disabled>Database Hosting: Host your database on your cloud provider.

### Phase 5: Scalability and Monitoring

<input type="checkbox" disabled>Scalability Planning: Design your architecture with scalability in mind. Use cloud-native services that can scale automatically (e.g., auto-scaling groups for EC2, serverless functions).

<input type="checkbox" disabled>Monitoring and Logging: Implement monitoring and logging tools (e.g., CloudWatch) to track application performance, identify errors, and ensure availability.

