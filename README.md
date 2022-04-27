# University of Economics in Poznan classes schedule scrape and upload to existing Google  Calendar

This is a scrapy project

To deploy:

Create a conda environment and run  `pip install -r requirments.txt`

Also you might need: 
```
conda install google-api-python-client
pip install --upgrade google-api-python-client oauth2client
```

First [create a google cloud project](https://developers.google.com/workspace/guides/create-project), and follow the tutorial for enabling the API
You have to authenticate with the Google API, so [download credentials](https://developers.google.com/workspace/guides/create-credentials)  from the Google Developer console, place the file in the working directory, and rename it to `credentials.json` 

Then you can run the scrapy project by typing `scrapy crawl uep-plan` , the browser will open to confirm authentication.
