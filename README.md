# coffee-balance-service

Сервис баланса пользователей. Отвечает за хранение и изменение баланса, взаимодействует с другими сервисами через события.

## Запуск

Перед запуском убедитесь, что **minikube запущен**.

В `Deployment` используется `imagePullPolicy: IfNotPresent`.  
При необходимости можно:
- изменить на `Always`, либо
- загрузить образы в minikube вручную.

```
kubectl apply -f k8s/namespace.yaml
```
```
kubectl create secret generic coffee-balance-secrets \
  --from-env-file=.env \
  -n balance-dev
```
```
kubectl apply -f k8s/postgres -n balance-dev
```
```
kubectl apply -f k8s/api -n balance-dev
```

Убедитесь, что включён minikube tunnel:
```
minikube tunnel
```

## API

Authorization: Bearer <JWT>

### POST /api/v1/balance/top-up

Вход:
```json
{
  "amount": 100
}
```
Выход:
```json
{
  "balance": 300
}
```

![img_1.png](img_1.png)

### GET /api/v1/balance

Authorization: Bearer <JWT>

Выход:
```json
{
  "user_id": "uuid",
  "balance": 300
}
```

![img.png](img.png)

