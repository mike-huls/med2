class DatabaseConnection:
    _pool = []
    _max_pool_size = 10

    def __new__(cls):
        # Return connection if there is one available
        if len(cls._pool) > 0:
            return cls._pool.pop()

        return super(DatabaseConnection, cls).__new__(cls)

    def close(self):
        # Return the connection to the pool
        self._pool.append(self)

    def name(self):
        return self._pool


# Usage
conn1 = DatabaseConnection()
conn2 = DatabaseConnection()

# Simulate closing and reusing a connection
conn1.close()
conn3 = DatabaseConnection()

print(id(conn1))
print(id(conn2))
print(id(conn3))

# Should print True because conn3 reuses the connection returned to the pool by conn1
print(conn3 is conn1)
