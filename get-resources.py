#!/usr/bin/env python
#List ARN's for all resources in a given AWS account configured in the Skew Config File.
import skew
from skew.arn import ARN
arn = ARN()
services=arn.service.choices()
services.sort()
print('Enumerating all resources in the following services: ' + ' '.join(services) + '\n')
for service in services:
    #skipping global services because the API endpoint fails due to it being a global service. Bug that needs fixing.
    if service == "iam" or service == "route53":
        print(service)  
        print('Skipping global services')
    else:
        print('******' + service + '******')
        uri = 'arn:aws:' + service + ':*:*:*/*'
        arn = skew.scan(uri)
    for i in arn:
        print(i.arn)