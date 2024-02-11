include env-vars/.env.prod
export $(shell sed 's/=.*//' env-vars/.env.prod)