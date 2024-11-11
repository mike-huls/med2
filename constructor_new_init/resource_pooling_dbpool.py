class DatabaseConnection:
    _pool = []
    _max_pool_size = 5
    _current_count = 0

    def __new__(cls):
        if cls._pool:
            # Reuse a connection from the pool
            return cls._pool.pop()
        elif cls._current_count < cls._max_pool_size:
            # Create a new connection if the max limit is not reached
            cls._current_count += 1
            return super(DatabaseConnection, cls).__new__(cls)
        else:
            raise Exception("Max pool size reached")

    def close(self):
        if len(self._pool) < self._max_pool_size:
            # Return the connection to the pool if there's space
            self._pool.append(self)
        else:
            # Discard the connection if the pool is full
            self._current_count -= 1


# Usage
connections = []

try:
    for _ in range(7):  # Trying to create more than max_pool_size (5) connections
        connections.append(DatabaseConnection())
except Exception as e:
    print(e)  # Should print "Max pool size reached"

# Simulate closing some connections
connections[0].close()
connections[1].close()

# Should succeed because we've closed 2 connections, making room in the pool
new_conn = DatabaseConnection()

# Check if the new connection is one of the closed ones (reuse from the pool)
print(new_conn is connections[0])  # Should print True
