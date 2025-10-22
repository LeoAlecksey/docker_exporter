# docker_exporter# Docker_exporter

Этот проект представляет собой простое приложение мониторинга состояния контейнеров Docker с использованием библиотеки prometheus_client для сбора и экспонирования метрик контейнера в формате Prometheus. Данные метрики позволяют отслеживать состояние каждого контейнера, включая название, образ и статус (running, exited, paused, crashed), что помогает оперативно реагировать на изменения в инфраструктуре.

## Getting started

## Description

Структура метрик
В приложении используются следующие типы метрик:

Gauge — используется для отслеживания текущего значения состояний контейнеров (container_status).
Метрики обновляются автоматически каждые 15 секунд и экспортируются на HTTP-сервер, запущенный на порту 8428.

Значение метрик:

|Status|Value|
|:-:|:-:|
|running|10|
|exited|1|
|paused|5|
|crashed|2|

## Usage

### VMagent & Prometheus config

Используется для сбора и хранения метрик с Docker exportera.

```yml
scrape_configs:
  - job_name: 'docker_exporter'
    static_configs:
      - targets: 
          - <host>:8428
```

### ***Grafana:***

**Пример 1:**

Visualization - stat

`sum(container_status_and_tag_images{instance="<host>:8428", state="running"}) / 10` - количество работающих контейнеров.

**Пример 2:**

Visualization - stat

`container_status_and_tag_images{instance="<host>:8428"}`

Legend - {{name}}:{{tag}}

Type - Instant

Value mapping:

|Condition|Display|text|Color|
|:-:|:-:|:-:|:-:|
|value|10|running|green|
|value|1|exited|red|
|value|5|paused|yellow|
|value|2|crashed|blue|

## Support and author

Alexey Andreev (<Alexey.Andreev@atom.team>)

## License

Read ./LICENSE in this repo.
