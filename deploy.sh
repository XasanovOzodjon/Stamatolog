#!/bin/bash

# Stamatolog deployment script

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting deployment process...${NC}"

# Update code from repository
echo -e "${YELLOW}Pulling latest code...${NC}"
git pull origin main

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install/Update dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Run migrations
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py migrate --noinput

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput

# Restart Gunicorn
echo -e "${YELLOW}Restarting application server...${NC}"
sudo systemctl restart stamatolog

# Restart Nginx
echo -e "${YELLOW}Restarting Nginx...${NC}"
sudo systemctl restart nginx

echo -e "${GREEN}Deployment completed successfully!${NC}"

# Check service status
echo -e "${YELLOW}Service status:${NC}"
sudo systemctl status stamatolog --no-pager
