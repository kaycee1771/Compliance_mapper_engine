#!/bin/bash
tar -czf /backups/daily_$(date +%F).tar.gz /var/www /etc/nginx /etc/mysql
aws s3 cp /backups/daily_$(date +%F).tar.gz s3://company-backups/