<h1 align="center">Welcome to timelimiter </h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />
  <img alt="Python" src="https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue"/>
  <a href="https://github.com/KeyesHsu/timelimiter/blob/main/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://codecov.io/gh/KeyesHsu/timelimiter" > 
    <img alt="codecov" src="https://codecov.io/gh/KeyesHsu/timelimiter/branch/main/graph/badge.svg?token=OV7YT73BHY"/> 
 </a>
</p>


Python time limiter library.

Beyond a certain wait interval, a successful result is unlikely.

##### Resources:
* [Changelog](https://github.com/KeyesHsu/timelimiter/blob/main/CHANGELOG.md)


## Install

```sh
pip install timelimiter
```


## Usage
1. Extend `TimeoutHandler` with `timeout` expressed in seconds。Override `_run` method。`MySQLTimeoutHandler` for example.

```python
from timelimiter.timeout_handler import TimeoutHandler, TimeoutHandlerFactory


class MySQLTimeoutHandler(TimeoutHandler):
    timeout = 0.5

    def __init__(self):
        super(MySQLTimeoutHandler, self).__init__()
        # Some way to get MySQL thread id
        self.thread_id = 1

    def _run(self):
        # Kill MySQL connection
        print(self.thread_id)


class MySQLTimeoutHandlerFactory(TimeoutHandlerFactory):
    def create_handler(self) -> TimeoutHandler:
        return MySQLTimeoutHandler()
```

2. Use `TimeLimiter` to wrap the function。

```python
from timelimiter.event_loop import start_loop
from timelimiter.time_limiter import TimeLimiter

start_loop()
factory = MySQLTimeoutHandlerFactory()

@TimeLimiter(factory)
def foo():
    # Do something
    ...
```

## Configuration
Use environment to set configuration.

| Name                  | Description                         | Default |
|-----------------------|-------------------------------------|---------|
| TIME_LIMITER_CAPACITY | Max capacity for time limiter queue | 100,000 |


## Run tests

```sh
make test
```


## Author

👤 **Keyes Hsu**

* Github: [@KeyesHsu](https://github.com/KeyesHsu)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/KeyesHsu/timelimiter/issues).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2022 [Keyes Hsu](https://github.com/KeyesHsu).<br />
This project is [MIT](https://github.com/KeyesHsu/timelimiter/blob/main/LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
