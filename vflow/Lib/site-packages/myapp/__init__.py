'''
#
# normal redis
#
#redis://:password@hostname:port/db_number
app.conf.broker_url = 'redis://localhost:6379/0'

#
# sentinel
#
app.conf.broker_url = 'sentinel://localhost:26379;sentinel://localhost:26380;sentinel://localhost:26381'
app.conf.broker_transport_options = { 'master_name': "cluster1" }


#
# when worker accepts a task
#
app.conf.broker_transport_options = {'visibility_timeout': 3600}  # 1 hour



#
# results
#
app.conf.result_backend = 'redis://localhost:6379/0'
app.conf.result_backend_transport_options = {'master_name': "mymaster"}    # sentinel
'''