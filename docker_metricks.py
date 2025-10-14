from prometheus_client import start_http_server, Summary, Enum
import time
import docker

# Создаем экземпляр клиента Docker через метод from_env()
client = docker.from_env()

# Метрика статуса контейнеров
container_status_metric = Enum(
    'container_status',
    'Docker container statuses',
    states=['running', 'exited'],
    labelnames=['name']
    )

def collect_container_metrics():
    containers = client.containers.list(all=True)
    for container in containers:
        name = container.name
        state = container.status
        if state == 'running':
            container_status_metric.labels(name=name).state('running')
        elif state == 'exited':
            container_status_metric.labels(name=name).state('exited')

if __name__ == '__main__':
# Запускаем сервер экспорта метрик на порте 8428 (можно установить любой удобный порт)
    start_http_server(8428)
    
    while True:
        try:
            collect_container_metrics()
        except Exception as e:
            print(f'Ошибка при сборе метрик: {e}')
        
# Обновляем метрики каждые 15 секунд
        time.sleep(15)