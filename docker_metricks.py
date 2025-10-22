from prometheus_client import start_http_server, Summary, Enum, Gauge
import time
import docker

# Создаем экземпляр клиента Docker через метод from_env()
try:
    client = docker.from_env()
except docker.errors.DockerException as e:
    print(f"Ошибка инициализации Docker-клиента: {e}")
    exit(1)

# Метрика статуса контейнеров
container_status_metric = Gauge(
    'container_status_and_tag_images',
    'Docker container statuses and tag',
    labelnames=['name', 'tag', 'state']
    )


def collect_container_metrics():

    try:
        containers = client.containers.list(all=True)
    except docker.errors.APIError as e:
        print(f"Ошибка при перечислении контейнеров: {e}")
        return

    for container in containers:
        try:
            name = container.name
            state = container.status
            # Получим image
            image = container.image.tags[0] if container.image.tags else 'unknown'
            # Отделяем TAG
            image = image.partition(':')
            image_tag = image[2]


            # Удаляем старую метрику перед добавлением новой
            labels_to_remove = {'name': name, 'tag': image_tag}
            existing_labels = list(container_status_metric._metrics.keys())
            for key in existing_labels:
                if key[0] == labels_to_remove['name'] and key[1] == labels_to_remove['tag']:
                    del container_status_metric._metrics[key]
                    break

            # Новая метрика
                        
            ## Установка значения метрики
            if state == 'running':
                value = 10
            elif state == 'exited':
                value = 1
            elif state == 'paused':
                value = 5
            elif state == 'crashed':
                value = 2
            else:
                value = 0

            container_status_metric.labels(name=name, tag=image_tag, state=state).set(value)

        except docker.errors.ImageNotFound as e:
            print(f"Ошибка при обработке изображения контейнера '{name}': {e}")
        except IndexError as e:
            print(f"Ошибка обработки имени образа контейнера '{name}' ({e})")
        except KeyError as e:
            print(f"Отсутствует требуемый ключ в метриках контейнера '{name}' ({e})")
        except Exception as e:
            print(f"Общая ошибка при обработке контейнера '{name}': {e}")

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
