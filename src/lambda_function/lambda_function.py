import json
import boto3
import logging
from botocore.exceptions import ClientError
from services.config_builder import ConfigBuilder

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

   config_builder = ConfigBuilder
   distribution_config = dict()
   
   logger.info(f'Start execution - {context.function_name}')
   client = boto3.client('cloudfront')

   try:

      distribution_config= event.get('DistributionConfig')

      if not distribution_config:
         distribution_config = config_builder.get_distribution_params(event)

      logger.info(f'Getting distribution configuration - {distribution_config}')
      response = client.create_distribution(
            DistributionConfig=distribution_config
        )
         
      distribution_domain_name = response['Distribution']['DomainName']
      distribution_url = f"https://{distribution_domain_name}"
         
      logger.info(f'Distribution created successfully with URL: {distribution_url}')
      return {
         'statusCode': 200,
         'body': json.dumps({'distribution_url': distribution_url})
      }

   except ClientError as e:
      logger.error(f'Error creating distribution: {e}')
      return {
         'statusCode': 500,
         'body': json.dumps({'error': str(e)})
      }


# 