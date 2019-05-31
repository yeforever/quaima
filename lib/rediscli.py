from redis import StrictRedis, ConnectionPool

# 使用默认方式连接到数据库
# 为和系统组区分，使用 最后一个 15
pool = ConnectionPool(host='192.168.0.106', db=15)
redis_cli = StrictRedis(connection_pool=pool)

