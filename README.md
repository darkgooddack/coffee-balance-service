# coffee-balance-service

1. alembic миграции 
2. compose (бд, api)
3. k8s (бд, api)
4. проверить user.registered 
5. проверить api (преобразование токена в user_id)

kubectl apply -f k8s/namespace.yaml

kubectl create secret generic coffee-balance-secrets --from-env-file=.env -n balance-dev

kubectl apply -f k8s/postgres -n balance-dev

kubectl apply -f k8s/api -n balance-dev
