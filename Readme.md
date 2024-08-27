# SMS Simulation Project

Author: Nikson Panigrahi

## Introduction

Hello, my initial plan was to use Python scripts to simulate the process. However, I decided to take it a step further, approaching it as I would in a production environment. To achieve this, I implemented RabbitMQ, Docker, and Redis. Each sender instance runs in its own Docker container, ensuring scalability and abstraction.

This project simulates sending a large number of SMS alerts, similar to an emergency alert service. The simulation consists of three main components:

1. **Producer**: Generates a configurable number of messages to random phone numbers.
2. **Senders**: Processes and simulates the sending of SMS messages.
3. **Monitor**: Tracks and reports the progress, including the number of messages sent, failed, and the average time per message.

The project leverages Docker, RabbitMQ, Redis, and Python to create a scalable and testable environment.

## Usage

### Running the Project

To manage and run the various components of the project, you can use the `Makefile` provided.

1. **Set the .env File:**
    Set the appropriate config params in .env file like:
    ```
    # Producer Configuration
    MESSAGE_COUNT=1000

    # Default Sender Configuration
    SENDER_MEAN_TIME=0.1
    SENDER_FAILURE_RATE=0.2

    # Monitor Configuration
    MONITOR_INTERVAL=5
    ```

2. **Start RabbitMQ and Redis:**
   ```bash
   make run-services
   ```

3. **Run Senders (Specify Number of Instances):**
    ```bash
    make run-senders SENDER_COUNT=3
    ```

    **Run Senders (With Custom Params):**
    ```bash
    make run-sender MEAN_TIME=2.0 FAIL_RATE=0.1
    ```

4. **Run Producer:**
    ```bash
    make run-producer
    ```

5. **Run Monitor:**
    ```bash
    make run-monitor
    ```

6. **Stop all Containers:**
    ```bash
    make stop
    ```

7. **Bring Down All Containers, Networks, and Volumes:**
    ```bash
    make down
    ```

## Design Diagram (Flow Structure)
Below is a basic flow structure of the SMS Simulation project:

```
+----------------+          +--------------+
|                |          |              |
|   Producer     +--------->|   RabbitMQ   |
|  (Generates    |          |   (Queue)    |
|   Messages)    |          |              |
+----------------+          +-------+------+
                                     |
                                     |
                                     v
                              +------+-------+
                              |              |
                              |   Senders    |---+
                              | (Processes   |   |
                              |  Messages)   |   |
                              +------+-------+   |
                                     |           |
                                     v           v
                              +------+-------+   |
                              |              |   |
                              |   Redis      |<--+
                              | (Stores      |
                              |  Metrics)    |
                              +------+-------+
                                     |
                                     v
                              +------+-------+
                              |              |
                              |   Monitor    |
                              | (Tracks &    |
                              |  Reports)    |
                              +--------------+

```
## Testing

### Running Tests

The project includes unit and functional tests to ensure the correct behavior of each component.

1. **Run Tests:**
    ```bash
    make test
    ```
2. **Run Test Coverage:**
    ```bash
    make coverage
    ```
3. **Clean Up Test Artifacts:**
    ```bash
    make clean
    ```

### Test Coverage Overview
    ```bash
        Name                     Stmts   Miss  Cover   Missing
        ------------------------------------------------------
        monitor.py                  21      2    90%   27-28
        producer.py                 24      2    92%   43-44
        sender.py                   39     11    72%   37, 40-56, 59
        tests/__init__.py            0      0   100%
        tests/test_monitor.py       17      0   100%
        tests/test_producer.py      25      0   100%
        tests/test_sender.py        34      0   100%
        ------------------------------------------------------
        TOTAL                      160     15    91%
    ```


## Next Steps:
I considered some additional steps, but they seemed beyond the scope of this project:

- Implementing Grafana and Prometheus to create a monitoring dashboard.
- Using Kubernetes for automatic resource allocation and scaling.
- Expanding test coverage to include functional tests.
