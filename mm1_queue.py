# -*- coding: utf-8 -*-

import numpy as np

def mm1_queue(lambda_, mu=1, total_time=3600):
    if lambda_ == 0:
        return 0
    n = int(np.round((lambda_ / mu) / (1 - (lambda_ / mu))))
    t = 0
    events, n_values = [], []
    breaker = False
    while t < total_time:
        if n == 0:
            arrival_time = np.random.exponential(1 / lambda_)
            t += arrival_time
            n_values.append((n, arrival_time))
            events.append((t, 'arrival'))
            n += 1
        else:
            arrival_time = np.random.exponential(1 / lambda_)
            service_time = np.random.exponential(1 / mu)
            if arrival_time < service_time:
                arrival_times = get_arrival_times(arrival_time, service_time, lambda_)
                for time_ in arrival_times:
                    t += time_
                    n_values.append((n, time_))
                    events.append((t, 'arrival'))
                    n += 1
                    if t > total_time:
                        breaker = True
                        break
                if breaker:
                    break
                delta_t = service_time - sum(arrival_times)
                t += delta_t
                n_values.append((n, delta_t))
                events.append((t, 'departure'))
                n -= 1
            else:
                service_times = get_service_times(arrival_time, service_time, mu, n)
                for time_ in service_times:
                    t += time_
                    n_values.append((n, time_))
                    events.append((t, 'departure'))
                    n -= 1
                    if t > total_time:
                        breaker = True
                        break
                if breaker:
                    break
                delta_t = arrival_time - sum(service_times)
                t += delta_t
                n_values.append((n, delta_t))
                events.append((t, 'arrival'))
                n += 1
    avg_customer = sum([n_values[idx][0] * n_values[idx][1] for idx in range(len(n_values))]) / t
    # total_cost = avg_customer + mu
    return avg_customer

def get_arrival_times(arrival_time, service_time, lambda_):
    arrival_times = [arrival_time]
    while sum(arrival_times) < service_time:
        new_arrival_time = np.random.exponential(1 / lambda_)
        arrival_times.append(new_arrival_time) 
    return arrival_times[:-1]

def get_service_times(arrival_time, service_time, mu, n):
    service_times = [service_time]
    while sum(service_times) < arrival_time:
        new_service_time = np.random.exponential(1 / mu)
        service_times.append(new_service_time)
    if len(service_times[:-1]) <= n:
        output = service_times[:-1]
    else:
        output = service_times[:n]
    return output
