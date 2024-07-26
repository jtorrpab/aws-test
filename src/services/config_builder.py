from uuid import uuid4
from dataclasses import dataclass

@dataclass
class ConfigBuilder():
   '''
   Builder for the distribution configuration
   '''
   
   def get_distribution_params(event):

      default_cache_behavior = event.get('default_cache_behavior')
      DistributionConfig = {
         'CallerReference': str(f"{event.get('origin_domain_name', '')}_{uuid4()}"),
         'Origins': {
            'Items': [
               {
                  'Id': 'origin-1',
                  'DomainName': event.get('origin_domain_name', ''),
                  'OriginPath': event.get('OriginPath', ''),
                  'CustomHeaders': {
                     'Quantity': 0,
                     'Items': event.get('CustomHeaders', [])
                  },
                  'S3OriginConfig': {
                     'OriginAccessIdentity': '',
                  }
               }
            ],
            'Quantity': 1
         },
         'DefaultCacheBehavior': {
            'TargetOriginId': 'origin-1',
            'ForwardedValues': default_cache_behavior.get('ForwardedValues', {
               'QueryString': False,
               'Cookies': {
                  'Forward': 'none'
               }
            }),
            'TrustedSigners': {
               'Enabled': False,
               'Quantity': 0
            },
            'ViewerProtocolPolicy': default_cache_behavior.get('ViewerProtocolPolicy', 'allow-all'),
            'MinTTL': default_cache_behavior.get('MinTTL', 0)
         },
         'Comment': event.get('comment', 'Created by Lambda function'),
         'Enabled': event.get('enabled', True),
         'PriceClass': event.get('PriceClass', 'PriceClass_100')
      }

      return DistributionConfig