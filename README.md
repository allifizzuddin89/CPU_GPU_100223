# Brief introduction
- Scraping for consumer motherboards, cpu, gpu list from known manufacturers.
- Extracting related data regarding cpu details, gpu details, motherboard's details.
- You may view the scraped data in the generated csv file in [directory](https://github.com/allifizzuddin89/CPU_GPU_100223/tree/master/cpu_gpu_mobo_spider/cpu_gpu_mobo_spider/spiders)

# Result
- See sample one of the generated result in csv file in [CSV FILE](https://github.com/allifizzuddin89/CPU_GPU_100223/blob/master/cpu_gpu_mobo_spider/cpu_gpu_mobo_spider/spiders/ASROCK_mobo_1150.csv)

## Run
- The working directory is CPU_GPU_100223/tree/master/cpu_gpu_mobo_spider/cpu_gpu_mobo_spider/spiders
- Activate the installed working environment
- Run the main.py in the working directory.
- Run <scrapy runspider main.py> in the terminal in the working directory
  OR simply run <scrapy crawl main.py> or <scrapy runspider whateverworkspacedirectory/main.py>
- Csv will be generated, already included via feed exporter

### Install environment
- Refer [CONDA Environment Installation](https://docs.anaconda.com/anaconda/install/)
 
### HOW-TO
- Clone the repository
```bash  
  git clone https://github.com/allifizzuddin89/CPU_GPU_100223.git 
```
- Create working environment (skip if already have any working environment)
```bash
  conda create --name scraping_env -c conda-forge python=3.9.13 scrapy=2.7.1
```
- Activate the working environment
```bash
  conda activate scraping_env
```
 - Run the spider
 - Every manufacturer's has their own python(spider) file.
 - Example for asrock motherboards:
 ```bash
    scrapy runspider CPU_GPU_100223/blob/master/cpu_gpu_mobo_spider/cpu_gpu_mobo_spider/spiders/asrock_mobo.py
 ```

## Troubleshoot / guide
- Error might happened due to the payload already expired or request being rejected by the server or the url/api address simply has been changed by the administrator.
  - Please bear in mind, the web owner might change the web's code dynamically anytime. Therefore this web scraping code might not work.
- Solution: 
  1. Include HTTP headers for request.
  2. Using rotating proxy, google it!
  
## DISCLAIMER
- This work only meant for educational, research and proof of work purpose only. 
- I will not responsible for any illegal activities.
- Every action is on your own responsibilities.
- Please respect robots.txt.
- Please don't hog down with relentless request, set the interval in the settings.py, under AUTOTHROTTLE. Scrapy made it easy!
